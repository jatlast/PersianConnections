// This file contains JavaScript for confirming the Admin_GenManualCheckForm
// and is used by Admin_GenManualCheckForm.cgi

function checkForm(theForm)
{ 
// ----- first_name
  if (theForm.first_name.value == "")
  {
    alert("Please enter a valid value for the \"First Name\" field.");
    theForm.first_name.focus();
    theForm.first_name.select();
    return (false);
  }

// ----- last_name
  if (theForm.last_name.value == "")
  {
    alert("Please enter a valid value for the \"Last Name\" field.");
    theForm.last_name.focus();
    theForm.last_name.select();
    return (false);
  }

// ----- street_address
  if (theForm.street_address.value == "")
  {
    alert("Please enter a valid value for the \"Street Address\" field.");
    theForm.street_address.focus();
    theForm.street_address.select();
    return (false);
  }

// ----- country
  if (theForm.country.value == "")
  {
    alert("Please enter a valid value for the \"Country\" field.");
    theForm.country.focus();
    theForm.country.select();
    return (false);
  }

// ----- check_number
  if (!validNumber(theForm.check_number.value))
  {
    alert("Please enter a valid \"Check #\".");
    theForm.check_number.focus();
    theForm.check_number.select();
    return (false);
  }

// ----- date
  if (!validNumber(theForm.date.value))
  {
    alert("Please enter a valid \"Date\".");
    theForm.date.focus();
    theForm.date.select();
    return (false);
  }

// ----- months_joined
  if (theForm.months_joined.selectedIndex < 1)
  {
    alert("Please select one of the \"Months Joined\" options.")
    theForm.months_joined.focus()
    return (false)
  }

// ----- bank_account_number
  if (!validNumber(theForm.bank_account_number.value))
  {
    alert("Please enter a valid \"Bank Account Number\".");
    theForm.bank_account_number.focus();
    theForm.bank_account_number.select();
    return (false);
  }

// ----- bank_ABA_code
  if (!validNumber(theForm.bank_ABA_code.value))
  {
    alert("Please enter a valid \"Bank ABA Code\".");
    theForm.bank_ABA_code.focus();
    theForm.bank_ABA_code.select();
    return (false);
  }

// ----- amount
  if (!validNumber(theForm.amount.value))
  {
    alert("Please enter a valid \"Amount\".");
    theForm.amount.focus();
    theForm.amount.select();
    return (false);
  }

return( finalConfirm(theForm) );

} // End checkFormFunction

function validNumber(myNumber)
{
invalidChars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    // field cannot be empty...
    if(myNumber == "")
    {
        return(false);
    }

    // does it contain any invalid characters...
    for (i=0; i<invalidChars.length; i++)
    {
        badChar = invalidChars.charAt(i);
        if (myNumber.indexOf(badChar, 0) > -1)
        {
            return(false);
        }
    }
return(true);
} // End validNumber function

function finalConfirm(myForm)
{
  var agree=confirm("Do you want to enter this check into the database?");
  if (agree)
  {
  	return(true);
  }
  else
  {
  	return(false);
  }
}
