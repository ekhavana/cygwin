#!/usr/bin/perl

use strict;
use LWP::Simple;
use CGI;
use URI::Escape;
use HTML::TreeBuilder;

use constant {MAXMATCHES => 30};

sub addfn($);
sub myprint(@);
sub wakey($);
sub save(\@@);

# Create one of our Objects
my $html = new CGI;

$CGI::POST_MAX = 64;
$CGI::DISABLE_UPLOADS = 1;

# Get our data
my $grep = $html->param('grep');
my $text = $html->param('text');
my $uri_esc_grep = uri_escape $grep;
my $html_esc_grep = $html->escapeHTML($grep);

$::packages = ();
$::count = 0;
use FindBin qw($Bin);
my @toprint;

$::DUPOUT = 0;

$| = 1;
if ($text) {
    myprint $html->header(-type=>'text/plain');
} else {
    myprint <<'EOF';
!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=us-ascii" />
    <link rel="stylesheet" type="text/css" href="http://cygwin.com/style.css" />
    <title>Cygwin Package List Search Results</title>
  </head>

<body>
<!--#include virtual="navbar.html" -->
<!--#include virtual="top.html" -->
<table>
EOF
}

eval '"foo" =~ /$grep/o';
if ($@ || $grep =~ m!\\\.\\\.!o) {
    save @toprint, $html->h3({-align=>'center'}, '*** Invalid regular expression search string: ', $html_esc_grep . "<br><br>\n");
    save @toprint, $html->h3({-align=>'center'}, '<a href="http://cygwin.com/packages/" align="center">Back</a>') unless $text;
} else {
    $SIG{ALRM} = \&wakey;
    alarm 45;
    save @toprint, $html->h1('Search Results'), "\n" unless $text;
    chdir "$Bin/../packages";
    my $truncated_search = 0;
    outer: for my $f (<*/*>) {
	open F, '<', $f or next;
	while (<F>) {
	    if (/$grep/o) {
		last outer if $truncated_search = $::count >= MAXMATCHES;
		addfn $f;
		last;
	    }
	}
	close F;
    }

    my $index;
    if (!open(INDEX, '<', 'index.html')) {
	%::packages = ();
    } else {
	$index = join('', <INDEX>);
	close INDEX;
    }

    my $sp = $text ? ' ' : '&nbsp;';
    save @toprint, ($text ? '' : $sp) . "Found <b>$::count</b> matches for <b>$html_esc_grep</b>";
    if ($truncated_search) {
	save @toprint, "${sp}${sp}${sp}${sp}(search truncated due to too many matches)<br><br>\n";
    } else {
	save @toprint, "<br><br>\n";
    }
    for my $p (sort keys %::packages) {
	for my $f (@{$::packages{$p}}) {
	    save @toprint, '<tr><td><img src="http://sourceware.org/icons/ball.gray.gif" height=10 width=10 alt=""></td>',
		   '<td cellspacing=10><a href="package-cat.cgi?file=' . uri_escape($f) . '&grep=' .
		   $uri_esc_grep . '">' . $f . '</a></td><td align="left">' . findheader($text, $p, $index) . "</td></tr>\n";
	}
    }
}
if (!$text) {
    push @toprint, <<'EOF';
</table>
</div>
</body>
</html>
EOF
}

alarm 0;
$SIG{ALRM} = 'DEFAULT';
if (!$text) {
    myprint @toprint;
} else {
    my $tree = HTML::TreeBuilder->new_from_content(join('', @toprint));
    myprint $tree->as_text;
}
exit 0;

sub addfn($) {
    if ($_[0] =~ m!^([^/]+)/!o) {
	push @{$::packages{$1}}, $_[0];
	$::count++;
    }
}

sub findheader {
    my $text = shift;
    my $p = shift;
    my $header = ($text && "\t") . (($_[0] =~ m!^.*<a href=.*?>\Q$p\E</a>.*?<td.*?>([^><]+)<!m)[0] || '');
    return $header;
}

sub myprint(@) {
    print @_;
    if ($::DUPOUT) {
	open my $log, '>>', "/tmp/package-grep.$$";
	print $log @_;
	close $log;
    }
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
    print "<!-- ...working... -->\n";
    $SIG{ALRM} = \&wakey;
    alarm 45;
}
