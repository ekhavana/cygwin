#!/usr/bin/perl

use strict;
use LWP::Simple;
use CGI;
use URI::Escape;
use HTML::TreeBuilder;

sub addfn($);
sub wakey($);
sub save(\@@);

# Create one of our Objects
my $html = new CGI;

# Get our data
my $grep = $html->param('grep');
my $text = $html->param('text');

$main::packages = ();
$main::count = 0;
use FindBin qw($Bin);
my @toprint;

if ($text) {
    print $html->header(-type=>'text/plain');
} else {
    print $html->header, "\n<html>\n<head>\n",
	  "<title>Package List Search Results</title>\n</head>\n",
	  LWP::Simple::get('http://cygwin.com/cygwin-header.html'),
	  "</td></table>\n", "<table>\n",
	  $html->h1({-align=>'center'}, 'Cygwin Package List'), "\n";
}

eval '"foo" =~ /$grep/o';
if ($@ || $grep =~ m!\\.\\.!o) {
    save @toprint, $html->h3({-align=>'center'}, '*** Invalid regular expression search string: ', $grep);
    save @toprint, $html->h3({-align=>'center'}, '<a href="http://cygwin.com/packages/" align="center">Back</a>') unless $text;
} else {
    $SIG{ALRM} = \&wakey;
    alarm 45;
    save @toprint, $html->h2({-align=>'center'}, 'Search Results'), "\n" unless $text;
    chdir "$Bin/../packages";
    for my $f (<*/*>) {
	open F, '<', $f or next;
	while (<F>) {
	    if (/$grep/o) {
		addfn $f;
		last;
	    }
	}
	close F;
    }

    my $index;
    if (!open(INDEX, '<', 'index.html')) {
	%main::packages = ();
    } else {
	$index = join('', <INDEX>);
	close INDEX;
    }

    save @toprint, "Found <b>$main::count</b> matches for <b>$grep</b>.<br><br>\n";
    if (%main::packages) {
	for my $p (sort keys %main::packages) {
	    for my $f (@{$main::packages{$p}}) {
		save @toprint, '<tr><td><img src="http://sourceware.org/icons/ball.gray.gif" height=10 width=10 alt=""></td>',
		       '<td cellspacing=10><a href="package-cat.cgi?file=' . uri_escape($f) . '&grep=' .
		       uri_escape($grep) . '">' . $f . '</a></td><td align="left">' . findheader($text, $p, $index) . "</td></tr>\n";
	    }
	}
    }
}
push @toprint, "</table>";
if (!$text) {
    open(FOOTER, '../cygwin-footer.html');
    push @toprint, <FOOTER>, $html->end_html;
    close FOOTER;
}

alarm 0;
$SIG{ALRM} = 'DEFAULT';
if (!$text) {
    print @toprint;
} else {
    my $tree = HTML::TreeBuilder->new_from_content(join('', @toprint));
    print $tree->as_text;
}
exit 0;

sub addfn($) {
    $main::count++;
    $_[0] =~ m!^([^/]+)/! or return;
    push(@{$main::packages{$1}}, $_[0]);
}

sub findheader {
    my $text = shift;
    my $p = shift;
    my $header = ($text && "\t") . (($_[0] =~ m!^.*<a href=.*?>\Q$p\E</a>.*?<td.*?>([^><]+)<!m)[0] || '');
    return $header;
}

sub save(\@@) {
    my $arr = shift;
    if ($text) {
        push(@$arr, "<pre>", @_, "</pre>");
    } else {
        push(@$arr, @_);
    }
}

sub wakey($) {
    print "<!-- working... -->\n";
    $SIG{ALRM} = \&wakey;
    alarm 45;
}
