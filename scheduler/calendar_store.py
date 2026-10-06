from database.db import get_connection

def save_calendar_item(platform, title, scheduled_at, status="Draft"):
    con = get_connection()
    con.execute("INSERT INTO calendar(platform,title,scheduled_at,status) VALUES (?,?,?,?)",
                (platform, title, scheduled_at, status))
    con.commit()
    con.close()

def list_calendar_items():
    con = get_connection()
    rows = con.execute("SELECT platform,title,scheduled_at,status FROM calendar ORDER BY scheduled_at").fetchall()
    con.close()
    return [{"platform": r[0], "title": r[1], "scheduled_at": r[2], "status": r[3]} for r in rows]
