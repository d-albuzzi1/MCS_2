import numpy as np
import matplotlib.pyplot as plt
import time
import os
import csv

from DCT_fast import dct2d_fast
from DCT_slow import dct2d_slow, dct1d

# Blocco di input di esempio (8x8)
blocco = np.array([
    [231, 32, 233, 161, 24, 71, 140, 245],
    [247, 40, 248, 245, 124, 204, 36, 107],
    [234, 202, 245, 167, 9, 217, 239, 173],
    [193, 190, 100, 167, 43, 180, 8, 70],
    [11, 24, 210, 177, 81, 243, 8, 112],
    [97, 195, 203, 47, 125, 114, 165, 181],
    [193, 70, 174, 167, 41, 30, 127, 245],
    [87, 149, 57, 192, 65, 129, 178, 228]
], dtype=np.float64)

# Risultato atteso DCT2 8x8 (per confronto)
blocco_atteso = np.array([
    [1.11e+03, 4.40e+01, 7.59e+01, -1.38e+02, 3.50e+00, 1.22e+02, 1.95e+02, -1.01e+02],
    [7.71e+01, 1.14e+02, -2.18e+01, 4.13e+01, 8.77e+00, 9.90e+01, 1.38e+02, 1.09e+01],
    [4.48e+01, -6.27e+01, 1.11e+02, -7.63e+01, 1.24e+02, 9.55e+01, -3.98e+01, 5.85e+01],
    [-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01, 2.66e+01, -3.68e+01, 6.61e+01, 1.25e+02],
    [-1.09e+02, -4.33e+01, -5.55e+01, 8.17e+00, 3.02e+01, -2.86e+01, 2.44e+00, -9.41e+01],
    [-5.38e+00, 5.66e+01, 1.73e+02, -3.54e+01, 3.23e+01, 3.34e+01, -5.81e+01, 1.90e+01],
    [7.88e+01, -6.45e+01, 1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02, 3.98e+01],
    [1.97e+01, -7.81e+01, 9.72e-01, -7.23e+01, -2.15e+01, 8.13e+01, 6.37e+01, 5.90e+00]
])

# Risultato atteso DCT1 della prima riga (per confronto)
riga_attesa = np.array([[4.01e+02, 6.60e+0, 1.09e+02, -1.12e+02, 6.54e+01, 1.21e+02, 1.16e+02, 2.88e+01]])

def benchmark_dct2():
    """
    Confronta le prestazioni di DCT2 lenta e veloce su matrici di diverse dimensioni.
    Misura i tempi e salva results e grafico.
    """
    Ns = [8, 16, 32, 64, 128, 256, 512]
    times_slow = []
    times_fast = []

    for N in Ns:
        matrix = np.random.rand(N, N)

        # Tempo DCT2 lenta
        start = time.perf_counter()
        dct2d_slow(matrix)
        elapsed_slow = time.perf_counter() - start
        times_slow.append(elapsed_slow)

        # Tempo DCT2 veloce
        start = time.perf_counter()
        dct2d_fast(matrix)
        elapsed_fast = time.perf_counter() - start
        times_fast.append(elapsed_fast)

        print(f"N={N}: slow={elapsed_slow:.4f}s, fast={elapsed_fast:.4f}s")

    # Crea la cartella results se non esiste
    os.makedirs("results", exist_ok=True)

    # Salva i results in CSV
    with open("results/benchmark_results.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Dimensione N", "Tempo DCT2 Lenta (s)", "Tempo DCT2 Veloce (s)"])
        for n, slow, fast in zip(Ns, times_slow, times_fast):
            writer.writerow([n, slow, fast])

    # Grafico semilogaritmico
    plt.figure(figsize=(8, 6))
    plt.semilogy(Ns, times_slow, 'o-', label='DCT2 lenta (O(N³))')
    plt.semilogy(Ns, times_fast, 's-', label='DCT2 veloce (O(N² logN))')
    plt.xlabel("Dimensione matrice N")
    plt.ylabel("Tempo di esecuzione (s)")
    plt.title("Confronto DCT2 lenta vs veloce")
    plt.legend()
    plt.grid(True, which="both", linestyle="--")
    plt.tight_layout()

    # Salva il grafico come immagine
    plt.savefig("results/confronto_dct2.png")
    plt.show()


if __name__ == "__main__":

    os.makedirs("results", exist_ok=True)

    print("========== TEST DI ACCURATEZZA ==========")
    print("Input (prima riga del blocco):")
    print(blocco[0, :])

    risultato_1d = dct1d(blocco[0, :])
    print("\nDCT1D :")
    print(np.round(risultato_1d, 2))
    np.savetxt("results/dct1_riga.csv", risultato_1d, delimiter=",", fmt="%.4f")
    print("Risultato atteso:")
    print(riga_attesa)

    risultato_2d = dct2d_slow(blocco)
    print("\nDCT2 :")
    print(np.round(risultato_2d, 2))
    np.savetxt("results/dct2_blocco.csv", risultato_2d, delimiter=",", fmt="%.4f")
    print("Risultato atteso:")
    print(blocco_atteso)


    print("\n========== TEST DI PERFORMANCE ==========")
    benchmark_dct2()
