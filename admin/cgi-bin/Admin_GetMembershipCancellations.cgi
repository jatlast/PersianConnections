#!/usr/local/bin/perl -w
use CGI qw/:standard/;

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

my $DebugThisAp			   = "0";
my $DebugCgiFunctions 	   = "0";
my $DebugDatabaseFunctions = "0";
my $DebugUtilityFunctions  = "0";

if($DebugThisAp eq "")
	{
		use strict;
	}

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "DatabaseFunctions.pl";
require "CgiFunctions.pl";
require "UtilityFunctions.pl";

my $ProgramName 	= "Admin_GetMembershipCancellations.cgi";

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

my $user_name 	= "";
my $sql_proc 	= "";
my $find_dups 	= "";
my $order_by 	= "";
my $asc_desc 	= "";
my $limit		= "";
my $index		= "";

if(CGI::param('sql_proc')) {$sql_proc  = CGI::param('sql_proc');}
if(CGI::param('find_dups')){$find_dups = CGI::param('find_dups');}
if(CGI::param('user_name')){$user_name = CGI::param('user_name');}
if(CGI::param('order_by')) {$order_by  = CGI::param('order_by');}
if(CGI::param('asc_desc')) {$asc_desc  = CGI::param('asc_desc');}
if(CGI::param('limit'))	   {$limit 	   = CGI::param('limit');}
if(CGI::param('index'))	   {$index 	   = CGI::param('index');}

# Determine and set the states for all possible sort conditions...
my $OrderBy  	 = "";
my $AscDesc    	 = "";
my $AscDesc_Not  = "";
my $Limit	 	 = "";
my $Index	 	 = "";
my $Total	 	 = 0;

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

if($order_by eq "")
	{
		$OrderBy = "membership_cancellation.date_cancelled";
	}
else
	{
		$OrderBy = $order_by;
	}
	
if($user_name eq "")
	{
		$UserName = "%";
	}
else
	{
		$UserName = $user_name;
	}
	
my $SqlStatement  = "";
# Determine if this is the first time in...
$SqlStatement = "admin_GetMembershipCancellations '$OrderBy', '$AscDesc', '$Limit', '$Index', '$UserName'";
$OrderBy = $order_by;

# Generate all dynamic HTML...
my $UniqueID      	 = "";
my $UserName      	 = "";
my $Email      	  	 = "";
my $DateStartedPaying= "";
my $DateCancelled    = "";
my $ReasonForLeaving = "";
my $MembershipPrices = "";
my $WebsiteDesign	 = "";
my $Suggestions      = "";

my $Temp	  	  = "";

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
						$Total = $$dataref{count};
							
						if($DebugThisAp eq "1")
							{
								print "<!-- count = ($Total) -->\n";
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
print "		   <H1><FONT color=\"red\">$Total</FONT> Profiles Found</H1>\n";
print "        </TD>\n";
print "       </TR>\n";
print "    </TABLE>\n";

	
print "   <!-- Begin Dynamic Content Table -->\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <!-- Begin Column Title Rows (Sortable) -->\n";
print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
print "        <TD>\n";
print "          <A href=\"javascript:newWindowGeneric('/DeleteAllCookies.html')\"><STRONG>Delete Cookies</STRONG></A>\n";
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/unique_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.unique_id&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By unique_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">unique id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.unique_id&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By unique_id\">unique id</A>\n";
	}
print "        </TD>\n";

print "        <TD>\n";
if($OrderBy =~ m/user_name/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By user_name\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">user name</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By user_name\">user name</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/email/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.email&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By email\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">email</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.email&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By email\">email</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/date_started_paying/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.date_started_paying&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By date_started_paying\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">date started paying</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.date_started_paying&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By date_started_paying\">date started paying</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/date_cancelled/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.date_cancelled&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By date_cancelled\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">date cancelled</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.date_cancelled&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By date_cancelled\">date cancelled</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/reason_for_leaving/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.reason_for_leaving&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By reason_for_leaving\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">reason for leaving</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.reason_for_leaving&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By reason_for_leaving\">reason for leaving</A>\n";
	}
print "        </TD>\n";

print "        <TD>\n";
if($OrderBy =~ m/membership_prices/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.membership_prices&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By membership_prices\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">membership prices</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.membership_prices&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By membership_prices\">membership prices</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/website_design/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.website_design&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By website_design\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">website design</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=membership_cancellation.website_design&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By website_design\">website design</A>\n";
	}
print "        </TD>\n";
	
# screen_quote and about_yourself are stored as "TEXT" fields and therefore can not be used in an "ORDER BY" clause...
print "        <TD>\n";			
print "          suggestions\n";
print "        </TD>\n";
	
print "      </TR>\n";
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
							
						$UniqueID = $$dataref{unique_id};
						# Remove trailing spaces from UniqueID...
						($UniqueID, $Temp) = split(/\s\s/, $UniqueID);
							
						$UserName = $$dataref{user_name};
						# Remove trailing spaces from user_name...
						($UserName, $Temp) = split(/\s\s/, $UserName);
							
						$Email = $$dataref{email};
						# Remove trailing spaces from Email...
						($Email, $Temp) = split(/\s\s/, $Email);
							
						$DateStartedPaying = $$dataref{date_started_paying};
							
						$DateCancelled = $$dataref{date_cancelled};
							
						$ReasonForLeaving = $$dataref{reason_for_leaving};

						$MembershipPrices = $$dataref{membership_prices};

						$WebsiteDesign = $$dataref{website_design};

						$Suggestions = $$dataref{suggestions};
							
						if($DebugThisAp eq "1")
							{
								print "<!--\n";
								print "unique_id           = ($UniqueID)\n";
								print "user_name           = ($UserName)\n";
								print "email               = ($Email)\n";
								print "date_started_paying = ($DateStartedPaying)\n";
								print "date_cancelled      = ($DateCancelled)\n";
								print "membership_prices   = ($MembershipPrices)\n";
								print "website_design      = ($WebsiteDesign)\n";
								print "suggestions         = ($Suggestions)\n";
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
						print "        </TD>\n";
						print "          <!-- unique_id -->\n";
						print "        <TD width=\"20\">\n";
						print "          $UniqueID\n";
						print "        </TD>\n";
						print "          <!-- user_name : View all table info for this user in new window -->\n";						
						print "        <TD valign=\"center\">\n";
						print "          <A href=\"javascript:newWindowGeneric('Admin_GetAllTableInfo.cgi?user_name=$UserName')\" title=\"View all tables for $UserName\">$UserName</A>\n";
						print "        </TD>\n";
						print "          <!-- email -->\n";						
						print "        <TD valign=\"center\">\n";
						print "          $Email\n";
						print "        </TD>\n";
						print "        </TD>\n";
						print "          <!-- date_started_paying -->\n";						
						print "        <TD valign=\"left\">\n";
						print "          $DateStartedPaying\n";
						print "        </TD>\n";
						print "          <!-- date_cancelled -->\n";						
						print "        <TD valign=\"left\">\n";
						print "          $DateCancelled\n";
						print "        </TD>\n";
						print "          <!-- reason_for_leaving -->\n";						
						print "        <TD valign=\"left\">\n";
						print "          $ReasonForLeaving\n";
						print "        </TD>\n";
						print "          <!-- membership_prices -->\n";						
						print "        <TD valign=\"left\">\n";
						print "          $MembershipPrices\n";
						print "        </TD>\n";
						print "          <!-- website_design -->\n";						
						print "        <TD valign=\"left\">\n";
						print "          $WebsiteDesign\n";
						print "        </TD>\n";
						print "          <!-- suggestions -->\n";						
						print "        <TD valign=\"left\">\n";
						print "          $Suggestions\n";
						print "        </TD>\n";
						print "      </TR>\n";
						print "      <!-- End $rows_processed Individual Content Row (Alternating Color) -->\n";
							
					}# END else (No db error) 
			}# END while
			
		print "      <TR>\n";
		print "          <!-- Limit by user_name form -->\n";
		print "        <TD colspan=\"15\" align=\"right\" height=\"21\">\n";
		print "   	    <FORM method=\"POST\" action=\"$ProgramName\">\n";
		print "          <FONT face=\"arial, Helvetica, sans-serif\" size=\"2\">Limit By User Name:</FONT>\n";
		print "          <INPUT name=\"user_name\" size=\"10\">\n";
		print "	         <INPUT type=\"hidden\" name=\"order_by\" value=\"$OrderBy\">\n";
		print "	         <INPUT type=\"hidden\" name=\"asc_desc\" value=\"$AscDesc\">\n";
		print "	         <INPUT type=\"hidden\" name=\"limit\" value=\"$Limit\">\n";
		print "	         <INPUT type=\"hidden\" name=\"index\" value=\"$Index\">\n";
		print "          <INPUT type=\"submit\" name=\"submit\" value=\"submit\">\n";
		print "         </FORM>\n";
		print "        </TD>\n";
		print "       </TR>\n";
		print "    </TABLE>\n";
		print "    <!-- End Dynamic Content Table -->\n";
	}# END if($status == SUCCEED)
else
	{
		print "ERROR: $SqlStatement Failed with dbresults status = ($status).\n";
	}
# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName?", $OrderBy, $AscDesc_Not, $Limit, $Index, $Total, $DebugUtilityFunctions, %Map);

#End HTML...
print "</HTML>\n";

exit 0;
