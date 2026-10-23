import sqlite3

def sample_users():
    return [
        {"id": 1, "name": "Ana"},
        {"id": 2, "name": "Ben"},
        {"id": 3, "name": "Cara"},
        {"id": 4, "name": "Dan"},
    ]

def sample_tasks():
    return [
        {"id": 100, "title": "Design schema", "assignee_id": 1},
        {"id": 101, "title": "Build API",     "assignee_id": 2},
        {"id": 102, "title": "Write tests",   "assignee_id": 1},
        {"id": 103, "title": "Setup CI",      "assignee_id": None},
        {"id": 104, "title": "Deploy",        "assignee_id": 3},
        {"id": 105, "title": "Docs",          "assignee_id": 2},
    ]

def no_tasks():
    return []

def alt_tasks():
    return [
        {"id": 201, "title": "A1", "assignee_id": 1},
        {"id": 202, "title": "A2", "assignee_id": 2},
        {"id": 203, "title": "A3", "assignee_id": None},
        {"id": 204, "title": "A4", "assignee_id": 1},
        {"id": 205, "title": "B1", "assignee_id": 3},
        {"id": 206, "title": "B2", "assignee_id": 2},
    ]

def task_count_per_user(users, tasks):
    # LEFT JOIN users to tasks so EVERY user appears, even one with no tasks.
    # Return a list of (user_name, task_count) tuples ordered by user name, with
    # COALESCE/COUNT giving 0 for users who have no assigned tasks.
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""create table users(id integer primary key,name text)""")
    cursor.execute("""create table tasks(id integer primary key,title text, assignee_id integer)""")

    for user in users:
        cursor.execute("""INSERT INTO users (id,name) VALUES (?,?)""",(user['id'],user['name']))

    for task in tasks:
        cursor.execute("""INSERT INTO tasks (id,title,assignee_id) VALUES (?,?,?)""",(task['id'],task['title'],task.get('assignee_id')))
    
    cursor.execute("""select users.name,coalesce(count(tasks.id),0) as task_count from users left join tasks on users.id = tasks.assignee_id group by users.id,users.name order by users.name""")
    result=cursor.fetchall()
    conn.close()
    return result

    pass