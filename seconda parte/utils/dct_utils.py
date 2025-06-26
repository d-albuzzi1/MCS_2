import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

def process_image(img_path, F, d):
    """
    Esegue la compressione DCT sull'immagine al percorso image_path usando i parametri F e d.
    Restituisce l'immagine compressa e l'immagine della differenza.
    """
    image = Image.open(img_path).convert("L")
    img_array = np.array(image, dtype=np.float64)

    h, w = img_array.shape
    h_crop = h - h % F
    w_crop = w - w % F
    img_array = img_array[:h_crop, :w_crop]

    output = np.zeros_like(img_array)

    def dct2(block):
        return dct(dct(block.T, norm='ortho').T, norm='ortho')

    def idct2(block):
        return idct(idct(block.T, norm='ortho').T, norm='ortho')

    for i in range(0, h_crop, F):
        for j in range(0, w_crop, F):
            block = img_array[i:i+F, j:j+F]
            c = dct2(block)

            for k in range(F):
                for l in range(F):
                    if k + l >= d:
                        c[k, l] = 0

            block_rec = idct2(c)
            block_rec = np.clip(np.round(block_rec), 0, 255)
            output[i:i+F, j:j+F] = block_rec

    # Calcola immagine di differenza
    amplification_factor=4
    diff_array = np.abs(img_array - output) * amplification_factor
    diff_array = np.clip(diff_array, 0, 255).astype(np.uint8)
    diff_image = Image.fromarray(diff_array)

    return Image.fromarray(output.astype(np.uint8)), diff_image


