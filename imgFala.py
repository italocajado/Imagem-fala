import cv2
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import threading

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

class ImagemFala:
    def __init__(self, master):
        self.master = master
        self.master.title("Imagem-Fala")
        self.cam = cv2.VideoCapture(0)

        # Label for displaying the camera feed
        self.lmain = Label(master)
        self.lmain.pack()

        # Label for displaying the text description of the image
        self.label_texto = Label(master, text="Descrição da imagem:", font=("Helvetica", 12))
        self.label_texto.pack()

        # Button for capturing an image
        self.button_capturar = Button(master, text="Capturar Imagem", command=self.capture)
        self.button_capturar.pack()

        # Button for extracting text from an image
        self.button_descricao = Button(master, text="Extrair Texto", command=self.desc_imagem)
        self.button_descricao.pack()

        # Call the ventana function
        self.ventana()

    def ventana(self):
        # Get the current frame
        ret, frame = self.cam.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img_tk = Image.fromarray(cv2image)
            self.img_tk = ImageTk.PhotoImage(self.img_tk)
            self.lmain.configure(image=self.img_tk)
            self.lmain.image = self.img_tk

            # Call the function to extract the text in a separate thread
            threading.Thread(target=self.desc_imagem, args=(cv2image,)).start()

        # Schedule the function to be called again after 1 millisecond
        self.master.after(1, self.ventana)
        threading.Thread(target=self.desc_imagem).start()

    def capture(self):
        # Get the current frame
        ret, frame = self.cam.read()

        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img_tk = Image.fromarray(cv2image)
            self.img_tk = ImageTk.PhotoImage(self.img_tk)
            self.lmain.configure(image=self.img_tk)
            self.lmain.image = self.img_tk

            descricao = self.desc_imagem(cv2image)
            self.label_texto.config(text=descricao)

            # Save the image
            img = Image.fromarray(cv2image)
            img.save("capture.png")
            messagebox.showinfo("Informação", "Imagem capturada com sucesso!")

        else:
            messagebox.showerror("Erro", "Erro ao capturar a imagem.")

    def desc_imagem(self, event=None):
        if self.img_tk is not None:
            img = Image.fromarray(self.img_tk)
            text_desc = pytesseract.image_to_string(img, lang='por')
            return text_desc
        else:
            return 'Sem descrição'
        
    def close_app(self):
        self.close_camera()
        self.master.destroy()

    def close_camera(self):
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    root = Tk()
    my_gui = ImagemFala(root)
    root.mainloop()