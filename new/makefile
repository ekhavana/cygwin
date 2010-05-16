.PHONY: all

all: $(addsuffix .stamp,$(wildcard *.html) style.css)

%.stamp: %
	@scp -Cqp $? sourceware.org:/www/sourceware/htdocs/cygwin/new
	@touch $@
