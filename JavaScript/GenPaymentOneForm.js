// This file contains JavaScript for confirming the Authorize.Net membership form
// and is used by GenAuthorizeNetForm.cgi

function modifyText(id, text) 
	{
		if(document.getElementById && text != '') 
		{
			obj = document.getElementById(id);
			obj.childNodes[0].data = text;
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

  return ( finalConfirm(theForm) )
} // End checkFormFunction

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
  if(months == 1)
  {
     MembershipName = "1 Month Premium"
  }
  if(months == 3)
  {
     MembershipName = "3 Month Premium"
  }
  if(months == 6)
  {
     MembershipName = "6 Month Premium"
  }

  if( confirm("Do you wish to pay for your " + MembershipName + " membership using your telephone bill?\n\nNote:\n\tIf you chose 'OK' a dialog box will appear.\n\tJust choose 'Open' then follow the simple\n\tinstructions provided by our Phone Billing application.") )
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
