function changeCatNum() {
    let x = document.getElementById("account_cat_selection").value;
    if(x === "Asset")
    {
        document.getElementById("initial_number_input").value = 1;
    }
    if(x === "Liability")
    {
        document.getElementById("initial_number_input").value = 2;
    }
    if(x === "Equity")
    {
        document.getElementById("initial_number_input").value = 3;
    }
    if(x === "Revenue")
    {
        document.getElementById("initial_number_input").value = 4;
    }
    if(x === "Expenses")
    {
        document.getElementById("initial_number_input").value = 5;
    }
}
