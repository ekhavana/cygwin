#!/usr/bin/perl

use strict;
use LWP::Simple;
use CGI;
use Cwd;
use File::Basename;

my $html = new CGI;

my $grep = $html->param('grep');
my $file = $html->param('file');

use FindBin qw($Bin);

print $html->header, "\n<html>\n<head>\n<title>Package List Search Results</title>\n</head>\n",
      LWP::Simple::get('http://cygwin.com/cygwin-header.html'), "\n";

chdir("$Bin/../packages");
my $here = getcwd;
chdir dirname($file);
my $there = getcwd;
chdir $here;
if (substr($there, 0, length($there)) . '/' ne "$here/" || !open(F, '<', $file)) {
    print $html->h1("Couldn't open file: $file");
} else {
    $_ = join('', <F>);
    s!($grep)!\<b\>$1\</b\>!mog if length($grep);
    print $_;
}

print "</table>";
open(FOOTER, '../cygwin-footer.html');
print <FOOTER>, $html->end_html;
close FOOTER;
