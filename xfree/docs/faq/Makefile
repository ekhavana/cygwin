# Generated automatically from Makefile.in by configure.
# Makefile.in generated automatically by automake 1.4 from Makefile.am

# Copyright (C) 1994, 1995-8, 1999 Free Software Foundation, Inc.
# This Makefile.in is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.


SHELL = /bin/sh

srcdir = ../../faq
top_srcdir = ../..
VPATH = ../../faq
prefix = /usr/local
exec_prefix = ${prefix}

bindir = ${exec_prefix}/bin
sbindir = ${exec_prefix}/sbin
libexecdir = ${exec_prefix}/libexec
datadir = ${prefix}/share
sysconfdir = ${prefix}/etc
sharedstatedir = ${prefix}/com
localstatedir = ${prefix}/var
libdir = ${exec_prefix}/lib
infodir = ${prefix}/info
mandir = ${prefix}/man
includedir = ${prefix}/include
oldincludedir = /usr/include

DESTDIR =

pkgdatadir = $(datadir)/cygwin-xfree-doc
pkglibdir = $(libdir)/cygwin-xfree-doc
pkgincludedir = $(includedir)/cygwin-xfree-doc

top_builddir = ..

ACLOCAL = aclocal
AUTOCONF = autoconf
AUTOMAKE = automake
AUTOHEADER = autoheader

INSTALL = /usr/bin/install -c
INSTALL_PROGRAM = ${INSTALL} $(AM_INSTALL_PROGRAM_FLAGS)
INSTALL_DATA = ${INSTALL} -m 644
INSTALL_SCRIPT = ${INSTALL_PROGRAM}
transform = s,x,x,

NORMAL_INSTALL = :
PRE_INSTALL = :
POST_INSTALL = :
NORMAL_UNINSTALL = :
PRE_UNINSTALL = :
POST_UNINSTALL = :
JADE = jade
MAKEINFO = makeinfo
NSGMLS = nsgmls
PACKAGE = cygwin-xfree-doc
VERSION = 0.0.8

MAX_TEX_RECURSION = 4

XML_DECL = $(srcdir)/../stylesheets/xml.dcl

HTML_SS = $(srcdir)/../stylesheets/website.dsl
PRINT_SS = /usr/share/sgml/docbook/dsssl-stylesheets/print/docbook.dsl

faq_xml_source = cygwin-xfree-faq.xml
extra_faq_xml_source = biblio.xml 	config.xml 	contrib.xml 	errors.xml 	fdl.xml 	general.xml 	glossary.xml 	licptc.xml 	install.xml 	usage.xml 	trouble.xml


extra_faq_html = biblio.html 	gfdl.html 	gfdl-aggregation-with-independent-works.html 	gfdl-applicability-and-definitions.html 	gfdl-collections-of-documents.html 	gfdl-combining-documents.html 	gfdl-copying-in-quantity.html 	gfdl-future-revisions-of-this-license.html 	gfdl-modifications.html 	gfdl-termination.html 	gfdl-translation.html 	gfdl-using-for-your-documents.html 	gfdl-verbation-copying.html 	glossary.html


extra_faq_ps = cygwin-xfree-faq.ps
extra_faq_pdf = cygwin-xfree-faq.pdf
extra_faq_txt = cygwin-xfree-faq.txt
extra_faq_rtf = cygwin-xfree-faq.rtf
extra_faq_dvi = cygwin-xfree-faq.dvi
extra_faq_tex = cygwin-xfree-faq.tex

faqdir = $(pkgdatadir)/faq
faq_DATA = cygwin-xfree-faq.html $(extra_faq_html) $(extra_faq_ps) 	$(extra_faq_pdf) $(extra_faq_txt) $(extra_faq_rtf)

EXTRA_DIST = $(faq_xml_source) $(extra_faq_xml_source)
mkinstalldirs = $(SHELL) $(top_srcdir)/mkinstalldirs
CONFIG_CLEAN_FILES = 
DATA =  $(faq_DATA)

DIST_COMMON =  Makefile.am Makefile.in


DISTFILES = $(DIST_COMMON) $(SOURCES) $(HEADERS) $(TEXINFOS) $(EXTRA_DIST)

TAR = gtar
GZIP_ENV = --best
all: all-redirect
.SUFFIXES:
$(srcdir)/Makefile.in: Makefile.am $(top_srcdir)/configure.in $(ACLOCAL_M4) 
	cd $(top_srcdir) && $(AUTOMAKE) --foreign faq/Makefile

Makefile: $(srcdir)/Makefile.in  $(top_builddir)/config.status $(BUILT_SOURCES)
	cd $(top_builddir) \
	  && CONFIG_FILES=$(subdir)/$@ CONFIG_HEADERS= $(SHELL) ./config.status


install-faqDATA: $(faq_DATA)
	@$(NORMAL_INSTALL)
	$(mkinstalldirs) $(DESTDIR)$(faqdir)
	@list='$(faq_DATA)'; for p in $$list; do \
	  if test -f $(srcdir)/$$p; then \
	    echo " $(INSTALL_DATA) $(srcdir)/$$p $(DESTDIR)$(faqdir)/$$p"; \
	    $(INSTALL_DATA) $(srcdir)/$$p $(DESTDIR)$(faqdir)/$$p; \
	  else if test -f $$p; then \
	    echo " $(INSTALL_DATA) $$p $(DESTDIR)$(faqdir)/$$p"; \
	    $(INSTALL_DATA) $$p $(DESTDIR)$(faqdir)/$$p; \
	  fi; fi; \
	done

uninstall-faqDATA:
	@$(NORMAL_UNINSTALL)
	list='$(faq_DATA)'; for p in $$list; do \
	  rm -f $(DESTDIR)$(faqdir)/$$p; \
	done
tags: TAGS
TAGS:


distdir = $(top_builddir)/$(PACKAGE)-$(VERSION)/$(subdir)

subdir = faq

distdir: $(DISTFILES)
	here=`cd $(top_builddir) && pwd`; \
	top_distdir=`cd $(top_distdir) && pwd`; \
	distdir=`cd $(distdir) && pwd`; \
	cd $(top_srcdir) \
	  && $(AUTOMAKE) --include-deps --build-dir=$$here --srcdir-name=$(top_srcdir) --output-dir=$$top_distdir --foreign faq/Makefile
	@for file in $(DISTFILES); do \
	  d=$(srcdir); \
	  if test -d $$d/$$file; then \
	    cp -pr $$/$$file $(distdir)/$$file; \
	  else \
	    test -f $(distdir)/$$file \
	    || ln $$d/$$file $(distdir)/$$file 2> /dev/null \
	    || cp -p $$d/$$file $(distdir)/$$file || :; \
	  fi; \
	done
info-am:
info: info-am
dvi-am:
dvi: dvi-am
check-am: all-am
	$(MAKE) $(AM_MAKEFLAGS) check-local
check: check-am
installcheck-am:
installcheck: installcheck-am
install-exec-am:
install-exec: install-exec-am

install-data-am: install-faqDATA
install-data: install-data-am

install-am: all-am
	@$(MAKE) $(AM_MAKEFLAGS) install-exec-am install-data-am
install: install-am
uninstall-am: uninstall-faqDATA
uninstall: uninstall-am
all-am: Makefile $(DATA)
all-redirect: all-am
install-strip:
	$(MAKE) $(AM_MAKEFLAGS) AM_INSTALL_PROGRAM_FLAGS=-s install
installdirs:
	$(mkinstalldirs)  $(DESTDIR)$(faqdir)


mostlyclean-generic:

clean-generic:

distclean-generic:
	-rm -f Makefile $(CONFIG_CLEAN_FILES)
	-rm -f config.cache config.log stamp-h stamp-h[0-9]*

maintainer-clean-generic:
mostlyclean-am:  mostlyclean-generic

mostlyclean: mostlyclean-am

clean-am:  clean-generic mostlyclean-am clean-local

clean: clean-am

distclean-am:  distclean-generic clean-am

distclean: distclean-am

maintainer-clean-am:  maintainer-clean-generic distclean-am
	@echo "This command is intended for maintainers to use;"
	@echo "it deletes files that may require special tools to rebuild."

maintainer-clean: maintainer-clean-am

.PHONY: uninstall-faqDATA install-faqDATA tags distdir info-am info \
dvi-am dvi check-local check check-am installcheck-am installcheck \
install-exec-am install-exec install-data-am install-data install-am \
install uninstall-am uninstall all-redirect all-am all installdirs \
mostlyclean-generic distclean-generic clean-generic \
maintainer-clean-generic clean mostlyclean distclean maintainer-clean


cygwin-xfree-faq.html $(extra_faq_html): $(HTML_SS) $(faq_xml_source) \
	$(extra_faq_xml_source)

$(extra_faq_tex): $(faq_xml_source) $(extra_faq_xml_source)

$(extra_faq_dvi): $(extra_faq_tex)

$(extra_faq_ps): $(extra_faq_dvi)

$(extra_faq_pdf): $(extra_faq_dvi)

$(extra_faq_txt): $(faq_xml_source) $(extra_faq_xml_source)

$(extra_faq_rtf): $(faq_xml_source) $(extra_faq_xml_source)

clean-local:
	rm -f *.htm *.html *.dvi *.tex *.ps *.pdf *.txt *.log *.aux *.rtf

check-local: 
	@for testfile in cygwin-xfree-faq.html $(extra_faq_html); do \
	  echo "$(NSGMLS) -wmin-tag -s $$testfile"; \
	  $(NSGMLS) -wmin-tag -s $$testfile || exit 1; \
	done

validate:
	$(NSGMLS) -wmin-tag -s $(srcdir)/$(faq_xml_source)

cygwin-xfree-faq.tex:
	$(SHELL) -c "$(JADE) -t tex -V tex-backend \
	-d $(PRINT_SS) -o $@ $(XML_DECL) $(srcdir)/$(faq_xml_source)"

cygwin-xfree-faq.dvi:
	# Trick from Adam Di Carlo <adam@onshore.com> to recurse jadetex 
	# "just enough".
	-cp -pf prior.aux pprior.aux
	-cp -pf $(shell basename $< .tex).aux prior.aux
	jadetex $<
	if ! cmp $(shell basename $< .tex).aux prior.aux &&		\
	   ! cmp $(shell basename $< .tex).aux pprior.aux &&		\
	   expr $(MAKELEVEL) '<' $(MAX_TEX_RECURSION); then		\
		rm -f $@						;\
		$(MAKE) $@						;\
	fi
	rm -f prior.aux pprior.aux

cygwin-xfree-faq.ps:
	dvips -f $< > $@

cygwin-xfree-faq.pdf:
	dvipdf -f $< > $@

cygwin-xfree-faq.html:
	$(SHELL) -c "$(NSGMLS) -wmin-tag -s $< && $(JADE) -t xml -ihtml \
	-d $(HTML_SS) -o $@ $(XML_DECL) $(srcdir)/$(faq_xml_source)"

cygwin-xfree-faq.txt:
	$(JADE) -t xml -V nochunks \
		-d $(HTML_SS) \
		$(XML_DECL) $(srcdir)/cygwin-xfree-faq.xml > dump.html
	lynx -force_html -dump dump.html > $@
	-rm -f dump.html

cygwin-xfree-faq.rtf:
	$(SHELL) -c "$(JADE) -t rtf -d $(PRINT_SS) -o $@ $(XML_DECL) \
	$(srcdir)/$(faq_xml_source)"

# Tell versions [3.59,3.63) of GNU make to not export all variables.
# Otherwise a system limit (for SysV at least) may be exceeded.
.NOEXPORT:
