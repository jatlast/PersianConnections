// This file contains JavaScript for confirming the Authorize.Net membership form
// and is used by GenAuthorizeNetForm.cgi

function checkForm(theForm)
{ 
// ----- months_joined
  var RadioOption = -1
  for (i=0; i<theForm.months_joined.length; i++)
  {
    if (theForm.months_joined[i].checked)
    {
       RadioOption = i
    }
  }
  if (RadioOption == -1)
  {
     alert("You Must Choose A Membership Plan")
     return (false)
  }


// ----- bank_ABA_code

  if (theForm.bank_ABA_code.value == "")
  {
    alert("Please enter a value for the \"Bank ABA Code\" field.")
    theForm.bank_ABA_code.focus()
    return (false)
  }
  if (!validNumber(theForm.bank_ABA_code.value))
  {
    alert("Please enter a valid \"Bank ABA Code\".");
    theForm.bank_ABA_code.focus();
    theForm.bank_ABA_code.select();
    return (false);
  }

  if (theForm.bank_ABA_code.value.length < 4)
  {
    alert("Please enter all numbers in the \"Bank ABA Code\" field.")
    theForm.bank_ABA_code.focus()
    theForm.bank_ABA_code.select()
    return (false)
  }

// ----- bank_account_number

  if (theForm.bank_account_number.value == "")
  {
    alert("Please enter a value for the \"Bank Account Number\" field.")
    theForm.bank_account_number.focus()
    return (false)
  }
  if (!validNumber(theForm.bank_account_number.value))
  {
    alert("Please enter a valid \"Bank Account Number\".");
    theForm.bank_account_number.focus();
    theForm.bank_account_number.select();
    return (false);
  }

  if (theForm.bank_account_number.value.length < 8)
  {
    alert("Please enter all numbers in the \"Bank Account Number\" field.")
    theForm.bank_account_number.focus()
    theForm.bank_account_number.select()
    return (false)
  }
  return ( finalConfirm(theForm) )
} // End checkFormFunction

function validNumber(myAccountNumber)
{
invalidChars = " abcdefghijklmnopqrstuvwxyz"

    // field cannot be empty...
    if(myAccountNumber == "")
    {
        return false
    }

    // does it contain any invalid characters...
    for (i=0; i<invalidChars.length; i++)
    {
        badChar = invalidChars.charAt(i)
        if (myAccountNumber.indexOf(badChar, 0) > -1)
        {
            return false
        }
    }

return true
} // End validAccountNumber function

function finalConfirm(myForm)
{
  var months = 0
  var amount = 0
  var card = 0
    for (i=0; i<myForm.months_joined.length; i++)
    {
      if (myForm.months_joined[i].checked)
      {
         months = myForm.months_joined[i].value
      }
    }
  if(months == 1)
  {
     MembershipName = "1 month"
  }
  if(months == 3)
  {
     MembershipName = "3 month"
  }
  if(months == 12)
  {
     MembershipName = "1 year"
  }
  if(months == 240)
  {
     MembershipName = "Lifetime"
  }

  if( confirm("Do you wish to sign up for a " + MembershipName + " recurring membership?") )
  {
	return true
  }
  else
  {
	return false
  }
}
