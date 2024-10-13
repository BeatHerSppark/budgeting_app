// PIE CHARTS
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

updateChartExpense(expenseCategoriesKeys, expenseCategoriesValues);
updateChartIncome(incomeCategoriesKeys, incomeCategoriesValues);


// EXPENSE VS INCOME CHART
var options = {
    chart: {
        type: 'bar',
        height: "100%",
    },
    stroke: {
        curve: 'smooth'
    },
    series: [
        {
            name: 'Income',
            data: incomeList
        },
        {
            name: 'Expenses',
            data: expenseList
        }
    ],
    xaxis: {
        categories: rangeList
    },
    tooltip: {
        shared: true,
        intersect: false
    },
    plotOptions: {
        bar: {
            horizontal: false,
            borderRadius: 10,
            borderRadiusApplication: 'end', // 'around', 'end'
            borderRadiusWhenStacked: 'last', // 'all', 'last'
            dataLabels: {
            }
        },
    },
    colors: ['#00E396', '#E91E63']
};

var chart = new ApexCharts(document.querySelector("#expenseIncomeChart"), options);

chart.render();

// SEARCH
