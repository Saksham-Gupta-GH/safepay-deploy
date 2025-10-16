# Testing Guide

## Test Accounts

The database is initialized with 4 users:

| Username | Password | Role | Balance |
|----------|----------|------|---------|
| user1 | 1234 | user | ₹50,000 |
| user2 | 1234 | user | ₹50,000 |
| admin | admin | admin | ₹50,000 |
| demo | demo123 | user | ₹75,000 |

## Testing Transactions Between Users

### Scenario 1: user1 sends money to user2

1. **Login as user1**
   - Username: `user1`
   - Password: `1234`
   - Role: `user`

2. **Go to New Transaction**
   - Click "New Transaction" button

3. **Fill Transaction Form**
   - **Receiver Username**: `user2`
   - **Full Name**: `John Doe`
   - **Gender**: `Male`
   - **Age**: `25`
   - **State**: `California`
   - **City**: `Los Angeles`
   - **Bank Branch**: `Main Branch`
   - **Account Type**: `Savings`
   - **Amount**: `1000`
   - **Transaction Type**: `Online`
   - **Merchant Category**: `Retail`

4. **Submit Transaction**
   - Click "Process Secure Transaction"
   - Verify success page shows:
     - Amount transferred: ₹1,000
     - New balance: ₹49,000
     - Digital signature verified ✓

5. **Logout and Login as user2**
   - Username: `user2`
   - Password: `1234`
   - Role: `user`

6. **Verify Receipt**
   - Check dashboard balance: ₹51,000
   - View transaction history
   - Confirm transaction appears

### Scenario 2: user2 sends money back to user1

Repeat the process with user2 as sender and user1 as receiver.

### Scenario 3: Admin View

1. **Login as admin**
   - Username: `admin`
   - Password: `admin`
   - Role: `admin`

2. **View Admin Dashboard**
   - See all 4 users with their balances
   - View all transactions across the system
   - Verify transaction details (hash, signature, verification status)

## Security Features to Verify

### 1. Encryption
- All transaction data is encrypted with AES-256
- Check the `enc_data` column in transactions table

### 2. Hashing
- Transaction integrity verified with SHA-256
- Check the `hash` column in transactions table

### 3. Digital Signatures
- RSA-2048 signatures for authentication
- Check the `verified` column shows "True"

### 4. Balance Validation
- Try sending more than available balance → Should fail
- Try sending to yourself → Should fail
- Try sending to non-existent user → Should fail

## Database Inspection

```bash
# View all users
sqlite3 database.db "SELECT username, role, balance FROM users;"

# View all transactions
sqlite3 database.db "SELECT id, customer_id, receiver_id, amount, verified FROM transactions;"

# Check specific user balance
sqlite3 database.db "SELECT username, balance FROM users WHERE username='user1';"
```

## Error Testing

### Test Invalid Transactions

1. **Insufficient Balance**
   - Login as user1
   - Try to send ₹100,000 (more than balance)
   - Should show error: "Insufficient balance"

2. **Self Transfer**
   - Login as user1
   - Try to send to user1
   - Should show error: "Cannot transfer to self"

3. **Invalid Receiver**
   - Login as user1
   - Try to send to "nonexistent_user"
   - Should show error: "Receiver not found"

4. **Invalid Credentials**
   - Try to login with wrong password
   - Should show error: "Invalid credentials"

## Performance Testing

### Multiple Transactions
Create a series of transactions to test:
- Database integrity
- Balance calculations
- Transaction history display
- Admin dashboard performance

### Example Flow:
1. user1 → user2: ₹1,000
2. user2 → demo: ₹500
3. demo → user1: ₹2,000
4. user1 → user2: ₹3,000

Final balances should be:
- user1: ₹48,000 (50,000 - 1,000 - 3,000 + 2,000)
- user2: ₹51,500 (50,000 + 1,000 + 3,000 - 500)
- demo: ₹73,500 (75,000 + 500 - 2,000)

## UI Testing

### Desktop
- Test all pages on desktop browser
- Verify responsive design
- Check hover effects on cards and buttons
- Verify gradient backgrounds display correctly

### Mobile
- Test on mobile viewport
- Verify forms are usable
- Check table scrolling on small screens
- Verify navigation works

## Security Testing

### Session Management
1. Login as user1
2. Open new tab, try to access /dashboard without login
3. Should redirect to login page

### Password Security
1. Check database: `sqlite3 database.db "SELECT password FROM users LIMIT 1;"`
2. Password should be hashed (pbkdf2_sha256$...)
3. Never stored in plain text

### Cryptographic Verification
1. Complete a transaction
2. Check database for encrypted data
3. Verify signature is present
4. Confirm verification status is "True"

## Deployment Testing

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 db.py

# Run application
python3 app.py

# Test at http://localhost:5000
```

### Production Testing (After Render Deployment)
1. Access your Render URL
2. Test all scenarios above
3. Check Render logs for errors
4. Verify database persists between requests
5. Test SSL certificate (https://)

## Troubleshooting

### Database Issues
```bash
# Reset database
rm database.db
python3 db.py
```

### Encryption Key Issues
```bash
# Reset encryption key
rm aes_key.bin
# Restart app (new key will be generated)
```

### View Logs
- Local: Check terminal output
- Render: Check dashboard logs tab

## Success Criteria

✅ All 4 users can login  
✅ Users can send/receive money  
✅ Balances update correctly  
✅ Transactions are encrypted  
✅ Digital signatures verify  
✅ Admin can view all data  
✅ Error handling works  
✅ UI is responsive  
✅ Security features active  
✅ Deployment successful  
