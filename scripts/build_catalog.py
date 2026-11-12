#!/usr/bin/env python3
"""Build the public catalog from every branches/*.json file. With optional HEIC conversion."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import shutil
import unicodedata

HEADERS = ['ID', 'Name', 'Category', 'Price', 'Stock']
MAX_ROWS = 20000

class InventoryError(ValueError):
    pass

def text(value):
    return unicodedata.normalize('NFKC', str('' if value is None else value)).strip()

def variant_id(color):
    return text(color).casefold()

def read_inventory(path,category_translations=None):
    """Read the same five-field JSON inventory format for every branch."""
    if path.suffix.lower() != '.json':
        raise InventoryError('Use a generated branch JSON file from the separate Mandalay Inventory Importer.')
    if path.stat().st_size > 20 * 1024 * 1024:
        raise InventoryError('Imported inventory exceeds 20 MB.')
    try:
        imported=json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise InventoryError('Cannot read imported inventory JSON.') from exc
    if not isinstance(imported,dict):raise InventoryError('Expected inventory JSON object.')
    incoming=imported.get('categoryTranslations',{})
    if not isinstance(incoming,dict):raise InventoryError('categoryTranslations must be an object.')
    for category,labels in incoming.items():
        if not isinstance(category,str) or len(category)>120 or not isinstance(labels,dict):
            raise InventoryError('Invalid category translation entry.')
        if any(lang not in ('mm','en','zh') or not isinstance(label,str) or not label.strip() or len(label)>120 for lang,label in labels.items()):
            raise InventoryError('Category translations must use nonempty mm/en/zh text.')
        if category_translations is not None:
            existing=category_translations.setdefault(category,{})
            for lang,label in labels.items():
                if lang in existing and existing[lang]!=label:raise InventoryError(f'Conflicting {lang} translation for category {category}.')
                existing[lang]=label
    headers=imported.get('headers')
    rows=imported.get('rows')
    layouts=[
        HEADERS,
        ['Product Code','Product Name','Color / Variant','Price (Ks)','Stock'],
        ['Product Code','Product Name','Category','Color / Variant','Price (Ks)','Stock'],
    ]
    if headers not in layouts:raise InventoryError('Expected headers: ID, Name, Category, Price, Stock.')
    if not isinstance(rows,list) or len(rows)>MAX_ROWS:raise InventoryError('Invalid inventory rows.')
    if any(not isinstance(row,list) or len(row)!=len(headers) or any(type(v) not in (str,int,float) for v in row) for row in rows):
        raise InventoryError('Each inventory row must match its headers.')
    normalized=[]
    for row in rows:
        if headers==HEADERS: normalized.append(row[:3]+['Standard']+row[3:])
        elif len(headers)==5: normalized.append(row[:2]+['']+row[2:])
        else:normalized.append(row)
    return list(enumerate(normalized,2))



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

def branch_photos(root,branch_id):
    # Sources stay outside dist; the build copies/converts only public product images.
    directory=root/'Products'/branch_id.replace('-','')
    destination=root/'dist/Products'/branch_id.replace('-','')
    if destination.exists():shutil.rmtree(destination)
    destination.mkdir(parents=True,exist_ok=True)
    if not directory.exists():return {}
    result={}
    allowed={'.jpg','.jpeg','.png','.webp','.avif','.gif','.heic','.heif'}
    for photo in sorted(directory.iterdir()):
        if not photo.is_file() or photo.suffix.lower() not in allowed:continue
        code=photo.stem.upper()
        if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,39}',code):raise InventoryError(f'Photo name must be a product ID: {photo.name}')
        if code in result:raise InventoryError(f'Multiple images for {code} in {directory}. Keep one image per product ID.')
        if photo.suffix.lower() in {'.heic','.heif'}:
            try:
                from PIL import Image,ImageOps
                from pillow_heif import register_heif_opener
                register_heif_opener()
            except ImportError as exc:raise InventoryError('HEIC support requires: python3 -m pip install -r requirements.txt') from exc
            target=destination/(code+'.jpg')
            try:
                with Image.open(photo) as image:
                    image=ImageOps.exif_transpose(image).convert('RGB')
                    image.thumbnail((1800,1800))
                    image.save(target,'JPEG',quality=88)
            except Exception as exc:raise InventoryError(f'Cannot convert HEIC image {photo.name}: {exc}') from exc
        else:
            target=destination/(code+photo.suffix.lower())
            shutil.copyfile(photo,target)
        version=hashlib.sha256(target.read_bytes()).hexdigest()[:12]
        result[code]=target.relative_to(root/'dist').as_posix()+'?v='+version
    return result

def build_catalog(root):
    source=root/'data/products.json'
    base=json.loads(source.read_text(encoding='utf-8'))
    products={p['id']:copy.deepcopy(p) for p in base}
    if len(products)!=len(base): raise InventoryError('Duplicate product codes in data/products.json.')
    for p in products.values():
        if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,39}',p['id']):
            raise InventoryError('Invalid master product code: '+p['id'])
        p.setdefault('category','')
        ids=[v['id'] for v in p['variants']]
        if len(ids)!=len(set(ids)): raise InventoryError('Duplicate master variant: '+p['id'])
    files=sorted((p for p in (root/'branches').iterdir() if p.is_file() and not p.name.startswith(('~$','.'))),key=natural_key)
    unsupported=[p.name for p in files if p.suffix.lower() in ('.xlsx','.xls','.xlsm','.csv','.numbers')]
    if unsupported: raise InventoryError('Remove old branch spreadsheets after migrating to JSON: '+', '.join(unsupported))
    files=[p for p in files if p.suffix.lower()=='.json']
    if not files: raise InventoryError('No branch .json files found in branches/.')
    generated=root/'dist/Products'
    if generated.exists():shutil.rmtree(generated)
    branches=[]; used_ids=set(); warnings=[]; category_translations={}
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
            photos=branch_photos(root,ident)
            for rownum,row in read_inventory(file,category_translations):
                code,product_name,category,color=[text(v) for v in row[:4]]
                if len(category)>120:raise InventoryError(f'Row {rownum}: Category exceeds 120 characters.')
                if not re.fullmatch(r'[A-Z0-9][A-Z0-9._-]{0,39}',code):
                    raise InventoryError(f'Row {rownum}: invalid Product Code. Use uppercase letters, numbers, hyphens, dots or underscores (max 40).')
                if not product_name or len(product_name)>160: raise InventoryError(f'Row {rownum}: Product Name is required (max 160 characters).')
                if not color or len(color)>60: raise InventoryError(f'Row {rownum}: Color / Variant is required (max 60 characters). Use Standard if not applicable.')
                vid=variant_id(color);key=(code,vid)
                if key in seen: raise InventoryError(f'Row {rownum}: duplicate {code} / {color}. Use one row for each product and variant.')
                seen.add(key)
                price=whole_number(row[4],'Price (Ks)',rownum);stock=whole_number(row[5],'Stock',rownum)
                if stock == 0: continue
                if code not in products:
                    products[code]={'id':code,'category':category,'name':{'en':product_name, **({'mm':product_name} if any('\u1000' <= c <= '\u109f' for c in product_name) else {})},'description':{'en':''},'variants':[]}
                p=products[code]
                if product_name not in p['name'].values():
                    warnings.append(f'{file.name} row {rownum}: keeping shared product name for {code}: {p["name"].get("en",code)}')
                if not any(v['id']==vid for v in p['variants']):
                    p['variants'].append({'id':vid,'color':color})
                inventory.append({'productId':code,'variantId':vid,'price':price,'stock':stock,'category':category,'image':photos.get(code,'assets/product-placeholder.svg')})
            contacts=about.get('branches',{}).get(ident,{})
            branches.append({'id':ident,'name':label,'source':file.name,'inventory':inventory,'hasInventory':bool(inventory),'contact':{k:contacts.get(k,'') for k in ['address','phone','viberUrl','facebookUrl','mapUrl','hours']}})
        except InventoryError as exc:
            raise InventoryError(f'{file.name}: {exc}') from exc
    return {'schemaVersion':1,'currency':'MMK','categoryTranslations':category_translations,'products':list(products.values()),'branches':branches,'about':{k:v for k,v in about.items() if k!='branches'}},warnings

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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check',action='store_true',help='Validate without changing the generated catalog.')
    args=parser.parse_args()
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
        return 0
    except (InventoryError,OSError,ValueError) as exc:
        print(f'Inventory update stopped: {exc}',file=sys.stderr)
        print('Fix the named inventory JSON file and upload it again. The live website is not changed by a failed build.',file=sys.stderr)
        return 1

if __name__=='__main__':sys.exit(main())
