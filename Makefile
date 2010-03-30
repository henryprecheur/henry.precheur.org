OUTPUT_DIR=./output/
RSYNC=rsync -vz --checksum --recursive
HOST=bitoku.koalabs.org

all: publish

publish:
	./publish.py

clean:
	-rm -rf ${OUTPUT_DIR}

upload: clean all
	${RSYNC} ${OUTPUT_DIR} ${HOST}:/var/www/henry.precheur.org/

dry-upload:
	${RSYNC} --dry-run ${OUTPUT_DIR} ${HOST}:/var/www/henry.precheur.org/
