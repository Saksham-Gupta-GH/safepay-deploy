import sqlite3
from hashing import hash_password

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    balance REAL DEFAULT 50000
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    receiver_id TEXT,
    name TEXT,
    gender TEXT,
    age INTEGER,
    state TEXT,
    city TEXT,
    branch TEXT,
    acc_type TEXT,
    amount REAL,
    txntype TEXT,
    merchant TEXT,
    balance REAL,
    enc_data TEXT,
    hash TEXT,
    signature BLOB,
    verified TEXT
)
""")

# --- Lightweight migrations for existing databases ---
# Ensure users.balance exists
cur.execute("PRAGMA table_info(users)")
user_cols = [r[1] for r in cur.fetchall()]
if "balance" not in user_cols:
    cur.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 50000")
    cur.execute("UPDATE users SET balance=50000 WHERE balance IS NULL")

# Ensure users.id exists and username is UNIQUE with id as PRIMARY KEY
cur.execute("PRAGMA table_info(users)")
user_info = cur.fetchall()
has_id_col = any(col[1] == "id" for col in user_info)
if not has_id_col:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users_new(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            balance REAL DEFAULT 50000
        )
    """)
    cur.execute("INSERT OR REPLACE INTO users_new (username, password, role, balance) SELECT username, password, role, COALESCE(balance, 50000) FROM users")
    cur.execute("DROP TABLE users")
    cur.execute("ALTER TABLE users_new RENAME TO users")

# Ensure transactions.receiver_id exists
cur.execute("PRAGMA table_info(transactions)")
txn_cols = [r[1] for r in cur.fetchall()]
if "receiver_id" not in txn_cols:
    cur.execute("ALTER TABLE transactions ADD COLUMN receiver_id TEXT")

cur.executemany("INSERT OR IGNORE INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)", [
    ("user1", hash_password("1234"), "user", 50000.0),
    ("user2", hash_password("1234"), "user", 50000.0),
    ("admin", hash_password("admin"), "admin", 50000.0),
    ("demo", hash_password("demo123"), "user", 75000.0)
])

con.commit()
con.close()
print("Database initialized!")
