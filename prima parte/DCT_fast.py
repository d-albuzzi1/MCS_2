from scipy.fftpack import dct

def dct2d_fast(matrix):
    """
    Versione veloce della DCT2 usando scipy.fftpack.dct.
    Applica DCT lungo righe, poi colonne (trasposizione).
    """
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')
