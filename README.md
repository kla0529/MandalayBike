# Mandalay Bike — website

Upload these contents to your GitHub repository root, including hidden .github.
Keep Settings → Pages → Source set to GitHub Actions. Each commit/push to the
default branch installs requirements, builds the catalog and publishes only dist.
No manual GitHub build command is needed.

## Updating an existing installation

Back up your branch JSON, photos and contacts first. Replace the website code,
workflow and requirements.txt with this version. Keep your own inventories and
contacts rather than replacing them with the empty setup files in this ZIP.
Branch 2 retains the six real AAG items supplied earlier, without invented categories.
The other included branches are empty. No illustrative demo products remain.
The logo and missing-photo asset are functional assets, not sample products.

Delete obsolete tests, templates, converter files, old product sample images,
old dist/assets/products and dist/assets/bike.jpg from the website repository.
Remove old nested duplicate project folders after preserving unique data.
Uploads do not delete old files automatically. Keep the separate importer app
on your computer, not in this website repository.

## Files and image naming

| Path | Purpose |
|---|---|
| branches/branch 1.json … branch 5.json | Public inventory, unchanged branch naming |
| Products/branch1/ID.jpg | Branch 1 source photo, named by product ID |
| Products/branch2/ID.png | Branch 2 source photo |
| Products/branch3/, branch4/, branch5/ | Other branch source photos |
| data/about.json | Your public contact details |
| data/products.json | Optional descriptions and translations; starts empty |
| scripts/build_catalog.py | Validate inventories and prepare public photos/catalog |
| requirements.txt | Pillow and HEIC decoding dependencies |
| dist/ | Website files and build output |

Examples: Products/branch1/NH865.jpg and Products/branch2/NH865.heic may show
different photos for the same ID in different branches. Keep one image per ID
per branch. Matching ID filename capitalization is ignored. Folder names are
case-sensitive: Products and branch1 as shown. Empty .gitkeep files preserve
the new folders in Git; remove them after adding photos if desired.

Supported input formats: JPG/JPEG, PNG, WebP, AVIF, GIF, HEIC and HEIF.
GitHub builds copy browser-compatible photos into dist/Products. HEIC/HEIF
files are converted to JPEG automatically using the installed image libraries.
Do not link raw HEIC files directly in the browser or commit generated dist/Products.
Unsupported/broken HEIC files stop the build with an error. Missing product
photos use the neutral placeholder. Source photo metadata can remain in original
JPG/PNG files, so remove private location metadata before uploading those publicly.

## Inventory and categories

The new importer emits headers ID, Name, Category, Price, Stock. Categories
come only from Category; GROUP is ignored. Missing/blank Category is allowed:
the product appears under All categories without an invented classification.
Category choices are generated from available products in the selected branch.
Previous five/six-column importer JSON remains readable, preserving existing
branch IDs and buying lists. Regenerate it when convenient to use the new schema.

Replace the matching branch JSON, commit/push and wait for Actions to pass.
Stock 0 is hidden. A later positive-stock snapshot restores the item. Never
upload original company XLSX files, customer records or credentials here.

## Language and hero

Burmese is the default for visitors without a saved choice. The language menu
shows Myanmar, UK and China flags. A chosen language is stored in that browser
and retained on refresh, branch changes and future visits. Clearing browser
data removes this preference; different devices do not share it.

The hero randomly selects a photo from the selected branch's available products
and changes every six seconds without immediately repeating a photo. It hides
the image area if there are no product photos, and stays still for visitors
who request reduced motion. Brand slogans, decorative stars and the promotional
banner have been removed.

## Local preview (optional)

Python 3.12+ is recommended for the pinned image packages:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_catalog.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Rebuild after each local inventory/photo update.
The published website needs no Python runtime in the customer's browser.
