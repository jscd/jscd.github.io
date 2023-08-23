#
# Author: Jake Zimmerman <jake@zimmerman.io>
#
# ===== Usage ================================================================
#
# make                  Prepare _site/ folder (all markdown & assets)
# make _site/index.html  Recompile just _site/index.html
#
# make watch            Start a local HTTP server and rebuild on changes
# PORT=4242 make watch  Like above, but use port 4242
#
# make clean            Delete all generated files
#
# ============================================================================

SOURCES := $(shell find src -type f -name '*.md')
TARGETS := $(patsubst src/%.md,_site/%.html,$(SOURCES))

.PHONY: all
all: _site/.nojekyll $(TARGETS)

.PHONY: clean
clean:
	rm -rf _site

.PHONY: watch
watch:
	./tools/serve.sh --watch

_site/.nojekyll: $(wildcard public/*) public/.nojekyll
	rm -vrf _site && mkdir -p _site && cp -vr public/.nojekyll public/* _site

.PHONY: _site
_site: _site/.nojekyll

# Generalized rule: how to build a .html file from each .md
# Note: you will need pandoc 2 or greater for this to work
_site/%.html: src/%.md template.html5 Makefile tools/build.sh
	tools/build.sh "$<" "$@"


