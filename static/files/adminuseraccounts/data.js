function showpopup(user) {
    min_date_today();
    document.getElementById("user_name").innerText=user;
    document.getElementById("user").value=user;
    document.getElementById("cover").style.width = "100%";
    document.getElementById("popup_suspension").style.display = "block";
}

function closepopup() {
    document.getElementById("cover").style.width="0%";
    document.getElementById("popup_suspension").style.display = "none"
}

function min_date_today() {
    const d = new Date();
    let day = d.getDate();
    let month = d.getMonth();
    month = month+1;
    let year = d.getFullYear();
    let date;
    if (month < 10) {
	    if(day < 10) {
            date = "" + year + "-0" + month + "-0" + day;
        }else{
            date = "" + year + "-0" + month + "-" + day;
        }
    }
    else {
	    if(day < 10){
            date = "" + year + "-" + month + "-0" + day;
        }else {
            date = "" + year + "-" + month + "-" + day;
        }
    }
    document.getElementById("date_start").min = date;
    document.getElementById("date_end").min = date;
}

function correct_date_range() {
    let start = document.getElementById("date_start").value;
    let end = document.getElementById("date_end").value;
    if(start === "") {
        min_date_today();
    }
    else {
        document.getElementById("date_end").min = start;
    }
    if(end === "") {
        document.getElementById("date_start").max = "";
    }
    else {
        document.getElementById("date_start").max = end;
    }
}

function required_dates() {
    if(document.getElementById("Range").checked === true){
        document.getElementById("date_start").required = true;
        document.getElementById("date_end").required = true;
    }
    else {
        document.getElementById("date_start").required = false;
        document.getElementById("date_end").required = false;
    }
}