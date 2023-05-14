SOURCES := $(shell find ./posts -name '*.md')
TARGETS := $(patsubst %.md,%.html,$(SOURCES))

STYLES := \
	../styles/tufte.css \
	../styles/pandoc.css \
	../styles/pandoc-solarized.css \
	../styles/tufte-extra.css \
	../fonts/fonts.css \
	../styles/blog-head.css

TEMPLATE := templates/tufte.html5
JINJA_TEMPLATES := templates/index.html.jinja templates/rss.xml.jinja

ASSEMBLY_SCRIPT := assemble.py

# Organizes generated HTML files, and 
.PHONY: all
all: $(TARGETS) $(JINJA_TEMPLATES) $(ASSEMBLY_SCRIPT)
	python $(ASSEMBLY_SCRIPT)

# Builds HTML files from Markdown ones
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

# Because the assembly script renames and moves files, just delete all HTML files
.PHONY: clean
clean:
	find . -name '*.html' -delete
	rm rss.xml

