#!/usr/local/bin/perl -w
use CGI qw/:standard/;

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

use strict;

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "DatabaseFunctions.pl";
require "CgiFunctions.pl";
require "UtilityFunctions.pl";

my $DebugThisAp			   = "1";
my $DebugCgiFunctions 	   = "1";
my $DebugDatabaseFunctions = "1";
my $DebugUtilityFunctions  = "1";

my $ProgramName  = "Admin_GenSendMail.cgi";

#Begin HTML so errors show up in browser...
print CGI::header('text/html');
print "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/1999/REC-html401-19991224/loose.dtd\">\n";
print "<HTML>\n";

# Determine what libraries to use base on the execution dir...
my $CurrentFilePath = __FILE__;
# Initialize LinkMap Hash variable "Map"...
my %Map = &UtilityFunctions::Load_LinkMap($CurrentFilePath, 1); 

# Severe Error:  No LinkMap.dat file found -- EXIT --
if($Map{'CONFIG'} eq 'ERROR')
	{
		&UtilityFunctions::Print_Error("LinkMap Error.<BR><BR>Contact Site Administrator.", $DebugUtilityFunctions, %Map);
	}
else
	{
		$Map{'PROGRAM_NAME'} = $ProgramName;
		print "<!-- $Map{'CONFIG'} -->\n" if $DebugThisAp eq "1";
	}

# declare global variables...
my $sent_from 	 = "";
my $sent_to 	 = "";
my $sent_bcc 	 = "";
my $subject		 = "";
my $message_text = "";

if(CGI::param('sent_from'))   {$sent_from 	 = CGI::param('sent_from');}
if(CGI::param('sent_to'))	  {$sent_to 	 = CGI::param('sent_to');}
if(CGI::param('sent_bcc'))	  {$sent_bcc 	 = CGI::param('sent_bcc');}
if(CGI::param('subject'))	  {$subject    	 = CGI::param('subject');}
if(CGI::param('message_text')){$message_text = CGI::param('message_text');}

# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);

if($message_text =~ m/duplicate_profiles/)
	{
	 	my $Duplicates = "\n\n";
		
		my $SqlStatement = "SELECT user_name FROM login_info where email = '$sent_to'";
		my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
		$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
		$status = $MSSQL::DBlib::dbh->dbsqlexec();
		
		##########################
		# Get ONLY result set...
		##########################
		# dbresults() must be called for each result set...
		$status = $MSSQL::DBlib::dbh->dbresults();
		if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
			{
				if($DebugThisAp eq "1")
					{
						print "<!-- SUCCESS: $SqlStatement returned with dbresults status = ($status). -->\n";
					}
				my %dataref = ("jason" => "baumbach");
				my $dataref = \%dataref;
				# If in debug mode, print information...
				if($DebugThisAp == 1)
					{
						print "<!-- SQL: $SqlStatement -->\n";
					}
				# Check for global DB error...
				if($DatabaseFunctions::DatabaseError eq "1")
					{
						print "ERROR: ($SqlStatement) Failed!<BR>\n";
					}
				else
					{
						# Prevent infinite loop...
						while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
							{
								# Since there is no global DB error check get 
								# all database fields returned by the query...
								
								my $UserName = $$dataref{user_name};
								# Build string that will replace "duplicate_profiles" in the "message_text" variable...
								$Duplicates = $Duplicates . "User Name:\t" . $UserName . "\n";
								
								if($DebugThisAp eq "1")
									{
										print "<!-- user_name = ($UserName) -->\n";
										print "<!-- Duplicates = ($Duplicates) -->\n";
									}
							}
					}# END else (No db error) 
				$Duplicates = $Duplicates . "\n";
				$message_text =~ s/duplicate_profiles/$Duplicates/g;			
			}# END if($status != FAIL)
		else
			{
				print "ERROR: $SqlStatement Failed for first result set!\n";
				$status = $MSSQL::DBlib::dbh->dbcancel();
			}
	}# End check to see if we need to look for duplicates in the DB

print "  <!-- Begin Entire Body NOT Logged In-->\n";
print "  <BODY>\n";
print "    <!-- Begin Main Table -->\n";
print "    <TABLE width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
print "      <!-- Begin Main Data Cell -->\n";
print "      <TR>\n";
print "        <TD bgcolor=$Map{'HTML_BODY_BGCOLOR'}>\n";
print "    	     <TABLE width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
print "            <TR align=\"center\">\n";
print "              <TD>\n";
print "                  <FONT color=\"#FFFFFF\" face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>$Map{'WHICH_CONNECTIONS'}</STRONG></FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
print "            <TR align=\"center\">\n";
print "              <TD>\n";
print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Admin Mail Page</STRONG></FONT>\n";
print "                  <BR>&nbsp;<BR>\n";
print "              </TD>\n";
print "            </TR>\n";
print "            <TR>\n";
print "              <TD>\n";
print "                <FORM method=\"POST\" action=\"Admin_SendMail.cgi\">\n";
print "    			     <TABLE width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
# sent_from field...
print "                    <!-- sent_from -->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "                        <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"><STRONG>From:</STRONG>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</FONT>\n";
print "						   <SELECT size=\"1\" name=\"sent_from\">\n";
print "                          <OPTION SELECTED>$sent_from</OPTION>\n";

for(my $j=1; $j<=$Map{'NUMBER_OF_MAIL_SENT_FROM'}; $j++)
	{
		my $from_option = 'ADMIN_MAIL_SENT_FROM_' . $j;
		# Add syntax highlighting for flagged words...
		print "                          <OPTION>$Map{$from_option}</OPTION>\n";
	}

print "                        </SELECT>\n";
print "                  	<BR>&nbsp;<BR>\n";
print "                      </TD>\n";
print "                    </TR>\n";
# sent_to field...
print "                    <!-- sent_to -->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "                        <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"><STRONG>To:</STRONG>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</FONT>\n";
print "						   <SELECT size=\"1\" name=\"sent_to\">\n";
print "                          <OPTION selected>$sent_to</OPTION>\n";
# if not an email address...
if($sent_to !~ m/@/)
	{
		for(my $j=1; $j<=$Map{'NUMBER_OF_MAIL_SENT_TO'}; $j++)
			{
				my $to_option = 'ADMIN_MAIL_SENT_TO_' . $j;
				# Add syntax highlighting for flagged words...
				print "                          <OPTION>$Map{$to_option}</OPTION>\n";
			}
		print "                        </SELECT>\n";
		print "						   <BR><FONT color=\"blue\" face=\"Arial, Helvetica, sans-serif\" size=\"-3\">If a single email is selected only that person will receive the message regardless of the \"Bcc:\" field below.\n";
		print "						   <BR>Otherwise send each user, returned by the selected query, a unique message replacing key words (user_name and last_name).</FONT>\n";
		print "                  	   <BR>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
	}
else
	{
		print "                        </SELECT>\n";
		print "                  	   <BR>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
	}
if($sent_bcc ne "")
	{
		# sent_bcc field...
		print "                    <!-- sent_bcc -->\n";
		print "                    <TR>\n";
		print "                      <TD>\n";
		print "                        <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"><STRONG>Bcc:</STRONG>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</FONT>\n";
		print "						   <SELECT size=\"1\" name=\"sent_bcc\">\n";
		print "                          <OPTION selected>$sent_bcc</OPTION>\n";
		
		for(my $j=1; $j<=$Map{'NUMBER_OF_MAIL_SENT_TO'}; $j++)
			{
				my $bcc_option = 'ADMIN_MAIL_SENT_TO_' . $j;
				# Add syntax highlighting for flagged words...
				print "                          <OPTION>$Map{$bcc_option}</OPTION>\n";
			}
			
		print "                        </SELECT>\n";
		print "						   <BR><FONT color=\"blue\" face=\"Arial, Helvetica, sans-serif\" size=\"-3\">Blind copy all users returned by the selected query using a single email message.\n";
		print "						   <BR>If blank the above \"To:\" field must contain a selection.</FONT>\n";
		print "                  	<BR>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
	}
# subject field...
print "                    <!-- subject -->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "                        <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"><STRONG>Subject:&nbsp;</STRONG>\n";
print "						   <INPUT type=\"text\" maxlength=\"128\" size=\"65\" name=\"subject\" wrap=\"none\" value=\"$subject\"></FONT>\n";
print "                  	<BR>&nbsp;<BR>\n";
print "                      </TD>\n";
print "                    </TR>\n";
# message_text field...
print "                    <!-- message_text-->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "                        <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"><STRONG>Text:</STRONG></FONT><BR>\n";
print "						   <TEXTAREA rows=\"20\" cols=\"65\" name=\"message_text\" wrap=\"none\">$message_text</TEXTAREA>\n";
print "                      </TD>\n";
print "                    </TR>\n";
# submit button...
print "                    <!-- submit -->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "                        <INPUT type=\"submit\" value=\"Submit\" name=\"submit\">\n";
# close window button...
print "                    <!-- close window -->\n";
print "						   <INPUT TYPE=BUTTON VALUE=\"Cancel\" onClick=\"Closer()\">\n";
print "                      </TD>\n";
print "                    </TR>\n";
print "						  <SCRIPT type=\"text/javascript\" language=\"javascript\">\n";
print "						  <!--\n";
print "    					 		 function Closer()\n";
print "    							 {\n";
print "        						 	  window.close()\n";
print "    							 }\n";
print "						  //-->\n";
print "						 </SCRIPT>\n";
print "                  </TABLE>\n";
print "                </FORM>\n";
print "              </TD>\n";
print "            </TR>\n";
print "          </TABLE>\n";
print "        </TD>\n";
print "        <!-- End Main Data Cell -->\n";
print "      </TR>\n";
print "      <!-- End Navigation and Main Row -->\n";
print "    </TABLE>\n";

# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom($ProgramName, "ASC", "DESC", 0, 1, 0, $DebugUtilityFunctions, %Map);

#End HTML...
print "</HTML>\n";
exit 0;

	