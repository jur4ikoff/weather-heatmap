from src.weather import WeatherManager
from models.weather import WeatherPoint
from models.geo import Geo

from time import time

import numpy as np
from scipy.interpolate import griddata
import asyncio


class WeatherMatrixRequestErr(Exception):
    def __init__(self, message=None):
        if message == None:
            self.message = "Error, size of request and response data is different"
        else:
            self.message = message

    def __str__(self):
        return f"raise Exception, message: {self.message}"


class WeatherMatrix:
    def __init__(self, leftdown: Geo, rightupper: Geo, width: int, height: int, proxy: str = None):
        self.proxy = proxy
        self.leftdown: Geo = leftdown
        self.rightupper: Geo = rightupper

        self.width: int = width
        self.height: int = height
        # self.width = 10
        # self.height = 5

        self.matrix: list[list[WeatherPoint]] = [
            [0] * self.width for _ in range(self.height)]

        dlat = (self.rightupper.latitude -
                self.leftdown.latitude) / (self.height - 1)
        dlong = (self.rightupper.longitude -
                 self.leftdown.longitude) / (self.width - 1)

        for i in range(self.height):
            for j in range(self.width):
                latitude = self.leftdown.latitude + i * dlat
                longitude = self.leftdown.longitude + j * dlong

                temp_geo: Geo = Geo(latitude=latitude, longitude=longitude)
                self.matrix[i][j] = WeatherPoint(
                    coordinates=temp_geo, temperature=None)

    async def request_weather(self, count_by_lat: int, count_by_long: int):
        """Функция запрашивает погоду в точках по latitude и longitude.
        count_by_lat, count_by_long: Количество точек на каждой оси"""
        print("starting request weather")
        
        dlat_index = self.height / count_by_lat
        dlong_index = self.width / count_by_long

        weather_manager = WeatherManager(self.proxy)
        tasks = []
        indexes = []

        cur_lat_index, cur_long_index = 0, 0
        while cur_lat_index < self.height:
            while cur_long_index < self.width:
                i = round(cur_lat_index)
                j = round(cur_long_index)
                indexes.append((i, j))
                temp_geo: Geo = self.matrix[i][j].coordinates
                task = asyncio.create_task(
                    weather_manager.get_weather_in_point_v1(temp_geo))
                tasks.append(task)

                cur_long_index += dlong_index

            cur_long_index = self.width - 1
            i = round(cur_lat_index)
            j = round(cur_long_index)
            indexes.append((i, j))
            temp_geo: Geo = self.matrix[i][j].coordinates
            task = asyncio.create_task(
                weather_manager.get_weather_in_point_v1(temp_geo))
            tasks.append(task)

            cur_long_index = 0
            cur_lat_index += dlat_index

        results = await asyncio.gather(*tasks)

        if len(results) != len(indexes):
            raise WeatherMatrixRequestErr()

        for k in range(len(indexes)):
            i, j = indexes[k]
            self.matrix[i][j].temperature = results[k]

    def interpolate(self):
        # Ваша матрица (пример)

        time_start = time()
        matrix = np.empty((self.height, self.width), dtype=float)

        for i in range(self.height):
            for j in range(self.width):
                temperature = self.matrix[i][j].temperature
                matrix[i, j] = temperature if temperature is not None else np.nan

        rows, cols = np.where(~np.isnan(matrix))
        values = matrix[~np.isnan(matrix)]

        # 2. Создаем сетку для всех точек матрицы
        grid_rows, grid_cols = np.mgrid[0:matrix.shape[0], 0:matrix.shape[1]]

        # 3. Интерполяция (линейная, кубическая или nearest)
        interpolated = griddata(
            (rows, cols),
            values,
            (grid_rows, grid_cols),
            method='linear',  # или 'nearest', 'cubic'
            fill_value=np.nan  # если не удалось интерполировать
        )

        # 4. Заполнение оставшихся NaN (если нужно)
        # Например, заменим их на среднее значение
        interpolated = np.where(
            np.isnan(interpolated),
            np.nanmean(interpolated),
            interpolated
        )

        print(
            f"Function interpolate working for {time() - time_start} seconds")
        return interpolated

    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.matrix[i][j])
