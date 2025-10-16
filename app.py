from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from encryption import encrypt_data, decrypt_data
from hashing import generate_hash, verify_password, hash_password
from digital_signature import sign_data, verify_signature

app = Flask(__name__)
app.secret_key = "safepay_secret_key_change_in_production"

def get_db():
    return sqlite3.connect("database.db")

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT username, password, role FROM users WHERE username=? AND role=?", (username, role))
        user = cur.fetchone()
        con.close()

        if user and verify_password(password, user[1]):
            session["user"] = username
            session["role"] = role
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    con = get_db()
    cur = con.cursor()
    if session["role"] == "admin":
        cur.execute("SELECT username, role, balance FROM users")
        users = cur.fetchall()
        cur.execute(
            """
            SELECT id, customer_id, receiver_id, amount, enc_data, hash, hex(signature) as signature_hex, verified
            FROM transactions
            ORDER BY id DESC
            """
        )
        txns = cur.fetchall()
        con.close()
        return render_template("admin_dashboard.html", users=users, txns=txns)
    else:
        cur.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
        bal_row = cur.fetchone()
        balance = bal_row[0] if bal_row else 0.0
        cur.execute("SELECT * FROM transactions WHERE customer_id=? OR receiver_id=? ORDER BY id DESC", (session["user"], session["user"]))
        data = cur.fetchall()
        con.close()
        return render_template("dashboard.html", data=data, balance=balance)

# ---------------- TRANSACTION ----------------
@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    if "user" not in session or session["role"] == "admin":
        return redirect("/")

    if request.method == "POST":
        base_data = {
            "Customer_ID": session["user"],
            "Receiver_ID": request.form["Receiver_ID"],
            "Customer_Name": request.form["Customer_Name"],
            "Gender": request.form["Gender"],
            "Age": int(request.form["Age"]),
            "State": request.form["State"],
            "City": request.form["City"],
            "Bank_Branch": request.form["Bank_Branch"],
            "Account_Type": request.form["Account_Type"],
            "Transaction_Amount": float(request.form["Transaction_Amount"]),
            "Transaction_Type": request.form["Transaction_Type"],
            "Merchant_Category": request.form["Merchant_Category"],
        }

        con = get_db()
        cur = con.cursor()
        try:
            cur.execute("BEGIN IMMEDIATE")
            if base_data["Customer_ID"] == base_data["Receiver_ID"]:
                raise ValueError("Cannot transfer to self")
            # Check balances and receiver existence
            cur.execute("SELECT balance FROM users WHERE username=?", (base_data["Customer_ID"],))
            row = cur.fetchone()
            if not row:
                raise ValueError("Sender not found")
            sender_balance = float(row[0])
            amount = float(base_data["Transaction_Amount"])
            if amount <= 0 or sender_balance < amount:
                raise ValueError("Insufficient balance")

            cur.execute("SELECT balance FROM users WHERE username=?", (base_data["Receiver_ID"],))
            row = cur.fetchone()
            if not row:
                raise ValueError("Receiver not found")
            receiver_balance = float(row[0])

            # Update balances
            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount
            cur.execute("UPDATE users SET balance=? WHERE username=?", (new_sender_balance, base_data["Customer_ID"]))
            cur.execute("UPDATE users SET balance=? WHERE username=?", (new_receiver_balance, base_data["Receiver_ID"]))

            # Build data for crypto with current Account_Balance
            data = dict(base_data)
            data["Account_Balance"] = sender_balance

            # Encrypt, hash, sign
            data_str = "|".join(str(v) for v in data.values())
            enc_data = encrypt_data(data_str)
            hash_value = generate_hash(data_str)
            signature = sign_data(hash_value)
            verified = verify_signature(hash_value, signature)

            # Record transaction
            cur.execute("""
                INSERT INTO transactions (
                    customer_id, receiver_id, name, gender, age, state, city, branch, acc_type, amount,
                    txntype, merchant, balance, enc_data, hash, signature, verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["Customer_ID"], data["Receiver_ID"], data["Customer_Name"], data["Gender"], data["Age"],
                data["State"], data["City"], data["Bank_Branch"], data["Account_Type"],
                amount, data["Transaction_Type"], data["Merchant_Category"],
                new_sender_balance, enc_data, hash_value, signature, str(verified)
            ))
            con.commit()
        except Exception as e:
            con.rollback()
            con.close()
            return render_template("transaction.html", error=str(e))
        con.close()

        return render_template(
            "transaction_result.html",
            verified=verified,
            amount=amount,
            receiver=base_data["Receiver_ID"],
            new_balance=new_sender_balance
        )

    return render_template("transaction.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            initial_balance = float(request.form.get("balance", "50000"))
        except ValueError:
            initial_balance = 50000.0
        role = "user"

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT 1 FROM users WHERE username=?", (username,))
        exists = cur.fetchone()
        if exists:
            con.close()
            return render_template("signup.html", error="Username already exists")

        cur.execute("INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)", (
            username, hash_password(password), role, initial_balance
        ))
        con.commit()
        con.close()
        return redirect(url_for("login"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
