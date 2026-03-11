from fastapi import FastAPI
import mysql.connector
import time

app = FastAPI()

db = None
cursor = None


@app.on_event("startup")
def startup():
    global db, cursor

    while True:
        try:
            db = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="appdb"
            )
            cursor = db.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
            """)

            print("Connected to MySQL")
            break

        except Exception as e:
            print("Waiting for MySQL...", e)
            time.sleep(5)


@app.get("/")
def home():
    return {"message": "Backend Running"}


@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


@app.post("/add-user")
def add_user(name: str, email: str):
    cursor.execute(
        "INSERT INTO users (name,email) VALUES (%s,%s)",
        (name, email)
    )
    db.commit()

    return {"message": "User added"}
