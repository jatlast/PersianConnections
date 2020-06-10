// This file contains JavaScript for verifing the UpdateAbout.exe generated form

function checkForm(theForm)
{

// ----- screen_quote
  if (!validParagraph(theForm.screen_quote.value, 5))
  {
    alert("Please enter a polite sentence or so into the \"Screen Quote\" field.");
    theForm.screen_quote.focus();
    return (false);
  }

// ----- about_yourself
  if (!validParagraph(theForm.about_yourself.value, 20))
  {
    alert("Please enter a polite paragraph or so into the \"About Yourself\" field.");
    theForm.about_yourself.focus();
    return (false);
  }

  return (true)
}

function validParagraph(string_to_test, minimum_words_allowed)
{
	var StringToTest_b = new String(string_to_test)
	var StringToTest_s = new String(string_to_test)
	var StingToTest_b_Array = new Array(1) 
	var StingToTest_s_Array = new Array(1) 
	StingToTest_b_Array = StringToTest_b.split(/\b/)
	StingToTest_s_Array = StringToTest_s.split(/\s/)

	if(StingToTest_s_Array.length < minimum_words_allowed)
	{
		alert("You must enter at least " + minimum_words_allowed + " words.");
		return (false);
	}
	else
	{
		for(var index = 0; index < StingToTest_b_Array.length; index++)
		{
		  if (checkForInvalidWords(StingToTest_b_Array[index]))
		  {
			alert("the word " + StingToTest_b_Array[index] + " is not allowed.");
			return (false);
		  }
		}

		for(var index = 0; index < StingToTest_s_Array.length; index++)
		{
			if (StingToTest_s_Array[index].length > 34)
			  {
				alert("the word " + StingToTest_s_Array[index] + " is too long.");
				return (false);
			  }
		}
	}
  return (true)
}

function checkForInvalidWords(word_to_test)
{
	var BadWord_Array = new Array("ass")
	BadWord_Array.push("cock");
	BadWord_Array.push("cocks");
	BadWord_Array.push("cos");
	BadWord_Array.push("cunt");
	BadWord_Array.push("cunts");
	BadWord_Array.push("dick");
	BadWord_Array.push("dicks");
	BadWord_Array.push("fuck");
	BadWord_Array.push("fucking");
	BadWord_Array.push("fucker");
	BadWord_Array.push("fucked");
	BadWord_Array.push("jende");
	BadWord_Array.push("kir");
	BadWord_Array.push("kos");
	BadWord_Array.push("oral");
	BadWord_Array.push("piss");
	BadWord_Array.push("pissing");
	BadWord_Array.push("pussies");
	BadWord_Array.push("pussy");
	BadWord_Array.push("shit");
	BadWord_Array.push("slut");
	BadWord_Array.push("sluts");
	BadWord_Array.push("whore");
	BadWord_Array.push("whores");

	for(var index = 0; index < BadWord_Array.length; index++)
	{
	  if (word_to_test == BadWord_Array[index])
	  {
		return (true);
	  }
	}
  return (false)
}

function back()
{
	window.history.back()
}
