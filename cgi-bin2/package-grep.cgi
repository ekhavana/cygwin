#!/usr/bin/perl

use strict;
use CGI;
use File::Basename;
use HTML::TreeBuilder;
use LWP::Simple;
use URI::Escape;

use constant {MAXMATCHES => 30};

sub addfn($);
sub findheader($$$);
sub include_virtual(@);
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
my $arch = $html->param('arch') || 'x86';
my $debug = $html->param('debug');
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
    myprint $html->header, $html->start_html(-title=>'Cygwin Package Search',
					     -dtd=>['-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
					     -style=>'../style.css');
    include_virtual "../navbar.html", "../top.html";

    print '<h1>Cygwin Package Search</h1>';
    print '<form method="GET" action="//cygwin.com/cgi-bin2/package-grep-test.cgi">';
    print 'Search package contents for a <a href="http://en.wikipedia.org/wiki/Regular_expression">regular expression</a> pattern, ';
    print 'or view the <a href="https://cygwin.com/packages/package_list.html">full list</a> of packages<br>';
    print '<input type="text" size=40 name="grep" value="' . $html_esc_grep . '">';
    print '<input type=submit value="Go"><br>';
    print '<input type="radio" name="arch" value="x86"'    . (($arch eq 'x86') ? 'checked="checked"' : '') . '>x86';
    print '<input type="radio" name="arch" value="x86_64"' . (($arch ne 'x86') ? 'checked="checked"' : '') . '>x86_64';
    print '</form>';
}

my $index;
$grep =~ s/^\s+|\s+$//g;
eval '"foo" =~ /$grep/o';
if ($@ || $grep =~ m!\\\.\\\.!o) {
    save @toprint, $html->h3({-align=>'center'}, '*** Invalid regular expression search string: ', $html_esc_grep . "<br><br>\n");
} elsif (length($grep)) {
    $SIG{ALRM} = \&wakey;
    alarm 45;
    save @toprint, $html->h1('Search Results'), "\n" unless $text;
    chdir "$Bin/../packages";
    my $truncated_search = 0;
    opendir my ($archdfd), $arch;
    for my $dir (sort readdir $archdfd) {
	next if substr($dir, 0, 1) eq '.';
	$dir = "$arch/$dir";
	opendir my $reldfd, "$dir" or next;	# presumably not a directory
	for my $f (sort readdir $reldfd) {
	    $f = "$dir/$f";
	    local $/;
	    open my $fd, '<', $f or next;
	    addfn $f if <$fd> =~ /$grep/om;
	    close $fd;
	}
	closedir $reldfd;
    }
    closedir $archdfd;

    if (!open(INDEX, '<', "$arch/packages.inc")) {
	%::packages = ();
	print "<h3>empty packages?</h3>" if $debug;
    } else {
	local $/;
	$index = <INDEX>;
	close INDEX;
	print "<h3>full packages</h3>" if $debug;
    }

    my $sp = $text ? ' ' : '&nbsp;';
    save @toprint, ($text ? '' : $sp) . "Found <b>$::count</b> matches for <b>$html_esc_grep</b>";
    if ($truncated_search) {
	save @toprint, "${sp}${sp}${sp}${sp}(search truncated due to too many matches)<br><br>\n";
    } else {
	save @toprint, "<br><br>\n";
    }
    push @toprint, "<ul>\n" if !$text;
    my $start;
    my $end;
    if ($text) {
	$start = '';
	$end = "\n";
    } else {
	$start = '<li>';
	$end = "</li>\n";
    }
    for my $p (sort keys %::packages) {
	for my $f (@{$::packages{$p}}) {
	    save @toprint, $start . '<a href="package-cat.cgi?file=' . uri_escape($f) . '&grep=' .
		 $uri_esc_grep . '">' . basename($f) . '</a> - ' . findheader($text, $p, $f) . $end;
	}
    }
    push @toprint, "</ul>\n" if !$text;
}
if (!$text) {
    push @toprint, <<'EOF';
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
    if ($_[0] =~ m!^.*?/([^/]+)/!o) {
print "<h3>HUH $1</h3>" if $debug;
	push @{$::packages{$1}}, $_[0];
	$::count++;
    }
}

sub findheader($$$) {
    my $text = shift;
    my $p = shift;
    my $f = shift;
    my $debuginfo = $p =~ s/-debuginfo$//;
    my $header = ($index =~ m!^.*<a href=.*?>\Q$p\E</a>.*?<td.*?>([^><]+)<!m)[0] || '';
    $header = "Debug information for $header" if $debuginfo;
    $header = "Source code for $header" if $f =~ /-src$/o;
    return $header;
}

sub include_virtual(@) {
    for my $f (@_) {
	open my $fd, '<', $f;
	myprint <$fd>;
	close $fd;
    }
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

