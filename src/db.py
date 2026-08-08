import sqlite3
from datetime import datetime

DB = "interview_os.db"


def connect():
    return sqlite3.connect(DB)


def init_db():
    con = connect()

    con.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            score INTEGER,
            created_at TEXT,
            summary TEXT,
            data TEXT
        )
    """)

    con.commit()
    con.close()


def save_session(candidate, report):
    import json

    con = connect()

    con.execute(
        """
        INSERT INTO interviews
        (name, role, score, created_at, summary, data)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            candidate["name"],
            candidate["role"],
            int(report.get("overall_score", 0)),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            report.get("candidate_pattern", ""),
            json.dumps({
                "candidate": candidate,
                "report": report
            })
        )
    )

    con.commit()
    con.close()


def get_history():
    con = connect()

    rows = con.execute(
        """
        SELECT name, role, score, created_at, summary
        FROM interviews
        ORDER BY id DESC
        """
    ).fetchall()

    con.close()

    return [
        {
            "name": row[0],
            "role": row[1],
            "score": row[2],
            "created_at": row[3],
            "summary": row[4]
        }
        for row in rows
    ]
