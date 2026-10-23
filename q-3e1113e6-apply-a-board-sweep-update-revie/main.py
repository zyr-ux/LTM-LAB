import sqlite3

def sample_board():
    return [
        {'title': 'A', 'status': 'review', 'priority': 5},
        {'title': 'B', 'status': 'review', 'priority': 1},
        {'title': 'C', 'status': 'todo',   'priority': 2},
        {'title': 'D', 'status': 'done',   'priority': 4},
    ]

def apply_changes(rows, min_priority):
    # Load rows, UPDATE review->done (capture rowcount),
    # then DELETE priority < min_priority (capture rowcount).
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""create table task(id integer primary key autoincrement,title text, status text, priority int)""")
    values = [(row['title'],row['status'],row['priority']) for row in rows]
    cursor.executemany("""insert into task (title,status,priority) values (?,?,?)""",values)

    cursor.execute("""update task set status=? where status=?""",('done','review'))
    updated=cursor.rowcount
    cursor.execute("""delete from task where priority<?""",(min_priority,))
    deleted=cursor.rowcount
    conn.commit()
    conn.close()
    return {'updated':updated,'deleted':deleted}
    pass