import numpy as np

def estimate_summary(estimates):
    # TODO: non-list -> None
    # TODO: FILTER out None entries (unestimated tasks); non-numeric -> None
    # TODO: empty (or all-None) -> {'total':0,'mean':0.0,'std':0.0,'min':0.0,'max':0.0}
    # TODO: build float array; return total(int), mean/std/min/max rounded to 2 dp

    if type(estimates) is not list:
        # return {'total':0,'mean':0.0,'std':0.0,'min':0.0,'max':0.0}
        return None

    # if set(estimates) == {None}:
    #     return {'total':0,'mean':0.0,'std':0.0,'min':0.0,'max':0.0}

    for estimate in estimates:
        if estimate is str:
            return None

    clean_estimates = list(filter(None,estimates))

    if not clean_estimates:
        return {'total':0,'mean':0.0,'std':0.0,'min':0.0,'max':0.0}

    arr = np.array(clean_estimates,dtype=float)

    total = int(arr.sum())
    mean = arr.mean()
    
    return {'total':int(arr.sum()),
            'mean':round(arr.mean(),2),
            'std':round(arr.std(),2),
            'min':round(arr.min(),2),
            'max':round(arr.max(),2)
            }
    pass