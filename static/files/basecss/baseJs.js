function showReports(){
    var links = document.getElementsByClassName("nav_reports_links");
    for(var i = 0; i < links.length; i++){
        links[i].style.display = "block";
    }
}

function hideReports(){
    var links = document.getElementsByClassName("nav_reports_links");
    for(var j = 0; j < links.length; j++){
        links[j].style.display = "none";
    }
}