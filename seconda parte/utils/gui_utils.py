from PIL import Image

def scala_proporzioni(img, max_lato):
    """
    Ridimensiona l'immagine mantenendo le proporzioni in modo che la dimensione massima (larghezza o altezza) sia max_size.
    """
    w, h = img.size
    scale = min(max_lato / w, max_lato / h)
    new_size = (int(w * scale), int(h * scale))
    img_resized = img.resize(new_size, Image.LANCZOS)
    return img_resized, new_size
