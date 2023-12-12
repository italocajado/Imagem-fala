from PIL import Image
import pytesseract
from gtts import gTTS
import os
import cv2
import tkinter as tk
from tkinter import ttk

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title('captura e descrição')

        self.btn_capture = ttk.Button(self.master, text="Tirar foto", command=self.tirar_foto)
        self.btn_capture.pack(pady=10)

        self.btn_process = ttk.Button(self.master, text="Processar e descrever", command=self.processar_desc)
        self.btn_process.pack(pady=10)

    def tirar_foto(self):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        name = 'foto.jpg'
        cv2.imwrite(name, frame)

    def processar_desc(self):
        caminho_img = 'foto.jpg'
        descricao = self.processar_img(caminho_img)
        self.desc_fala(descricao)         

    def processar_img(self, caminho_img):
        imagem = Image.open(caminho_img)
        text_desc = pytesseract.image_to_string(imagem)
        return text_desc

    def desc_fala(self, descricao):
        tts = gTTS(text=descricao, lang='pt')
        tts.save('descricao.mp3')
        os.system('start descricao.mp3')

def main():
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
