
function checkWholeForm(theForm) {
   var why = "";
   why += checkUsername(theForm.N.value);
   why += checkDropdown(theForm.selMonth.selectedIndex, "Birthday - Month");
   why += checkDropdown(theForm.selDay.selectedIndex, "Birthday - Day");
   why += checkDropdown(theForm.selYear.selectedIndex, "Birthday - Year");
   why += checkDropdown(theForm.G.selectedIndex, "I am a");
   why += checkDropdown(theForm.A1.selectedIndex, "Seeking a");
   why += checkZipCode(theForm.A2.value);
   why += checkDropdown(theForm.A8.selectedIndex, "My Occupation");
   why += checkDropdown(theForm.A7.selectedIndex, "My Ethnicity");
   why += checkDropdown(theForm.A3.selectedIndex, "My Hair");
   why += checkDropdown(theForm.A5.selectedIndex, "My Body Type");
   why += checkDropdown(theForm.A6.selectedIndex, "My Height - Feet");
   why += checkDropdown(theForm.A12.selectedIndex, "My Height - Inches");
   why += checkDropdown(theForm.A9.selectedIndex, "My Drinking Behavior");
   why += checkDropdown(theForm.A10.selectedIndex, "My Smoking Behavior");
   why += checkDropdown(theForm.A11.selectedIndex, "Relationship Status");
   why += isEmpty(theForm.AS1.value, "About me", 120);
   if (why != "") {
      alert(why);
   } else {
      theForm.method="get";
      theForm.target="_self";
      theForm.action="matchweb";
      theForm.submit();
   }
}

// phone number - strip out delimiters and check for 10 digits
function checkPhone (strng) {
var error = "";
if (strng == "") {
   error = "You didn't enter a phone number.\n";
}
var stripped = strng.replace(/[\(\)\.\-\ ]/g, ''); //strip out acceptable non-numeric characters
   if (isNaN(parseInt(stripped))) {
      error = "The phone number contains illegal characters.";

   }
   if (!(stripped.length == 10)) {
error = "The phone number is the wrong length. Make sure you included an area code.\n";
   } 
return error;
}

// zip - between 4-5 numeric chars
function checkZipCode (strng) {
   var error = "";
   var legalChars = /[0-9]{4,5}/; // allow only letters and numbers

   if (strng == "") {
      error = "You didn't enter a Zip Code.\n";
   }
   else if ((strng.length < 4) || (strng.length > 5)) {
      error = "The Zip Code is the wrong length.\n";
   }
   else if (!legalChars.test(strng)) {
     error = "The Zip Code contains illegal characters.\n";
   } 
return error;    
} 

// username - 1-16 chars, uc, lc, numbers and underscore only.
function checkUsername (strng) {
   var error = "";
   var illegalChars = /\W/; // allow letters, numbers, and underscores
   if (strng == "") {
      error = "You didn't enter a username.\n";
   } else if ((strng.length < 1) || (strng.length > 16)) {
      error = "The username is the wrong length.\n";
   }
   else if (illegalChars.test(strng)) {
   error = "The username contains illegal characters (use only letters, numbers, and underscores).\n";
   } 
return error;
}       
// non-empty textbox
function isEmpty(strng, fieldName, maxLen) {
var error = "";
  if (strng.length == 0) {
    error = "The " + fieldName + " text area has not been filled in.\n"
  } 
  if (strng.length > maxLen) {
    error = "The " + fieldName + " text area should not have more than 120 characters.\n"
  }
return error;  
}

// valid selector from dropdown list
function checkDropdown(choice, fieldName) {
var error = "";
   if (choice == 0) {
   error = "You didn't choose " + fieldName + " from the drop-down list.\n";
   }    
return error;
}

function CheckNumeric()
{
   // Get ASCII value of key that user pressed
   var key = window.event.keyCode;
   // Was key that was pressed a numeric character (0-9)?
   if ( key > 47 && key < 58 )
     return; // if so, do nothing
   else
     window.event.returnValue = null; // otherwise, 
                        // discard character
}

function CheckAlphaNumericUnderScore()
{
   // Get ASCII value of key that user pressed
   var key = window.event.keyCode;
   if ((key > 47 && key < 58) || (key > 64 && key < 91) || (key > 96 && key < 123) || key == 95 )
     return; // if so, do nothing
   else 
     window.event.returnValue = null; // otherwise, 
                        // discard character
}

function checkMobileForm(theForm) {
   var why = "";
   why += checkMobileNo(theForm.MSISDN.value);
   if (why != "") {
      alert(why);
   } else {
      theForm.method="post";
      theForm.target="_self";
      theForm.action="reg";
      theForm.submit();
   }
}

// username - 10 chars, numbers only.
function checkMobileNo (strng) {
   var error = "";
   var illegalChars = /\D/; // allow letters, numbers, and underscores
   if (strng == "") {
      error = "You didn't enter a phone number.\n";
   } else if (strng.length != 10) {
      error = "The phone number is the wrong length (should be 10 digits).\n";
   }
   else if (illegalChars.test(strng)) {
   error = "The phone number contains illegal characters (use only digits).\n";
   } 
return error;
}       
