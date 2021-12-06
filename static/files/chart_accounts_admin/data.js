function accounts_search() {
    var input, filter, table, tr, td, i, txtValue;
    var choice = document.getElementById("search_options").options.selectedIndex;
  input = document.getElementById("search_input");
  filter = input.value.toUpperCase();
  table = document.getElementById("chart_accounts_table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[choice];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function filter() {
  var table, tr, i, txtValueCat, txtValueSub, td2, td3, td6, txtValueDate;
  var category = document.getElementById("select_category").value;
  var subcategory = document.getElementById("subcategory_select_filter").value;
  var date_start = document.getElementById("start_date").value;
  var date_end = document.getElementById("end_date").value;
  const start_date = new Date(date_start.substr(0,4), date_start.substr(5,2), date_start.substr(8,2))
  const end_date = new Date(date_end.substr(0,4), date_end.substr(5,2), date_end.substr(8,2))
  table = document.getElementById("chart_accounts_table");
  tr = table.getElementsByTagName("tr");
  if(category === "All") {
    category = "";
  }
  if(subcategory === "All") {
    subcategory = "";
  }
  category = category.toUpperCase();
  subcategory = subcategory.toUpperCase();
  for (i = 0; i < tr.length; i++) {
      td2 = tr[i].getElementsByTagName("td")[2];
      td3 = tr[i].getElementsByTagName("td")[3];
      td6 = tr[i].getElementsByTagName("td")[6];
      if (td2 && td6 && td3) {
        txtValueCat = td2.textContent || td2.innerText;
        txtValueSub = td3.textContent || td3.innerText;
        txtValueDate = td6.textContent || td6.innerText;
        const date = new Date(txtValueDate.substr(0,4), txtValueDate.substr(5,2), txtValueDate.substr(8,2));
        if (txtValueCat.toUpperCase().indexOf(category) > -1 && txtValueSub.toUpperCase().indexOf(subcategory) > -1 &&
            start_date <= date && date <= end_date) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}


