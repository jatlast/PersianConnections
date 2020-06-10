#!/usr/local/bin/perl -w
use CGI qw/:standard/;

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "DatabaseFunctions.pl";
require "CgiFunctions.pl";
require "UtilityFunctions.pl";

my $DebugThisAp			   = "1";
my $DebugCgiFunctions 	   = "0";
my $DebugDatabaseFunctions = "0";
my $DebugUtilityFunctions  = "0";

if($DebugThisAp eq "")
	{
		use strict;
	}

my $ProgramName 	 = "Admin_TransactionsLogAudit.cgi";

# Set autoflush to true in order to force flushing upon each print...
#$| = 1;
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
		print "<!-- $Map{'SYSTEM'} -->\n" if $DebugThisAp eq "1";
	}

my $user_name 		 = "";
my $sql_proc 		 = "";
my $find_dups 		 = "";
my $order_by 		 = "";
my $asc_desc 		 = "";
my $limit			 = "";
my $index			 = "";
my $from_date		 = "";
my $to_date			 = "";
my $XResponseCode	 = "";
my $TransactionType = "";

if(CGI::param('sql_proc')) 		  {$sql_proc  		 = CGI::param('sql_proc');}
if(CGI::param('find_dups'))		  {$find_dups 		 = CGI::param('find_dups');}
if(CGI::param('user_name'))		  {$user_name 		 = CGI::param('user_name');}
if(CGI::param('order_by')) 		  {$order_by  		 = CGI::param('order_by');}
if(CGI::param('asc_desc')) 		  {$asc_desc  		 = CGI::param('asc_desc');}
if(CGI::param('limit'))	   		  {$limit 	   		 = CGI::param('limit');}
if(CGI::param('index'))	   		  {$index 	   		 = CGI::param('index');}
if(CGI::param('from_date'))	   	  {$from_date 	   	 = CGI::param('from_date');}
if(CGI::param('to_date'))	   	  {$to_date 	   	 = CGI::param('to_date');}
if(CGI::param('x_response_code')) {$XResponseCode  = CGI::param('x_response_code');}
if(CGI::param('transaction_type')){$TransactionType = CGI::param('transaction_type');}

# Determine and set the states for all possible sort conditions...
my $OrderBy  	 = "";
my $AscDesc    	 = "";
my $AscDesc_Not  = "";
my $Limit	 	 = "";
my $Index	 	 = "";
my $CountTotal	 = 0;
my $AmountTotal	 = 0;

my $AscDescGif   = "";
my $AscDescName  = "";

# Determine and set the states for all possible sort conditions...

# Reverse the sort order criteria
# check for DESC because if this is the first time in it will not be true...
if($asc_desc =~ m%DESC%)
	{
		# AscDesc sets what the next search will do...
		$AscDesc = "ASC";
		# AscDesc_Not sets what the Current search order is...
		$AscDesc_Not = "DESC";
		# AscDescGif and AscDescName are for the current search...
		$AscDescGif = "descending.gif";
		$AscDescName = "Descending";
	}
else
	{
		$AscDesc = "DESC";
		$AscDesc_Not = "ASC";
		$AscDescGif = "ascending.gif";
		$AscDescName = "Ascending";
	}
 
if($limit eq "")
	{
		$Limit = "100";
	}
else
	{
		$Limit = $limit;
	}
	
if($index eq "")
	{
		$Index = "1";
	}
else
	{
		$Index = $index;
	}

if($from_date eq "")
	{
		$from_date = "1/1/2001";
	}
if($to_date eq "")
	{
		$to_date = "1/1/2003";
	}

my $SqlStatement  = "";
# Determine if this is the first time in...
if($order_by eq "" and $sql_proc eq "")
	{
		# Since this is the first time in (all cgi fields are empty)
		# Run the stored procedures with its default peramaters...
		$SqlStatement = "admin_TransactionsLogAudit";
		$OrderBy  = "date_of_this_transaction";
	}
elsif($sql_proc ne "")
	{
		# Since this is NOT the first time in (all cgi fields are NOT empty)
		# Run the stored procedures with the passed in peramaters...
		$SqlStatement = "$sql_proc '$find_dups'";
		$OrderBy  = "user_name";
	}
else
	{
		# Since this is NOT the first time in (all cgi fields are NOT empty)
		# Run the stored procedures with the passed in peramaters...
		$SqlStatement = "admin_TransactionsLogAudit '$order_by', '$asc_desc', '$limit', '$index', '$user_name', '$from_date', '$to_date', '$XResponseCode', '$TransactionType'";
		$OrderBy  = $order_by;
	}

# Generate all dynamic HTML...
my $is_membership_active   	 = "";
my $transaction_id      	 = "";
my $x_customer_IP	      	 = "";
my $batch_transaction_id     = "";
my $sex      	   	  	 	 = "";
my $user_id      	   	  	 = "";
my $user_name_db		  	 = "";
my $card_type      	  	  	 = "";
my $name_on_card	      	 = "";
my $cvv2_code	    	  	 = "";
my $x_cvv2_resp_code	   	 = "";
my $account_number    	  	 = "";
my $expiration_month    	 = "";
my $expiration_year    	  	 = "";
my $transaction_type	     = "";
my $x_response_code      	 = "";
my $months_joined	      	 = "";
my $amount	  			  	 = "";
my $date_of_this_transaction = "";
my $date_of_next_transaction = "";
my $x_response_subcode  	 = "";
my $x_response_reason_code	 = "";
my $x_response_reason_text   = "";
my $x_auth_code   		  	 = "";
my $x_avs_code   		  	 = "";
my $x_trans_id 			  	 = "";
my $x_md5_hash 			  	 = "";
my $x_description 		  	 = "";
my $x_method				 = "";
my $bank_ABA_code	     	 = "";
my $bank_account_number	 	 = "";
my $country					 = "";
my $password				 = "";

my $Temp	  	  		  	 = "";

# Begin Debugging...	
if($DebugThisAp eq "1")
	{
		print "<!-- sql_proc = ($sql_proc) -->\n";
		print "<!-- find_dups= ($find_dups) -->\n";
		print "<!-- user_name= ($user_name) -->\n";
		print "<!-- OrderBy  = ($OrderBy) -->\n";
		print "<!-- AscDesc  = ($AscDesc) -->\n";
		print "<!-- Limit    = ($Limit) -->\n";
		print "<!-- Index    = ($Index) -->\n";
		print "<!-- DBUSER   = ($Map{'DBUSER'}) -->\n";
		print "<!-- DBPWD    = ($Map{'DBPWD'}) -->\n";
		print "<!-- DBNAME   = ($Map{'DBNAME'}) -->\n";
		print "<!-- ApName	 = ($0) -->\n";
		print "<!-- XResponseCode	 = ($XResponseCode) -->\n";
		print "<!-- TransactionType	 = ($TransactionType) -->\n";
	}
	
my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();

##########################
# Get FIRST result set...
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
						$CountTotal  = $$dataref{count_total};
						$AmountTotal = $$dataref{amount_total};
							
						if($DebugThisAp eq "1")
							{
								print "<!-- count_total  = ($CountTotal) -->\n";
								print "<!-- amount_total = ($AmountTotal) -->\n";
							}
					}
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first result set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);

# Begin Title Table...
print "   <!-- Begin Dynamic Content Table -->\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <TR>\n";
print "        <TD align=\"center\">\n";
print "		   <H1><FONT color=\"red\">$CountTotal</FONT> Transactions Found</H1>\n";
print "		   <H2>\$<FONT color=\"red\">$AmountTotal</FONT> Total</H2>\n";
print "        </TD>\n";
print "       </TR>\n";
print "    </TABLE>\n";

	
print "   <!-- Begin Dynamic Content Table -->\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <!-- Begin Column Title Rows (Sortable) -->\n";
print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
print "        <TD>\n";
print "          <A href=\"javascript:newWindowGeneric('/DeleteAllCookies.html')\"><STRONG>Delete Cookies</STRONG></A>\n";
print "        <HR>\n";			
if($OrderBy =~ m/is_membership_active/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=billing_info.is_membership_active&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By is_membership_active\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">is membership active</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=billing_info.is_membership_active&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By is_membership_active\">is membership active</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/transaction_id/ and $OrderBy !~ m/batch_transaction_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.transaction_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By transaction_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">transaction id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.transaction_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By transaction_id\">transaction id</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_response_reason_text/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_reason_text&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_reason_text\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">xrrt</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_reason_text&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_reason_text\">xrrt</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/batch_transaction_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.batch_transaction_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By batch_transaction_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">batch transaction id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.batch_transaction_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By batch_transaction_id\">batch transaction id</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_description/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_description&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_description\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">description</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_description&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_description\">description</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/sex/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.sex&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By sex\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">sex</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.sex&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By sex\">sex</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/user_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.user_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By user_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">user id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.user_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By user_id\">user id</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/user_name/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By user_name\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">user name</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By user_name\">user name</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/country/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=contact_info.country&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By country\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">country</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=contact_info.country&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By country\">country</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/card_type/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.card_type&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By card_type\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">card type</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.card_type&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By card_type\">card type</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/name_on_card/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.name_on_card&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By name_on_card\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">name on card</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.name_on_card&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By name_on_card\">name on card</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/account_number/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.account_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By account_number\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">account number</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.account_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By account_number\">account number</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/expiration_month/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.expiration_month&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By expiration_month\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">exp month</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.expiration_month&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By expiration_month\">exp month</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/expiration_year/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.expiration_year&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By expiration_year\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">exp year</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.expiration_year&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By expiration_year\">exp year</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/bank_ABA_number/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.bank_ABA_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By bank_ABA_number\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">ABA</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.bank_ABA_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By bank_ABA_number\">ABA</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/bank_account_number/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.bank_account_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By bank_account_number\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">account #</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.bank_account_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By bank_account_number\">account #</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/x_method/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_method&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_method\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">method</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_method&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_method\">method</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/transaction_type/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.transaction_type&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By transaction_type\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">transaction type</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.transaction_type&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By transaction_type\">transaction type</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/cvv2_code/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.cvv2_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By vv2_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">cvv2 code</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.cvv2_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By cvv2_code\">cvv2 code</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_cvv2_resp_code/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_cvv2_resp_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_cvv2_resp_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">cvv2 resp</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_cvv2_resp_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_cvv2_resp_code\">cvv2 resp</A>\n";
	}
print "        </TD>\n";

print "        <TD>\n";			
if($OrderBy =~ m/months_joined/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.months_joined&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By months_joined\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">months joined</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.months_joined&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By months_joined\">months joined</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/amount/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.amount&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By amount\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">amount</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.amount&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By amount\">amount</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/date_of_this_transaction/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.date_of_this_transaction&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By date_of_this_transaction\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">this trans date</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.date_of_this_transaction&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By date_of_this_transaction\">this trans date</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/date_of_next_transaction/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.date_of_next_transaction&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By date_of_next_transaction\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">next trans date</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.date_of_next_transaction&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By date_of_next_transaction\">next trans date</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/x_response_code/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">xrc</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_code\">xrc</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_response_subcode/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_subcode&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_subcode\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">xrs</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_subcode&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_subcode\">xrs</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_response_reason_code/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_reason_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_reason_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">xrrc</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_response_reason_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_response_reason_code\">xrrc</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/x_trans_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_trans_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_trans_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">trans id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_trans_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_trans_id\">trans id</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_customer_IP/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_customer_IP&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_customer_IP\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">customer IP</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_customer_IP&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_customer_IP\">customer IP</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/x_auth_code/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_auth_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_auth_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">auth</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_auth_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_auth_code\">auth</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_avs_code/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_avs_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_avs_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">avs</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_avs_code&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_avs_code\">avs</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/x_md5_hash/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_md5_hash&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_md5_hash\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">md5</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=transactions_log.x_md5_hash&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&x_response_code=$XResponseCode&transaction_type=$TransactionType\" title=\"Sort $AscDescName By x_md5_hash\">md5</A>\n";
	}
print "        </TD>\n";


print "	<!-- End Column Title Rows (Sortable) -->\n";

##########################
# Get SECOND result set...
##########################
# a simple counter variable...
my $rows_processed = 0;
# dbresults() must be called for each result set...
$status = $MSSQL::DBlib::dbh->dbresults();
if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
	{
		my %dataref = ("jason" => "baumbach");
		my $dataref = \%dataref;
		while ( ($rows_processed < ($Index+$Limit) ) && ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS ) )
			{
				# increment the row counter...
				$rows_processed++;
				# If in debug mode, print information...
				if($DebugThisAp == 1)
					{
						print "<!-- SQL: $SqlStatement -->\n";
					}
				# Check for global DB error...
				if($DatabaseFunctions::DatabaseError eq "1")
					{
						print "ERROR: ($SqlStatement) Failed!<BR>\n";
						last;
					}
				elsif($rows_processed >= $Index)
					{
						# Reset DatabaseError...	
						#						$DatabaseFunctions::DatabaseError = "0";
							
						# Since there is no global DB error check get 
						# all database fields returned by the query...
							
						$is_membership_active = $$dataref{is_membership_active};
						# insure a value for is_membership_active...
						if(! $is_membership_active){$transaction_id = "";}
					
						$transaction_id = $$dataref{transaction_id};
						# Remove trailing spaces from transaction_id...
						if($transaction_id){$transaction_id =~ s/\s//g}
    					else{$transaction_id = "";}
					
        				$batch_transaction_id = $$dataref{batch_transaction_id};
        				if($batch_transaction_id){$batch_transaction_id =~ s/\s//g}
						else{$batch_transaction_id = "";}
			
                		$sex = $$dataref{sex};
                		# Remove trailing spaces from sex...
                		if($sex){$sex =~ s/\s//g}
						else{$sex = "";}

                		$user_id = $$dataref{user_id};
                		# Remove trailing spaces from user_id...
                		if($user_id){$user_id =~ s/\s//g}
						else{$user_id = "";}

                    $user_name_db = $$dataref{user_name};
                    # Remove trailing spaces from user_name...
                    if($user_name_db){}
                    else{$user_name_db = "";}
                    	
                    $password = $$dataref{password};
                    # Remove trailing spaces from user_name...
                    if($password){}
                    else{$password = "";}

                    $country = $$dataref{country};
                    # Remove trailing spaces from country...
                    if($country){}
                    else{$country = "";}
                    	
                    $card_type = $$dataref{card_type};
                    if($card_type){}
                    else{$card_type = "";}
                    	
                    $name_on_card = $$dataref{name_on_card};
                    # Remove trailing spaces from name_on_card...
                    if($name_on_card){}
                    else{$name_on_card = "";}
                    	
                    $cvv2_code = $$dataref{cvv2_code};
                    # Remove trailing spaces from cvv2_code...
                    if($cvv2_code){$cvv2_code =~ s/\s//g}
                    else{$cvv2_code = "";}
                    	
                    $x_cvv2_resp_code = $$dataref{x_cvv2_resp_code};
                    # Remove trailing spaces from x_cvv2_resp_code...
                    if($x_cvv2_resp_code){$x_cvv2_resp_code =~ s/\s//g}
                    else{$x_cvv2_resp_code = "";}
                    	
                    $account_number = $$dataref{account_number};
                    # Remove trailing spaces from account_number...
                    if($account_number){$account_number =~ s/\s//g}
                    else{$account_number = "";}
                    	
                    $expiration_month = $$dataref{expiration_month};
                    if($expiration_month){}
                    else{$expiration_month = "";}
                    
                    $expiration_year = $$dataref{expiration_year};
                    if($expiration_year){}
                    else{$expiration_year = "";}
                    
                    $transaction_type = $$dataref{transaction_type};
                    if($transaction_type){$transaction_type =~ s/\s//g}
                    else{$transaction_type = "";}
                    
                    $x_response_code = $$dataref{x_response_code};
                    if($x_response_code){$x_response_code =~ s/\s//g}
                    else{$x_response_code = "";}
                    
                    $months_joined = $$dataref{months_joined};
                    if($months_joined){$months_joined =~ s/\s//g}
                    else{$months_joined = "";}
                    
                    $amount = $$dataref{amount};
                    if($amount){}
                    else{$amount = "";}
                    
                    $date_of_this_transaction = $$dataref{date_of_this_transaction};
                    if($date_of_this_transaction){}
                    else{$date_of_this_transaction = "";}
                    
                    $date_of_next_transaction = $$dataref{date_of_next_transaction};
                    if($date_of_next_transaction){}
                    else{$date_of_next_transaction = "";}
                    	
                    $x_response_subcode = $$dataref{x_response_subcode};
                    # Remove trailing spaces from x_response_subcode...
                    if($x_response_subcode){$x_response_subcode =~ s/\s//g}
                    else{$x_response_subcode = "";}
                    	
                    $x_response_reason_code = $$dataref{x_response_reason_code};
                    # Remove trailing spaces from x_response_reason_code...
                    if($x_response_reason_code){$x_response_reason_code =~ s/\s//g}
                    else{$x_response_reason_code = "";}
                    	
                    $x_response_reason_text = $$dataref{x_response_reason_text};
                    if($x_response_reason_text){}
                    else{$x_response_reason_text = "";}
                    	
                    $x_auth_code = $$dataref{x_auth_code};
                    # Remove trailing spaces from x_auth_code...
                    if($x_auth_code){$x_auth_code =~ s/\s//g}
                    else{$x_auth_code = "";}
                    	
                    $x_trans_id = $$dataref{x_trans_id};
                    if($x_trans_id){$x_trans_id =~ s/\s//g}
                    else{$x_trans_id = "";}
                    	
                    $x_customer_IP = $$dataref{x_customer_IP};
                    if($x_customer_IP){$x_customer_IP =~ s/\s//g}
                    else{$x_customer_IP = "";}
                    	
                    $x_md5_hash = $$dataref{x_md5_hash};
                    if($x_md5_hash){$x_md5_hash =~ s/\s//g}
                    else{$x_md5_hash = "";}
                    	
                    $x_description = $$dataref{x_description};
                    if($x_description){}
                    else{$x_description = "";}
                    	
                    $x_method = $$dataref{x_method};
                    if($x_method){$x_method =~ s/\s//g}
                    else{$x_method = "";}
                    	
                    $bank_ABA_code = $$dataref{bank_ABA_code};
                    if($bank_ABA_code){$bank_ABA_code =~ s/\s//g}
                    else{$bank_ABA_code = "";}
                    	
                    $bank_account_number = $$dataref{bank_account_number};
                    if($bank_account_number){$bank_account_number =~ s/\s//g}
                    else{$bank_account_number = "";}
                    	
                    if($DebugThisAp eq "1")
                    	{
                    		print "<!--\n";
                    		print "is_membership_active     = ($is_membership_active)\n";
                    		print "transaction_id           = ($transaction_id)\n";
                    		print "batch_transaction_id     = ($batch_transaction_id)\n";
                    		print "sex                  	= ($sex)\n";
                    		print "user_id                  = ($user_id)\n";
                    		print "user_name                = ($user_name_db)\n";
                    		print "card_type                = ($card_type)\n";
                    		print "name_on_card             = ($name_on_card)\n";
                    		print "cvv2_code				= ($cvv2_code)\n";
                    		print "account_number           = ($account_number)\n";
                    		print "expiration_month         = ($expiration_month)\n";
                    		print "expiration_year          = ($expiration_year)\n";
                    		print "transaction_type         = ($transaction_type)\n";
                    		print "x_response_code          = ($x_response_code)\n";
                    		print "months_joined            = ($months_joined)\n";
                    		print "amount                   = ($amount)\n";
                    		print "date_of_this_transaction = ($date_of_this_transaction)\n";
                    		print "date_of_next_transaction = ($amount)\n";
                    		print "x_response_subcode       = ($x_response_subcode)\n";
                    		print "x_response_reason_code   = ($x_response_reason_code)\n";
                    		print "x_response_reason_text   = ($x_response_reason_text)\n";
                    		print "x_auth_code              = ($x_auth_code)\n";
                    		print "x_avs_code               = ($x_avs_code)\n";
                    		print "x_trans_id               = ($x_trans_id)\n";
                    		print "x_customer_IP            = ($x_customer_IP)\n";
                    		print "x_md5_hash               = ($x_md5_hash)\n";
                    		print "x_description            = ($x_description)\n";
                    		print "x_method                 = ($x_method)\n";
                    		print "bank_ABA_code            = ($bank_ABA_code)\n";
                    		print "password					= ($password)\n";
                    		print "country      			= ($country)\n";
                    		print "-->\n";
                    	}
                    	
                    	
                    print "	<!-- Begin $rows_processed Individual Content Row (Alternating Color) -->\n";
                     
                     
                    if($rows_processed % 2 eq 0)
                    	{
                    		print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
                    	}
                    else
                    	{
                    		print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_2'}\">\n";
                    	}
                    print "          <!-- Checkbox and row number -->\n";						
                    print "        <TD width=\"20\">\n";
                    print "          $rows_processed\n";
                    print "        <HR>\n";
                    print "          <!-- is_membership_active -->\n";
                    if($is_membership_active == 1)
                    	{
                    		print "          <STRONG>Active</STRONG>\n";
                    	}
                    elsif($is_membership_active == 0 and $x_response_reason_text !~ m/This transaction has been approved/)
                    	{
                    		print "          <STRONG>Not Active</STRONG>\n";
                    	}
                    else
                    	{
                    		print "          <A href=\"javascript:newWindowGeneric('Admin_GetMembershipCancellations.cgi?&user_name=$user_name_db')\">View Cancellation...</A>\n";
                    	}
                    print "        </TD>\n";
                    print "          <!-- transaction_id -->\n";						
                    print "        <TD valign=\"bottom\">\n";
                    if($x_method =~ m/MANUAL/)
                    	{
		                    print "          $transaction_id\n";						
						}
					else
                    	{
		                    print "          <A href=\"javascript:newWindowGeneric('$Map{'ROOT'}/admin/log/$transaction_id.html')\" title=\"view the response page the user received when processing this transaction\">$transaction_id</A>\n";						
						}
                    print "        <HR>\n";
                    print "          <!-- x_response_reason_text -->\n";
                    if($x_response_reason_text =~ m/This transaction has been approved/)
                    	{
                    		print "          $x_response_reason_text\n";
                    	}
                    else
                    	{
                    		print "          <STRONG><FONT size=\"3\" color=\"#FF0033\">$x_response_reason_text</FONT></STRONG>\n";
                    	}
                    print "        <HR>\n";
                    print "          <!-- batch_transaction_id -->\n";						
                    print "          <A href=\"javascript:newWindowGeneric('$Map{'ROOT'}/admin/log/$batch_transaction_id.html')\" title=\"view the response page the user received when processing this transaction\">$batch_transaction_id</A>\n";
                    print "        <HR>\n";
                    print "          <!-- x_description -->\n";
                    print "          $x_description\n";
                    print "        </TD>\n";
                    print "          <!-- sex -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $sex\n";
                    print "        <HR>\n";
                    print "          <!-- user_id -->\n";
                    print "          $user_id\n";
                    print "        <HR>\n";
                    print "          <!-- user_name_db -->\n";
                    print "          $user_name_db\n";
                    print "        <HR>\n";
                    print "          <!-- country -->\n";
                    print "          $country\n";
                    print "        </TD>\n";
                    print "          <!-- card_type -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $card_type\n";
                    print "        <HR>\n";
                    print "          <!-- name_on_card -->\n";
                    print "          $name_on_card\n";
                    print "        <HR>\n";
                    print "          <!-- account_number -->\n";
                    print "          $account_number\n";
                    print "        <HR>\n";
                    print "          <!-- expiration_month -->\n";
                    print "          $expiration_month\n";
                    print "        <HR>\n";
                    print "          <!-- expiration_year -->\n";
                    print "          $expiration_year\n";
                    print "        </TD>\n";
                    print "          <!-- bank_ABA_code -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $bank_ABA_code\n";
                    print "        <HR>\n";
                    print "          <!-- bank_account_number -->\n";
                    print "          $bank_account_number\n";
                    print "        </TD>\n";
                    print "          <!-- x_method -->\n";
					print "        <TD valign=\"center\">\n";
                    print "          $x_method\n";
                    print "        <HR>\n";
                    print "          <!-- transaction_type -->\n";
                    if($transaction_type eq 'CREDIT' or $x_method eq 'MANUAL' or $x_response_reason_text !~ m/This transaction has been approved/)
                    	{
                    		print "          <STRONG><FONT size=\"3\" color=\"#FF0033\">$transaction_type</FONT></STRONG>\n" if $transaction_type eq 'CREDIT';
                    		print "          $transaction_type\n" if $transaction_type ne 'CREDIT';
                    	}
                    else
                    	{
                    		print "          <A href=\"javascript:newWindowCreditAccount('/cgi-bin/AuthorizeNetSendSSL.cgi?&admin_field=baumbach&user_name=$user_name_db&password=$password&months_joined=$months_joined&name_on_card=$name_on_card&card_type=$card_type&account_number=$account_number&exp_month=$expiration_month&exp_year=$expiration_year&x_trans_id=$x_trans_id&batch_transaction_id=&x_method=$x_method&bank_ABA_code=$bank_ABA_code&bank_account_number=$bank_account_number&transaction_type=CREDIT')\">Refund...</A>\n";
                    	}
                    print "        </TD>\n";
                    print "          <!-- cvv2_code -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $cvv2_code\n";
                    print "        <HR>\n";
                    print "          <!-- x_cvv2_resp_code -->\n";
                    print "          $x_cvv2_resp_code\n";
                    print "        </TD>\n";
                    print "          <!-- months_joined -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $months_joined\n";
                    print "        <HR>\n";
                    print "          <!-- amount -->\n";
                    print "          $amount\n";
                    print "        </TD>\n";
                    print "          <!-- date_of_this_transaction -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $date_of_this_transaction\n";
                    print "        </TD>\n";
                    print "          <!-- date_of_next_transaction -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $date_of_next_transaction\n";
                    print "        </TD>\n";
                    print "          <!-- x_response_code -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $x_response_code\n";
                    print "        <HR>\n";
                    print "          <!-- x_response_subcode -->\n";
                    print "          $x_response_subcode\n";
                    print "        <HR>\n";
                    print "          <!-- x_response_reason_code -->\n";
                    print "          $x_response_reason_code\n";
                    print "        </TD>\n";
                    print "          <!-- x_trans_id -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $x_trans_id\n";
                    print "        <HR>\n";
                    print "          <!-- x_customer_IP -->\n";
                    print "          $x_customer_IP\n";
                    print "        </TD>\n";
                    print "        <TD valign=\"center\">\n";
                    print "          <!-- x_auth_code -->\n";
                    print "          $x_auth_code\n";
                    print "        <HR>\n";
                    print "          <!-- x_avs_code -->\n";
                    print "          $x_avs_code\n";
                    print "        <HR>\n";
                    print "          <!-- x_md5_hash -->\n";
                    print "          $x_md5_hash\n";
                    print "        </TD>\n";
                    	
                    print "      <!-- End $rows_processed Individual Content Row (Alternating Color) -->\n";
                    	
                    }# END else (No db error) 
}# END while

	
print "      <TR>\n";
print "        <!-- Limiting Form -->\n";
print "        <TD colspan=\"13\" align=\"center\">\n";
print "   	    <FORM method=\"POST\" action=\"$ProgramName\">\n";
print "            <TABLE border=\"0\" cellspacing=\"0\" cellpadding=\"2\" bgcolor=\"#cacae3\" width=\"600\">\n";
print "              <TR>\n";
print "                <TD>\n";
print "                  <TABLE border=\"0\" width=\"100%\" cellspacing=\"0\" cellpadding=\"2\" bgcolor=\"#e3e3e3\">\n";
print "                    <TR>\n";
print "                      <TH bgcolor=\"#b3b3d7\" colspan=\"8\" align=\"left\" height=\"20\">\n";
print "                        <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">Limiting Form</FONT>\n";
print "                      </TH>\n";
print "                    </TR>\n";
print "                    <TR>\n";
print "                      <TD align=\"center\">\n";
print "                        <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">Date Range</FONT>\n";
print "                      </TD>\n";
print "                      <TD align=\"right\">\n";
print "                        <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">Status:</FONT>\n";
print "                      </TD>\n";
print "                      <TD>\n";
print "                        <SELECT name=\"x_response_code\">\n";
if($XResponseCode ne '')
	{
		print "                          <OPTION value=\"$XResponseCode\" selected>\n";
		if($XResponseCode eq "0")
			{
				print "                            Waiting\n";
			}
		elsif($XResponseCode eq "1")
			{
				print "                            Approved\n";
			}
		elsif($XResponseCode eq "2")
			{
				print "                            Declined\n";
			}
		elsif($XResponseCode eq "3")
			{
				print "                            Error\n";
			}
		else
			{
				print "                            ???\n";
			}
		print "                          </OPTION>\n";
	}
print "                          <OPTION value=\"\">\n";
print "                            All\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"0\">\n";
print "                            Waiting\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"1\">\n";
print "                            Approved\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"2\">\n";
print "                            Declined\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"3\">\n";
print "                            Error\n";
print "                          </OPTION>\n";
print "                        </SELECT>\n";
print "                      </TD>\n";
print "                    </TR>\n";
print "                    <TR>\n";
print "                      <TD align=\"center\">\n";
print "                        <INPUT size=\"10\" value=\"$from_date\" name=\"from_date\"> <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">&nbsp;to&nbsp;</FONT> <INPUT size=\"10\" value=\"$to_date\" name=\"to_date\">\n";
print "                      </TD>\n";
print "                      <TD align=\"right\">\n";
print "                        <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">Transaction Type:</FONT>\n";
print "                      </TD>\n";
print "                      <TD>\n";
print "                        <SELECT name=\"transaction_type\">\n";
if($TransactionType ne '')
	{
		print "                          <OPTION value=\"$TransactionType\" selected>\n";
		print "                            $TransactionType\n";
		print "                          </OPTION>\n";
	}
print "                          <OPTION value=\"\">\n";
print "                            All\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"AUTH_CAPTURE\">\n";
print "                            AUTH_CAPTURE\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"BYPASS\">\n";
print "                            BYPASS\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"MANUAL_CHECK\">\n";
print "                            MANUAL_CHECK\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"CREDIT\">\n";
print "                            CREDIT\n";
print "                          </OPTION>\n";
print "                          <OPTION value=\"VOID\">\n";
print "                            VOID\n";
print "                          </OPTION>\n";
print "                        </SELECT>\n";
print "                      </TD>\n";
print "                    </TR>\n";
print "                    <TR>\n";
print "                      <TD align=\"center\">\n";
print "                      </TD>\n";
print "                      <TD align=\"right\">\n";
print "                        <FONT size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"black\">User Name:</FONT>\n";
print "                      </TD>\n";
print "                      <TD>\n";
print "                        <INPUT name=\"user_name\" size=\"10\" value =\"$user_name\">\n";
print "                      </TD>\n";
print "                    </TR>\n";
print "                    <TR>\n";
print "                      <TD bgcolor=\"#cacae3\" colspan=\"3\" align=\"center\" valign=\"middle\" height=\"20\">\n";
print "	         <INPUT type=\"hidden\" name=\"order_by\" value=\"$OrderBy\">\n";
print "	         <INPUT type=\"hidden\" name=\"asc_desc\" value=\"$AscDesc\">\n";
print "	         <INPUT type=\"hidden\" name=\"limit\" value=\"$Limit\">\n";
print "	         <INPUT type=\"hidden\" name=\"index\" value=\"$Index\">\n";
print "                        <INPUT type=\"submit\" name=\"submit\" value=\"submit\">\n";
print "                      </TD>\n";
print "                    </TR>\n";
print "                  </TABLE>\n";
print "                </TD>\n";
print "              </TR>\n";
print "            </TABLE>\n";
print "          </FORM>\n";
print "        </TD>\n";
print "      </TR>\n";
	
	
print "    </TABLE>\n";
print "    <!-- End Dynamic Content Table -->\n";
}# END if($status == SUCCEED)
else
	{
		print "ERROR: $SqlStatement Failed with dbresults status = ($status).\n";
	}
# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName?", $OrderBy, $AscDesc_Not, $Limit, $Index, $CountTotal, $DebugUtilityFunctions, %Map);

#End HTML...
print "</HTML>\n";

exit 0;
