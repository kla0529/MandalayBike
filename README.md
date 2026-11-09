# Mandalay Bike website

This project serves the website and builds its public catalog. Excel reading
and Burmese conversion belong to the separate Mandalay Inventory Importer.
Browse products by branch, name or code. There are no categories.

## All branches use the same code

The builder automatically reads every branches/*.json file. Branch 3 needs
no separate page or code. Keep one file per branch, for example branch 3.json.
Every branch uses five fields: Product Code, Product Name, Color / Variant,
Price (Ks), Stock. Existing six-field inventories with Category are still
accepted; that unused column is ignored. Keep your edited inventory files.

Stock 0 is hidden; stock above 0 is shown. Each JSON is a complete snapshot.

## Local updates: build, then serve

Run this one command from this website project's folder. It builds the catalog
and starts a preview that rebuilds inventory when you refresh:

```bash
python3 scripts/build_catalog.py --serve
```

Check the build's branch summary. Branch 3 should show a positive product and
stock count if its input has available products. If it shows 0, check the
importer's result and closing stock. If the build reports an error, correct it
before expecting the website to update.

Open http://127.0.0.1:8000 and select Branch 3. Keep this Terminal running;
after replacing a branch JSON, refresh the page. Stop any older preview server
first if it already occupies port 8000. Control+C stops it.

If you prefer an ordinary static server, run python3 scripts/build_catalog.py
separately after each edit before refreshing. The automatic rebuild is available
only with --serve.
Confirm that you edited the same project's branches folder, not a different
extracted copy or the importer's Downloads output.

## Public GitHub site

Local changes do not update GitHub Pages. From your cloned repository:

```bash
git add "branches/branch 3.json"
git commit -m "Update Branch 3 inventory"
git push
```

GitHub Actions automatically runs python3 scripts/build_catalog.py after a
commit/push to the repository default branch; there is no manual GitHub build
command to run. Wait for Actions → Update branch catalog and publish to pass. It rebuilds and
publishes dist. An extracted ZIP is not a Git clone: in that case upload the
changed JSON through GitHub's branches folder and commit in the browser.
Keep Settings → Pages → Source set to GitHub Actions.

## Update this project version

Back up your real inventories, photos, contacts and descriptions. Replace
scripts/build_catalog.py, dist/app.js, dist/index.html and dist/style.css.
Update tests and the workflow if using Actions. Keep your own branches/*.json,
especially edited Branch 3. Package inventories are examples, not copies of
your latest local changes. Preserve custom data/about.json and data/products.json.

Delete obsolete website files if present: scripts/import_company_reports.py,
scripts/myanmar_text.py, tests/test_company_import.py, COMPANY-IMPORT.md and
UPDATE-GITHUB.md. Remove old branch XLSX files after retaining their JSON
replacements. Uploads do not remove obsolete files already in GitHub.
An unused nested Mandalay-bike directory can be removed after backing up any
unique changes. The website needs only scripts/build_catalog.py for building;
no Excel reader or converter belongs in this project.

## Daily workflow

Use the separate importer app to select company reports, enter the same JSON
filename for that branch, create/download the result and upload it. Automatic
Zawgyi conversion and zero-stock exclusion happen in the importer. Keep it
unchanged until its report/conversion rules need updates.

## Photos and shared metadata

Place code-named photos such as NH4978.jpg in dist/assets/products. Supported:
JPG, JPEG, PNG, WebP, SVG. One file per code, shared by all branches. Missing
photos use placeholders. Rebuild after changing photos.

Optional descriptions/translations are in data/products.json. Old category
properties are ignored. Contacts are in data/about.json. Use Unicode Burmese.

## Buying lists

Lists use localStorage in the customer's browser, separately per branch. Keep
the same domain and branch IDs to retain lists across website updates. Clearing
site data removes them; private browsing is temporary; devices do not sync.
Lists are for showing shop staff, not online orders or stock reservations.

## Checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_catalog.py --check
```

Python 3 is the only build dependency.
