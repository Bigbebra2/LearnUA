1) Creating a virtual environment:
python3 -m venv .venv

2) Activating the virtual enviroment
source .venv/bin/activate

3) Setting up the necessary dependencies:
pip install -r requirements.txt

4) Opening the app directory:
cd app

5) Stting up the .env and .flaskenv files:
// .env

SECRET_KEY=<your_secret_key>
JWT_SECRET_KEY=<your_jwt_secret_key>
DATABASE_URL=<your_database_url>

// .flaskenv

FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

6) Go back to the main directory:
cd ..

7) Init the database
flask db init
flask db migrate
flask db upgrade


8) Run the server:
flask run

Congratulations! Now server is running on http://127.0.0.1:5000 (by default)







