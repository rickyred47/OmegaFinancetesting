function validPassword() {
    var num = false;
	var cap = false;
	var spec = false;
	var pattern = new RegExp(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/);
	var input = document.getElementById("password1_input").value;
	if(input.length >= 8){
		document.getElementById("password8char").style.color = "green";
	}
	else{
		document.getElementById("password8char").style.color = "red";
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
}

function passwordMatch() {
	var password1 = document.getElementById("password1_input").value;
	var password2 = document.getElementById("password2_input").value;
	if(password1===password2){
		document.getElementById("passwordmatch").style.color = "green";
	}
	else{
		document.getElementById("passwordmatch").style.color = "red";
	}
}