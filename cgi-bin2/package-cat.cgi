#!/usr/bin/perl

use strict;
use LWP::Simple;
use CGI;

my $html = new CGI;

my $grep = $html->param('grep');
my $file = $html->param('file');

use FindBin qw($Bin);

print $html->header, "\n<html>\n<head>\n<title>Package List Search Results</title>\n</head>\n",
      LWP::Simple::get('http://cygwin.com/cygwin-header.html'), "\n",

chdir("$Bin/../packages");
if (!open(F, $file)) {
    print h1("Couldn't open file: $file");
} else {
    $_ = join('', <F>);
    s!$grep!\<b\>$grep\</b\>!mo if length($grep);
    print $_;
}

print "</table>";
open(FOOTER, '../cygwin-footer.html');
print <FOOTER>, $html->end_html;
close FOOTER;
