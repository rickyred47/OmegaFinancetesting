function changeCatNum() {
    let x = document.getElementById("accountcat_input").value;
    if(x === "Asset")
    {
        document.getElementById("catnumber_input").value = 1;
    }
    if(x === "Liability")
    {
        document.getElementById("catnumber_input").value = 2;
    }
    if(x === "Equity")
    {
        document.getElementById("catnumber_input").value = 3;
    }
    if(x === "Revenue")
    {
        document.getElementById("catnumber_input").value = 4;
    }
    if(x === "Expenses")
    {
        document.getElementById("catnumber_input").value = 5;
    }
}