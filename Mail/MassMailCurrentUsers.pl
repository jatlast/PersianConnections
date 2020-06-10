#!/usr/local/bin/perl -w

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

#use strict;

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "DatabaseFunctions.pl";
require "SendMailFunctions.pl";
require "UtilityFunctions.pl";

my $ProgramName = "MassMailCurrentUsers.pl";

my $DebugThisAp			   = "1";
my $DebugDatabaseFunctions = "0";
my $DebugMailSendFunctions = "0";
my $DebugUtilityFunctions  = "0";

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
		print "<!-- $Map{'CONFIG'} -->\n";
	}

# Log File Name...
my $RecoveryFile  = "Log/$Map{'MAIL_RECOVERY_FILE'}";

# Create and open the file that this program will populate...
open (RECOVERY_FILE, "> $RecoveryFile") || die "Can't open $RecoveryFile: $!\n";

my $Now = localtime();

print RECOVERY_FILE "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">\n";
print RECOVERY_FILE "<HTML>\n";
print RECOVERY_FILE "  <HEAD>\n";
print RECOVERY_FILE "    <TITLE>\n";
print RECOVERY_FILE "      	$ProgramName time out recovery file started at $Now\n";
print RECOVERY_FILE "    </TITLE>\n";
# Open in new JavaScript...
print RECOVERY_FILE"	 <SCRIPT type=\"text/javascript\" language=\"javascript\">\n";
print RECOVERY_FILE"	 <!--\n";
print RECOVERY_FILE"	 function newWindowGeneric(picName) \n";
print RECOVERY_FILE"	 {\n";
print RECOVERY_FILE"	 		var myWindow = window.open(picName, 'Guidelines', 'toolbar=no,location=no,scrollbars=yes,resizable=yes,width=850,height=1000')\n";
print RECOVERY_FILE"				myWindow.focus()\n";
print RECOVERY_FILE"	 }\n";
print RECOVERY_FILE"	 // -->\n";
print RECOVERY_FILE"	 </SCRIPT>\n";
	
print RECOVERY_FILE "  </HEAD>\n";
print RECOVERY_FILE "  <BODY>\n";
print RECOVERY_FILE "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"700\">\n";
print RECOVERY_FILE "            <TR align=\"left\">\n";
print RECOVERY_FILE "              <TD>\n";
print RECOVERY_FILE "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Results from sending multiple unique \"To:\" messages</STRONG></FONT>\n";
print RECOVERY_FILE "                  <BR>&nbsp;<BR>\n";
print RECOVERY_FILE "              </TD>\n";
print RECOVERY_FILE "            </TR>\n";


# Build email to send to the person receiving the new PC Mail...
my $BlatExe 		= "$Map{'BLAT_PATH'}/EXE/blat.exe ";
my $MailServer 		= $Map{'SMTP_HOST'};
my $SentFrom		= $Map{'EMAIL'};
my $BlatLog 		= "$Map{'LOG_FOLDER'}/Blat.log";

my $email			= "";
my $user_name		= "";
my $password		= "";

my $GoodMailCount 	= 0;
my $ErrorMailCount 	= 0;
my $Temp 		 	= "";

# Sql statement used to access the desired group to MAIL...
my $SqlStatement = $Map{'MAIL_SQL_STATEMENT'};

print RECOVERY_FILE "            <TR align=\"left\">\n";
print RECOVERY_FILE "              <TD>\n";
print RECOVERY_FILE "                  Mailing all users who are returned by the following SQL statement:\n";
print RECOVERY_FILE "                  <HR>\n";
print RECOVERY_FILE "                  $SqlStatement\n";
print RECOVERY_FILE "              </TD>\n";
print RECOVERY_FILE "            </TR>\n";
 
my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();

	
##########################
# Get Only result set...
##########################
# dbresults() must be called for each result set...
$status = $MSSQL::DBlib::dbh->dbresults();
if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
	{
		my $Count = 1;
		my $Bcc_Every = $Map{'MAIL_BCC_EVERY'}; #this is used with the modulus operator (%) to send a bcc mail every time (Bcc_Every % Count) == 0
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
			my $MaxCount = $Map{'MAIL_TOTAL_MAIL_TO_SEND'};
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					last if $Count > $MaxCount; 
						if($Count >= $Map{'MAIL_START_AFTER_MAIL_COUNT'}) # change this paramater to limit the number of mails sent
							{
								# Since there is no global DB error check if email address is valid
								if($$dataref{email} =~ m/^\@/ || $$dataref{email} !~ m/\@/ || $$dataref{email} eq "")
									{
										print "ERROR: ($$dataref{email}) Failed!\n";
									}
								else
									{
										$email = $$dataref{email};
										$email =~ s/\s//g;
											
										$user_name	= $$dataref{user_name};
										$password	= $$dataref{password};

										# Test...	
										if($Map{'MAIL_TEST_MODE'} eq "1")
    										{
												$email= $Map{'MAIL_TEST_MAIL'};
    										}
										
										my $BccAddress = $Map{'MAIL_BCC_MAIL'};
										
										my $Subject	= "Dear GLM Member,";
										my $Message = "$user_name,\n\n	we noticed that you were having trouble using our site as a free member. We would like to apologize for the inconvenience and let you know that we have fixed the problem with your account. It seems that whenever you tried to read profiles or your private mail the payment screen appeared in error.\n\nAll you need to do, in order to use all the features of the site for free, is upload a photo to your profile. Please come back and say hi to the other GLM members or just talk to a new friend using our LiveChat! application.\n\nRemember that GLM is completely free for all our members who upload a picture.\n\nPlease take a moment and go to $Map{'ROOT'}/login.html in order to log into your account then choose \"Manage You Pictures\" in the \"Update Profile\" section of your user homepage.\n\nYour login info is:\n\nUsername: $user_name\nPassword: $password\n\nOnce again we are sorry for the inconvenience.\n\nBest Wishes,\n\n$Map{'HTML_TITLE'} Management\n";
										
										my $return_code = "";
										# check if a status bcc mail should be sent...
										#print "Bcc_Every = $Bcc_Every\n";
										#print "mod = " . ($Count % $Bcc_Every) . "\n";
										if( ($Count % $Bcc_Every) == 0)
    										{
    										 	$return_code = &My_Send_Individual_Blat_Mail($BlatExe, $MailServer, $BlatLog, $SentFrom, $email, $BccAddress, $Subject, $Message);
    										}
										else
    										{
    										 	$return_code = &My_Send_Individual_Blat_Mail($BlatExe, $MailServer, $BlatLog, $SentFrom, $email, "", $Subject, $Message);
    										}

										if($return_code < 1)
											{
												$GoodMailCount++;
												print RECOVERY_FILE "<TR><TD>Sent Mail ($Count) to: $email</TD></TR>\n";
												print "($GoodMailCount) Sent mail to: ($email)\n";
											}
										else
											{
												$ErrorMailCount++;
												print RECOVERY_FILE "<TR><TD><FONT color=\"red\">Error!</FONT> Resend Mail ($Count): <A href=\"javascript:newWindowGeneric('$Map{'CGIBIN'}/Admin_GenSendMail.cgi?sent_from=$SentFrom&amp;sent_to=$email&amp;sent_bcc=&amp;subject=$Subject&amp;message_text=$Message')\">$email</A></TD></TR>\n";
												print "($ErrorMailCount) Error sending mail to: ($email)\n";
											}
									}# END else (valid Email Address)
							}# if count++ > 2240
						$Count++;
					}# END while != NO_MORE_ROWS
			}# END else (No db error) 
        }# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first result set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}
	
print RECOVERY_FILE "                    <TR>\n";
print RECOVERY_FILE "                      <TD>\n";
print RECOVERY_FILE "						   $GoodMailCount sent mail.\n";
print RECOVERY_FILE "                      </TD>\n";
print RECOVERY_FILE "                    </TR>\n";
print RECOVERY_FILE "                    <TR>\n";
print RECOVERY_FILE "                      <TD>\n";
print RECOVERY_FILE "						   $ErrorMailCount not sent mail.\n";
print RECOVERY_FILE "                      </TD>\n";
print RECOVERY_FILE "                    </TR>\n";
print RECOVERY_FILE "                    <TR>\n";
$Now = localtime();
print RECOVERY_FILE "                    <TR>\n";
print RECOVERY_FILE "                      <TD>\n";
print RECOVERY_FILE "						   End: $Now\n";
print RECOVERY_FILE "                      </TD>\n";
print RECOVERY_FILE "                    </TR>\n";
print RECOVERY_FILE "                    <!-- Close Window -->\n";
print RECOVERY_FILE "                    <TR>\n";
print RECOVERY_FILE "                      <TD>\n";
print RECOVERY_FILE "						   <INPUT TYPE=BUTTON VALUE=\"Close Window\" onClick=\"Closer()\">\n";
print RECOVERY_FILE "                      </TD>\n";
print RECOVERY_FILE "                    </TR>\n";
print RECOVERY_FILE "						  <SCRIPT type=\"text/javascript\" language=\"javascript\">\n";
print RECOVERY_FILE "						  <!--\n";
print RECOVERY_FILE "    					 		 function Closer()\n";
print RECOVERY_FILE "    							 {\n";
print RECOVERY_FILE "        						 	  window.close()\n";
print RECOVERY_FILE "    							 }\n";
print RECOVERY_FILE "						  //-->\n";
print RECOVERY_FILE "						 </SCRIPT>\n";
	
print RECOVERY_FILE "          </TABLE>\n";
print RECOVERY_FILE "        </TD>\n";
print RECOVERY_FILE "        <!-- End Main Data Cell -->\n";
print RECOVERY_FILE "      </TR>\n";
print RECOVERY_FILE "      <!-- End Navigation and Main Row -->\n";
print RECOVERY_FILE "    </TABLE>\n";
	
print RECOVERY_FILE "  </BODY>\n";
print RECOVERY_FILE "</HTML>\n";
	
close (RECOVERY_FILE);
	
sub My_Send_Individual_Blat_Mail
	{
		my($BlatPath, $MailServer, $BlatLogFilePath, $SentFrom, $SentTo, $BccFile, $Subject, $MessageText, %Map) = @_;
			
		my $TempFile		= "";
		my $TempFilePath 	= "C:\\Temp";
			
		(my $return_value, my $output)= &SendMailFunctions::Mail_Blat($BlatPath, $MailServer, $SentFrom, $SentTo, $BccFile, $Subject, $TempFile, $MessageText, $TempFilePath, $BlatLogFilePath, $DebugMailSendFunctions);
		if($return_value < 1)
			{
				return 0;
			}
		else
			{
				print "\n<!-- Mail_Blat Error return_value = $return_value \n output = $output\n-->\n" if $DebugThisAp eq "1";
				return 1;
			}
	}# END Send_Individual_Blat_Mail

exit 0;
