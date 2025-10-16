# SafePay - Secure Payment System

A secure payment system with cryptographic protection featuring AES-256 encryption, SHA-256 hashing, and RSA-2048 digital signatures.

## Features

- **User Authentication**: Secure login/signup with PBKDF2-SHA256 password hashing
- **Encrypted Transactions**: All transaction data encrypted with AES-256-CBC
- **Digital Signatures**: RSA-2048 signatures for transaction verification
- **Balance Management**: Real-time balance tracking and updates
- **Admin Dashboard**: Comprehensive view of all users and transactions
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS

## Security Features

- **AES-256 Encryption**: Industry-standard encryption for sensitive data
- **SHA-256 Hashing**: Cryptographic hashing for data integrity
- **RSA-2048 Signatures**: Digital signatures for authentication
- **PBKDF2 Password Hashing**: 200,000 iterations for secure password storage
- **HMAC Verification**: Message authentication codes for encrypted data

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd safepay-deploy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python db.py
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

### Default Credentials

- **User 1**: username: `user1`, password: `1234`
- **User 2**: username: `user2`, password: `1234`
- **Admin**: username: `admin`, password: `admin`
- **Demo User**: username: `demo`, password: `demo123`

## Deployment on Render.com

### Method 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and deploy

### Method 2: Manual Setup

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: safepay
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

### Important Notes for Deployment

- The database (`database.db`) and encryption key (`aes_key.bin`) will be created automatically during the build process
- For production, consider using a persistent database like PostgreSQL
- Update the `app.secret_key` in `app.py` to a secure random value
- The SQLite database will reset on each deployment (use persistent storage for production)

## Project Structure

```
safepay-deploy/
├── app.py                 # Main Flask application
├── db.py                  # Database initialization
├── encryption.py          # AES encryption/decryption
├── hashing.py            # Password hashing and SHA-256
├── digital_signature.py  # RSA digital signatures
├── requirements.txt      # Python dependencies
├── build.sh             # Build script for Render
├── render.yaml          # Render deployment configuration
├── .gitignore           # Git ignore file
├── templates/           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── transaction.html
│   ├── transaction_result.html
│   └── admin_dashboard.html
└── static/              # Static files (if needed)
```

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Cryptography**: cryptography library (AES, RSA, SHA-256)
- **Frontend**: HTML, Tailwind CSS, Font Awesome
- **Deployment**: Gunicorn, Render.com

## API Routes

- `GET/POST /` - Login page
- `GET/POST /signup` - User registration
- `GET /dashboard` - User/Admin dashboard
- `GET/POST /transaction` - Create new transaction
- `GET /logout` - Logout user

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
