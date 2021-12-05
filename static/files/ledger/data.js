function filter() {
    var table, tr, txtValue, td0, td3, td4, td5, txtDebit, txtCredit, txtBalance;
    var inDebit, inCredit, inBalance;
    var start_date = document.getElementById("start_date").value;
    var end_date = document.getElementById("end_date").value;
    var start_amount = document.getElementById("start_amount").value;
    var end_amount = document.getElementById("end_amount").value;
    const s_date = new Date(start_date.substr(0,4), start_date.substr(5,2), start_date.substr(8,2));
    const e_date = new Date(end_date.substr(0,4), end_date.substr(5,2), end_date.substr(8,2));
    table = document.getElementById("account_table");
    tr = table.getElementsByTagName("tr");
    for(var i = 0; i < tr.length; i++){
        td0 = tr[i].getElementsByTagName("td")[0];
        td3 = tr[i].getElementsByTagName("td")[3];
        td4 = tr[i].getElementsByTagName("td")[4];
        td5 = tr[i].getElementsByTagName("td")[5];
        if (td0 && td3 && td4 && td5) {
            txtValue = td0.textContent || td0.innerText;
            txtDebit = td3.textContent || td3.innerText;
            txtCredit = td4.textContent || td4.innerText;
            txtBalance = td5.textContent || td5.innerText;
            if(txtDebit === ""){
                inDebit = false;
            }else{
                inDebit = amountChoice(start_amount, end_amount, txtDebit);
            }
            if(txtCredit === ""){
                inCredit = false;
            }else{
                inCredit = amountChoice(start_amount, end_amount, txtCredit);
            }
            if(txtBalance === ""){
                inBalance = false;
            }else{
                inBalance = amountChoice(start_amount, end_amount, txtBalance);
            }
            const contentDate = new Date(txtValue.substr(0, 4), txtValue.substr(5, 2), txtValue.substr(8, 2));
            if (s_date <= contentDate && contentDate <= e_date && (inDebit || inCredit || inBalance)) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
function amountChoice(start, end, amount) {
    var start_num, end_num;
    var amount_num = parseInt(removeSymbols(amount));
    if(start === "" && end === ""){
        return true;
    }else if(start !== "" && end === ""){
        start_num = parseInt(start);
        return (start_num <= amount_num);
    }else if(start === "" && end !== ""){
        end_num = parseInt(removeSymbols(end));
        return (amount_num <= end_num);
    }else{
        start_num = parseInt(start);
        end_num = parseInt(end);
        return (start_num <= amount_num && amount_num <= end_num);
    }
}
function removeSymbols(string){
    string = string.replace("$", "");
    string = string.replace(",", "");
    return string;
}