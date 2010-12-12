#!/usr/bin/perl

use strict;
use LWP::Simple;
use CGI;
use URI::Escape;
use HTML::TreeBuilder;

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

$::DUPOUT = 1;

$| = 1;
if ($text) {
    myprint $html->header(-type=>'text/plain');
} else {
    myprint $html->header, "\n<html>\n<head>\n",
	  "<title>Package List Search Results</title>\n</head>\n",
	  LWP::Simple::get('http://cygwin.com/cygwin-header.html'),
	  "</td></table>\n", "<table>\n",
	  $html->h1({-align=>'center'}, 'Cygwin Package List'), "\n";
}

eval '"foo" =~ /$grep/o';
if ($@ || $grep =~ m!\\.\\.!o) {
    save @toprint, $html->h3({-align=>'center'}, '*** Invalid regular expression search string: ', $html_esc_grep);
    save @toprint, $html->h3({-align=>'center'}, '<a href="http://cygwin.com/packages/" align="center">Back</a>') unless $text;
} else {
    $SIG{ALRM} = \&wakey;
    alarm 45;
    save @toprint, $html->h2({-align=>'center'}, 'Search Results'), "\n" unless $text;
    chdir "$Bin/../packages";
    my $truncated_search = 0;
    outer: for my $f (<*/*>) {
	open F, '<', $f or next;
	while (<F>) {
	    if (/$grep/o) {
		last outer if $truncated_search = $::count >= 30;
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

    save @toprint, " Found <b>$::count</b> matches for <b>$html_esc_grep</b>";
    if ($truncated_search) {
	save @toprint, "&nbsp;&nbsp;&nbsp;&nbsp;(search truncated due to too many matches)<br><br>\n";
    } else {
	save @toprint, "<br><br>\n";
    }
    if (%::packages) {
	for my $p (sort keys %::packages) {
	    for my $f (@{$::packages{$p}}) {
		save @toprint, '<tr><td><img src="http://sourceware.org/icons/ball.gray.gif" height=10 width=10 alt=""></td>',
		       '<td cellspacing=10><a href="package-cat.cgi?file=' . uri_escape($f) . '&grep=' .
		       $uri_esc_grep . '">' . $f . '</a></td><td align="left">' . findheader($text, $p, $index) . "</td></tr>\n";
	    }
	}
    }
}
push @toprint, "</table>";
if (!$text) {
    open FOOTER, '../cygwin-footer.html';
    push @toprint, <FOOTER>, $html->end_html;
    close FOOTER;
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
    $::count++;
    $_[0] =~ m!^([^/]+)/! or return;
    push(@{$::packages{$1}}, $_[0]);
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
