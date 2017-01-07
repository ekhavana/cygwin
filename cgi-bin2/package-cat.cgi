#!/usr/bin/perl

use strict;
use LWP::Simple;
use CGI;
use Cwd;
use File::Basename;

sub include_virtual(@);

my $html = new CGI;

my $grep = $html->param('grep');
my $file = $html->param('file');

use FindBin qw($Bin);
print $html->header(-charset=>'utf-8'),
      $html->start_html(-title=>'Cygwin Package Listing',
                        -dtd=>['-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
                        -style=>'../style.css');
include_virtual "../navbar.html";
print '<div id="main">';
include_virtual "../top.html";

chdir("$Bin/../packages");
my $here = getcwd;
chdir dirname($file);
my $there = getcwd;
chdir $here;

if (substr($there, 0, length($here) + 1) ne "$here/" || !open(F, '<', $file)) {
    print "<br/><br/>\n", $html->h2("Error: couldn't open file: $file");
} else {
    local $/;
    $_ = <F>;

    # snatch the body of the listing html file
    s!.*<html>(.*)</html>.*!$1!so;
    s!.*<body>(.*)</body>.*!$1!so;

    s!($grep)!\<b\>$1\</b\>!mog if length($grep);
    print $_;
}

print '</div>';
print $html->end_html;

sub include_virtual(@) {
    for my $f (@_) {
	open my $fd, '<', $f;
	print <$fd>;
	close $fd;
    }
}
