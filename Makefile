OUTPUT_DIR=./output
RSYNC=rsync -vz --checksum --recursive
HOST=henry@bitoku.koalabs.org
PYTHON=$(HOME)/weblog/.env/bin/python

all: publish

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

publish: _weblog $(OUTPUT_DIR) $(OUTPUT_DIR)/style.css
	$(PYTHON) ./publish.py

_weblog: $(OUTPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)/weblog
	cp -R weblog/doc/* $(OUTPUT_DIR)/weblog
	cp -R weblog/files/* $(OUTPUT_DIR)/weblog

clean:
	-rm -rf $(OUTPUT_DIR)

STYLE_DIR = stylesheets
STYLESHEETS = $(STYLE_DIR)/normalize.css \
	      $(STYLE_DIR)/main.css \
	      $(STYLE_DIR)/archives.css

$(OUTPUT_DIR)/style.css: $(STYLESHEETS)
	cat $> > $@

re: clean all

upload: clean all
	$(RSYNC) $(OUTPUT_DIR) $(HOST):/var/www/henry.precheur.org/

dry-upload:
	$(RSYNC) --dry-run $(OUTPUT_DIR) $(HOST):/var/www/henry.precheur.org/
