OUTPUT_DIR=./output
RSYNC=rsync -vz --checksum --recursive
HOST=henry@bitoku.koalabs.org
PYTHON=$(HOME)/weblog/.env/bin/python

all: publish

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

publish: css $(OUTPUT_DIR)
	$(PYTHON) ./publish.py

clean:
	-rm -rf $(OUTPUT_DIR)

STYLE_DIR = stylesheets

css: $(OUTPUT_DIR)
	cat $(STYLE_DIR)/normalize.css $(STYLE_DIR)/main.css > $(OUTPUT_DIR)/style.css

re: clean all

upload: clean all
	$(RSYNC) $(OUTPUT_DIR) $(HOST):/var/www/henry.precheur.org/

dry-upload:
	$(RSYNC) --dry-run $(OUTPUT_DIR) $(HOST):/var/www/henry.precheur.org/
