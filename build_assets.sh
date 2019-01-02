#!/bin/bash
# Build CSS, JS and Python assets
set -e
echo ":: Build D-BAS"
python3 setup.py --quiet develop

echo ":: Install JS libs"
yarn install

echo ":: Compile and compress JS"

dbas_min_js="dbas.min.js"
websocket_min_js="websocket.min.js"
admin_min_js="admin.min.js"

find . \( -name ${dbas_min_js} -o -name ${websocket_min_js} -o -name ${admin_min_js} \) -type f -delete

npx google-closure-compiler --create_source_map dbas/static/js/${dbas_min_js}.map --compilation_level SIMPLE --js ./dbas/static/js/{main,ajax,d3,discussion,review}/*.js --js_output_file dbas/static/js/${dbas_min_js}
npx google-closure-compiler --create_source_map websocket/static/js/${websocket_min_js}.map --compilation_level SIMPLE --js ./websocket/static/js/*.js --js_output_file websocket/static/js/${websocket_min_js}
npx google-closure-compiler --create_source_map admin/static/js/${admin_min_js}.map --compilation_level SIMPLE --js ./admin/static/js/main/*.js --js_output_file admin/static/js/${admin_min_js}

echo ":: Compile and compress SASS"
sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed
sass dbas/static/css/creative.sass dbas/static/css/creative.css --style compressed

echo ":: Build translations"
cd dbas && ./i18n.sh
cd ../admin && ./i18n.sh
cd ../
