def extract_tasks(response):
    # Return a sorted list of normalised task dicts from an API response.

    if not isinstance(response,dict) or response.get('status') != 'ok':
        return []

    result = []

    for row in response.get('data') or []:
        if row.get('id') is None:
            continue

        try:
            task_id = int(row['id'])
        except (TypeError,ValueError):
            continue

        title = str(row.get('title', '')).strip()

        status = str(row.get('status','')).strip().lower()
        if status not in {'todo','in_progress','review','done'}:
            status = 'todo'

        try:
            priority = int(row.get('priority',3))
        except (TypeError, ValueError):
            priority = 3

        priority = max(1,min(5,priority))

        result.append({'id':task_id,'title':title,'status':status,'priority':priority})

    return sorted(result,key=lambda t:t['id'])
    pass


def api_fixture():
    return {
        "status": "ok",
        "data": [
            {"id": 3, "title": "  Ship release  ", "status": "In_Progress", "priority": "2"},
            {"id": 1, "title": "Fix login bug", "status": "TODO", "priority": 9},
            {"id": 2, "title": "Write docs", "priority": None},
            {"id": None, "title": "orphan", "status": "done"},
        ],
    }