#!/usr/local/bin/perl -w

# For CGI functionality
use CGI qw/:standard/;
# For database access
use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;
# For Automated web access
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Response;

use strict;

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "CgiFunctions.pl";
require "DatabaseFunctions.pl";
require "SendMailFunctions.pl";
require "UtilityFunctions.pl";

my $ProgramName = "Admin_BatchAuthNetSend.pl";

my $DebugThisAp			   = "1";
my $DebugCgiFunctions 	   = "1";
my $DebugDatabaseFunctions = "1";
my $DebugUtilityFunctions  = "1";
my $DebugMailSendFunctions = "1";

# Determine what libraries to use base on the execution dir...
my $CurrentFilePath = __FILE__;
# Initialize LinkMap Hash variable "Map"...
my %Map = &UtilityFunctions::Load_LinkMap($CurrentFilePath, 1); 
 
# Severe Error:  No LinkMap.dat file found -- EXIT --
if($Map{'CONFIG'} eq 'ERROR')
	{
		print "\n\nLinkMap Error.\n\n";
		exit -1;
	}
else
	{
		print "<!-- $Map{'CONFIG'} -->\n";
		$Map{'PROGRAM_NAME'} = $ProgramName;
	}

# Parse the current date...
(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst) = localtime(time);
# use parsed date to create unique name for transaction_id and SSLOG_FILE...
# Unique Name has the folling format username_m[m]_d[d]_yyyy_h[h]_m[m]_s[s]
my $UniqueID = "AutomatedTransactions_"  . ($mon+1)  . "_" . $mday  . "_" . ($year+1900) . "_" . $hour  . "_" . $min . "_" . $sec;
# use parsed date to create unique file name for SSLog file...
my $UniqueSSLogFile = "$Map{'LOG_FOLDER'}/"  . $UniqueID . ".html";

my $batch_transaction_id = $UniqueID;

# Create and open the file that this program will populate...
open (SSLOG_FILE, "> $UniqueSSLogFile") || die "Can't open $UniqueSSLogFile: $!\n";

print SSLOG_FILE "<HTML>\n";
my $ClockStart = localtime();
print SSLOG_FILE "Start: ($ClockStart)<BR><BR>\n";

print SSLOG_FILE "<!-- $Map{'CONFIG'} --><BR>\n" if $DebugThisAp eq "1";
print SSLOG_FILE "<!-- $Map{'SYSTEM'} --><BR>\n" if $DebugThisAp eq "1";

my $ua = new LWP::UserAgent;

if($Map{'SYSTEM'} eq 'DevCgi')
	{
			$ua->proxy('http', 'http://10.10.10.11:8080/');
		#$ua->no_proxy('secapl.com');
	}

my $user_name  		         = "";
my $password  		         = "";
my $sendable   	 	  	     = "";
my $transaction_type 	   	 = "";
my $date_of_this_transaction = "";
my $date_of_next_transaction = "";
my $card_type 	   	 		 = "";
my $name_on_card	         = "";
my $cvv2_code		         = "";
my $account_number			 = "";
my $expiration_month 		 = "";
my $expiration_year 		 = "";
my $x_method 				 = "";
my $bank_ABA_code			 = "";
my $bank_account_number 	 = "";
my $bank_account_type		 = "";
my $bank_name				 = "";
my $name_on_bank_account	 = "";
my $echeck_type				 = "";
my $rebilling_amount 		 = "";
my $plan_unique_id	 		 = "";
my $street_address			 = "";
my $city					 = "";
my $state					 = "";
my $zip						 = "";
my $country					 = "";
my $telephone				 = "";
my $months_joined			 = "1";

my $Count_TotalDollarSuccess   	 = 0;
my $Count_TotalDollarNotSendable = 0;
my $Count_TotalDollarError	  	 = 0;
my $Count_ProcessingAttempts  	 = 0;
my $Count_AlreadyPayingMember 	 = 0;
my $Count_NotSendable		  	 = 0;
my $Count_UsersCharged		  	 = 0;
my $Count_UsersNotCharged	  	 = 0;
my $Count_ProcessingErrors	  	 = 0;

# Build email to send as status report...
my $BlatPath 		= "$Map{'BLAT_PATH'}/EXE/blat.exe";
my $SMTP 			= "$Map{'SMTP_HOST'}";
my $From   			= "Admin\@" . $Map{'WHICH_CONNECTIONS'} . ".com";

my $To 				= "jatlast\@hotmail.com";

my $Bcc				= "";
my $Subject			= "$Map{'WHICH_CONNECTIONS'} nightly batch status.";
my $TempFile		= "";
my $Body 			= "To review the entire transaction data written by $ProgramName open the following log file:\n\n$Map{'ROOT'}/admin/log/"  . $UniqueID . ".html\n\n";
my $TempFilePath 	= "C:\\Temp";
my $BlatLogFilePath = "$Map{'BLAT_PATH'}/EXE/blat.log";
my $return_value = 0;
my $StatusMessage = "";

my $SqlStatement = "admin_BatchNightlyTransactionSend";

my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();
	
##########################
# Get result set...
##########################
# dbresults() must be called for each result set...
$status = $MSSQL::DBlib::dbh->dbresults();
if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
	{
		if($DebugThisAp eq "1")
			{
				print SSLOG_FILE "<!-- SUCCESS: $SqlStatement returned with dbresults status = ($status). -->\n";
			}
		my %dataref = ("jason" => "baumbach");
		my $dataref = \%dataref;
		# If in debug mode, print information...
		if($DebugThisAp == 1)
			{
				print SSLOG_FILE "<!-- SQL: $SqlStatement -->\n";
			}
		# Check for global DB error...
		if($DatabaseFunctions::DatabaseError eq "1")
			{
				print SSLOG_FILE "ERROR: ($SqlStatement) Failed!<BR>\n";
				$StatusMessage = "ERROR: ($SqlStatement) Failed!\n";
			}
		else
			{
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
							
						$user_name = $$dataref{user_name};
						$user_name =~ s/\s//g;
							
						$password = $$dataref{password};
						$password =~ s/\s//g;
							
						$sendable                 = $$dataref{sendable};
						$transaction_type 		  = $$dataref{transaction_type};
						$date_of_this_transaction = $$dataref{date_of_this_transaction};
						$date_of_next_transaction = $$dataref{date_of_next_transaction};
						$card_type  			  = $$dataref{card_type};
						$name_on_card  			  = $$dataref{name_on_card};

						$cvv2_code   = $$dataref{cvv2_code};
	                    if($cvv2_code){$cvv2_code =~ s/\s//g}
		                else{$cvv2_code = "";}

						$account_number  		  = $$dataref{account_number};
						$expiration_month  		  = $$dataref{expiration_month};
						$expiration_year  		  = $$dataref{expiration_year};
						$x_method  				  = $$dataref{x_method};
						$bank_ABA_code  		  = $$dataref{bank_ABA_code};
						$bank_account_number  	  = $$dataref{bank_account_number};
						$bank_account_type	  	  = $$dataref{bank_account_type	};
						$bank_name			  	  = $$dataref{bank_name};
						$name_on_bank_account  	  = $$dataref{name_on_bank_account};
						$echeck_type			  = $$dataref{echeck_type};
						$rebilling_amount		  = $$dataref{rebilling_amount};

						$plan_unique_id	= $$dataref{plan_unique_id};
	                    $plan_unique_id	=~ s/\s//g;

						$street_address		  	  = $$dataref{street_address};
						$city				  	  = $$dataref{city};
						$state				  	  = $$dataref{state};
						$zip					  = $$dataref{zip};
						$country				  = $$dataref{country};
						$telephone				  = $$dataref{telephone};
						
						if($DebugThisAp eq "1")
							{
								print SSLOG_FILE "<!-- user_name                = ($user_name) -->\n";
								print SSLOG_FILE "<!-- password                 = ($password) -->\n";
								print SSLOG_FILE "<!-- sendable                 = ($sendable) -->\n";
								print SSLOG_FILE "<!-- transaction_type         = ($transaction_type) -->\n";
								print SSLOG_FILE "<!-- date_of_this_transaction = ($date_of_this_transaction) -->\n";
								print SSLOG_FILE "<!-- date_of_next_transaction = ($date_of_next_transaction) -->\n";
								print SSLOG_FILE "<!-- card_type                = ($card_type) -->\n";
								print SSLOG_FILE "<!-- name_on_card             = ($name_on_card) -->\n";
								print SSLOG_FILE "<!-- cvv2_code				= ($cvv2_code) -->\n";
								print SSLOG_FILE "<!-- account_number           = ($account_number) -->\n";
								print SSLOG_FILE "<!-- expiration_month         = ($expiration_month) -->\n";
								print SSLOG_FILE "<!-- expiration_year          = ($expiration_year) -->\n";
								print SSLOG_FILE "<!-- x_method                 = ($x_method) -->\n";
								print SSLOG_FILE "<!-- bank_ABA_code            = ($bank_ABA_code) -->\n";
								print SSLOG_FILE "<!-- bank_account_number      = ($bank_account_number) -->\n";
								print SSLOG_FILE "<!-- bank_account_type	  	= ($bank_account_type) -->\n";
								print SSLOG_FILE "<!-- bank_name			  	= ($bank_name) -->\n";
								print SSLOG_FILE "<!-- name_on_bank_account  	= ($name_on_bank_account) -->\n";
								print SSLOG_FILE "<!-- echeck_type              = ($echeck_type) -->\n";
								print SSLOG_FILE "<!-- rebilling_amount         = ($rebilling_amount) -->\n";
								print SSLOG_FILE "<!-- plan_unique_id           = ($plan_unique_id) -->\n";
								print SSLOG_FILE "<!-- street_address           = ($street_address) -->\n";
								print SSLOG_FILE "<!-- city                     = ($city) -->\n";
								print SSLOG_FILE "<!-- state                    = ($state) -->\n";
								print SSLOG_FILE "<!-- zip                      = ($zip) -->\n";
								print SSLOG_FILE "<!-- country                  = ($country) -->\n";
								print SSLOG_FILE "<!-- telephone                = ($telephone) -->\n";
							}																		
 							
						if($sendable eq "1")
							{
								my $AuthorizeNetSendSSLURL	= "$Map{'ROOT'}/cgi-bin/AuthorizeNetSendSSL.cgi?months_joined=$months_joined&name_on_card=$name_on_card&card_type=$card_type&cvv2_code=$cvv2_code&account_number=$account_number&expiration_month=$expiration_month&expiration_year=$expiration_year&batch_transaction_id=$batch_transaction_id&x_method=$x_method&bank_ABA_code=$bank_ABA_code&bank_account_number=$bank_account_number&bank_account_type=$bank_account_type&bank_name=$bank_name&name_on_bank_account=$name_on_bank_account&echeck_type=$echeck_type&rebilling_amount=$rebilling_amount&plan_unique_id=$plan_unique_id&street_address=$street_address&city=$city&state_code=$state&zip=$zip&country_code=$country&telephone=$telephone&transaction_type=$transaction_type";
								
								# The request method must be GET or else AuthorizeNetSendSSL.cgi will not be able to process it...
								#    This is because of the way &CgiFunctions::Load_Query_String_Hash processes the URL
								my $request = new HTTP::Request('GET', $AuthorizeNetSendSSLURL);

#								$request->push_header(Referer => 'http://www.PersianConnections.com');
#								print SSLOG_FILE "Header Referer (" . $request->header('Referer') . ").<BR>\n";
								$request->header('Cookie' => "cookie_name=$user_name; cookie_password=$password");
								my $response = $ua->request($request);
								# URL...
								print SSLOG_FILE "<HR><BR><FONT face=\"Arial, Helvetica, sans-serif\" size=\"2\">$AuthorizeNetSendSSLURL</FONT><BR>\n";
								if ($response->is_success) 
									{
										my $TempResponseContent = $response->content;
										# Response HTML...
										if ($response->content =~ m/thank you for becomming/) 
											{
												# SUCCESS Processed OK...
												print SSLOG_FILE "<BR><STRONG>SUCCESS: credit card was charged $Map{'CURRENCY_SYMBOL'}$rebilling_amount for user name (<FONT size=\"3\" color=\"#6666FF\">$user_name</FONT>).</STRONG><BR>\n";
												
												$StatusMessage = $StatusMessage . "SUCCESS: credit card was charged $Map{'CURRENCY_SYMBOL'}$rebilling_amount for user name ($user_name).\n";
												
												$Count_TotalDollarSuccess += $rebilling_amount;
												$Count_UsersCharged++;
											}
										elsif ($TempResponseContent =~ m/Error Message:/) 
											{
													$TempResponseContent =~ m%<FONT face="Arial, Helvetica, sans-serif" size="2"><FONT color="#FF0033">(.*)</FONT></FONT>%;
												print SSLOG_FILE "<BR><STRONG><FONT size=\"3\" color=\"#FF0033\">ERROR</FONT>: Unable to process credit card for user name (<FONT size=\"3\" color=\"#6666FF\">$user_name</FONT>).</STRONG><BR>\n";
												print SSLOG_FILE "<BR><STRONG>Error Message: <FONT size=\"3\" color=\"#FF0033\"> $1</FONT></STRONG><BR>\n";

												$StatusMessage = $StatusMessage . "ERROR: Unable to process credit card for user name ($user_name).\n";
												$StatusMessage = $StatusMessage . "Error Message:  $1\n";

												$Count_ProcessingErrors++;
												$Count_TotalDollarError += $rebilling_amount;
												$Count_UsersNotCharged++;
											}
										elsif ($TempResponseContent =~ m/already a paying member/) 
											{
												print SSLOG_FILE "<BR><STRONG><FONT size=\"3\" color=\"#FF0033\">ERROR</FONT>: Unable to process credit card for user name (<FONT size=\"3\" color=\"#6666FF\">$user_name</FONT>).</STRONG><BR>\n";
												print SSLOG_FILE "<BR><STRONG><FONT size=\"3\" color=\"#6666FF\">Already a Paying Member</FONT></STRONG><BR>\n";

												$StatusMessage = $StatusMessage . "ERROR: Unable to process credit card for user name ($user_name).\n";
												$StatusMessage = $StatusMessage . "Already a Paying Member\n";
												
												$Count_TotalDollarError += $rebilling_amount;
												$Count_AlreadyPayingMember++;
												$Count_UsersNotCharged++;
											}
										else
											{
												print SSLOG_FILE $response->content;
												
												$StatusMessage = $StatusMessage . "ERROR: Unable to process credit card for user name ($user_name).\n";
												$StatusMessage = $StatusMessage . "Content: " . $response->content . "\n";

												$Count_TotalDollarError += $rebilling_amount;
												$Count_UsersNotCharged++;
											}
									} 
								else 
									{
										# ERROR Unable to process...
										print SSLOG_FILE "<BR><STRONG><FONT size=\"3\" color=\"#FF0033\">ERROR</FONT>: Unable to process credit card for user name (<FONT size=\"3\" color=\"#6666FF\">$user_name</FONT>).</STRONG><BR>\n";
										print SSLOG_FILE $response->content;

										$StatusMessage = $StatusMessage . "ERROR: Unable to process credit card for user name ($user_name).\n";
										$StatusMessage = $StatusMessage . "Content: " . $response->content . "\n";

										$Count_TotalDollarError += $rebilling_amount;
										$Count_UsersNotCharged++;
									}
							}# End Sendable
						else
							{
								print SSLOG_FILE "<BR><STRONG><FONT size=\"3\" color=\"#FF0033\">Not Sendable</FONT>: Unable to process transaction type ($transaction_type) for user name (<FONT size=\"3\" color=\"#6666FF\">$user_name</FONT>).<BR>User must be charged manually or cancelled!</STRONG><BR>\n";

								$StatusMessage = $StatusMessage . "Not Sendable: Unable to process transaction type ($transaction_type) for user name ($user_name).  User must be charged manually or cancelled!\n";
								
								$Count_TotalDollarNotSendable += $rebilling_amount;
								$Count_UsersNotCharged++;
								$Count_NotSendable++;
									
							}
						$Count_ProcessingAttempts++;					
						print SSLOG_FILE "<BR>---------------------------------------- # $Count_ProcessingAttempts ----------------------------------------<BR>\n";							
					}
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print SSLOG_FILE "ERROR: $SqlStatement Failed for first result set!\n";

		$StatusMessage = "ERROR: $SqlStatement Failed for first result set!\n";
		
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}



my $ClockEnd = localtime();

if($Count_ProcessingAttempts > 0)
	{
		my $output = "";
		$Body = $StatusMessage . "\n--------------------------\n" . $Body;
		($return_value,$output)= &SendMailFunctions::Mail_Blat($BlatPath, $SMTP, $From, $To, $Bcc, $Subject, $TempFile, $Body, $TempFilePath, $BlatLogFilePath, $DebugMailSendFunctions);
		if($return_value < 1)
			{
				print "\n<!-- Mail_Blat Success return_value = $return_value \n output = $output\n-->\n" if $DebugThisAp eq "1";
			}
		else
			{
				print "\n<!-- Mail_Blat Error return_value = $return_value \n output = $output\n-->\n" if $DebugThisAp eq "1";
			}
	}

print SSLOG_FILE "Total Attempts    : ($Count_ProcessingAttempts) Total Amount ($Map{'CURRENCY_SYMBOL'}" . ($Count_TotalDollarSuccess + $Count_TotalDollarError + $Count_TotalDollarNotSendable) . ")<BR>\n";
print SSLOG_FILE "Total Success     : ($Count_UsersCharged)  Total Charged ($Map{'CURRENCY_SYMBOL'}$Count_TotalDollarSuccess)<BR>\n";
print SSLOG_FILE "Total Not Sendable: ($Count_NotSendable)  Total Not Sendable ($Map{'CURRENCY_SYMBOL'}$Count_TotalDollarNotSendable)<BR>\n";
print SSLOG_FILE "Total Error       : ($Count_UsersNotCharged)  Total Not Charged ($Map{'CURRENCY_SYMBOL'}" . ($Count_TotalDollarError + $Count_TotalDollarNotSendable) . ")<BR>\n";
print SSLOG_FILE "Processing Errors : ($Count_ProcessingErrors)<BR>\n";
print SSLOG_FILE "Already A Member  : ($Count_AlreadyPayingMember)<BR>\n";

print SSLOG_FILE "End: ($ClockEnd)<BR>\n";
#print SSLOG_FILE "Duration: ($ClockStart - $ClockEnd)\n";
if($Count_ProcessingAttempts == 0)
	{
		print SSLOG_FILE "\n<!-- OK TO DELETE -->\n";
	}
print SSLOG_FILE "</HTML>\n";
close(SSLOG_FILE);

