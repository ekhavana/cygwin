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
print $html->header, $html->start_html(-title=>'Cygwin Package List Search Result',
				       -dtd=>['-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
				       -style=>'http://cygwin.com/style.css');
include_virtual "../navbar.html", "../top.html";

chdir("$Bin/../packages");
my $here = getcwd;
chdir dirname($file);
my $there = getcwd;
chdir $here;
if (substr($there, 0, length($here) + 1) ne "$here/" || !open(F, '<', $file)) {
    print $html->h1("Couldn't open file: $file");
} else {
    $_ = join('', <F>);
    s!($grep)!\<b\>$1\</b\>!mog if length($grep);
    print $_;
}

print <<'EOF';
</div>
</body>
</html>
EOF

sub include_virtual(@) {
    for my $f (@_) {
	open my $fd, '<', $f;
	print <$fd>;
	close $fd;
    }
}
