import numpy as np

def ticket_matrix():
    # Fixed 5x4 matrix of TaskFlow ticket embeddings used by the tests.
    return np.array([[1.0,0.0,0.0,0.0],[0.0,0.1,0.0,0.0],[0.9,0.1,0.0,0.0],[0.0,0.0,1.0,0.0],[0.5,0.0,0.5,0.0]])
    pass

def top_k(matrix, query, k):
    # Return the k rows most similar to query by cosine similarity, best first,
    # as a list of [row_index, rounded_score]. Break ties by smaller index.
    query = np.asarray(query,dtype=float)
    scored = []
    for index,row in enumerate(matrix):
        denom = np.linalg.norm(row)*np.linalg.norm(query)
        if denom == 0:
            score = 0.0
        else:
            score = np.dot(row,query)/denom
        
        score = float(round(score,6))
        scored.append([index,score])
    
    scored.sort(key=lambda x:(-x[1],x[0]))
    return scored[:k]
    pass