function filter() {
    var table, tr, txtValue, td0;
    var start_date = document.getElementById("start_date").value;
    var end_date = document.getElementById("end_date").value;
    const s_date = new Date(start_date.substr(0,4), start_date.substr(5,2), start_date.substr(8,2));
    const e_date = new Date(end_date.substr(0,4), end_date.substr(5,2), end_date.substr(8,2));
    table = document.getElementById("account_table");
    tr = table.getElementsByTagName("tr");
    for(var i = 0; i < tr.length; i++){
        td0 = tr[i].getElementsByTagName("td")[0];
        if (td0) {
            txtValue = td0.textContent || td0.innerText;
            const contentDate = new Date(txtValue.substr(0, 4), txtValue.substr(5, 2), txtValue.substr(8, 2));
            if (s_date <= contentDate && contentDate <= e_date) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}