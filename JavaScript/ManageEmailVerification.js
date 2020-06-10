// This file contains JavaScript for verifing the UpdateBilling.exe generated  form

function checkFormOne(theForm)
{ 
// ----- email_verification_code

  if (theForm.email_verification_code.value == "")
  {
    alert("Please enter a value for the \"Verification Code\" field.")
    theForm.email_verification_code.focus()
    return (false)
  }
return true
} // End checkFormOne function

function checkFormTwo(theForm)
{ 
// ----- new_email

  if (theForm.new_email.value == "")
  {
    alert("Please enter a value for the \"New Email Address\" field.")
    theForm.new_email.focus()
    return (false)
  }
  if (!validEmail(theForm.new_email.value))
  {
    alert("Please enter a valid \"New Email Address\" address.");
    theForm.new_email.focus();
    theForm.new_email.select();
    return (false);
  }
return true
} // End checkFormTwo function

function validEmail(email)
{
invalidChars = " /:,;"

    // email cannot be empty...
    if(email == "")
    {
        return false
    }

    // does it contain any invalid characters...
    for (i=0; i<invalidChars.length; i++)
    {
        badChar = invalidChars.charAt(i)
        if (email.indexOf(badChar, 0) > -1)
        {
            return false
        }
    }

    // there must be one "@" symbol...
    atPos = email.indexOf("@",1)
    if (atPos == -1)
    {
        return false
    }

    // and only one "@" symbol...
    if (email.indexOf("@", atPos+1) != -1)
    {
        return false
    }

    // and at least one "." after the "@"...
    periodPos = email.indexOf(".", atPos)
    if (periodPos == -1)
    {
        return false
    }

    // must be at least 2 characters after the "."...
    if (periodPos+3 > email.length)
    {
        return false
    }
return true
}

function newWindowGeneric(picName) 
{
		var myWindow = window.open(picName, 'CVV2Info', 'toolbar=no,location=no,scrollbars=yes,resizable=yes,width=600,height=800')
		myWindow.focus()
}


