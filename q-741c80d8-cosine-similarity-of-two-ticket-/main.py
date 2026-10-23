import numpy as np

def cosine_similarity(a, b):
    # Return the cosine similarity of vectors a and b, rounded to 6 decimals.
    # Return 0.0 if either vector has zero magnitude.
    a = np.asarray(a,dtype=float)
    b = np.asarray(b,dtype=float)

    denom = np.linalg.norm(a)*np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(round(np.dot(a,b)/denom,6))