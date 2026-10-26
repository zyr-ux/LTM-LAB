import sqlite3


def open_tasks_per_project(projects, tasks):
    conn = sqlite3.connect(':memory:')

    # Create the two tables
    conn.execute('CREATE TABLE projects (id INTEGER, name TEXT)')
    conn.execute('CREATE TABLE tasks (id INTEGER, project_id INTEGER, status TEXT)')

    # Insert every project using a parameterised INSERT (safe, no string interpolation)
    for project in projects:
        conn.execute('INSERT INTO projects (id, name) VALUES (?, ?)', (project['id'], project['name']))

    # Insert every task using a parameterised INSERT
    for task in tasks:
        conn.execute(
            'INSERT INTO tasks (id, project_id, status) VALUES (?, ?, ?)',
            (task['id'], task['project_id'], task['status'])
        )

    conn.commit()

    # LEFT JOIN so projects with zero tasks still appear.
    # SUM(CASE ...) counts tasks where status is NOT 'done'.
    # 'done' is bound as a parameter (?) — never interpolated into the SQL string.
    query = """
        SELECT
            p.id        AS project_id,
            p.name      AS name,
            SUM(CASE WHEN t.status != ? THEN 1 ELSE 0 END) AS open_count
        FROM projects AS p
        LEFT JOIN tasks AS t ON t.project_id = p.id
        GROUP BY p.id, p.name
        ORDER BY p.id ASC
    """
    cursor = conn.execute(query, ('done',))

    # Build a list of plain dicts from the query rows
    result = []
    for row in cursor.fetchall():
        result.append({
            'project_id': row[0],
            'name': row[1],
            'open_count': row[2],
        })

    conn.close()
    return result