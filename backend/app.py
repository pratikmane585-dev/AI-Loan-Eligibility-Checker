from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "loan_applications.db"


# -------------------------
# Database Setup
# -------------------------

def init_db():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            income REAL,
            credit_score INTEGER,
            employment TEXT,
            loan_amount REAL,
            tenure INTEGER,
            emi REAL,
            eligible INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# -------------------------
# Home
# -------------------------

@app.route("/")
def home():
    return "AI Loan Eligibility Checker Backend is Running!"


# -------------------------
# Loan Eligibility
# -------------------------

@app.route("/api/check-loan", methods=["POST"])
def check_loan():

    data = request.json

    name = data.get("name", "")
    age = int(data.get("age", 0))
    income = float(data.get("income", 0))
    credit_score = int(data.get("creditScore", 0))
    employment = data.get("employment", "")
    loan_amount = float(data.get("loanAmount", 0))
    tenure = int(data.get("tenure", 0))

    # -------------------------
    # Eligibility
    # -------------------------

    reasons = []

    if age < 18 or age > 60:
        reasons.append("Age should be between 18 and 60.")

    if income < 15000:
        reasons.append("Monthly income is below the basic requirement.")

    if credit_score < 650:
        reasons.append("Credit score is below the basic requirement.")

    eligible = len(reasons) == 0

    # -------------------------
    # EMI
    # -------------------------

    annual_rate = 10
    monthly_rate = annual_rate / 12 / 100
    months = tenure * 12

    if months > 0 and loan_amount > 0:

        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    else:
        emi = 0

    # -------------------------
    # Financial Tips
    # -------------------------

    tips = []

    if credit_score < 650:
        tips.append(
            "Try to improve your credit score by making payments on time."
        )

    elif credit_score >= 750:
        tips.append(
            "Your credit score is strong. Continue maintaining timely payments."
        )

    else:
        tips.append(
            "Maintain regular payments to gradually improve your credit profile."
        )

    if income > 0 and emi > income * 0.40:
        tips.append(
            "Your EMI is high compared with your income. "
            "Consider a lower loan amount or longer tenure."
        )
    else:
        tips.append(
            "Try to keep your monthly loan payments within a comfortable "
            "portion of your income."
        )

    if loan_amount > income * 60:
        tips.append(
            "The requested loan amount is high compared with your income."
        )

    if age < 25:
        tips.append(
            "Build a strong credit history and avoid unnecessary borrowing."
        )

    if employment == "Self Employed":
        tips.append(
            "Keep your income records and financial documents updated."
        )

    if employment == "Business":
        tips.append(
            "Maintain proper business income and tax records."
        )

    # -------------------------
    # Message
    # -------------------------

    if eligible:
        message = (
            "Based on the basic criteria, your profile may be eligible "
            "for the requested loan."
        )
    else:
        message = (
            "Your profile does not currently meet all basic eligibility "
            "criteria."
        )

    # -------------------------
    # Save to Database
    # -------------------------

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO applications
        (
            name,
            age,
            income,
            credit_score,
            employment,
            loan_amount,
            tenure,
            emi,
            eligible
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        income,
        credit_score,
        employment,
        loan_amount,
        tenure,
        round(emi, 2),
        int(eligible)
    ))

    connection.commit()
    application_id = cursor.lastrowid

    connection.close()

    # -------------------------
    # Response
    # -------------------------

    return jsonify({
        "success": True,
        "application_id": application_id,
        "name": name,
        "eligible": eligible,
        "emi": round(emi, 2),
        "message": message,
        "reasons": reasons,
        "tips": tips,
        "credit_score": credit_score,
        "employment": employment
    })


# -------------------------
# Get All Applications
# -------------------------

@app.route("/api/applications", methods=["GET"])
def get_applications():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """)

    applications = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return jsonify(applications)


# -------------------------
# Start Server
# -------------------------

if __name__ == "__main__":

    init_db()

    print("AI Loan Eligibility Checker Backend Started 🚀")

    app.run(debug=True, port=5000)