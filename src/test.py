from utils import in_range

def disconect(board, i, j, n, m):
        dx = [0,  0, 1, -1]
        dy = [1, -1, 0,  0]    
        visited = [False]*(n*m)
        visited[i*n + j] = True
        
        ni, nj = next(filter(lambda x: in_range(board, x[0], x[1]) and board[x[0]][x[1]] != 'O', 
                            [(i + dx[idx], j + dy[idx]) for idx in range(len(dx))]))
        visited[ni*n + nj] = True
        queue = [(ni, nj)]
        while queue:
            i, j = queue.pop()
            
            for idx in range(len(dx)):
                n_i, n_j = i + dx[idx], j + dy[idx]
                if in_range(board, n_i, n_j) and not visited[n_i*n + n_j]:
                    if not board[n_i][n_j] == 'O' and not board[n_i][n_j] == 'C':
                        queue.insert(0, (n_i, n_j))
                    visited[n_i*n + n_j] = True 
        return not all(visited)

board = [
    ['R', '.', '.', '.', 'O'],
    ['C', 'C', '.', '.', 'O'],
    ['.', '.', 'D', 'O', 'O'],
    ['O', 'O', 'O', '.', '.'],
    ['.', 'D', '.', 'K', 'K']
]

print(disconect(board, 3, 0, 5, 5))