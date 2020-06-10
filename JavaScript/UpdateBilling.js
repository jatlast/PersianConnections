// This file contains JavaScript for verifing the UpdateBilling.exe generated  form

function checkForm(theForm)
{ 
// ----- name_on_card
/*
  if (theForm.name_on_card.value == "")
  {
    alert("Please enter a valid value for the \"Cardholder's Name\" field.")
    theForm.name_on_card.focus()
    return (false)
  }

  // ----- cvv2_code

  if (theForm.cvv2_code.value == "")
  {
    alert("Please enter a 3 digit value for the \"CVV2\" field.")
    theForm.cvv2_code.focus()
    return (false)
  }
  if (!validAccountCode(theForm.cvv2_code.value))
  {
    alert("Please enter 3 valid digits in the \"CVV2\" field.");
    theForm.cvv2_code.focus();
    theForm.cvv2_code.select();
    return (false);
  }

  if (theForm.cvv2_code.value.length < 3)
  {
    alert("Please enter all 2 numbers in the \"CVV2\" field.")
    theForm.cvv2_code.focus()
    theForm.cvv2_code.select()
    return (false)
  }

// ----- account_number

  if (theForm.account_number.value == "")
  {
    alert("Please enter a value for the \"Card Account Number\" field.")
    theForm.account_number.focus()
    return (false)
  }
  if (!validAccountNumber(theForm.account_number.value))
  {
    alert("Please enter a valid \"Card Account Number\".");
    theForm.account_number.focus();
    theForm.account_number.select();
    return (false);
  }

  if (theForm.account_number.value.length < 16)
  {
    alert("Please enter all 16 characters in the \"Card Account Number\" field.")
    theForm.account_number.focus()
    theForm.account_number.select()
    return (false)
  }

  return (true)
} // End checkFormFunction

function validAccountNumber(myAccountNumber)
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
*/
return true
} // End validAccountNumber function

function newWindowGeneric(picName) 
{
		var myWindow = window.open(picName, 'CVV2Info', 'toolbar=no,location=no,scrollbars=yes,resizable=yes,width=600,height=800')
		myWindow.focus()
}

