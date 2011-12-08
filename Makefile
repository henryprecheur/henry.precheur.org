OUTPUT_DIR=./output/
RSYNC=rsync -vz --checksum --recursive
HOST=henry@bitoku.koalabs.org
SASS=sass
PYTHON=${HOME}/weblog/.env/bin/python

all: publish

publish:
	$(PYTHON) ./publish.py
	mkdir -p ${OUTPUT_DIR}stylesheets
	$(SASS) stylesheets/style.scss:${OUTPUT_DIR}stylesheets/style.css

clean:
	-rm -rf ${OUTPUT_DIR}

re: clean all

upload: clean all
	${RSYNC} ${OUTPUT_DIR} ${HOST}:/var/www/henry.precheur.org/

dry-upload:
	${RSYNC} --dry-run ${OUTPUT_DIR} ${HOST}:/var/www/henry.precheur.org/
