#!/bin/bash
# Build CSS, JS and Python assets

echo ":: Build D-BAS"
python setup.py --quiet develop

echo ":: Compile and compress JS"
google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/{main,ajax,d3,discussion,review}/*.js > dbas/static/js/dbas.min.js
google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/libs/cookie-2.1.3.js > dbas/static/js/libs/cookie-2.1.3.min.js
google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/libs/eu-cookie-law-popup.js > dbas/static/js/libs/eu-cookie-law-popup.min.js
google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./webhook/static/js/*.js > webhook/static/js/websocket.min.js
google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./admin/static/js/main/*.js > admin/static/js/admin.min.js

echo ":: Compile and compress SASS"
sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed
rm -r .sass-cache

echo ":: Build translations"
cd dbas && ./i18n.sh
cd ../admin && ./i18n.sh
cd ../
