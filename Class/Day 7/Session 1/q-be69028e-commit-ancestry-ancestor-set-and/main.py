def dag_fixture():
    return [
        {'id': 'a', 'parents': []},
        {'id': 'b', 'parents': ['a']},
        {'id': 'c', 'parents': ['a']},
        {'id': 'm', 'parents': ['b', 'c']},  # merge commit
        {'id': 'd', 'parents': ['m']},
    ]

def ancestors(commits, commit_id):
    # sorted list of all transitive ancestor ids (excluding commit_id)
    lookup =  {c['id']: c for c in commits}

    if commit_id not in lookup:
        return []

    visited = set()
    stack = list(lookup[commit_id]['parents'])

    while stack:
        current  = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        if current in lookup:
            stack.extend(lookup[current]['parents'])

    return sorted(visited)
    pass

def is_ancestor(commits, a, b):
    # True if a is an ancestor of b
    return a in ancestors(commits,b)
    pass