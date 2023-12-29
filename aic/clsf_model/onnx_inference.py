import cv2 as cv
import numpy as np
import onnxruntime as ort


class Inference:
    def __init__(self, model_path="./model.onnx"):
        self.sess = ort.InferenceSession(model_path)
        self.MEAN = np.array([0.079, 0.05, 0]) + 0.406
        self.STD = np.array([0.005, 0, 0.001]) + 0.224

    def _preprocess_img(self, image, height=224, width=224):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (height, width))
        image_data = image.transpose([2, 0, 1])  # transpose to CHW
        for channel in range(image_data.shape[0]):
            image_data[channel, :, :] = (
                image_data[channel, :, :] / 255 - self.MEAN[channel]
            ) / self.STD[channel]
        image_data = np.expand_dims(image_data, 0)
        return image_data

    def _index_to_label(self, ind):
        with open("./labels.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]
        return categories[ind]

    def _predict(self, image):
        output = self.sess.run([], {"input": image})[0]
        output = output.flatten()
        return np.argmax(output)

    def __call__(self, img):
        img = self._preprocess_img(img)
        ind = self._predict(img)
        label = self._index_to_label(ind)
        return label
