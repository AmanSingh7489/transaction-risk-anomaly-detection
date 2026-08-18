from flask import Flask, jsonify, render_template
from db import get_connection

app = Flask(__name__)


# ----------------------------------------
# Home API
# ----------------------------------------
@app.route("/")
def home():
    return "Welcome to Transaction Risk Detection Analysis (TRDA) Backend!"


# ----------------------------------------
# Dashboard HTML Page
# ----------------------------------------
@app.route("/dashboard-page")
def dashboard_page():
    return render_template("dashboard.html")


# ----------------------------------------
# Transactions API
# ----------------------------------------
@app.route("/transactions")
def transactions():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transactions LIMIT 10")

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Fraud Transactions API
# ----------------------------------------
@app.route("/fraud")
def fraud():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE is_fraud = 1
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Dashboard API
# ----------------------------------------
@app.route("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM transactions")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS fraud FROM transactions WHERE is_fraud = 1")
    fraud = cursor.fetchone()["fraud"]

    fraud_rate = round((fraud / total) * 100, 2)

    cursor.close()
    connection.close()

    return jsonify({
        "total_transactions": total,
        "fraud_transactions": fraud,
        "fraud_rate": f"{fraud_rate}%"
    })


# ----------------------------------------
# Category Risk API
# ----------------------------------------
@app.route("/category-risk")
def category_risk():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            merchant_category,
            COUNT(*) AS fraud_transactions
        FROM transactions
        WHERE is_fraud = 1
        GROUP BY merchant_category
        ORDER BY fraud_transactions DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Category Risk Rate API
# ----------------------------------------
@app.route("/category-risk-rate")
def category_risk_rate():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            merchant_category,
            COUNT(*) AS total_transactions,
            SUM(is_fraud) AS fraud_transactions,
            ROUND((SUM(is_fraud) / COUNT(*)) * 100, 2) AS fraud_rate
        FROM transactions
        GROUP BY merchant_category
        ORDER BY fraud_rate DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Monthly Fraud API
# ----------------------------------------
@app.route("/monthly-fraud")
def monthly_fraud():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            MONTH(transaction_date) AS month,
            COUNT(*) AS fraud_transactions
        FROM transactions
        WHERE is_fraud = 1
        GROUP BY MONTH(transaction_date)
        ORDER BY MONTH(transaction_date)
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)
# ----------------------------------------
# High Risk Transactions API
# ----------------------------------------
@app.route("/high-risk")
def high_risk():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            transaction_id,
            customer_id,
            amount,
            merchant_category,
            transaction_date
        FROM transactions
        WHERE is_fraud = 1
        AND amount > 700
        ORDER BY amount DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Amount Range API (Debug)
# ----------------------------------------
@app.route("/amount-range")
def amount_range():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            MIN(amount) AS min_amount,
            MAX(amount) AS max_amount,
            AVG(amount) AS avg_amount
        FROM transactions
        WHERE is_fraud = 1
    """)

    data = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Customer Transactions API
# ----------------------------------------
@app.route("/customer/<int:customer_id>")
def customer_transactions(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            transaction_id,
            customer_id,
            amount,
            merchant_category,
            is_fraud,
            transaction_date
        FROM transactions
        WHERE customer_id = %s
        ORDER BY transaction_date DESC
    """

    cursor.execute(query, (customer_id,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# ----------------------------------------
# Run Flask App
# ----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)