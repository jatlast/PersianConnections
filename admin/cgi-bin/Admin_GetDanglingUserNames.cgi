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

my $ProgramName = "Admin_GetDanglingUserNames.cgi";

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
	
my $SqlStatement  = "admin_GetDanglingUserNames";

# database variables...
my $UserName = "";

my $Total = 0;
# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);
	
my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();

##########################
# Get count result set...
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

# Begin the Body Table...
print "   <!-- Begin Dynamic Content Table -->\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <TR>\n";
print "          <!-- Limit by user_name form -->\n";
print "        <TD align=\"center\">\n";
print "		   <H1><FONT color=\"red\">$Total</FONT> Dangling User Names Found</H1>\n";
print "        </TD>\n";
print "       </TR>\n";
print "    </TABLE>\n";
##########################
# Get dangling result set...
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
				print "      <TR align=\"left\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
				print "        <TD>\n";
				print "          Count\n";
				print "        </TD>\n";
				print "        <TD>user name</TD>\n";
				print "      </TR>\n";
				 
				my $count = 0;
				# Prevent infinite loop...
				while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS) 
					{
						$count++;
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$UserName       = $$dataref{user_name};
							
						if($DebugThisAp eq "1")
							{
								print "<!-- user_name 		= ($UserName) -->\n";
							}
						# login_info variables...
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
						print "          $count\n";
						print "			 <HR>\n";
						print "          <A href=\"javascript:newWindowDeletePic('Admin_DeleteUser.cgi?user_name=$UserName')\">Delete</A>\n";
						print "        </TD>\n";
						print "        <TD valign=\"center\">\n";
						print "          <A href=\"javascript:newWindowSingleProfile('Admin_GetAllTableInfo.cgi?user_name=$UserName')\" title=\"View all table info for $UserName\">$UserName</A>\n";
						print "        </TD>\n";
						print "      </TR>\n";
					} # END while
				print "    </TABLE>\n";
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first Dangling user_names set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}


# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName", "", "", "0", "0", "0", $DebugUtilityFunctions, %Map);

#End HTML...
print "</HTML>\n";

exit 0;
