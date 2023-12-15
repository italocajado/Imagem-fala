import cv2
import numpy as np
import tensorflow
import keras
import yolo

def desc_imagem(self, imagem=None):
    if imagem is not None:
        # Carregar o modelo YOLOv3 pré-treinado
        net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # Converter a imagem para blob e detectar objetos
        blob = cv2.dnn.blobFromImage(imagem, 1/255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Desenhar caixas delimitadoras e rotular objetos detectados
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Ajustar as coordenadas das caixas delimitadoras à altura e largura da imagem
                    box = detection[0:4] * np.array([imagem.shape[1], imagem.shape[0], imagem.shape[1], imagem.shape[0]])
                    (centerX, centerY, width, height) = box.astype("int")

                    # Desenhar a caixa delimitadora e o rótulo
                    label = str(class_id)
                    cv2.rectangle(imagem, (centerX - width // 2, centerY - height // 2), (centerX + width // 2, centerY + height // 2), (0, 0, 255), 2)
                    cv2.putText(imagem, label, (centerX - width // 2, centerY - height // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Exibir a imagem com objetos detectados
        cv2.imshow("Imagem", imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        return ""