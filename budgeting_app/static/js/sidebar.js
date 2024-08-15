const burgerMenu = document.getElementById("toggle-btn");
const sidebarLogo = document.querySelector(".sidebar-logo")

// SIDEBAR LOGIC
window.onload = () => {
    document.getElementById("sidebar").classList.toggle("expand");
}

burgerMenu.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapse");
})

sidebarLogo.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapse");
})

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
    const progressPercentText = document.getElementById("progressPercentText");
    let stm = formatNumber(data?.spent_this_month);
    console.log(data.percent_spent);
    dataField.innerText = "$" + String(stm);
    progressPercent.style.width = `${data?.percent_spent}%`;
    progressPercent.innerText = `${data?.percent_spent}%`;
})