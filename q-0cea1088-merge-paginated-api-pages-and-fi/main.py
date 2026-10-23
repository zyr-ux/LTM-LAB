def merge_pages(pages, status=None):
    # Merge paginated response pages into one de-duplicated, sorted list.
    # If status is given, keep only tasks with that status.
    seen = set()
    result = []

    for page in sorted(pages, key = lambda p:p.get('page',0)):
        for task in page.get('results',[]):
            if task['id'] in seen:
                continue

            seen.add(task['id'])

            if status is not None and task.get('status')!=status:
                continue

            result.append(task)

    return sorted(result, key=lambda t: t['id'])
    pass


def pages_fixture():
    return [
        {"page": 2, "next": False, "results": [
            {"id": 4, "status": "done"},
            {"id": 5, "status": "todo"},
        ]},
        {"page": 1, "next": True, "results": [
            {"id": 1, "status": "todo"},
            {"id": 2, "status": "done"},
            {"id": 3, "status": "todo"},
            {"id": 4, "status": "done"},
        ]},
    ]