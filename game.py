import pygame
import random
import sqlite3
import time


pygame.init()
pygame.event.set_blocked(None)
pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN))
pygame.event.clear()
size = w, h = 900, 600
screen = pygame.display.set_mode(size)
hero_mega_val = 4
pygame.display.set_caption("DOTA")

cursor = pygame.image.load('data/cursor.png').convert_alpha()
pygame.mouse.set_cursor((4, 4), cursor)

pygame.mixer.music.load('data/music/music.mp3')
pygame.mixer.music.play(-1)

button_sound1 = pygame.mixer.Sound('data/music/click1.wav')
button_sound2 = pygame.mixer.Sound('data/music/click.wav')

with sqlite3.connect('database.db') as con:
    wins, losses, kills, deaths = con.execute(
        'SELECT * FROM statistic').fetchall()[0]


def init(wins, losses, kills, deaths):
    '''Начальный экран при запуске'''
    bg = pygame.image.load('data/bg.jpeg').convert()
    rect = screen.get_rect().fit(bg.get_rect())
    image = pygame.transform.smoothscale(bg.subsurface(rect), size, screen)
    font = pygame.font.Font(None, 50)
    text = font.render('WELCOME TO DOTA!', 1, '#FFD700')
    screen.blit(text, text.get_rect(center=(450, 40)))

    font = pygame.font.Font(None, 40)
    screen.blit(font.render('Statistics:', 1, '#FFD700'),
                (30, 100))
    screen.blit(font.render('Wins - ', 1, '#FFD700'),
                (70, 150))
    screen.blit(font.render(str(wins), 1, 'white'),
                (270, 150))
    screen.blit(font.render('Losses - ', 1, '#FFD700'),
                (70, 190))
    screen.blit(font.render(str(losses), 1, 'white'),
                (270, 190))

    screen.blit(font.render('Kills - ', 1, '#FFD700'),
                (70, 270))
    screen.blit(font.render(str(kills), 1, 'white'),
                (270, 270))
    screen.blit(font.render('Deaths - ', 1, '#FFD700'),
                (70, 310))
    screen.blit(font.render(str(deaths), 1, 'white'),
                (270, 310))

    button = pygame.Rect(0, 0, 300, 70)
    button.center = (450, 540)
    pygame.draw.rect(screen, '#FF00FF', button, 5)

    font = pygame.font.Font(None, 60)
    text = font.render('Play', 1, '#FF00FF')
    screen.blit(text, text.get_rect(center=button.center))

    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                button_sound1.play()
                break


def game_setting():
    '''Экран настройки параметров будущей игры'''
    global hero_mega_val, enemy_attack_m, enemy_attack_r, enemy_attack_w, enemy_attack_1
    screen.fill('gray12')
    pygame.draw.line(screen, 'white', (450, 0), (450, 460))
    pygame.draw.line(screen, 'white', (0, 75), (900, 75))
    pygame.draw.line(screen, 'white', (0, 460), (900, 460))

    font = pygame.font.Font(None, 40)
    text = font.render('Скины', 1, 'white')
    screen.blit(text, text.get_rect(center=(225, 40)))
    text = font.render('Уровень', 1, 'white')
    screen.blit(text, text.get_rect(center=(675, 40)))

    skins_rect = pygame.Rect(0, 0, 205, 246)
    skins_rect.center = (337, 250)
    pygame.draw.rect(screen, 'yellow', skins_rect, 4)

    choose_skin_rect = pygame.Rect(0, 0, 205, 246)
    choose_skin_rect.center = (112, 250)
    curtain_rect = pygame.Rect(0, 0, 201, 242)
    curtain_rect.center = choose_skin_rect.center
    pygame.draw.rect(screen, 'yellow', choose_skin_rect, 4)

    names = ['Монах', 'Огненный рыцарь', 'Жрица воды', 'Ветер Хашашин']
    coords = []
    font = pygame.font.Font(None, 30)
    for i in range(0, 4):
        y = skins_rect.y + i * 61.5
        coords.append(y)
        row = pygame.Rect(235, y, 205, 61.5)
        pygame.draw.rect(screen, 'yellow', row, 4)
        text = font.render(names[i], 1, (115, 207, 167))
        screen.blit(text, text.get_rect(center=row.center))

    monk_rect = pygame.Rect(235, coords[0], 205, 61.5)
    knight_rect = pygame.Rect(235, coords[1], 205, 61.5)
    pr_rect = pygame.Rect(235, coords[2], 205, 61.5)
    wind_rect = pygame.Rect(235, coords[3], 205, 61.5)

    map_1 = pygame.Rect(470, 127, 410, 61.5)
    map_2 = pygame.Rect(470, 188.5, 410, 61.5)
    text1 = font.render('Уровень "easy"', 1, (115, 207, 167))
    text2 = font.render('Уровень "medium"', 1, (115, 207, 167))

    screen.blit(text1, text1.get_rect(center=map_1.center))
    screen.blit(text2, text2.get_rect(center=map_2.center))
    pygame.draw.rect(screen, 'yellow', map_1, 4)
    pygame.draw.rect(screen, 'yellow', map_2, 4)

    start_button = pygame.Rect(225, 480, 450, 100)
    font = pygame.font.Font(None, 60)
    text = font.render('В бой!', 1, '#FF00FF')
    pygame.draw.rect(screen, '#FF00FF', start_button, 4)
    screen.blit(text, text.get_rect(center=start_button.center))

    image = pygame.image.load('data/pokoi.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w * 3,
                                           image.get_rect().h * 3))
    choose_ass = pygame.sprite.Group(
        AnimatedSprite_2(image, 8, 1, -230, 20))

    image = pygame.image.load('data/stay.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w * 3,
                                           image.get_rect().h * 3))
    choose_water = pygame.sprite.Group(
        AnimatedSprite_2(image, 8, 1, -230, 20))

    image = pygame.image.load('data/fire_stay.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w * 3,
                                           image.get_rect().h * 3))
    choose_knight = pygame.sprite.Group(
        AnimatedSprite_2(image, 8, 1, -185, 20))

    image = pygame.image.load('data/mon_stay.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w * 3,
                                           image.get_rect().h * 3))
    choose_monk = pygame.sprite.Group(
        AnimatedSprite_2(image, 6, 1, -320, -20))

    choose = choose_ass
    running = True
    clock = pygame.time.Clock()
    enemy_attack_m = 100
    enemy_attack_r = 150
    enemy_attack_w = 100
    enemy_attack_1 = 75
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if monk_rect.collidepoint(event.pos):
                    button_sound2.play()
                    choose = choose_monk
                    hero_mega_val = 1
                elif knight_rect.collidepoint(event.pos):
                    button_sound2.play()
                    choose = choose_knight
                    hero_mega_val = 2
                elif pr_rect.collidepoint(event.pos):
                    button_sound2.play()
                    choose = choose_water
                    hero_mega_val = 3
                elif wind_rect.collidepoint(event.pos):
                    button_sound2.play()
                    choose = choose_ass
                    hero_mega_val = 4
                elif map_1.collidepoint(event.pos):
                    button_sound2.play()
                    enemy_attack_m = 100
                    enemy_attack_r = 150
                    enemy_attack_w = 100
                    enemy_attack_1 = 75
                elif map_2.collidepoint(event.pos):
                    button_sound2.play()
                    enemy_attack_m = 150
                    enemy_attack_r = 200
                    enemy_attack_w = 125
                    enemy_attack_1 = 100
                elif start_button.collidepoint(event.pos):
                    running = False

        pygame.draw.rect(screen, 'gray12', curtain_rect)
        choose.draw(screen)
        choose.update()
        pygame.display.update()
        clock.tick(10)


class AnimatedSprite_2(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


init(wins, losses, kills, deaths)

game_setting()


def win():
    bg = pygame.image.load('data/you_win.png').convert()
    rect = screen.get_rect().fit(bg.get_rect())
    image = pygame.transform.smoothscale(bg.subsurface(rect), size, screen)

    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit()


def lose():
    bg = pygame.image.load('data/game_over.png').convert()
    rect = screen.get_rect().fit(bg.get_rect())
    image = pygame.transform.smoothscale(bg.subsurface(rect), size, screen)

    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit()


class Map(pygame.sprite.Sprite):
    mapa = pygame.image.load("data/bgr_fin.png").convert()

    def __init__(self, group):
        super().__init__(group)
        self.image = self.mapa
        self.rect = self.image.get_rect()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, delta_x, delta_y):
        self.dx = 0
        self.dy = 0
        self.dx -= delta_x
        self.dy -= delta_y


class Win(pygame.sprite.Sprite):
    image = pygame.image.load('data/you_win.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w / 5,
                                           image.get_rect().h / 5))

    def __init__(self, group, pos):
        super().__init__(group)
        self.rect = self.image.get_rect(center=(pos))
        shoot_zone = pygame.Rect(0, 0, 20, 20)
        shoot_zone.center = self.rect.center


class Lose(pygame.sprite.Sprite):
    image = pygame.image.load('data/game_over.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w / 5,
                                           image.get_rect().h / 5))

    def __init__(self, group, pos):
        super().__init__(group)
        self.rect = self.image.get_rect(center=(pos))
        shoot_zone = pygame.Rect(0, 0, 20, 20)
        shoot_zone.center = self.rect.center


class Tower(pygame.sprite.Sprite):
    image = pygame.image.load('data/tower2.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w / 5,
                                           image.get_rect().h / 5))

    def __init__(self, group, pos):
        super().__init__(group)
        self.rect = self.image.get_rect(center=(pos))
        shoot_zone = pygame.Rect(0, 0, 20, 20)
        shoot_zone.center = self.rect.center

    def center(self):
        return self.rect.center


class Shell(pygame.sprite.Sprite):
    image = pygame.image.load('data/shell3.png').convert_alpha()
    image = pygame.transform.scale(image, (image.get_rect().w / 5,
                                           image.get_rect().h / 5))

    def __init__(self, group, start_pos):
        super().__init__(group)
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = start_pos

    def update(self, enemy_pos):
        x, y = self.rect.x, self.rect.y
        x_en, y_en = enemy_pos
        global hp_hero_now, count_hero_check, hp_hero_die, count_hero
        if tower_enemy.rect.center[0] - ass.rect.center[0] <= 100 and tower_enemy.rect.center[1] - ass.rect.center[1] and gg_hero == 0:
            if x_en - 20 > x:
                self.rect.x += 1
            elif x_en - 20 < x:
                self.rect.x -= 1
            if y_en < y:
                self.rect.y -= 1
            elif y_en > y:
                self.rect.y += 1
            elif x_en - 20 == x and y_en == y:
                hp_hero_now -= 500
                count_hero_check += 500 / (hp_hero_die // 10)
                count_hero = int(count_hero_check)
                if count_hero > 10:
                    count_hero = 10
                self.rect.x += 100000


class Crips(pygame.sprite.Sprite):
    sheet1 = pygame.image.load("data/Run.png")
    sheet2 = pygame.image.load("data/Attack.png")

    def __init__(self, group, x1, y1):
        super().__init__(group)
        self.sheet = self.sheet1
        self.frames = []
        self.cut_sheet(self.sheet, 8, 1, x1, y1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(224, 112)

    def cut_sheet(self, sheet, columns, rows, x1, y1):
        self.rect = pygame.Rect(x1, y1, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, val):
        global all_team_crips_x, dmg, enemy_run, gg, tower_as_hp
        if self.rect.center[0] < enemy.rect.center[0] and enemy.rect.collidepoint(self.rect.center[0] - 70, self.rect.center[1]) and gg == 0:
            val = 2
            enemy_run = False
            enemy.update(0, 0, 4)
            dmg_2[all_team_crips_x.index(self.rect.center[0])] += 2
            if 16 in dmg_2 and self.rect.center[0] == all_team_crips_x[dmg_2.index(16)]:
                self.rect.x += 100000
                del dmg_2[dmg_2.index(16)]
                dmg_2.append(0)
        if tower_enemy.rect.center[0] - self.rect.center[0] <= 50 and self.rect.x < 10000 and val != 3:
            val = 2
            tower_as_hp -= 1
        elif self.rect.center[0] > enemy.rect.center[0] and enemy.rect.collidepoint(self.rect.center[0] + 80, self.rect.center[1]):
            val = 2
            enemy_run = False
            enemy.update(0, 0, 4)
        elif (self.rect.center[0] + 50 in all_en_crips_x or self.rect.center[0] + 49 in all_en_crips_x or self.rect.center[0] + 51 in all_en_crips_x) and val != 3:
            val = 2
            try:
                dmg[all_en_crips_x.index(self.rect.center[0] + 50)] += 2
            except:
                pass
            try:
                dmg[all_en_crips_x.index(self.rect.center[0] + 51)] += 2
            except:
                pass
            try:
                dmg[all_en_crips_x.index(self.rect.center[0] + 49)] += 2
            except:
                pass
            Enemy_crip.update(3)
        if val == 1:
            self.rect.x += 1
            old = self.rect
            self.sheet = self.sheet1
            self.frames = []
            self.cut_sheet(self.sheet, 8, 1, self.rect.x, self.rect.y)
            self.rect = old
        else:
            old = self.rect
            self.sheet = self.sheet2
            self.frames = []
            self.cut_sheet(self.sheet, 8, 1, self.rect.x, self.rect.y)
            self.rect = old
        if val == 3:
            if 16 in dmg_2 and self.rect.center[0] == all_team_crips_x[dmg_2.index(16)]:
                self.rect.x += 100000
                del dmg_2[dmg_2.index(16)]
                dmg_2.append(0)
        if val != 3:
            all_team_crips_x.append(self.rect.center[0])
            del all_team_crips_x[0]
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Crips_en(pygame.sprite.Sprite):
    sheet1 = pygame.image.load("data/Run.png")
    sheet1 = pygame.transform.flip(sheet1, 1, 0)
    sheet2 = pygame.image.load("data/Attack.png")
    sheet2 = pygame.transform.flip(sheet2, 1, 0)

    def __init__(self, group, x1, y1):
        super().__init__(group)
        self.sheet = self.sheet1
        self.frames = []
        self.cut_sheet(self.sheet, 8, 1, x1, y1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(224, 112)

    def cut_sheet(self, sheet, columns, rows, x1, y1):
        self.rect = pygame.Rect(x1, y1, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, val, x1=0, y1=0):
        global tower_en_hp
        if self.rect.center[0] < ass.rect.center[0] and ass.rect.collidepoint(self.rect.center[0] - 70, self.rect.center[1]):
            val = 2
        if self.rect.center[0] - tower_as.rect.center[0] <= 50 and self.rect.x > -1000 and val != 3:
            val = 2
            tower_en_hp -= 1
        elif self.rect.center[0] > ass.rect.center[0] and ass.rect.collidepoint(self.rect.center[0] + 80, self.rect.center[1]):
            val = 2
        elif (self.rect.center[0] - 50 in all_team_crips_x or self.rect.center[0] - 49 in all_team_crips_x or self.rect.center[0] - 51 in all_team_crips_x or self.rect.center[0] - 48 in all_team_crips_x or self.rect.center[0] - 52 in all_team_crips_x or self.rect.center[0] - 47 in all_team_crips_x or self.rect.center[0] - 53 in all_team_crips_x) and val != 3:
            val = 2
            try:
                dmg_2[all_team_crips_x.index(self.rect.center[0] - 50)] += 1
            except:
                pass
            try:
                dmg_2[all_team_crips_x.index(self.rect.center[0] - 51)] += 1
            except:
                pass
            try:
                dmg_2[all_team_crips_x.index(self.rect.center[0] - 49)] += 1
            except:
                pass
            Team_crip.update(3)
        if val == 1:
            self.rect.x -= 1
            old = self.rect
            self.sheet = self.sheet1
            self.frames = []
            self.cut_sheet(self.sheet, 8, 1, self.rect.x, self.rect.y)
            self.rect = old
        elif val == 2:
            old = self.rect
            self.sheet = self.sheet2
            self.frames = []
            self.cut_sheet(self.sheet, 8, 1, self.rect.x, self.rect.y)
            self.rect = old
        if val == 3:
            if 16 in dmg and self.rect.center[0] == all_en_crips_x[dmg.index(16)]:
                self.rect.x -= 100000
                del dmg[dmg.index(16)]
                dmg.append(0)
        if val != 3:
            all_en_crips_x.append(self.rect.center[0])
            del all_en_crips_x[0]
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Enemy(pygame.sprite.Sprite):
    sheet1 = pygame.image.load("data/stay.png")
    sheet2 = pygame.image.load("data/dei.png")
    sheet3 = pygame.image.load("data/water_att.png")
    sheet3_r = pygame.transform.flip(sheet3, 1, 0)
    sheet4 = pygame.image.load("data/water_run.png")
    sheet4_r = pygame.transform.flip(sheet4, 1, 0)
    r_ab = pygame.image.load("data/water_r.png")
    r_ab2 = pygame.transform.flip(r_ab, 1, 0)
    w_ab = pygame.image.load("data/water_w.png")
    w_ab2 = pygame.transform.flip(w_ab, 1, 0)
    q_ab = pygame.image.load("data/water_q.png")
    q_ab2 = pygame.transform.flip(q_ab, 1, 0)

    def __init__(self, group):
        super().__init__(group)
        self.sheet = self.sheet1
        self.frames = []
        self.cut_sheet(self.sheet, 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(224, 112)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(1100, 550, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x1, y1, val=2):
        old = self.rect
        if val == 1:
            old = self.rect
            self.sheet = self.sheet2
            self.frames = []
            self.cut_sheet(self.sheet, 16, 1)
            self.rect = old
        if val == 3:
            if ass.rect.x > self.rect.center[0]:
                self.sheet = self.sheet4
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif ass.rect.x < self.rect.center[0]:
                self.sheet = self.sheet4_r
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
        if val == 2:
            old = self.rect
            self.sheet = self.sheet1
            self.frames = []
            self.cut_sheet(self.sheet, 8, 1)
            self.rect = old
            self.rect.x = x1
            self.rect.y = y1
        if val == 4:
            if ass.rect.center[0] > self.rect.center[0]:
                self.sheet = self.sheet3
                self.frames = []
                self.cut_sheet(self.sheet, 7, 1)
                self.rect = old
            elif ass.rect.center[0] < self.rect.center[0]:
                self.sheet = self.sheet3_r
                self.frames = []
                self.cut_sheet(self.sheet, 7, 1)
                self.rect = old
        if val == 5:
            if ass.rect.center[0] > self.rect.center[0]:
                self.sheet = self.r_ab
                self.frames = []
                self.cut_sheet(self.sheet, 32, 1)
                self.rect = old
            elif ass.rect.center[0] < self.rect.center[0]:
                self.sheet = self.r_ab2
                self.frames = []
                self.cut_sheet(self.sheet, 32, 1)
                self.rect = old
        if val == 6:
            if ass.rect.center[0] > self.rect.center[0]:
                self.sheet = self.w_ab
                self.frames = []
                self.cut_sheet(self.sheet, 27, 1)
                self.rect = old
            elif ass.rect.center[0] < self.rect.center[0]:
                self.sheet = self.w_ab2
                self.frames = []
                self.cut_sheet(self.sheet, 27, 1)
                self.rect = old
        if val == 7:
            if ass.rect.center[0] > self.rect.center[0]:
                self.sheet = self.q_ab
                self.frames = []
                self.cut_sheet(self.sheet, 21, 1)
                self.rect = old
            elif ass.rect.center[0] < self.rect.center[0]:
                self.sheet = self.q_ab2
                self.frames = []
                self.cut_sheet(self.sheet, 21, 1)
                self.rect = old


class AnimatedSprite(pygame.sprite.Sprite):
    if hero_mega_val == 3:
        sheet1 = pygame.image.load("data/water_run.png")
        sheet2 = pygame.transform.flip(sheet1, 1, 0)
        sheet3 = pygame.image.load("data/stay.png")
        q_ab = pygame.image.load("data/water_q.png")
        w_ab = pygame.image.load("data/water_w.png")
        r_ab = pygame.image.load("data/water_r.png")
        q_ab2 = pygame.transform.flip(q_ab, 1, 0)
        w_ab2 = pygame.transform.flip(w_ab, 1, 0)
        r_ab2 = pygame.transform.flip(r_ab, 1, 0)
        att = pygame.image.load("data/water_att.png")
        att2 = pygame.transform.flip(att, 1, 0)
        hero_die_again = pygame.image.load("data/dei.png")
    elif hero_mega_val == 4:
        sheet1 = pygame.image.load("data/ass_ran.png")
        sheet2 = pygame.transform.flip(sheet1, 1, 0)
        sheet3 = pygame.image.load("data/pokoi.png")
        q_ab = pygame.image.load("data/Q.png")
        w_ab = pygame.image.load("data/W.png")
        r_ab = pygame.image.load("data/R.png")
        q_ab2 = pygame.transform.flip(q_ab, 1, 0)
        w_ab2 = pygame.transform.flip(w_ab, 1, 0)
        r_ab2 = pygame.transform.flip(r_ab, 1, 0)
        att = pygame.image.load("data/att.png")
        att2 = pygame.transform.flip(att, 1, 0)
        hero_die_again = pygame.image.load("data/ass_die.png")
    elif hero_mega_val == 1:
        sheet1 = pygame.image.load("data/mon_run.png")
        sheet2 = pygame.transform.flip(sheet1, 1, 0)
        sheet3 = pygame.image.load("data/mon_stay.png")
        q_ab = pygame.image.load("data/mon_q.png")
        w_ab = pygame.image.load("data/mon_w.png")
        r_ab = pygame.image.load("data/mon_r.png")
        q_ab2 = pygame.transform.flip(q_ab, 1, 0)
        w_ab2 = pygame.transform.flip(w_ab, 1, 0)
        r_ab2 = pygame.transform.flip(r_ab, 1, 0)
        att = pygame.image.load("data/mon_att.png")
        att2 = pygame.transform.flip(att, 1, 0)
        hero_die_again = pygame.image.load("data/mon_die.png")
    elif hero_mega_val == 2:
        sheet1 = pygame.image.load("data/fire_run.png")
        sheet2 = pygame.transform.flip(sheet1, 1, 0)
        sheet3 = pygame.image.load("data/fire_stay.png")
        q_ab = pygame.image.load("data/fire_q.png")
        w_ab = pygame.image.load("data/fire_w.png")
        r_ab = pygame.image.load("data/fire_r.png")
        q_ab2 = pygame.transform.flip(q_ab, 1, 0)
        w_ab2 = pygame.transform.flip(w_ab, 1, 0)
        r_ab2 = pygame.transform.flip(r_ab, 1, 0)
        att = pygame.image.load("data/fire_att.png")
        att2 = pygame.transform.flip(att, 1, 0)
        hero_die_again = pygame.image.load("data/fire_die.png")

    def __init__(self, group):
        super().__init__(group)
        self.sheet = self.sheet1
        self.frames = []
        self.cut_sheet(self.sheet, 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(224, 112)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(-300, 550, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x1, y1, act=0):
        old = self.rect
        if hero_mega_val == 4:
            if act == 4:
                if x1 > self.rect.center[0]:
                    self.sheet = self.att
                    self.frames = []
                    self.cut_sheet(self.sheet, 8, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.att2
                    self.frames = []
                    self.cut_sheet(self.sheet, 8, 1)
                    self.rect = old
            elif act == 1:
                if x1 > self.rect.center[0]:
                    self.sheet = self.q_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 8, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.q_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 8, 1)
                    self.rect = old
            elif act == 2:
                if x1 > self.rect.center[0]:
                    self.sheet = self.w_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 26, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.w_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 26, 1)
                    self.rect = old
            elif act == 3:
                if x1 > self.rect.center[0]:
                    self.sheet = self.r_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 30, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.r_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 30, 1)
                    self.rect = old
            elif act == 5:
                self.sheet = self.hero_die_again
                self.frames = []
                self.cut_sheet(self.sheet, 19, 1)
                self.rect = old
            elif act == 6:
                old = self.rect
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
                self.rect.x = x1
                self.rect.y = y1
            elif x1 > self.rect.center[0]:
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 < self.rect.center[0]:
                self.sheet = self.sheet2
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 == self.rect.center[0] and y1 == self.rect.center[1]:
                self.sheet = self.sheet3
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
        elif hero_mega_val == 1:
            if act == 4:
                if x1 > self.rect.center[0]:
                    self.sheet = self.att
                    self.frames = []
                    self.cut_sheet(self.sheet, 6, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.att2
                    self.frames = []
                    self.cut_sheet(self.sheet, 6, 1)
                    self.rect = old
            elif act == 1:
                if x1 > self.rect.center[0]:
                    self.sheet = self.q_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 12, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.q_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 12, 1)
                    self.rect = old
            elif act == 2:
                if x1 > self.rect.center[0]:
                    self.sheet = self.w_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 24, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.w_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 24, 1)
                    self.rect = old
            elif act == 3:
                if x1 > self.rect.center[0]:
                    self.sheet = self.r_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 25, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.r_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 25, 1)
                    self.rect = old
            elif act == 5:
                self.sheet = self.hero_die_again
                self.frames = []
                self.cut_sheet(self.sheet, 16, 1)
                self.rect = old
            elif act == 6:
                old = self.rect
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
                self.rect.x = x1
                self.rect.y = y1
            elif x1 > self.rect.center[0]:
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 < self.rect.center[0]:
                self.sheet = self.sheet2
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 == self.rect.center[0] and y1 == self.rect.center[1]:
                self.sheet = self.sheet3
                self.frames = []
                self.cut_sheet(self.sheet, 6, 1)
                self.rect = old
        elif hero_mega_val == 3:
            if act == 4:
                if x1 > self.rect.center[0]:
                    self.sheet = self.att
                    self.frames = []
                    self.cut_sheet(self.sheet, 7, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.att2
                    self.frames = []
                    self.cut_sheet(self.sheet, 7, 1)
                    self.rect = old
            elif act == 1:
                if x1 > self.rect.center[0]:
                    self.sheet = self.q_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 21, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.q_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 21, 1)
                    self.rect = old
            elif act == 2:
                if x1 > self.rect.center[0]:
                    self.sheet = self.w_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 27, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.w_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 27, 1)
                    self.rect = old
            elif act == 3:
                if x1 > self.rect.center[0]:
                    self.sheet = self.r_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 32, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.r_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 32, 1)
                    self.rect = old
            elif act == 5:
                self.sheet = self.hero_die_again
                self.frames = []
                self.cut_sheet(self.sheet, 16, 1)
                self.rect = old
            elif act == 6:
                old = self.rect
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
                self.rect.x = x1
                self.rect.y = y1
            elif x1 > self.rect.center[0]:
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 < self.rect.center[0]:
                self.sheet = self.sheet2
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 == self.rect.center[0] and y1 == self.rect.center[1]:
                self.sheet = self.sheet3
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
        elif hero_mega_val == 2:
            if act == 4:
                if x1 > self.rect.center[0]:
                    self.sheet = self.att
                    self.frames = []
                    self.cut_sheet(self.sheet, 11, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.att2
                    self.frames = []
                    self.cut_sheet(self.sheet, 11, 1)
                    self.rect = old
            elif act == 1:
                if x1 > self.rect.center[0]:
                    self.sheet = self.q_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 19, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.q_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 19, 1)
                    self.rect = old
            elif act == 2:
                if x1 > self.rect.center[0]:
                    self.sheet = self.w_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 28, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.w_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 28, 1)
                    self.rect = old
            elif act == 3:
                if x1 > self.rect.center[0]:
                    self.sheet = self.r_ab
                    self.frames = []
                    self.cut_sheet(self.sheet, 18, 1)
                    self.rect = old
                elif x1 < self.rect.center[0]:
                    self.sheet = self.r_ab2
                    self.frames = []
                    self.cut_sheet(self.sheet, 18, 1)
                    self.rect = old
            elif act == 5:
                self.sheet = self.hero_die_again
                self.frames = []
                self.cut_sheet(self.sheet, 13, 1)
                self.rect = old
            elif act == 6:
                old = self.rect
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
                self.rect.x = x1
                self.rect.y = y1
            elif x1 > self.rect.center[0]:
                self.sheet = self.sheet1
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 < self.rect.center[0]:
                self.sheet = self.sheet2
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old
            elif x1 == self.rect.center[0] and y1 == self.rect.center[1]:
                self.sheet = self.sheet3
                self.frames = []
                self.cut_sheet(self.sheet, 8, 1)
                self.rect = old


class Hp(pygame.sprite.Sprite):
    hp = pygame.image.load("data/hp.png").convert()
    hp1 = pygame.image.load("data/hp1.png").convert()

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.hp
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self, x1=0, y1=0, val=1):
        global n, x_hp, xx
        if n == 0 and val == 2:
            xx = x1
            n += 1
        if val == 1:
            if hp_die // 10 <= hp_die - hp_now:
                if self.rect.x == x_hp:
                    self.image = Hp.hp1
        elif val == 2:
            self.rect.x = xx
            self.rect.y = y1 - 40
            self.image = Hp.hp
            xx += 7
        elif val == 3:
            self.rect.x += x1
            self.rect.y += y1


class Hp_hero(pygame.sprite.Sprite):
    hp = pygame.image.load("data/hp.png").convert()
    hp1 = pygame.image.load("data/hp1.png").convert()

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.hp
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self, x1=0, y1=0, val=1):
        global n_hero, x_hp_hero, xx_hero
        if n_hero == 0 and val == 2:
            xx_hero = x1
            n_hero += 1
        if val == 1:
            if hp_hero_die // 10 <= hp_hero_die - hp_hero_now:
                if self.rect.x == x_hp_hero:
                    self.image = Hp_hero.hp1
        elif val == 2:
            self.rect.x = xx_hero
            self.rect.y = y1 - 40
            self.image = Hp_hero.hp
            xx_hero += 7
        elif val == 3:
            self.rect.x += x1
            self.rect.y += y1


camera = Camera()
dragon = pygame.sprite.Group()
Team_crip = pygame.sprite.Group()
Enemy_crip = pygame.sprite.Group()
Shells = pygame.sprite.Group()
HP = pygame.sprite.Group()
HP_HERO = pygame.sprite.Group()
mapa = Map(dragon)
ass = AnimatedSprite(dragon)
enemy = Enemy(dragon)
tower_as = Tower(dragon, (300, 650))
tower_enemy = Tower(dragon, (1100, 650))
x_hp = enemy.rect.center[0] - 40
y = enemy.rect.center[1]
x_hp_hero = ass.rect.center[0] - 40
crip_x = -300
crip_en_x = 1100
crip_y = 550
shell_en_x = 1100
shell_en_y = 650
all_team_crips_x = []
all_en_crips_x = []
tower_as_hp = 500
tower_en_hp = 500
dmg = []
dmg_2 = []
for i in range(10):
    x_hp += 7
    dragon.add(Hp(HP, x_hp, y))
    x_hp_hero += 7
    dragon.add(Hp_hero(HP_HERO, x_hp_hero, y))
for i in range(4):
    dragon.add(Crips(Team_crip, crip_x, crip_y))
    crip_x += 50
    dmg.append(0)
    all_team_crips_x.append(crip_x)
    dragon.add(Crips_en(Enemy_crip, crip_en_x, crip_y))
    crip_en_x -= 50
    dmg_2.append(0)
    all_en_crips_x.append(crip_en_x)
tic_res_crip = time.perf_counter()
toc_res_crip = 45
dragon.draw(screen)
crip_x = -300
cripen_en_x = 1100
pygame.display.update()
clock = pygame.time.Clock()
draw = False
stay = True
running = True
cam = False
Q = False
W = False
R = False
Die = False
check_attack_q = False
count_q = 0
count_w = 0
count_r = 0
count_enemy_r = 0
count_enemy_w = 0
count_enemy_q = 0
xx = 0
att_count = 0
enemy_att_count = 0
enemy_stay = False
attack = False
check_attack = False
tic_q = 0
toc_q = 3
tic_w = 0
toc_w = 6
tic_r = 0
toc_r = 30
tic_enemy_r = 0
toc_enemy_r = 30
tic_enemy_w = 0
toc_enemy_w = 10
tic_enemy_q = 0
toc_enemy_q = 4
tic_as_tower = 0
toc_as_tower = 4
n = 0
n_hero = 0
xx_hero = 0
gg = 0
gg_hero = 0
count_check = 0
toc_dienemy = 0
tic_dienemy = 15
toc_diehero = 0
tic_diehero = 15
toc_attenemy = 1
tic_attenemy = 0
die = 1
die_hero = 1
count = 0
i_hp = 0
count_hero = 0
count_hero_check = 0
i_hp_hero = 0
hp_die = 500
hp_now = hp_die
hero_attack = 100
hero_attack_q = 50
hero_attack_w = 50
hero_attack_r = 200
hp_hero_die = 2000
hp_hero_now = hp_die
enemy_attack = False
enemy_run = True
hero_die = False
enemy_q = False
enemy_w = False
enemy_r = False
x_res_enemy = 1350
y_res_enemy = 650
x_res_hero = -100
y_res_hero = 650
cam_max_x = 16
cam_max_y = ass.rect.center[1] - 500
enemy_attack_check = True
camera.update(ass.rect.center[0] - 20, ass.rect.center[1] - 500)
x_res_enemy -= ass.rect.center[0] - 20
y_res_enemy -= ass.rect.center[1] - 500
shell_en_x -= ass.rect.center[0] - 20
shell_en_y -= ass.rect.center[1] - 500
x_res_hero -= ass.rect.center[0] - 20
y_res_hero -= ass.rect.center[1] - 500
map(lambda x: x - 3, all_team_crips_x)
map(lambda x: x - 3, all_en_crips_x)
crip_x -= ass.rect.center[0] - 20
crip_en_x -= ass.rect.center[0] - 20
crip_y -= ass.rect.center[1] - 500
x_hp -= ass.rect.center[0] - 20
x_hp_hero -= ass.rect.center[0] - 20
for sprite in dragon:
    camera.apply(sprite)
screen.fill(0)
dragon.draw(screen)
pygame.display.update()
clock.tick(60)
while running:
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    if x > 890 and 10 < y < 589 and cam_max_x + 3 < 586:
        camera.update(3, 0)
        x1 -= 3
        cam_max_x += 3
        x_res_enemy -= 3
        x_res_hero -= 3
        shell_en_x -= 3
        crip_x -= 3
        crip_en_x -= 3
        x_hp -= 3
        x_hp_hero -= 3
        map(lambda x: x - 3, all_team_crips_x)
        map(lambda x: x - 3, all_en_crips_x)
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if y > 590 and 10 < x < 889 and cam_max_y < 600:
        camera.update(0, 3)
        cam_max_y += 3
        y1 -= 3
        y_res_enemy -= 3
        shell_en_y -= 3
        y_res_hero -= 3
        crip_y -= 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if x < 10 and 10 < y < 589 and cam_max_x - 3 > 0:
        camera.update(-3, 0)
        cam_max_x -= 3
        x1 += 3
        x_hp += 3
        x_hp_hero += 3
        shell_en_x += 3
        x_res_enemy += 3
        x_res_hero += 3
        map(lambda x: x + 3, all_team_crips_x)
        map(lambda x: x - 3, all_en_crips_x)
        crip_x += 3
        crip_en_x += 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if y < 10 and 10 < x < 889 and cam_max_y > 100:
        camera.update(0, -3)
        cam_max_y -= 3
        y1 += 3
        y_res_enemy += 3
        y_res_hero += 3
        shell_en_y += 3
        crip_y += 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if x > 890 and y > 590:
        camera.update(3, 3)
        x1 -= 3
        y1 -= 3
        x_res_enemy -= 3
        y_res_enemy -= 3
        shell_en_x -= 3
        shell_en_y -= 3
        x_res_hero -= 3
        y_res_hero -= 3
        map(lambda x: x - 3, all_team_crips_x)
        map(lambda x: x - 3, all_en_crips_x)
        crip_x -= 3
        crip_en_x -= 3
        crip_y -= 3
        x_hp -= 3
        x_hp_hero -= 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if y > 590 and 10 > x:
        camera.update(-3, 3)
        x1 += 3
        y1 -= 3
        x_res_enemy += 3
        y_res_enemy -= 3
        x_res_hero += 3
        shell_en_x += 3
        shell_en_y -= 3
        y_res_hero -= 3
        crip_x += 3
        crip_en_x -= 3
        map(lambda x: x + 3, all_team_crips_x)
        map(lambda x: x + 3, all_en_crips_x)
        crip_y -= 3
        x_hp += 3
        x_hp_hero += 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if x < 10 and 10 > y:
        camera.update(-3, -3)
        x1 += 3
        y1 += 3
        x_res_enemy += 3
        y_res_enemy += 3
        shell_en_x += 3
        shell_en_y += 3
        x_res_hero += 3
        map(lambda x: x + 3, all_team_crips_x)
        map(lambda x: x + 3, all_en_crips_x)
        y_res_hero += 3
        crip_x += 3
        crip_en_x += 3
        crip_y += 3
        x_hp += 3
        x_hp_hero += 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    if y < 10 and x > 890:
        camera.update(3, -3)
        x1 -= 3
        y1 += 3
        x_res_enemy -= 3
        y_res_enemy += 3
        shell_en_x -= 3
        shell_en_y += 3
        x_res_hero -= 3
        y_res_hero += 3
        map(lambda x: x - 3, all_team_crips_x)
        map(lambda x: x - 3, all_en_crips_x)
        crip_x -= 3
        crip_en_x += 3
        crip_y += 3
        x_hp -= 3
        x_hp_hero -= 3
        cam = True
        for sprite in dragon:
            camera.apply(sprite)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            x1, y1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            stay = False
            check_attack_q = True
            draw = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            x1, y1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            stay = False
            draw = False
            W = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            x1, y1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            stay = False
            draw = False
            R = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos[0], event.pos[1]
            if enemy.rect.center[0] - 10 <= x1 <= enemy.rect.center[0] + 10 and enemy.rect.center[1] + 14 <= y1 <= enemy.rect.center[1] + 56:
                check_attack = True
                stay = False
            else:
                draw = True
                stay = False
                x1, y1 = event.pos[0], event.pos[1]
                y1 = y1 - 28
    if cam:
        t = 80
    if 10 < x < 890 and 10 < y < 590:
        cam = False
        t = 70
    if check_attack:
        if ass.rect.center[0] < enemy.rect.center[0] and enemy.rect.collidepoint(ass.rect.center[0] - 70, ass.rect.center[1]):
            attack = True
            draw = False
            check_attack = False
        elif ass.rect.center[0] > enemy.rect.center[0] and enemy.rect.collidepoint(ass.rect.center[0] + 80, ass.rect.center[1]):
            attack = True
            draw = False
            check_attack = False
        else:
            draw = True
    if check_attack_q:
        if ass.rect.center[0] < enemy.rect.center[0] and enemy.rect.collidepoint(ass.rect.center[0] - 70, ass.rect.center[1]):
            Q = True
            draw = False
            check_attack_q = False
        elif ass.rect.center[0] > enemy.rect.center[0] and enemy.rect.collidepoint(ass.rect.center[0] + 80, ass.rect.center[1]):
            Q = True
            draw = False
            check_attack_q = False
        else:
            draw = True

    if gg_hero == 1:
        draw = False

    if draw:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
        ass.image = ass.frames[ass.cur_frame]
        if x1 != ass.rect.center[0] or y1 != ass.rect.center[1]:
            if x1 > ass.rect.center[0]:
                ass.rect.x += 1
                HP_HERO.update(1, 0, 3)
                x_hp_hero += 1
            elif x1 < ass.rect.center[0]:
                ass.rect.x -= 1
                HP_HERO.update(-1, 0, 3)
                x_hp_hero -= 1
            if y1 > ass.rect.center[1]:
                ass.rect.y += 1
                HP_HERO.update(0, 1, 3)
            elif y1 < ass.rect.center[1]:
                ass.rect.y -= 1
                HP_HERO.update(0, -1, 3)
        else:
            draw = False
            stay = True
            ass.update(x1, y1)
        ass.update(x1, y1)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)
    if stay:
        x1 = ass.rect.center[0]
        y1 = ass.rect.center[1]
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
        ass.image = ass.frames[ass.cur_frame]
        ass.update(x1, y1)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)
    if Q:
        if hero_mega_val == 2:
            z = 19
        else:
            z = 8
        if toc_q - tic_q >= 3:
            if count_q != z:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
                ass.image = ass.frames[ass.cur_frame]
                ass.update(x1, y1, 1)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                count_q = count_q + 1
            else:
                if not Die and count <= 10:
                    hp_now -= hero_attack_q
                    count_check += hero_attack_q / (hp_die // 10)
                    count = int(count_check)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                Q = False
                stay = True
                count_q = 0
                tic_q = time.perf_counter()
        else:

            stay = True
            Q = False
    if W:
        if toc_w - tic_w >= 6:
            if count_w != 26:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
                ass.image = ass.frames[ass.cur_frame]
                ass.update(x1, y1, 2)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                count_w += 1
            else:
                if not Die and count <= 10:
                    hp_now -= hero_attack_w
                    count_check += hero_attack_w / (hp_die // 10)
                    count = int(count_check)
                W = False
                stay = True
                count_w = 0
                tic_w = time.perf_counter()

        else:
            W = False
            stay = True
    if R:
        if toc_r - tic_r >= 30:
            if count_r != 30:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
                ass.image = ass.frames[ass.cur_frame]
                ass.update(x1, y1, 3)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                count_r += 1
            else:
                if not Die and count <= 10:
                    hp_now -= hero_attack_r
                    count_check += hero_attack_r / (hp_die // 10)
                    count = int(count_check)
                R = False
                stay = True
                count_r = 0
                tic_r = time.perf_counter()
        else:
            R = False
            stay = True
    if attack:
        if att_count != 8:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
            ass.image = ass.frames[ass.cur_frame]
            ass.update(x1, y1, 4)
            screen.fill(0)
            dragon.draw(screen)
            pygame.display.update()
            clock.tick(t)
            att_count += 1
        else:
            attack = False
            stay = True
            att_count = 0
            if not Die:
                hp_now -= hero_attack
                count_check += hero_attack / (hp_die // 10)
                count = int(count_check)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)

    if i_hp < count:
        HP.update()
        x_hp -= 7
        i_hp += 1
    else:
        if i_hp == 10:

            i_hp = 0
            count = 0
            count_check = 0.00000000000002
            Die = True
            enemy_stay = False
            enemy_attack_check = False
            enemy_attack = False
            hp_die = 1100
            hp_now = hp_die

    if Die:
        if die != 8:
            enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
            enemy.image = enemy.frames[enemy.cur_frame]
            enemy.update(0, 0, 1)
            screen.fill(0)
            dragon.draw(screen)
            pygame.display.update()
            die += 1
        else:
            gg = 1
            die = 0
            tic_dienemy = time.perf_counter()
            enemy_stay = False
            Die = False
            kills += 1
            enemy_attack_check = False
            with sqlite3.connect('database.db') as con:
                con.execute('UPDATE statistic SET kills = ?',
                            (str(kills))).fetchall()

    if not enemy_stay and gg == 1:
        if toc_dienemy - tic_dienemy >= 15:
            gg = 0
            enemy.update(x_res_enemy, y_res_enemy, 2)
            HP.update(enemy.rect.center[0] - 40, enemy.rect.center[1] + 40, 2)
            n = 0
            x_hp = enemy.rect.center[0] + 23
            if enemy.rect.center[0] != ass.rect.center[0] or enemy.rect.center[1] != ass.rect.center[1]:
                enemy_run = True
            else:
                enemy_stay = True
            enemy_attack_check = True

    if enemy_stay and gg == 0:
        enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
        enemy.image = enemy.frames[enemy.cur_frame]
        enemy.update(enemy.rect.x, enemy.rect.y, 2)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)

    if enemy_attack_check and gg == 0:
        if ass.rect.center[0] < enemy.rect.center[0] and enemy.rect.collidepoint(ass.rect.center[0] - 70, ass.rect.center[1]) and gg_hero == 0:
            enemy_run = False
            enemy_stay = False
            enemy_attack = True
            enemy_attack_check = False
        elif ass.rect.center[0] > enemy.rect.center[0] and enemy.rect.collidepoint(ass.rect.center[0] + 80, ass.rect.center[1]) and gg_hero == 0:
            enemy_run = False
            enemy_stay = False
            enemy_attack = True
            enemy_attack_check = False
        else:
            if enemy.rect.center[0] != ass.rect.center[0] or enemy.rect.center[1] != ass.rect.center[1] and gg_hero == 0:
                enemy_run = True
            else:
                enemy_stay = True
                enemy_run = False
            enemy_attack = False

    if enemy_attack and gg == 0:
        if toc_enemy_r - tic_enemy_r >= 30 and gg_hero == 0:
            enemy_r = True
        elif toc_enemy_w - tic_enemy_w >= 10 and gg_hero == 0:
            enemy_w = True
        elif toc_enemy_q - tic_enemy_q >= 4 and gg_hero == 0:
            enemy_q = True
        if toc_attenemy - tic_attenemy > 1 and toc_diehero - tic_diehero >= 15:
            if enemy_att_count != 7:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
                enemy.image = enemy.frames[enemy.cur_frame]
                enemy.update(enemy.rect.x, enemy.rect.y, 4)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                enemy_att_count += 1
            else:
                tic_attenemy = time.perf_counter()
                enemy_att_count = 0
                enemy_attack = False
                enemy_stay = True
                if not hero_die:
                    hp_hero_now -= enemy_attack_m
                    count_hero_check += enemy_attack_m / (hp_hero_die // 10)
                    count_hero = int(count_hero_check)
                    if count_hero > 10:
                        count_hero = 10

    if i_hp_hero < count_hero:
        HP_HERO.update()
        x_hp_hero -= 7
        i_hp_hero += 1
    else:
        if i_hp_hero == 10:
            i_hp_hero = 0
            count_hero = 0
            count_hero_check = 0.00000000000002
            hero_die = True
            stay = False
            check_attack = False
            attack = False
            hp_hero_die = 1100
            hp_hero_now = hp_hero_die

    if toc_attenemy - tic_attenemy > 1 and gg == 0:
        enemy_attack_check = True

    if enemy_run and gg == 0:
        enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
        enemy.image = enemy.frames[enemy.cur_frame]
        if enemy.rect.center[0] != ass.rect.center[0] or enemy.rect.center[1] != ass.rect.center[1]:
            enemy_stay = False
            if enemy.rect.center[0] > ass.rect.center[0]:
                enemy.rect.x -= 1
                HP.update(-1, 0, 3)
                x_hp -= 1
            elif enemy.rect.center[0] < ass.rect.center[0]:
                enemy.rect.x += 1
                HP.update(1, 0, 3)
                x_hp += 1
            if enemy.rect.center[1] > ass.rect.center[1]:
                enemy.rect.y -= 1
                HP.update(0, -1, 3)
            elif enemy.rect.center[1] < ass.rect.center[1]:
                enemy.rect.y += 1
                HP.update(0, 1, 3)
        else:
            enemy_run = False
            enemy_stay = True
            enemy.update(x1, y1, 3)
        enemy.update(x1, y1, 3)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)

    if hero_die:
        if die_hero != 17:
            ass.cur_frame = (ass.cur_frame + 1) % len(ass.frames)
            ass.image = ass.frames[ass.cur_frame]
            ass.update(0, 0, 5)
            screen.fill(0)
            dragon.draw(screen)
            pygame.display.update()
            die_hero += 1
        else:
            gg_hero = 1
            die_hero = 0
            tic_diehero = time.perf_counter()
            stay = False
            hero_die = False
            draw = False
            check_attack = False
            deaths += 1
            with sqlite3.connect('database.db') as con:
                con.execute('UPDATE statistic SET deaths = ?',
                            (str(deaths))).fetchall()

    if not stay and gg_hero == 1:
        if toc_diehero - tic_diehero >= 15:
            gg_hero = 0
            ass.update(x_res_hero, y_res_hero, 6)
            HP_HERO.update(ass.rect.center[0] - 40, ass.rect.center[1] + 40, 2)
            n_hero = 0
            x_hp_hero = ass.rect.center[0] + 23
            draw = True
            stay = True
            check_attack = True
            enemy_run = True
            enemy_check_attack = True

    if enemy_r and gg == 0:
        if toc_enemy_r - tic_enemy_r >= 30 and gg_hero == 0:
            enemy_attack_check = False
            enemy_stay = False
            enemy_run = False
            if count_enemy_r != 30:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
                enemy.image = enemy.frames[enemy.cur_frame]
                enemy.update(x1, y1, 5)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                count_enemy_r += 1
            else:
                if not hero_die:
                    hp_hero_now -= enemy_attack_r
                    count_hero_check += enemy_attack_r / (hp_hero_die // 10)
                    count_hero = int(count_hero_check)
                    if count_hero > 10:
                        count_hero = 10
                enemy_r = False
                enemy_stay = True
                enemy_attack_check = True
                enemy_run = True
                count_enemy_r = 0
                tic_enemy_r = time.perf_counter()

    if enemy_w and gg == 0:
        if toc_enemy_w - tic_enemy_w >= 10 and gg_hero == 0:
            enemy_attack_check = False
            enemy_stay = False
            enemy_run = False
            if count_enemy_w != 27:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
                enemy.image = enemy.frames[enemy.cur_frame]
                enemy.update(x1, y1, 6)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                count_enemy_w += 1
            else:
                if not hero_die:
                    hp_hero_now -= enemy_attack_w
                    count_hero_check += enemy_attack_w / (hp_hero_die // 10)
                    count_hero = int(count_hero_check)
                    if count_hero > 10:
                        count_hero = 10
                enemy_w = False
                enemy_stay = True
                enemy_attack_check = True
                enemy_run = True
                count_enemy_w = 0
                tic_enemy_w = time.perf_counter()

    if enemy_q and gg == 0:
        if toc_enemy_q - tic_enemy_q >= 4 and gg_hero == 0:
            enemy_attack_check = False
            enemy_stay = False
            enemy_run = False
            if count_enemy_q != 21:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                enemy.cur_frame = (enemy.cur_frame + 1) % len(enemy.frames)
                enemy.image = enemy.frames[enemy.cur_frame]
                enemy.update(x1, y1, 7)
                screen.fill(0)
                dragon.draw(screen)
                pygame.display.update()
                clock.tick(t)
                count_enemy_q += 1
            else:
                if not hero_die:
                    hp_hero_now -= enemy_attack_w
                    count_hero_check += enemy_attack_1 / (hp_hero_die // 10)
                    count_hero = int(count_hero_check)
                    if count_hero > 10:
                        count_hero = 10
                enemy_q = False
                enemy_stay = True
                enemy_attack_check = True
                enemy_run = True
                count_enemy_q = 0
                tic_enemy_q = time.perf_counter()

    Team_crip.update(1)
    screen.fill(0)
    dragon.draw(screen)
    pygame.display.update()
    clock.tick(t)

    Enemy_crip.update(1)
    screen.fill(0)
    dragon.draw(screen)
    pygame.display.update()
    clock.tick(t)

    if toc_res_crip - tic_res_crip >= 45:
        dragon.add(Crips(Team_crip, crip_x, crip_y))
        crip_x += 50
        dmg.append(0)
        all_team_crips_x.append(0)
        dragon.add(Crips(Team_crip, crip_x, crip_y))
        crip_x += 50
        dmg.append(0)
        all_team_crips_x.append(0)
        dragon.add(Crips(Team_crip, crip_x, crip_y))
        crip_x += 50
        dmg.append(0)
        all_team_crips_x.append(0)
        dragon.add(Crips(Team_crip, crip_x, crip_y))
        crip_x += 50
        dmg.append(0)
        all_team_crips_x.append(0)
        crip_x += -200

    if toc_res_crip - tic_res_crip >= 45:
        dragon.add(Crips_en(Enemy_crip, crip_en_x, crip_y))
        crip_en_x -= 50
        dmg_2.append(0)
        all_en_crips_x.append(0)
        dragon.add(Crips_en(Enemy_crip, crip_en_x, crip_y))
        crip_en_x -= 50
        dmg_2.append(0)
        all_en_crips_x.append(0)
        dragon.add(Crips_en(Enemy_crip, crip_en_x, crip_y))
        crip_en_x -= 50
        dmg_2.append(0)
        all_en_crips_x.append(0)
        dragon.add(Crips_en(Enemy_crip, crip_en_x, crip_y))
        crip_en_x -= 50
        dmg_2.append(0)
        all_en_crips_x.append(0)
        crip_en_x += 200
        tic_res_crip = time.perf_counter()

    if tower_enemy.rect.center[0] - ass.rect.center[0] <= 100 and tower_enemy.rect.center[1] - ass.rect.center[1]:
        if toc_as_tower - tic_as_tower >= 6:
            dragon.add(Shell(Shells, (shell_en_x, shell_en_y)))
            tic_as_tower = time.perf_counter()
        Shells.update(ass.rect.center)
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)
    if tower_as_hp <= 0:
        win()
        wins += 1
        with sqlite3.connect('database.db') as con:
            con.execute('UPDATE statistic SET wins = ?',
                        (str(wins))).fetchall()
        running = False
    elif tower_en_hp <= 0:
        lose()
        los = Lose(dragon, (450, 300))
        screen.fill(0)
        dragon.draw(screen)
        pygame.display.update()
        clock.tick(t)
        losses += 1
        with sqlite3.connect('database.db') as con:
            con.execute('UPDATE statistic SET losses = ?',
                        (str(losses))).fetchall()
        running = False

    toc_q = time.perf_counter()
    toc_w = time.perf_counter()
    toc_r = time.perf_counter()
    toc_enemy_r = time.perf_counter()
    toc_enemy_w = time.perf_counter()
    toc_enemy_q = time.perf_counter()
    toc_dienemy = time.perf_counter()
    toc_diehero = time.perf_counter()
    toc_attenemy = time.perf_counter()
    toc_res_crip = time.perf_counter()
    toc_as_tower = time.perf_counter()