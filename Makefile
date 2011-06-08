OUTPUT_DIR=./output/
RSYNC=rsync -vz --checksum --recursive
HOST=henry@bitoku.koalabs.org

all: publish

publish:
	${HOME}/weblog/env/bin/python ./publish.py
	mkdir -p ${OUTPUT_DIR}stylesheets
	sass stylesheets/style.scss:${OUTPUT_DIR}stylesheets/style.css
	# mkdir -p ${OUTPUT_DIR}scripts
	# ln -f scripts/background.js ${OUTPUT_DIR}scripts/background.js

clean:
	-rm -rf ${OUTPUT_DIR}

re: clean all

upload: clean all
	${RSYNC} ${OUTPUT_DIR} ${HOST}:/var/www/henry.precheur.org/

dry-upload:
	${RSYNC} --dry-run ${OUTPUT_DIR} ${HOST}:/var/www/henry.precheur.org/
