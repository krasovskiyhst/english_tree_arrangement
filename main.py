import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class TileCalculator:

    def __init__(self, room, tile, start_tiling, angle):
        self.room_length, self.room_width = room  # Длина и ширина помещения
        self.tile_length, self.tile_width = tile  # Длина и ширина плитки
        self.angle = angle - 45  # Угол сдвига оси укладки
        if angle <= 45:
            self.start_tiling = {'x': -self.room_length, 'y': self.room_width}
        elif angle > 45 and angle < 75:
            self.start_tiling = {'x': -self.room_length, 'y': 0}
        elif angle >= 75:
            self.start_tiling = {'x': -self.room_length, 'y': -self.room_width}

        # self.start_tiling = {'x': start_tiling[0], 'y': start_tiling[1]}  # Координаты начала оси укладки
        self.point_1 = self.start_tiling  # Начальные координаты 1 точки
        self.point_2 = self.start_tiling  # Начальные координаты 2 точки
        self.point_3 = self.start_tiling  # Начальные координаты 3 точки
        self.point_4 = self.start_tiling  # Начальные координаты 4 точки
        self.fig, self.ax = plt.subplots()
        self.right = True  # Переключает направление плиток. Начинаем с правой

    def _shift_axle(self):
        self.start_tiling = {
            "x": self.start_tiling["x"] + (2 ** 0.5) * self.tile_length * math.cos(math.radians(self.angle - 45)),
            "y": self.start_tiling["y"] + (2 ** 0.5) * self.tile_length * math.sin(math.radians(self.angle - 45))
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

        self.point_1 = self.point_4  # Первая точка плитки всегда совпадает с последней точкой предыдущей плитки

        if self.right:
            # Построение правой плитки
            self.point_2 = {
                "x": self.point_1["x"] + self.tile_length * math.cos(math.radians(self.angle)),
                "y": self.point_1["y"] + self.tile_length * math.sin(math.radians(self.angle))
            }
            self.point_3 = {
                "x": self.point_1["x"] + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.cos(
                    math.radians(self.angle + math.degrees(math.atan(self.tile_width / self.tile_length)))),
                "y": self.point_1["y"] + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.sin(
                    math.radians(self.angle + math.degrees(math.atan(self.tile_width / self.tile_length))))
            }
            self.point_4 = {
                "x": self.point_1["x"] + self.tile_width * math.cos(math.radians(self.angle + 90)),
                "y": self.point_1["y"] + self.tile_width * math.sin(math.radians(self.angle + 90))
            }
        else:
            # Построение левой плитки
            self.point_2 = {
                "x": self.point_1["x"] + self.tile_length * math.cos(math.radians(self.angle + 90)),
                "y": self.point_1["y"] + self.tile_length * math.sin(math.radians(self.angle + 90))
            }
            self.point_3 = {
                "x": self.point_1["x"] + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.cos(
                    math.radians(self.angle + (90 - math.degrees(math.atan(self.tile_width / self.tile_length))))),
                "y": self.point_1["y"] + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.sin(
                    math.radians(self.angle + (90 - math.degrees(math.atan(self.tile_width / self.tile_length)))))
            }
            self.point_4 = {
                "x": self.point_1["x"] + self.tile_width * math.cos(math.radians(self.angle)),
                "y": self.point_1["y"] + self.tile_width * math.sin(math.radians(self.angle))
            }

        self.right = not self.right  # Меняем направление

        if self.point_1["y"] - self.tile_length >= self.room_width:
            # Если нижняя часть плитки касается
            # или выходит за верхнюю стену комнаты, то сдвигаем ось укладки
            self.right = True
            self._shift_axle()
        if self.start_tiling["x"] > self.room_length:
            # Останавливаем, если начало оси укладки выходит за правую стену комнаты
            return None

        ################
        # Визульное построение плиток

        ################

        return [self.point_1, self.point_2, self.point_3, self.point_4]

    def get_items(self):
        self._create_a_room()
        items = []
        # Цикл, в котором строим только несколько плиток
        # for i in range(200):
        #     item = self._get_item_bound()
        #     print(item)
        #     if not item:
        #         break

        # # Цикл, который будет использоваться в итоге (все плитки)
        while True:
            item = self._get_item_bound()
            print(item)
            items.append(item)
            if not item:
                break

        for item in items:
            try:
                item[0]["x"]
            except:
                continue
            if item[0]["x"] > self.room_length and item[1]["x"] > self.room_length and item[2]["x"] > self.room_length and item[3]["x"] > self.room_length:
                items.remove(item)
                continue
            if item[0]["y"] > self.room_width and item[1]["y"] > self.room_width and item[2]["y"] > self.room_width and item[3]["y"] > self.room_width:
                items.remove(item)
                continue

            plt.plot([
                item[0]["x"],
                item[1]["x"],
                item[2]["x"],
                item[3]["x"],
            ],
                [
                    item[0]["y"],
                    item[1]["y"],
                    item[2]["y"],
                    item[3]["y"]
                ],
            )
        plt.show()  # Показать окно


if __name__ == '__main__':
    # Входящие данные
    ROOM = (600, 600)  # x(room_length), y(room_width)
    TILE = (200, 40)  # Плитка
    START_TILING = (0, 0)  # Начало оси укладки
    ANGLE = 30  # Угол поворота оси укладки. Пока оси сдвигаются корректно при 0 и 30 градусах

    session_calculate = TileCalculator(ROOM, TILE, START_TILING, ANGLE)
    session_calculate.get_items()
