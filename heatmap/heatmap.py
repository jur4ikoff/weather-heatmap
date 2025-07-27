import math
import numpy as np
import os
from PIL import Image
import colorsys


MIN_TEMP = -50
MAX_TEMP = 50


class HetmapDataEmptyException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            self.message = "Error, weather matrix is empty"
        else:
            self.message = message

    def __str__(self):
        return f"raise Exception, message: {self.message}"
    
class HeatmapFileNotFoundException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            self.message = "Error, file not exist"
        else:
            self.message = message

    def __str__(self):
        return f"raise Exception, message: {self.message}"

class HeatmapErrImageException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            self.message = "Error image"
        else:
            self.message = message

    def __str__(self):
        return f"raise Exception, message: {self.message}"

class HeatMap:
    def __init__(self, filepath, weather_matrix):
        self.filepath = filepath
        self.output = filepath

        self.weather_matrix = weather_matrix
        self.height = len(self.weather_matrix)

        if self.height == 0:
            raise HetmapDataEmptyException()
        else:
            self.width = len(self.weather_matrix[0])

        if not os.path.exists(self.filepath):
            raise HeatmapFileNotFoundException()

        try:
            self.open_image() 
        except Exception as e:
            print(e)
            raise HeatmapErrImageException()

    def get_heatmap(self):
        heatmap_rgb = self.generate_gradient(self.weather_matrix)

        result = self.overlay_blend(self.image, heatmap_rgb)
        result = (np.clip(result, 0, 1) * 255).astype(np.uint8)

        pil_image = Image.fromarray(result)
        # pil_image.show()
        pil_image.save(self.output)

    def open_image(self):
        image_pil = Image.open(self.filepath)
        self.image = np.array(image_pil, dtype=np.float32) / 255.0
        self.image = self.grayscale_weighted(self.image)
        


    def generate_gradient(self, weather_data):
        gradient = np.zeros((self.height, self.width, 3),
                            dtype=np.uint8)  # 3 channels for RGB
        for i in range(self.height):
            for j in range(self.width):
                temp = weather_data[i][j]

                rgb_color = self.get_color_by_weather(temp)
                gradient[i][j] = rgb_color

        return gradient

    def overlay_blend(self, image, color):
        return image * (color / 255.0)
        # # Проверяем, нужно ли нормализовать (если значения в [0, 255])
        # if image.dtype == np.uint8 or np.max(image) > 1.0:
        #     base = image.astype(np.float32) / 255.0
        # else:
        #     base = image.copy()

        # if color.dtype == np.uint8 or np.max(color) > 1.0:
        #     overlay = color.astype(np.float32) / 255.0
        # else:
        #     overlay = color.copy()

        # # Применение формулы Overlay с np.where (автоматически работает по каналам)
        # result = np.where(base < 0.5, 2 * base * overlay,
        #                   1 - 2 * (1 - base) * (1 - overlay))

        # # Возврат в исходный диапазон
        # if image.dtype == np.uint8 or np.max(image) > 1.0:
        #     result = (result * 255).clip(0, 255).astype(np.uint8)

        # return result

    @staticmethod
    def get_color_by_weather(temperature: int) -> np.array:
        """Функция возвращает цвет погоды по температуе. Возвращеемый тип: 
        np.array([x, y, z], dtype=np.float32)"""

        if temperature < MIN_TEMP:
            temperature = MIN_TEMP
        if temperature > MAX_TEMP:
            temperature = MAX_TEMP

        temperature += math.fabs(MIN_TEMP)
        delta_temp = MAX_TEMP - MIN_TEMP

        temp_koef = temperature / delta_temp
        temp_koef = 1 - temp_koef
        temp_koef *= 0.7  # Умножаем, потому что используем не всю часть круга

        h, s, v = temp_koef, 1.0, 1.0  # HSB (180°, 80%, 90%)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)  # Возвращает значения в [0, 1]

        # Масштабирование до [0, 255] (если нужно)
        r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
        return np.array([r_int, g_int, b_int])

    def grayscale_weighted(self, image):
        return image.mean(axis=2, keepdims=True)


if __name__ == "__main__":
    color = HeatMap.get_color_by_weather(-20)
    print(color)
