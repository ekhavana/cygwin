<?

/*
 * script to test a connection and selection of a database on
 * a MySQL server.
 */

$dbhost = "localhost";
$dbuser = "elfyn";
$dbpass = "";
$dbname = "cygwindb";

if (!($dbh = mysql_connect ($dbhost, $dbuser, $dbpass))) {
  printf ("Failed to connect to MySQL server `%s'", $dbhost);
  exit (1);
} elseif (!mysql_select_db ("cygwindb")) {
  printf ("Failed to select database `%s' on MySQL server `%s'", $dbname, $dbhost);
  exit (1);
} else {
  printf ("Connect to MySQL server `%s' as user `%s'", $dbhost, $dbuser);
}

?>
