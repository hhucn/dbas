dbas_min_js = dbas.min.js
websocket_min_js = websocket.min.js
admin_min_js = admin.min.js

dbas: python clean-js js sass i18n

python:
	python3 setup.py --quiet develop

install-js:
	yarn install

js: install-js
	npx google-closure-compiler \
	--create_source_map dbas/static/js/${dbas_min_js}.map \
	--compilation_level SIMPLE \
	--js ./dbas/static/js/main/*.js \
	./dbas/static/js/ajax/*.js \
	./dbas/static/js/d3/*.js \
	./dbas/static/js/discussion/*.js \
	./dbas/static/js/review/*.js \
	--js_output_file dbas/static/js/${dbas_min_js}
	\
	npx google-closure-compiler \
	--create_source_map admin/static/js/${admin_min_js}.map \
	--compilation_level SIMPLE \
	--js ./admin/static/js/main/*.js \
	--js_output_file admin/static/js/${admin_min_js}

clean-js:
	find . \( -name ${dbas_min_js} -o -name ${admin_min_js} \) -type f -delete

sass:
	@echo ":: Compile SASS"
	sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed
	sass dbas/static/css/creative.sass dbas/static/css/creative.css --style compressed

i18n:
	cd dbas && ./i18n.sh
	cd admin && ./i18n.sh