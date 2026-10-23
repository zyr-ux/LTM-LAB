import numpy as np

def total_estimated_hours(estimates):
    # TODO: if estimates is not a list, return None
    # TODO: if any entry is None or non-numeric, return None (never NaN)
    # TODO: empty list -> 0
    # TODO: build a float NumPy array and return int(arr.sum())
    
    
    if type(estimates) is not list:
        return
    
    for estimate in estimates:
        if estimate is None:
            return None
        if not isinstance(estimate, (int,float)):
            return None

    if len(estimates)==0:
        return 0
    
    arr = np.array(estimates,dtype=float)

    return int(arr.sum())
    pass