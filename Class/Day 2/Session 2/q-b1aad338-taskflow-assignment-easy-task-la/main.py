def format_task_label(title='untitled', status='todo'):
    # TODO: if title is empty or None, replace it with 'untitled'
    # TODO: return '[STATUS] Title' with STATUS uppercased
    if title=="" or title==None:
        title='untitled'
    
    return (f"[{status.upper()}] {title}")

