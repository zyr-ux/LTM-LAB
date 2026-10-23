import itertools


def paginate(items, size):
    """Lazily yield successive lists ('pages') of up to `size` items
    from the iterable `items`. If size <= 0, yield nothing.
    Hint: iter(items) + itertools.islice.
    """

    if size<=0:
        return
    
    it = iter(items)

    while True:
        page = list(itertools.islice(it,size))
        if not page:
            break
        
        yield page
    # TODO
    pass


def find_first(events, status):
    """Return the 'id' of the first event whose 'status' matches,
    else None. Use next(<generator expression>, None).
    """
    # TODO
    return next((event.get('id') for event in events if event.get('status')==status),None)
    pass