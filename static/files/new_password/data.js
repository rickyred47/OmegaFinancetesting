var num = false;
var cap = false;
var spec = false;
var match = true;
var char = false;

function validPassword() {
	document.getElementById("error_message").style.display = "none"
    num = false;
	cap = false;
	spec = false;
	var pattern = new RegExp(/[\s~`!@#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?()\._]/g);
	var input = document.getElementById("password1_input").value;
	if(input.length >= 8){
		document.getElementById("password8char").style.color = "green";
		char = true;
	}
	else{
		document.getElementById("password8char").style.color = "red";
		char = false;
	}
	for(var x = 0; x < input.length; x++){
		var character = input.charAt(x);
		if(/^\d+$/.test(character)){
			num = true;
		}
		else if(pattern.test(character)){
			spec = true;
		}
		else if(character === character.toUpperCase()){
			cap = true;
		}
	}
	if(cap){
		document.getElementById("passwordcap").style.color = "green";
	}
	else{
		document.getElementById("passwordcap").style.color = "red";
	}

	if(num){
		document.getElementById("passwordnum").style.color = "green";
	}
	else{
		document.getElementById("passwordnum").style.color = "red";
	}

	if(spec){
		document.getElementById("passwordspec").style.color = "green";
	}
	else{
		document.getElementById("passwordspec").style.color = "red";
	}

	passwordMatch();
	if(num && spec && cap && match && char){
		document.getElementById("error_message2").style.display = "none";
	}
}

function passwordMatch() {
	var password1 = document.getElementById("password1_input").value;
	var password2 = document.getElementById("password2_input").value;
	if(password1===password2){
		document.getElementById("passwordmatch").style.color = "green";
		match = true;
	}
	else{
		document.getElementById("passwordmatch").style.color = "red";
		match = false;
	}
}
function checkValid(){
	if(num && spec && cap && match && char){
		document.getElementById("submit_btn").click();
	}else{
		document.getElementById("error_message2").style.display = "block";
	}
}
