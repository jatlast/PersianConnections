// Jump between telephone number fields...var isNN = (navigator.appName.indexOf("Netscape")!=-1);
function autoTab(input, len, e) 
{
	var keyCode = (isNN) ? e.which : e.keyCode;
	var filter = (isNN) ? [0,8,9] : [0,8,9,16,17,18,37,38,39,40,46];
	if(input.value.length >= len && !containsElement(filter,keyCode)) 
	{
		input.value = input.value.slice(0, len);
		input.form[(getIndex(input)+1) % input.form.length].focus();
	}
	
	function containsElement(arr, ele) 
	{
		var found = false, index = 0;
		while(!found && index < arr.length)
		if(arr[index] == ele)
		found = true;
		else
		index++;
		return found;
	}
	
	function getIndex(input) 
	{
		var index = -1, i = 0, found = false;
		while (i < input.form.length && index == -1)
		if (input.form[i] == input)index = i;
		else i++;
		return index;
	}
	return true;
}

function checkPhoneFields(theForm)
{
   var why = "";

// ----- phone1
   why += isEmpty(theForm.phone1.value, "First Three Digits", 3, 3);
   why += checkPhone(theForm.phone1.value);

// ----- phone2
   why += isEmpty(theForm.phone2.value, "Second Three Digits", 3, 3);
   why += checkPhone(theForm.phone2.value);

// ----- phone3
   why += isEmpty(theForm.phone3.value, "Last Four Digits", 4, 4);
   why += checkPhone(theForm.phone3.value);

if (why != "") 
	{
		alert(why);
		return (false)
	} 
else 
	{
		return (true)
	}
}
  
function checkCarrierFields(theForm)
{
   var why = "";

// ----- carrier
   why += checkDropdown(theForm.carrier.selectedIndex, "your Carrier");

// ----- state
   why += checkDropdown(theForm.state.selectedIndex, "your State");

if (why != "") 
	{
		alert(why);
		return (false)
	} 
else 
	{
		return (true)
	}
}
  
function checkCCFields(theForm)
{
   var why = "";

// ----- pack
  var RadioOption = -1
  for (i=0; i<theForm.pack.length; i++)
  {
    if (theForm.pack[i].checked)
    {
       RadioOption = i
    }
  }
  if (RadioOption == -1)
  {
     why += "You must choose the number of credits you want to purchase.\n";
  }

// ----- fname
   why += isEmpty(theForm.fname.value, "First Name", 0, 32);

// ----- lname
   why += isEmpty(theForm.lname.value, "Last Name", 0, 32);

// ----- city
   why += isEmpty(theForm.city.value, "City", 0, 32);

// ----- zip
   why += checkZipCode(theForm.zip.value);

// ----- cctype
   why += checkDropdown(theForm.cctype.selectedIndex, "your Card Type");

// ----- ccn
   why += checkCCNumber(theForm.ccn.value);

// ----- exmon
   why += checkDropdown(theForm.exmon.selectedIndex, "your Expiration Month");

// ----- exyear
   why += checkDropdown(theForm.exyear.selectedIndex, "your Expiration Year");

// ----- agree
  if (!theForm.agree.checked)
  {
     why += "You must make sure your phone has 2-way text mesaging.\n";
  }

if (why != "") 
	{
		alert(why);
		return (false)
	} 
else 
	{
		return (true)
	}
}
  
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
   error = "You didn't enter a complete phone number.\n";
}
var stripped = strng.replace(/[\(\)\.\-\ ]/g, ''); //strip out acceptable non-numeric characters
   if (isNaN(parseInt(stripped))) {
      error = "The phone number contains illegal characters.\n";
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

// Credit Card Number - between 13-19 numeric chars
function checkCCNumber (strng) {
   var error = "";
   var legalChars = /[0-9]{4,5}/; // allow only letters and numbers

   if (strng == "") {
      error = "You didn't enter a Credit Card Number.\n";
   }
   else if ((strng.length < 13) || (strng.length > 19)) {
      error = "The Credit Card Number is the wrong length.\n";
   }
   else if (!legalChars.test(strng)) {
     error = "The Credit Card Number contains illegal characters.\n";
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
function isEmpty(strng, fieldName, minLen, maxLen) {
var error = "";
  if (strng.length == 0) {
    error = "The " + fieldName + " text area has not been filled in.\n"
  } 
  if (strng.length > maxLen) {
    error = "The " + fieldName + " text area should not have more than " + maxLen + " characters.\n"
  }
  if (strng.length < minLen) {
    error = "The " + fieldName + " text area should have " + minLen + " characters.\n"
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

