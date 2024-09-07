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

// BUDGET HISTORY
const displayItems = (items, count) => {
    for (let i = 0; i < count && i < items.length; i++) {
        items[i].style.display = 'table-row';
    }
}
const budgetHistory = document.getElementById("budgetHistory");
let itemsToShow = 10;
let incrementBy = 10;
let firstTimeHistory = true;
let seeMoreListener = false;
budgetHistory.addEventListener("click", async () => {
    const response = await fetch("/app/get-expenses", {method: "POST"});
    const data = await response.json();
    const historyModal = document.getElementById("historyModalToggle");

    if(historyModal) {
        const historyTable = document.getElementById("historyTable");
        const seeMore = document.getElementById("seeMoreHistory");
        let rows;
        if(firstTimeHistory) {
            firstTimeHistory = false;
            data.expenses.forEach(expense => {
                const dateObj = new Date(expense.date);
                const parts = dateObj.toLocaleDateString('en-US', {year: 'numeric',month: 'short',day: '2-digit'}).split(' ');
                const formattedDate = `${parts[0]}. ${parts[1]} ${parts[2]}`;
                historyTable.innerHTML += `
                    <tr style="display: none;">
                        <td class="align-middle text-left"><input type="checkbox" name="selected_transaction" id="${expense.id}" value="${expense.id}"></td>
                        <td class="align-middle text-left fw-bold text-danger">${expense.transaction_type}</td>
                        <td class="align-middle text-left">${expense.amount}</td>
                        <td class="align-middle text-left"><div class="d-flex align-items-center gap-2"><i class="lni ${expense.category__icon_tag}"></i><div>${expense.category__title}</div></div></td>
                        <td class="align-middle text-left">${formattedDate}</td>
                        <td class="align-middle text-left">${expense.comment}</td>
                        <td class="align-middle text-left">
                            <button
                                class="border-0 bg-white"
                                id="edit_transaction"
                                data-bs-toggle="modal"
                                data-bs-target="#editModalToggle"
                                data-bs-id="${expense.id}"
                                data-bs-type="${expense.transaction_type}"
                                data-bs-amount="${expense.amount}"
                                data-bs-category="${expense.category__title}"
                                data-bs-date="${expense.date.slice(0, -1)}"
                                data-bs-comment="${expense.comment}"
                            >
                                <i class="lni lni-cog fs-5 mt-2"></i>
                            </button>
                        </td>
                    </tr>
                `
            })
            rows = document.querySelectorAll("#historyTable tr");
            displayItems(rows, itemsToShow);
        }

        rows = document.querySelectorAll("#historyTable tr");
        if(itemsToShow >= rows.length) {
            seeMore.style.display = "none";
        }
        if(!seeMoreListener) {
            seeMore.addEventListener("click", () => {
                itemsToShow += incrementBy;
                displayItems(rows, itemsToShow);
                if(itemsToShow >= rows.length) {
                    seeMore.style.display = "none";
                }
            })
            seeMoreListener = true;
        }
    }
})