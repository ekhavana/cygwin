all: ../index.html

../index.html: make_awards_list.pl index.html.tpl awardees.csv awards.csv award_types.csv
	perl make_awards_list.pl < index.html.tpl > ../index.html
	chmod +x ../index.html
