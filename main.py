from random import choices, choice
import sys
import pygame
import os
import datetime
import sqlite3
from config import *
from style import *


# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Bomb(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bomb.jpg", (255, 255, 255)),
                                   (40, 40))

    def __init__(self, x, y, GOG=True):
        super().__init__(all_sprites)
        if GOG:
            self.image = Bomb.image
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def delete(self):
        all_sprites.remove(all_sprites)


class Board:
    def __init__(self, screen_size, width, height, count):

        self.width = width  # Ширина поля
        self.height = height  # Высота поля
        self.count = count  # Количество мин

        w, h = screen_size

        self.left = 50
        self.top = 90
        self.cell_size = (w - 100) // width

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if not self.lose_detect:
                    GOG = False
                    if self.map[i][j] != '.' and self.map[i][j] != '*':
                        GOG = True
                    if self.map[i][j] == '*':
                        col = 'black'
                    elif self.map[i][j] == '.':
                        col = 'black'
                    else:
                        col = 'grey'

                    pygame.draw.rect(screen, pygame.Color("white"), (
                        self.left + j * self.cell_size,
                        self.top + i * self.cell_size, self.cell_size,
                        self.cell_size), 1)

                    pygame.draw.rect(screen, pygame.Color(col), (
                        self.left + j * self.cell_size + 1,
                        self.top + i * self.cell_size + 1,
                        self.cell_size - 2,
                        self.cell_size - 2),
                                     0)

                    if GOG:
                        cnt = str(self.map[i][j])
                        if cnt == 'F':
                            color = (102, 51, 0)
                        elif cnt == '1':
                            color = (0, 0, 179)
                        elif cnt == '2':
                            color = (0, 179, 60)
                        elif cnt == '3':
                            color = (179, 36, 0)
                        elif cnt == '4':
                            color = (0, 0, 102)
                        else:
                            color = (0, 0, 0)

                        font = pygame.font.Font(None, 53)
                        text = font.render(str(self.map[i][j]), True,
                                           color)
                        text_x = self.left + j * self.cell_size + 10
                        text_y = self.top + i * self.cell_size + 5
                        screen.blit(text, (text_x, text_y))
                else:
                    square = i * self.width + j
                    if (self.map[i][j] == 'F' and square in self.MINES) or \
                            self.map[i][j] == '*':
                        x, y = (
                            self.left + j * self.cell_size,
                            self.top + i * self.cell_size)
                        self.map[i][j] = '*'

                        bomb = Bomb(x, y)
                        all_sprites.add(bomb)

                        col = 'red'
                    elif self.map[i][j] == '.':
                        col = 'black'
                    else:
                        col = 'grey'

                    pygame.draw.rect(screen, pygame.Color("white"), (
                        self.left + j * self.cell_size,
                        self.top + i * self.cell_size, self.cell_size,
                        self.cell_size), 1)

                    pygame.draw.rect(screen, pygame.Color(col), (
                        self.left + j * self.cell_size + 1,
                        self.top + i * self.cell_size + 1,
                        self.cell_size - 2,
                        self.cell_size - 2),
                                     0)
                    if self.map[i][j] == '.':

                        font = pygame.font.Font(None, 53)
                        text = font.render(str(' '), True,
                                           (255, 0, 0))
                        text_x = self.left + j * self.cell_size + 10
                        text_y = self.top + i * self.cell_size + 5
                        screen.blit(text, (text_x, text_y))
                    else:
                        cnt = str(self.map[i][j])
                        if cnt == 'F':
                            color = (102, 51, 0)
                        elif cnt == '1':
                            color = (0, 0, 179)
                        elif cnt == '2':
                            color = (0, 179, 60)
                        elif cnt == '3':
                            color = (179, 36, 0)
                        elif cnt == '4':
                            color = (0, 0, 102)
                        else:
                            color = (0, 0, 0)
                        font = pygame.font.Font(None, 53)
                        text = font.render(str(self.map[i][j]), True,
                                           color)
                        text_x = self.left + j * self.cell_size + 10
                        text_y = self.top + i * self.cell_size + 5
                        screen.blit(text, (text_x, text_y))

                    # <======== Вы проиграли! ========>
                    pygame.draw.rect(screen, BUTTON, (265, 10, 185, 70))

                    font = pygame.font.SysFont("bahnschrift", 25)

                    text = font.render("Вы проиграли!", True, TITLE)

                    text_x = 357 - text.get_width() // 2
                    text_y = 50 - text.get_height() // 2

                    screen.blit(text, (text_x, text_y))
                    # <======== Вы проиграли! ========>

                    # <======== Рестарт ========>
                    pygame.draw.rect(screen, BUTTON, (50, 10, 185, 70))

                    font = pygame.font.SysFont("bahnschrift", 35)

                    text = font.render("Рестарт", True, TITLE)

                    text_x = 142 - text.get_width() // 2
                    text_y = 45 - text.get_height() // 2

                    screen.blit(text, (text_x, text_y))
                    # <======== Рестарт ========>


def generate_neighbors(square):
    """ Возвращает клетки соседствующие с square """
    if square == 0:
        data = (1, 11, 10)

    elif square == 9:
        data = (8, 18, 19)

    elif square == 90:
        data = (80, 81, 91)

    elif square == 99:
        data = (89, 88, 98)

    elif square in (1, 2, 3, 4, 5, 6, 7, 8):
        data = (
            square - 1, square - 1 + 10, square + 10, square + 1 + 10,
            square + 1)

    elif square in (91, 92, 93, 94, 95, 96, 97, 98):
        data = (
            square - 1, square - 1 - 10, square - 10, square + 1 - 10,
            square + 1)

    elif square in (10, 20, 30, 40, 50, 60, 70, 80):
        data = (
            square - 10, square + 1 - 10, square + 1, square + 1 + 10,
            square + 10)

    elif square in (19, 29, 39, 49, 59, 69, 79, 89):
        data = (
            square - 10, square - 10 - 1, square - 1, square - 1 + 10,
            square + 10)

    else:
        data = (
            square - 1 - 10, square - 10, square + 1 - 10, square + 1,
            square + 1 + 10, square + 10, square - 1 + 10, square - 1)

    return data


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def load_level():
    filename = "data/map.txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # print(level_map)
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


class Minesweeper(Board):

    def __init__(self, screen, screen_size, width, height, count):
        super().__init__(screen_size, width, height, count)

        # <============ СЧЕТ ============>
        self.now = datetime.datetime.now()
        self.start_time = datetime.datetime.timestamp(self.now)
        self.finish_time = None
        self.points = None
        self.data = ':'.join(
            reversed(str(self.now).split()[0].replace('-', ':').split(':')))
        self.time = str(self.now).split()[1].split('.')[0]
        # <============ СЧЕТ ============>

        self.map = load_level()  # Загружаем карту
        self.screen = screen

        self.restart = False

        self.lose_detect = False

        self.win_detect = False

        self.count = count

        self.lst = []

        l_board = [i for i in range(height * width)]

        self.MINES = choices(l_board, k=count)  # Мины

        # print(self.MINES)
        for mine in self.MINES:
            i, j = mine // height, mine % width
            self.lst.append(mine)
            # print(f"i-> {i} | j-> {j}")
            self.map[i][j] = '*'

    def cell_to_square(self, cell):
        i, j = cell
        square = j * self.width + i
        return square

    def get_click(self, mouse_pos, first_move, gog):
        cell = self.get_cell(mouse_pos)
        if gog:
            self.open_cell(cell, first_move)
        else:
            self.open_flag(cell)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < self.left or mouse_pos[
            0] > self.left + self.cell_size * len(
            self.map[0]) or mouse_pos[1] \
                < self.top or mouse_pos[1] > self.top + self.cell_size * len(
            self.map):
            return None
        return (
            (mouse_pos[0] - self.left) // self.cell_size,
            (mouse_pos[1] - self.top) // self.cell_size)

    def open_flag(self, cell):
        if not self.lose_detect and not self.win_detect:

            j, i = cell
            square = self.cell_to_square(cell)

            if self.map[i][j] == '.' or self.map[i][j] == '*':
                self.map[i][j] = 'F'
            elif self.map[i][j] == 'F':
                if square in self.MINES:
                    self.map[i][j] = '*'
                else:
                    self.map[i][j] = '.'
            GOG = self.check_win()
            if GOG:
                self.win_detect = True
                self.win()

    def check_win(self):
        cnt = sum([i.count('.') for i in self.map])
        GOG = cnt == 0
        return GOG

    def open_cell(self, cell, first_move=False):
        if not self.lose_detect and not self.win_detect:
            try:
                j, i = cell
                square = self.cell_to_square(cell)
                if first_move:
                    if square in self.MINES:
                        self.MINES.remove(square)
                        self.lst.remove(square)

                        i, j = square // self.height, square % self.width

                        cnt = self.get_cnt_mines(square)

                        if cnt:
                            self.map[i][j] = cnt
                        else:
                            self.map[i][j] = ' '

                        l_board = [i for i in range(self.height * self.width)]
                        while True:
                            mine = choice(l_board)
                            # print(f"mine -> {mine}")
                            if mine not in self.MINES and mine != square:
                                i, j = mine // self.height, mine % self.width
                                self.map[i][j] = '*'
                                self.MINES.append(mine)
                                self.lst.append(mine)
                                break
                # print(self.lst)
                if square in self.MINES:
                    self.lose()
                if square not in self.lst:
                    self.lst.append(square)
                    cnt = self.get_cnt_mines(square)
                    # print(cell, square, cnt)
                    if cnt:
                        if self.map[i][j] == '.' or self.map[i][j] == 'f':
                            self.map[i][j] = cnt
                        else:
                            # print('ПРОМАХ', i, j)
                            pass
                        GOG = self.check_win()
                        if GOG:
                            self.win_detect = True
                            self.win()
                    else:
                        self.map[i][j] = ' '
                        data = generate_neighbors(square)
                        sys.setrecursionlimit(3000)
                        for square in data:
                            cell = (square % self.height, square // self.width)
                            self.open_cell(cell)
                            # print(f"рекурсия ___ {cell}, {i} {j}")
                            # time.sleep(0.02)
                        GOG = self.check_win()
                        if GOG:
                            self.win_detect = True
                            self.win()
            except Exception as e:
                pass

    def lose(self):
        # print('Ты проиграл, ты попал на мину!')
        self.lose_detect = True

    def win(self):
        # print('Ты выйграл!')
        self.now = datetime.datetime.now()
        self.finish_time = datetime.datetime.timestamp(self.now)
        self.points = str(int(self.finish_time - self.start_time))

        # print(f"data-> {self.data} | time-> {self.time} | points-> {self.points}")

        self.win_detect = True
        win_screen(self.data, self.time, self.points)

    def get_cnt_mines(self, square):
        data = generate_neighbors(square)
        # print(f"info-> {data, self.MINES}")
        cnt = 0
        for i in data:
            if i in self.MINES:
                cnt += 1
        return cnt


def win_screen(data, time, points):
    try:
        global first_move
        first_move = True
        connect = sqlite3.connect('data/database.db')
        cursor = connect.cursor()

        data = str(data)
        time = str(time)
        points = str(points)

        global screen, screen_size
        width, height = screen_size

        fon = pygame.transform.scale(load_image('background.png'), screen_size)
        screen.blit(fon, (0, 0))

        font = pygame.font.SysFont("bahnschrift", 50)
        text = font.render("Ты выйграл!", True, TITLE)

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 8 + 20 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))

        # ============================

        # <====== Главная рамка ======>
        pygame.draw.rect(screen, BUTTON, (50, 170, 400, 210), 5)
        # <====== Главная рамка ======>

        # <====== 1 Горизонтал. линия ======>
        pygame.draw.line(screen, BUTTON, (50, 240), (450, 240), 5)
        # <====== 1 Горизонтал. линия ======>

        # <====== 2 Горизонтал. линия ======>
        pygame.draw.line(screen, BUTTON, (50, 310), (450, 310), 5)
        # <====== 2 Горизонтал. линия ======>

        # <====== 1 Вертикал. линия ======>
        pygame.draw.line(screen, BUTTON, (220, 170), (220, 380), 5)
        # <====== 1 Вертикал. линия ======>

        # <====== Дата ======>
        font = pygame.font.SysFont("bahnschrift", 50)
        text = font.render("Дата", True, TABLE_NAMES)

        text_x = 130 - text.get_width() // 2
        text_y = 210 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Дата ======>

        # <====== Время ======>
        font = pygame.font.SysFont("bahnschrift", 45)
        text = font.render("Время", True, TABLE_NAMES)

        text_x = 130 - text.get_width() // 2
        text_y = 280 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Время ======>

        # <====== Счет ======>
        font = pygame.font.SysFont("bahnschrift", 50)
        text = font.render("Счет", True, TABLE_NAMES)

        text_x = 130 - text.get_width() // 2
        text_y = 340 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Счет ======>

        # <====== Главное меню ======>
        pygame.draw.rect(screen, BUTTON, (100, 450, 300, 50))

        font = pygame.font.SysFont("bahnschrift", 35)

        text = font.render("Главное меню", True, PLAY)

        text_x = 250 - text.get_width() // 2
        text_y = 475 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Главное меню ======>

        # <====== Свое Дата ======>
        font = pygame.font.SysFont("bahnschrift", 35)

        text = font.render(data, True, TABLE_VALUES)

        text_x = 335 - text.get_width() // 2
        text_y = 210 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Свое Дата ======>

        # <====== Свое Время ======>
        font = pygame.font.SysFont("bahnschrift", 35)

        text = font.render(time, True, TABLE_VALUES)

        text_x = 335 - text.get_width() // 2
        text_y = 280 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Свое Время ======>

        # <====== Свое Cчет ======>
        font = pygame.font.SysFont("bahnschrift", 35)

        text = font.render(points, True, TABLE_VALUES)

        text_x = 340 - text.get_width() // 2
        text_y = 340 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Свое Cчет ======>

        cursor.execute("""
        INSERT INTO board(data, time, points) VALUES(?, ?, ?)
        """, (data, time, points))

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
    except Exception as e:
        pass


def lider_board(screen, screen_size):
    try:

        connect = sqlite3.connect('data/database.db')
        cursor = connect.cursor()

        width, height = screen_size

        fon = pygame.transform.scale(load_image('background.png'), screen_size)
        screen.blit(fon, (0, 0))

        # <====== Главное меню ======>
        pygame.draw.rect(screen, BUTTON, (100, 450, 300, 50))

        font = pygame.font.SysFont("bahnschrift", 30)

        text = font.render("Главное меню", True, PLAY)

        text_x = 250 - text.get_width() // 2
        text_y = 475 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== Главное меню ======>

        font = pygame.font.SysFont("bahnschrift", 50)
        # print(pygame.font.get_fonts())
        # print(pygame.font.match_font('arial'))
        text = font.render("Таблица Рекордов", True, TITLE)

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 7 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))

        # ============================

        # <====== Главная рамка ======>
        pygame.draw.rect(screen, BUTTON, (50, 120, 400, 300), 5)
        # <====== Главная рамка ======>

        # <====== 1 Горизонтал. линия ======>
        pygame.draw.line(screen, BUTTON, (50, 195), (450, 195), 5)
        # <====== 1 Горизонтал. линия ======>

        # <====== 2 Горизонтал. линия ======>
        pygame.draw.line(screen, BUTTON, (50, 270), (450, 270), 5)
        # <====== 2 Горизонтал. линия ======>

        # <====== 3 Горизонтал. линия ======>
        pygame.draw.line(screen, BUTTON, (50, 345), (450, 345), 5)
        # <====== 3 Горизонтал. линия ======>

        # <====== 1 Вертикал. линия ======>
        pygame.draw.line(screen, BUTTON, (183, 120), (183, 420), 5)
        # <====== 1 Вертикал. линия ======>

        # <====== 2 Вертикал. линия ======>
        pygame.draw.line(screen, BUTTON, (316, 120), (316, 420), 5)
        # <====== 2 Вертикал. линия ======>

        # <====== 1 Горизонтал. линия Дата ======>
        font = pygame.font.SysFont("bahnschrift", 40)
        text = font.render("Дата", True, TABLE_NAMES)

        text_x = 115 - text.get_width() // 2
        text_y = 160 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== 1 Горизонтал. линия Дата ======>

        # <====== 1 Горизонтал. линия Время ======>
        font = pygame.font.SysFont("bahnschrift", 40)

        text = font.render("Время", True, TABLE_NAMES)

        text_x = 250 - text.get_width() // 2
        text_y = 160 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== 1 Горизонтал. линия Время ======>

        # <====== 1 Горизонтал. линия Счет ======>
        font = pygame.font.SysFont("bahnschrift", 40)

        text = font.render("Счет", True, TABLE_NAMES)

        text_x = 385 - text.get_width() // 2
        text_y = 160 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <====== 1 Горизонтал. линия Счет ======>

        result = [i for i in
                  cursor.execute("""SELECT * from board""").fetchall()]
        result.sort(key=lambda i: i[-1])
        lenght = len(result)
        place = 0
        while lenght:
            if place == 3:
                break

            id, data, time, points = result[place]

            # <======== Дата ========>
            font = pygame.font.SysFont("bahnschrift", 25)

            text = font.render(data, True, TABLE_VALUES)

            text_x = 115 - text.get_width() // 2
            text_y = (235 - text.get_height() // 2) + 75 * place

            screen.blit(text, (text_x, text_y))
            # <======== Дата ========>

            # <======== Время ========>
            font = pygame.font.SysFont("bahnschrift", 30)

            text = font.render(time, True, TABLE_VALUES)

            text_x = 250 - text.get_width() // 2
            text_y = (235 - text.get_height() // 2) + 75 * place

            screen.blit(text, (text_x, text_y))
            # <======== Время ========>

            # <======== Счет ========>
            font = pygame.font.SysFont("bahnschrift", 30)

            text = font.render(str(points), True, TABLE_VALUES)

            text_x = 380 - text.get_width() // 2
            text_y = (235 - text.get_height() // 2) + 75 * place

            screen.blit(text, (text_x, text_y))
            # <======== Счет ========>

            lenght -= 1
            place += 1

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
    except Exception as e:
        pass


def start_screen(screen, screen_size):
    try:
        global first_move
        first_move = True
        width, height = screen_size

        fon = pygame.transform.scale(load_image('background.png'), screen_size)
        screen.blit(fon, (0, 0))

        font = pygame.font.SysFont("bahnschrift", 60)
        text = font.render("Сапер", True, TITLE)

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 3 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))

        # ============================

        button_x_1 = width // 2
        button_y_1 = height // 2

        pygame.draw.rect(screen, BUTTON,
                         (button_x_1 - 100, button_y_1 - 25,
                          200, 50), 0)

        font = pygame.font.SysFont("bahnschrift", 40)
        text = font.render("Играть!", True, PLAY)

        button_x_text_1 = width // 2 - text.get_width() // 2
        button_y_text_1 = height // 2 - text.get_height() // 2

        screen.blit(text, (button_x_text_1, button_y_text_1))

        # ============================

        button_x_2 = width // 2
        button_y_2 = height // 2 + 80

        pygame.draw.rect(screen, BUTTON,
                         (button_x_2 - 100, button_y_2 - 25,
                          200, 50), 0)

        font = pygame.font.SysFont("bahnschrift", 40)
        text = font.render("Рекорды", True, RECORD)

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
                    if button_x_1 - 100 < x < button_x_1 + 100 and button_y_1 - 25 < y < button_y_1 + 25:
                        return
                    elif button_x_2 - 100 < x < button_x_2 + 100 and button_y_2 - 25 < y < button_y_2 + 25:
                        bomb = Bomb(None, None, False)
                        bomb.delete()
                        lider_board(screen, screen_size)
            pygame.display.flip()
    except Exception as e:
        pass


def terminate():
    pygame.quit()
    sys.exit


all_sprites = pygame.sprite.Group()

screen, screen_size = None, None
first_move = True


def main():
    global screen, screen_size, first_move

    pygame.init()

    width, height, count = width_map, height_map, count_mines
    screen_size = (500, 500)

    map = open('data/map.txt', 'w')
    map.truncate()
    for i in range(1, height + 1):
        string = '.' * width
        map.write(string)
        if i != height:
            map.write('\n')
    map.close()

    screen = pygame.display.set_mode(screen_size)
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Сапер')

    start_screen(screen, screen_size)

    board = Minesweeper(screen, screen_size, width, height, count)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if board.lose_detect:
                        # 50, 10, 185, 70
                        x, y = event.pos
                        if 50 < x < 235 and 10 < y < 80:
                            start_screen(screen, screen_size)
                            board = Minesweeper(screen, screen_size, width,
                                                height, count)
                            bomb = Bomb(None, None, False)
                            bomb.delete()
                            first_move = True
                    if first_move:
                        board.get_click(event.pos, first_move,
                                        True)  # True - открыть клетку
                        first_move = False
                    else:
                        board.get_click(event.pos, first_move, True)
                elif event.button == 3:
                    board.get_click(event.pos, False,
                                    False)  # False - поставить флаг

        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
