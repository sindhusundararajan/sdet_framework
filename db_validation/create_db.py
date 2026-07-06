import sqlite3
import os


def create_test_database():
    db_path = os.path.join(os.path.dirname(__file__), "test_etl.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SOURCE TABLE — raw data before ETL
    # Simulates SAP or MySQL source
    cursor.execute("Drop Table if exists source_employees")
    cursor.execute("""
            CREATE TABLE source_employees(
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   department TEXT,
                   salary REAL,
                   status TEXT
                   )
    """)

# Insert 10 source records — 2 are inactive (should be filtered by ETL)
    cursor.executemany("""
            INSERT INTO source_employees VALUES(?,?,?,?,?)
    """, [
        (1,  "Leanne Graham",   "Engineering", 95000, "active"),
        (2,  "Ervin Howell",    "Marketing",   72000, "active"),
        (3,  "Clementine",      "Engineering", 88000, "active"),
        (4,  "Patricia Lebsack", "Finance",      91000, "active"),
        (5,  "Chelsey Dietrich", "HR",           67000, "active"),
        (6,  "Mrs. Dennis",     "Engineering", 102000, "active"),
        (7,  "Kurtis Weissnat", "Marketing",   74000, "active"),
        (8,  "Nicholas Runolfsdottir", "Finance", 85000, "active"),
        (9,  "Glenna Reichert", "HR",           69000, "inactive"),  # filtered
        (10, "Clementina DuBuque", "Engineering", 97000, "inactive"),   # filtered
    ])

    cursor.execute("DROP TABLE IF EXISTS dest_employees")
    cursor.execute("""
            CREATE TABLE dest_employees (
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   department TEXT,
                   salary REAL,
                   annual_bonus REAL -- new column added by ETL transform
                   )
    """)

    # LOAD only active employees + calculate bonus (10% of salary)
    cursor.executemany("""
            INSERT INTO dest_employees VALUES(?,?,?,?,?)
    """, [
        (1,  "Leanne Graham",   "Engineering", 95000,  9500.0),
        (2,  "Ervin Howell",    "Marketing",   72000,  7200.0),
        (3,  "Clementine",      "Engineering", 88000,  8800.0),
        (4,  "Patricia Lebsack", "Finance",      91000,  9100.0),
        (5,  "Chelsey Dietrich", "HR",           67000,  6700.0),
        (6,  "Mrs. Dennis",     "Engineering", 102000, 10200.0),
        (7,  "Kurtis Weissnat", "Marketing",   74000,  7400.0),
        (8,  "Nicholas Runolfsdottir", "Finance", 85000,  8500.0),
    ])

    conn.commit()
    conn.close()
    print(f"Database created at: {db_path}")
    return db_path


if __name__ == "__main__":
    create_test_database()
