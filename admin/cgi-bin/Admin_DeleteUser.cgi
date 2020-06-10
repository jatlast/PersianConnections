#!/usr/local/bin/perl -w

use MSSQL::DBlib;
use MSSQL::DBlib::Const::General;
use MSSQL::DBlib::Const::Datatypes;

use strict;
use CGI qw/:standard/;

# Add directories to perl environment path...
# Smithers
unshift @INC, "D:/Required/INC/";
# Grimes
unshift @INC, "C:/Required/INC/";

require "DatabaseFunctions.pl";
require "CgiFunctions.pl";
require "SendMailFunctions.pl";
require "UtilityFunctions.pl";

my $DebugThisAp			   = "1";
my $DebugCgiFunctions 	   = "1";
my $DebugDatabaseFunctions = "1";
my $DebugUtilityFunctions  = "1";
my $DebugMailSendFunctions = "1";

my $ProgramName = "Admin_DeleteUser.cgi";

my $count = 0;

#Begin HTML so errors show up in browser...
print CGI::header('text/html');
print "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/1999/REC-html401-19991224/loose.dtd\">\n";
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

# declare global variables...
my $user_name 	 = "";
my $sent_from 	 = "";
my $sent_to 	 = "";
my $sent_bcc 	 = "";
my $subject		 = "";
my $message_text = "";

if(CGI::param('user_name'))   {$user_name    = CGI::param('user_name');}
if(CGI::param('sent_from'))   {$sent_from 	 = CGI::param('sent_from');}
if(CGI::param('sent_to'))	  {$sent_to 	 = CGI::param('sent_to');}
if(CGI::param('sent_bcc'))	  {$sent_bcc 	 = CGI::param('sent_bcc');}
if(CGI::param('subject'))	  {$subject    	 = CGI::param('subject');}
if(CGI::param('message_text')){$message_text = CGI::param('message_text');}

# Escape special characters...
if($subject =~ m/"/)
	{
		$subject =~ s/"/""/g;
	}
#print "<!-- pre removal message_text ($message_text) -->\n";
if($message_text =~ m/"/)
	{
		$message_text =~ s/"/""/g;
	}

# Output all beginning HTML...
&UtilityFunctions::Print_Admin_HTML_Top($ProgramName, $DebugUtilityFunctions, %Map);


print "  <!-- Begin Entire Body NOT Logged In-->\n";
print "  <BODY>\n";
print "    <!-- Begin Main Table -->\n";
print "    <TABLE width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
print "      <!-- Begin Main Data Cell -->\n";
print "      <TR>\n";
print "        <TD bgcolor=$Map{'HTML_BODY_BGCOLOR'}>\n";
print "    	     <TABLE width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"3\">\n";
print "            <TR align=\"center\">\n";
print "              <TD>\n";
print "                  <FONT color=\"#FFFFFF\" face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>$Map{'WHICH_CONNECTIONS'}</STRONG></FONT>\n";
print "              </TD>\n";
print "            </TR>\n";
print "            <TR align=\"center\">\n";
print "              <TD>\n";
print "                  <FONT face=\"Arial, Helvetica, sans-serif\" size=\"3\"><STRONG>Admin Delete User Results Page</STRONG></FONT>\n";
print "                  <BR>&nbsp;<BR>\n";
print "              </TD>\n";
print "            </TR>\n";

if($DebugThisAp eq "1")
	{
		print "<!--\n";
		print "user_name = ($user_name)\n";
		print "sent_from = ($sent_from)\n";
		print "sent_to = ($sent_to)\n";
		print "sent_bcc = ($sent_bcc)\n";
		print "subject = ($subject)\n";
		print "message_text = ($message_text)\n";
		print "-->\n";
	}

my $SqlStatement = "admin_DeleteEntireProfileByUserName \"$user_name\"";
my $return_value = &DatabaseFunctions::Run_This_Sql_Statement($Map{'DBUSER'}, $Map{'DBPWD'}, $Map{'DBNAME'}, 'Admin_DeleteUser.cgi', $SqlStatement, $DebugDatabaseFunctions);
print "\n<!-- Run_This_Sql_Statement return_value = $return_value-->\n" if $DebugThisAp eq "1";
if($return_value eq "1")
	{
			# User Was Deleted...
		print "<TR><TD>$user_name was successfully deleted.<BR><A href=\"javascript:newWindowGeneric('Admin_GenSendMail.cgi?sent_from=$sent_from&amp;sent_to=$sent_to&amp;sent_bcc=&amp;subject=$subject&amp;message_text=$message_text')\"> Send mail to $user_name</A></TD></TR>\n";
	}
else
	{
			if($sent_from eq "" or $sent_to eq "")
			{
					print "<TR><TD><FONT color=\"red\">$user_name.</FONT> was probably deleted.<BR><A href=\"Admin_GetDanglingUserNames.cgi?user_name=$user_name\">Return to Get Dangling User Names</A> and refresh the screen to make sure</TD></TR>\n";
			}
		else
			{
				print "<TR><TD><FONT color=\"red\">$user_name was NOT deleted. </FONT> <BR>View the source and note the database messages.<BR>(Use F5 to try deleting $user_name again)</TD></TR>\n";
			}
	}
	
print "                    <!-- submit -->\n";
print "                    <TR>\n";
print "                      <TD>\n";
print "						   <INPUT TYPE=BUTTON VALUE=\"Close Window\" onClick=\"Closer()\">\n";
print "                      </TD>\n";
print "                    </TR>\n";
print "						  <SCRIPT type=\"text/javascript\" language=\"javascript\">\n";
print "						  <!--\n";
print "    					 		 function Closer()\n";
print "    							 {\n";
print "        						 	  window.close()\n";
print "    							 }\n";
print "						  //-->\n";
print "						 </SCRIPT>\n";
	
print "          </TABLE>\n";
print "        </TD>\n";
print "        <!-- End Main Data Cell -->\n";
print "      </TR>\n";
print "      <!-- End Navigation and Main Row -->\n";
print "    </TABLE>\n";
# Output all ending HTML...
&UtilityFunctions::Print_Admin_HTML_Bottom($ProgramName, "ASC", "DESC", 0, 1, 0, $DebugUtilityFunctions, %Map);
	
#End HTML...
print "</HTML>\n";
exit 0;
