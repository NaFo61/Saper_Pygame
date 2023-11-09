# -*- coding: utf-8 -*-
import datetime
import random
import sqlite3
import sys

import pygame

import config
import load
import style

__all__ = []


def get_text_color(text):
    """Определение цвета ячейки"""
    colors = {
        "F": style.cell_f,
        "1": style.cell_1,
        "2": style.cell_2,
        "3": style.cell_3,
        "4": style.cell_4,
    }
    return colors.get(text, style.cell_else)


class Bomb(pygame.sprite.Sprite):
    """
    Класс бомбы, имеет свойство картинки, а так же атрибуты положения
    """

    def __init__(self, x, y):
        super().__init__(all_sprites)
        global SCREEN_SIZE, value
        w, h = SCREEN_SIZE
        size = (w - 100) // value
        image = pygame.transform.scale(
            load.load_image("bomb.jpg", (255, 255, 255)),
            (size, size),
        )
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Board:
    """
    Класс поля, отвечает за отображение всего поля, мин, ячеек и тд
    """

    def __init__(self, screen_size, value, count):
        """Магический метод инициализации"""
        self.value = value
        self.count = count  # Количество мин

        w, h = screen_size

        self.left = 50
        self.top = 90
        self.cell_size = (w - 100) // self.value
        self.font_size = 65 - ((self.value - 8) * 5)

    @staticmethod
    def render_lose(screen):
        """Рисует надпись <Вы проиграли!>"""
        pygame.draw.rect(screen, style.BUTTON, (265, 10, 185, 70))

        font = pygame.font.SysFont("bahnschrift", 25)

        text = font.render("Вы проиграли!", True, style.TITLE)

        text_x = 357 - text.get_width() // 2
        text_y = 50 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))

    @staticmethod
    def render_restart(screen):
        """Рисует кнопку <Рестарт>"""
        pygame.draw.rect(screen, style.BUTTON, (50, 10, 185, 70))

        font = pygame.font.SysFont("bahnschrift", 35)

        text = font.render("Рестарт", True, style.TITLE)

        text_x = 142 - text.get_width() // 2
        text_y = 45 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))

    @staticmethod
    def draw_cell_rect(screen, cell_rect, flag, col):
        """Рисует белую ячейку"""
        border_color = pygame.Color("white")
        fill_color = pygame.Color(col)
        border_thickness = 1 if flag else 0

        pygame.draw.rect(screen, border_color, cell_rect, border_thickness)
        pygame.draw.rect(screen, fill_color, cell_rect.inflate(-2, -2), 0)

    def render(self, screen):
        """Метод, который отображает все поле"""
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if not self.lose_detect:
                    self.render_cell(screen, i, j)
                else:
                    self.render_end_game(screen, i, j)
                    # <======== Вы проиграли! ========>
                    self.render_lose(screen)
                    # <======== Вы проиграли! ========>

                    # <======== Рестарт ========>
                    self.render_restart(screen)
                    # <======== Рестарт ========>

    def render_end_game(self, screen, i, j):
        """Отображения проигрыша"""
        square = i * self.value + j
        if (self.map[i][j] == "F" and square in self.MINES) or self.map[i][
            j
        ] == "*":
            x, y = (
                self.left + j * self.cell_size,
                self.top + i * self.cell_size,
            )
            self.map[i][j] = "*"

            bomb: Bomb = Bomb(x, y)
            all_sprites.add(bomb)

            col = "red"
        elif self.map[i][j] == ".":
            col = "black"
        else:
            col = "grey"

        pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (
                self.left + j * self.cell_size,
                self.top + i * self.cell_size,
                self.cell_size,
                self.cell_size,
            ),
            1,
        )

        pygame.draw.rect(
            screen,
            pygame.Color(col),
            (
                self.left + j * self.cell_size + 1,
                self.top + i * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2,
            ),
            0,
        )
        if self.map[i][j] == ".":
            font = pygame.font.Font(None, self.font_size)
            text = font.render(str(" "), True, (255, 0, 0))
            text_x = self.left + j * self.cell_size + 10
            text_y = self.top + i * self.cell_size + 5
            screen.blit(text, (text_x, text_y))
        else:
            cnt = str(self.map[i][j])
            color = get_text_color(cnt)
            font = pygame.font.Font(None, self.font_size)
            text = font.render(str(self.map[i][j]), True, color)
            text_x = self.left + j * self.cell_size + 10
            text_y = self.top + i * self.cell_size + 5
            screen.blit(text, (text_x, text_y))

    def render_cell(self, screen, i, j):
        """Отображение ячейки"""
        cell_value = self.map[i][j]
        flag = cell_value != "." and cell_value != "*"
        col = "black" if cell_value == "*" or cell_value == "." else "grey"

        cell_rect = pygame.Rect(
            self.left + j * self.cell_size,
            self.top + i * self.cell_size,
            self.cell_size,
            self.cell_size,
        )

        self.draw_cell_rect(screen, cell_rect, flag, col)

        if flag:
            self.render_cell_text(screen, i, j)

    def render_cell_text(self, screen, i, j):
        """Отображение текста ячейки"""
        cell_value = str(self.map[i][j])
        color = get_text_color(cell_value)

        font = pygame.font.Font(None, self.font_size)
        text_rendered = font.render(cell_value, True, color)

        text_x = self.left + j * self.cell_size + 10
        text_y = self.top + i * self.cell_size + 5

        screen.blit(text_rendered, (text_x, text_y))


class Minesweeper(Board):
    """Главный класс сапера"""

    def __init__(self, screen, screen_size, value, count):
        """Метод инициализации"""
        super().__init__(screen_size, value, count)

        # <============ СЧЕТ ============>
        self.now = datetime.datetime.now()
        self.start_time = datetime.datetime.timestamp(self.now)
        self.finish_time = None
        self.points = None
        self.data = ":".join(
            reversed(str(self.now).split()[0].replace("-", ":").split(":")),
        )
        self.time = str(self.now).split()[1].split(".")[0]
        # <============ СЧЕТ ============>

        self.map = load.load_level()
        self.screen = screen

        self.value = value
        self.restart = False

        self.lose_detect = False

        self.win_detect = False

        self.count = count

        self.lst = []

        l_board = [i for i in range(value * value)]

        self.MINES = random.sample(l_board, k=count)  # Мины
        for mine in self.MINES:
            i, j = mine // value, mine % value
            self.lst.append(mine)
            self.map[i][j] = "*"

    def generate_neighbors(self, square):
        row, col = square % self.value, square // self.value
        neighbors = []
        for r in range(max(0, row - 1), min(self.value - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.value - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                neighbors.append(self.cell_to_square((r, c)))
        return neighbors

    def cell_to_square(self, cell):
        """Перевод клетки (i, j) -> square"""
        i, j = cell
        square = j * self.value + i
        return square

    def get_click(self, mouse_pos, first_move, flag):
        """Определение клика"""
        cell = self.get_cell(mouse_pos)
        if flag:
            self.open_cell(cell, first_move)
        else:
            self.open_flag(cell)

    def get_cell(self, mouse_pos):
        """Определение ячейки по координатам клика"""
        if (
                mouse_pos[0] < self.left
                or mouse_pos[0] > self.left + self.cell_size * len(self.map[0])
                or mouse_pos[1] < self.top
                or mouse_pos[1] > self.top + self.cell_size * len(self.map)
        ):
            return None
        return (
            (mouse_pos[0] - self.left) // self.cell_size,
            (mouse_pos[1] - self.top) // self.cell_size,
        )

    def open_flag(self, cell):
        """Открыть флаг"""
        if not self.lose_detect and not self.win_detect:
            j, i = cell
            square = self.cell_to_square(cell)

            if self.map[i][j] == "." or self.map[i][j] == "*":
                self.map[i][j] = "F"
            elif self.map[i][j] == "F":
                if square in self.MINES:
                    self.map[i][j] = "*"
                else:
                    self.map[i][j] = "."
            flag = self.check_win()
            if flag:
                self.win_detect = True
                self.win()

    def check_win(self):
        """Проверка на победу"""
        cnt = sum([i.count(".") for i in self.map])
        return True if not cnt else False

    def open_cell(self, cell, first_move=False):
        """Открытие ячейки"""
        if cell is None or self.lose_detect or self.win_detect:
            return

        j, i = cell
        square = self.cell_to_square(cell)

        if first_move and square in self.MINES:
            self.handle_first_move(square)

        if square in self.MINES:
            self.lose_detect = True
        elif square not in self.lst:
            self.lst.append(square)
            cnt = self.get_cnt_mines(square)
            if cnt:
                if self.map[i][j] == "." or self.map[i][j] == "f":
                    self.map[i][j] = cnt
            else:
                self.map[i][j] = " "
                self.recursively_open_neighbors(square)

            flag = self.check_win()
            if flag:
                self.win_detect = True
                self.win()

    def handle_first_move(self, square):
        """Открытие, когда это первый ход"""
        self.MINES.remove(square)
        self.lst.remove(square)

        i, j = square // self.value, square % self.value
        cnt = self.get_cnt_mines(square)

        if cnt:
            self.map[i][j] = cnt
        else:
            self.map[i][j] = " "

        mb_mines = [
            i
            for i in range(self.value * self.value)
            if i not in self.MINES and i != square
        ]

        mine = random.choice(mb_mines)
        i, j = mine // self.value, mine % self.value
        self.map[i][j] = "*"
        self.MINES.append(mine)
        self.lst.append(mine)

    def recursively_open_neighbors(self, square):
        """Открытие рекурсией по соседям"""
        data = self.generate_neighbors(square)
        sys.setrecursionlimit(3000)

        for neighbor_square in data:
            cell = (
                neighbor_square % self.value,
                neighbor_square // self.value,
            )
            self.open_cell(cell)

    def win(self):
        """Победа"""
        self.now = datetime.datetime.now()
        self.finish_time = datetime.datetime.timestamp(self.now)
        self.points = str(int(self.finish_time - self.start_time))
        self.win_detect = True
        win_screen(self.data, self.time, self.points)

    def get_cnt_mines(self, square):
        """Вывести количество мин вокруг клетки"""
        data = self.generate_neighbors(square)
        cnt = 0
        for i in data:
            if i in self.MINES:
                cnt += 1
        return cnt


def win_screen(data, time, points):
    """Экран победы"""
    global first_move, screen, SCREEN_SIZE
    first_move = True
    connect = sqlite3.connect("data/database.db")
    cursor = connect.cursor()

    width, height = SCREEN_SIZE

    fon = pygame.transform.scale(
        load.load_image("background.png"),
        SCREEN_SIZE,
    )
    screen.blit(fon, (0, 0))

    font = pygame.font.SysFont("bahnschrift", 50)
    text = font.render("Ты выиграл!", True, style.TITLE)

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 8 + 20 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))

    # ============================

    # <====== Главная рамка ======>
    pygame.draw.rect(
        screen,
        style.BUTTON,
        (50, 170, 400, 210),
        5,
    )
    # <====== Главная рамка ======>

    # <====== Горизонтальные линии ======>
    for i in range(2):
        pygame.draw.line(
            screen,
            style.BUTTON,
            (50, 240 + 70 * i),
            (450, 240 + 70 * i),
            5,
        )
    # <====== Горизонтальные линии ======>

    # <====== 1 Вертикальная линия ======>
    pygame.draw.line(
        screen,
        style.BUTTON,
        (220, 170),
        (220, 380),
        5,
    )
    # <====== 1 Вертикальная линия ======>

    columns = [
        ("Дата", data),
        ("Время", time),
        ("Счет", points),
    ]

    for index, column in enumerate(columns):
        # <====== Надпись ======>
        font = pygame.font.SysFont("bahnschrift", 50)
        text = font.render(column[0], True, style.TABLE_NAMES)

        text_x = 130 - text.get_width() // 2
        text_y = 210 + 70 * index - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Надпись ======>

        # <====== Пользователь ======>
        font = pygame.font.SysFont("bahnschrift", 35)

        text = font.render(column[1], True, style.TABLE_VALUES)

        text_x = 335 - text.get_width() // 2
        text_y = 210 + 70 * index - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Пользователь ======>

    # <====== Главное меню ======>
    pygame.draw.rect(screen, style.BUTTON, (100, 450, 300, 50))

    font = pygame.font.SysFont("bahnschrift", 35)

    text = font.render("Главное меню", True, style.PLAY)

    text_x = 250 - text.get_width() // 2
    text_y = 475 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))
    # <====== Главное меню ======>

    cursor.execute(
        """
    INSERT INTO board(data, time, points) VALUES(?, ?, ?)
    """,
        (data, time, points),
    )

    connect.commit()
    cursor.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                if 100 < x < 400 and 450 < y < 500:
                    main()
        pygame.display.flip()


def lider_board(screen, screen_size):
    """Экран лидерборд"""
    connect = sqlite3.connect("data/database.db")
    cursor = connect.cursor()

    width, height = screen_size

    fon = pygame.transform.scale(
        load.load_image("background.png"),
        screen_size,
    )
    screen.blit(fon, (0, 0))

    # <====== Главное меню ======>
    pygame.draw.rect(screen, style.BUTTON, (100, 450, 300, 50))

    font = pygame.font.SysFont("bahnschrift", 30)

    text = font.render("Главное меню", True, style.PLAY)

    text_x = 250 - text.get_width() // 2
    text_y = 475 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))
    # <====== Главное меню ======>

    font = pygame.font.SysFont("bahnschrift", 50)
    text = font.render("Таблица Рекордов", True, style.TITLE)

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 7 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))

    # <====== Главная рамка ======>
    pygame.draw.rect(screen, style.BUTTON, (50, 120, 400, 300), 5)
    # <====== Главная рамка ======>

    # <====== Горизонтальные линии ======>
    for i in range(3):
        pygame.draw.line(
            screen,
            style.BUTTON,
            (50, 195 + 75 * i),
            (450, 195 + 75 * i),
            5,
        )
    # <====== Горизонтальные линии ======>

    # <====== Вертикальные линии ======>
    for i in range(2):
        pygame.draw.line(
            screen,
            style.BUTTON,
            (183 + 133 * i, 120),
            (183 + 133 * i, 420),
            5,
        )
    # <====== Вертикальные линии ======>

    # <====== Надписи ======>
    columns = ["Дата", "Время", "Счет"]
    for index, column in enumerate(columns):
        font = pygame.font.SysFont("bahnschrift", 40)
        text = font.render(column, True, style.TABLE_NAMES)

        text_x = 115 + 135 * index - text.get_width() // 2
        text_y = 160 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
    # <====== Надписи ======>

    result = [i for i in cursor.execute("""SELECT * from board""").fetchall()]
    result.sort(key=lambda i: i[-1])
    for place in range(len(result[:3])):
        id, data, time, points = result[place]

        # <======== Дата ========>
        font = pygame.font.SysFont("bahnschrift", 25)

        text = font.render(data, True, style.TABLE_VALUES)

        text_x = 115 - text.get_width() // 2
        text_y = (235 - text.get_height() // 2) + 75 * place

        screen.blit(text, (text_x, text_y))
        # <======== Дата ========>

        # <======== Время ========>
        font = pygame.font.SysFont("bahnschrift", 30)

        text = font.render(time, True, style.TABLE_VALUES)

        text_x = 250 - text.get_width() // 2
        text_y = (235 - text.get_height() // 2) + 75 * place

        screen.blit(text, (text_x, text_y))
        # <======== Время ========>

        # <======== Счет ========>
        font = pygame.font.SysFont("bahnschrift", 30)

        text = font.render(str(points), True, style.TABLE_VALUES)

        text_x = 380 - text.get_width() // 2
        text_y = (235 - text.get_height() // 2) + 75 * place

        screen.blit(text, (text_x, text_y))
        # <======== Счет ========>

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                if 100 < x < 400 and 450 < y < 500:
                    main()
        pygame.display.flip()


def start_screen(screen, screen_size):
    """Главный экран"""
    global first_move
    first_move = True
    width, height = screen_size

    fon = pygame.transform.scale(
        load.load_image("background.png"),
        screen_size,
    )
    screen.blit(fon, (0, 0))

    font = pygame.font.SysFont("bahnschrift", 60)
    text = font.render("Сапер", True, style.TITLE)

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 3 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))

    # ============================

    button_x_1 = width // 2
    button_y_1 = height // 2

    pygame.draw.rect(
        screen,
        style.BUTTON,
        (button_x_1 - 100, button_y_1 - 25, 200, 50),
        0,
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    text = font.render("Играть!", True, style.PLAY)

    button_x_text_1 = width // 2 - text.get_width() // 2
    button_y_text_1 = height // 2 - text.get_height() // 2

    screen.blit(text, (button_x_text_1, button_y_text_1))

    # ============================

    button_x_2 = width // 2
    button_y_2 = height // 2 + 80

    pygame.draw.rect(
        screen,
        style.BUTTON,
        (button_x_2 - 100, button_y_2 - 25, 200, 50),
        0,
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    text = font.render("Рекорды", True, style.RECORD)

    button_x_text_2 = width // 2 - text.get_width() // 2
    button_y_text_2 = height // 2 + 80 - text.get_height() // 2

    screen.blit(text, (button_x_text_2, button_y_text_2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                if (
                        button_x_1 - 100 < x < button_x_1 + 100
                        and button_y_1 - 25 < y < button_y_1 + 25
                ):
                    return
                elif (
                        button_x_2 - 100 < x < button_x_2 + 100
                        and button_y_2 - 25 < y < button_y_2 + 25
                ):
                    clear_all_sprites()
                    lider_board(screen, screen_size)
        pygame.display.flip()


def terminate():
    """Выход из приложения"""
    pygame.quit()
    sys.exit()


def clear_all_sprites():
    """Очистить все спрайты, очистить бомбы"""
    all_sprites.remove(all_sprites)


# Глобальные переменные
first_move = True

# Инициализация Pygame
pygame.init()

# Создание группы спрайтов
all_sprites: pygame.sprite.Group = pygame.sprite.Group()

# Инициализация экрана и его размеров
SCREEN_SIZE = (500, 500)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Сапер")

value, count = (
    config.value,
    config.count_mines,
)
if (not (8 <= value <= 15)) or (not (value ** 2 > count)):
    print("Invalid parameters in config")
    sys.exit()


def create_empty_map(value):
    """Создать пустое поле"""
    with open("data/map.txt", "w") as map_file:
        for i in range(value):
            string = "." * value
            map_file.write(string)
            if i < value - 1:
                map_file.write("\n")


def create_database():
    with sqlite3.connect("data/database.db") as connect:
        cursor = connect.cursor()

        sql = """
        DROP TABLE IF EXISTS board;
        """

        cursor.execute(sql)

        sql = """
        CREATE TABLE board (
            id     INTEGER PRIMARY KEY ASC AUTOINCREMENT
                           UNIQUE,
            data   VARCHAR,
            time   VARCHAR,
            points INTEGER
        );
        """

        cursor.execute(sql)

        connect.commit()


def main():
    """Главная функция"""
    global screen, SCREEN_SIZE, first_move, value, count

    pygame.init()

    create_empty_map(value)

    start_screen(screen, SCREEN_SIZE)

    board = Minesweeper(screen, SCREEN_SIZE, value, count)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if board.lose_detect:
                        x, y = event.pos
                        if 50 < x < 235 and 10 < y < 80:
                            start_screen(screen, SCREEN_SIZE)
                            board = Minesweeper(
                                screen,
                                SCREEN_SIZE,
                                value,
                                count,
                            )
                            clear_all_sprites()
                            first_move = True
                    if first_move:
                        board.get_click(
                            event.pos,
                            first_move,
                            True,
                        )
                        first_move = False
                    else:
                        board.get_click(event.pos, first_move, True)
                elif event.button == 3:
                    board.get_click(
                        event.pos,
                        False,
                        False,
                    )

        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    create_database()
    main()
