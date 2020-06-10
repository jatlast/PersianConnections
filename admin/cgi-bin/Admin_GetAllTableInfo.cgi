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

my $ProgramName = "Admin_GetAllTableInfo.cgi";

#Begin HTML so errors show up in browser...
print CGI::header('text/html');
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

my $user_name 	= "";

if(CGI::param('user_name'))	{$user_name = CGI::param('user_name');}


	
my $SqlStatement  = "";
# Determine if this is the first time in...
if($user_name eq "")
	{
		# Since this is the first time in (all cgi fields are empty)
		# Run the stored procedures with its default peramaters...
		$SqlStatement 	= "admin_GetIndividualTableInfoByUserName";
		$user_name = "PersianConnections";
	}
else
	{
		# Since this is NOT the first time in (all cgi fields are NOT empty)
		# Run the stored procedures with the passed in peramater...
		$SqlStatement = "admin_GetIndividualTableInfoByUserName '$user_name'";
	}

# login_info variables...
my $UserId_l    	 = "";
my $UserName_l       = "";
my $MembershipType_l = "";
my $Password_l       = "";
my $PasswordHint_l   = "";
my $Email_l      	 = "";
my $Sex_l			 = "";
my $CreationDate_l   = "";
my $LastLogin_l	  	 = "";
my $PhotoSubmitted_l = "";

# contact_info variables...
my $UserName_c      = "";
my $FirstName_c		= "";
my $LastName_c		= "";
my $StreetAddress_c = "";
my $City_c	      	= "";
my $State_c	      	= "";
my $Country_c	    = "";
my $Zip_c			= "";
my $Telephone_c		= "";

# personal_info variables...
my $UserName_p      = "";
my $SexPreference_p	= "";
my $Age_p			= "";
my $MaritalStatus_p	= "";
my $Profession_p   	= "";
my $Education_p    	= "";
my $Religion_p	    = "";
my $Height_p		= "";
my $Weight_p		= "";
my $Eyes_p			= "";
my $Hair_p			= "";
my $MinAgeDesired_p	= "";
my $MaxAgeDesired_p	= "";
my $Cook_p			= "";
my $Smoke_p			= "";
my $Drink_p			= "";
my $Party_p		  	= "";
my $Political_p		= "";
my $HousingStatus_p	= "";

# about_info variables...
my $UserName_a      = "";
my $ScreenQuote_a	= "";
my $AboutYourself_a = "";
my $Questionable_a  = "";

# relationship variables...
my $UserName_r        = "";
my $PreferNotToSay_r  = "";
my $AnyRelationship_r = "";
my $HangOut_r  		  = "";
my $ShortTerm_r  	  = "";
my $LongTerm_r  	  = "";
my $TalkEmail_r  	  = "";
my $PhotoExchange_r   = "";
my $Marriage_r  	  = "";
my $Other_r  		  = "";

# pictures variables...
my $UserName_pi       = "";
my $Photo_1_pi	      = "";
my $Photo_2_pi    	  = "";
my $Photo_3_pi    	  = "";
my $Photo_4_pi    	  = "";
my $Photo_5_pi	      = "";

# mail variables...
my $MailId_m       	  = "";
my $SentTo_m	      = "";
my $SentFrom_m    	  = "";
my $Subject_m    	  = "";
my $MessageText_m     = "";
my $WhenSent_m	      = "";
my $WhenRead_m	      = "";
my $SenderDeleted_m	  = "";
my $ReceiverDeleted_m = "";

# book_marks variables...
my $UserName_b     	  = "";
my $BookMark_b	      = "";

# billing_info variables...
my $UserName_bi    	         = "";
my $CardType_bi	             = "";
my $NameOnCard_bi	         = "";
my $AccountNumber_bi	     = "";
my $ExpirationMonth_bi	     = "";
my $ExpirationYear_bi	     = "";
my $IsMembershipActive_bi	 = "";
my $DateMembershipExpires_bi = "";
my $BankABACode_bi	      	 = "";
my $BankAccountNumber_bi	 = "";

# transactions_log variables...
my $TransactionId_t    	    = "";
my $UserName_t	            = "";
my $TransactionType_t	    = "";
my $XResponseCode_t	        = "";
my $MonthsJoined_t	        = "";
my $Amount_t                = "";
my $DateOfThisTransaction_t	= "";
my $DateOfNextTransaction_t = "";
my $XResponseSubcode_t	    = "";
my $XResponseReasonCode_t	= "";
my $XResponseReasonText_t	= "";
my $XAuthCode_t	 			= "";
my $XAvsCode_t	 			= "";
my $XTransId_t	 			= "";
my $XMd5Hash_t	 			= "";
my $XDescription_t	 		= "";
my $BatchTransactionId_t	= "";
my $UserId_t	 			= "";
my $CardType_t	 			= "";
my $NameOnCard_t	 		= "";
my $AccountNumber_t	 		= "";
my $ExpirationMonth_t	 	= "";
my $ExpirationYear_t	 	= "";
my $XMethod_t	 			= "";
my $BankABACode_t	 		= "";
my $BankAccountNumber_t	 	= "";

# billing_info variables...
my $UserName_bi    	         = "";
my $CardType_bi	             = "";
my $NameOnCard_bi	         = "";
my $AccountNumber_bi	     = "";
my $ExpirationMonth_bi	     = "";
my $ExpirationYear_bi	     = "";
my $IsMembershipActive_bi	 = "";
my $DateMembershipExpires_bi = "";
my $BankABACode_bi	      	 = "";
my $BankAccountNumber_bi	 = "";

# membership_cancellation variables...
my $UniqueId_mc    	     = "";
my $UserName_mc          = "";
my $Email_mc	         = "";
my $DateStartedPaying_mc = "";
my $DateCancelled_mc	 = "";
my $ReasonForLeaving_mc  = "";
my $MembershipPrices_mc	 = "";
my $WebsiteDesign_mc 	 = "";
my $Suggestions_mc	     = "";

my $Temp = "";

# Begin Debugging...	
if($DebugThisAp eq "1")
	{
		print "<!-- user_name= ($user_name) -->\n";
	}
	
# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);
	
# Begin the Body Table...
print "   <!-- Begin Dynamic Content Table -->\n";
#print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
        print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
		print "      <TR>\n";
		print "          <!-- Limit by user_name form -->\n";
		print "        <TD align=\"center\">\n";
		print "		   <H1>Individual results for: <FONT color=\"red\">$user_name</FONT></H1>\n";
		print "        </TD>\n";
		print "       </TR>\n";
		print "    </TABLE>\n";

my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();

##########################
# Get login_info result set...
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
            #####################################
            # Output for login_info
            #####################################
            
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">login info</FONT>\n";
            print "        </TD>\n";
            print "        <TD>user id</TD>\n";
            print "        <TD>user name</TD>\n";
            print "        <TD>membership type</TD>\n";
            print "        <TD>password</TD>\n";
            print "        <TD>password hint</TD>\n";
            print "        <TD>email</TD>\n";
            print "        <TD>sex</TD>\n";
            print "        <TD>creation date</TD>\n";
            print "        <TD>last login</TD>\n";
            print "        <TD>photo submitted</TD>\n";
            print "      </TR>\n";
            
            
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserId_l    	  = $$dataref{user_id};
						$UserName_l       = $$dataref{user_name};
						$MembershipType_l = $$dataref{membership_type};
						$Password_l       = $$dataref{password};
						$PasswordHint_l   = $$dataref{password_hint};
						$Email_l      	  = $$dataref{email};
						$Sex_l			  = $$dataref{sex};
						$CreationDate_l   = $$dataref{creation_date};
						$LastLogin_l	  = $$dataref{last_login};
						$PhotoSubmitted_l = $$dataref{photo_submitted};
							
						if($DebugThisAp eq "1")
							{
								print "<!-- user_id 		= ($UserId_l) -->\n";
								print "<!-- user_name 		= ($UserName_l) -->\n";
								print "<!-- membership_type = ($MembershipType_l) -->\n";
								print "<!-- password 		= ($Password_l) -->\n";
								print "<!-- password_hint 	= ($PasswordHint_l) -->\n";
								print "<!-- email 		  	= ($Email_l) -->\n";
								print "<!-- sex   			= ($Sex_l) -->\n";
								print "<!-- creation_date  	= ($CreationDate_l) -->\n";
								print "<!-- last_login 	  	= ($LastLogin_l) -->\n";
								print "<!-- photo_submitted = ($PhotoSubmitted_l) -->\n";
							}
                            # login_info variables...
                            print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                            
                            print "          <!-- Checkbox and row number -->\n";						
                            print "        <TD width=\"20\">\n";
                            print "          login_info\n";
                            print "        </TD>\n";
                            
                            print "        <TD>$UserId_l</TD>\n";
                            print "        <TD>$UserName_l</TD>\n";
                            print "        <TD>$MembershipType_l</TD>\n";
                            print "        <TD>$Password_l</TD>\n";
                            print "        <TD>$PasswordHint_l</TD>\n";
                            print "        <TD>$Email_l</TD>\n";
                            print "        <TD>$Sex_l</TD>\n";
                            print "        <TD>$CreationDate_l</TD>\n";
                            print "        <TD>$LastLogin_l</TD>\n";
                            print "        <TD>$PhotoSubmitted_l</TD>\n";
                            print "      </TR>\n";
					} # END while
                 print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first login_info set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

##########################
# Get contact_info result set...
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
            #####################################
            # Output for contact_info
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">contact info</FONT>\n";
            print "        </TD>\n";
            print "        <TD>user name</TD>\n";
            print "        <TD>first name</TD>\n";
            print "        <TD>last name</TD>\n";
            print "        <TD>street address</TD>\n";
            print "        <TD>city</TD>\n";
            print "        <TD>state</TD>\n";
            print "        <TD>country</TD>\n";
            print "        <TD>zip</TD>\n";
            print "        <TD>telephone</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_c      = $$dataref{user_name};
						$FirstName_c	 = $$dataref{first_name};
						$LastName_c		 = $$dataref{last_name};
						$StreetAddress_c = $$dataref{street_address};
						$City_c	      	 = $$dataref{city};
						$State_c	     = $$dataref{state};
						$Country_c	     = $$dataref{country};
						$Zip_c			 = $$dataref{zip};
						$Telephone_c	 = $$dataref{telephone};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name 	   	= ($UserName_c) -->\n";
								print "<!-- first_name 	   	= ($FirstName_c) -->\n";
								print "<!-- last_name 	   	= ($LastName_c) -->\n";
								print "<!-- street_address 	= ($StreetAddress_c) -->\n";
								print "<!-- city 		   	= ($City_c) -->\n";
								print "<!-- state 		   	= ($State_c) -->\n";
								print "<!-- country   	   	= ($Country_c) -->\n";
								print "<!-- zip  		   	= ($Zip_c) -->\n";
								print "<!-- telephone 	  	= ($Telephone_c) -->\n";
							}
                        
                        # contact_info variables...
                        print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          contact_info\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$UserName_c</TD>\n";
                        print "        <TD>$FirstName_c</TD>\n";
                        print "        <TD>$LastName_c</TD>\n";
                        print "        <TD>$StreetAddress_c</TD>\n";
                        print "        <TD>$City_c</TD>\n";
                        print "        <TD>$State_c</TD>\n";
                        print "        <TD>$Country_c</TD>\n";
                        print "        <TD>$Zip_c</TD>\n";
                        print "        <TD>$Telephone_c</TD>\n";
                        print "      </TR>\n";
					}# END while
                print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first contact_info set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

##########################
# Get personal_info result set...
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
            #####################################
            # Output for personal_info
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">personal info</FONT>\n";
            print "        </TD>\n";
            
            # personal_info variables...
            print "        <TD>user name</TD>\n";
            print "        <TD>sex preference</TD>\n";
            print "        <TD>age</TD>\n";
            print "        <TD>marital status</TD>\n";
            print "        <TD>profession</TD>\n";
            print "        <TD>education</TD>\n";
            print "        <TD>religion</TD>\n";
            print "        <TD>height</TD>\n";
            print "        <TD>weight</TD>\n";
            print "        <TD>eyes</TD>\n";
            print "        <TD>hair</TD>\n";
            print "        <TD>min age desired</TD>\n";
            print "        <TD>max age desired</TD>\n";
            print "        <TD>cook</TD>\n";
            print "        <TD>smoke</TD>\n";
            print "        <TD>drink</TD>\n";
            print "        <TD>party</TD>\n";
            print "        <TD>political</TD>\n";
            print "        <TD>housing status</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_p     = $$dataref{user_name};
						$SexPreference_p= $$dataref{sex_preference};
						$Age_p			= $$dataref{age};
						$MaritalStatus_p= $$dataref{marital_status};
						$Profession_p   = $$dataref{profession};
						$Education_p    = $$dataref{education};
						$Religion_p		= $$dataref{religion};
						$Height_p		= $$dataref{height};
						$Weight_p		= $$dataref{weight};
						$Eyes_p			= $$dataref{eyes};
						$Hair_p			= $$dataref{hair};
						$MinAgeDesired_p= $$dataref{min_age_desired};
						$MaxAgeDesired_p= $$dataref{max_age_desired};
						$Cook_p			= $$dataref{cook};
						$Smoke_p		= $$dataref{smoke};
						$Drink_p		= $$dataref{drink};
						$Party_p		= $$dataref{party};
						$Political_p	= $$dataref{political};
						$HousingStatus_p= $$dataref{housing_status};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name 	   	= ($UserName_p) -->\n";
								print "<!-- sex_preference 	= ($SexPreference_p) -->\n";
								print "<!-- age 	   		= ($Age_p) -->\n";
								print "<!-- marital_status 	= ($MaritalStatus_p) -->\n";
								print "<!-- profession 	   	= ($Profession_p) -->\n";
								print "<!-- education 	   	= ($Education_p) -->\n";
								print "<!-- religion 	   	= ($Religion_p) -->\n";
								print "<!-- height 	   		= ($Height_p) -->\n";
								print "<!-- weight 	   		= ($Weight_p) -->\n";
								print "<!-- eyes 	   		= ($Eyes_p) -->\n";
								print "<!-- hair 	   		= ($Hair_p) -->\n";
								print "<!-- min_age_desired = ($MinAgeDesired_p) -->\n";
								print "<!-- max_age_desired = ($MaxAgeDesired_p) -->\n";
								print "<!-- cook 	   		= ($Cook_p) -->\n";
								print "<!-- smoke 	   		= ($Smoke_p) -->\n";
								print "<!-- drink 	   		= ($Drink_p) -->\n";
								print "<!-- party 	   		= ($Party_p) -->\n";
								print "<!-- political 	   	= ($Political_p) -->\n";
								print "<!-- housing_status 	= ($HousingStatus_p) -->\n";
							}
                        
                        print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          personal_info\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$UserName_p</TD>\n";
                        print "        <TD>$SexPreference_p</TD>\n";
                        print "        <TD>$Age_p</TD>\n";
                        print "        <TD>$MaritalStatus_p</TD>\n";
                        print "        <TD>$Profession_p</TD>\n";
                        print "        <TD>$Education_p</TD>\n";
                        print "        <TD>$Religion_p</TD>\n";
                        print "        <TD>$Height_p</TD>\n";
                        print "        <TD>$Weight_p</TD>\n";
                        print "        <TD>$Eyes_p</TD>\n";
                        print "        <TD>$Hair_p</TD>\n";
                        print "        <TD>$MinAgeDesired_p</TD>\n";
                        print "        <TD>$MaxAgeDesired_p</TD>\n";
                        print "        <TD>$Cook_p</TD>\n";
                        print "        <TD>$Smoke_p</TD>\n";
                        print "        <TD>$Drink_p</TD>\n";
                        print "        <TD>$Party_p</TD>\n";
                        print "        <TD>$Political_p</TD>\n";
                        print "        <TD>$HousingStatus_p</TD>\n";
                        print "      </TR>\n";
					}# END while
               print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first personal_info set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

##########################
# Get about_info result set...
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
            #####################################
            # Output for about_info
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">about info</FONT>\n";
            print "        </TD>\n";
            
            # about_info variables...
            print "        <TD>user name</TD>\n";
            print "        <TD>screen quote</TD>\n";
            print "        <TD>about yourself</TD>\n";
            print "        <TD>questionable</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_a      = $$dataref{user_name}; 
						$ScreenQuote_a	 = $$dataref{screen_quote};
						$AboutYourself_a = $$dataref{about_yourself};
						$Questionable_a  = $$dataref{questionable};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name 	   	= ($UserName_a) -->\n";
								print "<!-- screen_quote 	= ($ScreenQuote_a) -->\n";
								print "<!-- about_yourself 	= ($AboutYourself_a) -->\n";
								print "<!-- quesitonable 	= ($Questionable_a) -->\n";
							}
                        
                        print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          about_info\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$UserName_a</TD>\n";
                        print "        <TD>$ScreenQuote_a</TD>\n";
                        print "        <TD>$AboutYourself_a</TD>\n";
                        print "        <TD>$Questionable_a</TD>\n";
                        print "      </TR>\n";
					}# END while
               print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first about_info set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

##########################
# Get relationship result set...
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
            #####################################
            # Output for relationship
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">relationship</FONT>\n";
            print "        </TD>\n";
            
            # relationship variables...
            print "        <TD>user_name</TD>\n";
            print "        <TD>prefer not to say</TD>\n";
            print "        <TD>any relationship</TD>\n";
            print "        <TD>hang out</TD>\n";
            print "        <TD>short term</TD>\n";
            print "        <TD>long term</TD>\n";
            print "        <TD>talk email</TD>\n";
            print "        <TD>photo exchange</TD>\n";
            print "        <TD>marriage</TD>\n";
            print "        <TD>other</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_r        = $$dataref{user_name};
						$PreferNotToSay_r  = $$dataref{prefer_not_to_say};
						$AnyRelationship_r = $$dataref{any_relationship};
						$HangOut_r  	   = $$dataref{hang_out};
						$ShortTerm_r  	   = $$dataref{short_term};
						$LongTerm_r  	   = $$dataref{long_term};
						$TalkEmail_r  	   = $$dataref{talk_email};
						$PhotoExchange_r   = $$dataref{photo_exchange};
						$Marriage_r  	   = $$dataref{marriage};
						$Other_r  		   = $$dataref{other};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name 	   	  = ($UserName_r) -->\n";
								print "<!-- prefer_not_to_say = ($PreferNotToSay_r) -->\n";
								print "<!-- any_relationship  = ($AnyRelationship_r) -->\n";
								print "<!-- hang_out 	   	  = ($HangOut_r) -->\n";
								print "<!-- short_term 	   	  = ($ShortTerm_r) -->\n";
								print "<!-- long_term 	   	  = ($LongTerm_r) -->\n";
								print "<!-- talk_email 	   	  = ($TalkEmail_r) -->\n";
								print "<!-- photo_exchange 	  = ($PhotoExchange_r) -->\n";
								print "<!-- marriage 	   	  = ($Marriage_r) -->\n";
								print "<!-- other 	   		  = ($Other_r) -->\n";
							}
                        
                        print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          relationship\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$UserName_r</TD>\n";
                        print "        <TD>$PreferNotToSay_r</TD>\n";
                        print "        <TD>$AnyRelationship_r</TD>\n";
                        print "        <TD>$HangOut_r</TD>\n";
                        print "        <TD>$ShortTerm_r</TD>\n";
                        print "        <TD>$LongTerm_r</TD>\n";
                        print "        <TD>$TalkEmail_r</TD>\n";
                        print "        <TD>$PhotoExchange_r</TD>\n";
                        print "        <TD>$Marriage_r</TD>\n";
                        print "        <TD>$Other_r</TD>\n";
                        print "      </TR>\n";
					}# END while
                print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first relationship set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

##########################
# Get pictures result set...
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
            #####################################
            # Output for pictures
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">pictures</FONT>\n";
            print "        </TD>\n";
            
            # login_info variables...
            print "        <TD>user name</TD>\n";
            print "        <TD>photo_1</TD>\n";
            print "        <TD>photo_2</TD>\n";
            print "        <TD>photo_3</TD>\n";
            print "        <TD>photo_4</TD>\n";
            print "        <TD>photo_5</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_pi = $$dataref{user_name};
						$Photo_1_pi	 = $$dataref{photo_1};
						$Photo_2_pi  = $$dataref{photo_2};
						$Photo_3_pi  = $$dataref{photo_3};
						$Photo_4_pi  = $$dataref{photo_4};
						$Photo_5_pi	 = $$dataref{photo_5};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name= ($UserName_pi) -->\n";
								print "<!-- photo_1  = ($Photo_1_pi) -->\n";
								print "<!-- photo_2  = ($Photo_2_pi) -->\n";
								print "<!-- photo_3  = ($Photo_3_pi) -->\n";
								print "<!-- photo_4  = ($Photo_4_pi) -->\n";
								print "<!-- photo_5  = ($Photo_5_pi) -->\n";
							}
                        
                        print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          pictures\n";
                        print "        </TD>\n";
                        # pictures variables...
                        
                        print "        <TD>$UserName_pi</TD>\n";
                        print "        <TD>$Photo_1_pi</TD>\n";
                        print "        <TD>$Photo_2_pi</TD>\n";
                        print "        <TD>$Photo_3_pi</TD>\n";
                        print "        <TD>$Photo_4_pi</TD>\n";
                        print "        <TD>$Photo_5_pi</TD>\n";
                        print "      </TR>\n";
					}# END while
                 print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first pictures set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

##########################
# Get mail result set...
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
			my $count = 0;
            #####################################
            # Output for mail
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">mail</FONT>\n";
            print "        </TD>\n";
            
            # mail variables...
            print "        <TD>mail id</TD>\n";
            print "        <TD>sent to</TD>\n";
            print "        <TD>sent from</TD>\n";
            print "        <TD>subject</TD>\n";
            print "        <TD>message text</TD>\n";
            print "        <TD>when sent</TD>\n";
            print "        <TD>when read</TD>\n";
            print "        <TD>sender deleted</TD>\n";
            print "        <TD>receiver deleted</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					$count++;
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$MailId_m          = $$dataref{mail_id};
						$SentTo_m	       = $$dataref{sent_to};
						$SentFrom_m    	   = $$dataref{sent_from};
						$Subject_m    	   = $$dataref{subject};
						$MessageText_m     = $$dataref{message_text};
						$WhenSent_m	       = $$dataref{when_sent};
						#$WhenRead_m	       = $$dataref{when_read};
						$SenderDeleted_m   = $$dataref{sender_deleted};
						$ReceiverDeleted_m = $$dataref{receiver_deleted};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- mail_id 		 = ($MailId_m) -->\n";
								print "<!-- sent_to 		 = ($SentTo_m) -->\n";
								print "<!-- sent_from 		 = ($SentFrom_m) -->\n";
								print "<!-- subject 		 = ($Subject_m) -->\n";
								print "<!-- message_text 	 = ($MessageText_m) -->\n";
								print "<!-- when_sent 		 = ($WhenSent_m) -->\n";
								#print "<!-- when_read 		 = ($WhenRead_m) -->\n";
								print "<!-- sender_deleted 	 = ($SenderDeleted_m) -->\n";
								print "<!-- receiver_deleted = ($ReceiverDeleted_m) -->\n";
							}

						if($count % 2 eq 0)
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
							}
						else
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
							}
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          mail\n";
						print "		   	 $count\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$MailId_m</TD>\n";
                        print "        <TD>$SentTo_m</TD>\n";
                        print "        <TD>$SentFrom_m</TD>\n";
                        print "        <TD>$Subject_m</TD>\n";
                        print "        <TD>$MessageText_m</TD>\n";
                        print "        <TD>$WhenSent_m</TD>\n";
                        print "        <TD>$WhenRead_m</TD>\n";
                        print "        <TD>$SenderDeleted_m</TD>\n";
                        print "        <TD>$ReceiverDeleted_m</TD>\n";
                        print "      </TR>\n";
					}# END while
                print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first mail set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}


##########################
# Get book_marks result set...
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
			my $count = 0;
            #####################################
            # Output for book_marks
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">book marks</FONT>\n";
            print "        </TD>\n";
            print "        <TD>user_name</TD>\n";
            print "        <TD>book_mark</TD>\n";
            print "      </TR>\n";	
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					$count++;
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_b = $$dataref{user_name};
						$BookMark_b	= $$dataref{book_mark};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name = ($UserName_b) -->\n";
								print "<!-- book_mark = ($BookMark_b) -->\n";
							}

						if($count % 2 eq 0)
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
							}
						else
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
							}
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          book_marks\n";
						print "		   	 $count\n";
                        print "        </TD>\n";
						# book_marks variables...
                        print "        <TD>$UserName_b</TD>\n";
                        print "        <TD>$BookMark_b</TD>\n";
                        print "      </TR>\n";	
					}# END while
				print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first book_marks set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}
	

##########################
# Get billing_info result set...
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
			my $count = 0;
            #####################################
            # Output for billing_info
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">billing_info</FONT>\n";
            print "        </TD>\n";
            
            # billing_info variables...
            print "        <TD>user name</TD>\n";
            print "        <TD>card type</TD>\n";
            print "        <TD>name on card</TD>\n";
            print "        <TD>account number</TD>\n";
            print "        <TD>expiration month</TD>\n";
            print "        <TD>expiration year</TD>\n";
            print "        <TD>is membership active</TD>\n";
            print "        <TD>date membership expires</TD>\n";
            print "        <TD>bank ABA code</TD>\n";
            print "        <TD>bank account number</TD>\n";
            print "      </TR>\n";# billing_info variables...
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					$count++;
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName_bi              = $$dataref{user_name};
						$CardType_bi	          = $$dataref{card_type};
						$NameOnCard_bi    	      = $$dataref{name_on_card};
						$AccountNumber_bi    	  = $$dataref{account_number};
						$ExpirationMonth_bi       = $$dataref{expiration_month};
						$ExpirationYear_bi	      = $$dataref{expiration_year};
						$IsMembershipActive_bi	  = $$dataref{is_membership_active};
						$DateMembershipExpires_bi = $$dataref{date_membership_expires};
						$BankABACode_bi 		  = $$dataref{bank_ABA_code};
						$BankAccountNumber_bi 	  = $$dataref{bank_account_number};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name               = ($UserName_bi) -->\n";
								print "<!-- card_type               = ($CardType_bi) -->\n";
								print "<!-- name_on_card            = ($NameOnCard_bi) -->\n";
								print "<!-- account_number          = ($AccountNumber_bi) -->\n";
								print "<!-- expiration_month        = ($ExpirationMonth_bi) -->\n";
								print "<!-- expiration_year         = ($ExpirationYear_bi) -->\n";
								print "<!-- is_membership_active    = ($IsMembershipActive_bi) -->\n";
								print "<!-- date_membership_expires = ($DateMembershipExpires_bi) -->\n";
								print "<!-- bank_ABA_code           = ($BankABACode_bi) -->\n";
								print "<!-- bank_account_number     = ($BankAccountNumber_bi) -->\n";
							}

						if($count % 2 eq 0)
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
							}
						else
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
							}
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          billing_info\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$UserName_bi</TD>\n";
                        print "        <TD>$CardType_bi</TD>\n";
                        print "        <TD>$NameOnCard_bi</TD>\n";
                        print "        <TD>$AccountNumber_bi</TD>\n";
                        print "        <TD>$ExpirationMonth_bi</TD>\n";
                        print "        <TD>$ExpirationYear_bi</TD>\n";
                        print "        <TD>$IsMembershipActive_bi</TD>\n";
                        print "        <TD>$DateMembershipExpires_bi</TD>\n";
                        print "        <TD>$BankABACode_bi</TD>\n";
                        print "        <TD>$BankAccountNumber_bi</TD>\n";
                        print "      </TR>\n";
					}# END while
                print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first billing_info set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}
	

##########################
# Get transactions_log result set...
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
			my $count = 0;
            #####################################
            # Output for transactions_log
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">transactions_log</FONT>\n";
            print "        </TD>\n";
            
            # transactions_log variables...
            print "        <TD>transaction id\n";
            print "        <HR>\n";
            print "        x response reason text\n";
            print "        <HR>\n";
            print "        batch transaciton id\n";
            print "        <HR>\n";
            print "        x description</TD>\n";
            print "        <TD>user id\n";
            print "        <HR>\n";
            print "        user name</TD>\n";
            print "        <TD>card type\n";
            print "        <HR>\n";
            print "        name on card\n";
            print "        <HR>\n";
            print "        account number\n";
            print "        <HR>\n";
            print "        expiration month\n";
            print "        <HR>\n";
            print "        expiration year</TD>\n";
            print "        <TD>bank ABA code\n";
            print "        <HR>\n";
            print "        bank account number</TD>\n";
            print "        <TD>x method\n";
            print "        <HR>\n";
            print "        transaction type</TD>\n";
            print "        <TD>months joined</TD>\n";
            print "        <TD>amount</TD>\n";
            print "        <TD>date of this transaction</TD>\n";
            print "        <TD>date of next transaction</TD>\n";
            print "        <TD>x response code\n";
            print "        <HR>\n";
            print "        x response subcode\n";
            print "        <HR>\n";
            print "        x response reason code</TD>\n";
            print "        <TD>x trans id</TD>\n";
            print "        <TD>x auth code\n";
            print "        <HR>\n";
            print "        x avs code\n";
            print "        <HR>\n";
            print "        x md5 hash</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					$count++;
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$TransactionId_t         = $$dataref{transaction_id};
						$UserName_t	             = $$dataref{user_name};
						$TransactionType_t    	 = $$dataref{transaction_type};
						$XResponseCode_t    	 = $$dataref{x_response_code};
						$MonthsJoined_t          = $$dataref{months_joined};
						$Amount_t	             = $$dataref{amount};
						$DateOfThisTransaction_t = $$dataref{date_of_this_transaction};
						$DateOfNextTransaction_t = $$dataref{date_of_next_transaction};
						$XResponseSubcode_t 	 = $$dataref{x_response_subcode};
						$XResponseReasonCode_t 	 = $$dataref{x_response_reason_code};
						$XResponseReasonText_t 	 = $$dataref{x_response_reason_text};
						$XAuthCode_t 	  		 = $$dataref{x_auth_code};
						$XAvsCode_t 	  		 = $$dataref{x_avs_code};
						$XTransId_t 	  		 = $$dataref{x_trans_id};
						$XMd5Hash_t 	  		 = $$dataref{x_md5_hash};
						$XDescription_t 	  	 = $$dataref{x_description};
						$BatchTransactionId_t 	 = $$dataref{batch_transaction_id};
						$UserId_t 	  			 = $$dataref{user_id};
						$CardType_t 	  		 = $$dataref{card_type};
						$NameOnCard_t 	  		 = $$dataref{name_on_card};
						$AccountNumber_t 	  	 = $$dataref{account_number};
						$ExpirationMonth_t 	  	 = $$dataref{expiration_month};
						$ExpirationYear_t 	  	 = $$dataref{expiration_year};
						$XMethod_t 	  			 = $$dataref{x_method};
						$BankABACode_t 	  		 = $$dataref{bank_ABA_code};
						$BankAccountNumber_t 	 = $$dataref{bank_account_number};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- transaction_id           = ($TransactionId_t) -->\n";
								print "<!-- user_name                = ($UserName_t) -->\n";
								print "<!-- transaction_type         = ($TransactionType_t) -->\n";
								print "<!-- x_response_code          = ($XResponseCode_t) -->\n";
								print "<!-- months_joined            = ($MonthsJoined_t) -->\n";
								print "<!-- amount                   = ($Amount_t) -->\n";
								print "<!-- date_of_this_transaction = ($DateOfThisTransaction_t) -->\n";
								print "<!-- date_of_next_transaciton = ($DateOfNextTransaction_t) -->\n";
								print "<!-- x_response_subcode       = ($XResponseSubcode_t) -->\n";
								print "<!-- x_response_reason_code   = ($XResponseReasonCode_t) -->\n";
								print "<!-- x_response_reason_text   = ($XResponseReasonText_t) -->\n";
								print "<!-- x_auth_code              = ($XAuthCode_t) -->\n";
								print "<!-- x_avs_code               = ($XAvsCode_t) -->\n";
								print "<!-- x_trans_id               = ($XTransId_t) -->\n";
								print "<!-- x_md5_hash               = ($XMd5Hash_t) -->\n";
								print "<!-- x_description            = ($XDescription_t) -->\n";
								print "<!-- batch_transaciton_id     = ($BatchTransactionId_t) -->\n";
								print "<!-- user_id                  = ($UserId_t) -->\n";
								print "<!-- card_type                = ($CardType_t) -->\n";
								print "<!-- name_on_card             = ($NameOnCard_t) -->\n";
								print "<!-- account_number           = ($AccountNumber_t) -->\n";
								print "<!-- expiration_month         = ($ExpirationMonth_t) -->\n";
								print "<!-- expiration_year          = ($ExpirationYear_t) -->\n";
								print "<!-- x_method                 = ($XMethod_t) -->\n";
								print "<!-- bank_ABA_code            = ($BankABACode_t) -->\n";
								print "<!-- bank_account_number      = ($BankAccountNumber_bi) -->\n";
							}

						if($count % 2 eq 0)
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
							}
						else
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
							}
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          transactions_log\n";
						print "		   	 $count\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$TransactionId_t\n";
						print "        <HR>\n";
                        print "        $XResponseReasonText_t\n";
						print "        <HR>\n";
                        print "        $BatchTransactionId_t\n";
						print "        <HR>\n";
                        print "        $XDescription_t</TD>\n";
                        print "        <TD>$UserId_t\n";
						print "        <HR>\n";
                        print "        $UserName_t</TD>\n";
                        print "        <TD>$CardType_t\n";
						print "        <HR>\n";
                        print "        $NameOnCard_t\n";
						print "        <HR>\n";
                        print "        $AccountNumber_t\n";
						print "        <HR>\n";
                        print "        $ExpirationMonth_t\n";
						print "        <HR>\n";
                        print "        $ExpirationYear_t</TD>\n";
                        print "        <TD>$BankABACode_bi\n";
						print "        <HR>\n";
                        print "        $BankAccountNumber_bi</TD>\n";
                        print "        <TD>$XMethod_t\n";
						print "        <HR>\n";
                        print "        $TransactionType_t</TD>\n";
                        print "        <TD>$MonthsJoined_t</TD>\n";
                        print "        <TD>$Amount_t</TD>\n";
                        print "        <TD>$DateOfThisTransaction_t</TD>\n";
                        print "        <TD>$DateOfNextTransaction_t</TD>\n";
                        print "        <TD>$XResponseCode_t\n";
						print "        <HR>\n";
                        print "        $XResponseSubcode_t\n";
						print "        <HR>\n";
                        print "        $XResponseReasonCode_t</TD>\n";
                        print "        <TD>$XTransId_t</TD>\n";
                        print "        <TD>$XAuthCode_t\n";
						print "        <HR>\n";
                        print "        $XAvsCode_t\n";
						print "        <HR>\n";
                        print "        $XMd5Hash_t</TD>\n";
                        print "      </TR>\n";
					}# END while
                print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first transactions_log set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}
	
##########################
# Get membership_cancellation result set...
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
			my $count = 0;
            #####################################
            # Output for membership_cancellation
            #####################################
            print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
            print "      <!-- Begin Column Title Rows (Sortable) -->\n";
            print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
            print "        <TD>\n";
            print "          <FONT color=\"red\">membership_cancellation</FONT>\n";
            print "        </TD>\n";
            
            # membership_cancellation variables...
            print "        <TD>unique id</TD>\n";
            print "        <TD>user name</TD>\n";
            print "        <TD>email</TD>\n";
            print "        <TD>date started paying</TD>\n";
            print "        <TD>date cancelled</TD>\n";
            print "        <TD>reason for leaving</TD>\n";
            print "        <TD>membership prices</TD>\n";
            print "        <TD>website design</TD>\n";
            print "        <TD>suggestions</TD>\n";
            print "      </TR>\n";
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
					$count++;
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UniqueId_mc          = $$dataref{unique_id};
						$UserName_mc	      = $$dataref{user_name};
						$Email_mc    	      = $$dataref{email};
						$DateStartedPaying_mc = $$dataref{date_started_paying};
						$DateCancelled_mc     = $$dataref{date_cancelled};
						$ReasonForLeaving_mc  = $$dataref{reason_for_leaving};
						$MembershipPrices_mc  = $$dataref{membership_prices};
						$WebsiteDesign_mc     = $$dataref{website_design};
						$Suggestions_mc       = $$dataref{suggestions};
						
						if($DebugThisAp eq "1")
							{
								print "<!-- unique_id           = ($UniqueId_mc) -->\n";
								print "<!-- user_name           = ($UserName_mc) -->\n";
								print "<!-- email               = ($Email_mc) -->\n";
								print "<!-- date_started_paying = ($DateStartedPaying_mc) -->\n";
								print "<!-- date_cancelled      = ($DateCancelled_mc) -->\n";
								print "<!-- reason_for_leaving  = ($ReasonForLeaving_mc) -->\n";
								print "<!-- membership_prices   = ($MembershipPrices_mc) -->\n";
								print "<!-- website_design      = ($WebsiteDesign_mc) -->\n";
								print "<!-- suggestions         = ($Suggestions_mc) -->\n";
							}

						if($count % 2 eq 0)
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
							}
						else
							{
								print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
							}
                        
                        print "          <!-- Checkbox and row number -->\n";						
                        print "        <TD width=\"20\">\n";
                        print "          membership_cancellation\n";
						print "		   	 $count\n";
                        print "        </TD>\n";
                        
                        print "        <TD>$UniqueId_mc</TD>\n";
                        print "        <TD>$UserName_mc</TD>\n";
                        print "        <TD>$Email_mc</TD>\n";
                        print "        <TD>$DateStartedPaying_mc</TD>\n";
                        print "        <TD>$DateCancelled_mc</TD>\n";
                        print "        <TD>$ReasonForLeaving_mc</TD>\n";
                        print "        <TD>$MembershipPrices_mc</TD>\n";
                        print "        <TD>$WebsiteDesign_mc</TD>\n";
                        print "        <TD>$Suggestions_mc</TD>\n";
                        print "      </TR>\n";
					}# END while
                print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first membership_cancellation set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}


        print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
		print "      <TR>\n";
		print "          <!-- Limit by user_name form -->\n";
		print "        <TD colspan=\"15\" align=\"right\" height=\"21\">\n";
		print "   	    <FORM method=\"POST\" action=\"$ProgramName\">\n";
		print "          <FONT face=\"arial, Helvetica, sans-serif\" size=\"2\">Enter User Name:</FONT>\n";
		print "          <INPUT name=\"user_name\" size=\"10\">\n";
		print "          <INPUT type=\"submit\" name=\"submit\" value=\"submit\">\n";
		print "         </FORM>\n";
		print "        </TD>\n";
		print "       </TR>\n";
		print "    </TABLE>\n";

# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName", "", "", "0", "0", "0", $DebugUtilityFunctions, %Map);

#End HTML...
print "</HTML>\n";

exit 0;
