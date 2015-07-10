#!/usr/bin/env perl

use strict;
use warnings;

use constant AWARDEES    => 'awardees.csv';
use constant AWARD_TYPES => 'award_types.csv';
use constant AWARDS      => 'awards.csv';

# Token in the input template to be replaced by the list of awards:
use constant LIST_TOKEN => '__LIST_OF_AWARDS__';

# More than this many stars are printed as "x N": 
use constant MAX_STARS => 5;

use Data::Dumper;
use POSIX qw(strftime);
use Text::CSV;

my $csv = Text::CSV->new();

# Read award types

$csv->column_names('Name','Image','Alt','Default Count','Field Order');
open(my $f_award_types, "grep -Ev '^\\s*(#|\$)' @{[ AWARD_TYPES ]} |")
	or die "Can't read @{[ AWARD_TYPES ]}: $!";
my @award_types = @{ $csv->getline_hr_all($f_award_types, 1) }
	or die "Can't parse CSV in @{[ AWARD_TYPES ]}: $!";
close $f_award_types;

my (%award_types);
foreach my $a (@award_types) {
	my $name = $a->{Name};
	delete $a->{Name};
	$a->{'Default Count'} ||= 0;
	$a->{'Alt'} ||= '';
	$a->{'img_html'} = "<img src=\"$a->{Image}\" alt=\"$a->{Alt}\" />";
	$award_types{$name} = $a;
}
my @award_type_names = sort { $award_types{$a}{'Field Order'} <=> $award_types{$b}{'Field Order'} } keys %award_types;

#print Data::Dumper->Dump([\%award_types], ['%award_types']);
#exit;

# Read awardees

$csv->column_names('Initials','Name','Email');
open(my $f_awardees, "grep -Ev '^\\s*(#|\$)' @{[ AWARDEES ]} |")
	or die "Can't read @{[ AWARDEES ]}: $!";
my @awardees = @{ $csv->getline_hr_all($f_awardees, 1) }
	or die "Can't parse CSV in @{[ AWARDEES ]}: $!";
close $f_awardees;

my %awardees;
foreach my $a (@awardees) {
	my $name = $a->{Initials};
	if (defined $awardees{$name}) {
		die "Awardee initials $name are used twice in @{[ AWARDEES ]}";
	}
	delete $a->{Initials};
	$a->{latest_date} = '';
	$awardees{$name} = $a;
}

#print join "\n", sort keys %awardees;
#print Data::Dumper->Dump([\%awardees], ['%awardees']);
#exit;

# Read awards

$csv->column_names('Awardee','URL','Description', @award_type_names);
open(my $f_awards, "grep -Ev '^\\s*(#|\$)' @{[ AWARDS ]} |")
	or die "Can't read @{[ AWARDS ]}: $!";
my @awards = @{ $csv->getline_hr_all($f_awards, 1) }
	or die "Can't parse CSV in @{[ AWARDS ]}: $!";
close $f_awards;

#print Data::Dumper->Dump([\@awards], ['@awards']);
#exit;

# Compile awards by awardee

my $line = 1;
foreach my $award (@awards) {
	++$line;
	# Set zeros for missing award counts
	$award->{$_} ||= 0 foreach @award_type_names;
	# Assign default award(s) if all award count fields are zero/empty/missing
	if (! grep $award->{$_}, @award_type_names) {
		foreach my $type (@award_type_names) {
			$award->{$type} = $award_types{$type}{'Default Count'};
		}
	}

	# Get the award date, used for sorting awardees by latest award 
	# and for sorting awards within each awardee. 
	# The "date" is actually just a part of the award URL (yyyy-mm-nnnnn, where
	# nnnnn is the sequence number within each month on one of the cygwin mailing lists).
	# This is close enough for sorting, except that sequence #s from the two lists
	# generally won't sort correctly together within each month.  Oh well.
	if ($award->{URL} =~ m{/ml/cygwin(?:|-\w+)/(\d+)-(\d+)/msg(\d+)}) {
		$award->{date} = "$1-$2-$3";
	}
	elsif ($award->{URL} =~ m{/ml/cygwin(?:|-\w+)/(\d+)-q(\d)/msg(\d+)}) {
		my %month = ('1' => '03', '2' => '06', '3' => '09', '4' => '12');
		$award->{date} = "$1-$month{$2}-$3";
	}
	else {
		warn "@{[ AWARDS ]} line $line: Can't determine date from award URL";
	}

	# Assign to awardee
	my $awardee = $award->{Awardee};
	if (! defined($awardees{$awardee})) {
		die "@{[ AWARDS ]} line $line: Awardee $awardee not found in @{[ AWARDEES ]}. Create an entry for $awardee in @{[ AWARDEES ]} and try again";
	}
	push @{$awardees{$awardee}{awards}}, $award;
	# Track latest award date for this awardee:
	if (defined($award->{date}) && $award->{date} gt ($awardees{$awardee}{latest_date} || '')) {
		$awardees{$awardee}{latest_date} = $award->{date};
	}
}

#print Data::Dumper->Dump([\%awardees], ['%awardees']);
#exit;

# Create the list of awards.
# Latest awardee first; sort by increasing date within each awardee.

my @list;
push @list, '<ul>';

# For each awardee (latest first):
foreach my $initials (sort { $awardees{$b}{latest_date} cmp $awardees{$a}{latest_date} } keys %awardees) {

	my %awardee = %{$awardees{$initials}};
	next unless defined $awardee{awards};

	# Print awardee header
	push @list, "<li><a name=\"$initials\"" . (defined($awardee{Email}) ? " href=\"mailto:$awardee{Email}\"" : '') 
		. ">$awardee{Name}</a>";

	# Print list of awards
	my $last_award;
	foreach my $award (sort { $a->{date} cmp $b->{date} } @{$awardee{awards}}) {
		$last_award = $award;
		my $text = "<a href=\"$award->{URL}\">";
		foreach my $type (@award_type_names) {
			my $nawards = $award->{$type};
			if ($nawards > MAX_STARS) {
				$text .= "$award_types{$type}{img_html}<span class=\"times\">&times;&nbsp;$nawards</span>";
			}
			else {
				$text .= $award_types{$type}{img_html} x $award->{$type};
			}
		}
		my ($y, $m) = $award->{date} =~ /^(\d+)-(\d+)/;
		$text .= '</a> <span class="date">(' . strftime('%b %Y', 0, 0, 0, 1, $m-1, $y-1900) . ')</span>';
		push @list, $text;
	}
	# Append description of the last award only, for now
	push @list, "&ndash; $last_award->{Description}" if $last_award->{Description};

	push @list, '', '</li>';
}

push @list, '</ul>';

# Read the input template, substitute the list, print result

my $list = join "\n", @list;
while (<>) {
	s/@{[ LIST_TOKEN ]}/$list/o;
	print;
}

