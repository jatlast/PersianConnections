#!/usr/local/bin/perl -w

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
require "SendMailFunctions.pl";
require "UtilityFunctions.pl";

my $ProgramName = "Admin_BatchMailUsersBeforeRebilling.pl";

my $DebugThisAp			   = "0";
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
		print "<!-- $Map{'SYSTEM'} -->\n";
	}

# Parse the current date...
(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst) = localtime(time);
# use parsed date to create unique name for the RECOVERY_FILE...
# Unique Name has the folling format Admin_BatchUnreadMail_m[m]_d[d]_yyyy_h[h]_m[m]_s[s]
my $UniqueID = "Admin_BatchRebillReminder_"  . ($mon+1)  . "_" . $mday  . "_" . ($year+1900) . "_" . $hour  . "_" . $min . "_" . $sec;
# use parsed date to create unique file name for RECOVERY_FILE file...
my $UniqueRecoveryFile = "$Map{'LOG_FOLDER'}/"  . $UniqueID . ".html";

# Create and open the file that this program will populate...
open (RECOVERY_FILE, "> $UniqueRecoveryFile") || die "Can't open $UniqueRecoveryFile: $!\n";

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
print RECOVERY_FILE "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Results from sending multiple unique \"To:\" messages to users due for rebilling within 7 days.</STRONG></FONT>\n";
print RECOVERY_FILE "                  <BR>&nbsp;<BR>\n";
print RECOVERY_FILE "              </TD>\n";
print RECOVERY_FILE "            </TR>\n";


# Build email to send to the person receiving the new PC Mail...
my $BlatExe 		= "$Map{'BLAT_PATH'}/EXE/blat.exe ";
my $MailServer 		= "$Map{'SMTP_HOST'}";
my $BlatLog 		= "$Map{'BLAT_PATH'}/LOG/Blat.log";

my $SentFrom 		= "";

my $GoodMailCount 	= 0;
my $ErrorMailCount 	= 0;
my $Temp 		 	= "";

my $user_name	 				= "";
my $date_of_next_transaction	= "";
my $days_until_next_transaction	= "";
my $last_four_digits 			= "";
my $rebilling_amount 			= "";
my $card_expires				= "";
my $user_logged_in_this_month	= "";
my $membership_type				= "";
my $password					= "";
my $email						= "";
my $sex							= "";
my $days_since_last_login		= "";
my $email_verification_code		= "";
my $is_email_verified			= "";

my $RootURL	= "";
my $WebName	= "";
my $Message = "";

# Sql statement used to access the desired group to SPAM...
my $SqlStatement = 'admin_BatchMailUsersBeforeRebilling';

print RECOVERY_FILE "            <TR align=\"left\">\n";
print RECOVERY_FILE "              <TD>\n";
print RECOVERY_FILE "                  Mailing all users who are returned by the following SQL statement:\n";
print RECOVERY_FILE "                  <HR>\n";
print RECOVERY_FILE "                  $SqlStatement\n";
print RECOVERY_FILE "              </TD>\n";
print RECOVERY_FILE "            </TR>\n";
 
my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "RebillWarningMail");
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
		my $Bcc_Every = 1; #this is used with the modulus operator (%) to send a bcc mail every time (Bcc_Every % Count) == 0
		my %dataref = ("jason" => "baumbach");
		my $dataref = \%dataref;
		# If in debug mode, print information...
		if($DebugThisAp == 1)
			{
				print RECOVERY_FILE "<!-- SQL: $SqlStatement -->\n";
			}
		# Check for global DB error...
		if($DatabaseFunctions::DatabaseError eq "1")
			{
				print RECOVERY_FILE "ERROR: ($SqlStatement) Failed!<BR>\n";
			}
		else
			{

			my $MaxCount = 10000;
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					last if $Count > $MaxCount; 
						if($Count >= 0) # change this paramater to limit the number of mails sent
							{
								# Get info from DB...
								$email = $$dataref{email};
#								$email = 'jatlast@hotmail.com';
								# Since there is no global DB error check if email address is valid
								if($email !~ m/\@/g || $email eq "")
									{
										print RECOVERY_FILE "\n<!-- Email ERROR: user_name = ($user_name) dataref{email} = ($$dataref{email}) -->\n";
										$ErrorMailCount++;
									}
								else
									{
										$user_name	 				 = $$dataref{user_name};
										$date_of_next_transaction	 = $$dataref{date_of_next_transaction};
										$days_until_next_transaction = $$dataref{days_until_next_transaction};
										$last_four_digits 			 = $$dataref{last_four_digits};
										$rebilling_amount 			 = $$dataref{rebilling_amount};
										$card_expires				 = $$dataref{card_expires};
										$user_logged_in_this_month	 = $$dataref{user_logged_in_this_month};
										$membership_type			 = $$dataref{membership_type};
										$password					 = $$dataref{password};
										$sex						 = $$dataref{sex};
										$days_since_last_login		 = $$dataref{days_since_last_login};
										$email_verification_code	 = $$dataref{email_verification_code};
										$is_email_verified			 = $$dataref{is_email_verified};

										if($DebugThisAp eq "1")
											{
												print RECOVERY_FILE "<!-- user_name                   = ($user_name) -->\n";
												print RECOVERY_FILE "<!-- date_of_next_transaction    = ($date_of_next_transaction) -->\n";
												print RECOVERY_FILE "<!-- days_until_next_transaction = ($days_until_next_transaction) -->\n";
												print RECOVERY_FILE "<!-- last_four_digits            = ($last_four_digits) -->\n";
												print RECOVERY_FILE "<!-- rebilling_amount            = ($rebilling_amount) -->\n";
												print RECOVERY_FILE "<!-- card_expires                = ($card_expires) -->\n";
												print RECOVERY_FILE "<!-- user_logged_in_this_month   = ($user_logged_in_this_month) -->\n";
												print RECOVERY_FILE "<!-- membership_type             = ($membership_type) -->\n";
												print RECOVERY_FILE "<!-- password                    = ($password) -->\n";
												print RECOVERY_FILE "<!-- sex                         = ($sex) -->\n";
												print RECOVERY_FILE "<!-- days_since_last_login       = ($days_since_last_login) -->\n";
												print RECOVERY_FILE "<!-- email_verification_code     = ($email_verification_code) -->\n";
												print RECOVERY_FILE "<!-- is_email_verified           = ($is_email_verified) -->\n";
											}																		
										my $BccAddress = 'baumbach@optonline.net';
										
										$SentFrom 		= $Map{'EMAIL'};

										my $Subject	= "Urgent $Map{'WHICH_CONNECTIONS'} message for";

										if($sex eq "1")
											{
												$Subject = $Subject . " Mr. $user_name";
											}
										else
											{
												$Subject = $Subject . " Ms. $user_name";
											}
										
										$Message = "This is a courtesy message from $Map{'WHICH_CONNECTIONS'} for:\n\nUser Name:	$user_name\nPassword:	$password\n\n";
										
										
										$Message = $Message . "In order to maintain your \'$membership_type\' membership privileges, your credit card ending in $last_four_digits is due to be re-billed $Map{'CURRENCY_SYMBOL'}$rebilling_amount in $days_until_next_transaction days by $Map{'WHICH_CONNECTIONS'}.\n\n\n\n";

										# Use until processing source fixes their DB...
										if(1 == 1)
											{
												$Message = $Message . "----------------- Billing Notice -------------------------------\n\n";
												$Message = $Message . "Your credit card may have been billed as \"Gecko Technologies Group.\" The description should have been \"Internet Classifieds.\" Our credit card processing company made an error on our client\'s past statements but the \"Gecko Technologies Group\" description is still valid for your account. You will notice that \"Internet Classifieds\" will appear on your future statements. You do NOT need to take any further action. Everything is fine.\n\n\n\n";
											}

										# Inform the user they must login to their account within the month prior to their re-billing date
										# Detail how to login.
										if($user_logged_in_this_month eq 'NO')
											{
												$Message = $Message . "----------------- Lack of Usage --------------------------------\n\n";
												$Message = $Message . "Our records indicate that you have not logged in for $days_since_last_login days.\n\n";
												$Message = $Message . "For the convenience of our paying members we do not re-bill users unless they have used our services within the 60 days prior to their re-billing date.\n\n";
												$Message = $Message . "To avoid any interruption to your service, including the ability to contact other users, please login before $date_of_next_transaction:\n\n";

												$Message = $Message . "  Login to your $Map{'WHICH_CONNECTIONS'} account\n";
												$Message = $Message . "  $Map{'ROOT'}/LogIn.html\n\n\n\n";
											}
											

										# Inform the user their credit card will expire prior to the next rebilling.
										# Detail how to update the credit card information.
										if($card_expires eq 'YES')
											{
												$Message = $Message . "----------- Credit Card Expires Soon ---------------------------\n\n";
												$Message = $Message . "Our records indicate that your credit card ending in $last_four_digits will expire before, $date_of_next_transaction, the date your membership expires.\n\n";
												$Message = $Message . "To avoid any interruption to your service, including the ability to contact other users, please login and update your credit card expiration date by following these steps:\n\n";

												$Message = $Message . "1.  Login to your $Map{'WHICH_CONNECTIONS'} account\n";
												$Message = $Message . "    $Map{'ROOT'}/LogIn.html\n";
												$Message = $Message . "2.  On the \'Member Home\' page click the \'Update Card Info...\' link.\n";
												$Message = $Message . "    $Map{'CGIBIN'}/UpdateBilling.exe\n";
												$Message = $Message . "3.  Enter the new credit card expiration date\n";
												$Message = $Message . "4.  Click \'submit\'\n\n\n\n";
											}
											
										# Inform the user their email address needs to be verified
										# Detail how to verify their email address.
										if($is_email_verified eq '0')
											{
												$Message = $Message . "----------- Email Address Requires Verification ----------------\n\n";
												$Message = $Message . "Our records indicate that your email address \'$email\' needs to be verified.\n";
												$Message = $Message . "To avoid any interruption to your service, including the ability to contact other users, please login and verify your email address by following these steps:\n\n";

												$Message = $Message . "1.  Login to your $Map{'WHICH_CONNECTIONS'} account\n";
												$Message = $Message . "    $Map{'ROOT'}/LogIn.html\n";
												$Message = $Message . "2.  On the \'Member Home\' page click \'Change/Verify My Email Address\'.\n";
												$Message = $Message . "    $Map{'CGIBIN'}/ManageEmailVerification.cgi\n";
												$Message = $Message . "3.  Under \'Option 1\' enter the following verification code:\n";
												$Message = $Message . "    $email_verification_code\n";
												$Message = $Message . "4.  Click \'Verify_My_Email_Address\'\n\n\n\n";
											}

										# Detail how to cancel premium membership.
										$Message = $Message . "--------------- Account Cancellation Details -------------------\n\n";
										$Message = $Message . "You may cancel your \'$membership_type\' membership at any time you wish.  If you decide to cancel your \'$membership_type\' membership you will still be able to use all the premium features of your account until $date_of_next_transaction.  If you do not cancel your \'$membership_type\' membership there will be an automatic renewal every month until you do decide to cancel.\n\n";
										$Message = $Message . "To cancel your \'$membership_type\' subscription follow these steps:\n\n";

										$Message = $Message . "1.  Login to your $Map{'WHICH_CONNECTIONS'} account\n";
										$Message = $Message . "    $Map{'ROOT'}/LogIn.html\n";
										$Message = $Message . "2.  On the \'Member Home\' page click \'Cancel $membership_type Membership...\'.\n";
										$Message = $Message . "    $Map{'ROOT'}/CancelMembership.html\n";
										$Message = $Message . "3.  Fill out the form, being as detailed as possible, to help us improve our site.\n";
										$Message = $Message . "4.  Click \'Cancel My \"Premium\" Membership\'\n\n\n\n";

										# End of mail...
										$Message = $Message . "If you have any questions please contact us at $Map{'EMAIL'}\n\n";
										$Message = $Message . "Sincerely,\n\n";
										$Message = $Message . "Jay Peterman\n";
										$Message = $Message . "$Map{'WHICH_CONNECTIONS'}\n";
										$Message = $Message . "Client Relations Manager\n\n\n";
 
										if($email =~ m/hotmail.com/i)
											{
												$Message = $Message . "\n\n\n\nNOTE:  In order to avoid improper browser behavior please copy and past the link you wish to access into a seperate browser's address bar.";
												$Message = $Message . "\n\nWe apologize for the inconvenience this may cause you, but unfortunately your current Hotmail window has an external domain that will cause login problems while navigating $Map{WHICH_CONNECTIONS}.";
											}

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
												$Message =~ s/\"/%22/gis;
												$Message =~ s/\'/%22/gis;
												print RECOVERY_FILE "<TR><TD><FONT color=\"red\">Error!</FONT> Resend Mail ($Count): <A href=\"javascript:newWindowGeneric('$Map{'ROOT'}/admin/cgi-bin/Admin_GenSendMail.cgi?sent_from=$SentFrom&amp;sent_to=$email&amp;sent_bcc=&amp;subject=$Subject&amp;message_text=$Message')\">$email</A></TD></TR>\n";
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
		my $TempFilePath 	= "C://Temp";
			
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
