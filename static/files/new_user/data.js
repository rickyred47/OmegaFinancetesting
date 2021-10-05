// JavaScript Document
function validPassword() {
	var num = false;
	var cap = false;
	var spec = false;
	var pattern = new RegExp(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/);
	var input = document.getElementById("psswrdtxt_input").value;
	if(input.length >= 8){
		document.getElementById("psswrd8char").style.color = "green";
		document.getElementById("check8char").style.visibility = "visible";
	}
	else{
		document.getElementById("psswrd8char").style.color = "red";
		document.getElementById("check8char").style.visibility = "hidden";
	}
	for(var x = 0; x < input.length; x++){
		var charcater = input.charAt(x);
		if(/^\d+$/.test(charcater)){
			num = true;
		}
		else if(pattern.test(charcater)){
			spec = true;
		}
		else if(charcater == charcater.toUpperCase()){
			cap = true;
		}
	}
	if(cap){
		document.getElementById("psswrdcap").style.color = "green";
		document.getElementById("checkcap").style.visibility = "visible";
	}
	else{
		document.getElementById("psswrdcap").style.color = "red";
		document.getElementById("checkcap").style.visibility = "hidden";
	}
	
	if(num){
		document.getElementById("psswrdnumlbl").style.color = "green";
		document.getElementById("checknum").style.visibility = "visible";
	}
	else{
		document.getElementById("psswrdnumlbl").style.color = "red";
		document.getElementById("checknum").style.visibility = "hidden";
	}
	
	if(spec){
		document.getElementById("psswrdspecharlbl").style.color = "green";
		document.getElementById("checkspechar").style.visibility = "visible";
	}
	else{
		document.getElementById("psswrdspecharlbl").style.color = "red";
		document.getElementById("checkspechar").style.visibility = "hidden";
	}
		
}

function passwordMatch() {
	var password1 = document.getElementById("psswrdtxt_input").value;
	var password2 = document.getElementById("repsswrdtxtbx_input").value;
	if(password1==password2){
		document.getElementById("psswrdmatchlbl").style.color = "green";
	}
	else{
		document.getElementById("psswrdmatchlbl").style.color = "red";
	}
}

function passwordPassed() {
	var num = false;
	var length = false
	var cap = false;
	var spec = false;
	var pattern = new RegExp(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/);
	var input = document.getElementById("psswrdtxt_input").value;
	if(input.length >= 8){
		length = true;
	}
	
	for(var x = 0; x < input.length; x++){
		var charcater = input.charAt(x);
		if(/^\d+$/.test(charcater)){
			num = true;
		}
		else if(pattern.test(charcater)){
			spec = true;
		}
		else if(charcater == charcater.toUpperCase()){
			cap = true;
		}
	}
	var matched = false;
	var password1 = document.getElementById("psswrdtxt_input").value;
	var password2 = document.getElementById("repsswrdtxtbx_input").value;
	if(password1==password2){
		matched=true;
	}
	
	if(!(num && cap && spec && length)){
		alert("The password is not valid")
	}
	else if(!matched){
		alert("The passwords do not matched")
	}
	
}
function clearPage() {
	document.getElementById("firstname_input").value = "";
	document.getElementById("lastname_input").value = "";
	document.getElementById("emailtxtbx_input").value = "";
	document.getElementById("psswrdtxt_input").value = "";
	document.getElementById("repsswrdtxtbx_input").value = "";
	document.getElementById("streetaddress_input").value = "";
	document.getElementById("aptnum_input").value = "";
	document.getElementById("zipcodetxt_input").value = "";
	document.getElementById("dobtxt_input").value = "";
	document.getElementById("psswrdmatchlbl").style.color = "red";
	document.getElementById("psswrdspecharlbl").style.color = "red";
	document.getElementById("checkspechar").style.visibility = "hidden";
	document.getElementById("psswrdnumlbl").style.color = "red";
	document.getElementById("checknum").style.visibility = "hidden";
	document.getElementById("psswrdcap").style.color = "red";
	document.getElementById("checkcap").style.visibility = "hidden";
	document.getElementById("psswrd8char").style.color = "red";
	document.getElementById("check8char").style.visibility = "hidden";
}