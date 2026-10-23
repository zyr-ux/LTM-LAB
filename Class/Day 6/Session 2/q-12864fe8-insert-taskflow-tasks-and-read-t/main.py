import sqlite3

def sample_tasks():
    return [
        {'title': 'Write spec', 'status': 'todo', 'priority': 5},
        {'title': 'Build API', 'status': 'in_progress', 'priority': 4},
        {'title': 'Review PR', 'status': 'todo', 'priority': 2},
        {'title': 'Ship v1', 'status': 'done', 'priority': 3},
    ]

def insert_and_fetch(rows, status):
    # Create an in-memory DB, parameterised-insert every row,
    # then return the titles for `status` ordered by id.
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""create table task(id integer primary key autoincrement,title text, status text, priority int)""")
    values = [(row['title'],row['status'],row['priority']) for row in rows]
    cursor.executemany("""insert into task (title,status,priority) values (?,?,?)""",values)
    cursor.execute("""select title from task where status=? order by id """,(status,))
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result
    pass