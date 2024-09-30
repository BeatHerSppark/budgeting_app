const burgerMenu = document.getElementById("toggle-btn");
const sidebarLogo = document.querySelector(".sidebar-logo")

// ADD TRANSACTIONS
const incomeModal = document.getElementById("incomeModalToggle");
const expenseModal = document.getElementById("expenseModalToggle");
let openedIncomeOnce = false;
if(incomeModal) {
    incomeModal.addEventListener("show.bs.modal", async e => {
        const amountInput = document.getElementById("amountIncome");
        const currencyInput = document.getElementById("currencyIncome");
        const shownAmountInput = document.getElementById("shownAmountIncome");

        currencyInput.value = userCurrency;

        let debounceTimeout;
        if(!openedIncomeOnce) {
            shownAmountInput.addEventListener("input", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownAmountInput.value, currencyInput.value, 'USD');
                    amountInput.value = formatNumber(convertedAmount);
                    console.log(amountInput.value);
                }, 300);
            })
            currencyInput.addEventListener("change", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownAmountInput.value, currencyInput.value, 'USD');
                    amountInput.value = convertedAmount;
                    console.log(amountInput.value);
                }, 300);
            })
        }

        openedIncomeOnce = true;
    })
}
let openedExpenseOnce = false;
if(expenseModal) {
    expenseModal.addEventListener("show.bs.modal", async e => {
        const amountInput = document.getElementById("amountExpense");
        const currencyInput = document.getElementById("currencyExpense");
        const shownAmountInput = document.getElementById("shownAmountExpense");

        currencyInput.value = userCurrency;

        let debounceTimeout;
        if(!openedExpenseOnce) {
            shownAmountInput.addEventListener("input", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownAmountInput.value, currencyInput.value, 'USD');
                    amountInput.value = formatNumber(convertedAmount);
                    console.log(amountInput.value);
                }, 300);
            })
            currencyInput.addEventListener("change", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownAmountInput.value, currencyInput.value, 'USD');
                    amountInput.value = convertedAmount;
                    console.log(amountInput.value);
                }, 300);
            })
        }

        openedExpenseOnce = true;
    })
}

// EDIT TRANSACTIONS
const editModal = document.getElementById("editModalToggle");
let openedOnce = false;
if(editModal) {
    editModal.addEventListener("show.bs.modal", async e => {
        if(!requestPath.split("/")[2]) {
            if(!openedOnce) document.getElementById("modal-body").innerHTML += `<input type="hidden" name="path" id="path" value="dashboard">`;
        } else {
            if(!openedOnce) document.getElementById("modal-body").innerHTML += `<input type="hidden" name="path" id="path" value="${requestPath.split("/")[2]}">`;
        }

        const button = e.relatedTarget;
        const id = button.getAttribute("data-bs-id");
        const type = button.getAttribute("data-bs-type");
        let amount = button.getAttribute("data-bs-amount");
        const category = button.getAttribute("data-bs-category");
        const date = button.getAttribute("data-bs-date");
        const comment = button.getAttribute("data-bs-comment");
        const currency = button.getAttribute("data-bs-currency");
        let shownAmount = await convertCurrency(amount, 'USD', currency);
        shownAmount = userCurrency == "MKD" ? Math.round(shownAmount) : shownAmount;

        const idInput = editModal.querySelector("#id");
        const typeInput = editModal.querySelector("#transaction_type");
        const amountInput = editModal.querySelector("#amount");
        const shownAmountInput = editModal.querySelector("#shownAmount");
        const categoryInput = editModal.querySelector("#category");
        const dateInput = editModal.querySelector("#date");
        const commentInput = editModal.querySelector("#comment");
        const currencyInput = editModal.querySelector("#currency");

        fetch("/app/dashboard-get-categories", {
            body: JSON.stringify({ category_type: type }),
            method: "POST",
        })
        .then(res => res.json())
        .then(data => {
            data.categories.forEach(category => {
                categoryInput.innerHTML += `<option value="${category.title}">${category.title}</option>`
            })
            if(category=="Uncategorized") {
                categoryInput.value = "Choose a category";
            }
            else {
                categoryInput.value = category;
            }
        })

        idInput.value = id;
        typeInput.value = type;
        amountInput.value = amount;
        shownAmountInput.value = shownAmount;
        dateInput.value = date;
        commentInput.value = comment;
        currencyInput.value = currency;

        let debounceTimeout;
        if(!openedOnce) {
            shownAmountInput.addEventListener("input", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownAmountInput.value, currencyInput.value, 'USD');
                    amountInput.value = formatNumber(convertedAmount);
                    console.log(amountInput.value);
                }, 300);
            })
            currencyInput.addEventListener("change", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownAmountInput.value, currencyInput.value, 'USD');
                    amountInput.value = convertedAmount;
                    console.log(amountInput.value);
                }, 300);
            })
        }

        openedOnce = true;
    })

    editModal.addEventListener("hide.bs.modal", e => {
        const categoryInput = editModal.querySelector("#category");
        categoryInput.innerHTML = `<option selected>Choose a category</option>`
    })
}

// EDIT BUDGET
const editBudgetModal = document.getElementById("editBudgetModal");
const editBudgetBtn = document.getElementById("editBudgetBtn");
const budgetInput = document.getElementById("budget");
const editModalBtn = document.getElementById("editBudget");
let openedBudget = false;

if(editBudgetModal) {
    editBudgetModal.addEventListener("show.bs.modal", async e => {
        let budget = editModalBtn.getAttribute("data-bs-budget");
        const currency = editModalBtn.getAttribute("data-bs-currency");
        let shownBudget = await convertCurrency(budget, 'USD', currency);
        shownBudget = userCurrency == "MKD" ? Math.round(shownBudget) : shownBudget;

        const budgetInput = editBudgetModal.querySelector("#budget");
        const shownBudgetInput = editBudgetModal.querySelector("#shownBudget");
        const currencyInput = editBudgetModal.querySelector("#currency");

        budgetInput.value = budget;
        shownBudgetInput.value = shownBudget;
        currencyInput.value = currency;

        let debounceTimeout;
        if(!openedBudget) {
            shownBudgetInput.addEventListener("input", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownBudgetInput.value, currencyInput.value, 'USD');
                    budgetInput.value = convertedAmount;
                    console.log(budgetInput.value);
                }, 300);
            })
            currencyInput.addEventListener("change", () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    convertedAmount = await convertCurrency(shownBudgetInput.value, currencyInput.value, 'USD');
                    budgetInput.value = convertedAmount;
                    console.log(budgetInput.value);
                }, 300);
            })
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
        }

        openedBudget = true;
    })
}

// GET BUDGET
function formatNumber(number) {
    let formattedNumber = parseFloat(number).toFixed(2);
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
    const budget_passed = document.getElementById("budget_passed");
    let stm = data?.spent_this_month;
    dataField.innerText = stm;
    progressPercent.style.width = `${data?.percent_spent}%`;
    hiddenProgress.style.width = `${data?.percent_spent}%`;
    progressPercent.innerText = `${data?.percent_spent}%`;
    hiddenPercent.innerText = `${data?.percent_spent}%`;
    if(data?.percent_spent > 100 || data?.percent_spent <0) {
        convertedBudget = convertCurrency(-data?.remaining_budget, 'USD', userCurrency)
        .then(budget => {
            spending_info.style.display = "none";
            budget_passed.innerHTML = `Budget passed by ${formatCurrency(budget, userCurrency)}`
        })
    }
    else {
        budget_passed.style.display = "none";
        daily_spending.innerText = `${data?.daily_spending}`;
        days_left.innerText = `${data?.days_left}`;
    }
})

const fom = document.getElementById("firstOfMonth");
const lom = document.getElementById("lastOfMonth");
const getFomAndLom = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();

    const firstDay = new Date(year, month, 1);
    const firstDayFormatted = firstDay.toLocaleDateString('en-US', { month: 'short', day: '2-digit' });

    const lastDay = new Date(year, month + 1, 0);
    const lastDayFormatted = lastDay.toLocaleDateString('en-US', { month: 'short', day: '2-digit' });

    return [firstDayFormatted, lastDayFormatted];
}
fom.innerText = getFomAndLom()[0];
lom.innerText = getFomAndLom()[1];

// BUDGET HISTORY
const displayItems = (items, count) => {
    for (let i = 0; i < count && i < items.length; i++) {
        items[i].style.display = 'table-row';
    }
}
const budgetHistory = document.getElementById("budgetHistory");
const budgetHistory2 = document.getElementById("budgetHistory2");
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
            for(expense of data.expenses) {
                const dateObj = new Date(expense.date);
                const parts = dateObj.toLocaleDateString('en-US', {year: 'numeric',month: 'short',day: '2-digit'}).split(' ');
                const formattedDate = `${parts[0]}. ${parts[1]} ${parts[2]}`;
                const convertedAmount = await convertCurrency(expense.amount, 'USD', userCurrency);
                let formattedAmount = formatCurrency(convertedAmount, userCurrency);
                historyTable.innerHTML += `
                    <tr style="display: none;">
                        <td class="align-middle text-left fw-bold text-danger">${expense.transaction_type}</td>
                        <td class="align-middle text-left">${formattedAmount}</td>
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
                                data-bs-currency="${userCurrency}"
                            >
                                <i class="lni lni-cog fs-5 mt-2"></i>
                            </button>
                        </td>
                    </tr>
                `
            }
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

budgetHistory2.addEventListener("click", async () => {
    const response = await fetch("/app/get-expenses", {method: "POST"});
    const data = await response.json();
    const historyModal = document.getElementById("historyModalToggle");

    if(historyModal) {
        const historyTable = document.getElementById("historyTable");
        const seeMore = document.getElementById("seeMoreHistory");
        let rows;
        if(firstTimeHistory) {
            firstTimeHistory = false;
            for(expense of data.expenses) {
                const dateObj = new Date(expense.date);
                const parts = dateObj.toLocaleDateString('en-US', {year: 'numeric',month: 'short',day: '2-digit'}).split(' ');
                const formattedDate = `${parts[0]}. ${parts[1]} ${parts[2]}`;
                const convertedAmount = await convertCurrency(expense.amount, 'USD', userCurrency);
                let formattedAmount = formatCurrency(convertedAmount, userCurrency);
                historyTable.innerHTML += `
                    <tr style="display: none;">
                        <td class="align-middle text-left fw-bold text-danger">${expense.transaction_type}</td>
                        <td class="align-middle text-left">${formattedAmount}</td>
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
                                data-bs-currency="${userCurrency}"
                            >
                                <i class="lni lni-cog fs-5 mt-2"></i>
                            </button>
                        </td>
                    </tr>
                `
            }
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