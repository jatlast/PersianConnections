#!/usr/local/bin/perl -w
use CGI qw/:standard/;

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

use strict;

#Begin HTML so errors show up in browser...
print CGI::header('text/html');
print "<HTML>\n";

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "CgiFunctions.pl";
require "DatabaseFunctions.pl";
require "UtilityFunctions.pl";

my $ProgramName = "Admin_GenManualCheckForm.cgi";

my $DebugThisAp			   = "0";
my $DebugCgiFunctions 	   = "0";
my $DebugDatabaseFunctions = "0";
my $DebugUtilityFunctions  = "0";

# Determine what libraries to use base on the execution dir...
my $CurrentFilePath = __FILE__;
# Initialize LinkMap Hash variable "Map"...
my %Map = &UtilityFunctions::Load_LinkMap($CurrentFilePath, $DebugUtilityFunctions); 
 
# Severe Error:  No LinkMap.dat file found -- EXIT --
if($Map{'CONFIG'} eq 'ERROR')
	{
		&UtilityFunctions::Print_Error("LinkMap Error.<BR><BR>Contact Site Administrator.", $DebugUtilityFunctions, %Map);
	}
else
	{
		$Map{'PROGRAM_NAME'} = $ProgramName;
		print "<!-- $Map{'SYSTEM'} -->\n" if $DebugThisAp eq "1";
	}

# Output all beginning HTML...
#&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);
&UtilityFunctions::Print_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);


my $user_name 			   = "";
my $first_name			   = "";
my $last_name  			   = "";
my $street_address		   = "";
my $city 				   = "";
my $state   			   = "";
my $zip 	   			   = "";
my $country 			   = "";
my $check_number 	   	   = "";
my $date				   = "";
my $amount 		   		   = "";
my $months_joined  		   = "";
my $bank_account_number    = "";
my $bank_ABA_code		   = "";
my $submit  			   = "";


if(CGI::param('user_name'))	         {$user_name 		   = CGI::param('user_name');}
if(CGI::param('first_name'))	     {$first_name 		   = CGI::param('first_name');}
if(CGI::param('last_name'))	         {$last_name 		   = CGI::param('last_name');}
if(CGI::param('street_address'))	 {$street_address 	   = CGI::param('street_address');}
if(CGI::param('city'))				 {$city 			   = CGI::param('city');}
if(CGI::param('state'))				 {$state 			   = CGI::param('state');}
if(CGI::param('zip'))				 {$zip 				   = CGI::param('zip');}
if(CGI::param('country'))			 {$country 			   = CGI::param('country');}
if(CGI::param('check_number'))		 {$check_number 	   = CGI::param('check_number');}
if(CGI::param('date'))				 {$date 			   = CGI::param('date');}
if(CGI::param('amount'))			 {$amount 			   = CGI::param('amount');}
if(CGI::param('months_joined'))		 {$months_joined	   = CGI::param('months_joined');}
if(CGI::param('bank_account_number')){$bank_account_number = CGI::param('bank_account_number');}
if(CGI::param('bank_ABA_code'))		 {$bank_ABA_code 	   = CGI::param('bank_ABA_code');}
if(CGI::param('submit'))			 {$submit 			   = CGI::param('submit');}

# Parse the current date...
(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst) = localtime(time);
# use parsed date to create unique name for transaction_id and SSLOG_FILE...
# Unique Name has the folling format username_m[m]_d[d]_yyyy_h[h]_m[m]_s[s]
my $UniqueID = $user_name . "_"  . ($mon+1)  . "_" . $mday  . "_" . ($year+1900) . "_" . $hour  . "_" . $min . "_" . $sec;

my $transaction_id = $UniqueID;

if($submit eq "Update Form" or $submit eq "")
	{
		my $SqlStatement = "admin_GenManualCheckForm '$user_name'";
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
				# for split() function...
				my $Temp = "";
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
									
								$user_name 	        = $$dataref{user_name};
								$first_name 	  	= $$dataref{first_name};
								$last_name   		= $$dataref{last_name};
								$street_address     = $$dataref{street_address};
								$city  	  			= $$dataref{city};
								$state  	  		= $$dataref{state};
								($state, $Temp) = split(/\s\s/, $state);
								$zip  	  			= $$dataref{zip};
								$country  	  		= $$dataref{country};
								($country, $Temp) = split(/\s\s/, $country);
									
								$bank_ABA_code    	= $$dataref{bank_ABA_code};
								$bank_account_number= $$dataref{bank_account_number};
									
								if($DebugThisAp eq "1")
									{
										print "<!-- user_name           = ($user_name) -->\n";
										print "<!-- first_name          = ($first_name) -->\n";
										print "<!-- last_name           = ($last_name) -->\n";
										print "<!-- street_address      = ($street_address) -->\n";
										print "<!-- city                = ($city) -->\n";
										print "<!-- state               = ($state) -->\n";
										print "<!-- zip                 = ($zip) -->\n";
										print "<!-- country             = ($country) -->\n";
										print "<!-- bank_ABA_code       = ($bank_ABA_code) -->\n";
										print "<!-- bank_account_number = ($bank_account_number) -->\n";
									}
							}
					}# END else (No db error) 
			}# END if($status != FAIL)
		else
			{
				print "ERROR: $SqlStatement Failed for first result set!\n";
				$status = $MSSQL::DBlib::dbh->dbcancel();
			}
			
		print "          <TABLE border=\"0\" cellspacing=\"3\" cellpadding=\"3\" width=\"100%\">\n";
		print "            <TR valign=\"bottom\">\n";
		print "              <TD height=\"29\" width=\"604\" align=\"left\">\n";
		print "                <P>\n";
		if($DatabaseFunctions::DatabaseError eq "1005")
			{
 			 	print "                  <FONT face=\"Arial, Helvetica, sans-serif\" color=\"#FFFFFF\"><STRONG><FONT color=\"red\">ERROR:  </FONT>User Name <FONT color=\"red\">$user_name</FONT> not found in the $Map{'WHICH_CONNECTIONS'} database.<BR>Use the Get User Data by entering a different user name then push the Update Form button.</STRONG></FONT>\n";
			}
        else
            {
 			 	print "                  <FONT face=\"Arial, Helvetica, sans-serif\" color=\"#FFFFFF\"><STRONG>Manually enter <FONT color=\"red\">$user_name</FONT>'s check into the $Map{'WHICH_CONNECTIONS'} database.</STRONG></FONT>\n";
            }
		
		print "                </P>\n";
		print "              </TD>\n";
		print "            </TR>\n";
		print "            <TR>\n";
			
			
		print "        <TD width=\"667\" bgcolor=\"$Map{'HTML_BODY_BGCOLOR'}\" height=\"394\" valign=\"top\">\n";
		print "          <FORM onsubmit=\"return checkForm(this)\" method=\"POST\" action=\"$Map{'ROOT'}/admin/cgi-bin/Admin_GenManualCheckForm.cgi\">\n";
		print "            <TABLE width=\"714\" border=\"1\" bgcolor=\"#ffffcc\" cellpadding=\"2\" cellspacing=\"2\" bordercolorlight=\"#ffcc33\" bordercolordark=\"#ffcc33\" bordercolor=\"#ffcc66\" height=\"170\">\n";
		print "              <TR valign=\"middle\">\n";
		print "                <TD height=\"108\">\n";
		print "                  <TABLE border=\"0\" cellspacing=\"0\" cellpadding=\"5\" height=\"166\" width=\"100%\">\n";
		print "                    <TR>\n";
		print "                      <TD>\n";
		print "                        <TABLE width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\n";
		print "                          <TR>\n";
		print "                            <TD>\n";
		if($first_name ne "")
			{
				print "                              	<INPUT size=\"10\" maxlength=\"32\" value=\"$first_name\" name=\"first_name\"> \n";
			}
		else
			{
				print "                              	<INPUT size=\"10\" maxlength=\"32\" value=\"FirstName\" name=\"first_name\"> \n";
			}
			
		if($last_name ne "")
			{
				print "                              	<INPUT size=\"10\" maxlength=\"32\" value=\"$last_name\" name=\"last_name\"> \n";
			}
		else
			{
				print "                              	<INPUT size=\"10\" maxlength=\"32\" value=\"LastName\" name=\"last_name\"> \n";
			}
		print "                              <BR>\n";
		if($street_address ne "")
			{
				print "                              	<INPUT size=\"25\" maxlength=\"64\" value=\"$street_address\" name=\"street_address\"> \n";
			}
		else
			{
				print "                              	<INPUT size=\"25\" maxlength=\"64\" value=\"StreetAddress\" name=\"street_address\"> \n";
			}
		print "                              <BR>\n";
		if($city ne "")
			{
				print "                              	<INPUT size=\"10\" maxlength=\"32\" value=\"$city\" name=\"city\"> \n";
			}
		else
			{
				print "                              	<INPUT size=\"10\" maxlength=\"32\" value=\"City\" name=\"city\"> \n";
			}
		print "				<FONT size=\"2\" color=\"black\"><STRONG> , </STRONG> \n";
		if($state ne "")
			{
				print "                              	<INPUT size=\"2\" maxlength=\"2\" value=\"$state\" name=\"state\"> \n";
			}
		else
			{
				print "                              	<INPUT size=\"2\" maxlength=\"2\" value=\"??\" name=\"state\"> \n";
			}
		if($zip ne "")
			{
				print "                              	<INPUT size=\"5\" maxlength=\"5\" value=\"$zip\" name=\"zip\">\n";
			}
		else
			{
				print "                              	<INPUT size=\"5\" maxlength=\"5\" value=\"Zip\" name=\"zip\">\n";
			}
		print "                              <BR>\n";
		if($country ne "")
			{
				print "                               	<INPUT size=\"10\" maxlength=\"32\" value=\"$country\" name=\"country\"></FONT>\n";
			}
		else
			{
				print "                               	<INPUT size=\"10\" maxlength=\"32\" value=\"Country\" name=\"country\"></FONT>\n";
			}
		print "                            </TD>\n";
		print "                            <TD align=\"right\">\n";
		print "                              	<FONT color=\"black\" size=\"3\"><STRONG>Check #:</STRONG></FONT>\n";
		print "                              	<BR>\n";
		print "                              	<BR>\n";
		print "                       		<FONT color=\"black\" size=\"3\"><STRONG>Date:</STRONG></FONT>\n";
		print "                            </TD>\n";
		print "                            <TD align=\"right\" width=\"1%\">\n";
		print "                              	<INPUT size=\"9\" maxlength=\"20\" value=\"CheckNumber\" name=\"check_number\">\n";
		print "                              	<BR>\n";
		print "                              	<BR>\n";
		print "                               	<INPUT size=\"10\" maxlength=\"10\" value=\"mm/dd/yyyy\" name=\"date\">\n";
		print "                            </TD>\n";
		print "                          </TR>\n";
		print "                        </TABLE>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
		print "                    <TR>\n";
		print "                      <TD>\n";
		print "                        <TABLE width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\n";
		print "                          <TR>\n";
		print "                            <TD align=\"right\" width=\"1%\">\n";
		print "                              <FONT color=\"black\" size=\"3\"><STRONG>Which:&nbsp;</STRONG></FONT>\n";
		print "                            </TD>\n";
		print "                            <TD>\n";
		print "                              <FONT color=\"black\" size=\"3\"><U><STRONG>&nbsp;&nbsp;&nbsp;$Map{'WHICH_CONNECTIONS'}.com&nbsp;&nbsp;&nbsp;</STRONG></U></FONT>\n";
		print "                            </TD>\n";
        print "                          <!--    months_joined    -->\n";
        print "                            <TD align=\"right\">\n";
        print "                              <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\"><STRONG>Months Joined:&nbsp;</STRONG></FONT>\n";
        print "                            </TD>\n";
        print "                            <TD width=\"1%\" align=\"right\">\n";
        print "                              <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"> <SELECT size=\"1\" name=\"months_joined\">\n";
        print "                                <OPTION SELECTED value=\"0\">\n";
        print "                                  ???\n";
        print "                                </OPTION>\n";
        print "                                <OPTION value=\"1\">\n";
        print "                                  1\n";
        print "                                </OPTION>\n";
        print "                                <OPTION value=\"3\">\n";
        print "                                  3\n";
        print "                                </OPTION>\n";
        print "                                <OPTION value=\"12\">\n";
        print "                                  12\n";
        print "                                </OPTION>\n";
        print "                                <OPTION value=\"240\">\n";
        print "                                  Life\n";
        print "                                </OPTION>\n";
        print "                              </SELECT></FONT>\n";
        print "                            </TD>\n";
        print "                          </TR>\n";
		print "                        </TABLE>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
		print "                    <TR>\n";
		print "                      <TD>\n";
		print "                        <TABLE width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\n";
		print "                          <TR>\n";
		print "                            <TD align=\"right\" width=\"1%\">\n";
		print "                              <FONT color=\"black\" size=\"3\"><STRONG>Name:&nbsp;</STRONG></FONT>\n";
		print "                            </TD>\n";
		print "                            <TD>\n";
		print "                              <INPUT size=\"32\" maxlength=\"32\" value=\"$user_name\" name=\"user_name\">\n";
		print "                            </TD>\n";
		print "                            <TD align=\"right\">\n";
		print "                              <FONT color=\"black\" size=\"3\"><STRONG>Amount:&nbsp;\$</STRONG></FONT>\n";
		print "                            </TD>\n";
		print "                            <TD align=\"right\" width=\"1%\">\n";
		print "                              <INPUT size=\"10\" maxlength=\"10\" value=\"Amount\" name=\"amount\">\n";
		print "                            </TD>\n";
		print "                          </TR>\n";
		print "                        </TABLE>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
		print "                    <TR>\n";
		print "                      <TD>\n";
		print "                        <TABLE width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\n";
		print "                          <TR>\n";
		print "                            <TD align=\"left\">\n";
		if($bank_account_number ne "")
			{
				print "                               	<INPUT size=\"10\" maxlength=\"10\" value=\"$bank_account_number\" name=\"bank_account_number\"> \n";
			}
		else
			{
				print "                               	<INPUT size=\"10\" maxlength=\"10\" value=\"AccountNumber\" name=\"bank_account_number\"> \n";
			}
		print "				<FONT color=\"black\" size=\"3\"><STRONG> : </STRONG></FONT>\n";
		if($bank_account_number ne "")
			{
				print "                               	<INPUT size=\"10\" maxlength=\"10\" value=\"$bank_ABA_code\" name=\"bank_ABA_code\">\n";
			}
		else
			{
				print "                               	<INPUT size=\"10\" maxlength=\"10\" value=\"ABA\" name=\"bank_ABA_code\">\n";
			}
		print "                            </TD>\n";
		print "                            <TD align=\"right\">\n";
		if($DatabaseFunctions::DatabaseError ne "1005")
			{
 			 	print "                  <INPUT type=\"submit\" name=\"submit\" value=\"Submit Check\">\n";
			}
        else
            {
 			 	print "                  <!-- do not show the submit button because the username was not found in the DB -->\n";
            }
		print "                            </TD>\n";
		print "                          </TR>\n";
		print "                        </TABLE>\n";
		print "                      </TD>\n";
		print "                    </TR>\n";
		print "                  </TABLE>\n";
		print "                </TD>\n";
		print "              </TR>\n";
		print "            </TABLE>\n";
		print "            </FORM>\n";
		print "        </TD>\n";
		print "      </TR>\n";			
	}
elsif($submit eq "Submit Check")
	{
		my $x_trans_id = $check_number;
		my $x_md5_hash = $date;
		my $x_description = $street_address . "|" . $city . "|" . $state . "|" . $zip . "|" . $country;
		my $name_on_card = $first_name . "|" . $last_name;
		# Initialize the sql statement and build it as you go...												   														  
		my $SqlStatement = "transaction_manual_check_post \"$UniqueID\", \"$user_name\", \"$months_joined\", \"$amount\", \"$x_trans_id\", \"$x_md5_hash\", \"$x_description\", \"$name_on_card\", \"$bank_ABA_code\", \"$bank_account_number\"";
			
		my $return_value = &DatabaseFunctions::Run_This_Sql_Statement($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, $ProgramName, $SqlStatement, $DebugDatabaseFunctions);
		print "\n<!-- Run_This_Sql_Statement return_value = $return_value-->\n" if $DebugThisAp eq "1";
		if($return_value eq "1")
			{
				print "\n<!-- SUCCESS:  Received message for ($transaction_id) was successfully logged to the DB. -->\n";
					
				print "                        <TABLE border=\"0\" width=\"100%\" cellspacing=\"3\" cellpadding=\"3\">\n";
				# Approved...
				# user_name / WHICH_CONNECTIONS...
				print "                          <TR>\n";
				print "                            <TD height=\"30\" colspan=\"3\">\n";
				print "                              <FONT face=\"Arial, Helvetica, sans-serif\"><STRONG><FONT size=\"3\"><FONT color=\"#FF0033\">$user_name</FONT>'s check was posted to the $Map{'WHICH_CONNECTIONS'} database.</FONT></STRONG></FONT>\n";
				print "                            </TD>\n";
				print "                          </TR>\n";
					
				# transaction_id...
				print "                          <TR valign=\"middle\">\n";
				print "                            <TD height=\"30\" width=\"32%\">\n";
				print "                              <STRONG><FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">Transaction ID:</FONT></STRONG>\n";
				print "                            </TD>\n";
				print "                            <TD height=\"30\" colspan=\"2\">\n";
				print "                              <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"> $transaction_id</FONT>\n";
				print "                            </TD>\n";
				print "                          </TR>\n";
				# x_md5_hash...
				print "                          <TR valign=\"middle\">\n";
				print "                            <TD height=\"30\" width=\"32%\">\n";
				print "                              <STRONG><FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">Date:</FONT></STRONG>\n";
				print "                            </TD>\n";
				print "                            <TD height=\"30\" colspan=\"2\">\n";
				print "                              <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"> $x_md5_hash</FONT>\n";
				print "                            </TD>\n";
				print "                          </TR>\n";
				# months_joined / amount...
				print "                          <TR valign=\"middle\">\n";
				print "                            <TD height=\"30\" width=\"32%\">\n";
				print "                              <STRONG><FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">Membership Type:</FONT></STRONG>\n";
				print "                            </TD>\n";
				print "                            <TD height=\"30\" width=\"13%\">\n";
				print "                              <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">$months_joined Months</FONT>\n";
				print "                            </TD>\n";
				print "                            <TD height=\"30\" width=\"55%\">\n";
				print "                              <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">Total: $amount (US \$)</FONT>\n";
				print "                            </TD>\n";
				print "                          </TR>\n";
				# name_on_card...
				print "                          <TR valign=\"middle\">\n";
				print "                            <TD height=\"30\" width=\"32%\">\n";
				print "                              <STRONG><FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">Name On Check:</FONT></STRONG>\n";
				print "                            </TD>\n";
				print "                            <TD height=\"30\" colspan=\"2\">\n";
				print "                              <FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\"> $name_on_card</FONT>\n";
				print "                            </TD>\n";
				print "                          </TR>\n";
			}
		else
			{
    		my $ErrorText = "";
    		if($DatabaseFunctions::DatabaseError eq "1006")
    			{
    			 	$ErrorText = "<FONT COLOR=\"#8B0000\">ERROR: User \"$user_name\" is already a paying member.</FONT><BR>\n";
    			}
			elsif($DatabaseFunctions::DatabaseError eq "1012")
				{
					$ErrorText = "<FONT COLOR=\"#8B0000\">You must first <A href=\"$Map{'CGIBIN'}/ManageEmailVerification.cgi\">verify your email address</A> before becoming a premium member.</FONT><BR><A href=\"$Map{'CGIBIN'}/ManageEmailVerification.cgi\">click here to verify email...</A><BR><BR><FONT COLOR=\"#0000FF\">Note: If you think this is incorrect please contact $Map{'EMAIL'}.</FONT><BR>\n";
				}
    		else
    			{
    			 	$ErrorText = "<FONT COLOR=\"#8B0000\">ERROR: There was a database error while trying to enter a manual check for \"$user_name\".</FONT>\n";
    			}
			&UtilityFunctions::Print_Error($ErrorText, $DebugUtilityFunctions, %Map);
			}
	}
#print "            <TR>\n";
#print "              <TD height=\"2\">\n";
#print "                &nbsp;\n";
#print "              </TD>\n";
#print "            </TR>\n";
print "          </TABLE>\n";
print "            <FORM method=\"POST\" action=\"$Map{'ROOT'}/admin/cgi-bin/Admin_GenManualCheckForm.cgi\">\n";
print "              <TABLE border=\"0\" cellspacing=\"0\" cellpadding=\"2\" bgcolor=\"#cacae3\" width=\"300\">\n";
print "                <TR>\n";
print "                  <TD align=\"center\">\n";
print "                    <TABLE border=\"0\" width=\"100%\" cellspacing=\"0\" cellpadding=\"2\" bgcolor=\"#e3e3e3\">\n";
print "                      <TR>\n";
print "                        <TH bgcolor=\"#b3b3d7\" colspan=\"8\" align=\"left\" height=\"20\">\n";
print "                          <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">Get User Data</FONT>\n";
print "                        </TH>\n";
print "                      </TR>\n";
print "                      <TR>\n";
print "                        <TD align=\"center\">\n";
print "                        </TD>\n";
print "                        <TD align=\"right\">\n";
print "                          <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">User Name:</FONT>\n";
print "                        </TD>\n";
print "                        <TD>\n";
print "                          <INPUT name=\"user_name\" size=\"20\" value=\"$user_name\">\n";
print "                        </TD>\n";
print "                      </TR>\n";
print "                      <TR>\n";
print "                        <TD bgcolor=\"#cacae3\" colspan=\"3\" align=\"center\" valign=\"middle\" height=\"20\">\n";
print "						   	   <INPUT type=\"submit\" name=\"submit\" value=\"Update Form\">\n";
print "                        </TD>\n";
print "                      </TR>\n";
print "                    </TABLE>\n";
print "                  </TD>\n";
print "                </TR>\n";
print "              </TABLE>\n";
print "          </FORM>\n";

print "<SCRIPT language=\"javascript\" src=\"$Map{'ROOT'}/JavaScript/Admin_GenManualCheckForm.js\"></SCRIPT>\n";

&UtilityFunctions::Print_HTML_Bottom($ProgramName, $DebugUtilityFunctions, %Map);

#End BODY...
print "</BODY>\n";

#End HTML...
print "</HTML>\n";
exit 0;
