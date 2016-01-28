#!/bin/bash -x
# helper script to prepare html manpages for website

# html from man2html needs some cleanup:
# - skip first 2 lines of output, contains a Content-type: header
# - user@host examples get turned into mailto: links, don't want that
# - turn the local man2html link into a link to a link to man2html website
# - don't use links for pages we don't generate
# (remove all relative hrefs except those on the list of pages we generate)

function convert_to_html_and_fixup
{
    output=$1.1.html
    zless `man -w $1` | man2html -r | tail --lines=+3 >$output
    perl -p -i -e 's#<A HREF="mailto:.*">(.*)</A>#\1#' $output
    perl -p -i -e 's#http://localhost/cgi-bin/man/man2html#http://savannah.nongnu.org/projects/man2html/#' $output
    perl -p -i -e 's#<A HREF="\.\./(?!(man1/Xserver.1|man5/XWinrc.5|man1/XWin.1|man1/startxwin.1|index)).*?">(.*?)</A>#\2#g' $output
}

convert_to_html_and_fixup "startxwin"
convert_to_html_and_fixup "Xserver"
convert_to_html_and_fixup "XWin"
convert_to_html_and_fixup "xwinclip"
convert_to_html_and_fixup "xtow"
convert_to_html_and_fixup "xlaunch"
convert_to_html_and_fixup "xwin-xdg-menu"

convert_to_html_and_fixup "XWinrc"
mv XWinrc.1.html ../man5/XWinrc.5.html
