import sqlite3

DB_PATH = "testcases.db"


def save_testcase(
    testcase_description,
    pattern,
    api_name,
    request_type,
    testcase_type,
    db_path=DB_PATH,
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO api_testcases (testcase_description, pattern, api_name, request_type, testcase_type)
        VALUES (?, ?, ?, ?, ?)
    """,
        (testcase_description, pattern, api_name, request_type, testcase_type),
    )
    conn.commit()
    conn.close()


def get_testcases(api_name=None, testcase_type=None, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM api_testcases"
    params = []
    if api_name and testcase_type:
        query += " WHERE api_name = ? AND testcase_type = ?"
        params = [api_name, testcase_type]
    elif api_name:
        query += " WHERE api_name = ?"
        params = [api_name]
    elif testcase_type:
        query += " WHERE testcase_type = ?"
        params = [testcase_type]
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
