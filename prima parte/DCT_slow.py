import numpy as np

def dct1d(x):
    """
    Calcola la DCT 1D di un vettore x.
    """
    N = len(x)
    result = np.zeros(N)

    for k in range(N):
        somma = 0.0
        for n in range(N):
            angolo = (np.pi * k * (2 * n + 1)) / (2 * N)
            coseno = np.cos(angolo)
            somma += x[n] * coseno

        if k == 0:
            alpha = np.sqrt(1 / N)
        else:
            alpha = np.sqrt(2 / N)

        result[k] = alpha * somma

    return result


def dct2d_slow(matrix):
    """
    Calcola la DCT 2D applicando dct1d su righe e colonne.
    """
    N = matrix.shape[0]
    temp = np.zeros_like(matrix)

    # DCT su ogni riga
    for i in range(N):
        temp[i, :] = dct1d(matrix[i, :])

    # DCT su ogni colonna
    for j in range(N):
        temp[:, j] = dct1d(temp[:, j])

    return temp

