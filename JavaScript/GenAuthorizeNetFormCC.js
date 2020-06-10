// This file contains JavaScript for confirming the Authorize.Net membership form
// and is used by GenAuthorizeNetForm.cgi

function checkPromotionalCode(theForm) 
{
// ----- promotion_code
  if (theForm.promotion_code.value == "")
  {
    alert("Please enter a valid value for the \"Promotional Code\" field.")
    theForm.promotion_code.focus()
    return (false)
  }
}

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

// ----- name_on_card
  if (theForm.name_on_card.value == "")
  {
    alert("Please enter a valid value for the \"Name\" field.")
    theForm.name_on_card.focus()
    return (false)
  }

// ----- street_address
  if (theForm.street_address.value == "" || theForm.street_address.value.length < 3)
  {
    alert("Please enter a valid value for the \"Address\" field.")
    theForm.street_address.focus()
    return (false)
  }

// ----- city
  if (theForm.city.value == "" || theForm.city.value.length < 2)
  {
    alert("Please enter a valid value for the \"City\" field.")
    theForm.city.focus()
    return (false)
  }

// ----- state
  if (theForm.state.selectedIndex < 1)
  {
    alert("Please select one of the \"State\" options.")
    theForm.state.focus()
    return (false)
  }

// ----- country
  if (theForm.country.selectedIndex < 1)
  {
    alert("Please select one of the \"Country\" options.")
    theForm.country.focus()
    return (false)
  }

// ----- zip
  if (theForm.zip.value == "" || theForm.zip.value.length < 5)
  {
    alert("Please enter a valid value for the \"Postal Code\" field.")
    theForm.zip.focus()
    return (false)
  }

// ----- telephone
  if (theForm.telephone.value == "" || theForm.telephone.value.length < 10)
  {
    alert("Please enter a valid value for the \"Telephone\" field.")
    theForm.telephone.focus()
    return (false)
  }

// ----- card_type
  if (theForm.card_type.selectedIndex < 1)
  {
    alert("Please select one of the \"Card Type\" options.")
    theForm.card_type.focus()
    return (false)
  }

// ----- expiration_month
  if (theForm.expiration_month.selectedIndex < 1)
  {
    alert("Please select one of the \"Expiration Month\" options.")
    theForm.expiration_month.focus()
    return (false)
  }

// ----- expiration_year
  if (theForm.expiration_year.selectedIndex < 1)
  {
    alert("Please select one of the \"Expiration Year\" options.")
    theForm.expiration_year.focus()
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

  if (theForm.account_number.value.length < 13)
  {
    alert("Please enter at least 13 characters in the \"Card Account Number\" field.")
    theForm.account_number.focus()
    theForm.account_number.select()
    return (false)
  }

  // ----- cvv2_code

  if (theForm.cvv2_code.value == "")
  {
    alert("Please enter valid digits for the \"CVV2\" field.")
    theForm.cvv2_code.focus()
    return (false)
  }
  if (!validAccountCode(theForm.cvv2_code.value))
  {
    alert("Please enter valid digits in the \"CVV2\" field.");
    theForm.cvv2_code.focus();
    theForm.cvv2_code.select();
    return (false);
  }

  if (theForm.cvv2_code.value.length < 3)
  {
    alert("Please enter valid digits in the \"CVV2\" field.")
    theForm.cvv2_code.focus()
    theForm.cvv2_code.select()
    return (false)
  }

  return ( finalConfirm(theForm) )
} // End checkFormFunction

function checkPromotionForm(theForm)
{ 
  return ( finalConfirm(theForm) )
} // End checkFormFunction


function validAccountCode(myAccountCode)
{
invalidChars = " abcdefghijklmnopqrstuvwxyz"

    // field cannot be empty...
    if(myAccountCode == "")
    {
        return false
    }

    // does it contain any invalid characters...
    for (i=0; i<invalidChars.length; i++)
    {
        badChar = invalidChars.charAt(i)
        if (myAccountCode.indexOf(badChar, 0) > -1)
        {
            return false
        }
    }
return true
} // End validAccountCode function

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
return true
} // End validAccountNumber function

function finalConfirm(myForm)
{
  var months = 0
  var MembershipName = 0
//  var cardHolder = myForm.name_on_card.value
  var card = 0
    for (i=0; i<myForm.months_joined.length; i++)
    {
      if (myForm.months_joined[i].checked)
      {
         months = myForm.months_joined[i].value
      }
    }
  if(months == 0)
  {
     MembershipName = "Promotional"
  }
  if(months == 1)
  {
     MembershipName = "1 month recurring"
  }
  if(months == 3)
  {
     MembershipName = "3 month recurring"
  }
  if(months == 6)
  {
     MembershipName = "6 month recurring"
  }
  if(months == 12)
  {
     MembershipName = "1 year recurring"
  }
  if(months == 240)
  {
     MembershipName = "Lifetime"
  }

/*
  if(myForm.card_type.value == 4)
  {
     card = "Visa"
  }
  if(myForm.card_type.value == 5)
  {
     card = "Master Card"
  }
*/
  if( confirm("Do you wish to sign up for a " + MembershipName + " membership?") )
  {
	return true
  }
  else
  {
	return false
  }
}

function newWindowGeneric(picName) 
{
		var myWindow = window.open(picName, 'CVV2Info', 'toolbar=no,location=no,scrollbars=yes,resizable=yes,width=600,height=800')
		myWindow.focus()
}
