import random
import pygame
import sys
from pygame.locals import *

window_width = 800
window_height = 500
cell_size = 20
cell_width_num = int(window_width / cell_size)
cell_height_num = int(window_height / cell_size)

white = (255, 255, 255)
background = (88, 87, 86)


def start_UI():
    while True:
        UI.fill(background)
        game_title = pygame.font.Font('freesansbold.ttf', 80).render('SNAKE!', True, white)
        game_title_rect = game_title.get_rect()
        game_title_rect.center = (window_width / 2, window_height / 2 - 100)
        UI.blit(game_title, game_title_rect)
        rules = pygame.font.Font('freesansbold.ttf', 30).render('Rules', True, white)
        rules_rect = rules.get_rect()
        rules_rect.center = (window_width/2, window_height/2 - 30)
        UI.blit(rules, rules_rect)
        one = pygame.font.Font('freesansbold.ttf', 20).render("1.Don't touch the edges of the window.", True, white)
        one_rect = one.get_rect()
        one_rect.center = (window_width/2,window_height/2)
        UI.blit(one, one_rect)
        two = pygame.font.Font('freesansbold.ttf', 20).render("2.Don't touch the body of the snake.", True, white)
        two_rect = two.get_rect()
        two_rect.center = (window_width / 2, window_height / 2 + 30)
        UI.blit(two, two_rect)
        three = pygame.font.Font('freesansbold.ttf', 20).render('3.Red apple:1 point    Gold apple:5 points', True, white)
        three_rect = three.get_rect()
        three_rect.center = (window_width / 2, window_height / 2 + 60)
        UI.blit(three, three_rect)
        tip_to_start()

        if if_is_pressed():
            pygame.event.get()
            return
        pygame.display.update()


def play():
    startx = random.randint(10, cell_width_num - 10)
    starty = random.randint(10, cell_height_num - 10)
    up = "up"
    down = "down"
    left = "left"
    right = "right"
    first = 0
    snake = [{'x': startx, 'y': starty},{'x': startx - 1, 'y': starty},{'x': startx - 2, 'y': starty},{'x': startx - 3, 'y': starty}]
    direction = right
    apple = apple_position(snake)
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over()
            # 如果选择的方向与原方向正好相反，则无法修改方向
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and (direction != right):
                    direction = left
                elif (event.key == K_RIGHT) and (direction != left):
                    direction = right
                elif (event.key == K_UP) and (direction != down):
                    direction = up
                elif (event.key == K_DOWN) and (direction != up):
                    direction = down
                elif event.key == K_ESCAPE:
                    game_over()
        if direction == up:
            new = {'x': snake[first]['x'], 'y': snake[first]['y'] - 1}
        elif direction == down:
            new = {'x': snake[first]['x'], 'y': snake[first]['y'] + 1}
        elif direction == left:
            new = {'x': snake[first]['x'] - 1, 'y': snake[first]['y']}
        elif direction == right:
            new = {'x': snake[first]['x'] + 1, 'y': snake[first]['y']}
        snake.insert(0, new)
        # snake是否碰到自己或边缘
        if snake[first]['x'] == -1 or snake[first]['x'] == cell_width_num or snake[first]['y'] == -1 or snake[first]['y'] == cell_height_num:
            return  
        for i in snake[1:]:
            if i['x'] == snake[first]['x'] and i['y'] == snake[first]['y']:
                return  

        # snake是否吃到树莓
        if snake[first]['x'] == apple['x'] and snake[first]['y'] == apple['y']:
            score += result(apple['ran'])
            apple = apple_position(snake)
        else:
            del snake[-1]
        UI.fill(background)
        dark_gray = (40, 40, 40)
        for x in range(0, window_width, cell_size):
            pygame.draw.line(UI, dark_gray, (x, 0), (x, window_height))
        for y in range(0, window_height, cell_size):
            pygame.draw.line(UI, dark_gray, (0, y), (window_width, y))

        draw_snake(snake)
        draw_apple(apple)
        show_result(score)
        pygame.display.update()
        speed = 10
        game_clock.tick(speed)


def tip_to_start():
    tip = pygame.font.Font('freesansbold.ttf', 25).render('Press any key then you can get started.', True, white)
    tip_rect = tip.get_rect()
    tip_rect.top = window_height - 50
    tip_rect.left = window_width - 500
    UI.blit(tip, tip_rect)


def if_is_pressed():
    if pygame.event.get(QUIT):
        game_over()
    key_event = pygame.event.get(KEYDOWN)
    if len(key_event) == 0:
        return None
    if key_event[0].key == K_ESCAPE:
        game_over()
    return key_event[0].key


def draw_snake(snake):
    for i in snake:
        x = i['x'] * cell_size
        y = i['y'] * cell_size
        snake_rect = pygame.Rect(x, y, cell_size, cell_size)
        snake_colour = (128, 128, 105)
        pygame.draw.rect(UI, snake_colour, snake_rect)


def apple_position(snake):
    position = {'x': random.randint(5, cell_width_num - 4), 'y': random.randint(5, cell_height_num - 4), 'ran':random.randint(1, 20)}
    location = {'x':position['x'], 'y':position['y']}
    while location in snake:
        position = {'x': random.randint(5, cell_width_num - 4), 'y': random.randint(5, cell_height_num - 4),
                    'ran': random.randint(1, 20)}
        location = {'x': position['x'], 'y': position['y']}
    return position


def draw_apple(i):
    x = i['x'] * cell_size
    y = i['y'] * cell_size
    apple_rect = pygame.Rect(x, y, cell_size, cell_size)
    dark_red = (98, 3, 23)
    gold = (225, 215, 0)
    random_num = i['ran']
    if random_num % 3 == 0:
        pygame.draw.rect(UI, gold, apple_rect)
    else:
        pygame.draw.rect(UI, dark_red, apple_rect)


def result(num):
    if num % 3 == 0:
        point = 5
    else:
        point = 1
    return point


def show_result(score):
    final_score = pygame.font.Font('freesansbold.ttf', 18).render('Final Score: %s' % score, True, white)
    final_score_rect = final_score.get_rect()
    final_score_rect.topleft = (window_width - 200, 10)
    UI.blit(final_score, final_score_rect)


def end_UI():
    game_over = pygame.font.Font('freesansbold.ttf', 80).render('Game Over', True, white)
    game_over_rect = game_over.get_rect()
    game_over_rect.center = (window_width / 2, window_height / 2)

    UI.blit(game_over, game_over_rect)
    tip_to_start()
    pygame.display.update()
    if_is_pressed()

    while True:
        if if_is_pressed():
            pygame.event.get()
            return


def game_over():
    pygame.quit()
    sys.exit()


global game_clock, UI
pygame.init()
game_clock = pygame.time.Clock()
UI = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('SNAKE!')
start_UI()
while True:
    play()
    end_UI()
