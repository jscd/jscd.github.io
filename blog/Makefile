# What to compile by default?
SOURCES := $(shell find ./posts -name '*.md')
TARGETS := $(patsubst %.md,%.html,$(SOURCES))

STYLES := \
	../styles/tufte.css \
	../styles/pandoc.css \
	../styles/pandoc-solarized.css \
	../styles/tufte-extra.css

TEMPLATE := templates/tufte.html5

.PHONY: all
all: $(TARGETS)

# Note: you will need pandoc 2 or greater for this to work

## Generalized rule: how to build a .html file from each .md
%.html: %.md $(TEMPLATE) $(STYLES)
	pandoc \
		--katex \
		--section-divs \
		--from markdown+tex_math_single_backslash \
		--filter pandoc-sidenote \
		--to html5+smart \
		--template=$(TEMPLATE) \
		$(foreach style,$(STYLES),--css ../../$(style)) \
		--output $@ \
		$<

.PHONY: clean
clean:
	rm -f $(TARGETS)

