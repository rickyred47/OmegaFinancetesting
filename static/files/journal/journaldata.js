let debit_counter = 0;
let credit_counter =  0;

function show_journal_entry(){
    document.getElementById("journal_entry").style.display = "block";
}
function close_journal_entry(){
    document.getElementById("clear").click();
    document.getElementById("journal_entry").style.display = "none";
}
function add_account_input(type){
  var select_name = "" + type + "_account";
  var select_name_div = "" + type + "_accounts_div"
  var amount_name = "" + type + "_amount";
  var amount_name_input = "" + type + "_amount_input";
  var select_input = document.getElementById(select_name);
  var amount_input = document.getElementById(amount_name_input);
  var padding = parseInt(document.getElementById("credit_amount").style.paddingTop, 10);
  padding = padding + 30;
  var padding1 = "" + padding + "px";
  var cln = select_input.cloneNode(true);
  var cln1 = amount_input.cloneNode(true);
  document.getElementById(select_name_div).appendChild(cln);
  document.getElementById(amount_name).appendChild(cln1);
  if(type === 'debit') {
      debit_counter++;
      var name = "" + type + "_account_select" + debit_counter;
      var name2 = "" + type + "_account_amount" + debit_counter;
      cln.setAttribute("id", name);
      cln1.setAttribute("id", name2);
      document.getElementById("credit_amount").style.paddingTop = padding1;
      cln1.style.height = "30px";
  }else if(type === 'credit') {
      credit_counter++;
      var name1 = "" + type + "_account_select" + credit_counter;
      var name3 = "" + type + "_account_amount" + credit_counter;
      cln.setAttribute("id",name1);
      cln1.setAttribute("id", name3);
      cln1.style.height = "30px";
  }
}
function delete_account_input(type){
    if(type === 'debit') {
        if (debit_counter > 0) {
            var name = "" + type + "_account_select" + debit_counter;
            var name2 = "" + type + "_account_amount" + debit_counter;
            var select_input = document.getElementById(name);
            var amount_input = document.getElementById(name2);
            var pad = parseInt(document.getElementById("credit_amount").style.paddingTop, 10);
            pad = pad - 30;
            document.getElementById("credit_amount").style.paddingTop = "" + pad + "px";
            select_input.remove();
            amount_input.remove();
            debit_counter--;
        }
    }else if(type === 'credit') {
        if(credit_counter > 0){
            var name1 = "" + type + "_account_select" + credit_counter;
            var name3 = "" + type + "_account_amount" + credit_counter;
            var select_input1 = document.getElementById(name1);
            var amount_input1 = document.getElementById(name3);
            select_input1.remove();
            amount_input1.remove();
            credit_counter--;
        }
    }
}