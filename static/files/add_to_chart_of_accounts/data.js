function checkLocation(){
    var index = document.getElementById("select_order").selectedIndex;
    var options = document.getElementById("select_order").options;
    var text = options[index].text;
    var value = options[index].value;
    if ( text.length > (value.length + 2) )
    {
        document.getElementById("warning_cover").style.width= "100%";
        document.body.style.overflow = "hidden";
        document.getElementById("warning_div").style.display= "block";
    }else {
        if(checkSelectAccounts()) {
            document.getElementById("true_false").value = "false";
            document.getElementById("submit_add").click();
        }
    }
}
function closeWarning() {
    document.getElementById("warning_cover").style.width= "0%";
    document.body.style.overflow = "";
    document.getElementById("warning_div").style.display= "none";
}
function submitTrue(){
    closeWarning()
    if(checkSelectAccounts()) {
        document.getElementById("true_false").value = "true";
        document.getElementById("submit_add").click();
    }
}
function checkSelectAccounts(){
    var value = document.getElementById("select_accounts").value;
    if(value === "") {
        document.getElementById("error_message").style.display = "block";
        return false
    }else{
        document.getElementById("error_message").style.display = "none";
        return true
    }
}
function changeMessage(){
    var value = document.getElementById("select_accounts").value;
    if(value === ""){
        document.getElementById("error_message").style.display = "block";
    }else{
        document.getElementById("error_message").style.display = "none";
    }
}