#!/usr/local/bin/perl -w

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

use strict;
use CGI qw/:standard/;

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "DatabaseFunctions.pl";
require "CgiFunctions.pl";
require "SendMailFunctions.pl";
require "UtilityFunctions.pl";

my $DebugThisAp			   = "1";
my $DebugCgiFunctions 	   = "1";
my $DebugDatabaseFunctions = "1";
my $DebugUtilityFunctions  = "1";
my $DebugMailSendFunctions = "1";

my $count = 0;

my $ProgramName  = "Admin_SendMail.cgi";

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

my $SqlStatement  = "";
my $BCC_FILE_NAME = "";

my $multiple_to   = "0";
my $multiple_bcc  = "0";
# Escape special characters...
if($subject =~ m/"/)
	{
		$subject =~ s/"/""/g;
	}
#print "<!-- pre removal message_text ($message_text) -->\n";
if($message_text =~ m/"/)
	{
		$message_text =~ s/"/""/g;
	}

# Check for single email address...
if($sent_to !~ m/@/ && $sent_to !~ m/Select Query/)
	{
		$SqlStatement = $sent_to;
		$multiple_to = "1";
	}
elsif($sent_bcc ne "" && $sent_bcc !~ m/Select Query/)
	{
		$SqlStatement = $sent_bcc;
		$multiple_bcc = "1";
	}

	
# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);


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
print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Admin Mail Sent Page</STRONG></FONT>\n";
print "                  <BR>&nbsp;<BR>\n";
print "              </TD>\n";
print "            </TR>\n";

if($DebugThisAp eq "1")
	{
		print "<!--\n";
		print "sent_from = ($sent_from)\n";
		print "sent_to = ($sent_to)\n";
		print "sent_bcc = ($sent_bcc)\n";
		print "subject = ($subject)\n";
		print "message_text = ($message_text)\n";
		print "SqlStatement = ($SqlStatement)\n";
		print "multiple_to = ($multiple_to)\n";
		print "multiple_bcc = ($multiple_bcc)\n";
		print "-->\n";
	}
# Send unique messages to multiple users using the "To:" field
if($SqlStatement ne "" && $multiple_to eq "1" && 1 == 0)
	{
		my $TimeOutRecoveryFile = "$Map{'BLAT_PATH'}/EXE/Admin_SendMail_cgi.html";
		# Create and open the "BCC:" file that blat will use to send mail...
		open (TIME_OUT_FILE, "> $TimeOutRecoveryFile") || die "Can't open $TimeOutRecoveryFile: $!\n";
			
		print TIME_OUT_FILE "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">\n";
		print TIME_OUT_FILE "<HTML>\n";
		print TIME_OUT_FILE "  <HEAD>\n";
		print TIME_OUT_FILE "    <TITLE>\n";
		print TIME_OUT_FILE "      	Admin_SendMail.cgi time out recovery file\n";
		print TIME_OUT_FILE "    </TITLE>\n";
		# Open in new JavaScript...
		print TIME_OUT_FILE"	 <SCRIPT type=\"text/javascript\" language=\"javascript\">\n";
		print TIME_OUT_FILE"	 <!--\n";
		print TIME_OUT_FILE"	 function newWindowGeneric(picName) \n";
		print TIME_OUT_FILE"	 {\n";
		print TIME_OUT_FILE"	 		var myWindow = window.open(picName, 'Guidelines', 'toolbar=no,location=no,scrollbars=yes,resizable=yes,width=850,height=1000')\n";
		print TIME_OUT_FILE"				myWindow.focus()\n";
		print TIME_OUT_FILE"	 }\n";
		print TIME_OUT_FILE"	 // -->\n";
		print TIME_OUT_FILE"	 </SCRIPT>\n";

		print TIME_OUT_FILE "  </HEAD>\n";
		print TIME_OUT_FILE "  <BODY>\n";
		print TIME_OUT_FILE "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"700\">\n";
		print TIME_OUT_FILE "            <TR align=\"left\">\n";
		print TIME_OUT_FILE "              <TD>\n";
		print TIME_OUT_FILE "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Results from sending multiple unique \"To:\" messages</STRONG></FONT>\n";
		print TIME_OUT_FILE "                  <BR>&nbsp;<BR>\n";
		print TIME_OUT_FILE "              </TD>\n";
		print TIME_OUT_FILE "            </TR>\n";
			
		print "            <TR align=\"left\">\n";
		print "              <TD>\n";
		print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Results from sending multiple unique \"To:\" messages</STRONG></FONT>\n";
		print "                  <BR>&nbsp;<BR>\n";
		print "              </TD>\n";
		print "            </TR>\n";
		print "            <TR align=\"left\">\n";
		print "              <TD>\n";
		print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">In the event of a time out open this file: </FONT><A href=\"javascript:newWindowGeneric('$TimeOutRecoveryFile')\">$TimeOutRecoveryFile</A>\n";
		print "                  <BR>&nbsp;<BR>\n";
		print "              </TD>\n";
		print "            </TR>\n";
		my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "Admin_SendMail.cgi");
		$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
		$status = $MSSQL::DBlib::dbh->dbsqlexec();
			
		##########################
		# Get FIRST result set...
		##########################
		# dbresults() must be called for each result set...
		$status = $MSSQL::DBlib::dbh->dbresults();
		if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
			{
				my %dataref = ("jason" => "baumbach");
				my $dataref = \%dataref;
				my $UserName      = "";
				my $Sex			  = "";
				my $Email      	  = "";
				my $LastName      = "";
				my $Temp      	  = "";
				# If in debug mode, print information...
				if($DebugThisAp eq "1")
					{
						print TIME_OUT_FILE "<!-- SQL: $SqlStatement -->\n";
						print "<!-- SQL: $SqlStatement -->\n";
					}
				# Check for global DB error...
				if($DatabaseFunctions::DatabaseError eq "1")
					{
						print TIME_OUT_FILE "<TR><TD>ERROR: ($SqlStatement) Failed!</TD></TR>\n";
						print "<TR><TD>ERROR: ($SqlStatement) Failed!</TD></TR>\n";
					}
				else
					{
						# Prevent infinite loop...
						while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
							{
								# Limit the number of iterations for testing...
								if($count++ < 500)
									{
										# Since there is no global DB error check if email address is valid
										if($$dataref{email} =~ m/^\@/ || $$dataref{email} eq "")
											{
												print TIME_OUT_FILE "<TR><TD>ERROR: ($$dataref{email}) Failed!</TD></TR>\n";
												print "<TR><TD>ERROR: ($$dataref{email}) Failed!</TD></TR>\n";
											}
										else
											{
												$UserName = $$dataref{user_name};
												# Remove trailing spaces from user_name...
												($UserName, $Temp) = split(/\s\s/, $UserName);
													
												$Sex = $$dataref{sex};
												# Remove trailing spaces from password...
												($Sex, $Temp) = split(/\s\s/, $Sex);
													
												$Email = $$dataref{email};
												# Remove trailing spaces from user_name...
												($Email, $Temp) = split(/\s\s/, $Email);
													
												$LastName = $$dataref{last_name};
												# Remove trailing spaces from photo_5...
												($LastName, $Temp) = split(/\s\s/, $LastName);
												# Set last_name = user_name if last_name is blank...
												if($LastName eq "" or $LastName eq " ")
													{
														$LastName = $UserName;
													}
													
												my $Subject		  = $subject;
												my $MessageText	  = $message_text;
													
												# replace keys to personalize the mail...
												$Subject     =~ s/user_name/$UserName/g;
												$MessageText =~ s/user_name/$UserName/g;
												# Male...
												if($Sex eq "1")
													{
														$Subject     =~ s/last_name/Mr. $LastName/g;
														$MessageText =~ s/last_name/Mr. $LastName/g;
													}
												# Female...
												elsif($Sex eq "2")
													{
														$Subject   	 =~ s/last_name/Ms. $LastName/g;
														$MessageText =~ s/last_name/Ms. $LastName/g;
													}
												# Unknown...
												else
													{
														$Subject   	 =~ s/last_name/$LastName/g;
														$MessageText =~ s/last_name/$LastName/g;
													}
												if($DebugThisAp eq "1")
													{
														print TIME_OUT_FILE "<!-- Email   =($Email) -->\n";
														print TIME_OUT_FILE "<!-- Subject =($Subject) -->\n";
														print TIME_OUT_FILE "<!-- Message =($MessageText) -->\n";
															
														print "<!-- Email   =($Email) -->\n";
														print "<!-- Subject =($Subject) -->\n";
														print "<!-- Message =($MessageText) -->\n";
													}
												# call the sub to sent the mail...
												my $return_value = &Send_Individual_Blat_Mail($sent_from, $Email, "", $Subject, $MessageText, %Map);
												if($return_value < 1)
													{
														print TIME_OUT_FILE "<TR><TD>Error! Resend Mail ($count): <A href=\"javascript:newWindowGeneric('$Map{'ADMIN_CGIBIN'}/Admin_GenSendMail.cgi?sent_from=$sent_from&amp;sent_to=$Email&amp;sent_bcc=&amp;subject=$Subject&amp;message_text=$MessageText')\">$Email</A></TD></TR>\n";
													}
												else
													{
														print TIME_OUT_FILE "<TR><TD>View/Resend Mail ($count): <A href=\"javascript:newWindowGeneric('$Map{'ADMIN_CGIBIN'}/Admin_GenSendMail.cgi?sent_from=$sent_from&amp;sent_to=$Email&amp;sent_bcc=&amp;subject=$Subject&amp;message_text=$MessageText')\">$Email</A></TD></TR>\n";
													}
													
											}# END else (valid Email Address)
									}# if count++ > 2240
							}# END while != NO_MORE_ROWS
					}# END else (No db error) 
			}# END if($status != FAIL)
		else
			{
				print TIME_OUT_FILE "<TR><TD>ERROR: $SqlStatement Failed for first result set!</TD></TR>\n";
				print "<TR><TD>ERROR: $SqlStatement Failed for first result set!</TD></TR>\n";
				$status = $MSSQL::DBlib::dbh->dbcancel();
			}
		print TIME_OUT_FILE "                    <!-- submit -->\n";
		print TIME_OUT_FILE "                    <TR>\n";
		print TIME_OUT_FILE "                      <TD>\n";
		print TIME_OUT_FILE "						   <INPUT TYPE=BUTTON VALUE=\"Close Window\" onClick=\"Closer()\">\n";
		print TIME_OUT_FILE "                      </TD>\n";
		print TIME_OUT_FILE "                    </TR>\n";
		print TIME_OUT_FILE "						  <SCRIPT type=\"text/javascript\" language=\"javascript\">\n";
		print TIME_OUT_FILE "						  <!--\n";
		print TIME_OUT_FILE "    					 		 function Closer()\n";
		print TIME_OUT_FILE "    							 {\n";
		print TIME_OUT_FILE "        						 	  window.close()\n";
		print TIME_OUT_FILE "    							 }\n";
		print TIME_OUT_FILE "						  //-->\n";
		print TIME_OUT_FILE "						 </SCRIPT>\n";
			
		print TIME_OUT_FILE "          </TABLE>\n";
		print TIME_OUT_FILE "        </TD>\n";
		print TIME_OUT_FILE "        <!-- End Main Data Cell -->\n";
		print TIME_OUT_FILE "      </TR>\n";
		print TIME_OUT_FILE "      <!-- End Navigation and Main Row -->\n";
		print TIME_OUT_FILE "    </TABLE>\n";
			
		print TIME_OUT_FILE "  </BODY>\n";
		print TIME_OUT_FILE "</HTML>\n";
		close(TIME_OUT_FILE);
	}# End if($SqlStatement ne "" && $multiple_to eq "1")
# Send one bulk mail message to multiple users using the "Bcc:" field
elsif($SqlStatement ne "" && $multiple_bcc eq "1" && 1 == 0)
	{
		print "            <TR align=\"left\">\n";
		print "              <TD>\n";
		print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Results from sending one bulk \"Bcc:\" message</STRONG></FONT>\n";
		print "                  <BR>&nbsp;<BR>\n";
		print "              </TD>\n";
		print "            </TR>\n";
		# Parse the current date...
		(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst) = localtime(time);
		# use parsed date to create unique file name...
		$BCC_FILE_NAME = $SqlStatement . "_" . ($mon+1)  . "_" . $mday  . "_" . ($year+1900) . ".txt";
		if($DebugThisAp == 1)
			{
				print "<!-- BCC_FILE_NAME = ($BCC_FILE_NAME) -->\n";
			}
		# Create and open the "BCC:" file that blat will use to send mail...
		open (BCC_FILE, "> $Map{'BLAT_PATH'}/EXE/$BCC_FILE_NAME") || die "Can't open $Map{'BLAT_PATH'}/EXE/$BCC_FILE_NAME: $!\n";
		# execute the SQL commands to access the database...
		my $BccFile	= "$Map{'BLAT_PATH'}/EXE/$BCC_FILE_NAME";
			
		my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "Admin_SendMail.cgi");
		$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
		$status = $MSSQL::DBlib::dbh->dbsqlexec();
			
		##########################
		# Get FIRST result set...
		##########################
		# dbresults() must be called for each result set...
		$status = $MSSQL::DBlib::dbh->dbresults();
		if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
			{
				my %dataref = ("jason" => "baumbach");
				my $dataref = \%dataref;
				my $EmailAddress = "";
				# If in debug mode, print information...
				if($DebugThisAp == 1)
					{
						print "<!-- SQL: $SqlStatement -->\n";
					}
				# Check for global DB error...
				if($DatabaseFunctions::DatabaseError eq "1")
					{
						print "<TD>ERROR: ($SqlStatement) Failed!</TD>\n";
					}
				else
					{
						# Prevent infinite loop...
						while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
							{
								# Limit the number of iterations for testing...
								if($count++ < 10)
									{
										# Since there is no global DB error check if email address is valid
										if($$dataref{email} =~ m/^\@/ || $$dataref{email} eq "")
											{
												print "ERROR: ($$dataref{email}) Failed!\n";
											}
										else
											{
												# bind to the info in the db...
												$EmailAddress = $$dataref{email};
												$EmailAddress =~ s/\s//g;
												# populate the BCC_FILE...
												if($count < 2)
													{
														print BCC_FILE "$EmailAddress";
													}
												else
													{
														print BCC_FILE ",$EmailAddress";
													}
											}# END else (valid Email Address)
									}# if count++ > 2240
							}# END while != NO_MORE_ROWS
					}# END else (No db error) 
				# Close the BCC_FILE...
				close (BCC_FILE);
				&Send_Individual_Blat_Mail($sent_from, $sent_from, $BccFile, $subject, $message_text, %Map);
			}# END if($status != FAIL)
		else
			{
				print "<TR><TD>ERROR: $SqlStatement Failed for first result set!</TD></TR>\n";
				$status = $MSSQL::DBlib::dbh->dbcancel();
			}
	}# End elsif($SqlStatement ne "" && $multiple_bcc eq "1")
# Send one mail message to one user using the "To:" field
elsif($SqlStatement eq "" && $multiple_to eq "0" && $multiple_bcc eq "0" && $sent_to !~ m/Select Query/)
	{
		print "            <TR align=\"left\">\n";
		print "              <TD>\n";
		print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Results from sending one unique \"To:\" message</STRONG></FONT>\n";
		print "                  <BR>&nbsp;<BR>\n";
		print "              </TD>\n";
		print "            </TR>\n";
		&Send_Individual_Blat_Mail($sent_from, $sent_to, "", $subject, $message_text, %Map);
	}# end elsif($SqlStatement eq "" && $multiple_to eq "0" && $multiple_bcc eq "0")
else
	{
		print "<TR><TD>This should never happen.<BR>Remember, this cgi must be called by Admin_GenSendMail.cgi.</TD></TR>\n";
	}
	
print "                    <!-- submit -->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "						   <INPUT TYPE=BUTTON VALUE=\"Close Window\" onClick=\"Closer()\">\n";
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
	
print "          </TABLE>\n";
print "        </TD>\n";
print "        <!-- End Main Data Cell -->\n";
print "      </TR>\n";
print "      <!-- End Navigation and Main Row -->\n";
print "    </TABLE>\n";
# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName", "ASC", "DESC", 0, 1, 0, $DebugUtilityFunctions, %Map);
	
#End HTML...
print "</HTML>\n";
exit 0;



sub Send_Individual_Blat_Mail
	{
		my($SentFrom, $SentTo, $BccFile, $Subject, $MessageText, %Map) = @_;
		#Prepare to send the individual or BCC mail...
			
		# Build email to send to the person receiving the new PC Mail...
		my $BlatPath 		= "$Map{'BLAT_PATH'}/EXE/blat.exe";
		my $MailServer 		= "$Map{'SMTP_HOST'}";
		my $TempFile		= "";
		my $TempFilePath 	= "C://Temp";
		my $BlatLogFilePath = "$Map{'LOG_FOLDER'}/blat.log";
			
		if($MessageText eq "")
			{
				$MessageText = "No message.";
			}
			
		(my $return_value, my $output)= &SendMailFunctions::Mail_Blat($BlatPath, $MailServer, $SentFrom, $SentTo, $BccFile, $Subject, $TempFile, $MessageText, $TempFilePath, $BlatLogFilePath, $DebugMailSendFunctions);
		if($return_value < 1)
			{
				print "<TR><TD><FONT color=\"blue\">Mail_Blat <STRONG>Success</STRONG><BR>return_value=($return_value)<BR>output=($output)</FONT></TD></TR>\n";
				if($BccFile eq "")
					{
						#						print "<TR><TD>($count) Sent Mail To: ($SentTo)</TD></TR>\n";
						print "<TR><TD>View/Resend mail ($count) in new window: <A href=\"javascript:newWindowGeneric('Admin_GenSendMail.cgi?sent_from=$SentFrom&amp;sent_to=$SentTo&amp;sent_bcc=&amp;subject=$Subject&amp;message_text=$MessageText')\">$SentTo</A></TD></TR>\n";
					}
				else
					{
						# Open the BCC file...
						open (LOCALFILE, $BccFile) || die "Can't open $BccFile: $!\n";
							
						print "<TR><TD>Sent Mail To: ($SentTo) with ($count) Blind Copies (Bcc)</TD></TR>\n";
						# Read each line of the file that needs to be parsed until EOF...
						while (<LOCALFILE>) 
							{
								# Replace the commas with spaces to make the print out look better
								$_ =~ s/,/ /g;
								print "<TR><TD>$_</TD></TR>\n";
							}# End While loop
						# Close file...
						close (LOCALFILE);
					}
				return 1;
			}
		else
			{
				print "<TR><TD><FONT color=\"red\">Mail_Blat <STRONG>Error</STRONG><BR>return_value=($return_value)<BR>output=($output)</FONT></TD></TR>\n";
				print "<TR><TD>Mail ($count) Error. Resend in new window: <A href=\"javascript:newWindowGeneric('Admin_GenSendMail.cgi?sent_from=$SentFrom&amp;sent_to=$SentTo&amp;sent_bcc=&amp;subject=$Subject&amp;message_text=$MessageText')\">$SentTo</A></TD></TR>\n";
					
				return -1;
			}
	}
