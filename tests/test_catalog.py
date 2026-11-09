import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import threading
from urllib.request import urlopen
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/build_catalog.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        (self.root/'data').mkdir();(self.root/'branches').mkdir();(self.root/'dist/assets').mkdir(parents=True)
        for filename in ['products.json','about.json']:
            shutil.copy2(ROOT/'tests/fixtures'/filename,self.root/'data'/filename)
        shutil.copy2(ROOT/'dist/assets/product-placeholder.svg',self.root/'dist/assets/product-placeholder.svg')
        shutil.copy2(ROOT/'tests/fixtures/branch-sample.json',self.root/'branches/branch 1.json')
        for i in range(2,6):shutil.copy2(ROOT/'tests/fixtures/empty-branch.json',self.root/f'branches/branch {i}.json')
        (self.root/'dist/catalog.json').write_text('{"previous":true}')
    def tearDown(self):self.temp.cleanup()
    def build(self):return builder.build_catalog(self.root)[0]
    def test_branch_files_and_five_branches(self):
        catalog=self.build();self.assertEqual([b['name'] for b in catalog['branches']],[f'Branch {i}' for i in range(1,6)])
        self.assertEqual(len(catalog['branches'][0]['inventory']),11)
        self.assertFalse(catalog['branches'][1]['hasInventory'])
    def test_new_file_discovers_branch_and_contact_card(self):
        shutil.copy2(ROOT/'tests/fixtures/empty-branch.json',self.root/'branches/branch 6.json')
        branches=self.build()['branches'];self.assertEqual(branches[-1]['id'],'branch-6');self.assertEqual(branches[-1]['name'],'Branch 6');self.assertEqual(branches[-1]['contact']['phone'],'')
    def test_two_branches_keep_different_price_and_stock(self):
        real=builder.read_inventory
        def reader(path):
            if path.name=='branch 2.json':return [(2,['MB-001','Mountain Bike X1','Red','380000','3'])]
            return real(path)
        with patch.object(builder,'read_inventory',side_effect=reader):catalog=self.build()
        first=catalog['branches'][0]['inventory'][0];second=catalog['branches'][1]['inventory'][0]
        self.assertEqual(first['price'],250);self.assertEqual(second['price'],380000);self.assertEqual(second['stock'],3)
    def test_new_products_and_variants_get_shared_metadata(self):
        real=builder.read_inventory
        def reader(path):
            if path.name=='branch 2.json':return [(2,['NEW-001','Basket','Standard','12000','7']),(3,['MB-001','Mountain Bike X1','Green','300000','2'])]
            return real(path)
        with patch.object(builder,'read_inventory',side_effect=reader):catalog=self.build()
        p=next(p for p in catalog['products'] if p['id']=='NEW-001');self.assertEqual(p['variants'][0]['image'],'assets/product-placeholder.svg');self.assertEqual(p['name']['en'],'Basket')
        self.assertTrue(any(v['id']=='green' for p in catalog['products'] if p['id']=='MB-001' for v in p['variants']))
    def test_invalid_input_leaves_generated_catalog_unchanged(self):
        original=(self.root/'dist/catalog.json').read_bytes();real=builder.read_inventory
        def reader(path):
            return [(2,['MB-001','Mountain Bike X1','Red','','3'])] if path.name=='branch 2.json' else real(path)
        with patch.object(builder,'read_inventory',side_effect=reader),self.assertRaisesRegex(builder.InventoryError,'branch 2.json.*Price.*blank'):
            catalog=self.build();builder.publish(self.root,catalog)
        self.assertEqual((self.root/'dist/catalog.json').read_bytes(),original)
    def test_duplicates_are_rejected(self):
        real=builder.read_inventory
        def reader(path):
            return [(2,['MB-001','Mountain Bike X1','Red','100','3']),(3,['MB-001','Mountain Bike X1','red','120','4'])] if path.name=='branch 2.json' else real(path)
        with patch.object(builder,'read_inventory',side_effect=reader),self.assertRaisesRegex(builder.InventoryError,'duplicate'):self.build()
    def test_removing_file_removes_branch(self):
        (self.root/'branches/branch 5.json').unlink();self.assertEqual(len(self.build()['branches']),4)
    def test_blank_and_zero_are_different(self):
        self.assertEqual(builder.whole_number('0','Stock',2),0)
        for value in ['', '-1','1.5','abc','NaN','Infinity']:
            with self.assertRaises(builder.InventoryError):builder.whole_number(value,'Stock',2)
        self.assertEqual(builder.whole_number('၁၂၃,၀၀၀','Price',2),123000)
    def test_conflicting_branch_filename_is_rejected(self):
        shutil.copy2(ROOT/'tests/fixtures/empty-branch.json',self.root/'branches/branch-1.json')
        with self.assertRaisesRegex(builder.InventoryError,'same branch ID'):self.build()
    def test_old_excel_inventory_rejected(self):
        (self.root/'branches/branch 2.xlsx').write_bytes(b'old format')
        with self.assertRaisesRegex(builder.InventoryError,'Remove old branch spreadsheets'):
            self.build()

    def test_json_invalid_row_rejected(self):
        path=self.root/'branches/branch 2.json'
        path.write_text(json.dumps({'headers':builder.HEADERS,'rows':[['NH001','Item','Standard',100,True]]}))
        with self.assertRaises(builder.InventoryError):builder.read_inventory(path)

    def test_local_preview_refresh_rebuilds_edited_branch_3(self):
        server=builder.HTTPServer(('127.0.0.1',0),builder.live_handler(self.root))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        address=f'http://127.0.0.1:{server.server_port}/catalog.json'
        try:
            with urlopen(address) as response:
                self.assertEqual(json.load(response)['branches'][2]['inventory'],[])
            path=self.root/'branches/branch 3.json'
            path.write_text(json.dumps({'headers':builder.HEADERS,'rows':[['NEW-003','Branch 3 item','Standard',25000,4]]}))
            with urlopen(address) as response:
                branch=json.load(response)['branches'][2]
                self.assertEqual(branch['id'],'branch-3')
                self.assertEqual(branch['inventory'],[{'productId':'NEW-003','variantId':'standard','price':25000,'stock':4}])
            path.write_text(json.dumps({'headers':builder.HEADERS,'rows':[['NEW-003','Branch 3 item','Standard',26000,0]]}))
            with urlopen(address) as response:
                self.assertEqual(json.load(response)['branches'][2]['inventory'],[])
        finally:
            server.shutdown();server.server_close();thread.join()

    def test_dangerous_contact_url_is_rejected(self):
        about=json.loads((self.root/'data/about.json').read_text());about['facebookUrl']='javascript:alert(1)';(self.root/'data/about.json').write_text(json.dumps(about))
        with self.assertRaisesRegex(builder.InventoryError,'https'):self.build()
    def test_zero_stock_is_excluded_and_missing_rows_not_copied(self):
        real=builder.read_inventory
        with patch.object(builder,'read_inventory',side_effect=lambda p: [(2,['MB-001','Mountain Bike X1','Red','200000','0'])] if p.name=='branch 2.json' else real(p)):
            catalog=self.build()
        self.assertEqual(catalog['branches'][1]['inventory'],[])
    def test_legacy_inventory_category_is_ignored(self):
        path=self.root/'branches/branch 2.json'
        path.write_text(json.dumps({'headers':builder.HEADERS[:2]+['Category']+builder.HEADERS[2:],
            'rows':[['NEW-007','Example item','Any old category','Standard',100,2]]}))
        catalog=self.build()
        self.assertEqual(catalog['branches'][1]['inventory'][0]['stock'],2)
        self.assertNotIn('category',next(p for p in catalog['products'] if p['id']=='NEW-007'))

    def put_photo(self,name='MB-011.jpg'):
        folder=self.root/'dist/assets/products';folder.mkdir(exist_ok=True)
        path=folder/name
        shutil.copy2(ROOT/'tests/fixtures/product-photo.jpg',path)
        return path

    def test_new_imported_product_gets_photo_by_code(self):
        self.put_photo();real=builder.read_inventory
        with patch.object(builder,'read_inventory',side_effect=lambda p: [(2,['MB-011','Rocking Chair','Brown','290','10'])] if p.name=='branch 2.json' else real(p)):
            catalog=self.build()
        p=next(p for p in catalog['products'] if p['id']=='MB-011')
        self.assertTrue(p['variants'][0]['image'].startswith('assets/products/MB-011.jpg?v='))
        self.assertEqual(catalog['branches'][1]['inventory'][0]['price'],290)

    def test_no_matching_photo_uses_placeholder_ignoring_manual_path(self):
        source=self.root/'data/products.json';products=json.loads(source.read_text())
        products[0]['variants'][0]['image']='assets/old-photo-does-not-exist.jpg'
        source.write_text(json.dumps(products))
        p=next(p for p in self.build()['products'] if p['id']=='MB-001')
        self.assertTrue(all(v['image']=='assets/product-placeholder.svg' for v in p['variants']))

    def test_photo_directly_in_assets_is_detected(self):
        shutil.copy2(ROOT/'tests/fixtures/product-photo.jpg',self.root/'dist/assets/MB-001.jpg')
        p=next(p for p in self.build()['products'] if p['id']=='MB-001')
        self.assertTrue(all(v['image'].startswith('assets/MB-001.jpg?v=') for v in p['variants']))

    def test_case_insensitive_photo_applies_to_all_variants(self):
        self.put_photo('mb-001.JPG')
        p=next(p for p in self.build()['products'] if p['id']=='MB-001')
        self.assertTrue(all(v['image'].startswith('assets/products/mb-001.JPG?v=') for v in p['variants']))

    def test_photo_add_replace_remove_updates_catalog(self):
        def image():return next(p for p in self.build()['products'] if p['id']=='MB-001')['variants'][0]['image']
        self.assertEqual(image(),'assets/product-placeholder.svg')
        photo=self.put_photo('MB-001.jpg');first=image()
        photo.write_bytes(photo.read_bytes()+b'\n');self.assertNotEqual(image(),first)
        photo.unlink();self.assertEqual(image(),'assets/product-placeholder.svg')

    def test_duplicate_photo_formats_fail_without_overwriting_catalog(self):
        self.put_photo('MB-001.jpg');self.put_photo('MB-001.png')
        original=(self.root/'dist/catalog.json').read_bytes()
        with self.assertRaisesRegex(builder.InventoryError,'Multiple product photos for MB-001'):
            catalog=self.build();builder.publish(self.root,catalog)
        self.assertEqual((self.root/'dist/catalog.json').read_bytes(),original)

if __name__=='__main__':unittest.main()
