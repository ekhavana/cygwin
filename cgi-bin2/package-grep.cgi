#!/usr/bin/perl

use CGI;

# Create one of our Objects
my $html = new CGI;

# Get our data
my $grep = $html->param('grep');

use FindBin qw($Bin);

print header, start_html('Package List Search Results'), h1('Package List Search Results');
print "bin = $Bin, grep = $grep\n";
print hr;
