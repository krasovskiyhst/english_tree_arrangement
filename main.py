import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class TileCalculator:

    def __init__(self, room, tile, start_tiling, angle):
        self.room_length, self.room_width = room  # Длина и ширина помещения
        self.tile_length, self.tile_width = tile  # Длина и ширина плитки
        self.angle = angle - 45  # Угол оси укладки
        if angle <= 45:
            self.start_tiling = {'x': -self.room_length, 'y': self.room_width}
        elif angle > 45 and angle < 75:
            self.start_tiling = {'x': -self.room_length, 'y': 0}
        elif angle >= 75:
            self.start_tiling = {'x': -self.room_length, 'y': -self.room_width}

        # self.start_tiling = {'x': start_tiling[0], 'y': start_tiling[1]}  # Координаты начала оси укладки
        self.fig, self.ax = plt.subplots()
        self.right = True  # Переключает направление плиток. Начинаем с правой

    def _shift_axle(self):
        self.right = True
        self.start_tiling = {
            "x": self.start_tiling["x"] + (2 ** 0.5) * self.tile_length * math.cos(math.radians(self.angle - 45)),
            "y": self.start_tiling["y"] + (2 ** 0.5) * self.tile_length * math.sin(math.radians(self.angle - 45))
        }
        x, y = self.start_tiling["x"], self.start_tiling["y"]
        return x, y

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

    def show_tiles(self, items):
        for item in items:
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

    def _tiles_in_the_room(self, item):
        # if item[0]["x"] > self.room_length and item[1]["x"] > self.room_length and item[2]["x"] > self.room_length and \
        #         item[3]["x"] > self.room_length:
        #     return

        # if item[0]["y"] > self.room_width and item[1]["y"] > self.room_width and item[2]["y"] > self.room_width and \
        #         item[3]["y"] > self.room_width:
        #     return
        if self.start_tiling["x"] > self.room_length:
            # Останавливаем, если начало оси укладки выходит за правую стену комнаты
            return
        return True

    def _get_item_bound(self, x, y, angle):
        point_1 = {"x": x, "y": y}
        if self.right:
            # Построение правой плитки
            point_2 = {
                "x": x + self.tile_length * math.cos(math.radians(angle)),
                "y": y + self.tile_length * math.sin(math.radians(angle))
            }
            point_3 = {
                "x": x + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.cos(
                    math.radians(angle + math.degrees(math.atan(self.tile_width / self.tile_length)))),
                "y": y + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.sin(
                    math.radians(angle + math.degrees(math.atan(self.tile_width / self.tile_length))))
            }
            point_4 = {
                "x": x + self.tile_width * math.cos(math.radians(angle + 90)),
                "y": y + self.tile_width * math.sin(math.radians(angle + 90))
            }
        else:
            # Построение левой плитки
            point_2 = {
                "x": x + self.tile_length * math.cos(math.radians(angle + 90)),
                "y": y + self.tile_length * math.sin(math.radians(angle + 90))
            }
            point_3 = {
                "x": x + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.cos(
                    math.radians(angle + (90 - math.degrees(math.atan(self.tile_width / self.tile_length))))),
                "y": y + (self.tile_length ** 2 + self.tile_width ** 2) ** 0.5 * math.sin(
                    math.radians(angle + (90 - math.degrees(math.atan(self.tile_width / self.tile_length)))))
            }
            point_4 = {
                "x": x + self.tile_width * math.cos(math.radians(angle)),
                "y": y + self.tile_width * math.sin(math.radians(angle))
            }

        self.right = not self.right  # Меняем направление

        return [point_1, point_2, point_3, point_4]

    def get_items(self):
        self._create_a_room()
        items = []
        x = self.start_tiling["x"]
        y = self.start_tiling["y"]
        for i in range(400):
            item = self._get_item_bound(x, y, self.angle)
            x, y = item[3]["x"], item[3]["y"]
            if item[0]["y"] - self.tile_length >= self.room_width or item[0]["x"] - self.tile_width >= self.room_width:
                # Если нижняя часть плитки касается
                # или выходит за верхнюю стену комнаты, то сдвигаем ось укладки
                x, y = self._shift_axle()
            if not self._tiles_in_the_room(item):
                break

            print(item)
            items.append(item)
        self.show_tiles(items)
        return items


if __name__ == '__main__':
    # Входящие данные
    ROOM = (600, 600)  # x(room_length), y(room_width)
    TILE = (200, 40)  # Плитка
    START_TILING = (0, 0)  # Начало оси укладки
    ANGLE = 90  # Угол поворота оси укладки. Пока оси сдвигаются корректно при 0 и 30 градусах

    session_calculate = TileCalculator(ROOM, TILE, START_TILING, ANGLE)
    session_calculate.get_items()
