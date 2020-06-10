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

my $ProgramName = "ML_GetCampaignSummary.cgi";

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

my @QueryStringParams;
my %QueryStringHash;

# Load the values passed in into the QueryStringHash...
@QueryStringParams = CGI::param();
%QueryStringHash = &CgiFunctions::Load_Query_String_Hash(\@QueryStringParams, \$DebugCgiFunctions);

	
my $SqlStatement  = "";

if($QueryStringHash{'min_value'} and $QueryStringHash{'max_value'})
	{
		$SqlStatement = "admin_GetSummaryCampaignInfoByMinMaxId \'$QueryStringHash{'min_value'}\', \'$QueryStringHash{'max_value'}\'";
	}
else
	{
		&UtilityFunctions::Print_Error("LinkMap Error.<BR><BR>Contact Site Administrator.", $DebugUtilityFunctions, %Map);
	}

my $total_attempted    			  = "";
my $total_failed				  = "";
my $total_succeded				  = "";
my $percent_presumed_sent		  = "";
my $total_clicks				  = "";
my $unique_clicks				  = "";
my $total_joined				  = "";
my $total_paid					  = "";
my $percent_succeded_that_clicked = "";
my $percent_clicks_that_joined	  = "";

my $Temp = "";


# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);

# Begin Title Table...
print "   <!-- Begin Dynamic Content Table -->\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <TR>\n";
print "        <TD align=\"center\">\n";
print "		   <H1>Campaign info</H1>\n";
print "        </TD>\n";
print "       </TR>\n";
print "    </TABLE>\n";

	
print "   <!-- Begin Dynamic Content Table -->\n";
print "   <FORM name=\"FormOne\" method=\"GET\" action=\"test.cgi\" onSubmit=\"return checkForm(this)\">\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <!-- Begin Column Title Rows (Sortable) -->\n";
print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
print "        <TD>\n";
print "          total attempted\n";
print "        </TD>\n";
print "        <TD>\n";
print "          total failed\n";
print "        </TD>\n";
print "        <TD>\n";
print "          total succeded\n";
print "        </TD>\n";
print "        <TD>\n";
print "          \% presumed sent\n";
print "        </TD>\n";
print "        <TD>\n";
print "          total clicks\n";
print "        </TD>\n";
print "        <TD>\n";
print "          unique clicks\n";
print "        </TD>\n";
print "        <TD>\n";
print "          total joined\n";
print "        </TD>\n";
print "        <TD>\n";
print "          total paid\n";
print "        </TD>\n";
print "        <TD>\n";
print "          \% succeded that clicked\n";
print "        </TD>\n";
print "        <TD>\n";
print "          \% clicks that joined\n";
print "        </TD>\n";
	
print "      </TR>\n";
print "	<!-- End Column Title Rows (Sortable) -->\n";

my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'ML_DBUSER'}, $Map{'ML_DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();

##########################
# Get SECOND result set...
##########################
# a simple counter variable...
$status = $MSSQL::DBlib::dbh->dbresults();
if($status != FAIL && $DatabaseFunctions::DatabaseError ne "1")
	{
		my %dataref = ("jason" => "baumbach");
		my $dataref = \%dataref;
		while ($MSSQL::DBlib::dbh->dbnextrow2($dataref, 1) != NO_MORE_ROWS )
			{
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
				else
					{
						# Since there is no global DB error check get 
						# all database fields returned by the query...
						$total_attempted    		  = $$dataref{total_attempted};
						$total_failed				  = $$dataref{total_failed};
						$total_succeded				  = $$dataref{total_succeded};
						$percent_presumed_sent		  = $$dataref{percent_presumed_sent};
						$total_clicks				  = $$dataref{total_clicks};
						$unique_clicks				  = $$dataref{unique_clicks};
						$total_joined				  = $$dataref{total_joined};
						$total_paid					  = $$dataref{total_paid};
						$percent_succeded_that_clicked= $$dataref{percent_succeded_that_clicked};
						$percent_clicks_that_joined   = $$dataref{percent_clicks_that_joined};
							
						if($DebugThisAp eq "1")
							{
								print "<!-- total_attempted               = ($total_attempted) -->\n";
								print "<!-- total_failed                  = ($total_failed) -->\n";
								print "<!-- total_succeded                = ($total_succeded) -->\n";
								print "<!-- percent_presumed_sent         = ($percent_presumed_sent) -->\n";
								print "<!-- total_clicks                  = ($total_clicks) -->\n";
								print "<!-- unique_clicks                 = ($unique_clicks) -->\n";
								print "<!-- total_joined                  = ($total_joined) -->\n";
								print "<!-- total_paid                    = ($total_paid) -->\n";
								print "<!-- percent_succeded_that_clicked = ($percent_succeded_that_clicked) -->\n";
								print "<!-- percent_clicks_that_joined    = ($percent_clicks_that_joined) -->\n";
							}
							
						print "      <TR bgcolor=\"$Map{'OUTBOX_COLOR_1'}\">\n";
						print "          <!-- total_attempted -->\n";
						print "        <TD>\n";
						print "          $total_attempted\n";
						print "        </TD>\n";
							
						print "          <!-- total_failed -->\n";
						print "        <TD>\n";
						print "          $total_failed\n";
						print "        </TD>\n";
							
						print "          <!-- total_succeded -->\n";
						print "        <TD>\n";
						print "          $total_succeded\n";
						print "        </TD>\n";
							
						print "          <!-- percent_presumed_sent -->\n";
						print "        <TD>\n";
						print "          $percent_presumed_sent\n";
						print "        </TD>\n";

						print "          <!-- total_clicks -->\n";
						print "        <TD>\n";
						print "          $total_clicks\n";
						print "        </TD>\n";

						print "          <!-- unique_clicks -->\n";
						print "        <TD>\n";
						print "          $unique_clicks\n";
						print "        </TD>\n";

						print "          <!-- total_joined -->\n";
						print "        <TD>\n";
						print "          $total_joined\n";
						print "        </TD>\n";

						print "          <!-- total_paid -->\n";
						print "        <TD>\n";
						print "          $total_paid\n";
						print "        </TD>\n";

						print "          <!-- percent_succeded_that_clicked -->\n";
						print "        <TD>\n";
						print "          $percent_succeded_that_clicked\n";
						print "        </TD>\n";

						print "          <!-- percent_clicks_that_joined -->\n";
						print "        <TD>\n";
						print "          $percent_clicks_that_joined\n";
						print "        </TD>\n";

						print "      </TR>\n";
							
					}# END else (No db error) 
			}# END while
			
		print "      <TR>\n";
		print "          <!-- Limit by min / max values -->\n";
		print "        <TD colspan=\"15\" align=\"right\" height=\"21\">\n";
		print "          <FONT face=\"arial, Helvetica, sans-serif\" size=\"2\">Get Campaigns between </FONT>\n";
		print "          <INPUT type=\"text\" name=\"min_value\" size=\"10\">\n";
		print "          <FONT face=\"arial, Helvetica, sans-serif\" size=\"2\"> and </FONT>\n";
		print "          <INPUT type=\"text\" name=\"max_value\" size=\"10\">\n";
		print "          <INPUT type=\"submit\" name=\"submit\" value=\"submit\">\n";
		print "        </TD>\n";
		print "       </TR>\n";
		print "    </TABLE>\n";
		print "   </FORM>\n";
		print "   <!-- End Dynamic Content Table -->\n";
	}# END if($status == SUCCEED)
else
	{
		print "ERROR: $SqlStatement Failed with dbresults status = ($status).\n";
	}
# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName?", "", "", "100", "1", "1", $DebugUtilityFunctions, %Map);

#End HTML...
#print "<SCRIPT type=\"text/javascript\" language=\"javascript\" src=\"/JavaScript/ML_GetAllMailSentLog.js\"></SCRIPT>";
print "</HTML>\n";

exit 0;
