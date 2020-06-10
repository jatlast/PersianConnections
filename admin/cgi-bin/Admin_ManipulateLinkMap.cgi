#!/usr/local/bin/perl -w
use CGI qw/:standard/;
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
my $DebugUtilityFunctions  = "1";

my $ProgramName = "Admin_ManipulateLinkMap.cgi";

#Begin HTML so errors show up in browser...
print CGI::header('text/html');
print "<HTML>\n";

# Determine what libraries to use base on the execution dir...
my $CurrentFilePath = __FILE__;
# Initialize LinkMap Hash variable "Map"...
my %Map = &UtilityFunctions::Load_Both_LinkMaps($CurrentFilePath, $DebugUtilityFunctions); 

# Severe Error:  No LinkMap.dat file found -- EXIT --
if($Map{'CONFIG'} eq 'ERROR')
	{
		&UtilityFunctions::Print_Error("LinkMap Error.<BR><BR>Contact Site Administrator.", $DebugUtilityFunctions, %Map);
	}
else
	{
		$Map{'PROGRAM_NAME'} = $ProgramName;
		print "<!-- ADMIN_LINKMAP_FILE = $Map{'ADMIN_LINKMAP_FILE'} -->\n" if $DebugThisAp eq "1";
		print "<!-- LINKMAP_FILE = $Map{'LINKMAP_FILE'} -->\n" if $DebugThisAp eq "1";
	}

my $PercentSavings 	 = 0;
my $PastDecimal 	 = 0;
my $DoTheMath 	 	 = 0;

my $LinkMapReplaced			= 0;
my $RestoredFromBackup		= 0;

my $PreviousActionText = "";

my $Preview					= "empty";
my $Restore					= "empty";
my $Overwrite				= "empty";
my $UndoOverwrite			= "empty";

if(CGI::param('Preview'))		{$Preview		= CGI::param('Preview');}
if(CGI::param('Restore'))		{$Restore		= CGI::param('Restore');}
if(CGI::param('Overwrite'))		{$Overwrite		= CGI::param('Overwrite');}
if(CGI::param('UndoOverwrite'))	{$UndoOverwrite = CGI::param('UndoOverwrite');}

my $SYSTEM                 = "empty";
my $DBNAME                 = "empty";
my $DBUSER                 = "empty";
my $DBPWD                  = "empty";
my $ADMIN_DBUSER           = "empty";
my $ADMIN_DBPWD            = "empty";
my $ROOT                   = "empty";
my $IMAGES                 = "empty";
my $PICTURES               = "empty";
my $CGIBIN                 = "empty";
my $STYLE_SHEET            = "empty";
my $HTML_POPUP_BGCOLOR     = "empty";
my $HTML_HEADFOOT_BGCOLOR  = "empty";
my $HTML_NAV_BGCOLOR       = "empty";
my $HTML_BODY_BGCOLOR      = "empty";
my $INBOX_COLOR_1          = "empty";
my $INBOX_COLOR_2          = "empty";
my $OUTBOX_COLOR_1         = "empty";
my $OUTBOX_COLOR_2         = "empty";
my $HTML_TITLE             = "empty";
my $HTML_HEAD              = "empty";
my $COPYRIGHT_YEAR         = "empty";
my $EMAIL                  = "empty";
my $WHICH_CONNECTIONS      = "empty";
my $FIRSTARROW             = "empty";
my $NEXTARROW              = "empty";
my $PREVIOUSARROW          = "empty";
my $LASTARROW              = "empty";
my $LOGO                   = "empty";
my $FOOTER                 = "empty";
my $NO_PIC_SMALL           = "empty";
my $NO_PIC_MEDIUM          = "empty";
my $NO_PIC_LARGE           = "empty";
my $EMAILSYMBOL            = "empty";
my $DELETSYMBOL            = "empty";
my $BOOKMARKSYMBOL         = "empty";
my $UNREADSYMBOL           = "empty";
my $LINESYMBOL             = "empty";
my $SPACESYMBOL            = "empty";
my $PROCESSINGSYMBOL       = "empty";
my $BECOME_PREMIUM_MEMBER  = "empty";
my $BECOME_MEMBER_GIF      = "empty";
my $SMTP_HOST              = "empty";
my $BLAT_PATH              = "empty";
my $AUTHORIZE_TEST_MODE    = "empty";
my $PRICE_ONE              = "empty";
my $PRICE_THREE            = "empty";
my $PRICE_TWELVE           = "empty";
my $PRICE_LIFETIME         = "empty";
my $LOG_FOLDER             = "empty";
my $PICTURES_FOLDER        = "empty";
my $DOS_PICTURES_FOLDER    = "empty";
my $ADV_CGIBIN			   = "empty";
my $ADV_RETRIEVE		   = "empty";
my $ADV_HOST_UNIQUE_ID     = "empty";

if($Preview eq "Preview" || $Overwrite eq "Overwrite")
{
if(CGI::param('SYSTEM'))					{$SYSTEM                		= CGI::param('SYSTEM');}
if(CGI::param('DBNAME'))					{$DBNAME                		= CGI::param('DBNAME');}
if(CGI::param('DBUSER'))					{$DBUSER                		= CGI::param('DBUSER');}
if(CGI::param('DBPWD'))						{$DBPWD                 		= CGI::param('DBPWD');}
if(CGI::param('ADMIN_DBUSER'))				{$ADMIN_DBUSER             		= CGI::param('ADMIN_DBUSER');}
if(CGI::param('ADMIN_DBPWD'))				{$ADMIN_DBPWD             		= CGI::param('ADMIN_DBPWD');}
if(CGI::param('ROOT'))						{$ROOT                  		= CGI::param('ROOT');}
if(CGI::param('IMAGES'))					{$IMAGES                		= CGI::param('IMAGES');}
if(CGI::param('PICTURES'))					{$PICTURES              		= CGI::param('PICTURES');}
if(CGI::param('CGIBIN'))					{$CGIBIN                		= CGI::param('CGIBIN');}
if(CGI::param('STYLE_SHEET'))				{$STYLE_SHEET              		= CGI::param('STYLE_SHEET');}
if(CGI::param('HTML_POPUP_BGCOLOR'))		{$HTML_POPUP_BGCOLOR    		= CGI::param('HTML_POPUP_BGCOLOR');}
if(CGI::param('HTML_HEADFOOT_BGCOLOR'))		{$HTML_HEADFOOT_BGCOLOR 		= CGI::param('HTML_HEADFOOT_BGCOLOR');}
if(CGI::param('HTML_NAV_BGCOLOR'))			{$HTML_NAV_BGCOLOR      		= CGI::param('HTML_NAV_BGCOLOR');}
if(CGI::param('HTML_BODY_BGCOLOR'))			{$HTML_BODY_BGCOLOR     		= CGI::param('HTML_BODY_BGCOLOR');}
if(CGI::param('INBOX_COLOR_1'))				{$INBOX_COLOR_1         		= CGI::param('INBOX_COLOR_1');}
if(CGI::param('INBOX_COLOR_2'))				{$INBOX_COLOR_2         		= CGI::param('INBOX_COLOR_2');}
if(CGI::param('OUTBOX_COLOR_1'))			{$OUTBOX_COLOR_1        		= CGI::param('OUTBOX_COLOR_1');}
if(CGI::param('OUTBOX_COLOR_2'))			{$OUTBOX_COLOR_2        		= CGI::param('OUTBOX_COLOR_2');}
if(CGI::param('HTML_TITLE'))				{$HTML_TITLE            		= CGI::param('HTML_TITLE');}
if(CGI::param('HTML_HEAD'))					{$HTML_HEAD             		= CGI::param('HTML_HEAD');}
if(CGI::param('COPYRIGHT_YEAR'))			{$COPYRIGHT_YEAR        		= CGI::param('COPYRIGHT_YEAR');}
if(CGI::param('EMAIL'))						{$EMAIL                 		= CGI::param('EMAIL');}
if(CGI::param('WHICH_CONNECTIONS'))			{$WHICH_CONNECTIONS     		= CGI::param('WHICH_CONNECTIONS');}
if(CGI::param('FIRSTARROW'))				{$FIRSTARROW            		= CGI::param('FIRSTARROW');}
if(CGI::param('NEXTARROW'))					{$NEXTARROW             		= CGI::param('NEXTARROW');}
if(CGI::param('PREVIOUSARROW'))				{$PREVIOUSARROW         		= CGI::param('PREVIOUSARROW');}
if(CGI::param('LASTARROW'))					{$LASTARROW             		= CGI::param('LASTARROW');}
if(CGI::param('LOGO'))						{$LOGO                  		= CGI::param('LOGO');}
if(CGI::param('FOOTER'))					{$FOOTER                  		= CGI::param('FOOTER');}
if(CGI::param('NO_PIC_SMALL'))				{$NO_PIC_SMALL          		= CGI::param('NO_PIC_SMALL');}
if(CGI::param('NO_PIC_MEDIUM'))				{$NO_PIC_MEDIUM         		= CGI::param('NO_PIC_MEDIUM');}
if(CGI::param('NO_PIC_LARGE'))				{$NO_PIC_LARGE          		= CGI::param('NO_PIC_LARGE');}
if(CGI::param('EMAILSYMBOL'))				{$EMAILSYMBOL           		= CGI::param('EMAILSYMBOL');}
if(CGI::param('DELETSYMBOL'))				{$DELETSYMBOL           		= CGI::param('DELETSYMBOL');}
if(CGI::param('BOOKMARKSYMBOL'))			{$BOOKMARKSYMBOL        		= CGI::param('BOOKMARKSYMBOL');}
if(CGI::param('UNREADSYMBOL'))				{$UNREADSYMBOL          		= CGI::param('UNREADSYMBOL');}
if(CGI::param('LINESYMBOL'))				{$LINESYMBOL            		= CGI::param('LINESYMBOL');}
if(CGI::param('SPACESYMBOL'))				{$SPACESYMBOL           		= CGI::param('SPACESYMBOL');}
if(CGI::param('PROCESSINGSYMBOL'))			{$PROCESSINGSYMBOL      		= CGI::param('PROCESSINGSYMBOL');}
if(CGI::param('BECOME_PREMIUM_MEMBER'))		{$BECOME_PREMIUM_MEMBER 		= CGI::param('BECOME_PREMIUM_MEMBER');}
if(CGI::param('BECOME_MEMBER_GIF'))			{$BECOME_MEMBER_GIF     		= CGI::param('BECOME_MEMBER_GIF');}
if(CGI::param('SMTP_HOST'))					{$SMTP_HOST             		= CGI::param('SMTP_HOST');}
if(CGI::param('BLAT_PATH'))					{$BLAT_PATH             		= CGI::param('BLAT_PATH');}
if(CGI::param('AUTHORIZE_TEST_MODE'))		{$AUTHORIZE_TEST_MODE   		= CGI::param('AUTHORIZE_TEST_MODE');}
if(CGI::param('PRICE_ONE'))					{$PRICE_ONE             		= CGI::param('PRICE_ONE');}
if(CGI::param('PRICE_THREE'))				{$PRICE_THREE           		= CGI::param('PRICE_THREE');}
if(CGI::param('PRICE_TWELVE'))				{$PRICE_TWELVE          		= CGI::param('PRICE_TWELVE');}
if(CGI::param('PRICE_LIFETIME'))			{$PRICE_LIFETIME        		= CGI::param('PRICE_LIFETIME');}
if(CGI::param('LOG_FOLDER'))				{$LOG_FOLDER            		= CGI::param('LOG_FOLDER');}
if(CGI::param('PICTURES_FOLDER'))			{$PICTURES_FOLDER       		= CGI::param('PICTURES_FOLDER');}
if(CGI::param('DOS_PICTURES_FOLDER'))		{$DOS_PICTURES_FOLDER   		= CGI::param('DOS_PICTURES_FOLDER');}
if(CGI::param('ADV_CGIBIN'))				{$ADV_CGIBIN			   		= CGI::param('ADV_CGIBIN');}
if(CGI::param('ADV_RETRIEVE'))				{$ADV_RETRIEVE			   		= CGI::param('ADV_RETRIEVE');}
if(CGI::param('ADV_HOST_UNIQUE_ID'))		{$ADV_HOST_UNIQUE_ID	   		= CGI::param('ADV_HOST_UNIQUE_ID');}

# Copy web variable values into the Map hash to prepare them to store to the LinkMap.dat file...
$Map{'SYSTEM'}					= $SYSTEM;               
$Map{'DBNAME'}					= $DBNAME;               
$Map{'DBUSER'}					= $DBUSER;               
$Map{'DBPWD'}					= $DBPWD;                
$Map{'ADMIN_DBUSER'}			= $ADMIN_DBUSER;               
$Map{'ADMIN_DBPWD'}				= $ADMIN_DBPWD;                
$Map{'ROOT'}					= $ROOT;                 
$Map{'IMAGES'}					= $IMAGES;               
$Map{'PICTURES'}				= $PICTURES;
$Map{'CGIBIN'}					= $CGIBIN;               
$Map{'STYLE_SHEET'}				= $STYLE_SHEET;               
$Map{'HTML_POPUP_BGCOLOR'}		= $HTML_POPUP_BGCOLOR;
$Map{'HTML_HEADFOOT_BGCOLOR'}	= $HTML_HEADFOOT_BGCOLOR;
$Map{'HTML_NAV_BGCOLOR'}		= $HTML_NAV_BGCOLOR;
$Map{'HTML_BODY_BGCOLOR'}		= $HTML_BODY_BGCOLOR;
$Map{'INBOX_COLOR_1'}			= $INBOX_COLOR_1;
$Map{'INBOX_COLOR_2'}			= $INBOX_COLOR_2;
$Map{'OUTBOX_COLOR_1'}			= $OUTBOX_COLOR_1;
$Map{'OUTBOX_COLOR_2'}			= $OUTBOX_COLOR_2;
$Map{'HTML_TITLE'}				= $HTML_TITLE;
$Map{'HTML_HEAD'}				= $HTML_HEAD;
$Map{'COPYRIGHT_YEAR'}			= $COPYRIGHT_YEAR;
$Map{'EMAIL'}					= $EMAIL;
$Map{'WHICH_CONNECTIONS'}		= $WHICH_CONNECTIONS;
$Map{'FIRSTARROW'}				= $FIRSTARROW;
$Map{'NEXTARROW'}				= $NEXTARROW;
$Map{'PREVIOUSARROW'}			= $PREVIOUSARROW;
$Map{'LASTARROW'}				= $LASTARROW;
$Map{'LOGO'}					= $LOGO;
$Map{'FOOTER'}					= $FOOTER;
$Map{'NO_PIC_SMALL'}			= $NO_PIC_SMALL;
$Map{'NO_PIC_MEDIUM'}			= $NO_PIC_MEDIUM;
$Map{'NO_PIC_LARGE'}			= $NO_PIC_LARGE;
$Map{'EMAILSYMBOL'}				= $EMAILSYMBOL;
$Map{'DELETSYMBOL'}				= $DELETSYMBOL;
$Map{'BOOKMARKSYMBOL'}			= $BOOKMARKSYMBOL;
$Map{'UNREADSYMBOL'}			= $UNREADSYMBOL;
$Map{'LINESYMBOL'}				= $LINESYMBOL;
$Map{'SPACESYMBOL'}				= $SPACESYMBOL;
$Map{'PROCESSINGSYMBOL'}		= $PROCESSINGSYMBOL;
$Map{'BECOME_PREMIUM_MEMBER'}	= $BECOME_PREMIUM_MEMBER;
$Map{'BECOME_MEMBER_GIF'}		= $BECOME_MEMBER_GIF;
$Map{'SMTP_HOST'}				= $SMTP_HOST;
$Map{'BLAT_PATH'}				= $BLAT_PATH;
$Map{'AUTHORIZE_TEST_MODE'}		= $AUTHORIZE_TEST_MODE;
$Map{'PRICE_ONE'}				= $PRICE_ONE;
$Map{'PRICE_THREE'}				= $PRICE_THREE;
$Map{'PRICE_TWELVE'}			= $PRICE_TWELVE;
$Map{'PRICE_LIFETIME'}			= $PRICE_LIFETIME;
$Map{'LOG_FOLDER'}				= $LOG_FOLDER;
$Map{'PICTURES_FOLDER'}			= $PICTURES_FOLDER;
$Map{'DOS_PICTURES_FOLDER'}		= $DOS_PICTURES_FOLDER;
$Map{'ADV_CGIBIN'}				= $ADV_CGIBIN;
$Map{'ADV_RETRIEVE'}			= $ADV_RETRIEVE;
$Map{'ADV_HOST_UNIQUE_ID'}		= $ADV_HOST_UNIQUE_ID;
}

if ($Preview eq "Preview") 
{
	$PreviousActionText = "Preview";

}
elsif ($Overwrite eq "Overwrite")
{
	$PreviousActionText = "Overwrite";
	# Create a Backup copy of the LinkMap.dat file as LinkMap.bak before overwriting it...
	my $return_value = &UtilityFunctions::BackUp_LinkMaps($DebugUtilityFunctions, %Map);
	if($return_value == 1)
		{
			print "<!-- SUCCESS: $Map{'ADMIN_LINKMAP_FILE'} file backed up successfully to $Map{'CONFIG'}/LinkMap.bak. -->\n";
			print "<!-- SUCCESS: $Map{'LINKMAP_FILE'} file backed up successfully to $Map{'CONFIG'}/LinkMap.bak. -->\n";
			# Overwrite current LinkMap.dat using current web page variables...
			my $return_value = &UtilityFunctions::Overwrite_Both_LinkMaps($DebugUtilityFunctions, %Map);
			if($return_value == 1)
				{
					print "<!-- SUCCESS: $Map{'ADMIN_LINKMAP_FILE'} file overwritten successfully. -->\n";
					print "<!-- SUCCESS: $Map{'LINKMAP_FILE'} file overwritten successfully. -->\n";
					$LinkMapReplaced = 1;

					# Reload the freshly written LinkMap.dat hash variables into %Map...
					# Initialize LinkMap Hash variable "Map"...
					my %Map = &UtilityFunctions::Load_Both_LinkMaps($Map{'ADMIN_LINKMAP_FILE'}, $DebugUtilityFunctions); 

					# Severe Error:  No LinkMap.dat file found -- EXIT --
					if($Map{'CONFIG'} eq 'ERROR')
						{
							&UtilityFunctions::Print_Error("LinkMap Error.<BR><BR>Contact Site Administrator.", $DebugUtilityFunctions, %Map);
						}
					else
						{
							print "<!-- ADMIN_LINKMAP_FILE = $Map{'ADMIN_LINKMAP_FILE'} -->\n" if $DebugThisAp eq "1";
							print "<!-- LINKMAP_FILE = $Map{'LINKMAP_FILE'} -->\n" if $DebugThisAp eq "1";
						}
				}
			else
				{
					print "<FONT color=\"red\">ERROR</FONT>: ($return_value) Unable to overwrite $Map{'LINKMAP_FILE'} file.<BR>\n";
				}
		}
	else
		{
			print "<FONT color=\"red\">ERROR</FONT>: ($return_value) Unable to back up $Map{'ADMIN_LINKMAP_FILE'} file.<BR>\n";
			print "<FONT color=\"red\">ERROR</FONT>: ($return_value) Unable to back up $Map{'LINKMAP_FILE'} file.<BR>\n";
		}
}
# Removed because of IIS authentification problems !!!!!!!1
#elsif ($UndoOverwrite eq "UndoOverwrite")
elsif (0)
{
	$PreviousActionText = "Overwrite Undone";
	# Overwrite current LinkMap.dat file using LinkMap.bak file...
	my $return_value = &UtilityFunctions::Restore_LinkMaps_From_Backups($DebugUtilityFunctions, %Map);
	if($return_value == 1)
		{
			print "<!-- SUCCESS: Restored $Map{'CONFIG'}\LinkMap.dat from $Map{'CONFIG'}\LinkMap.bak. -->\n";
			$RestoredFromBackup = 1;

			# Reload the freshly written LinkMap.dat hash variables into %Map...
			# Determine what LinkMap.dat file to open...
			my $CurrentFilePath = $Map{'LINKMAP_FILE'};
			# Initialize LinkMap Hash variable "Map"...
			my $Map;
			my %Map = &UtilityFunctions::Load_Both_LinkMaps($CurrentFilePath, $DebugUtilityFunctions); 

			# Severe Error:  No LinkMap.dat file found -- EXIT --
			if($Map{'CONFIG'} eq 'ERROR')
				{
					&UtilityFunctions::Print_Error("LinkMap Error.<BR><BR>Contact Site Administrator.", $DebugUtilityFunctions, %Map);
				}
			else
				{
					print "<!-- $Map{'LINKMAP_FILE'} has been reloaded successfully -->\n";
				}
		}
	else
		{
			print "<FONT color=\"red\">ERROR</FONT>: ($return_value) Unable to restore $Map{'LINKMAP_FILE'} file from $Map{'CONFIG'}\LinkMap.bak.<BR>\n";
		}
}
elsif ($Restore eq "Restore")
{
	$PreviousActionText = "Restore";
}
else
{
	$PreviousActionText = "First time in";
}



&Print_Current_LinkMap_HTML($DebugThisAp, %Map);

print "</HTML>\n";
 

sub Print_Current_LinkMap_HTML
	{
		(my $Debug, my %Map) = @_;

&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);

		print "<html>\n";
		print "<head>\n";
		print "<FORM name=\"theForm\" onSubmit=\"return checkForm(this)\" method=\"POST\" action=\"$Map{'ROOT'}/admin/cgi-bin/Admin_ManipulateLinkMap.cgi\">\n";
		print "<title>$Map{'HTML_TITLE'}</title>\n";
		print "</head>\n";
		print "<body>\n";
		print "<table border=\"0\" cellpadding=\"4\" cellspacing=\"4\" width=\"800\">\n";
		print "<tr align=\"left\">\n";
		print "<td colspan=\"2\" bgcolor=$Map{'HTML_HEADFOOT_BGCOLOR'} height=\"38\" valign=\"middle\">\n";
# LOGO
		print "<INPUT type=\"checkbox\" title=\"Change LOGO...?\" onClick=\"changeLOGO(theForm)\">\n";
		print "<img alt=\"LOGO\" src=\"$Map{'IMAGES'}/$Map{'LOGO'}\" border=\"0\" width=\"500\" height=\"40\"></td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr>\n";
# HTML_NAV_BGCOLOR
		print "<td nowrap bgcolor=$Map{'HTML_NAV_BGCOLOR'} valign=\"top\" width=\"150\" height=\"394\">\n";
		print "<INPUT type=\"checkbox\" title=\"Change HTML_NAV_BGCOLOR...?\" onClick=\"changeHTML_NAV_BGCOLOR(theForm)\">\n";
		print "<FONT size=\"-1\">(<FONT color=\"red\">$Map{'HTML_NAV_BGCOLOR'}</FONT>)</FONT>\n";
		print "<table border=\"0\" cellpadding=\"3\" cellspacing=\"3\" width=\"150\">\n";
		print "<tr>\n";
		print "<td>&nbsp;</td>\n";
		print "</tr>\n";
		print "\n";
# ROOT
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change ROOT...?\" onClick=\"changeROOT(theForm)\">\n";
		print "<a title=\"ROOT\" href=\"$Map{'ROOT'}\">$Map{'ROOT'}</a>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# IMAGES
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change IMAGES...?\" onClick=\"changeIMAGES(theForm)\">\n";
		print "<a title=\"IMAGES\" href=\"$Map{'IMAGES'}\">$Map{'IMAGES'}</a>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# PICTURES
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change PICTURES...?\" onClick=\"changePICTURES(theForm)\">\n";
		print "<a title=\"PICTURES\" href=\"$Map{'PICTURES'}\">$Map{'PICTURES'}</a>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# CGIBIN
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change CGIBIN...?\" onClick=\"changeCGIBIN(theForm)\">\n";
		print "<a title=\"CGIBIN\" href=\"$Map{'CGIBIN'}\">$Map{'CGIBIN'}</a>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# STYLE_SHEET
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change STYLE_SHEET...?\" onClick=\"changeSTYLE_SHEET(theForm)\">\n";
		print "<FONT size=\"-3\">STYLE_SHEET = (<FONT color=\"red\">$Map{'STYLE_SHEET'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# EMAIL
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change EMAIL...?\" onClick=\"changeEMAIL(theForm)\">\n";
		print "<a title=\"EMAIL\" href=\"$Map{'EMAIL'}\">$Map{'EMAIL'}</a>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# HTML_TITLE
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change HTML_TITLE...?\" onClick=\"changeHTML_TITLE(theForm)\">\n";
		print "<FONT size=\"-3\">HTML_TITLE = (<FONT color=\"red\">$Map{'HTML_TITLE'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# HTML_HEAD
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change HTML_HEAD...?\" onClick=\"changeHTML_HEAD(theForm)\">\n";
		print "<FONT size=\"-3\">HTML_HEAD = (<FONT color=\"red\">$Map{'HTML_HEAD'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# DBNAME
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change DBNAME...?\" onClick=\"changeDBNAME(theForm)\">\n";
		print "<FONT size=\"-3\">DBNAME = (<FONT color=\"red\">$Map{'DBNAME'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# DBUSER
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change DBUSER...?\" onClick=\"changeDBUSER(theForm)\">\n";
		print "<FONT size=\"-3\">DBUSER = (<FONT color=\"red\">$Map{'DBUSER'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# DBPWD
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change DBPWD...?\" onClick=\"changeDBPWD(theForm)\">\n";
		print "<FONT size=\"-3\">DBPWD = (<FONT color=\"red\">$Map{'DBPWD'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# ADMIN_DBUSER
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change Admin DBUSER...?\" onClick=\"changeADMIN_DBUSER(theForm)\">\n";
		print "<FONT size=\"-3\">Admin DBUSER = (<FONT color=\"red\">$Map{'ADMIN_DBUSER'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# ADMIN_DBPWD
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change Admin DBPWD...?\" onClick=\"changeADMIN_DBPWD(theForm)\">\n";
		print "<FONT size=\"-3\">Admin DBPWD = (<FONT color=\"red\">$Map{'ADMIN_DBPWD'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# SMTP_HOST
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change SMTP_HOST...?\" onClick=\"changeSMTP_HOST(theForm)\">\n";
		print "<FONT size=\"-3\">SMTP_HOST = (<FONT color=\"red\">$Map{'SMTP_HOST'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# BLAT_PATH
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change BLAT_PATH...?\" onClick=\"changeBLAT_PATH(theForm)\">\n";
		print "<FONT size=\"-3\">BLAT_PATH = (<FONT color=\"red\">$Map{'BLAT_PATH'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# AUTHORIZE_TEST_MODE
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change AUTHORIZE_TEST_MODE...?\" onClick=\"changeAUTHORIZE_TEST_MODE(theForm)\">\n";
		print "<FONT size=\"-3\">AUTHORIZE_TEST_MODE = (<FONT color=\"red\">$Map{'AUTHORIZE_TEST_MODE'}</FONT>) <FONT color=\"blue\">1</FONT>=Test / <FONT color=\"blue\">00</FONT>=Live</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# PRICE_ONE
		print "<tr>\n";
		print "<TD nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change PRICE_ONE...?\" onClick=\"changePRICE_ONE(theForm)\">\n";
		print "<FONT size=\"-3\">PRICE_ONE = (<FONT color=\"red\">$Map{'PRICE_ONE'}</FONT>)</FONT>\n";
		print "</TD>\n";
		print "<TD height=\"30\" width=\"215\">\n";
		print "</TD>\n";
		print "</TR>\n";
		# Calculate the potential amount of savings...
		$DoTheMath = $Map{'PRICE_THREE'};
		$DoTheMath /= ( $Map{'PRICE_ONE'} * 3 );
		$DoTheMath -= 1;
		$DoTheMath *= (-100);
		# Split the number in two at the decimal...
		($PercentSavings, $PastDecimal) = split(/\./, $DoTheMath);
		# Check if rounding is needed...
		if(substr($PastDecimal, 1, 1) > 5)
		{
		 $PercentSavings++;
		}
# PRICE_THREE
		print "<TR>\n";
		print "<TD nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change PRICE_THREE...?\" onClick=\"changePRICE_THREE(theForm)\">\n";
		print "<FONT size=\"-3\">PRICE_THREE = (<FONT color=\"red\">$Map{'PRICE_THREE'}</FONT>) save <FONT color=\"blue\">" . $PercentSavings . "</FONT>%</FONT>\n";
		print "</TD>\n";
		print "</TR>\n";
		# Calculate the potential amount of savings...
		$DoTheMath = $Map{'PRICE_TWELVE'};
		$DoTheMath /= ( $Map{'PRICE_ONE'} * 12 );
		$DoTheMath -= 1;
		$DoTheMath *= (-100);
		# Split the number in two at the decimal...
		($PercentSavings, $PastDecimal) = split(/\./, $DoTheMath);
		# Check if rounding is needed...
		if(substr($PastDecimal, 1, 1) > 5)
		{
		 $PercentSavings++;
		}
# PRICE_TWELVE
		print "<TR>\n";
		print "<TD nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change PRICE_TWELVE...?\" onClick=\"changePRICE_TWELVE(theForm)\">\n";
		print "<FONT size=\"-3\">PRICE_TWELVE = (<FONT color=\"red\">$Map{'PRICE_TWELVE'}</FONT>) save <FONT color=\"blue\">" . $PercentSavings . "</FONT>%</FONT>\n";
		print "</TD>\n";
		print "</TR>\n";
		# Calculate the potential amount of savings...
		$DoTheMath = $Map{'PRICE_LIFETIME'};
		$DoTheMath /= ( $Map{'PRICE_ONE'} * 240 );
		$DoTheMath -= 1;
		$DoTheMath *= (-100);
		# Split the number in two at the decimal...
		($PercentSavings, $PastDecimal) = split(/\./, $DoTheMath);
		# Check if rounding is needed...
		if(substr($PastDecimal, 1, 1) > 5)
		{
		 $PercentSavings++;
		}
# PRICE_LIFETIME
		print "<TR>\n";
		print "<TD nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change PRICE_LIFETIME...?\" onClick=\"changePRICE_LIFETIME(theForm)\">\n";
		print "<FONT size=\"-3\">PRICE_LIFETIME = (<FONT color=\"red\">$Map{'PRICE_LIFETIME'}</FONT>) save <FONT color=\"blue\">" . $PercentSavings . "</FONT>%</FONT>\n";
		print "</TD>\n";
		print "</tr>\n";
# LOG_FOLDER
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change LOG_FOLDER...?\" onClick=\"changeLOG_FOLDER(theForm)\">\n";
		print "<FONT size=\"-3\">LOG_FOLDER<BR>(<FONT color=\"red\">$Map{'LOG_FOLDER'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# PICTURES_FOLDER
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change PICTURES_FOLDER...?\" onClick=\"changePICTURES_FOLDER(theForm)\">\n";
		print "<FONT size=\"-3\">PICTURES_FOLDER<BR>(<FONT color=\"red\">$Map{'PICTURES_FOLDER'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# DOS_PICTURES_FOLDER
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change DOS_PICTURES_FOLDER...?\" onClick=\"changeDOS_PICTURES_FOLDER(theForm)\">\n";
		print "<FONT size=\"-3\">DOS_PICTURES_FOLDER<BR>(<FONT color=\"red\">$Map{'DOS_PICTURES_FOLDER'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";

# ADV_CGIBIN
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change ADV_CGIBIN...?\" onClick=\"changeADV_CGIBIN(theForm)\">\n";
		print "<FONT size=\"-3\">ADV_CGIBIN = (<FONT color=\"red\">$Map{'ADV_CGIBIN'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# ADV_RETRIEVE
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change ADV_RETRIEVE...?\" onClick=\"changeADV_RETRIEVE(theForm)\">\n";
		print "<FONT size=\"-3\">ADV_RETRIEVE = (<FONT color=\"red\">$Map{'ADV_RETRIEVE'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# ADV_HOST_UNIQUE_ID
		print "<tr>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change ADV_HOST_UNIQUE_ID...?\" onClick=\"changeADV_HOST_UNIQUE_ID(theForm)\">\n";
		print "<FONT size=\"-3\">ADV_HOST_UNIQUE_ID = (<FONT color=\"red\">$Map{'ADV_HOST_UNIQUE_ID'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";

# HTML_POPUP_BGCOLOR
		print "<tr bgcolor=$Map{'HTML_POPUP_BGCOLOR'}>\n";
		print "<td nowrap>\n";
		print "<INPUT type=\"checkbox\" title=\"Change HTML_POPUP_BGCOLOR...?\" onClick=\"changeHTML_POPUP_BGCOLOR(theForm)\">\n";
		print "<FONT size=\"-3\">HTML_POPUP_BGCOLOR = (<FONT color=\"red\">$Map{'HTML_POPUP_BGCOLOR'}</FONT>)</FONT>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
		print "</table>\n";
		print "</td>\n";
# HTML_BODY_BGCOLOR
		print "<td bgcolor=$Map{'HTML_BODY_BGCOLOR'} valign=\"top\">\n";
		print "<HR>$PreviousActionText<HR>\n";
		print "<INPUT type=\"checkbox\" title=\"Change HTML_BODY_BGCOLOR...?\" onClick=\"changeHTML_BODY_BGCOLOR(theForm)\">\n";
		print "<FONT size=\"-1\">(<FONT color=\"red\">$Map{'HTML_BODY_BGCOLOR'}</FONT>)</FONT></FONT>\n";
		print "<table border=\"0\" width=\"100%\" cellspacing=\"3\" cellpadding=\"3\">\n";
		print "<BR>\n";
		print "<tr>\n";
		print "<td valign=\"top\" align=\"left\">\n";
# NO_PIC_LARGE
		print "<INPUT type=\"checkbox\" title=\"Change NO_PIC_LARGE...?\" onClick=\"changeNO_PIC_LARGE(theForm)\">\n";
		print "<img alt=\"NO_PIC_LARGE\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'NO_PIC_LARGE'}\" width=\"175\" height=\"183\"></td>\n";
# BECOME_MEMBER_GIF
		print "<td align=\"left\">\n";
		print "<INPUT type=\"checkbox\" title=\"Change BECOME_MEMBER_GIF...?\" onClick=\"changeBECOME_MEMBER_GIF(theForm)\">\n";
		print "<img alt=\"BECOME_MEMBER_GIF\" src=\"$Map{'IMAGES'}/$Map{'BECOME_MEMBER_GIF'}\" width=\"100\" height=\"50\" border=\"0\">\n";
# EMAILSYMBOL
		print "<INPUT type=\"checkbox\" title=\"Change EMAILSYMBOL...?\" onClick=\"changeEMAILSYMBOL(theForm)\">\n";
		print "<img alt=\"EMAILSYMBOL\" align=\"right\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'EMAILSYMBOL'}\">\n";
		print "</td>\n";
# BECOME_PREMIUM_MEMBER
		print "<td height=\"40\" colspan=\"2\" align=\"left\" valign=\"middle\">\n";
		print "<INPUT type=\"checkbox\" title=\"Change BECOME_PREMIUM_MEMBER...?\" onClick=\"changeBECOME_PREMIUM_MEMBER(theForm)\">\n";
		print "<img alt=\"BECOME_PREMIUM_MEMBER\" src=\"$Map{'IMAGES'}/$Map{'BECOME_PREMIUM_MEMBER'}\" width=\"275\" height=\"20\" border=\"0\">\n";
# BOOKMARKSYMBOL
		print "<INPUT type=\"checkbox\" title=\"Change BOOKMARKSYMBOL...?\" onClick=\"changeBOOKMARKSYMBOL(theForm)\">\n";
		print "<img alt=\"BOOKMARKSYMBOL\" align=\"right\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'BOOKMARKSYMBOL'}\">\n";
		print "</td>\n";
		print "</tr>\n";
		print "</table>\n";
		print "\n";
		print "<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"3\">\n";
# INBOX_COLOR_1
		print "<tr bgcolor=$Map{'INBOX_COLOR_1'}>\n";
		print "<td width=\"25\"><INPUT type=\"checkbox\" title=\"Change INBOX_COLOR_1...?\" onClick=\"changeINBOX_COLOR_1(theForm)\"></td>\n";
		print "<td width=\"197\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#990033\" size=\"4\"><strong>Inbox</strong></font></td>\n";
		print "<td width=\"125\">&nbsp;</td>\n";
		print "<td width=\"132\">&nbsp;</td>\n";
		print "<td width=\"60\">&nbsp;</td>\n";
		print "<td width=\"48\">&nbsp;</td>\n";
		print "</tr>\n";
		print "\n";
# INBOX_COLOR_2
		print "<tr bgcolor=$Map{'INBOX_COLOR_2'}>\n";
		print "<td width=\"25\"><INPUT type=\"checkbox\" title=\"Change INBOX_COLOR_2...?\" onClick=\"changeINBOX_COLOR_2(theForm)\"></td>\n";
		print "<td width=\"197\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#000066\" size=\"2\"><strong><font color=\"#663399\">Messages</font></strong></font> </td>\n";
		print "<td width=\"125\">&nbsp;</td>\n";
		print "<td width=\"132\">&nbsp;</td>\n";
		print "<td width=\"60\">&nbsp;</td>\n";
		print "<td width=\"48\">&nbsp;</td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr bgcolor=$Map{'INBOX_COLOR_1'}>\n";
		print "<td width=\"25\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>New</strong></font> </td>\n";
		print "<td width=\"197\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>From</strong></font> </td>\n";
		print "<td width=\"125\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Subject</strong></font> </td>\n";
		print "<td width=\"132\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Received</strong></font> </td>\n";
		print "<td width=\"60\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Profile</strong></font> </td>\n";
		print "<td width=\"48\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Delete</strong></font> </td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr bgcolor=$Map{'INBOX_COLOR_2'}>\n";
		print "<td width=\"25\">\n";
# UNREADSYMBOL
		print "<INPUT type=\"checkbox\" title=\"Change UNREADSYMBOL...?\" onClick=\"changeUNREADSYMBOL(theForm)\">\n";
		print "<img alt=\"UNREADSYMBOL\" src=\"$Map{'IMAGES'}/$Map{'UNREADSYMBOL'}\" width=\"10\" height=\"8\">\n";
		print "</td>\n";
		print "<td width=\"197\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>UserName</strong></font> </td>\n";
		print "<td width=\"125\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong><font color=\"#000000\">RE: Subject</font></strong></font></td>\n";
		print "<td width=\"132\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>Dec 16 2001 5:31PM</strong></font> </td>\n";
# NO_PIC_SMALL
		print "<td width=\"60\">\n";
		print "<INPUT type=\"checkbox\" title=\"Change NO_PIC_SMALL...?\" onClick=\"changeNO_PIC_SMALL(theForm)\">\n";
		print "<img alt=\"NO_PIC_SMALL\" height=\"57\" src=\"$Map{'IMAGES'}/$Map{'NO_PIC_SMALL'}\" width=\"57\" border=\"0\">\n";
		print "</td>\n";
# DELETSYMBOL
		print "<td width=\"48\">\n";
		print "<div align=\"center\">\n";
		print "<INPUT type=\"checkbox\" title=\"Change DELETSYMBOL...?\" onClick=\"changeDELETSYMBOL(theForm)\">\n";
		print "<img alt=\"DELETSYMBOL\" src=\"$Map{'IMAGES'}/$Map{'DELETSYMBOL'}\" border=\"0\">\n";
		print "</div>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr bgcolor=$Map{'INBOX_COLOR_1'}>\n";
		print "<td width=\"25\">\n";
# SPACESYMBOL
		print "<INPUT type=\"checkbox\" title=\"Change SPACESYMBOL...?\" onClick=\"changeSPACESYMBOL(theForm)\">\n";
		print "<img alt=\"SPACESYMBOL\" src=\"$Map{'IMAGES'}/$Map{'SPACESYMBOL'}\" width=\"10\" height=\"8\">\n";
		print "</td>\n";
		print "<td width=\"197\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>UserName</strong></font> </td>\n";
		print "<td width=\"125\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong><font color=\"#000000\">Subject</font></strong></font></td>\n";
		print "<td width=\"132\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>Dec 16 2001 3:34PM</strong></font> </td>\n";
		print "<td width=\"60\"><img alt=\"NO_PIC_SMALL\" height=\"57\" src=\"$Map{'IMAGES'}/$Map{'NO_PIC_SMALL'}\" width=\"57\" border=\"0\"></td>\n";
		print "<td width=\"48\">\n";
		print "<div align=\"center\">\n";
		print "<img alt=\"DELETSYMBOL\" src=\"$Map{'IMAGES'}/$Map{'DELETSYMBOL'}\" border=\"0\">\n";
		print "</div>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr>\n";
		print "<td>&nbsp;</td>\n";
		print "</tr>\n";
		print "\n";
# OUTBOX_COLOR_1
		print "<tr bgcolor=$Map{'OUTBOX_COLOR_1'}>\n";
		print "<td width=\"25\"><INPUT type=\"checkbox\" title=\"Change OUTBOX_COLOR_1...?\" onClick=\"changeOUTBOX_COLOR_1(theForm)\"></td>\n";
		print "<td width=\"197\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#990033\" size=\"4\"><strong>Outbox</strong></font></td>\n";
		print "<td width=\"125\">&nbsp;</td>\n";
		print "<td width=\"132\">&nbsp;</td>\n";
		print "<td width=\"60\">&nbsp;</td>\n";
		print "<td width=\"48\">&nbsp;</td>\n";
		print "</tr>\n";
		print "\n";
# OUTBOX_COLOR_2
		print "<tr bgcolor=$Map{'OUTBOX_COLOR_2'}>\n";
		print "<td width=\"25\"><INPUT type=\"checkbox\" title=\"Change OUTBOX_COLOR_2...?\" onClick=\"changeOUTBOX_COLOR_2(theForm)\"></td>\n";
		print "<td width=\"197\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#000066\" size=\"2\"><strong><font color=\"#663399\">Messages</font></strong></font> </td>\n";
		print "<td width=\"125\">&nbsp;</td>\n";
		print "<td width=\"132\">&nbsp;</td>\n";
		print "<td width=\"60\">&nbsp;</td>\n";
		print "<td width=\"48\">&nbsp;</td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr bgcolor=$Map{'OUTBOX_COLOR_1'}>\n";
		print "<td width=\"25\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>New</strong></font> </td>\n";
		print "<td width=\"197\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>To</strong></font> </td>\n";
		print "<td width=\"125\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Subject</strong></font> </td>\n";
		print "<td width=\"132\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Sent / Read</strong></font> </td>\n";
		print "<td width=\"60\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Profile</strong></font> </td>\n";
		print "<td width=\"48\"><font face=\"Arial, Helvetica, sans-serif\" color=\"#663399\" size=\"-2\"><strong>Delete</strong></font> </td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr bgcolor=$Map{'OUTBOX_COLOR_2'}>\n";
		print "<td width=\"25\">\n";
		print "<img alt=\"UNREADSYMBOL\" src=\"$Map{'IMAGES'}/$Map{'UNREADSYMBOL'}\" width=\"10\" height=\"8\">\n";
		print "</td>\n";
		print "<td width=\"197\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>UserName</strong></font> </td>\n";
		print "<td width=\"125\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong><font color=\"#000000\">Subject</font></strong></font> </td>\n";
		print "<td width=\"132\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>Dec 17 2001 4:06PM</strong></font><font size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"red\"><strong>Unread</strong></font> </td>\n";
		print "<td width=\"60\"><img alt=\"NO_PIC_SMALL\" height=\"57\" src=\"$Map{'IMAGES'}/$Map{'NO_PIC_SMALL'}\" width=\"57\" border=\"0\"></td>\n";
		print "<td width=\"48\">\n";
		print "<div align=\"center\">\n";
		print "<img alt=\"DELETSYMBOL\" src=\"$Map{'IMAGES'}/$Map{'DELETSYMBOL'}\" border=\"0\">\n";
		print "</div>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
		print "<tr bgcolor=$Map{'OUTBOX_COLOR_1'}>\n";
		print "<td width=\"25\">\n";
		print "<img alt=\"SPACESYMBOL\" src=\"$Map{'IMAGES'}/$Map{'SPACESYMBOL'}\" width=\"10\" height=\"8\">\n";
		print "</td>\n";
		print "<td width=\"197\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>UserName</strong></font> </td>\n";
		print "<td width=\"125\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong><font color=\"#000000\">Subject</font></strong></font></td>\n";
		print "<td width=\"132\"><font size=\"2\" face=\"Arial, Helvetica, sans-serif\"><strong>Dec 17 2001 2:51PM</strong></font><font size=\"2\" face=\"Arial, Helvetica, sans-serif\" color=\"red\"><strong>Dec 17 2001 3:01PM</strong></font> </td>\n";
		print "<td width=\"60\"><img alt=\"NO_PIC_SMALL\" height=\"57\" src=\"$Map{'IMAGES'}/$Map{'NO_PIC_SMALL'}\" width=\"57\" border=\"0\"></td>\n";
		print "<td width=\"48\">\n";
		print "<div align=\"center\">\n";
		print "<img alt=\"DELETSYMBOL\" src=\"$Map{'IMAGES'}/$Map{'DELETSYMBOL'}\" border=\"0\">\n";
		print "</div>\n";
		print "</td>\n";
		print "</tr>\n";
		print "</table>\n";
		print "\n";
		print "<table width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
		print "<tr>\n";
		print "<td height=\"20\" width=\"207\">&nbsp;</td>\n";
		print "<td height=\"20\" width=\"90\">\n";
# FIRSTARROW
		print "<INPUT type=\"checkbox\" title=\"Change FIRSTARROW...?\" onClick=\"changeFIRSTARROW(theForm)\">\n";
		print "<img alt=\"FIRSTARROW\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'FIRSTARROW'}\" width=\"90\" height=\"20\">\n";
		print "</td>\n";
		print "<td height=\"20\" width=\"90\">\n";
# PREVIOUSARROW
		print "<INPUT type=\"checkbox\" title=\"Change PREVIOUSARROW...?\" onClick=\"changePREVIOUSARROW(theForm)\">\n";
		print "<img alt=\"PREVIOUSARROW\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'PREVIOUSARROW'}\" width=\"90\" height=\"20\">\n";
		print "</td>\n";
		print "<td height=\"20\" width=\"90\">\n";
# NEXTARROW
		print "<INPUT type=\"checkbox\" title=\"Change NEXTARROW...?\" onClick=\"changeNEXTARROW(theForm)\">\n";
		print "<img alt=\"NEXTARROW\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'NEXTARROW'}\" width=\"90\" height=\"20\">\n";
		print "</td>\n";
		print "<td height=\"20\" width=\"90\">\n";
# LASTARROW
		print "<INPUT type=\"checkbox\" title=\"Change LASTARROW...?\" onClick=\"changeLASTARROW(theForm)\">\n";
		print "<img alt=\"LASTARROW\" border=\"0\" src=\"$Map{'IMAGES'}/$Map{'LASTARROW'}\" width=\"90\" height=\"20\">\n";
		print "</td>\n";
		print "</tr>\n";
		print "</table>\n";
		print "</td>\n";
		print "</tr>\n";
		print "\n";
# FOOTER
		print "<tr>\n";
		print "<td colspan=\"2\" bgcolor=$Map{'HTML_HEADFOOT_BGCOLOR'} height=\"50\" valign=\"middle\">\n";
		print "<INPUT type=\"checkbox\" title=\"Change FOOTER...?\" onClick=\"changeFOOTER(theForm)\">\n";
		print "<img alt=\"FOOTER\" src=\"$Map{'IMAGES'}/$Map{'FOOTER'}\" border=\"0\" height=\"50\">\n";
		print "<BR>\n";
# HTML_HEADFOOT_BGCOLOR
		print "<INPUT type=\"checkbox\" title=\"Change HTML_HEADFOOT_BGCOLOR...?\" onClick=\"changeHTML_HEADFOOT_BGCOLOR(theForm)\">\n";
		print "<FONT size=\"-1\">(<FONT color=\"red\">$Map{'HTML_HEADFOOT_BGCOLOR'}</FONT>)</FONT>\n";
		print "<BR>\n";
# WHICH_CONNECTIONS
		print "<INPUT type=\"checkbox\" title=\"Change WHICH_CONNECTIONS...?\" onClick=\"changeWHICH_CONNECTIONS(theForm)\">\n";
		print "<font size=\"4\" face=\"Arial, Helvetica, sans-serif\">$Map{'WHICH_CONNECTIONS'}.com</font><br>\n";
# COPYRIGHT_YEAR
		print "<INPUT type=\"checkbox\" title=\"Change COPYRIGHT_YEAR...?\" onClick=\"changeCOPYRIGHT_YEAR(theForm)\">\n";
		print "<font face=\"Arial, Helvetica, sans-serif\" size=\"2\"> Copyright &copy; $Map{'COPYRIGHT_YEAR'} $Map{'WHICH_CONNECTIONS'}.com. All rights reserved.</font>\n";
		print "</td>\n";
		print "</tr>\n";
		print "</table>\n";
		print "<SCRIPT language=\"javascript\" src=\"/JavaScript/Admin_ManipulateLinkMap.js\"></SCRIPT>\n";
		print "</body>\n";
		print "<INPUT type=\"submit\" name=\"Preview\" value=\"Preview\" onClick=\"resetOverwrite(theForm)\">\n";
		print "<INPUT type=\"submit\" name=\"Restore\" value=\"Restore\" onClick=\"resetOverwrite(theForm)\">\n";

		print "<INPUT type=\"submit\" name=\"Overwrite\" value=\"Over Write\" onClick=\"initializeOverwrite(theForm)\">\n";
#		print "<INPUT type=\"submit\" name=\"UndoOverwrite\" value=\"Undo OverWrite\" onClick=\"initializeUndoOverwrite(theForm)\">\n";

		print "<INPUT type=\"hidden\" name=\"SYSTEM\" value=\"$Map{'SYSTEM'}\">\n";
		print "<INPUT type=\"hidden\" name=\"DBNAME\" value=\"$Map{'DBNAME'}\">\n";
		print "<INPUT type=\"hidden\" name=\"DBUSER\" value=\"$Map{'DBUSER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"DBPWD\" value=\"$Map{'DBPWD'}\">\n";
		print "<INPUT type=\"hidden\" name=\"ADMIN_DBUSER\" value=\"$Map{'ADMIN_DBUSER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"ADMIN_DBPWD\" value=\"$Map{'ADMIN_DBPWD'}\">\n";
		print "<INPUT type=\"hidden\" name=\"ROOT\" value=\"$Map{'ROOT'}\">\n";
		print "<INPUT type=\"hidden\" name=\"IMAGES\" value=\"$Map{'IMAGES'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PICTURES\" value=\"$Map{'PICTURES'}\">\n";
		print "<INPUT type=\"hidden\" name=\"CGIBIN\" value=\"$Map{'CGIBIN'}\">\n";
		print "<INPUT type=\"hidden\" name=\"STYLE_SHEET\" value=\"$Map{'STYLE_SHEET'}\">\n";
		print "<INPUT type=\"hidden\" name=\"HTML_POPUP_BGCOLOR\" value=$Map{'HTML_POPUP_BGCOLOR'}>\n";
		print "<INPUT type=\"hidden\" name=\"HTML_HEADFOOT_BGCOLOR\" value=$Map{'HTML_HEADFOOT_BGCOLOR'}>\n";
		print "<INPUT type=\"hidden\" name=\"HTML_NAV_BGCOLOR\" value=$Map{'HTML_NAV_BGCOLOR'}>\n";
		print "<INPUT type=\"hidden\" name=\"HTML_BODY_BGCOLOR\" value=$Map{'HTML_BODY_BGCOLOR'}>\n";
		print "<INPUT type=\"hidden\" name=\"INBOX_COLOR_1\" value=$Map{'INBOX_COLOR_1'}>\n";
		print "<INPUT type=\"hidden\" name=\"INBOX_COLOR_2\" value=$Map{'INBOX_COLOR_2'}>\n";
		print "<INPUT type=\"hidden\" name=\"OUTBOX_COLOR_1\" value=$Map{'OUTBOX_COLOR_1'}>\n";
		print "<INPUT type=\"hidden\" name=\"OUTBOX_COLOR_2\" value=$Map{'OUTBOX_COLOR_2'}>\n";
		print "<INPUT type=\"hidden\" name=\"HTML_TITLE\" value=\"$Map{'HTML_TITLE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"HTML_HEAD\" value=\"$Map{'HTML_HEAD'}\">\n";
		print "<INPUT type=\"hidden\" name=\"COPYRIGHT_YEAR\" value=\"$Map{'COPYRIGHT_YEAR'}\">\n";
		print "<INPUT type=\"hidden\" name=\"EMAIL\" value=\"$Map{'EMAIL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"WHICH_CONNECTIONS\" value=\"$Map{'WHICH_CONNECTIONS'}\">\n";
		print "<INPUT type=\"hidden\" name=\"FIRSTARROW\" value=\"$Map{'FIRSTARROW'}\">\n";
		print "<INPUT type=\"hidden\" name=\"NEXTARROW\" value=\"$Map{'NEXTARROW'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PREVIOUSARROW\" value=\"$Map{'PREVIOUSARROW'}\">\n";
		print "<INPUT type=\"hidden\" name=\"LASTARROW\" value=\"$Map{'LASTARROW'}\">\n";
		print "<INPUT type=\"hidden\" name=\"LOGO\" value=\"$Map{'LOGO'}\">\n";
		print "<INPUT type=\"hidden\" name=\"FOOTER\" value=\"$Map{'FOOTER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"NO_PIC_SMALL\" value=\"$Map{'NO_PIC_SMALL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"NO_PIC_MEDIUM\" value=\"$Map{'NO_PIC_MEDIUM'}\">\n";
		print "<INPUT type=\"hidden\" name=\"NO_PIC_LARGE\" value=\"$Map{'NO_PIC_LARGE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"EMAILSYMBOL\" value=\"$Map{'EMAILSYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"DELETSYMBOL\" value=\"$Map{'DELETSYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"BOOKMARKSYMBOL\" value=\"$Map{'BOOKMARKSYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"UNREADSYMBOL\" value=\"$Map{'UNREADSYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"LINESYMBOL\" value=\"$Map{'LINESYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"SPACESYMBOL\" value=\"$Map{'SPACESYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PROCESSINGSYMBOL\" value=\"$Map{'PROCESSINGSYMBOL'}\">\n";
		print "<INPUT type=\"hidden\" name=\"BECOME_PREMIUM_MEMBER\" value=\"$Map{'BECOME_PREMIUM_MEMBER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"BECOME_MEMBER_GIF\" value=\"$Map{'BECOME_MEMBER_GIF'}\">\n";
		print "<INPUT type=\"hidden\" name=\"SMTP_HOST\" value=\"$Map{'SMTP_HOST'}\">\n";
		print "<INPUT type=\"hidden\" name=\"BLAT_PATH\" value=\"$Map{'BLAT_PATH'}\">\n";
		print "<INPUT type=\"hidden\" name=\"AUTHORIZE_TEST_MODE\" value=\"$Map{'AUTHORIZE_TEST_MODE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PRICE_ONE\" value=\"$Map{'PRICE_ONE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PRICE_THREE\" value=\"$Map{'PRICE_THREE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PRICE_TWELVE\" value=\"$Map{'PRICE_TWELVE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PRICE_LIFETIME\" value=\"$Map{'PRICE_LIFETIME'}\">\n";
		print "<INPUT type=\"hidden\" name=\"LOG_FOLDER\" value=\"$Map{'LOG_FOLDER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"PICTURES_FOLDER\" value=\"$Map{'PICTURES_FOLDER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"DOS_PICTURES_FOLDER\" value=\"$Map{'DOS_PICTURES_FOLDER'}\">\n";
		print "<INPUT type=\"hidden\" name=\"ADV_CGIBIN\" value=\"$Map{'ADV_CGIBIN'}\">\n";
		print "<INPUT type=\"hidden\" name=\"ADV_RETRIEVE\" value=\"$Map{'ADV_RETRIEVE'}\">\n";
		print "<INPUT type=\"hidden\" name=\"ADV_HOST_UNIQUE_ID\" value=\"$Map{'ADV_HOST_UNIQUE_ID'}\">\n";
		print "</FORM>\n";
		print "\n";
		print "</html>\n";
	}
exit 0;