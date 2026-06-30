import sqlite3, sys, traceback

DB = "task_manager.db"
OUT = "dump.sql"

def integrity(conn):
    cur = conn.execute("PRAGMA integrity_check;")
    return cur.fetchone()

def dump_sql(conn, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")

try:
    conn = sqlite3.connect(DB)
    print("Running PRAGMA integrity_check...")
    res = integrity(conn)
    print("integrity_check:", res)
    if res and res[0] == "ok":
        print("Dumping database to", OUT)
        dump_sql(conn, OUT)
        print("Dump complete.")
    else:
        print("Integrity check failed; still attempting partial dump.")
        try:
            dump_sql(conn, OUT)
            print("Partial dump saved to", OUT)
        except Exception:
            traceback.print_exc()
    conn.close()
except Exception:
    traceback.print_exc()
    sys.exit(1)