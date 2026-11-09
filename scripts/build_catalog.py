#!/usr/bin/env python3
"""Build the public catalog from every branches/*.json file. Standard library only."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit

HEADERS = ['Product Code', 'Product Name', 'Color / Variant', 'Price (Ks)', 'Stock']
MAX_ROWS = 20000
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg'}

class InventoryError(ValueError):
    pass

def text(value):
    return unicodedata.normalize('NFKC', str('' if value is None else value)).strip()

def variant_id(color):
    return text(color).casefold()

def read_inventory(path):
    """Read the same five-field JSON inventory format for every branch."""
    if path.suffix.lower() != '.json':
        raise InventoryError('Use a generated branch JSON file from the separate Mandalay Inventory Importer.')
    if path.stat().st_size > 20 * 1024 * 1024:
        raise InventoryError('Imported inventory exceeds 20 MB.')
    try:
        imported=json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise InventoryError('Cannot read imported inventory JSON.') from exc
    # Accept prior six-field files so existing user inventories need no rewrite.
    legacy=HEADERS[:2]+['Category']+HEADERS[2:]
    if not isinstance(imported,dict) or imported.get('headers') not in (HEADERS,legacy):
        raise InventoryError('Imported inventory must use the five standard headers.')
    rows=imported.get('rows')
    if not isinstance(rows,list) or len(rows)>MAX_ROWS:
        raise InventoryError('Invalid imported inventory rows.')
    if any(not isinstance(row,list) or len(row)!=len(imported['headers']) or any(type(v) not in (str,int,float) for v in row) for row in rows):
        raise InventoryError('Each imported inventory row must have five text/number values.')
    if imported['headers']==legacy: rows=[row[:2]+row[3:] for row in rows]
    return list(enumerate(rows,2))


def whole_number(value,field,rownum):
    value=text(value)
    if not value:
        raise InventoryError(f'Row {rownum}: {field} is blank. Enter a number; use 0 for no stock.')
    value=''.join(str(unicodedata.digit(c)) if c.isdigit() else c for c in value).replace(',','')
    # Excel can serialize integral numeric values as 12.0 or scientific notation.
    from decimal import Decimal, InvalidOperation
    try:
        number=Decimal(value)
        if not number.is_finite() or number < 0 or number != number.to_integral_value() or number > 9007199254740991:
            raise InvalidOperation
        return int(number)
    except (InvalidOperation,ValueError):
        raise InventoryError(f'Row {rownum}: {field} must be a non-negative whole number, without currency symbols.')

def branch_identity(path):
    ident=re.sub(r'[^a-z0-9]+','-',path.stem.lower()).strip('-')
    if not ident or len(ident)>60:
        raise InventoryError('Use a simple branch filename such as branch-6.json.')
    label=' '.join(part.capitalize() for part in ident.split('-'))
    return ident,label

def natural_key(path):
    return [int(p) if p.isdigit() else p for p in re.split(r'(\d+)',path.name.lower())]

def validate_url(value,field):
    if not value:return
    allowed=('https://','viber://') if field=='viberUrl' else ('https://',)
    if not isinstance(value,str) or not value.startswith(allowed):
        raise InventoryError(f'{field}: use a full https:// link (or viber:// for Viber).')

def product_photos(root):
    """One shared photo per product code, independent of inventory and variants."""
    folder=root/'dist/assets/products'
    folder.mkdir(parents=True,exist_ok=True)
    photos={}
    # The dedicated folder takes priority; also accept code photos directly in assets.
    for directory in [folder,root/'dist/assets']:
        local={}
        for photo in sorted(directory.iterdir()):
            if not photo.is_file() or photo.suffix.lower() not in PHOTO_EXTENSIONS:continue
            code=photo.stem.upper()
            if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,39}',code):continue
            if code in local:
                raise InventoryError(f'Multiple product photos for {code}: {local[code].name}, {photo.name}. Keep one file per product code in {directory.relative_to(root)}.')
            local[code]=photo
        for code,photo in local.items():photos.setdefault(code,photo)
    return photos

def assign_product_photos(root,products,photos):
    if not (root/'dist/assets/product-placeholder.svg').is_file():
        raise InventoryError('Missing placeholder image: dist/assets/product-placeholder.svg')
    for product in products.values():
        photo=photos.get(product['id'])
        if photo:
            # Updating the file also changes the URL, so browsers load its new contents.
            version=hashlib.sha256(photo.read_bytes()).hexdigest()[:12]
            image=photo.relative_to(root/'dist').as_posix()+'?v='+version
            for variant in product['variants']:variant['image']=image
        else:
            for variant in product['variants']:
                variant['image']='assets/product-placeholder.svg'

def build_catalog(root):
    source=root/'data/products.json'
    base=json.loads(source.read_text(encoding='utf-8'))
    products={p['id']:copy.deepcopy(p) for p in base}
    photos=product_photos(root)
    if len(products)!=len(base): raise InventoryError('Duplicate product codes in data/products.json.')
    for p in products.values():
        if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,39}',p['id']):
            raise InventoryError('Invalid master product code: '+p['id'])
        p.pop('category',None)
        ids=[v['id'] for v in p['variants']]
        if len(ids)!=len(set(ids)): raise InventoryError('Duplicate master variant: '+p['id'])
    files=sorted((p for p in (root/'branches').iterdir() if p.is_file() and not p.name.startswith(('~$','.'))),key=natural_key)
    unsupported=[p.name for p in files if p.suffix.lower() in ('.xlsx','.xls','.xlsm','.csv','.numbers')]
    if unsupported: raise InventoryError('Remove old branch spreadsheets after migrating to JSON: '+', '.join(unsupported))
    files=[p for p in files if p.suffix.lower()=='.json']
    if not files: raise InventoryError('No branch .json files found in branches/.')
    branches=[]; used_ids=set(); warnings=[]
    about=json.loads((root/'data/about.json').read_text(encoding='utf-8'))
    for field in ['viberUrl','facebookUrl']:
        validate_url(about.get(field,''),field)
    for contacts in about.get('branches',{}).values():
        for field in ['viberUrl','facebookUrl','mapUrl']:
            validate_url(contacts.get(field,''),field)
    for file in files:
        try:
            ident,label=branch_identity(file)
            if ident in used_ids: raise InventoryError('Another filename produces the same branch ID: '+ident)
            used_ids.add(ident); inventory=[]; seen=set()
            for rownum,row in read_inventory(file):
                code,product_name,color=[text(v) for v in row[:3]]
                if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,39}',code):
                    raise InventoryError(f'Row {rownum}: invalid Product Code. Use uppercase letters, numbers, hyphens, dots or underscores (max 40).')
                if not product_name or len(product_name)>160: raise InventoryError(f'Row {rownum}: Product Name is required (max 160 characters).')
                if not color or len(color)>60: raise InventoryError(f'Row {rownum}: Color / Variant is required (max 60 characters). Use Standard if not applicable.')
                vid=variant_id(color);key=(code,vid)
                if key in seen: raise InventoryError(f'Row {rownum}: duplicate {code} / {color}. Use one row for each product and variant.')
                seen.add(key)
                price=whole_number(row[3],'Price (Ks)',rownum);stock=whole_number(row[4],'Stock',rownum)
                if stock == 0: continue
                if code not in products:
                    products[code]={'id':code,'name':{'en':product_name, **({'mm':product_name} if any('\u1000' <= c <= '\u109f' for c in product_name) else {})},'description':{'en':''},'variants':[]}
                p=products[code]
                if product_name not in p['name'].values():
                    warnings.append(f'{file.name} row {rownum}: keeping shared product name for {code}: {p["name"].get("en",code)}')
                if not any(v['id']==vid for v in p['variants']):
                    p['variants'].append({'id':vid,'color':color})
                inventory.append({'productId':code,'variantId':vid,'price':price,'stock':stock})
            contacts=about.get('branches',{}).get(ident,{})
            branches.append({'id':ident,'name':label,'source':file.name,'inventory':inventory,'hasInventory':bool(inventory),'contact':{k:contacts.get(k,'') for k in ['address','phone','viberUrl','facebookUrl','mapUrl','hours']}})
        except InventoryError as exc:
            raise InventoryError(f'{file.name}: {exc}') from exc
    assign_product_photos(root,products,photos)
    return {'schemaVersion':1,'currency':'MMK','products':list(products.values()),'branches':branches,'about':{k:v for k,v in about.items() if k!='branches'}},warnings

def publish(root,catalog):
    dest=root/'dist/catalog.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    # Validate every file before replacing the only data file read by visitors.
    fd,temp=tempfile.mkstemp(prefix='.catalog-',suffix='.json',dir=dest.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(catalog,f,ensure_ascii=False,indent=2); f.write('\n')
        os.replace(temp,dest)
    finally:
        if os.path.exists(temp):os.unlink(temp)

def live_handler(root):
    """Refresh the local preview from branch files whenever its catalog is read."""
    class PreviewHandler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(root/'dist'),**kwargs)

        def do_GET(self):
            if urlsplit(self.path).path == '/catalog.json':
                try:
                    catalog,_=build_catalog(root)
                    publish(root,catalog)
                except (InventoryError,OSError,ValueError) as exc:
                    print(f'Local preview update stopped: {exc}',file=sys.stderr,flush=True)
                    self.send_error(422,str(exc))
                    return
            super().do_GET()

        def end_headers(self):
            self.send_header('Cache-Control','no-store')
            super().end_headers()

    return PreviewHandler

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check',action='store_true',help='Validate without changing the generated catalog.')
    parser.add_argument('--serve',action='store_true',help='Build and start a local preview; refresh rebuilds branch changes.')
    parser.add_argument('--port',type=int,default=8000,help='Local preview port (default 8000).')
    args=parser.parse_args()
    if args.check and args.serve:parser.error('--check and --serve cannot be combined')
    try:
        catalog,warnings=build_catalog(args.root.resolve())
        if not args.check:publish(args.root,catalog)
        report=['Branch inventory validation','', '| Branch | Product variants | Stock units |','|---|---:|---:|']
        for b in catalog['branches']:
            report.append(f'| {b["name"]} | {len(b["inventory"])} | {sum(i["stock"] for i in b["inventory"])} |')
        if warnings: report+=['','Name differences (shared names retained):']+warnings
        print('\n'.join(report))
        if os.getenv('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f:f.write('\n'.join(report)+'\n')
        if args.serve:
            with HTTPServer(('127.0.0.1',args.port),live_handler(args.root.resolve())) as server:
                print(f'Local website: http://127.0.0.1:{server.server_port}/ — refresh after changing a branch JSON. Control+C stops it.',flush=True)
                try:server.serve_forever()
                except KeyboardInterrupt:pass
        return 0
    except (InventoryError,OSError,ValueError) as exc:
        print(f'Inventory update stopped: {exc}',file=sys.stderr)
        print('Fix the named inventory JSON file and upload it again. The live website is not changed by a failed build.',file=sys.stderr)
        return 1

if __name__=='__main__':sys.exit(main())
