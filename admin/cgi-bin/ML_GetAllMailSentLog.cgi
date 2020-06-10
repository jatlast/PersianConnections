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

my $ProgramName = "ML_GetAllMailSentLog.cgi";

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
if($QueryStringHash{'asc_desc'} =~ m%DESC%)
	{
		# AscDesc sets what the next search will do...
		$AscDesc = "ASC";
		# AscDesc_Not sets what the Current search order is...
		$AscDesc_Not = "DESC";
		# AscDescGif and AscDescName are for the current search...
		$AscDescGif = "descending.gif";
		$AscDescName = "Descending";
	}
elsif($QueryStringHash{'asc_desc'} =~ m%ASC%)
	{
		# AscDesc sets what the next search will do...
		$AscDesc = "DESC";
		# AscDesc_Not sets what the Current search order is...
		$AscDesc_Not = "ASC";
		# AscDescGif and AscDescName are for the current search...
		$AscDescGif = "ascending.gif";
		$AscDescName = "Ascending";
	}
else
	{
		$AscDesc = "ASC";
		$AscDesc_Not = "DESC";
		$AscDescGif = "descending.gif";
		$AscDescName = "Descending";
	}
 
if($QueryStringHash{'limit'})
	{
		$Limit = $QueryStringHash{'limit'};
	}
else
	{
		$Limit = "100";
	}
	
if($QueryStringHash{'index'})
	{
		$Index = $QueryStringHash{'index'};
	}
else
	{
		$Index = "1";
	}
	
my $SqlStatement  = "";
# Determine if this is the first time in...
if($QueryStringHash{'order_by'} eq "" and $QueryStringHash{'sql_proc'} eq "")
	{
		# Since this is the first time in (all cgi fields are empty)
		# Run the stored procedures with its default peramaters...
		$SqlStatement = "ML_GetMailSentLog";
		$OrderBy  = "unique_id";
	}
elsif($QueryStringHash{'sql_proc'} ne "")
	{
		# Since this is NOT the first time in (all cgi fields are NOT empty)
		# Run the stored procedures with the passed in peramaters...
		$SqlStatement = "$QueryStringHash{'sql_proc'}";
		$OrderBy  = "unique_id";
	}
else
	{
		# Since this is NOT the first time in (all cgi fields are NOT empty)
		# Run the stored procedures with the passed in peramaters...
		$SqlStatement = "ML_GetMailSentLog \'$QueryStringHash{'order_by'}\', \'$QueryStringHash{'asc_desc'}\', \'$QueryStringHash{'limit'}\', \'$QueryStringHash{'index'}\'";
		$OrderBy  = $QueryStringHash{'order_by'};
	}

# Generate all dynamic HTML...
# mail_sent_log variables...
my $unique_id    	= "";
my $target_audience = "";
my $when_sent		= "";
my $number_sent     = "";
my $message_sent	= "";
my $times_clicked   = "";

my $Temp = "";

my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'ML_DBUSER'}, $Map{'ML_DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
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
print "		   <H1><FONT color=\"red\">$Total</FONT> Campaigns Found</H1>\n";
print "        </TD>\n";
print "       </TR>\n";
print "    </TABLE>\n";

	
print "   <!-- Begin Dynamic Content Table -->\n";
print "   <FORM name=\"FormOne\" method=\"GET\" action=\"ML_GetCampaignSummary.cgi\" onSubmit=\"return checkForm(this)\">\n";
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_NAV_BGCOLOR'}\">\n";
print "      <!-- Begin Column Title Rows (Sortable) -->\n";
print "      <TR align=\"center\" bgcolor=\"$Map{'HTML_HEADFOOT_BGCOLOR'}\">\n";
print "        <TD>\n";
print "          Row Number\n";
print "        </TD>\n";
#print "        <TD>\n";
#print "          <A href=\"javascript:newWindowGeneric('/admin/cgi-bin/Admin_GenSendMail.cgi')\"><STRONG>Open Admin Email</STRONG></A>\n";
#print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/unique_id/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.unique_id&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By unique_id\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">unique id</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.unique_id&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By unique id\">unique id</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/target_audience/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.target_audience&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By target_audience\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">target audience</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.target_audience&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By target_audience\">target audience</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/when_sent/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.when_sent&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By when_sent\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">when sent</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.when_sent&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By when_sent\">when sent</A>\n";
	}
print "        </TD>\n";

print "        <TD>\n";			
if($OrderBy =~ m/number_sent/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.number_sent&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By number_sent\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">number sent</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.number_sent&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By number_sent\">number sent</A>\n";
	}
print "        </TD>\n";
# message_sent is stored as "TEXT" and therefore can not be used in an "ORDER BY" clause...
print "        <TD>\n";			
print "          message sent\n";
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/times_clicked/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.times_clicked&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By times_clicked\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">times clicked</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?order_by=mail_sent_log.times_clicked&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By times_clicked\">times clicked</A>\n";
	}
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
							
						$unique_id    	 = $$dataref{unique_id};
						$target_audience = $$dataref{target_audience};
						$when_sent		 = $$dataref{when_sent};
						$number_sent     = $$dataref{number_sent};
#						$message_sent	 = $$dataref{message_sent};
						$times_clicked   = $$dataref{times_clicked};
							
						if($DebugThisAp eq "1")
							{
								print "<!-- unique_id       = ($unique_id) -->\n";
								print "<!-- target_audience = ($target_audience) -->\n";
								print "<!-- when_sent       = ($when_sent) -->\n";
								print "<!-- number_sent     = ($number_sent) -->\n";
#								print "<!-- message_sent    = ($message_sent) -->\n";
								print "<!-- times_clicked   = ($times_clicked) -->\n";
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
						print "        <TD>\n";
						print "          <INPUT type=\"radio\" name=\"unique_id_min\" value=\"$unique_id\" onClick=\"setMinValueWithRadioValue(FormOne);\">&nbsp;>&nbsp;$unique_id&nbsp;>&nbsp;<INPUT type=\"radio\" name=\"unique_id_max\" value=\"$unique_id\" onClick=\"setMaxValueWithRadioValue(FormOne);\">\n";
						print "        </TD>\n";

						print "          <!-- target_audience -->\n";
						print "        <TD>\n";
						print "          $target_audience\n";
						print "        </TD>\n";
							
						print "          <!-- when_sent -->\n";
						print "        <TD>\n";
						print "          $when_sent\n";
						print "        </TD>\n";
							
						print "          <!-- number_sent -->\n";
						print "        <TD>\n";
						print "          $number_sent\n";
						print "        </TD>\n";
							
						print "          <!-- message_sent -->\n";
						print "        <TD>\n";
						print "          <A href=\"javascript:newWindowGeneric('ML_GetHtmlSent.cgi?unique_id=$unique_id')\"><STRONG>view HTML sent...</STRONG></A>\n";
						print "        </TD>\n";
							
						print "          <!-- times_clicked -->\n";
						print "        <TD>\n";
						print "          $times_clicked\n";
						print "        </TD>\n";
						print "      </TR>\n";
						print "      <!-- End $rows_processed Individual Content Row (Alternating Color) -->\n";
							
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
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName?", $OrderBy, $AscDesc_Not, $Limit, $Index, $Total, $DebugUtilityFunctions, %Map);



#End HTML...
print "<SCRIPT type=\"text/javascript\" language=\"javascript\" src=\"../../JavaScript/ML_GetAllMailSentLog.js\"></SCRIPT>";
print "</HTML>\n";

exit 0;
