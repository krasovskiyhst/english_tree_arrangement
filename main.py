import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class TileCalculator:

    def __init__(self, room, tile, start_tiling, angle):
        self.start_tiling = {'x': start_tiling[0], 'y': start_tiling[1]}  # Координаты начала оси укладки
        self.point_1 = self.start_tiling  # Начальные координаты 1 точки
        self.point_2 = self.start_tiling  # Начальные координаты 2 точки
        self.point_3 = self.start_tiling  # Начальные координаты 3 точки
        self.point_4 = self.start_tiling  # Начальные координаты 4 точки
        self.fig, self.ax = plt.subplots()
        self.room_length, self.room_width = room  # Длина и ширина помещения
        self.tile_length, self.tile_width = tile  # Длина и ширина плитки
        self.angle = angle  # Угол сдвига оси укладки
        self.right = True  # Переключает направление плиток. Начинаем с правой

    def _shift_axle(self):
        self.start_tiling = {
            "x": self.start_tiling["x"] + self.tile_length,
            "y": self.start_tiling["y"] - self.tile_length
        }
        self.point_1 = self.start_tiling
        self.point_2 = self.start_tiling
        self.point_3 = self.start_tiling
        self.point_4 = self.start_tiling
        return

    def _create_a_room(self):
        self.ax.add_patch(
            patches.Rectangle(
                (0, 0),
                self.room_length,
                self.room_width,
                edgecolor='#2E4C61',
                facecolor='#6AB1E0',
                fill=True
            )
        )

    def _get_item_bound(self):
        sin_angle = math.sin(math.radians(self.angle))
        shift_x = self.tile_length * sin_angle
        shift_y = self.tile_width * sin_angle

        self.point_1 = self.point_4  # Первая точка плитки всегда совпадает с последней точкой предыдущей плитки
        # То, что далее находится в скобках, например (self.point_1["x"] + self.tile_length)
        # это логика построения самих плиток, но не сдвига.
        if self.right:
            # Построение правой плитки
            self.point_2 = {
                "x": (self.point_1["x"] + self.tile_length) - shift_x,
                "y": self.point_1["y"] + shift_x
            }
            self.point_3 = {
                "x": self.point_2["x"] - shift_y,
                "y": (self.point_2["y"] + self.tile_width) - shift_y
            }
            self.point_4 = {
                "x": (self.point_3["x"] - self.tile_length) + shift_x,
                "y": self.point_3["y"] - shift_x
            }
        else:
            # Построение левой плитки
            self.point_2 = {
                "x": self.point_1["x"] - shift_x,
                "y": (self.point_1["y"] + self.tile_length) - shift_x
            }
            self.point_3 = {
                "x": (self.point_2["x"] + self.tile_width) - shift_y,
                "y": self.point_2["y"] + shift_y
            }
            self.point_4 = {
                "x": self.point_3["x"] + shift_x,
                "y": (self.point_3["y"] - self.tile_length) + shift_x
            }

        self.right = not self.right  # Меняем направление

        if self.point_1["y"] >= self.room_width:
            # Если нижняя часть плитки касается
            # или выходит за верхнюю стену комнаты, то сдвигаем ось укладки
            self.right = True
            self._shift_axle()
        if self.start_tiling["x"] > self.room_length:
            # Останавливаем, если ось укладки выходит за правую стену комнаты
            return None

        ################
        # Визульное построение плиток
        plt.plot([
            self.point_1["x"],
            self.point_2["x"],
            self.point_3["x"],
            self.point_4["x"],
        ],
            [
                self.point_1["y"],
                self.point_2["y"],
                self.point_3["y"],
                self.point_4["y"]
            ],
        )
        ################

        return [self.point_1, self.point_2, self.point_3, self.point_4]

    def get_items(self):
        self._create_a_room()
        # Цикл, в котором строим только несколько плиток
        for i in range(200):
            item = self._get_item_bound()
            print(item)
            if not item:
                break

        # # Цикл, который будет использоваться в итоге (все плитки)
        # while True:
        #     item = self._get_item_bound()
        #     print(item)
        #     if not item:
        #         break

        plt.show()  # Показать окно


if __name__ == '__main__':
    # Входящие данные
    ROOM = (600, 600)  # x(room_length), y(room_width)
    TILE = (200, 40)  # Плитка
    START_TILING = (0, 0)  # Начало оси укладки
    ANGLE = 30  # Угол поворота оси укладки. Пока оси сдвигаются корректно при 0 и 30 градусах

    session_calculate = TileCalculator(ROOM, TILE, START_TILING, ANGLE)
    session_calculate.get_items()
