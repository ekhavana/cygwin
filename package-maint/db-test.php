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
  printf ("connection failed for user `%s' on server `%s': %s", $dbuser, $dbhost, mysql_error ());
  exit (1);
} elseif (!mysql_select_db ($dbname)) {
  printf ("selection failed for database `%s' on server `%s;@ %s", $dbname, $dbhost, mysql_error ());
  exit (1);
} else {
  printf ("successfully connected to server `%s' as user `%s'", $dbhost, $dbuser);
}

?>
