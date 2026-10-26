import sqlite3


def tasks_by_status(tasks, status):
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE tasks (id INTEGER, title TEXT, status TEXT)')

    # Insert every task row using a parameterised INSERT (avoids SQL injection)
    for task in tasks:
        conn.execute(
            'INSERT INTO tasks (id, title, status) VALUES (?, ?, ?)',
            (task['id'], task['title'], task['status'])
        )

    conn.commit()

    # Run a parameterised SELECT — the status value is passed as a parameter, never glued into the SQL
    cursor = conn.execute(
        'SELECT id, title, status FROM tasks WHERE status = ? ORDER BY id ASC',
        (status,)
    )

    # Convert each row (tuple) into a plain dict
    result = []
    for row in cursor.fetchall():
        result.append({'id': row[0], 'title': row[1], 'status': row[2]})

    conn.close()
    return result