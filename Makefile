OUTPUT_DIR=./output
RSYNC=rsync -vz --checksum --recursive
HOST=henry@bitoku.koalabs.org
VIRTUAL_ENV=.env
PYTHON=$(VIRTUAL_ENV)/bin/python

all: render _copy

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

.PHONY: _copy rmenv reenv clean

_url=https://raw.github.com/pypa/virtualenv/develop/virtualenv.py
$(VIRTUAL_ENV):
	curl --silent $(_url) | python2.7 - $@
	$@/bin/pip install hg+https://bitbucket.org/henry/weblog

rmenv:
	rm -rf $(VIRTUAL_ENV)

reenv: rmenv $(VIRTUAL_ENV)

_copy: _weblog $(OUTPUT_DIR) $(OUTPUT_DIR)/style.css
	for i in favicon.ico robots.txt sitemap.xml redirect.conf; do \
		ln -f $${i} $(OUTPUT_DIR); \
	done
	test -d $(OUTPUT_DIR)/vanpy || mkdir $(OUTPUT_DIR)/vanpy
	cp -r vanpy/test $(OUTPUT_DIR)/vanpy

render: $(VIRTUAL_ENV)
	$(PYTHON) ./publish.py $(OUTPUT_DIR)

render-final: $(VIRTUAL_ENV)
	$(PYTHON) ./publish.py --rewrite $(OUTPUT_DIR)

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
	cat $(STYLESHEETS) > $@

re: clean all

upload: clean render-final _copy
	$(RSYNC) $(OUTPUT_DIR)/ $(HOST):/var/www/henry.precheur.org/

upload-test: clean render-final _copy
	$(RSYNC) $(OUTPUT_DIR)/ $(HOST):/var/www/henry2.precheur.org/

dry-upload:
	$(RSYNC) --dry-run $(OUTPUT_DIR) $(HOST):/var/www/henry.precheur.org/
