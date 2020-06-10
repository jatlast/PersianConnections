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

my $ProgramName 	 = "Admin_FlirtTransactionsLogAudit.cgi";

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
my $ccresp_resp		 = "";

if(CGI::param('sql_proc')) 		  {$sql_proc  		 = CGI::param('sql_proc');}
if(CGI::param('find_dups'))		  {$find_dups 		 = CGI::param('find_dups');}
if(CGI::param('user_name'))		  {$user_name 		 = CGI::param('user_name');}
if(CGI::param('order_by')) 		  {$order_by  		 = CGI::param('order_by');}
if(CGI::param('asc_desc')) 		  {$asc_desc  		 = CGI::param('asc_desc');}
if(CGI::param('limit'))	   		  {$limit 	   		 = CGI::param('limit');}
if(CGI::param('index'))	   		  {$index 	   		 = CGI::param('index');}
if(CGI::param('from_date'))	   	  {$from_date 	   	 = CGI::param('from_date');}
if(CGI::param('to_date'))	   	  {$to_date 	   	 = CGI::param('to_date');}
if(CGI::param('ccresp_resp'))     {$ccresp_resp		 = CGI::param('ccresp_resp');}

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
		$from_date = "1/1/2003";
	}
if($to_date eq "")
	{
		$to_date = "1/1/2004";
	}

my $SqlStatement  = "";
# Determine if this is the first time in...
if($order_by eq "" and $sql_proc eq "")
	{
		# Since this is the first time in (all cgi fields are empty)
		# Run the stored procedures with its default peramaters...
		$SqlStatement = "admin_FlirtTransactionsLogAudit";
		$OrderBy  = "transaction_date";
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
		$SqlStatement = "admin_FlirtTransactionsLogAudit '$order_by', '$asc_desc', '$limit', '$index', '$user_name', '$from_date', '$to_date', '$ccresp_resp'";
		$OrderBy  = $order_by;
	}

# Generate all dynamic HTML...
my $sex      	   	  	 	 = "";
my $password				 = "";
my $transaction_id      	 = "";
my $ccresp_resp			     = "";
my $cresp_resonstr		     = "";
my $addcr_respstr		     = "";
my $transaction_date		 = "";
my $user_id      	   	  	 = "";
my $user_name_db		  	 = "";
my $first_name     	   	  	 = "";
my $last_name      	   	  	 = "";
my $phone1				  	 = "";
my $phone2				  	 = "";
my $phone3				  	 = "";
my $carrier				  	 = "";
my $city				  	 = "";
my $state				  	 = "";
my $zip					  	 = "";
my $package				  	 = "";
my $addcr_credits		  	 = "";
my $cresp_amount		  	 = "";
my $card_type      	  	  	 = "";
my $expiration_month    	 = "";
my $expiration_year    	  	 = "";
my $account_number    	  	 = "";
my $affiliate_id	      	 = "";

my $Temp	  	  		  	 = "";

# Begin Debugging...	
if($DebugThisAp eq "1")
	{
		print "<!-- sql_proc     = ($sql_proc) -->\n";
		print "<!-- find_dups    = ($find_dups) -->\n";
		print "<!-- user_name    = ($user_name) -->\n";
		print "<!-- OrderBy      = ($OrderBy) -->\n";
		print "<!-- AscDesc      = ($AscDesc) -->\n";
		print "<!-- Limit        = ($Limit) -->\n";
		print "<!-- Index        = ($Index) -->\n";
		print "<!-- DBUSER       = ($Map{'DBUSER'}) -->\n";
		print "<!-- DBPWD        = ($Map{'DBPWD'}) -->\n";
		print "<!-- DBNAME       = ($Map{'DBNAME'}) -->\n";
		print "<!-- ApName	     = ($0) -->\n";
		print "<!-- ccresp_resp	 = ($ccresp_resp) -->\n";
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
#print "        <HR>\n";			
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/transaction_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.transaction_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By transaction_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">transaction id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.transaction_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By transaction_id\">transaction id</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/ccresp_resp/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.ccresp_resp&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By ccresp_resp\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">ccresp_resp</A> -- \n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.ccresp_resp&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By ccresp_resp\">ccresp_resp</A> -- \n";
	}
if($OrderBy =~ m/addcr_credits/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.addcr_credits&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By addcr_credits\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">credits</A> \n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.addcr_credits&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By addcr_credits\">credits</A> \n";
	}
if($OrderBy =~ m/addcr_respstr/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=contact_info.addcr_respstr&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By addcr_respstr\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">addcr_respstr</A> for \n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=contact_info.addcr_respstr&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By addcr_respstr\">addcr_respstr</A> for \n";
	}
if($OrderBy =~ m/ccresp_amount/)
	{
		print "          \$<A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.ccresp_amount&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By ccresp_amount\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">amount</A>\n";
	}
else
	{
		print "          \$<A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.ccresp_amount&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By ccresp_amount\">amount</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/ccresp_reasonstr/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.ccresp_reasonstr&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By ccresp_reasonstr\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">ccresp_reasonstr</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.ccresp_reasonstr&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By ccresp_reasonstr\">ccresp_reasonstr</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/sex/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.sex&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By sex\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">sex</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.sex&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By sex\">sex</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/user_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.user_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By user_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">user id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.user_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By user_id\">user id</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/user_name/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By user_name\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">user name</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By user_name\">user name</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/card_type/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.card_type&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By card_type\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">card type</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.card_type&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By card_type\">card type</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/last_name/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.last_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By last_name\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">last name</A>, \n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.last_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By last_name\">last name</A>, \n";
	}
if($OrderBy =~ m/first_name/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.first_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By first_name\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">first name</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.first_name&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By first_name\">first name</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/account_number/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.account_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By account_number\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">account number</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.account_number&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By account_number\">account number</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/expiration_month/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.expiration_month&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By expiration_month\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">exp month</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.expiration_month&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By expiration_month\">exp month</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/expiration_year/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.expiration_year&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By expiration_year\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">exp year</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.expiration_year&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By expiration_year\">exp year</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/city/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.city&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By city\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">city</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.city&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By city\">city</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/state/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.state&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By state\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">state</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.state&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By state\">state</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/zip/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.zip&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By zip\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">zip</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.zip&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By zip\">zip</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/phone1/)
	{
		print "          (<A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.phone1&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By phone1\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">phone1</A>)\n";
	}
else
	{
		print "          (<A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.phone1&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By phone1\">phone1</A>) \n";
	}
if($OrderBy =~ m/phone2/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.phone2&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By phone2\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">phone2</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.phone2&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By phone2\">phone2</A>\n";
	}
if($OrderBy =~ m/phone3/)
	{
		print "          - <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.phone3&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By phone3\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">phone3</A>\n";
	}
else
	{
		print "          - <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.phone3&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By phone3\">phone3</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/carrier/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.carrier&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By vv2_code\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">carrier</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.carrier&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By carrier\">carrier</A>\n";
	}
print "        </TD>\n";

print "        <TD>\n";			
if($OrderBy =~ m/transaction_date/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.transaction_date&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By transaction_date\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">trans date</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.transaction_date&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By transaction_date\">trans date</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/package/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.package&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By package\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">package</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.package&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By package\">package</A>\n";
	}
print "        <HR>\n";			
if($OrderBy =~ m/affiliate_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.affiliate_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By affiliate_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">affiliate id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=flirt_transactions_log.affiliate_id&asc_desc=$AscDesc&limit=$Limit&index=$Index&from_date=$from_date&to_date=$to_date&ccresp_resp=$ccresp_resp\" title=\"Sort $AscDescName By affiliate_id\">affiliate id</A>\n";
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
							
						$transaction_id = $$dataref{transaction_id};
						# Remove trailing spaces from transaction_id...
						if($transaction_id){$transaction_id =~ s/\s//g}
    					else{$transaction_id = "";}
					
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

                    $addcr_respstr = $$dataref{addcr_respstr};
                    # Remove trailing spaces from addcr_respstr...
                    if($addcr_respstr){}
                    else{$addcr_respstr = "";}
                    	
                    $card_type = $$dataref{card_type};
                    if($card_type){}
                    else{$card_type = "";}
                    	
                    $first_name = $$dataref{first_name};
                    # Remove trailing spaces from first_name...
                    if($first_name){}
                    else{$first_name = "";}
                    	
                    $last_name = $$dataref{last_name};
                    # Remove trailing spaces from first_name...
                    if($last_name){}
                    else{$last_name = "";}
                    	
                    $carrier = $$dataref{carrier};
                    # Remove trailing spaces from carrier...
                    if($carrier){$carrier =~ s/\s//g}
                    else{$carrier = "";}
                    	
                    $city = $$dataref{city};
                    # Remove trailing spaces from city...
                    if($city){$city =~ s/\s//g}
                    else{$city = "";}
                    	
                    $state = $$dataref{state};
                    if($state){}
                    else{$state = "";}
                    	
                    $zip = $$dataref{zip};
                    if($zip){$zip =~ s/\s//g}
                    else{$zip = "";}

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
                    
                    $phone3 = $$dataref{phone3};
                    if($phone3){$phone3 =~ s/\s//g}
                    else{$phone3 = "";}
                                        
                    $addcr_credits = $$dataref{addcr_credits};
                    if($addcr_credits){$addcr_credits =~ s/\s//g}
                    else{$addcr_credits = "";}
                    
                    $ccresp_amount = $$dataref{ccresp_amount};
                    if($ccresp_amount){}
                    else{$ccresp_amount = "";}
                    
                    $transaction_date = $$dataref{transaction_date};
                    if($transaction_date){}
                    else{$transaction_date = "";}
                    
                    $package = $$dataref{package};
                    # Remove trailing spaces from package...
                    if($package){$package =~ s/\s//g}
                    else{$package = "";}
                    	
                    $affiliate_id = $$dataref{affiliate_id};
                    # Remove trailing spaces from affiliate_id...
                    if($affiliate_id){$affiliate_id =~ s/\s//g}
                    else{$affiliate_id = "";}
                    	
                    $ccresp_resp = $$dataref{ccresp_resp};
                    if($ccresp_resp){}
                    else{$ccresp_resp = "";}
                    	
                    $ccresp_reasonstr = $$dataref{ccresp_reasonstr};
                    if($ccresp_reasonstr){}
                    else{$ccresp_reasonstr = "";}
                    	
                    $phone2 = $$dataref{phone2};
                    if($phone2){$phone2 =~ s/\s//g}
                    else{$phone2 = "";}
                    	
                    $phone1 = $$dataref{phone1};
                    if($phone1){$phone1 =~ s/\s//g}
                    else{$phone1 = "";}
                    	
                    if($DebugThisAp eq "1")
                    	{
                    		print "<!--\n";
                    		print "sex                  	= ($sex)\n";
                    		print "password					= ($password)\n";
                    		print "transaction_id           = ($transaction_id)\n";
                    		print "user_id                  = ($user_id)\n";
                    		print "user_name                = ($user_name_db)\n";
                    		print "card_type                = ($card_type)\n";
                    		print "first_name               = ($first_name)\n";
                    		print "last_name                = ($last_name)\n";
                    		print "carrier				    = ($carrier)\n";
                    		print "account_number           = ($account_number)\n";
                    		print "expiration_month         = ($expiration_month)\n";
                    		print "expiration_year          = ($expiration_year)\n";
                    		print "phone3		            = ($phone3)\n";
                    		print "zip                      = ($zip)\n";
                    		print "addcr_credits            = ($addcr_credits)\n";
                    		print "ccresp_amount            = ($ccresp_amount)\n";
                    		print "transaction_date         = ($transaction_date)\n";
                    		print "ccresp_amount            = ($ccresp_amount)\n";
                    		print "package                  = ($package)\n";
                    		print "affiliate_id             = ($affiliate_id)\n";
                    		print "ccresp_resp              = ($ccresp_resp)\n";
                    		print "ccresp_reasonstr         = ($ccresp_reasonstr)\n";
                    		print "phone2                   = ($phone2)\n";
                    		print "addcr_respstr            = ($addcr_respstr)\n";
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
                    print "        </TD>\n";
                    print "          <!-- transaction_id -->\n";						
                    print "        <TD valign=\"bottom\">\n";
                    if($phone2 =~ m/MANUAL/)
                    	{
		                    print "          $transaction_id\n";						
						}
					else
                    	{
		                    print "          <A href=\"javascript:newWindowGeneric('$Map{'ROOT'}/admin/log/$transaction_id.html')\" title=\"view the response page the user received when processing this transaction\">$transaction_id</A>\n";						
						}
                    print "        <HR>\n";
                    print "          <!-- ccresp_resp -->\n";
                    if($ccresp_resp =~ m/Approved/)
                    	{
                    		print "          $ccresp_resp -- \n";
                    	}
                    else
                    	{
                    		print "          <STRONG><FONT size=\"3\" color=\"#FF0033\">$ccresp_resp</FONT></STRONG> -- \n";
                    	}
                    print "          <!-- addcr_credits -->\n";
                    print "          $addcr_credits \n";
                    print "          <!-- addcr_respstr -->\n";
                    print "          $addcr_respstr for \n";
                    print "          <!-- ccresp_amount -->\n";
                    print "          \$$ccresp_amount\n";
                    print "        <HR>\n";
                    print "          <!-- ccresp_reasonstr -->\n";
                    print "          $ccresp_reasonstr\n";
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
                    print "        </TD>\n";
                    print "          <!-- card_type -->\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $card_type\n";
                    print "        <HR>\n";
                    print "          <!-- las_name, first_name -->\n";
                    print "          $last_name, $first_name\n";
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
                    print "        <TD valign=\"center\">\n";
                    print "          <!-- city -->\n";
                    print "          $city\n";
                    print "        <HR>\n";
                    print "          <!-- state -->\n";
                    print "          $state\n";
                    print "        <HR>\n";
                    print "          <!-- zip -->\n";
                    print "          $zip\n";
                    print "        </TD>\n";
                    print "        <TD valign=\"center\">\n";
                    print "          <!-- (phone1) phone2 - phone3 -->\n";
                    print "          ($phone1) $phone2 - $phone3\n";
                    print "        </TD>\n";
                    print "        <TD valign=\"center\">\n";
                    print "          <!-- carrier -->\n";
                    print "          $carrier\n";
                    print "        </TD>\n";
                    print "        <TD valign=\"center\">\n";
                    print "          $addcr_credits\n";
                    print "        <HR>\n";
                    print "          <!-- transaction_date -->\n";
                    print "          $transaction_date\n";
                    print "        </TD>\n";
                    print "        <TD valign=\"center\">\n";
                    print "          <!-- package -->\n";
                    print "          $package\n";
                    print "        <HR>\n";
                    print "          <!-- affiliate_id -->\n";
                    print "          $affiliate_id\n";
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
print "                        <SELECT name=\"ccresp_resp\">\n";
if($ccresp_resp ne '')
	{
		print "                          <OPTION value=\"$ccresp_resp\" selected>\n";
		print "                            $ccresp_resp\n";
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
