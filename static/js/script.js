console.log("JavaScript Started");

fetch("/dashboard")
.then(response => {
    console.log("Response Status:", response.status);
    return response.json();
})
.then(data => {

    console.log("Data Received:", data);

    document.getElementById("total").innerText = data.total_transactions;
    document.getElementById("fraud").innerText = data.fraud_transactions;
    document.getElementById("rate").innerText = data.fraud_rate;

    console.log("Dashboard Updated Successfully");

})
.catch(error => {
    console.error("ERROR:", error);
});
// ------------------------------
// Category Risk Chart
// ------------------------------

fetch("/category-risk")
.then(response => response.json())
.then(data => {

    const categories = [];
    const fraudCounts = [];

    data.forEach(item => {

        categories.push(item.merchant_category);
        fraudCounts.push(item.fraud_transactions);

    });

    const ctx = document.getElementById("categoryChart").getContext("2d");

    new Chart(ctx, {

    type: "bar",

    data: {

        labels: categories,

        datasets: [{

            label: "Fraud Transactions",

            data: fraudCounts,

            backgroundColor: [
                "#3498db",
                "#2ecc71",
                "#f39c12",
                "#e74c3c",
                "#9b59b6"
            ],

            borderColor: "#2c3e50",

            borderWidth: 2,

            borderRadius: 8

        }]

    },

    options: {

        responsive: true,

        plugins: {

            title: {

                display: true,

                text: "Fraud Transactions by Merchant Category",

                font: {

                    size: 20

                }

            },

            legend: {

                display: false

            }

        },

        scales: {

            y: {

                beginAtZero: true,

                title: {

                    display: true,

                    text: "Number of Fraud Transactions"

                }

            },

            x: {

                title: {

                    display: true,

                    text: "Merchant Category"

                }

            }

        }

    }

});
})
.catch(error => {
    console.error("Chart Error:", error);
});
// ------------------------------
// Monthly Fraud Trend Chart
// ------------------------------

fetch("/monthly-fraud")
.then(response => response.json())
.then(data => {

    const monthNames = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ];

    const months = [];
    const fraudCounts = [];

    data.forEach(item => {

        months.push(monthNames[item.month]);
        fraudCounts.push(item.fraud_transactions);

    });

    const ctx2 = document.getElementById("monthlyChart").getContext("2d");

    new Chart(ctx2, {

        type: "line",

        data: {

            labels: months,

            datasets: [{

                label: "Monthly Fraud",

                data: fraudCounts,

                borderColor: "#e74c3c",

                backgroundColor: "rgba(231,76,60,0.2)",

                fill: true,

                tension: 0.4,

                pointRadius: 5

            }]

        },

        options: {

            responsive: true,

            plugins: {

                title: {

                    display: true,

                    text: "Monthly Fraud Trend",

                    font: {

                        size: 20

                    }

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    title: {

                        display: true,

                        text: "Fraud Transactions"

                    }

                },

                x: {

                    title: {

                        display: true,

                        text: "Month"

                    }

                }

            }

        }

    });

})
.catch(error => {
    console.error("Monthly Chart Error:", error);
});
// ------------------------------
// High Risk Transactions Table
// ------------------------------

fetch("/high-risk")
.then(response => response.json())
.then(data => {

    const tableBody = document.querySelector("#transactionTable tbody");

    tableBody.innerHTML = "";

    data.forEach(item => {

        const row = `
            <tr>
                <td>${item.transaction_id}</td>
                <td>${item.customer_id}</td>
                <td>₹${parseFloat(item.amount).toFixed(2)}</td>
                <td>${item.merchant_category}</td>
                <td>${new Date(item.transaction_date).toLocaleDateString()}</td>
            </tr>
        `;

        tableBody.innerHTML += row;

    });

})
.catch(error => {
    console.error("Table Error:", error);
});