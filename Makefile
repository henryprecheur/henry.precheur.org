OUTPUT_DIR=./output
RSYNC=rsync -vz --checksum --recursive
HOST=henry@bitoku.koalabs.org
VIRTUAL_ENV=.env
VIRTUAL_ENV_PYTHON=$(VIRTUAL_ENV)/bin/python
PYTHON=python2.7

all: render _copy
final: render-final _copy

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

.PHONY: _copy rmenv reenv clean

_url=https://raw.github.com/pypa/virtualenv/develop/virtualenv.py
$(VIRTUAL_ENV):
	virtualenv $@
	$@/bin/pip install hg+https://bitbucket.org/henry/weblog

rmenv:
	rm -rf $(VIRTUAL_ENV)

reenv: rmenv $(VIRTUAL_ENV)

_copy: _weblog $(OUTPUT_DIR) $(OUTPUT_DIR)/style.css
	for i in favicon.ico robots.txt sitemap.xml redirect.conf; do \
		ln -f $${i} $(OUTPUT_DIR); \
	done
	mkdir -p $(OUTPUT_DIR)/images
	cp images/logo.png $(OUTPUT_DIR)/images
	cp -r font output
	test -d $(OUTPUT_DIR)/vanpy || mkdir $(OUTPUT_DIR)/vanpy
	cp -r vanpy/test $(OUTPUT_DIR)/vanpy

render: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV_PYTHON) ./publish.py $(OUTPUT_DIR)

render-final: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV_PYTHON) ./publish.py --rewrite $(OUTPUT_DIR)

serve:
	$(VIRTUAL_ENV) -m SimpleHTTPServer

_weblog: $(OUTPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)/weblog
	cp -R weblog/doc/* $(OUTPUT_DIR)/weblog
	cp -R weblog/files/* $(OUTPUT_DIR)/weblog

clean:
	-rm -rf $(OUTPUT_DIR)

STYLE_DIR = stylesheets
STYLESHEETS = $(STYLE_DIR)/normalize.css \
	      $(STYLE_DIR)/main.css \
	      $(STYLE_DIR)/archives.css \
	      $(STYLE_DIR)/fonts.css \

$(STYLE_DIR)/normalize.css:
	curl http://necolas.github.io/normalize.css/3.0.0/normalize.css > $@

$(OUTPUT_DIR)/style.css: $(STYLESHEETS)
	cat $(STYLESHEETS) > $@

re: clean all

upload: clean render-final _copy
	$(RSYNC) $(OUTPUT_DIR)/ $(HOST):/var/www/henry.precheur.org

upload-test: clean render-final _copy
	$(RSYNC) $(OUTPUT_DIR)/ $(HOST):/var/www/henry2.precheur.org

dry-upload: clean render-final _copy
	$(RSYNC) --dry-run $(OUTPUT_DIR)/ $(HOST):/var/www/henry.precheur.org
