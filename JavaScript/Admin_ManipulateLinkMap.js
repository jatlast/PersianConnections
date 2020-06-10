// This is the function that performs form verification. It will be invoked
// from the onSubmit() event handler. The handler should return whatever
// value this function returns.
function checkForm(myForm)
{
	if(myForm.Overwrite.value == "Overwrite")
	{
		var msg;
		var empty_fields = "";
		var errors = "";

		// Loop through the elements of the form, looking for all 
		// hidden. Then, check for fields that are empty and make a list of them.
		// Put together error messages for fields that are wrong.
		for(var i = 0; i < myForm.length; i++) 
			{
			var e = myForm.elements[i];
			if (e.type == "hidden")
				{
					// first check if the field is empty
					if ( (e.value == null) || (e.value == "") || (e.value == "empty") )//|| has_blank(e) ) 
					{
						empty_fields += "\n       " + e.name;
						continue;
					}
				}
			}

		// Now, if there were any errors, display the messages, and
		// return false to prevent the form from being submitted. 
		// Otherwise return true.
		if (!empty_fields) return ( finalConfirm(theForm) );

		msg  = "______________________________________________________\n\n"
		msg += "The form was not submitted because of the following error(s).\n";
		msg += "Please correct these error(s) and re-submit.\n";
		msg += "______________________________________________________\n\n"

		if (empty_fields) 
		{
			msg += "- The following required field(s) are empty:" 
					+ empty_fields + "\n";
			if (errors) msg += "\n";
		}
		msg += errors;

		msg += "\n\n"
		msg += "1: Close this dialog and press the 'Preview' button.\n";
		msg += "   This will display all the hidden fields in question\n";
		msg += "    to the browser.\n\n";
		msg += "2: Scan the page with CTL^F to find the string 'empty'.\n";
		msg += "   If you can't find 'empty' one of the fields may\n";
		msg += "    contain a space, be null, or even blank.\n\n";
		msg += "3: You can't OverWrite LinkMap.dat with incorrect data\n";
		msg += "    so you have to find all errored values.\n\n";
		msg += "4: OverWriting with a value of 'empty' will corrupt the\n";
		msg += "    LinkMap.dat file so they all should be replaced.\n\n";
		msg += "5: If all else fails you can restore from the LinkMap.dat\n";
		msg += "    file by pressing the 'Restore' button.";

		alert(msg);
		return false;
	}
}

function finalConfirm(myForm)
{
  if( confirm("Are you sure you want to overwrite the current LinkMap.dat file?") )
  {
	return true;
  }
  else
  {
	return false;
  }
}


// A utility function that returns true if a string contains any 
// whitespace characters.
function has_blank(s)
{
    for(var i = 0; i < s.length; i++) {
        var c = s.charAt(i);
        if ((c == ' ') || (c == '\n') || (c == '\t')) 
		{
			return false;
		}
    }
    return true;
}

// initializeOverwrite
function initializeOverwrite(myForm)
{
	myForm.Overwrite.value = "Overwrite";
// removed because of IIS permissions problems!!!!!!!!!
//	resetUndoOverwrite(myForm);
}

// initializeUndoOverwrite
function initializeUndoOverwrite(myForm)
{
	myForm.UndoOverwrite.value = "UndoOverwrite";
	resetOverwrite(myForm);
}

// resetOverwrite
function resetOverwrite(myForm)
{
	myForm.Overwrite.value = "Over Write";
}

// resetUndoOverwrite
function resetUndoOverwrite(myForm)
{
	myForm.UndoOverwrite.value = "Undo OverWrite";
}


// SYSTEM
function changeSYSTEM(myForm)
{
	var NewValue = prompt('Enter a value for SYSTEM', myForm.SYSTEM.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.SYSTEM.value = NewValue;
    }
}

// DBNAME
function changeDBNAME(myForm)
{
	var NewValue = prompt('Enter a value for DBNAME', myForm.DBNAME.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.DBNAME.value = NewValue;
    }
}

// DBUSER
function changeDBUSER(myForm)
{
	var NewValue = prompt('Enter a value for DBUSER', myForm.DBUSER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.DBUSER.value = NewValue;
    }
}

// DBPWD
function changeDBPWD(myForm)
{
	var NewValue = prompt('Enter a value for DBPWD', myForm.DBPWD.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.DBPWD.value = NewValue;
    }
}

// ADMIN_DBUSER
function changeADMIN_DBUSER(myForm)
{
	var NewValue = prompt('Enter a value for Admin DBUSER', myForm.ADMIN_DBUSER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.ADMIN_DBUSER.value = NewValue;
    }
}

// ADMIN_DBPWD
function changeADMIN_DBPWD(myForm)
{
	var NewValue = prompt('Enter a value for Admin DBPWD', myForm.ADMIN_DBPWD.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.ADMIN_DBPWD.value = NewValue;
    }
}

// ROOT
function changeROOT(myForm)
{
	var NewValue = prompt('Enter a value for ROOT', myForm.ROOT.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.ROOT.value = NewValue;
    }
}

// IMAGES
function changeIMAGES(myForm)
{
	var NewValue = prompt('Enter a value for IMAGES', myForm.IMAGES.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.IMAGES.value = NewValue;
    }
}

// changePICTURES
function changePICTURES(myForm)
{
	var NewValue = prompt('Enter a value for PICTURES', myForm.PICTURES.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PICTURES.value = NewValue;
    }
}

// CGIBIN
function changeCGIBIN(myForm)
{
	var NewValue = prompt('Enter a value for CGIBIN', myForm.CGIBIN.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.CGIBIN.value = NewValue;
    }
}

// STYLE_SHEET
function changeSTYLE_SHEET(myForm)
{
	var NewValue = prompt('Enter a value for STYLE_SHEET', myForm.STYLE_SHEET.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.STYLE_SHEET.value = NewValue;
    }
}

// HTML_POPUP_BGCOLOR
function changeHTML_POPUP_BGCOLOR(myForm)
{
	var NewValue = prompt('Enter a value for HTML_POPUP_BGCOLOR', myForm.HTML_POPUP_BGCOLOR.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.HTML_POPUP_BGCOLOR.value = NewValue;
    }
}

// HTML_HEADFOOT_BGCOLOR
function changeHTML_HEADFOOT_BGCOLOR(myForm)
{
	var NewValue = prompt('Enter a value for HTML_HEADFOOT_BGCOLOR', myForm.HTML_HEADFOOT_BGCOLOR.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.HTML_HEADFOOT_BGCOLOR.value = NewValue;
    }
}

// HTML_NAV_BGCOLOR
function changeHTML_NAV_BGCOLOR(myForm)
{
	var NewValue = prompt('Enter a value for HTML_NAV_BGCOLOR', myForm.HTML_NAV_BGCOLOR.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.HTML_NAV_BGCOLOR.value = NewValue;
    }
}

// HTML_BODY_BGCOLOR
function changeHTML_BODY_BGCOLOR(myForm)
{
	var NewValue = prompt('Enter a value for HTML_BODY_BGCOLOR', myForm.HTML_BODY_BGCOLOR.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.HTML_BODY_BGCOLOR.value = NewValue;
    }
}

// INBOX_COLOR_1
function changeINBOX_COLOR_1(myForm)
{
	var NewValue = prompt('Enter a value for INBOX_COLOR_1', myForm.INBOX_COLOR_1.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.INBOX_COLOR_1.value = NewValue;
    }
}

// INBOX_COLOR_2
function changeINBOX_COLOR_2(myForm)
{
	var NewValue = prompt('Enter a value for INBOX_COLOR_2', myForm.INBOX_COLOR_2.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.INBOX_COLOR_2.value = NewValue;
    }
}

// OUTBOX_COLOR_1
function changeOUTBOX_COLOR_1(myForm)
{
	var NewValue = prompt('Enter a value for OUTBOX_COLOR_1', myForm.OUTBOX_COLOR_1.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.OUTBOX_COLOR_1.value = NewValue;
    }
}

// OUTBOX_COLOR_2
function changeOUTBOX_COLOR_2(myForm)
{
	var NewValue = prompt('Enter a value for OUTBOX_COLOR_2', myForm.OUTBOX_COLOR_2.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.OUTBOX_COLOR_2.value = NewValue;
    }
}

// HTML_TITLE
function changeHTML_TITLE(myForm)
{
	var NewValue = prompt('Enter a value for HTML_TITLE', myForm.HTML_TITLE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.HTML_TITLE.value = NewValue;
    }
}

// HTML_HEAD
function changeHTML_HEAD(myForm)
{
	var NewValue = prompt('Enter a value for HTML_HEAD', myForm.HTML_HEAD.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.HTML_HEAD.value = NewValue;
    }
}

// COPYRIGHT_YEAR
function changeCOPYRIGHT_YEAR(myForm)
{
	var NewValue = prompt('Enter a value for COPYRIGHT_YEAR', myForm.COPYRIGHT_YEAR.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.COPYRIGHT_YEAR.value = NewValue;
    }
}

// EMAIL
function changeEMAIL(myForm)
{
	var NewValue = prompt('Enter a value for EMAIL', myForm.EMAIL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.EMAIL.value = NewValue;
    }
}

// WHICH_CONNECTIONS
function changeWHICH_CONNECTIONS(myForm)
{
	var NewValue = prompt('Enter a value for WHICH_CONNECTIONS', myForm.WHICH_CONNECTIONS.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.WHICH_CONNECTIONS.value = NewValue;
    }
}

// FIRSTARROW
function changeFIRSTARROW(myForm)
{
	var NewValue = prompt('Enter a value for FIRSTARROW', myForm.FIRSTARROW.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.FIRSTARROW.value = NewValue;
    }
}

// NEXTARROW
function changeNEXTARROW(myForm)
{
	var NewValue = prompt('Enter a value for NEXTARROW', myForm.NEXTARROW.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.NEXTARROW.value = NewValue;
    }
}

// PREVIOUSARROW
function changePREVIOUSARROW(myForm)
{
	var NewValue = prompt('Enter a value for PREVIOUSARROW', myForm.PREVIOUSARROW.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PREVIOUSARROW.value = NewValue;
    }
}

// LASTARROW
function changeLASTARROW(myForm)
{
	var NewValue = prompt('Enter a value for LASTARROW', myForm.LASTARROW.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.LASTARROW.value = NewValue;
    }
}

// LOGO
function changeLOGO(myForm)
{
	var NewValue = prompt('Enter a value for LOGO', myForm.LOGO.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.LOGO.value = NewValue;
    }
}

// FOOTER
function changeFOOTER(myForm)
{
	var NewValue = prompt('Enter a value for FOOTER', myForm.FOOTER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.FOOTER.value = NewValue;
    }
}

// NO_PIC_SMALL
function changeNO_PIC_SMALL(myForm)
{
	var NewValue = prompt('Enter a value for NO_PIC_SMALL', myForm.NO_PIC_SMALL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.NO_PIC_SMALL.value = NewValue;
    }
}

// NO_PIC_MEDIUM
function changeNO_PIC_MEDIUM(myForm)
{
	var NewValue = prompt('Enter a value for NO_PIC_MEDIUM', myForm.NO_PIC_MEDIUM.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.NO_PIC_MEDIUM.value = NewValue;
    }
}

// NO_PIC_LARGE
function changeNO_PIC_LARGE(myForm)
{
	var NewValue = prompt('Enter a value for NO_PIC_LARGE', myForm.NO_PIC_LARGE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.NO_PIC_LARGE.value = NewValue;
    }
}

// EMAILSYMBOL
function changeEMAILSYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for EMAILSYMBOL', myForm.EMAILSYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.EMAILSYMBOL.value = NewValue;
    }
}

// DELETSYMBOL
function changeDELETSYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for DELETSYMBOL', myForm.DELETSYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.DELETSYMBOL.value = NewValue;
    }
}

// BOOKMARKSYMBOL
function changeBOOKMARKSYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for BOOKMARKSYMBOL', myForm.BOOKMARKSYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.BOOKMARKSYMBOL.value = NewValue;
    }
}

// UNREADSYMBOL
function changeUNREADSYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for UNREADSYMBOL', myForm.UNREADSYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.UNREADSYMBOL.value = NewValue;
    }
}

// LINESYMBOL
function changeLINESYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for LINESYMBOL', myForm.LINESYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.LINESYMBOL.value = NewValue;
    }
}

// SPACESYMBOL
function changeSPACESYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for SPACESYMBOL', myForm.SPACESYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.SPACESYMBOL.value = NewValue;
    }
}

// PROCESSINGSYMBOL
function changePROCESSINGSYMBOL(myForm)
{
	var NewValue = prompt('Enter a value for PROCESSINGSYMBOL', myForm.PROCESSINGSYMBOL.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PROCESSINGSYMBOL.value = NewValue;
    }
}

// BECOME_PREMIUM_MEMBER
function changeBECOME_PREMIUM_MEMBER(myForm)
{
	var NewValue = prompt('Enter a value for BECOME_PREMIUM_MEMBER', myForm.BECOME_PREMIUM_MEMBER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.BECOME_PREMIUM_MEMBER.value = NewValue;
    }
}

// BECOME_MEMBER_GIF
function changeBECOME_MEMBER_GIF(myForm)
{
	var NewValue = prompt('Enter a value for BECOME_MEMBER_GIF', myForm.BECOME_MEMBER_GIF.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.BECOME_MEMBER_GIF.value = NewValue;
    }
}

// SMTP_HOST
function changeSMTP_HOST(myForm)
{
	var NewValue = prompt('Enter a value for SMTP_HOST', myForm.SMTP_HOST.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.SMTP_HOST.value = NewValue;
    }
}

// BLAT_PATH
function changeBLAT_PATH(myForm)
{
	var NewValue = prompt('Enter a value for BLAT_PATH', myForm.BLAT_PATH.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.BLAT_PATH.value = NewValue;
    }
}

// AUTHORIZE_TEST_MODE
function changeAUTHORIZE_TEST_MODE(myForm)
{
	var NewValue = prompt('Enter a value for AUTHORIZE_TEST_MODE', myForm.AUTHORIZE_TEST_MODE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.AUTHORIZE_TEST_MODE.value = NewValue;
    }
}

// PRICE_ONE
function changePRICE_ONE(myForm)
{
	var NewValue = prompt('Enter a value for PRICE_ONE', myForm.PRICE_ONE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PRICE_ONE.value = NewValue;
    }
}

// PRICE_THREE
function changePRICE_THREE(myForm)
{
	var NewValue = prompt('Enter a value for PRICE_THREE', myForm.PRICE_THREE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PRICE_THREE.value = NewValue;
    }
}

// PRICE_TWELVE
function changePRICE_TWELVE(myForm)
{
	var NewValue = prompt('Enter a value for PRICE_TWELVE', myForm.PRICE_TWELVE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PRICE_TWELVE.value = NewValue;
    }
}

// PRICE_LIFETIME
function changePRICE_LIFETIME(myForm)
{
	var NewValue = prompt('Enter a value for PRICE_LIFETIME', myForm.PRICE_LIFETIME.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PRICE_LIFETIME.value = NewValue;
    }
}

// LOG_FOLDER
function changeLOG_FOLDER(myForm)
{
	var NewValue = prompt('Enter a value for LOG_FOLDER', myForm.LOG_FOLDER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.LOG_FOLDER.value = NewValue;
    }
}

// PICTURES_FOLDER
function changePICTURES_FOLDER(myForm)
{
	var NewValue = prompt('Enter a value for PICTURES_FOLDER', myForm.PICTURES_FOLDER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.PICTURES_FOLDER.value = NewValue;
    }
}

// DOS_PICTURES_FOLDER
function changeDOS_PICTURES_FOLDER(myForm)
{
	var NewValue = prompt('Enter a value for DOS_PICTURES_FOLDER', myForm.DOS_PICTURES_FOLDER.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.DOS_PICTURES_FOLDER.value = NewValue;
    }
}  

// ADV_CGIBIN
function changeADV_CGIBIN(myForm)
{
	var NewValue = prompt('Enter a value for ADV_CGIBIN', myForm.ADV_CGIBIN.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.ADV_CGIBIN.value = NewValue;
    }
}

// ADV_RETRIEVE
function changeADV_RETRIEVE(myForm)
{
	var NewValue = prompt('Enter a value for ADV_RETRIEVE', myForm.ADV_RETRIEVE.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.ADV_RETRIEVE.value = NewValue;
    }
}

// ADV_HOST_UNIQUE_ID
function changeADV_HOST_UNIQUE_ID(myForm)
{
	var NewValue = prompt('Enter a value for ADV_HOST_UNIQUE_ID', myForm.ADV_HOST_UNIQUE_ID.value);
	if (NewValue==' ' || NewValue==null)
	{
		// do nothing
	}
	else
	{
		myForm.ADV_HOST_UNIQUE_ID.value = NewValue;
    }
}

