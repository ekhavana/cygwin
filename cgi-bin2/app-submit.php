<?
# Copyright 2003 Daniel Reed <n@ml.org>
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 2 of the License, or (at your option) any later 
# version.

# TODO
# Have $templates[] replaced with individual template .txt files.
# I would like to extend this to send an email-confirmation to the supposed 
#  maintainer, which they will simply reply to confirm it as legitimate (similar 
#  to how ezmlm confirms mailing list subscriptions).
# I could further integrate this into ~nmlorg/staging/ (which handles pulling, 
#  auto-reviewing, and uploading package updates) and send a second confirmation 
#  mail to the maintainer when the package is uploaded: When the maintainer 
#  replies to that second confirmation, a message would be sent to 
#  cygwin-announce on their behalf. This second confirmation would include a URL 
#  to this script with the relevant information encoded, so the maintainer could 
#  modify the -announce message contents instead of simply accepting the 
#  default.
# [cosmetic] mywordwrap() requires that lines are always preceded by a blank 
#  line. This is not a major problem, but requires the templates to have blank 
#  lines between From: and To: and Subject:, and between the three URLs, which 
#  is just aesthetically displeasing.
# [cosmetic] It might be nicer to have each Submit button correspond to a 
#  separate <form>, with a lot if <input type="hidden">'s to keep relevant data 
#  intact for the subsequent forms. This would allow people to correct mistakes 
#  without having to go Back first.

	$_REQUEST2 = array();
	while (list($key, $val) = each($_REQUEST))
		$_REQUEST2[$key] = stripslashes($val);
	$_REQUEST = $_REQUEST2;

	$step1ar = array(
		"PACKAGE_NAME"		=> 'The printed name of the package.',
		"SUBMISSION_TYPE"	=> 'new,update,correction,announce:Format for a new package, update to a new vendor version, correction for a broken package, or announcement to cygwin-announce.',
	);
	$step2ar = array(
		"PACKAGE_TARNAME"	=> 'The name of the package as it will appear in setup.exe (typically the same as PACKAGE_NAME with lowercase letters, and spaces replaced with hyphens or underscores).',
		"PACKAGE_VERSION"	=> 'The current/new version of the package.',
		"PACKAGE_RELEASE"	=> 'The Cygwin-specific release number of the package.',
		"PACKAGE_TEASER"	=> 'The teaser line summarizing the package (sdesc in setup.hint).',
		"PACKAGE_DESCRIPTION"	=> 'The full description of the package (ldesc in setup.hint).',
		"PACKAGE_BUGREPORT"	=> 'The prefered means of contacting the package maintainer regarding problems (cygwin@cygwin.com, your email address, or a separate bug-report address).',
	);
	$templates = array(
		"new" =>  "From: You <your@email.address>\n"
			. "\n"
			. "To: cygwin-apps@cygwin.com\n"
			. "\n"
			. "Subject: New: @PACKAGE_NAME@ @PACKAGE_VERSION@\n"
			. "\n"
			. "I am pleased to announce the availability of @PACKAGE_NAME@ @PACKAGE_VERSION@ for the Cygwin Net Release.\n"
			. "\n"
			. "@PACKAGE_DESCRIPTION@\n"
			. "\n"
			. "@PACKAGE_TARNAME@-@PACKAGE_VERSION@-@PACKAGE_RELEASE@ is available from:\n"
			. "\n"
			. "sdesc: @PACKAGE_TEASER@\n"
			. "\n"
			. "BIN http://\n"
			. "\n"
			. "SRC http://\n"
			. "\n"
			. "HINT http://\n"
			. "\n"
			. "Please let me know if you have any problems with the packaging.\n"
			. "\n"
			. "Thanks.",
		"update" =>
			  "From: You <your@email.address>\n"
			. "\n"
			. "To: cygwin-apps@cygwin.com\n"
			. "\n"
			. "Subject: Update: @PACKAGE_NAME@ @PACKAGE_VERSION@\n"
			. "\n"
			. "I have updated the @PACKAGE_NAME@ package to the new vendor version @PACKAGE_VERSION@. Please upload at your earliest convenience.\n"
			. "\n"
			. "@PACKAGE_TARNAME@-@PACKAGE_VERSION@-@PACKAGE_RELEASE@ is available from:\n"
			. "\n"
			. "BIN http://\n"
			. "\n"
			. "SRC http://\n"
			. "\n"
			. "HINT http://\n"
			. "\n"
			. "Thanks.",
		"correction" =>
			  "From: You <your@email.address>\n"
			. "\n"
			. "To: cygwin-apps@cygwin.com\n"
			. "\n"
			. "Subject: Update: @PACKAGE_NAME@ @PACKAGE_VERSION@-@PACKAGE_RELEASE@\n"
			. "\n"
			. "I have updated the @PACKAGE_NAME@ package to @PACKAGE_VERSION@-@PACKAGE_RELEASE@. Please upload at your earliest convenience.\n"
			. "\n"
			. "[CHANGEME: A partial list of what was wrong with the earlier submission.]\n"
			. "\n"
			. "@PACKAGE_TARNAME@-@PACKAGE_VERSION@-@PACKAGE_RELEASE@ is available from:\n"
			. "\n"
			. "BIN http://\n"
			. "\n"
			. "SRC http://\n"
			. "\n"
			. "HINT http://\n"
			. "\n"
			. "Thanks.",
		"announce" =>
			  "From: You <your@email.address>\n"
			. "\n"
			. "To: cygwin-announce@cygwin.com\n"
			. "\n"
			. "Subject: Update: @PACKAGE_NAME@ @PACKAGE_VERSION@-@PACKAGE_RELEASE@\n"
			. "\n"
			. "I have updated the @PACKAGE_NAME@ package to @PACKAGE_VERSION@-@PACKAGE_RELEASE@.\n"
			. "\n"
			. "@PACKAGE_DESCRIPTION@\n"
			. "\n"
			. "[CHANGEME: The full list of what the submission contains. For example, condensed ChangeLog entries for this version, or what you changed for this release. If this is an announcement for a new package, this may be blank.]\n"
			. "\n"
			. "To update your installation, click on the \"Install Cygwin now\" link on the http://cygwin.com/ web page. This downloads setup.exe to your system. Then, run setup and answer all of the questions.\n"
			. "\n"
			. "To install @PACKAGE_NAME@ for the first time, choose \"@PACKAGE_TARNAME@\" from the packages list, in the \"@PACKAGE_CATEGORY@\" category. If you already have @PACKAGE_NAME@ installed, the update will be pre-selected.\n"
			. "\n"
			. "Remember that some mirror sites may not have updated before this announcement is made. If your usual mirror does not have the latest version of this package, please be patient or select an alternate mirror.\n"
			. "\n"
			. "If you have general questions or comments, please send them to <@PACKAGE_BUGREPORT@>. I would appreciate it if you would use this address rather than emailing me directly.\n"
			. "\n"
			. "Thanks.",
	);

	$step1 = true;
	reset($step1ar);
	while (list($key, $val) = each($step1ar))
		if (!isset($_REQUEST[$key]))
			$step1 = false;
	$step2 = true;
	reset($step2ar);
	while (list($key, $val) = each($step2ar))
		if (!isset($_REQUEST[$key]))
			$step2 = false;

	function mywordwrap($str) {
		$str = str_replace("\r\n", "\n", $str);
		$str = str_replace("\n\n", "@PARAGRAPH@", $str);
		$str = str_replace("\n", " ", $str);
		$str = str_replace("@PARAGRAPH@", "\n\n", $str);
		return(wordwrap($str));
	}

	function dosubs($str) {
		global	$_REQUEST;

		while (list($key, $val) = each($_REQUEST))
			if ($val != "")
				$str = str_replace("@" . $key . "@", $val, $str);
		return($str);
	}

	function grab_maintainer($line) {
		if (strstr($line, "<"))
			$maintainer = preg_replace("#^.* <(.*)>$#", "\$1", $line);
		else if (strstr($line, "("))
			$maintainer = preg_replace("#^(.*) \(.*\)$#", "\$1", $line);
		else
			$maintainer = $line;
		$maintainer = str_replace(" at ", "@", $maintainer);
		$maintainer = str_replace(" dot ", ".", $maintainer);
		return($maintainer);
	}

	function grabhint($name) {
		$name = strtolower($name);
		$name = str_replace("_", "", $name);
		$name = str_replace("-", "", $name);
		$name = str_replace(" ", "", $name);

		$inname = false;
		$info = array();

		$fd = fopen("/sourceware/ftp/anonftp/pub/cygwin/setup.ini", "r");
		while ($line = fgets($fd)) {
			$line = trim($line);
			if ($inname && ($line == ""))
				break;
			else if ($line[0] == "@") {
				$cur = substr($line, 2);
				$cur = strtolower($cur);
				$cur = str_replace("_", "", $cur);
				$cur = str_replace("-", "", $cur);
				$cur = str_replace(" ", "", $cur);

				if ($cur == $name) {
					$info["tarname"] = substr($line, 2);
					$inname = true;
				}
			} else if ($inname) {
				if ($line[0] == "[")
					break;
				$what = strtok($line, ":");
				$rest = trim(strtok(""));
				if ($rest[0] == '"') {
					$rest = substr($rest, 1);
					if (!strchr(substr($rest, 1), '"'))
						while ($line = fgets($fd)) {
							$rest .= " " . trim($line);
							if ($rest[strlen($rest)-1] == '"')
								break;
						}
					$rest = substr($rest, 0, strlen($rest)-1);
				}
				$info[$what] = $rest;
			}
		}
		fclose($fd);

		return($info);
	}

	function printsubs($subs) {
		global	$_REQUEST;

		while (list($key, $desc) = each($subs)) {
			echo mywordwrap($key . " " . $desc) . "\n";
			$prefix = strtok($key, "_");
			$suffix = strtok("");
			if ($suffix == "DESCRIPTION")
				echo "<textarea name=\"" . $key . "\" rows=5 cols=76>" . htmlentities(mywordwrap($_REQUEST[$key], 76)) . "</textarea>\n";
			else if ($suffix == "TYPE") {
				$vals = strtok($desc, ":");
				$desc = strtok("");
				$poss = strtok($vals, ",");
				do {
					echo "<input type=\"radio\" name=\"" . $key . "\" value=\"" . $poss . "\"";
					if ($_REQUEST[$key] == $poss)
						echo " checked=checked";
					echo "> " . ucwords($poss) . "\n";
				} while ($poss = strtok(","));
			} else if ($suffix == "TEASER")
				echo "<input name=\"" . $key . "\" size=60 value=\"" . htmlentities($_REQUEST[$key]) . "\">\n";
			else
				echo "<input name=\"" . $key . "\" size=20 value=\"" . htmlentities($_REQUEST[$key]) . "\">\n";
			echo "\n";
		}
		echo "<input type=\"submit\">\n\n";
	}

	echo "<pre>\n";
	echo "<form action=\"app-submit.php\" method=\"POST\">\n";

	printsubs($step1ar);
	if ($step1) {
		if (!isset($_REQUEST["PACKAGE_TARNAME"]))
			$_REQUEST["PACKAGE_TARNAME"] = str_replace(" ", "-", strtolower($_REQUEST["PACKAGE_NAME"]));
		$hint = grabhint($_REQUEST["PACKAGE_NAME"]);
		if (sizeof($hint) == 0)
			$hint = grabhint($_REQUEST["PACKAGE_TARNAME"]);
		if (sizeof($hint) > 0) {
			$ver = strtok($hint["version"], "-");
			$rel = 0+strtok("");
			$sdesc = $hint["sdesc"];
			$ldesc = $hint["ldesc"];
			$category = strtok($hint["category"], " ");
			if (($_REQUEST["SUBMISSION_TYPE"] == "update") && (strlen($ver) > 1)) {
				$i = strlen($ver)-1;
				while (($i > 0) && ctype_digit($ver[$i]))
					$i--;
				if (!ctype_digit($ver[$i]))
					$i++;
				$ver = substr($ver, 0, $i) . (1+substr($ver, $i));
				$rel = 1;
			} else if ($_REQUEST["SUBMISSION_TYPE"] == "correction")
				$rel++;
			$_REQUEST["PACKAGE_TARNAME"] = $hint["tarname"];
		}
		if ($rel == 0)
			$rel = 1;

		if (!isset($_REQUEST["PACKAGE_VERSION"]))
			$_REQUEST["PACKAGE_VERSION"] = $ver;
		if (!isset($_REQUEST["PACKAGE_RELEASE"]))
			$_REQUEST["PACKAGE_RELEASE"] = $rel;
		if (!isset($_REQUEST["PACKAGE_TEASER"]))
			$_REQUEST["PACKAGE_TEASER"] = $sdesc;
		if (!isset($_REQUEST["PACKAGE_DESCRIPTION"]))
			$_REQUEST["PACKAGE_DESCRIPTION"] = $ldesc;
		if (!isset($_REQUEST["PACKAGE_BUGREPORT"]))
			$_REQUEST["PACKAGE_BUGREPORT"] = 'cygwin@cygwin.com';
		if (!isset($_REQUEST["PACKAGE_CATEGORY"]))
			$_REQUEST["PACKAGE_CATEGORY"] = $category;
		printsubs($step2ar);
	}
	if ($step2) {
		if (!isset($_REQUEST["MESSAGE_CONTENTS"]))
			$message = dosubs($templates[$_REQUEST["SUBMISSION_TYPE"]]);
		else
			$message = dosubs($_REQUEST["MESSAGE_CONTENTS"]);
		echo wordwrap("Feel free to paste this into an email of your own, or continue and I will send it for you.\n");
		echo "<textarea name=\"MESSAGE_CONTENTS\" rows=20 cols=76>" . htmlentities(mywordwrap($message, 76)) . "</textarea>\n";
		echo "<input type=\"submit\">\n\n";
	}
	if (isset($_REQUEST["MESSAGE_CONTENTS"])) {
		$message = $_REQUEST["MESSAGE_CONTENTS"];
		$message = str_replace("\r\n", "\n", $message);
		$message = trim($message);
		$messagear = explode("\n", $message);
		do {
			$from = array_shift($messagear);
		} while ((sizeof($messagear) > 0) && ($from == ""));
		$from = str_replace("From: ", "", $from);
		do {
			$to = array_shift($messagear);
		} while ((sizeof($messagear) > 0) && ($to == ""));
		$to = str_replace("To: ", "", $to);
		do {
			$subject = array_shift($messagear);
		} while ((sizeof($messagear) > 0) && ($subject == ""));
		$subject = str_replace("Subject: ", "", $subject);
		while ($messagear[0] == "")
			array_shift($messagear);
		$message = implode("\n", $messagear);

		echo wordwrap("Please confirm the following information then Submit to send to &lt;" . $to . "&gt;.\n");
		echo htmlentities("From: " . $from) . "\n";
		echo htmlentities("To: " . $to) . "\n";
		echo htmlentities("Subject: " . $subject) . "\n";
		echo "\n";
		echo htmlentities(mywordwrap($message, 80));
		echo "\n<input type=\"hidden\" name=\"final\" value=\"done\">";
		echo "<input type=\"submit\">\n\n";
		if (isset($_REQUEST["final"])) {
			if ($_SERVER["REMOTE_HOST"] != "")
				$received = "from " . $_SERVER["REMOTE_HOST"] . " (" . $_SERVER["REMOTE_ADDR"] . ")\r\n  by " . $_SERVER["SERVER_NAME"] . " with HTTP; " . date("r");
			else
				$received = "from " . $_SERVER["REMOTE_ADDR"] . "\r\n  by " . $_SERVER["SERVER_NAME"] . " with HTTP; " . date();
			$headers = "Received: " . $received . "\r\n"
				. "From: " . $from . "\r\n";
			if (($from != "") && ($subject != "") && ($to != ""))
				mail($to, $subject, $message, trim($headers), "-f" . grab_maintainer($from));
		}
	}

	echo "</form>\n";
	echo "</pre>\n";
?>
