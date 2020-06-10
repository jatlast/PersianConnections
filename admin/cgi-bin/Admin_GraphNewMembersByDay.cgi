#!/usr/local/bin/perl -w
use CGI qw/:standard/;

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

use GD::Graph::bars;
use GD::Graph::colour;
use GD::Graph::Data;

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

my $DebugPrintColorHTML	   = "0";

my $ProgramName 	= "Admin_GraphNewMembersByDay.cgi";

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
	}

my $goto_day		= "";
my $goto_month		= "";
my $goto_year 		= "";

if(CGI::param('goto_day'))	{$goto_day 	 = CGI::param('goto_day');}
if(CGI::param('goto_month')){$goto_month = CGI::param('goto_month');}
if(CGI::param('goto_year'))	{$goto_year  = CGI::param('goto_year');}

my $SqlStatement  = "";
# Determine if this is the first time in...
if($goto_month eq "")
	{
		# Since this is the first time in (all cgi fields are empty)
		# Run the stored procedures with its default peramaters...
		$SqlStatement 	= "admin_GraphHourlyCreationDateStatsByDayMonthYear";
	}
else
	{
		# Since this is NOT the first time in (all cgi fields are NOT empty)
		# Run the stored procedures with the passed in peramaters...
		$SqlStatement = "admin_GraphHourlyCreationDateStatsByDayMonthYear '$goto_day', '$goto_month', '$goto_year'";
	}

my $DaysInMonth  = "";
my $SearchDay	 = "";
my $SearchMonth  = "";
my $SearchYear 	 = "";

my $Hour	 	 = "";
my $NewMembers 	 = 0;

my @HourArray = ("1 AM", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12 PM", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11");
my @MonthArray = ("", "January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

my %MaxDaysInEachMonthHash = (
  'January' => 31
, 'Febuary' => 28
, 'March' => 31
, 'April' => 30
, 'May' => 31
, 'June' => 30
, 'July' => 31
, 'August' => 31
, 'September' => 30
, 'October' => 31
, 'November' => 30
, 'December' => 31
);

my @ColorsArray = ($Map{'GRAPH_COLOR_1'}
					, $Map{'GRAPH_COLOR_2'}
					, $Map{'GRAPH_COLOR_3'}
					, $Map{'GRAPH_COLOR_4'}
					, $Map{'GRAPH_COLOR_5'}
					, $Map{'GRAPH_COLOR_6'}
					);
my @LegendArray = ("Paying Now"
					, "Have Paid"
					, "Affiliated"
					, "Added Photos"
					, "Validated"
					, "Joined"
					);

my $status = $MSSQL::DBlib::dbh = MSSQL::DBlib->dblogin($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, "$ProgramName");
$status = $MSSQL::DBlib::dbh->dbcmd($SqlStatement);
$status = $MSSQL::DBlib::dbh->dbsqlexec();

##########################
# Get days_in_month result set...
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
						$DaysInMonth = $$dataref{days_in_month};
							
						if($DebugThisAp eq "1")
							{
								while( (my $Key, my $Value) = each(%$dataref) )
								{
									print "<FONT color=\"blue\">$Key</FONT> <FONT color=\"red\">$Value</FONT><BR>\n" if $DebugPrintColorHTML eq "1";
									print "<!-- $Key = ($Value) -->\n";
								}                
							}	
					}
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first result set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}


##########################
# Get search_day
# 	  , search_month 
# 	  , search_year 
# result set...
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
						$SearchDay = $$dataref{search_day};
						$SearchMonth = $$dataref{search_month};
						$SearchYear = $$dataref{search_year};
							
						if($DebugThisAp eq "1")
							{
								while( (my $Key, my $Value) = each(%$dataref) )
								{
									print "<FONT color=\"blue\">$Key</FONT> <FONT color=\"red\">$Value</FONT><BR>\n" if $DebugPrintColorHTML eq "1";
									print "<!-- $Key = ($Value) -->\n";
								}                
							}	
					}
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first result set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}

my @DaysArray;
my @NewMemberArray;
my @ValidEmailArray;
my @AddedPhotosArray;
my @ThroughAffiliateArray;
my @HavePaidArray;
my @PayingNowArray;

for(my $i=0; $i<23; $i++)
	{
		push (@NewMemberArray        	, 0);
		push (@ValidEmailArray       	, 0);
		push (@AddedPhotosArray      	, 0);
		push (@ThroughAffiliateArray 	, 0);
		push (@HavePaidArray	      	, 0);
		push (@PayingNowArray			, 0);
	}

my $TotalNewMembers			= 0;
my $TotalValidEmails		= 0;
my $TotalAddedPhotos		= 0;
my $TotalThroughAffiliate	= 0;
my $TotalHavePaid			= 0;
my $TotalPayingNow			= 0;

##########################
# Get repeating hour
#				, new_members 
# result set...
##########################
my $TotalNewMembers = 0;
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
						$Hour = $$dataref{loop_date};
							
						$NewMemberArray	        [$Hour]	= $$dataref{new_members};             
						$ValidEmailArray	    [$Hour]	= $$dataref{validated_email};         
						$AddedPhotosArray	    [$Hour]	= $$dataref{added_photos};            
						$ThroughAffiliateArray	[$Hour]	= $$dataref{joined_through_affiliate};
						$HavePaidArray	        [$Hour]	= $$dataref{paid_in_the_past};        
						$PayingNowArray			[$Hour]	= $$dataref{paying_now};              
							
						$TotalNewMembers		+= $$dataref{new_members};
						$TotalValidEmails		+= $$dataref{validated_email};
						$TotalAddedPhotos		+= $$dataref{added_photos};
						$TotalThroughAffiliate	+= $$dataref{joined_through_affiliate};
						$TotalHavePaid			+= $$dataref{paid_in_the_past};
						$TotalPayingNow			+= $$dataref{paying_now};
							
						if($DebugThisAp eq "1")
							{
								while( (my $Key, my $Value) = each(%$dataref) )
								{
									print "<FONT color=\"blue\">$Key</FONT> <FONT color=\"red\">$Value</FONT><BR>\n" if $DebugPrintColorHTML eq "1";
									print "<!-- $Key = ($Value) -->\n";
								}                
							}	
					}
			}# END else (No db error) 
	}# END if($status != FAIL)
else
	{
		print "ERROR: $SqlStatement Failed for first result set!\n";
		$status = $MSSQL::DBlib::dbh->dbcancel();
	}
	
#print "@DaysArray\n";
#print "@NewMemberArray\n";
#print "$TotalNewMembers\n";

my $FileExtension = ".png";
my $FileName = "GraphNewMembers_" . $SearchDay . $MonthArray[$SearchMonth] . $SearchYear . $FileExtension;

#print "File name: $FileName\n";

my $datavalues = GD::Graph::Data->new([
[ @HourArray ]
, [ @PayingNowArray]
, [ @HavePaidArray]
, [ @ThroughAffiliateArray]
, [ @AddedPhotosArray]
, [ @ValidEmailArray]
, [ @NewMemberArray]
]);

# Create our graph object
my $graph = GD::Graph::bars->new(800, 600);
#$graph->set_x_axis_font(gdLargFont, 18);

my @NewMemberArray_Sorted = sort(@NewMemberArray);
my $Y_MaxValue = 100;
if(pop(@NewMemberArray_Sorted) > $Y_MaxValue)
	{
		$Y_MaxValue = pop(@NewMemberArray_Sorted);
	}

# Set useful variables such as our axis labels, title, 
# coloring, etc
$graph->set(
title => "$TotalNewMembers Joined $TotalValidEmails Verified $TotalAddedPhotos Added Photos $TotalThroughAffiliate Affiliated $TotalHavePaid Paid $TotalPayingNow Paying - $MonthArray[$SearchMonth], $SearchDay $SearchYear"
, x_label => "Hour"
, y_label => "Number"
#  , y_max_value => pop(@NewMemberArray_Sorted)
, bar_spacing => $Map{'GRAPH_BAR_SPACING'}
, x_label_position => 1/2
, x_labels_vertical => 1
, shadow_depth => $Map{'GRAPH_SHADOW_DEPTH'}
, transparent => 1
, cumulate => $Map{'GRAPH_CUMULATE'}
, x_long_ticks => $Map{'GRAPH_X_LONG_TICKS'}
, y_long_ticks => $Map{'GRAPH_Y_LONG_TICKS'}
, labelclr => $Map{'GRAPH_LABELS_COLOR'}
, legendclr => $Map{'GRAPH_LEGEND_COLOR'}
, textclr => $Map{'GRAPH_TEXT_COLOR'}
, dclrs => \@ColorsArray
);

$graph->set_legend(@LegendArray);

# Actually plot the data
$graph->plot($datavalues) or die $graph->error;

# Output the image as a PNG
open(OUTPUT, ">$Map{'PICTURES_FOLDER'}/$FileName") or print "Can't open $FileName: $!\n";
binmode OUTPUT;
print OUTPUT $graph->gd->png();
close(OUTPUT);

my $verified_over_total;
my $affiliated_over_total;

my $added_photos_over_total;
my $have_paid_over_total;
my $paying_now_over_total;

my $added_photos_over_verified;
my $have_paid_over_verified;
my $paying_now_over_verified;

# Verified Over Joined
if ($TotalNewMembers > 0 and $TotalValidEmails > 0) 
	{
		$verified_over_total = ($TotalValidEmails/$TotalNewMembers*100);
		$verified_over_total = sprintf("%.2f\%", $verified_over_total);
		# Added Photos
		if ($TotalAddedPhotos > 0) 
			{
				$added_photos_over_total = ($TotalAddedPhotos/$TotalNewMembers*100);
				$added_photos_over_total = sprintf("%.2f\%", $added_photos_over_total);

				$added_photos_over_verified = ($TotalAddedPhotos/$TotalValidEmails*100);
				$added_photos_over_verified = sprintf("%.2f\%", $added_photos_over_verified);
			}
		else
			{
				$added_photos_over_total = "N/A";
				$added_photos_over_verified = "N/A";
			}

		# Have Paid
		if ($TotalHavePaid > 0) 
			{
				$have_paid_over_total = ($TotalHavePaid/$TotalNewMembers*100);
				$have_paid_over_total = sprintf("%.2f\%", $have_paid_over_total);

				$have_paid_over_verified = ($TotalHavePaid/$TotalValidEmails*100);
				$have_paid_over_verified = sprintf("%.2f\%", $have_paid_over_verified);
			}
		else
			{
				$have_paid_over_total = "N/A";
				$have_paid_over_verified = "N/A";
			}

		# Paying Now
		if ($TotalPayingNow > 0) 
			{
				$paying_now_over_total = ($TotalPayingNow/$TotalNewMembers*100);
				$paying_now_over_total = sprintf("%.2f\%", $paying_now_over_total);

				$paying_now_over_verified = ($TotalPayingNow/$TotalValidEmails*100);
				$paying_now_over_verified = sprintf("%.2f\%", $paying_now_over_verified);
			}
		else
			{
				$paying_now_over_total = "N/A";
				$paying_now_over_verified = "N/A";
			}

		# Affiliated
		if ($TotalThroughAffiliate > 0) 
			{
				$affiliated_over_total = ($TotalPayingNow/$TotalNewMembers*100);
				$affiliated_over_total = sprintf("%.2f\%", $affiliated_over_total);
			}
		else
			{
				$affiliated_over_total = "N/A";
			}
	}
else
	{
		$verified_over_total = "N/A";
	}


# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);
	
# Begin the Body Table...
print "    <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"100%\" bgcolor=\"$Map{'HTML_BODY_BGCOLOR'}\">\n";
print "      <TR>\n";
print "        <TD colspan=\"5\" align=\"center\">\n";
print "          <H3>\n";
print "             <FONT color=\"$Map{'GRAPH_COLOR_6'}\">$TotalNewMembers Joined</FONT>\n";
print "				<FONT color=\"$Map{'GRAPH_COLOR_5'}\">$TotalValidEmails Verified</FONT>\n";
print "				<FONT color=\"$Map{'GRAPH_COLOR_4'}\">$TotalAddedPhotos Added Photos</FONT>\n";
print "				<FONT color=\"$Map{'GRAPH_COLOR_3'}\">$TotalThroughAffiliate Affiliated</FONT>\n";
print "				<FONT color=\"$Map{'GRAPH_COLOR_2'}\">$TotalHavePaid Paid</FONT>\n";
print "				<FONT color=\"$Map{'GRAPH_COLOR_1'}\">$TotalPayingNow Paying</FONT>\n";
print "				- <A href=\"Admin_GraphNewMembersByMonth.cgi?goto_month=$SearchMonth&goto_year=$SearchYear\">$MonthArray[$SearchMonth]</A> $SearchDay, <A href=\"Admin_GraphNewMembersByYear.cgi?goto_year=$SearchYear\">$SearchYear</A>\n";
print "          </H3>\n";
print "        </TD>\n";
print "      </TR>\n";
print "      <TR>\n";
print "        <TD align=\"left\">\n";
print "          <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
# Title
print "            <TR>\n";
print "              <TD colspan=\"2\" align=\"left\">\n";
print "					Of Those Who <FONT color=\"$Map{'GRAPH_COLOR_6'}\">Joined</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Affiliated / Total
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_3'}\">$affiliated_over_total</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_3'}\">Joined Through Affiliate</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Verified / Total
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_5'}\">$verified_over_total</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_5'}\">Verified</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Added Photos / Total
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_4'}\">$added_photos_over_total</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_4'}\">Added Photos</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Have Paid / Total
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_2'}\">$have_paid_over_total</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		            <FONT color=\"$Map{'GRAPH_COLOR_2'}\">Have Paid</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Paying Now / Total
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_1'}\">$paying_now_over_total</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_1'}\">Are Still Paying</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Space...
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					&nbsp;\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "					&nbsp;\n";
print "              </TD>\n";
print "            </TR>\n";
# Title
print "            <TR>\n";
print "              <TD colspan=\"2\" align=\"left\">\n";
print "					Of Those Who <FONT color=\"$Map{'GRAPH_COLOR_5'}\">Verified</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Added Photos / Verified
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_4'}\">$added_photos_over_verified</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_4'}\">Added Photos</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Have Paid / Verified
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_2'}\">$have_paid_over_verified</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_2'}\">Have Paid</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
# Paying Now / Verified
print "            <TR>\n";
print "              <TD align=\"right\">\n";
print "					<FONT color=\"$Map{'GRAPH_COLOR_1'}\">$paying_now_over_verified</FONT>\n";
print "              </TD>\n";
print "              <TD align=\"left\">\n";
print "		             <FONT color=\"$Map{'GRAPH_COLOR_1'}\">Are Still Paying</FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
print "			 </TABLE>\n";
print "        </TD>\n";
print "        <TD align=\"center\">\n";
#print "            <A href=\"javascript:newWindowGeneric('../../Pictures/$FileName')\"><IMG src=\"../../Pictures/$FileName\" alt=\"$MonthArray[$SearchMonth] $SearchYear $TotalNewMembers new members graphed by day\" width=\"800\" height=\"600\"></A>\n";
print "            <IMG src=\"../../Pictures/$FileName\" alt=\"$MonthArray[$SearchMonth] $SearchDay, $SearchYear $TotalNewMembers new members graphed by hour\" width=\"800\" height=\"600\">\n";
print "        </TD>\n";
print "        <TD colspan=\"5\" align=\"left\">\n";

# Create day/amount links table...
print "          <TABLE border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";

for(my $i=0; $i<23; $i++)
	{
		print "            <TR>\n";
		print "              <TD>\n";
		if($NewMemberArray[$i] > 0)
			{
				if($i == 11)
					{
						print "              <HR>\n";
					}
				print "                $HourArray[$i]\n";
				print "              </TD>\n";
				print "              <TD align=\"left\">\n";
				if($i == 11)
					{
						print "              <HR>\n";
					}
				print "                <A href=\"\"><FONT color=\"#FF0000\">$NewMemberArray[$i]</FONT></A>\n";
			}
		else
			{
				if($i == 11)
					{
						print "              <HR>\n";
					}
				print "                $HourArray[$i]\n";
				print "              </TD>\n";
				print "              <TD align=\"left\">\n";
				if($i == 11)
					{
						print "              <HR>\n";
					}
				print "                $NewMemberArray[$i]\n";
			}
		print "              </TD>\n";
		print "            </TR>\n";
	}
print "      </TABLE>\n";

print "      <TR>\n";
print "        <TD colspan=\"5\" align=\"center\">\n";
if($SearchDay eq "1")
	{
		if($SearchMonth eq "1")
			{
				print "          <A href=\"$ProgramName?goto_day=" . $MaxDaysInEachMonthHash{$MonthArray[12]} . "&goto_month=12&goto_year=" . ($SearchYear-1) ."\">$MonthArray[12]  $MaxDaysInEachMonthHash{$MonthArray[12]}, " . ($SearchYear-1) ."</A>&nbsp;&nbsp;\n";
			}
		else
			{
				print "          <A href=\"$ProgramName?goto_day=" . $MaxDaysInEachMonthHash{$MonthArray[$SearchMonth-1]} . "&goto_month=" . ($SearchMonth-1) ."&goto_year=$SearchYear\">$MonthArray[$SearchMonth-1]  $MaxDaysInEachMonthHash{$MonthArray[$SearchMonth-1]}, $SearchYear</A>&nbsp;&nbsp;\n";
			}
			
	}
else
	{
		print "          <A href=\"$ProgramName?goto_day=" . ($SearchDay-1) . "&goto_month=$SearchMonth&goto_year=$SearchYear\">$MonthArray[$SearchMonth] " . ($SearchDay-1) . ", $SearchYear</A>&nbsp;&nbsp;\n";
	}
	
print "          $MonthArray[$SearchMonth] $SearchDay, $SearchYear&nbsp;&nbsp;\n"; 

if($SearchDay eq $DaysInMonth)
	{
		if($SearchMonth eq "12")
			{
				print "          <A href=\"$ProgramName?goto_day=1&goto_month=1&goto_year=" . ($SearchYear+1) ."\">$MonthArray[1],  1 " . ($SearchYear+1) ."</A>&nbsp;&nbsp;\n";
			}
		else
			{
				print "          <A href=\"$ProgramName?goto_day=1&goto_month=" . ($SearchMonth+1) . "&goto_year=$SearchYear\">$MonthArray[$SearchMonth+1]  1, $SearchYear</A>&nbsp;&nbsp;\n";
			}
	}
else
	{
		print "          <A href=\"$ProgramName?goto_day=" . ($SearchDay+1) . "&goto_month=$SearchMonth&goto_year=$SearchYear\">$MonthArray[$SearchMonth] " . ($SearchDay+1) . ", $SearchYear</A>&nbsp;&nbsp;\n";
	}

print "        </TD>\n";
print "      </TR>\n";
print "    </TABLE>\n";

# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom("$ProgramName", "", "", 0, 0, 0, $DebugUtilityFunctions, %Map);

#End HTML...
print "</HTML>\n";

exit 0;
