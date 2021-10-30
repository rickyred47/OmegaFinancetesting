function accounts_search() {
    var input, filter, table, tr, td, i, txtValue;
    var choice = document.getElementById("search_options").options.selectedIndex;
  input = document.getElementById("search_input");
  filter = input.value.toUpperCase();
  table = document.getElementById("accounts_table");
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
  var table, tr, i, txtValueCat, txtValueSub, txtValueSta, td2, td8, td3;
  var category = document.getElementById("accountcat_input").value;
  var subcategory = document.getElementById("accountsubcat_input").value;
  var status = document.getElementById("accountstatus_input").value;
  table = document.getElementById("accounts_table");
  tr = table.getElementsByTagName("tr");
  if(category === "All") {
    category = "";
  }
  if(subcategory === "All") {
    subcategory = "";
  }
  if(status === "All") {
    status = "";
  }
  category = category.toUpperCase();
  subcategory = subcategory.toUpperCase();
  status = status.toUpperCase();
  for (i = 0; i < tr.length; i++) {
      td2 = tr[i].getElementsByTagName("td")[2];
      td8 = tr[i].getElementsByTagName("td")[8];
      td3 = tr[i].getElementsByTagName("td")[3];
      if (td2 && td8 && td3) {
        txtValueCat = td2.textContent || td2.innerText;
        txtValueSub = td3.textContent || td3.innerText;
        txtValueSta = td8.textContent || td8.innerText;
        if (txtValueCat.toUpperCase().indexOf(category) > -1 && txtValueSub.toUpperCase().indexOf(subcategory) > -1 && txtValueSta.toUpperCase().indexOf(status) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}


