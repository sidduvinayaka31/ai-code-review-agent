import sqlite3
import hashlib

def get_user_data(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # High Severity: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

def hash_password(password):
    # Medium/High Severity: Weak Hashing Algorithm (MD5)
    return hashlib.md5(password.encode()).hexdigest()

def process_data(data):
    # Code Smell / Anti-pattern: Too much complexity / nested loops
    result = []
    for i in data:
        if i > 0:
            for j in range(i):
                if j % 2 == 0:
                    for k in range(j):
                        if k == 1:
                            result.append(k)
    return result
