import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class HeatMap:
    def __init__(self, filepath, weather_matrix):
        self.filepath = filepath
        self.filepath = "test.jpg"
        self.output = "out.jpg"

        self.weather_matrix = weather_matrix
        self.height = len(self.weather_matrix)
        self.width = len(
            self.weather_matrix[0]) if len(self.weather_matrix) > 0 else 0

        # self.image = cv2.imread(self.filepath)
        # self.image = Image.open(self.filepath)
        # image_np = np.array(self.image)

        image = Image.open(self.filepath)
        numpy_image = np.array(image, dtype=np.float32)

        gradient = np.linspace(0, 1, self.width)
        gradient = np.tile(gradient, (self.height, 1))

        # heatmap_rgb = self.gradient_to_heatmap(gradient)
        print(gradient)
        print("_________________________")
        self.weather_matrix = np.clip(self.weather_matrix, 0, 1) / 255.0
        print(self.weather_matrix)
        heatmap_rgb = self.gradient_to_heatmap(self.weather_matrix)

        # alpha = 0.5  # Прозрачность heatmap (0.0 = исходное, 1.0 = полный heatmap)
        # result = numpy_image * (1 - alpha) + heatmap_rgb * alpha

        result = numpy_image * heatmap_rgb
        result = (np.clip(result, 0, 1) * 255).astype(np.uint8)

        # tinted = (np.clip(tinted, 0, 1) * 255).astype(np.uint8)

        pil_image = Image.fromarray(result)
        pil_image.show()
        pil_image.save(self.output)
        # cv2.imwrite("output.jpg", cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

        # plt.figure(figsize=(10, 5))
        # plt.imshow(numpy_image)
        # plt.title("Blended with Red")
        # plt.show()

    def gradient_to_heatmap(self, gradient):
        r = np.clip(2.0 * gradient - 20, 0, 1)
        g = np.clip(2.0 * gradient - 40, 0, 1)
        b = np.clip(2.0 * gradient - 50, 0, 1)

        return np.stack([r, g, b], axis=-1)
    # def open_image(self):
