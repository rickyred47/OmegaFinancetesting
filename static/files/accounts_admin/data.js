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