from fastapi import FastAPI
import psycopg2
import os
import time

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            conn = get_connection()
            conn.close()
            return True
        except Exception:
            retries -= 1
            time.sleep(3)
    return False

@app.on_event("startup")
def startup():
    if not wait_for_db():
        raise Exception("Could not connect to database after retries")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(100),
            location VARCHAR(100)
        );
    """)
    cur.execute("SELECT COUNT(*) FROM employees;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO employees (name, department, location) VALUES (%s, %s, %s);",
            [
                ("Alice Johnson", "Engineering", "Bangalore"),
                ("Bob Smith", "DevOps", "Mumbai"),
                ("Carol White", "Data & AI", "Hyderabad"),
                ("David Brown", "Cloud", "Pune"),
                ("Eva Green", "Security", "Delhi"),
                ("Frank Lee", "Engineering", "Chennai"),
                ("Grace Kim", "DevOps", "Bangalore"),
            ]
        )
    conn.commit()
    cur.close()
    conn.close()

@app.get("/")
def root():
    return {"message": "NAGP K8s Assignment - API is running"}

@app.get("/employees")
def get_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, department, location FROM employees;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "department": r[2], "location": r[3]}
        for r in rows
    ]
