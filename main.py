import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class TileCalculator:

    def __init__(self, room, tile, start_tiling, angle):
        self.room_length, self.room_width = room  # Длина и ширина помещения
        self.tile_length, self.tile_width = tile  # Длина и ширина плитки
        self.angle = angle - 45  # Угол оси укладки
        shift_x, shift_y = start_tiling[0], start_tiling[1]
        if angle < 45:
            if start_tiling[0] > self.tile_length:
                shift_x = 0
            if start_tiling[1] < 0:
                shift_y = 0
            self.start_tiling = {'x': -self.room_length + shift_x, 'y': self.room_width + shift_y}
        elif angle >= 45 and angle < 90:
            if start_tiling[0] > self.tile_length:
                shift_x = 0
            if start_tiling[1] < 0 or start_tiling[1] > self.room_width:
                shift_y = 0
            self.start_tiling = {'x': -self.room_length + shift_x - self.room_width, 'y': 0 + shift_y}
        elif angle >= 90:
            if start_tiling[0] > self.tile_length:
                shift_x = 0
            if start_tiling[1] + self.tile_length > 0:
                shift_y = 0
            self.start_tiling = {'x': -self.room_length + shift_x, 'y': -self.room_width + shift_y}

        self.fig, self.ax = plt.subplots()

    def _shift_axle(self):
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

    def show_tiles(self, items, color=None):
        for item in items:
            plt.plot([
                item[0]["x"],
                item[1]["x"],
                item[2]["x"],
                item[3]["x"],
                item[0]["x"],
            ],
                [
                    item[0]["y"],
                    item[1]["y"],
                    item[2]["y"],
                    item[3]["y"],
                    item[0]["y"],
                ],
                color=color,
                # linestyle=(0, (5, 2, 1, 2)),
            )
            # plt.plot([
            #     item[0]["x"],
            #     item[1]["x"],
            #     item[2]["x"],
            # ],
            #     [

            #         item[0]["y"],
            #         item[1]["y"],
            #         item[2]["y"],
            #     ],
            #     color='red',
            #     linestyle=(0, (5, 2, 1, 2)),
            # )

    def _remove_redundant_items(self, item):
        if item[0]["x"] > self.room_length and item[1]["x"] > self.room_length and item[2]["x"] > self.room_length and \
                item[3]["x"] > self.room_length:
            return

        if item[0]["y"] > self.room_width and item[1]["y"] > self.room_width and item[2]["y"] > self.room_width and \
                item[3]["y"] > self.room_width:
            return

        if item[0]["x"] < 0 and item[1]["x"] < 0 and item[2]["x"] < 0 and item[3]["x"] < 0:
            return
        if item[0]["y"] < 0 and item[1]["y"] < 0 and item[2]["y"] < 0 and item[3]["y"] < 0:
            return

        return True

    def _get_item_bound(self, x, y, angle, right):
        point_1 = {"x": x, "y": y}
        if right:
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
            direction = {"right": True}
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
            direction = {"right": False}

        return [point_1, point_2, point_3, point_4, direction]

    def get_the_tiles_included_in_the_room(self, items):
        items_in_the_toom = []
        for item in items:
            if item[0]["x"] > self.room_length or item[1]["x"] > self.room_length or item[2]["x"] > self.room_length or \
                    item[3]["x"] > self.room_length:
                continue

            if item[0]["y"] > self.room_width or item[1]["y"] > self.room_width or item[2]["y"] > self.room_width or \
                    item[3]["y"] > self.room_width:
                continue

            if item[0]["x"] < 0 or item[1]["x"] < 0 or item[2]["x"] < 0 or item[3]["x"] < 0:
                continue
            if item[0]["y"] < 0 or item[1]["y"] < 0 or item[2]["y"] < 0 or item[3]["y"] < 0:
                continue
            items_in_the_toom.append(item)

        return items_in_the_toom

    def get_items(self):
        self._create_a_room()
        items = []
        x = self.start_tiling["x"]
        y = self.start_tiling["y"]
        right = True
        while True:
            item = self._get_item_bound(x, y, self.angle, right)
            right = not right  # Меняем направление
            x, y = item[3]["x"], item[3]["y"]
            if item[0]["y"] - self.tile_length > self.room_width or item[0]["x"] - self.tile_length > self.room_length:
                right = True
                x, y = self._shift_axle()
            if self.start_tiling["x"] - self.room_length > self.room_length:
                break
            if self.start_tiling["y"] + self.room_width < -self.room_width:
                break
            if not self._remove_redundant_items(item):
                continue

            items.append(item)

        return items


if __name__ == '__main__':
    ROOM = (600, 820)  # x(room_length), y(room_width)
    TILE = (200, 40)  # Плитка
    START_TILING = (-100, 0)  # Начало оси укладки
    ANGLE = 45  # Угол поворота оси укладки. Пока оси сдвигаются корректно при 0 и 30 градусах

    session_calculate = TileCalculator(ROOM, TILE, START_TILING, ANGLE)
    items = session_calculate.get_items()
    print(len(items))
    session_calculate.show_tiles(items, '#DCE1F5')
    items_in_the_toom = session_calculate.get_the_tiles_included_in_the_room(items)
    print(items_in_the_toom)
    print(len(items_in_the_toom))
    session_calculate.show_tiles(items_in_the_toom,  'green')
    plt.show()  # Показать окно
