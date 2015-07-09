The gold star page is now generated from a page template and a database of awardees,
award types, and awards.  This is way easier and more consistent than the old method
of manually maintaining the page, which required a lot of typing of biolerplate HTML
and moving entries around.

To update the gold star page:

(1) cd src
(2) Add the new award entry(ies) to awards.csv.
(3) Add corresponding new entries to awardees.csv and award_types.csv, if needed.
(4) Run make. This will regenerate ../index.html.
(5) cd .. and commit the changes to CVS.

make runs make_awards_list.pl, which rebuilds index.html based on the contents of the following files:

awards.csv - list of awards: awardee, URL reference, description, and counts of each different
	award type awarded.
awardees.csv - list of people who've received awards: initials, name, and obfuscated email address.
award_types.csv - list of different award types: name, image file, and default award count.
index.html.tpl - template file for index.html. This is just index.html with a placeholder
	for where the award list should be inserted.

For each award, if all of the award counts are empty or missing, the default award counts
from award_types.csv are applied.  This allows you to skip entering a bunch of zeros or the
default single gold star in every award.

