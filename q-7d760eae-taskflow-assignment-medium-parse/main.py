import csv
import io


def parse_tasks_csv(csv_text):
    if not csv_text or not csv_text.strip():
        return []
    reader = csv.DictReader(io.StringIO(csv_text))
    out = []
    for row in reader:
        # TODO: skip rows with a blank id
        # TODO: build a typed dict (int id, stripped title, int/0 points, bool done)
        if not row['id'].strip():
            continue
        task={
            'id':int(row['id']),
            'title':row['title'].strip(),
            'points': int(row['points']) if row['points'].strip() else 0,
            'done':row['done'].strip().lower() == 'true'
        }
        out.append(task)
        pass
    return out