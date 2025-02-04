import pygame
import os
import random
from pprint import pprint

if __name__ == '__main__':
    def load_level(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [list(line.strip()) for line in mapFile]
        return list(level_map)


    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        return image


    pygame.init()
    all_sprites = pygame.sprite.Group()
    pygame.display.set_caption('^_^')
    size = width, height = 450, 450
    screen = pygame.display.set_mode(size)
    apple = load_image('apple.png')
    grass1 = load_image('grass1.jpg')
    grass2 = load_image('grass2.png')
    body = load_image('body.png')
    body_rotate = load_image('rotate.png')
    tail = load_image('tail.png')
    wall = load_image('wall.png')


    class SnakeHead(pygame.sprite.Sprite):
        image = load_image("snake_head1.png")

        def __init__(self):
            super().__init__()
            self.frames = []
            self.cut_sheet(self.image, 12, 2)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rotate = 0
            self.rect = self.image.get_rect()

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def frame_update(self, *args, **kwargs):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.rotate(self.frames[self.cur_frame], self.rotate)

        def update(self, x, y, rotate, *args, **kwargs):
            self.rotate = rotate
            self.rect.x = x
            self.rect.y = y


    class Watermelon(pygame.sprite.Sprite):
        image = load_image("apple.png")

        def __init__(self):
            super().__init__()
            self.image = Watermelon.image
            self.rect = self.image.get_rect()

        def update(self, x, y, *args, **kwargs):
            self.rect.x = x
            self.rect.y = y


    class Bomb(pygame.sprite.Sprite):
        image = load_image("bomb.png")

        def __init__(self):
            super().__init__()
            self.image = Bomb.image
            self.rect = self.image.get_rect()
            self.rect.x = -30
            self.rect.y = -30

        def update(self, x, y, *args, **kwargs):
            self.rect.x = x
            self.rect.y = y


    class Board:
        def __init__(self, mode, bomb_mode=False):
            self.width = 15
            self.height = 15
            self.cell_size = 30
            self.snake_len = 2
            self.snake = []
            self.board = load_level(mode)
            self.head_pos = [7, 4]
            self.vector = (0, 0)
            self.corner = False
            self.rotate = False
            self.bomb = bomb_mode
            snake_head.update(120, 210, 0)
            watermelon.update(360, 210)
            if bomb_mode:
                bomb.update(390, 210)
            else:
                bomb.update(-30, -30)
            self.fill()

        def fill(self):
            for x in enumerate(self.board):
                for y in enumerate(x[1]):
                    if y[1] == '.':
                        screen.blit(grass1, ((y[0] * self.cell_size), (x[0] * self.cell_size)))
                    if y[1] == ',':
                        screen.blit(grass2, ((y[0] * self.cell_size), (x[0] * self.cell_size)))
                    if y[1] == '#':
                        screen.blit(wall, ((y[0] * self.cell_size), (x[0] * self.cell_size)))


    class Snake(Board):
        def move(self):
            global running, end_screen

            def snake_check(coords, head=False):
                if head:
                    list = self.snake[0:-2]
                else:
                    list = self.snake
                for i in list:
                    if coords == i[0:2]:
                        return False
                return True

            super().fill()
            self.head_pos[0] += self.vector[0]
            self.head_pos[1] += self.vector[1]
            if self.head_pos[0] == -1:
                self.head_pos[0] = self.height - 1
            if self.head_pos[0] == self.height:
                self.head_pos[0] = 0
            if self.head_pos[1] == -1:
                self.head_pos[1] = self.width - 1
            if self.head_pos[1] == self.width:
                self.head_pos[1] = 0

            rotate = 0
            if self.vector[0] == 1:
                rotate = 270
            elif self.vector[0] == -1:
                rotate = 90
            elif self.vector[1] == -1:
                rotate = 180

            self.snake.append([self.head_pos[0], self.head_pos[1], rotate, self.rotate, self.corner])
            self.corner = False

            if (not snake_check(self.head_pos, True) and self.snake_len > 4) or self.board[self.snake[-1][1]][
                self.snake[-1][0]] == '#':
                end_screen = True

            if len(self.snake) > self.snake_len:
                del self.snake[0]

            if self.vector == (0, 0):
                screen.blit(tail, ((self.cell_size * 3), (self.cell_size * 7)))
                return None

            for i in enumerate(self.snake):
                if i[0] == 0:
                    if self.vector != (0, 0):
                        if self.snake[i[0] + 1][4]:
                            i[1][2] = self.snake[i[0] + 1][2] - 270
                        else:
                            i[1][2] = self.snake[i[0] + 1][2]
                    image = pygame.transform.rotate(tail, i[1][2])
                    screen.blit(image, ((i[1][1] * self.cell_size), (i[1][0] * self.cell_size)))
                elif i[1][3] and i[0] != 0:
                    self.rotate = False
                    image = pygame.transform.rotate(body_rotate, i[1][2])
                    screen.blit(image, ((i[1][1] * self.cell_size), (i[1][0] * self.cell_size)))
                elif i[0] == self.snake_len - 1:
                    snake_head.update((i[1][1] * self.cell_size), (i[1][0] * self.cell_size), i[1][2])
                else:
                    image = pygame.transform.rotate(body, i[1][2])
                    screen.blit(image, ((i[1][1] * self.cell_size), (i[1][0] * self.cell_size)))

            player_rect = pygame.Rect(snake_head.rect.x, snake_head.rect.y, 30, 30)
            if player_rect.colliderect((bomb.rect.x, bomb.rect.y, 30, 30)):
                end_screen = True

            if player_rect.colliderect((watermelon.rect.x, watermelon.rect.y, 30, 30)):
                self.snake_len += 1
                if self.snake_len == 169 and self.board[0][
                    0] == '#' or self.snake_len == 225 or self.snake_len == 224 and self.bomb:
                    end_screen = True

                while True:
                    apple_pos = [random.choice(range(self.height)), random.choice(range(self.width))]
                    if snake_check(apple_pos) and self.board[apple_pos[0]][apple_pos[1]] != '#':
                        watermelon.update(apple_pos[1] * self.cell_size, apple_pos[0] * self.cell_size)
                        break

                if self.bomb:
                    while True:
                        bomb_pos = [random.choice(range(self.height)), random.choice(range(self.width))]
                        if snake_check(bomb_pos) and snake_check(
                                (bomb_pos[0] + self.vector[0], bomb_pos[1] + self.vector[1]),
                                head=True) and bomb_pos != (watermelon.rect.x // 30, watermelon.rect.y // 30):
                            bomb.update(bomb_pos[1] * self.cell_size, bomb_pos[0] * self.cell_size)
                            break

        def rotation(self, vector):
            if vector != (0, 0):
                self.snake[-1][3] = True
            if (self.vector[1] == 1 and vector[0] == -1) or (self.vector[1] == -1 and vector[0] == 1) or (
                    self.vector[0] == 1 and vector[1] == 1) or (self.vector[0] == -1 and vector[1] == -1):
                self.snake[-1][2] += 270
                self.snake[-1][4] = True
            self.vector = vector
            self.move()


    def draw_button(screen, text, x, y, width, height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height))

        font = pygame.font.Font(None, 40)
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surf, text_rect)


    def start_game(mode, bomb_mode=False):
        global running, snake, start_screen
        start_screen = False
        screen.fill((68, 148, 74))
        snake = Snake(mode, bomb_mode)


    def quit_game():
        global running
        running = False


    def menu():
        global start_screen, end_screen
        start_screen = True
        end_screen = False


    def show_start_screen(screen):
        screen.fill((68, 148, 74))

        font = pygame.font.Font(None, 74)
        title_text = font.render('Змейка', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(width // 2, height // 4))
        screen.blit(title_text, title_rect)
        draw_button(screen, "Стены", width // 2 - 70, height // 2, 140, 50, (0, 255, 0), (0, 200, 0),
                    lambda: start_game('level1.txt'))
        draw_button(screen, "С бомбой", width // 2 - 70, height // 2 - 70, 140, 50, (0, 255, 0), (0, 200, 0),
                    lambda: start_game('level0.txt', bomb_mode=True))
        draw_button(screen, "Без стен", width // 2 - 70, height // 2 + 70, 140, 50, (0, 255, 0), (0, 200, 0),
                    lambda: start_game('level0.txt'))
        draw_button(screen, "Выйти", width // 2 - 70, height // 2 + 140, 140, 50, (255, 0, 0), (200, 0, 0), quit_game)


    def show_end_screen(screen, score, win=False):
        screen.fill((68, 148, 74))

        font = pygame.font.Font(None, 50)
        if not win:
            title_text = font.render(f'Поражение', True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(width // 4, height // 4))
        else:
            title_text = font.render(f'Победа', True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(width // 4, height // 4))
        screen.blit(title_text, title_rect)
        title_text = font.render(f'Количество очков:{snake.snake_len - 2}', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(width // 2, height // 3))
        screen.blit(title_text, title_rect)
        draw_button(screen, "Меню", width // 2 - 200, height // 2 + 70, 140, 50, (0, 255, 0), (0, 200, 0), menu)
        draw_button(screen, "Выйти", width // 2 - 200, height // 2 + 140, 140, 50, (255, 0, 0), (200, 0, 0), quit_game)


    snake_head = SnakeHead()
    watermelon = Watermelon()
    bomb = Bomb()
    all_sprites.add(bomb)
    all_sprites.add(snake_head)
    all_sprites.add(watermelon)
    running = True
    move = True
    start_screen = True
    end_screen = False
    clock = pygame.time.Clock()
    fps = 8
    while running:
        if start_screen:
            show_start_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()

        elif end_screen:
            if snake.snake_len == 225 or snake.snake_len == 169 and snake.board[0][
                0] == '#' or snake.snake_len == 224 and self.bomb:
                show_end_screen(screen, snake.snake_len, True)
            else:
                show_end_screen(screen, snake.snake_len)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()

        else:
            snake.fill()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RIGHT, pygame.K_d] and snake.vector[1] != -1 and snake.vector[1] != 1:
                        snake.rotation((0, 1))
                        move = False
                    elif event.key in [pygame.K_LEFT, pygame.K_a] and snake.vector[1] != 1 and snake.vector[1] != -1:
                        snake.rotation((0, -1))
                        move = False
                    elif event.key in [pygame.K_DOWN, pygame.K_s] and snake.vector[0] != -1 and snake.vector[0] != 1:
                        snake.rotation((1, 0))
                        move = False
                    elif event.key in [pygame.K_UP, pygame.K_w] and snake.vector[0] != 1 and snake.vector[0] != -1:
                        snake.rotation((-1, 0))
                        move = False

            if move:
                snake.move()
            else:
                move = True
            snake_head.frame_update()
            all_sprites.draw(screen)
            clock.tick(fps)
            pygame.display.flip()
    pygame.quit()
