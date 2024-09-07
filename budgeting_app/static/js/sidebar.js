const burgerMenu = document.getElementById("toggle-btn");
const sidebarLogo = document.querySelector(".sidebar-logo")

// SIDEBAR LOGIC

// EDIT BUDGET
const editBudgetBtn = document.getElementById("editBudgetBtn");
const budgetInput = document.getElementById("budget");

editBudgetBtn.addEventListener("click", ()=> {
    if(budgetInput.value) {
        fetch("/app/edit-budget", {
            body: JSON.stringify({
                budget: budgetInput.value,
            }),
            method: "POST",
        })
        .then(res => res.json())
        .then(data => location.reload())
    }
})

// GET BUDGET
function formatNumber(number) {
    let formattedNumber = parseFloat(number).toFixed(2); // Round to 2 decimals
    if (formattedNumber.endsWith(".00")) {
        formattedNumber = formattedNumber.slice(0, -3);
    }
    formattedNumber = formattedNumber.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

    return formattedNumber;
}

fetch("/app/get-budget", {
    method: "POST",
})
.then(res => res.json())
.then(data => {
    const dataField = document.getElementById("spent_this_month");
    const progressPercent = document.getElementById("progressPercent");
    const hiddenProgress = document.getElementById("hiddenProgress");
    const hiddenPercent = document.getElementById("hiddenPercent");
    const daily_spending = document.getElementById("daily_spending");
    const days_left = document.getElementById("days_left");
    const spending_info = document.getElementById("spending_info");
    let stm = formatNumber(data?.spent_this_month);
    dataField.innerText = "$" + String(stm);
    if(data?.percent_spent > 100 || data?.percent_spent <=0) {
        spending_info.innerHTML = `Budget passed by $${-data?.remaining_budget}`
    }
    progressPercent.style.width = `${data?.percent_spent}%`;
    hiddenProgress.style.width = `${data?.percent_spent}%`;
    progressPercent.innerText = `${data?.percent_spent}%`;
    hiddenPercent.innerText = `${data?.percent_spent}%`;
    daily_spending.innerText = `${data?.daily_spending}`;
    days_left.innerText = `${data?.days_left}`;
})