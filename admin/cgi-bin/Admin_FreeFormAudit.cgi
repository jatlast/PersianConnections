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
my $DebugCgiFunctions 	   = "0";
my $DebugDatabaseFunctions = "0";
my $DebugUtilityFunctions  = "0";

my $ProgramName 	= "Admin_FreeFormAudit.cgi";

# Set autoflush to true in order to force flushing upon each print...
#$| = 1;
#Begin HTML so errors show up in browser...
print CGI::header('text/html');
print "<HTML>\n";

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
		print "<!-- $Map{'CONFIG'} -->\n" if $DebugThisAp eq "1";
		print "<!-- $Map{'SYSTEM'} -->\n" if $DebugThisAp eq "1";
		print "<!-- $Map{'LINKMAP_FILE_SPECIFIC'} -->\n" if $DebugThisAp eq "1";
	}

my $user_name 	= "";
my $email	 	= "";
my $sql_proc 	= "";
my $find_dups 	= "";
my $order_by 	= "";
my $asc_desc 	= "";
my $limit		= "";
my $index		= "";

if(CGI::param('sql_proc')) {$sql_proc  = CGI::param('sql_proc');}
if(CGI::param('find_dups')){$find_dups = CGI::param('find_dups');}
if(CGI::param('user_name')){$user_name = CGI::param('user_name');}
if(CGI::param('email'))	   {$email	   = CGI::param('email');}
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
elsif($asc_desc =~ m%ASC%)
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
	
my $SqlStatement  = "";
# Determine if this is the first time in...
if($order_by eq "" and $sql_proc eq "")
	{
		# Since this is the first time in (all cgi fields are empty)
		# Run the stored procedures with its default peramaters...
		$SqlStatement = "admin_FreeFormAudit";
		$OrderBy  = "creation_date";
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
		$SqlStatement = "admin_FreeFormAudit '$order_by', '$asc_desc', '$limit', '$index', '$user_name', '$email'";
		$OrderBy  = $order_by;
	}

# Generate all dynamic HTML...
my $UserName      = "";
my $Password      = "";
my $Sex			  = "";
my $Email      	  = "";
my $Photo_1	      = "";
my $Photo_2    	  = "";
my $Photo_3    	  = "";
my $Photo_4    	  = "";
my $Photo_5	      = "";
my $Small_Photo_1 = "";
my $Small_Photo_2 = "";
my $Small_Photo_3 = "";
my $Small_Photo_4 = "";
my $Small_Photo_5 = "";
my $LastName      = "";
my $City	      = "";
my $ScreenQuote	  = "";
my $AboutYourself = "";
my $Questionable  = "";
my $CreationDate  = "";
my $LastLogin	  = "";

my $CityHighlight   = "";
my $ScreenQuoteHighlight   = "";
my $AboutYourselfHighlight = "";

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
#print "        <TD>\n";
#print "          <A href=\"javascript:newWindowGeneric('/admin/cgi-bin/Admin_GenSendMail.cgi')\"><STRONG>Open Admin Email</STRONG></A>\n";
#print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/email/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.email&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By email\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">email</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.email&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By email\">email</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";
if($OrderBy =~ m/user_name/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By user_name\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">user name</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.user_name&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By user_name\">user name</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/password/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.password&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By password\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">password</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.password&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By password\">password</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/photo_1/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_1&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_1\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">photo 1</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_1&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_1\">photo 1</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/photo_2/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_2&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_2\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">photo 2</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_2&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_2\">photo 2</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/photo_3/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_3&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_3\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">photo 3</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_3&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_3\">photo 3</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/photo_4/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_4&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_4\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">photo 4</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_4&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_4\">photo 4</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/photo_5/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_5&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_5\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">photo 5</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=pictures.photo_5&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By photo_5\">photo 5</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/city/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=contact_info.city&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By city\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">city</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=contact_info.city&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By city\">city</A>\n";
	}
print "        </TD>\n";
	
# screen_quote and about_yourself are stored as "TEXT" fields and therefore can not be used in an "ORDER BY" clause...
print "        <TD>\n";			
print "          screen quote\n";
print "        <HR>\n";			
print "          about yourself\n";
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/questionable/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=about_info.questionable&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By questionable\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">Q</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=about_info.questionable&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By questionable\">Q</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/creation_date/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.creation_date&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By creation_date\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">creation date</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.creation_date&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By creation_date\">creation date</A>\n";
	}
print "        </TD>\n";
	
print "        <TD>\n";			
if($OrderBy =~ m/last_login/)
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.last_login&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By last_login\"><IMG src=\"../../images/$AscDescGif\" height=\"7\" hspace=\"3\" width=\"7\" border=\"0\" alt=\"sort gif\">last login</A>\n";
	}
else
	{
		print "          <A href=\"/admin/cgi-bin/$ProgramName?user_name=$user_name&order_by=login_info.last_login&asc_desc=$AscDesc&limit=$Limit&index=$Index\" title=\"Sort $AscDescName By last_login\">last login</A>\n";
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
							
						$UserName = $$dataref{user_name};
						# Remove trailing spaces from user_name...
						($UserName, $Temp) = split(/\s\s/, $UserName);
							
						$Password = $$dataref{password};
						# Remove trailing spaces from password...
						($Password, $Temp) = split(/\s\s/, $Password);
							
						$Sex = $$dataref{sex};
						# Remove trailing spaces from password...
						($Sex, $Temp) = split(/\s\s/, $Sex);
							
						$Email = $$dataref{email};
						# Remove trailing spaces from user_name...
						($Email, $Temp) = split(/\s\s/, $Email);
							
						$Photo_1	   = $$dataref{photo_1};
						# Remove trailing spaces from photo_1...
						($Photo_1, $Temp) = split(/\s\s/, $Photo_1);
						if($Photo_1 eq "Nothing")
							{
								$Photo_1		= "../images/$Map{'NO_PIC_SMALL'}";
								$Small_Photo_1	= "../images/$Map{'NO_PIC_SMALL'}";
							}
						else
							{
								$Small_Photo_1 = "60x60_" . $Photo_1;
							}
							
						$Photo_2	   = $$dataref{photo_2};
						# Remove trailing spaces from photo_2...
						($Photo_2, $Temp) = split(/\s\s/, $Photo_2);
						if($Photo_2 eq "Nothing")
							{
								$Photo_2		= "../images/$Map{'NO_PIC_SMALL'}";
								$Small_Photo_2	= "../images/$Map{'NO_PIC_SMALL'}";
							}
						else
							{
								$Small_Photo_2 = "60x60_" . $Photo_2;
							}
							
						$Photo_3	   = $$dataref{photo_3};
						# Remove trailing spaces from photo_3...
						($Photo_3, $Temp) = split(/\s\s/, $Photo_3);
						if($Photo_3 eq "Nothing")
							{
								$Photo_3		= "../images/$Map{'NO_PIC_SMALL'}";
								$Small_Photo_3	= "../images/$Map{'NO_PIC_SMALL'}";
							}
						else
							{
								$Small_Photo_3 = "60x60_" . $Photo_3;
							}
							
						$Photo_4	   = $$dataref{photo_4};
						# Remove trailing spaces from photo_4...
						($Photo_4, $Temp) = split(/\s\s/, $Photo_4);
						if($Photo_4 eq "Nothing")
							{
								$Photo_4		= "../images/$Map{'NO_PIC_SMALL'}";
								$Small_Photo_4	= "../images/$Map{'NO_PIC_SMALL'}";
							}
						else
							{
								$Small_Photo_4 = "60x60_" . $Photo_4;
							}
							
						$Photo_5	   = $$dataref{photo_5};
						# Remove trailing spaces from photo_5...
						($Photo_5, $Temp) = split(/\s\s/, $Photo_5);
						if($Photo_5 eq "Nothing")
							{
								$Photo_5	= "../images/$Map{'NO_PIC_SMALL'}";
								$Small_Photo_5	= "../images/$Map{'NO_PIC_SMALL'}";
							}
						else
							{
								$Small_Photo_5 = "60x60_" . $Photo_5;
							}
							
						$LastName = $$dataref{last_name};
						# Remove trailing spaces from password...
						($LastName, $Temp) = split(/\s\s/, $LastName);
						#						print "<!-- LastName = ($LastName)\n";
						if($LastName eq " ")
							{
								$LastName = $UserName;
							}
							
						$City		   = $$dataref{city};
						$ScreenQuote   = $$dataref{screen_quote};
						$AboutYourself = $$dataref{about_yourself};
						$Questionable  = $$dataref{questionable};
						$CreationDate  = $$dataref{creation_date};
						$LastLogin	   = $$dataref{last_login};
						 
						$CityHighlight = $City;
						$ScreenQuoteHighlight = $ScreenQuote;
						$AboutYourselfHighlight = $AboutYourself;
							
						for(my $j=1; $j<=$Map{'NUMBER_OF_WORDS_TO_FLAG'}; $j++)
							{
								my $LM_KEY = 'WORD_TO_FLAG_' . $j;
								# Add syntax highlighting for flagged words...
								if($CityHighlight =~ m%$Map{$LM_KEY}%i)
									{
										# Add highlights for word matched...
										$CityHighlight =~ s%$&%<STRONG><FONT color=\"red\">$&</FONT></STRONG>%g;
									}
									
								if($ScreenQuoteHighlight =~ m%$Map{$LM_KEY}%i)
									{
										# Add highlights for word matched...
										$ScreenQuoteHighlight =~ s%$&%<STRONG><FONT color=\"red\">$&</FONT></STRONG>%g;
									}
									
								if($AboutYourselfHighlight =~ m%$Map{$LM_KEY}%i)
									{
										# Add highlights for word matched...
										$AboutYourselfHighlight =~ s%$&%<STRONG><FONT color=\"red\">$&</FONT></STRONG>%g;
									}
							}
							
							
						if($DebugThisAp eq "1")
							{
								print "<!--\n";
								print "user_name = ($UserName)\n";
								print "password = ($Password)\n";
								print "sex = ($Sex)\n";
								print "photo_1 = ($Photo_1)\n";
								print "photo_2 = ($Photo_2)\n";
								print "photo_3 = ($Photo_3)\n";
								print "photo_4 = ($Photo_4)\n";
								print "photo_5 = ($Photo_5)\n";
								print "last_name = ($LastName)\n";
								print "city = ($City)\n";
								print "screen_quote = ($ScreenQuote)\n";
								print "about_yourself = ($AboutYourself)\n";
								print "questionable = ($Questionable)\n";
								print "creation_date = ($CreationDate)\n";
								print "last_login = ($LastLogin)\n";
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
						print "          <A href=\"javascript:newWindowDeletePic('/admin/cgi-bin/Admin_DeleteUser.cgi?user_name=$UserName&amp;sent_from=Admin\@$Map{'WHICH_CONNECTIONS'}.com&amp;sent_to=$Email&amp;sent_bcc=&amp;subject=Urgent message from $Map{'WHICH_CONNECTIONS'}!";
						if($Sex eq "1")
							{
								print "&amp;message_text=Dear Mr. $LastName, this is a message to inform you that your account on $Map{'WHICH_CONNECTIONS'} under the user name $UserName has been deleted.')\" title=\"Send $UserName external email\">Delete User</A>\n";
							}
						else
							{
								print "&amp;message_text=Dear Ms. $LastName, this is a message to inform you that your account on $Map{'WHICH_CONNECTIONS'} under the user name $UserName has been deleted.')\" title=\"Send $UserName external email\">Delete User</A>\n";
							}
						#						print "			 <INPUT name=\"allbox\" type=\"checkbox\" value=\"Check All\" onclick=\"CheckAll();\">\n";
						print "        </TD>\n";
						print "          <!-- Send user a message in new window -->\n";
						print "        <TD valign=\"center\">\n";
						print "          <A href=\"javascript:newWindowGeneric('/admin/cgi-bin/Admin_GenSendMail.cgi?sent_from=Admin\@$Map{'WHICH_CONNECTIONS'}.com&amp;sent_to=$Email&amp;sent_bcc=&amp;subject=Urgent message from $Map{'WHICH_CONNECTIONS'}!";
						if($Sex eq "1")
							{
								print "&amp;message_text=Dear Mr. $LastName, this is a message concerning your account on $Map{'WHICH_CONNECTIONS'} under the user name $UserName.')\" title=\"Send $UserName external email\">$Email</A>\n";
							}
						else
							{
								print "&amp;message_text=Dear Ms. $LastName, this is a message concerning your account on $Map{'WHICH_CONNECTIONS'} under the user name $UserName.')\" title=\"Send $UserName external email\">$Email</A>\n";
							}
						print "        </TD>\n";
						print "          <!-- View all table info for this user in new window -->\n";						
						print "        <TD valign=\"center\">\n";
						print "          <A href=\"javascript:newWindowGeneric('Admin_GetAllTableInfo.cgi?user_name=$UserName')\" title=\"View all tables for $UserName\">$UserName</A>\n";
						print "        </TD>\n";
						print "          <!-- password and login as user in new window -->\n";
						print "        <TD valign=\"center\">\n";
						print "          <A href=\"javascript:newWindowBecomeUser('/cgi-bin/LogIn.exe?user_name=$UserName&amp;password=$Password&amp;submit=submit')\" title=\"Login as $UserName\">$Password</A>\n";
						print "        </TD>\n";
							
						print "          <!-- Delete photo_1 and href to sender's profile -->\n";
						print "        <TD>\n";
						print "          <A href=\"javascript:newWindowGeneric('/Pictures/$Photo_1')\"><IMG alt=\"View photo_1 full size\" height=\"57\" src=\"../../Pictures/$Small_Photo_1\" width=\"57\" border=\"0\"></A>\n";
						print "            <A href=\"javascript:newWindowDeletePic('/cgi-bin/UploadPicture.cgi?submit=Delete Photo&delete_picture_number=1&photo_1=$Photo_1&admin_field=baumbach&user_name=$UserName&password=$Password')\">delete</A>\n";
						print "        </TD>\n";
							
						print "          <!-- Delete photo_2 and href to sender's profile -->\n";
						print "        <TD>\n";
						print "          <A href=\"javascript:newWindowGeneric('/Pictures/$Photo_2')\"><IMG alt=\"View photo_2 full size\" height=\"57\" src=\"../../Pictures/$Small_Photo_2\" width=\"57\" border=\"0\"></A>\n";
						print "            <A href=\"javascript:newWindowDeletePic('/cgi-bin/UploadPicture.cgi?submit=Delete Photo&delete_picture_number=2&photo_2=$Photo_2&admin_field=baumbach&user_name=$UserName&password=$Password')\">delete</A>\n";
						print "        </TD>\n";
							
						print "          <!-- Delete photo_3 and href to sender's profile -->\n";
						print "        <TD>\n";
						print "          <A href=\"javascript:newWindowGeneric('/Pictures/$Photo_3')\"><IMG alt=\"View photo_3 full size\" height=\"57\" src=\"../../Pictures/$Small_Photo_3\" width=\"57\" border=\"0\"></A>\n";
						print "            <A href=\"javascript:newWindowDeletePic('/cgi-bin/UploadPicture.cgi?submit=Delete Photo&delete_picture_number=3&photo_3=$Photo_3&admin_field=baumbach&user_name=$UserName&password=$Password')\">delete</A>\n";
						print "        </TD>\n";
							
						print "          <!-- Delete photo_4 and href to sender's profile -->\n";
						print "        <TD>\n";
						print "          <A href=\"javascript:newWindowGeneric('/Pictures/$Photo_4')\"><IMG alt=\"View photo_4 full size\" height=\"57\" src=\"../../Pictures/$Small_Photo_4\" width=\"57\" border=\"0\"></A>\n";
						print "            <A href=\"javascript:newWindowDeletePic('/cgi-bin/UploadPicture.cgi?submit=Delete Photo&delete_picture_number=4&photo_4=$Photo_4&admin_field=baumbach&user_name=$UserName&password=$Password')\">delete</A>\n";
						print "        </TD>\n";
							
						print "          <!-- Delete photo_5 and href to sender's profile -->\n";
						print "        <TD>\n";
						print "          <A href=\"javascript:newWindowGeneric('/Pictures/$Photo_5')\"><IMG alt=\"View photo_5 full size\" height=\"57\" src=\"../../Pictures/$Small_Photo_5\" width=\"57\" border=\"0\"></A>\n";
						print "            <A href=\"javascript:newWindowDeletePic('/cgi-bin/UploadPicture.cgi?submit=Delete Photo&delete_picture_number=5&photo_5=$Photo_5&admin_field=baumbach&user_name=$UserName&password=$Password')\">delete</A>\n";
						print "        </TD>\n";
							
						print "        <TD align=\"left\" valign=\"bottom\">$CityHighlight\n";
						print "        </TD>\n";
							
						print "        <TD align=\"left\" valign=\"bottom\">";
						print "		   	   $ScreenQuoteHighlight\n";
						print "        	   <HR>";
						print "		   	   $AboutYourselfHighlight\n";
						print "        </TD>\n";
						print "        <TD align=\"left\" valign=\"bottom\">$Questionable\n";
						print "        </TD>\n";
						print "        <TD align=\"left\" valign=\"center\">\n";
						print "          $CreationDate\n";
						print "        </TD>\n";
						print "        <TD align=\"left\" valign=\"center\">\n";
						print "          $LastLogin\n";
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
