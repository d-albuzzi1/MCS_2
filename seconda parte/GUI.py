import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from utils.dct_utils import process_image
from utils.gui_utils import scala_proporzioni
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DCTApp(ctk.CTk):
    def __init__(self):
        """
        Inizializzazione della finestra GUI, configurazione del layout.
        """
        super().__init__()

        self.title("Compressione Immagine BMP")
        self.geometry("1080x720")

        # Frame laterale con pulsanti e input
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(side="left", padx=10, pady=20, fill="y")

        self.select_button = ctk.CTkButton(self.control_frame, text="Seleziona immagine BMP", command=self.select_image)
        self.select_button.pack(pady=10)

        self.f_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Ampiezza F (es. 8, 16,32+)", width=180)
        self.f_entry.pack(pady=10)

        self.d_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Soglia d (es. F-1)", width=180)
        self.d_entry.pack(pady=10)

        self.confirm_button = ctk.CTkButton(self.control_frame, text="Comprimi immagine", command=self.apply_dct)
        self.confirm_button.pack(pady=10)

        # Etichetta per il file selezionato
        self.file_label = ctk.CTkLabel(self, text="Nessun file selezionato")
        self.file_label.pack(pady=5)

        # Frame centrale per le immagini
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(pady=0)

        # Variabili
        self.image_path = None

    def select_image(self):
        """
        Apre un file dialog per selezionare un'immagine BMP, aggiorna l'interfaccia mostrando
        il nome del file selezionato, carica e mostra l'immagine originale ridimensionata.
        """
        filetypes = [("Bitmap Images", "*.bmp")]
        path = filedialog.askopenfilename(title="Scegli un'immagine BMP", filetypes=filetypes)
        if path:
            self.image_path = path
            original_size = os.path.getsize(self.image_path)
            self.file_label.configure(text=os.path.basename(path))

            # Mostra immagine originale
            self.original_img = Image.open(path).convert("L")
            img_resized, size = scala_proporzioni(self.original_img, 300)
            self.original_size = size
            self.tk_image_original = ctk.CTkImage(light_image=img_resized, size=size)

            if hasattr(self, "original_label"):
                self.original_label.configure(image=self.tk_image_original)
            else:
                self.original_label = ctk.CTkLabel(self.image_frame, image=self.tk_image_original, text="")
                self.original_label.grid(row=0, column=0, padx=10, pady=10)

                self.original_text = ctk.CTkLabel(self.image_frame, text=f"Originale: {original_size / 1024:.2f} KB")
                self.original_text.grid(row=1, column=0)

    def apply_dct(self):
        """
        Esegue la compressione dell'immagine selezionata tramite DCT, utilizzando i parametri F e d inseriti dall'utente.
        """
        if not self.image_path:
            print("Nessun file selezionato.")
            return

        try:
            F = int(self.f_entry.get())
            d = int(self.d_entry.get())
            if not (0 <= d <= (2 * F - 2)):
                raise ValueError("d fuori intervallo.")
        except ValueError as e:
            print("Errore nei parametri:", e)
            return

        # Esegui DCT
        img_result, diff_image = process_image(self.image_path, F, d)

        # Visualizza immagine compressa
        img_result_resized, size_result = scala_proporzioni(img_result, 300)

        temp_path = "temp_compressed.bmp"
        img_result.save(temp_path)
        compressed_size = os.path.getsize(temp_path)
        os.remove(temp_path)

        self.tk_image_result = ctk.CTkImage(light_image=img_result_resized, size=self.original_size)

        # Visualizza immagine differenza
        diff_image_resized, size_diff = scala_proporzioni(diff_image, 300)
        self.tk_image_diff = ctk.CTkImage(light_image=diff_image_resized, size=self.original_size)

        # Label dell'immagine compressa
        if hasattr(self, "result_label"):
            self.result_label.configure(image=self.tk_image_result)
        else:
            self.result_label = ctk.CTkLabel(self.image_frame, image=self.tk_image_result, text="")
            self.result_label.grid(row=0, column=1, padx=10, pady=10)

            self.result_text = ctk.CTkLabel(self.image_frame, text=f"Compressa: {compressed_size / 1024:.2f} KB")
            self.result_text.grid(row=1, column=1)

        # Label dell'immagine differenza
        if hasattr(self, "diff_label"):
            self.diff_label.configure(image=self.tk_image_diff)
        else:
            self.diff_label = ctk.CTkLabel(self.image_frame, image=self.tk_image_diff, text="")
            self.diff_label.grid(row=2, column=0, columnspan=2, pady=10)

            self.diff_text = ctk.CTkLabel(self.image_frame, text="Differenza")
            self.diff_text.grid(row=3, column=0, columnspan=2)

app = DCTApp()
app.mainloop()
