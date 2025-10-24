import sqlite3

def init_db(db_path="testcases.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_testcases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            testcase_description TEXT NOT NULL,
            pattern TEXT,
            api_name TEXT NOT NULL,
            request_type TEXT NOT NULL,
            testcase_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()