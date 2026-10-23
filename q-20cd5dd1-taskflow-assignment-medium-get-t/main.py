def handle_list_tasks(query, tasks):
    result = list(tasks)
    # 1. filter by status if provided
    # 2. validate + apply limit if provided (422 on bad limit)
    # 3. return {'status_code': 200, 'body': result}
    pass
    result = list(tasks)

    if 'status' in query:
        result = [t for t in result if t.get('status') == query['status']]

    
    if 'limit' in query:
        try:
            limit = int(query['limit'])
            if limit <=0:
                raise ValueError
        except (ValueError, TypeError):
            return {
                'status_code':422,
                'body':{'error':'invalid limit'}
            }

        result = result[:limit]

    return {
        'status_code':200,
        'body':result
    }