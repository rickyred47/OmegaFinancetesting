
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
    var div_children, new_select_id_name, new_minus_id, div_id, new_div_id, div_amount_id, column_id;
    var new_div_amount_id, new_amount_input_id_name;
    if(type === 'debit'){
        div_id = "" + type + "_accounts_div" + debit_counter;
        div_amount_id = "" + type + "_amount" + debit_counter;
    }else {
        div_id = "" + type + "_accounts_div" + credit_counter;
        div_amount_id = "" + type + "_amount" + credit_counter;
    }

    var account_div = document.getElementById(div_id);
    var credit_div_before = document.getElementById("break");
    var accounts_column = document.getElementsByTagName("td")[1];
    var cln_div = account_div.cloneNode(true);

    column_id = "" + type + "_amount_column";
    var div_amount = document.getElementById(div_amount_id);
    var cln_div_amount = div_amount.cloneNode(true);
    var column = document.getElementById(column_id);
    column.appendChild(cln_div_amount);

    if(type === 'debit'){
        debit_counter++;
        new_div_amount_id = "" + type + "_amount" + debit_counter;
        new_amount_input_id_name = "" + type + "_amount_input" + debit_counter;
        new_div_id = "" + type + "_accounts_div" + debit_counter;
        new_select_id_name= "" + type + "_account_select" + debit_counter;
        new_minus_id = "" + type + "_minus_btn" + debit_counter;
        accounts_column.insertBefore(cln_div, credit_div_before);
        cln_div.id = new_div_id;

        changeCreditPos("Add");

        set_counter_input_text(debit_counter, type);

    }else if(type ==='credit'){
        credit_counter++;
        new_div_amount_id = "" + type + "_amount" + credit_counter;
        new_amount_input_id_name = "" + type + "_amount_input" + credit_counter;
        new_div_id = "" + type + "_accounts_div" + credit_counter;
        new_select_id_name= "" + type + "_account_select" + credit_counter;
        new_minus_id = "" + type + "_minus_btn" + credit_counter;
        accounts_column.appendChild(cln_div);
        cln_div.id = new_div_id;

        set_counter_input_text(credit_counter, type);
    }

    div_children = cln_div.children;
    div_children[0].name = new_select_id_name;
    div_children[0].id = new_select_id_name;
    div_children[2].id = new_minus_id;

    cln_div_amount.id = new_div_amount_id;
    var cln_div_amount_children = cln_div_amount.children;
    cln_div_amount_children[1].name = new_amount_input_id_name;
    cln_div_amount_children[1].id = new_amount_input_id_name;
    balanced();

}


function delete_account_input(type, clicked_id){
    var number, div_id, div, div_amount_id, div_amount;
    if(type === 'debit' && debit_counter > 0){
        number = clicked_id.substr(15);
        div_id = "" + type + "_accounts_div" + number;
        div= document.getElementById(div_id);
        div.remove();
        debit_counter --;

        div_amount_id = "" + type + "_amount" + number;
        div_amount = document.getElementById(div_amount_id);
        div_amount.remove();
        changeCreditPos("Sub");

        set_counter_input_text(debit_counter, type);

    }else if(type === 'credit' && credit_counter > 0){
        number1 = clicked_id.substr(16);
        div_id= "" + type + "_accounts_div" + number1;
        div = document.getElementById(div_id);
        div.remove();
        credit_counter --;

        div_amount_id = "" + type + "_amount" + number1;
        div_amount = document.getElementById(div_amount_id);
        div_amount.remove();

        set_counter_input_text(credit_counter, type);

    }
    rename();
    balanced();

}
function rename(){
    var new_div_id, new_select_id_name, new_minus_id, column_amount_d_children, column_amount_c_children,  column_amount_d, column_amount_c;
    var d_counter = 0;
    var c_counter = 0;
    var column = document.getElementById("accounts_column");
    var column_children = column.children;
    column_amount_d = document.getElementById("debit_amount_column");
    column_amount_c = document.getElementById("credit_amount_column");
    column_amount_d_children = column_amount_d.children;
    column_amount_c_children = column_amount_c.children;
    var isDebit = true;
    for(var i = 0; i < column_children.length; i++){
        if(column_children[i].nodeName === 'BR'){
            isDebit = false;
        }else if(column_children[i].nodeName === 'DIV'){
            if(isDebit){
                column_amount_d_children[d_counter].id = "debit_amount" + d_counter;
                var div_amount_d_children = column_amount_d_children[d_counter].children;
                div_amount_d_children[1].name = "debit_amount_input" + d_counter;
                div_amount_d_children[1].id = "debit_amount_input" + d_counter;
                new_div_id = "debit_accounts_div" + d_counter;
                new_select_id_name= "debit_account_select" + d_counter;
                new_minus_id = "debit_minus_btn" + d_counter;
                d_counter ++;
            }else {
                column_amount_c_children[c_counter].id = "credit_amount" + c_counter;
                var div_amount_c_children = column_amount_c_children[c_counter].children;
                div_amount_c_children[1].name = "credit_amount_input" + c_counter;
                div_amount_c_children[1].id = "credit_amount_input" + c_counter;
                new_div_id = "credit_accounts_div" + c_counter;
                new_select_id_name= "credit_account_select" + c_counter;
                new_minus_id = "credit_minus_btn" + c_counter;
                c_counter ++;
            }
            column_children[i].id = new_div_id;
            var div_children = column_children[i].children;
            div_children[0].name = new_select_id_name;
            div_children[0].id = new_select_id_name;
            div_children[2].id = new_minus_id;
        }
    }
}
function set_counter_input_text(counter, type){
    var element_id = "" + type + "_accounts_counter";
    document.getElementById(element_id ).value = counter;
}

function selected_options(){
    var account_column = document.getElementById("accounts_column");
    var divs = account_column.children;
    var div_elements;
    for(var x = 0; x < divs.length; x++){

    }
}
function balanced(){
    var debit_amount_id, credit_amount_id, amount;
    var debit_total = 0;
    var credit_total = 0;
    for(var i = 0; i <= debit_counter; i++){
        debit_amount_id = "debit_amount_input" + i;
        amount = document.getElementById(debit_amount_id).value;
        if(amount === ""){
            amount = "0";
        }
        debit_total = debit_total + parseInt(amount);
    }
    for(var j = 0; j <= credit_counter; j++){
        credit_amount_id = "credit_amount_input" + j;
        amount = document.getElementById(credit_amount_id).value;
        if(amount === ""){
            amount = "0";
        }
        credit_total = credit_total + parseInt(amount);
    }
    if(credit_total === debit_total){
        document.getElementById("balanced_error").style.display = "none";
        document.getElementById("submit").disabled = false;
        for(var k = 0; k <= debit_counter; k++){
            debit_amount_id = "debit_amount_input" + k;
            document.getElementById(debit_amount_id).style.boxShadow = "0px 0px 10px green";
        }
        for(var l = 0; l <= credit_counter; l++){
            credit_amount_id = "credit_amount_input" + l;
            document.getElementById(credit_amount_id).style.boxShadow = "0px 0px 10px green";
        }

    }else {
        document.getElementById("balanced_error").style.display = "";
        document.getElementById("submit").disabled = true;
        for(var m = 0; m <= debit_counter; m++){
            debit_amount_id = "debit_amount_input" + m;
            document.getElementById(debit_amount_id).style.boxShadow = "0px 0px 10px red";
        }
        for(var n = 0; n <= credit_counter; n++){
            credit_amount_id = "credit_amount_input" + n;
            document.getElementById(credit_amount_id).style.boxShadow = "0px 0px 10px red";
        }
    }
}
function filter(){
    var table, tr, txtValueStatus,td7, i, txtDateValue, td0;
    var status = document.getElementById("select_status").value;
    var start_date = document.getElementById("start_date").value;
    var end_date = document.getElementById("end_date").value;
    const s_date = new Date(start_date.substr(0,4), start_date.substr(5,2), start_date.substr(8,2));
    const e_date = new Date(end_date.substr(0,4), end_date.substr(5,2), end_date.substr(8,2));
    table = document.getElementById("journal_table");
    tr = table.getElementsByTagName("tr");
    if(status === "All"){
        status = "";
    }
    status = status.toUpperCase();
    for(i = 0; i < tr.length; i++){
        td7 = tr[i].getElementsByTagName("td")[14];
        td0 = tr[i].getElementsByTagName("td")[0];
        if(td7 && td0){
            var td_p = td7.children;
            txtValueStatus = td_p[0].textContent || td_p[0].innerText;
            txtDateValue = td0.textContent || td0.innerText;
            const contentDate = new Date(txtDateValue.substr(0,4), txtDateValue.substr(5,2), txtDateValue.substr(8,2));
            if(txtValueStatus.toUpperCase().indexOf(status) > -1 && s_date <= contentDate && contentDate <= e_date){
                tr[i].style.display = "";
            }else {
                tr[i].style.display = "none";
            }
        }
    }
}
function showComment(event) {
    document.getElementById("background_reason").style.display = "block";
    document.getElementById("cover").style.width = "300%";
    document.getElementById("cover").style.height = "300%";
    document.body.style.overflow = "hidden";

}
function hideComment() {
    document.getElementById("background_reason").style.display = "none";
    document.getElementById("cover").style.width = "0%";
    document.getElementById("cover").style.height = "0%";
    document.body.style.overflow = "";
}
function submitInfo() {
    hideComment();
    document.getElementById("reason_text_form").value = document.getElementById("reason_text_area").value;
    document.getElementById("reject_btn").click();
}
function clearInfo() {
    var div_id, div, amount_id, div_amount;
    for(var i = 0; debit_counter >= 1; --debit_counter){
        div_id = "debit_accounts_div" + debit_counter;
        amount_id = "debit_amount" + debit_counter;
        div = document.getElementById(div_id);
        div.remove();
        div_amount = document.getElementById(amount_id);
        div_amount.remove();
        changeCreditPos("Sub");
    }
    for(i = 0; credit_counter >= 1; --credit_counter){
        div_id = "credit_accounts_div" + credit_counter;
        amount_id = "credit_amount" + credit_counter;
        div = document.getElementById(div_id);
        div.remove();
        div_amount = document.getElementById(amount_id);
        div_amount.remove();
    }
    document.getElementById("debit_accounts_div0").value = "";
    document.getElementById("credit_accounts_div0").value = "";
    document.getElementById("clear_btn").click();

   const now = new Date();
		let now_day = now.getDate();
		let now_month = now.getMonth();
		now_month = now_month + 1;
		let year = now.getFullYear();
		let date;
		if (now_month < 10) {
			if(now_day < 10) {
				date = "" + year + "-0" + now_month + "-0" + now_day;
			} else {
				date = "" + year + "-0" + now_month + "-" + now_day;
			}
		}
		else {
			if(now_day < 10){
				date = "" + year + "-" + now_month + "-0" + now_day;
			} else {
				date = "" + year + "-" + now_month + "-" + now_day;
			}
		}
		document.getElementById("journal_date").min = date;
		document.getElementById("journal_date").value = date;

   document.getElementById("balanced_error").style.display = "none";
   document.getElementById("submit").disabled = true;
   document.getElementById("debit_amount_input0").style.boxShadow = "";
   document.getElementById("credit_amount_input0").style.boxShadow = "";

   clearSelect();
}
function changeCreditPos(addSub){
    var padding = document.getElementById("credit_amount_column").style.paddingTop;
    var padding_num = parseInt(padding, 10);
    if(addSub === "Add"){
        padding_num = padding_num + 30;
    } else if(addSub === "Sub"){
        padding_num = padding_num - 30;
    }
    padding = "" + padding_num + "px";
    document.getElementById("credit_amount_column").style.paddingTop = padding;
}
