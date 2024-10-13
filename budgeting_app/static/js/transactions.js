// DATE LOGIC
const todayBtn = document.getElementById("todayBtn");
const weekBtn = document.getElementById("weekBtn");
const monthBtn = document.getElementById("monthBtn");
const yearBtn = document.getElementById("yearBtn");
const allTimeBtn = document.getElementById("allTimeBtn");

const formatDate = (date) => {
    let year = date.getFullYear();
    let month = (date.getMonth() + 1).toString();
    let day = date.getDate().toString();
    if (month.length < 2) {
        month = '0' + month;
    }
    if (day.length < 2) {
        day = '0' + day;
    }

    return `${year}-${month}-${day}`;
}

const getMonday = (d) => {
    d = new Date(d);
    let day = d.getDay(),
        diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
}

const getFirstOfMonth = (d) => {
    d = new Date(d);
    return new Date(d.getFullYear(), d.getMonth(), 1);
}

const getFirstOfYear = (d) => {
    d = new Date(d);
    return new Date(d.getFullYear(), 0, 1);
}

todayBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: today,
            end: today,
            selected_date: "today",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //todayBtn.href = `?start=${encodeURIComponent(today)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("today")}`;
})

weekBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let monday = formatDate( getMonday(new Date()) );
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: monday,
            end: today,
            selected_date: "week",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //weekBtn.href = `?start=${encodeURIComponent(monday)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("week")}`;
})

monthBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let firstOfMonth = formatDate( getFirstOfMonth(new Date()) );
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: firstOfMonth,
            end: today,
            selected_date: "month",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //monthBtn.href = `?start=${encodeURIComponent(firstOfMonth)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("month")}`;
})

yearBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let firstOfYear = formatDate( getFirstOfYear(new Date()) );
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: firstOfYear,
            end: today,
            selected_date: "year",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //yearBtn.href = `?start=${encodeURIComponent(firstOfYear)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("year")}`;
})

allTimeBtn.addEventListener("click", () => {
    let earliestDate = formatDate(new Date(0));
    let today = formatDate(new Date());
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: earliestDate,
            end: today,
            selected_date: "allTime",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //allTimeBtn.href = `?start=${encodeURIComponent(earliestDate)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("allTime")}`;
})

// DELETE TRANSACTIONS
const transaction_checkboxes = document.querySelectorAll("td input");

transaction_checkboxes.forEach(checkbox => {
    checkbox.addEventListener("change", () => {
        if(checkbox.checked) {
            document.getElementById("dashboard_delete_transactions").classList.remove("d-none");
            document.getElementById("dashboard_delete_transactions").classList.add("d-block");
        }
        let noneSelected=true;
        transaction_checkboxes.forEach(checkbox2 => {
            if(checkbox2.checked) {
                noneSelected=false;
            }
        })
        if(noneSelected) {
            document.getElementById("dashboard_delete_transactions").classList.remove("d-block");
            document.getElementById("dashboard_delete_transactions").classList.add("d-none");
        }
    })
})

const dashboard_delete_transactions = document.getElementById("dashboard_delete_transactions");

dashboard_delete_transactions.addEventListener("click", () => {
    let idArray = [];
    transaction_checkboxes.forEach(checkbox => {
        if(checkbox.checked) idArray.push(checkbox.id);
    })

    fetch("/app/dashboard-delete-transactions", {
        body: JSON.stringify({ checkedIDs: idArray }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => {
        location.reload();
    })
})

// CHART
async function fetchChartData() {
    const response = await fetch("/app/get-pie-chart", {
                    method: "POST",
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });

    const data = await response.json();

    const expenseCategoryTitles = Object.keys(data["expenseCategories"]);
    const expenseCategoryValues = Object.values(data["expenseCategories"]);
    updateChartExpense(expenseCategoryTitles, expenseCategoryValues);

    const incomeCategoryTitles = Object.keys(data["incomeCategories"]);
    const incomeCategoryValues = Object.values(data["incomeCategories"]);
    updateChartIncome(incomeCategoryTitles, incomeCategoryValues);
}

const updateChartExpense = (expenseCategoryTitles, expenseCategoryValues) => {
    if(expenseCategoryTitles.length>0) {
        var options = {
            chart: {
                type: 'donut',
            },
            series: expenseCategoryValues,
            labels: expenseCategoryTitles,
            legend: {
                position: 'bottom',
            }
        };

        var chart = new ApexCharts(document.querySelector("#pieChartExpense"), options);
        chart.render();
    }
    else {
        var options = {
            chart: {
                type: 'donut',
            },
            series: [100],
            labels: ["No transactions yet"],
            colors: ['#9f9f9f'],
            legend: {
                position: 'bottom',
            }
        };

        var chart = new ApexCharts(document.querySelector("#pieChartExpense"), options);
        chart.render();
    }
}

const updateChartIncome = (incomeCategoryTitles, incomeCategoryValues) => {
    if(incomeCategoryTitles.length>0) {
        var options = {
            chart: {
                type: 'donut',
            },
            series: incomeCategoryValues,
            labels: incomeCategoryTitles,
            legend: {
                position: 'bottom',
            }
        };

        var chart = new ApexCharts(document.querySelector("#pieChartIncome"), options);
        chart.render();
    }
    else {
        var options = {
            chart: {
                type: 'donut',
            },
            series: [100],
            labels: ["No transactions yet"],
            colors: ['#9f9f9f'],
            legend: {
                position: 'bottom',
            }
        };

        var chart = new ApexCharts(document.querySelector("#pieChartIncome"), options);
        chart.render();
    }
}

fetchChartData();

// SORT TRANSACTIONS
const sortDate = document.getElementById("sortDate");
const sortAmount = document.getElementById("sortAmount");

sortDate.addEventListener('click', async () => {
    const response = await fetch("/app/set-sort-date", {
        method: "POST",
    });

    const data = await response.json();
    location.reload();
})

sortAmount.addEventListener('click', async () => {
    const response = await fetch("/app/set-sort-amount", {
        method: "POST",
    });

    const data = await response.json();
    location.reload();
})

// SEARCH TRANSACTIONS
const searchInput = document.getElementById("searchInput");
const tableMain = document.querySelector(".table-main");
const tableSearch = document.querySelector(".table-search");
const paginationContainer = document.querySelector(".pagination-container");
const searchBody = document.querySelector(".search-body");
const noResults = document.getElementById("no-results");
tableSearch.style.display = 'none';
noResults.style.display = 'none';
let debounceTimeout;

async function convertSearchAmount(search_transactions) {
    for(let item of search_transactions) {
        const dateObj = new Date(item.date);
        console.log(item.date.slice(0, -6));
        const parts = dateObj.toLocaleDateString('en-US', {year: 'numeric',month: 'short',day: '2-digit'}).split(' ');
        const formattedDate = `${parts[0]}. ${parts[1]} ${parts[2]}`;
        const convertedAmount = await convertCurrency(item.amount, 'USD', userCurrency);
        let formattedAmount = formatCurrency(convertedAmount, userCurrency);
        searchBody.innerHTML += `
            <tr>
            <td class="align-middle text-left"><input type="checkbox" name="selected_transaction" id="${item.id}" value="${item.id}"></td>
            <td class="align-middle text-left fw-bold ${item.transaction_type=="Expense" ? "text-danger" : "text-success"}">${item.transaction_type}</td>
            <td class="align-middle text-left">${formattedAmount}</td>
            <td class="align-middle text-left"><div class="d-flex align-items-center gap-2"><i class="lni ${item.category__icon_tag}"></i><div>${item.category__title}</div></div></td>
            <td class="align-middle text-left">${formattedDate}</td>
            <td class="align-middle text-left">${item.comment}</td>
            <td class="align-middle text-left">
                <button
                    class="border-0 bg-white"
                    id="edit_transaction"
                    data-bs-toggle="modal"
                    data-bs-target="#editModalToggle"
                    data-bs-id="${item.id}"
                    data-bs-type="${item.transaction_type}"
                    data-bs-amount="${item.amount}"
                    data-bs-category="${item.category__title}"
                    data-bs-date="${item.date.slice(0, -6)}"
                    data-bs-comment="${item.comment}"
                    data-bs-currency="${userCurrency}"
                >
                    <i class="lni lni-cog fs-5 mt-2"></i>
                </button>
            </td>
            </tr>
        `
    }
}

async function handleSearchConversion(searchValue) {
    const convertedAmount = await convertCurrency(searchValue, userCurrency, 'USD');
    formattedAmount = parseInt(convertedAmount);
    console.log(convertedAmount)
    console.log(parseFloat(formattedAmount.toString().slice(0, searchValue.length)));

    fetch("/app/search-transactions", {
        body: JSON.stringify({ searchText: parseFloat(formattedAmount.toString().slice(0, searchValue.length)) }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => {
        tableMain.style.display = 'none';
        tableSearch.style.display = 'block';
        if(data.search_transactions.length === 0) {
            tableSearch.style.display = 'none';
            noResults.style.display = 'block';
        } else {
            noResults.style.display = 'none';
            convertSearchAmount(data.search_transactions);
        }
    })
}

searchInput.addEventListener("keyup", (e) => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {

        const ignoredKeys = [
            'Control', 'Alt', 'Shift', 'Meta', 'ArrowUp', 'ArrowDown',
            'ArrowLeft', 'ArrowRight', 'CapsLock', 'Escape', 'Tab',
            'Enter', 'PageUp', 'PageDown', 'Home', 'End', 'Insert'
        ];
        if(!ignoredKeys.includes(e.key)) {
            const searchValue = e.target.value;
            noResults.style.display = 'none';
            if(searchValue.trim().length>0) {
                paginationContainer.style.display = 'none';
                searchBody.innerHTML = "";
                if(!isNaN(searchValue)) {
                    handleSearchConversion(searchValue);
                }
                else {
                    fetch("/app/search-transactions", {
                        body: JSON.stringify({ searchText: searchValue }),
                        method: "POST",
                    })
                    .then(res => res.json())
                    .then(data => {
                        tableMain.style.display = 'none';
                        tableSearch.style.display = 'block';
                        if(data.search_transactions.length === 0) {
                            tableSearch.style.display = 'none';
                            noResults.style.display = 'block';
                        } else {
                            noResults.style.display = 'none';
                            convertSearchAmount(data.search_transactions);
                        }
                    })
                }
            }
            else {
                tableMain.style.display = 'block';
                tableSearch.style.display = 'none';
                paginationContainer.style.display = 'flex';
            }
        }
    }, 300);
})

// CUSTOM DATES
const setDatesBtn = document.getElementById("submitCustomDates");
setDatesBtn.addEventListener("click", () => {
    let startDate = document.getElementById("startDate");
    let endDate = document.getElementById("endDate");
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: formatDate(new Date(startDate.value)),
            end: formatDate(new Date(endDate.value)),
            selected_date: "custom",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
})