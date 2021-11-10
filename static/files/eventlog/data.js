function filter() {
  var table, tr, i, td1, txtValueDate;
  var date_start = document.getElementById("start_date").value;
  var date_end = document.getElementById("end_date").value;
  const start_date = new Date(date_start.substr(0,4), date_start.substr(5,2), date_start.substr(8,2));
  const end_date = new Date(date_end.substr(0,4), date_end.substr(5,2), date_end.substr(8,2));
  table = document.getElementById("events_table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[1];
    txtValueDate = td1.textContent || td1.innerText;
    const date = new Date(txtValueDate.substr(0,4), txtValueDate.substr(5,2), txtValueDate.substr(8,2));
    if (start_date <= date && date <= end_date) {
        tr[i].style.display = "";
        }
    else {
        tr[i].style.display = "none";
        }
    }
  }