#!/usr/bin/perl

use strict;
use CGI qw':standard';

sub addfn($);

# Create one of our Objects
my $html = new CGI;

# Get our data
my $grep = $html->param('grep');

$main::packages = ();
use FindBin qw($Bin);

print $html->header, "\n<html>\n<head>\n<title>Package List Search Results</title>\n</head>\n",
      "<!--#include virtual=\"cygwin-header.html\" --></td></table>\n",
      "<table align=\"center\">\n",
      $html->h1({-align=>'center'}, 'Cygwin Package List'), "\n",
      $html->h2({-align=>'center'}, 'Search Results'), "\n";

chdir("$Bin/../packages");
for my $f (<*/*>) {
    open(F, $f) or next;
    while (<F>) {
	if (/$grep/o) {
	    addfn($f);
	    last;
	}
    }
    close F;
}

my $index;
if (!open(INDEX, 'index.html')) {
    %main::packages = ();
} else {
    $index = join('', <INDEX>);
    close INDEX;
}

if (!%main::packages) {
    print "<br><br>No packages contained search string '<tt>$grep<tt>'";
} else {
    for my $p (sort keys %main::packages) {
	for my $f (@{$main::packages{$p}}) {
	    print '<tr><td><img src="http://sources.redhat.com/icons/ball.gray.gif" height=10 width=10 alt=""></a></td><td cellspacing=10><a href="../packages/' . $f . '">' . $f . '</a></td><td align="left">' . findheader($p, $index) . "</td></tr>\n";
	}
    }
}
print "</table>";
print "<!--#include virtual=\"cygwin-footer.html\" -->\n", $html->end_html;

sub addfn($) {
    $_[0] =~ m!^([^/]+)/! or return;
    push(@{$main::packages{$1}}, $_[0]);
}

sub findheader {
    my $p = shift;
    my $header = ($_[0] =~ m!^.*<a href=.*?>$p</a>.*?<td.*?>([^><]+)<!m)[0];
    return $header || '';
}
