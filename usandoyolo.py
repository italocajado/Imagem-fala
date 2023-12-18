import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import gtts

def detect_and_convert(image):
    model = load_model('yolov3.h5') # Load the trained YOLO model
    labels = open('labels.txt').read().strip().split('\n') # Read labels from the text file

    # Preprocess the image and run it through the model
    image = cv2.resize(image, (416, 416))
    image = image / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    detections = model.predict(image)
    boxes = []
    scores = []
    classIDs = []

    for i in range(0, detections.shape[2]):
        box = detections[0, 0, i, 0:4]
        score = detections[0, 0, i, 4]

        if score > 0.5:
            boxes.append(box)
            scores.append(score)
            classIDs.append(i)

    indices = cv2.dnn.NMSBoxes(boxes, scores, 0.5, 0.4)

    # Process each detected object
    for i in indices.flatten():
        box = boxes[i]
        x = int(box[0] * image.shape[1])
        y = int(box[1] * image.shape[0])
        w = int(box[2] * image.shape[1])
        h = int(box[3] * image.shape[0])

        label = labels[classIDs[i]]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert the detected object to audio
        audio = text_to_speech(label)

        # Save the audio to a file
        with open('output.wav', 'wb') as f:
            f.write(audio)

def text_to_speech(text):
    # Use a text-to-speech library to convert the text to audio
    tts = gtts.gTTS(text=text, lang='por')
    return tts.save("output.wav")