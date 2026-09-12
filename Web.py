from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect("tax.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tax_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            income REAL NOT NULL,
            tax REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- TAX CALCULATION ----------------

def calculate_tax(income):

    # Example slabs for academic project

    if income <= 400000:
        tax = 0

    elif income <= 800000:
        tax = (income - 400000) * 0.05

    else:
        tax = 20000 + (income - 800000) * 0.10

    return tax


# ---------------- HTML + CSS ----------------

HTML = """
<!DOCTYPE html>

<html>

<head>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Income Tax Calculator</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;

            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;

            background: linear-gradient(135deg, #667eea, #764ba2);

            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 450px;
        }

        .card {
            background: white;

            padding: 30px;

            border-radius: 25px;

            box-shadow: 0 15px 40px rgba(0,0,0,0.25);
        }

        h1 {
            text-align: center;

            color: #333;

            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;

            color: #777;

            margin-bottom: 30px;
        }

        label {
            display: block;

            font-weight: bold;

            margin-bottom: 8px;

            color: #333;
        }

        input {
            width: 100%;

            padding: 15px;

            border: 1px solid #ddd;

            border-radius: 12px;

            font-size: 16px;

            margin-bottom: 20px;
        }

        input:focus {
            outline: none;

            border-color: #667eea;
        }

        button {
            width: 100%;

            padding: 15px;

            border: none;

            border-radius: 12px;

            background: #667eea;

            color: white;

            font-size: 17px;

            font-weight: bold;

            cursor: pointer;
        }

        button:hover {
            background: #5568d8;
        }

        .result {
            margin-top: 25px;

            padding: 20px;

            border-radius: 15px;

            background: #f2f4ff;
        }

        .result h2 {
            margin-top: 0;

            color: #333;
        }

        .tax {
            margin-top: 15px;

            padding: 18px;

            background: #667eea;

            color: white;

            border-radius: 12px;

            display: flex;

            justify-content: space-between;
        }

        .tax strong {
            font-size: 20px;
        }

        .error {
            margin-top: 20px;

            padding: 15px;

            background: #ffe5e5;

            color: red;

            border-radius: 10px;

            text-align: center;
        }

        .footer {
            text-align: center;

            color: #999;

            margin-top: 20px;

            font-size: 12px;
        }

    </style>

</head>


<body>

<div class="container">

    <div class="card">

        <h1>💰 MODERN INCOME TAX CALCULATOR </h1>

        <p class="subtitle">
            Calculate your estimated income tax
        </p>


        <form method="POST">

            <label>Enter Your Name</label>

            <input
                type="text"
                name="name"
                placeholder="Enter your name"
                required
            >


            <label>Annual Income (₹)</label>

            <input
                type="number"
                name="income"
                placeholder="Enter annual income"
                min="0"
                required
            >


            <button type="submit">
                Calculate Tax
            </button>

        </form>


        {% if result %}

        {% if result.error %}

        <div class="error">
            {{ result.error }}
        </div>

        {% else %}

        <div class="result">

            <h2>Tax Calculation</h2>

            <p>
                <b>Name:</b> {{ result.name }}
            </p>

            <p>
                <b>Annual Income:</b>
                ₹{{ "%.2f"|format(result.income) }}
            </p>

            <div class="tax">

                <span>Estimated Tax</span>

                <strong>
                    ₹{{ "%.2f"|format(result.tax) }}
                </strong>

            </div>

        </div>

        {% endif %}

        {% endif %}


        <div class="footer">
            Income Tax Calculator | Python Flask
        </div>

    </div>

</div>


<script>

    document.querySelector("form").addEventListener("submit", function() {

        const income =
            document.querySelector("input[name='income']").value;

        if (income < 0) {

            alert("Income cannot be negative.");

        }

    });

</script>


</body>

</html>
"""


# ---------------- HOME PAGE ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        name = request.form.get("name")

        income = float(request.form.get("income"))

        if income < 0:

            result = {
                "error": "Income cannot be negative."
            }

        else:

            tax = calculate_tax(income)

            # Save data to database

            conn = sqlite3.connect("tax.db")

            conn.execute(
                """
                INSERT INTO tax_records
                (name, income, tax)
                VALUES (?, ?, ?)
                """,
                (name, income, tax)
            )

            conn.commit()

            conn.close()


            result = {

                "name": name,

                "income": income,

                "tax": tax

            }


    return render_template_string(HTML, result=result)


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":

    create_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
