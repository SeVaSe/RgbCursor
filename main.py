import pygame  # Импорт библиотеки Pygame
import sys  # Импорт библиотеки sys
import random  # Импорт библиотеки random
import colorsys  # Импорт библиотеки colorsys

# Инициализация Pygame
pygame.init()

# Размер окна
WINDOW_WIDTH = 800  # Ширина окна
WINDOW_HEIGHT = 600  # Высота окна

# Цвета
BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона (черный)
LINE_FADE_SPEED = 1  # Скорость затухания линий
LINE_MOVE_SPEED = 2  # Скорость движения линий к курсору
LINE_COLOR_CHANGE_SPEED = 0.5  # Скорость изменения цвета линий

# Создание окна
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Создание окна Pygame заданного размера
pygame.display.set_caption("Линии, следящие за курсором")  # Установка заголовка окна

# Создание класса для линий
class Line:
    """КЛАСС СОЗДАНИЯ ЛИНИИ"""
    def __init__(self, start, color):  # Конструктор класса Line
        self.start = start  # Установка начальной позиции линии
        self.end = start  # Установка конечной позиции линии (по умолчанию равна начальной)
        self.color = color  # Установка цвета линии
        self.alpha = 255  # Начальная прозрачность
        self.width = 2  # Начальная ширина линии
        self.pulsating = False  # Флаг, указывающий, имеет ли линия пульсацию

    def move_towards(self, target):
        """дживежение линии за курсором"""
        dx = target[0] - self.end[0]  # Вычисление изменения по горизонтали до цели
        dy = target[1] - self.end[1]  # Вычисление изменения по вертикали до цели
        length = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Расчет длины вектора
        dx /= length  # Нормализация изменения по горизонтали
        dy /= length  # Нормализация изменения по вертикали
        self.end = (self.end[0] + dx * LINE_MOVE_SPEED, self.end[1] + dy * LINE_MOVE_SPEED)  # Движение линии к цели
        self.alpha -= LINE_FADE_SPEED  # Уменьшение прозрачности
        if self.pulsating:  # Если линия имеет пульсацию
            self.width = random.randint(1, 10)  # Изменение ширины линии случайным образом

    def is_faded(self):
        return self.alpha <= 0  # Проверка, затухла ли линия

# Создание списка линий
lines = []

# Главный цикл программы
running = True  # Флаг для выполнения цикла
pulsate_counter = 0  # Счетчик для пульсации линий
pulsate_duration = 30  # Интервал пульсации линий
hue = 0.0  # Начальное значение цвета (Hue)
hue_speed = 0.001  # Скорость изменения цвета

while running:  # Основной игровой цикл
    for event in pygame.event.get():  # Обработка событий Pygame, включая закрытие окна
        if event.type == pygame.QUIT:
            running = False

    # Заливка фона
    window.fill(BACKGROUND_COLOR)  # Заполнение окна черным цветом

    # Получение текущей позиции курсора
    cursor_x, cursor_y = pygame.mouse.get_pos()

    # Удаление линий, которые достигли конца затухания
    lines = [line for line in lines if not line.is_faded()]

    # Создание новой линии
    hue += hue_speed  # Изменение цвета линии
    line_color = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(hue % 1, 1, 1))  # Преобразование цвета в RGB
    new_line = Line((cursor_x, cursor_y), line_color)  # Создание новой линии

    # Добавление пульсации к каждой десятой линии
    pulsate_counter += 1
    if pulsate_counter == pulsate_duration:
        new_line.pulsating = True  # Включение пульсации для новой линии
        pulsate_counter = 0

    lines.append(new_line)  # Добавление новой линии в список

    # Обновление и движение линий
    for line in lines:
        line.move_towards((cursor_x, cursor_y))  # Движение линии к текущей позиции курсора

    # Отрисовка и обновление линий
    for line in lines:
        pygame.draw.line(window, line.color, line.start, line.end, line.width)  # Отрисовка линии

    # Обновление экрана
    pygame.display.update()  # Обновление отображаемого содержимого

# Завершение Pygame
pygame.quit()
sys.exit()
