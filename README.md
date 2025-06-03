
## 🚀 Project Setup Instructions

Follow these steps to get your Flask project up and running:

---

### 1. ✅ Create a virtual environment
```bash
python3 -m venv .venv
```

---

### 2. ✅ Activate the virtual environment
```bash
source .venv/bin/activate
```

---

### 3. ✅ Install required dependencies
```bash
pip install -r requirements.txt
```

---

### 4. ✅ Open the app directory
```bash
cd app
```

---

### 5. ⚙️ Set up the environment files

#### `.env`
```dotenv
SECRET_KEY=<your_secret_key>
JWT_SECRET_KEY=<your_jwt_secret_key>
DATABASE_URL=<your_database_url>
```

#### `.flaskenv`
```dotenv
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
```

---

### 6. 🔙 Go back to the main project directory
```bash
cd ..
```

---

### 7. 🛠️ Initialize the database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### 8. 🚦 Run the server
```bash
flask run
```

---

🎉 **Congratulations!** Your server is now running at:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)
