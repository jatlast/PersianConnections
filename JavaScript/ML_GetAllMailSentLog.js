// This is the function that performs form verification. It will be invoked
// from the onSubmit() event handler. The handler should return whatever
// value this function returns.
function checkForm(myForm)
{
	if(!isNum(myForm.min_value.value))
	{
		alert("You must enter a valid Min number");
	    myForm.min_value.focus();
		return (false);
	}

	if(!isNum(myForm.max_value.value))
	{
		alert("You must enter a valid Max number");
	    myForm.max_value.focus();
		return (false);
	}

	if(myForm.min_value.value > myForm.max_value.value)
	{
		alert("Error:  Min > Max");
	    myForm.min_value.focus();
		return (false);
	}
	return (true);
}

// isNum
function isNum(passedVal)
{
//	alert("within isNum")
	if(passedVal == "")
	{
		return (false);
	}
	for(i=0; i<passedVal.length; i++)
	{
		if(passedVal.charAt(i) < "0")
		{
			return (false);
		}
		if(passedVal.charAt(i) > "9")
		{
			return (false);
		}
	}
	return (true);
}

// setMinValueWithRadioValue
function setMinValueWithRadioValue(myForm)
{	
	var return_value = -1;
	for(var i=0; i<myForm.unique_id_min.length; i++)
	{
		if (myForm.unique_id_min[i].checked)
		{
			return_value = i;
			document.FormOne.min_value.value = myForm.unique_id_min[i].value;
		}
	}

	if(return_value < 0)
	{
		alert("Error setting unique_id min value.");
	}
}

// setMaxValueWithRadioValue
function setMaxValueWithRadioValue(myForm)
{	
	var return_value = -1;
	for(var i=0; i<myForm.unique_id_max.length; i++)
	{
		if (myForm.unique_id_max[i].checked)
		{
			return_value = i;
			document.FormOne.max_value.value = myForm.unique_id_max[i].value;
		}
	}

	if(return_value < 0)
	{
		alert("Error setting unique_id max value.");
	}
}

