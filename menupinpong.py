import pygame
import client

pygame.init()
pygame.mixer.init()

SCENMENU = 1
SCENSETTINGS = 2
SCENMUSIC = 3
SCENBAL = 4
SCENBG = 5
scen = SCENMENU

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню Пінг-Понг")

icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("images/dg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

font_menu = pygame.font.Font("font1.otf", 40)
font = pygame.font.Font("font1.otf", 30)
font_small = pygame.font.Font("font1.otf", 20)

class animation:
    def __init__(self, x, y, width, height, images):
        self.images = [pygame.transform.scale(pygame.image.load(img), (width, height))
                       for img in images]
        self.frame_index = 0
        self.image_speed = 0.3
        self.rect = self.images[0].get_rect(topleft=(x, y))
        self.cur_img = self.images[0]

    def reset(self):
        screen.blit(self.cur_img, (self.rect.x, self.rect.y))

    def animate(self):
        self.frame_index += self.image_speed
        if self.frame_index >= len(self.images):
            self.frame_index = 0
        self.cur_img = self.images[int(self.frame_index)]

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_idle = (0, 255, 0)
        self.color_hover = (0, 200, 0)
        self.color = self.color_idle
        self.text = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.color_hover
        else:
            self.color = self.color_idle

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        screen.blit(self.text, self.text_rect)

# ===== АНИМАЦИЯ =====
player_run = [
    'images/1.png','images/2.png','images/3.png',
    'images/4.png','images/5.png','images/6.png'
]
animation1 = animation(10, 500, 100, 100, player_run)

# ===== ТЕКСТ =====
text_menu = font_menu.render("Pin-Pong Game!", True, (255, 255, 255))

# ===== КНОПКИ =====
# Главные кнопки меню
start_btn = Button(WIDTH // 2 - 125, 200, 250, 50, "Start game")
settings_btn = Button(WIDTH // 2 - 125, 280, 250, 50, "Settings")
exit_btn = Button(WIDTH // 2 - 125, 360, 250, 50, "Exit")

# Кнопки настроек
exit_settings_btn = Button(WIDTH // 2 + 130, 75, 50, 50, "x")
exit_settings_btn.color_idle = (255, 0, 0)
exit_settings_btn.color_hover = (200, 0, 0)

# Настройки окна settings
frame_settings = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 250, 400, 500)
images_ball = Button(WIDTH // 2 - 162, HEIGHT // 2 - 100, 325, 50, "Ball Images")
images_bg = Button(WIDTH // 2 - 162, HEIGHT // 2 - 25, 325, 50, "Bg Images")
mixic = Button(WIDTH // 2 - 162, HEIGHT // 2 + 50, 325, 50, "Music")

# Окно выбора мяча
ball_exit = Button(730, 25, 50, 50, "x")
ball_exit.color_idle = (255, 0, 0)
ball_exit.color_hover = (200, 0, 0)
frame_ball = pygame.Rect(10, 10, 780, 580)

# Загрузка мячей с увеличенным размером
ball1 = pygame.image.load("images/ball_1.png")
ball1 = pygame.transform.scale(ball1, (120, 120))  # Увеличенный размер

ball2 = pygame.image.load("images/ball_2.png")
ball2 = pygame.transform.scale(ball2, (120, 120))  # Увеличенный размер

ball3 = pygame.image.load("images/ball_3.png")
ball3 = pygame.transform.scale(ball3, (120, 120))  # Увеличенный размер

ball4 = pygame.image.load("images/ball_4.png")
ball4 = pygame.transform.scale(ball4, (120, 120))  # Увеличенный размер

# Рамки для мячей (2 слева, 2 справа)
ball1_frame = pygame.Rect(100, 70, 150, 150)      # Слева сверху
ball2_frame = pygame.Rect(100, 250, 150, 150)     # Слева снизу
ball3_frame = pygame.Rect(550, 70, 150, 150)      # Справа сверху
ball4_frame = pygame.Rect(550, 250, 150, 150)     # Справа снизу

# Кнопка применения мяча
apply_ball_btn = Button(300, 450, 200, 50, "Apply Ball")

# Окно выбора фона
bg_exit = Button(730, 25, 50, 50, "x")
bg_exit.color_idle = (255, 0, 0)
bg_exit.color_hover = (200, 0, 0)
frame_bg = pygame.Rect(10, 10, 780, 580)

# Загрузка фонов
bg1 = pygame.image.load("images/bg_1.jpg")
bg1 = pygame.transform.scale(bg1, (200, 100))

bg2 = pygame.image.load("images/bg_2.jpg")
bg2 = pygame.transform.scale(bg2, (200, 100))

bg3 = pygame.image.load("images/bg_3.jpg")
bg3 = pygame.transform.scale(bg3, (200, 100))

bg4 = pygame.image.load("images/bg_4.jpg")
bg4 = pygame.transform.scale(bg4, (200, 100))

# Рамки для фонов (2 слева, 2 справа)
bg1_frame = pygame.Rect(100, 70, 225, 125)      # Слева сверху
bg2_frame = pygame.Rect(100, 220, 225, 125)     # Слева снизу
bg3_frame = pygame.Rect(475, 70, 225, 125)      # Справа сверху
bg4_frame = pygame.Rect(475, 220, 225, 125)     # Справа снизу

# Кнопка применения фона (опущена ниже)
apply_bg_btn = Button(250, 450, 300, 50, "Apply Bg")

# Окно музыки
exit_mizic = Button(WIDTH // 2 + 130, 75, 50, 50, "x")
exit_mizic.color_idle = (255, 0, 0)
exit_mizic.color_hover = (200, 0, 0)
frame_mizic = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 250, 400, 500)
music_btn_stop = Button(WIDTH // 2 - 162, HEIGHT // 2 + 50, 325, 50, "Pause Music")

# Музыка
click_sound = pygame.mixer.Sound("mizic/minecraft-click-cropped.mp3")
bg_sound = pygame.mixer.Sound("mizic/dbg_song.wav")

# Флаги для отслеживания состояния
music_playing = True
music_started = True

# Переменные для хранения выбранных элементов
selected_bg = None
selected_ball = None
selected_bg_1 = None

start_game_flag = False

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(bg, (0, 0))
    
    # Включаем музыку только один раз при старте
    if not music_started:
        bg_sound.play(-1)  # -1 означает бесконечное повторение
        music_started = True
        music_playing = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if scen == SCENMENU:
                if start_btn.rect.collidepoint(event.pos):
                    # Здесь будет запуск игры
                    import subprocess
                    subprocess.Popen(['python', 'server.py'])
                    start_game_flag = True
                    running = False
                    click_sound.play()
                elif settings_btn.rect.collidepoint(event.pos):
                    scen = SCENSETTINGS
                    click_sound.play()
                elif exit_btn.rect.collidepoint(event.pos):
                    running = False
                    click_sound.play()

            elif scen == SCENSETTINGS:
                if images_ball.rect.collidepoint(event.pos):
                    scen = SCENBAL
                    click_sound.play()
                elif images_bg.rect.collidepoint(event.pos):
                    scen = SCENBG
                    click_sound.play()
                elif mixic.rect.collidepoint(event.pos):
                    scen = SCENMUSIC
                    click_sound.play()
                elif exit_settings_btn.rect.collidepoint(event.pos):
                    scen = SCENMENU
                    click_sound.play()

            elif scen == SCENBAL:
                if ball_exit.rect.collidepoint(event.pos):
                    scen = SCENSETTINGS
                    click_sound.play()
                elif apply_ball_btn.rect.collidepoint(event.pos):
                    if selected_ball:
                        with open("data.txt", "w") as f:
                            f.write(selected_ball)
                        click_sound.play()
                elif ball1_frame.collidepoint(event.pos):
                    selected_ball = "1"
                    print("Ball 1 selected")
                    click_sound.play()
                elif ball2_frame.collidepoint(event.pos):
                    selected_ball = "2"
                    print("Ball 2 selected")
                    click_sound.play()
                elif ball3_frame.collidepoint(event.pos):
                    selected_ball = "3"
                    print("Ball 3 selected")
                    click_sound.play()
                elif ball4_frame.collidepoint(event.pos):
                    selected_ball = "4"
                    print("Ball 4 selected")
                    click_sound.play()

            elif scen == SCENBG:
                if bg_exit.rect.collidepoint(event.pos):
                    scen = SCENSETTINGS
                    click_sound.play()
                elif apply_bg_btn.rect.collidepoint(event.pos):
                    if selected_bg:
                        bg = selected_bg
                        with open("data_bg.txt", "w") as f:
                            f.write(selected_bg_1)
                        click_sound.play()
                elif bg1_frame.collidepoint(event.pos):
                    selected_bg = pygame.transform.scale(pygame.image.load("images/bg_1.jpg"), (WIDTH, HEIGHT))
                    selected_bg_1 = "bg_1"
                    click_sound.play()
                elif bg2_frame.collidepoint(event.pos):
                    selected_bg = pygame.transform.scale(pygame.image.load("images/bg_2.jpg"), (WIDTH, HEIGHT))
                    selected_bg_1 = "bg_2"
                    click_sound.play()
                elif bg3_frame.collidepoint(event.pos):
                    selected_bg = pygame.transform.scale(pygame.image.load("images/bg_3.png"), (WIDTH, HEIGHT))
                    selected_bg_1 = "bg_3"
                    click_sound.play()
                elif bg4_frame.collidepoint(event.pos):
                    selected_bg = pygame.transform.scale(pygame.image.load("images/bg_4.jpg"), (WIDTH, HEIGHT))
                    selected_bg_1 = "bg_4"
                    click_sound.play()
                
                with open("data_bg.txt", "w") as f:
                    f.write(selected_bg_1)

            elif scen == SCENMUSIC:
                if exit_mizic.rect.collidepoint(event.pos):
                    scen = SCENSETTINGS
                    click_sound.play()
                elif music_btn_stop.rect.collidepoint(event.pos):
                    if music_playing:
                        bg_sound.stop()
                        music_playing = False
                    else:
                        bg_sound.play(-1)
                        music_playing = True
                    click_sound.play()

    if scen == SCENMENU:
        start_btn.update()
        settings_btn.update()
        exit_btn.update()

        start_btn.draw(screen)
        settings_btn.draw(screen)
        exit_btn.draw(screen)

        animation1.animate()
        animation1.reset()

        screen.blit(text_menu, (WIDTH // 2 - text_menu.get_width() // 2, 100))

    elif scen == SCENSETTINGS:
        pygame.draw.rect(screen, (50, 50, 50), frame_settings, border_radius=10)
        exit_settings_btn.update()
        exit_settings_btn.draw(screen)
        images_ball.update()
        images_ball.draw(screen)
        images_bg.update()
        images_bg.draw(screen)
        mixic.update()
        mixic.draw(screen)

    elif scen == SCENBAL:
        pygame.draw.rect(screen, (50, 50, 50), frame_ball, border_radius=10)
        
        # Получаем позицию мыши для подсветки
        mouse_pos = pygame.mouse.get_pos()
        
        # Заголовок
        title_text = font.render("Select Ball", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))
        
        ball_exit.update()
        ball_exit.draw(screen)
        
        # Рисуем рамки для мячей с подсветкой
        frame_color = (100, 100, 100)
        
        # Рамка 1 (слева сверху)
        pygame.draw.rect(screen, frame_color, ball1_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), ball1_frame, width=2, border_radius=10)
        if ball1_frame.collidepoint(mouse_pos) or selected_ball == "1":
            pygame.draw.rect(screen, (255, 255, 0), ball1_frame, width=4, border_radius=10)  # Желтая подсветка
        # Картинка мяча по центру рамки
        screen.blit(ball1, (ball1_frame.x + (ball1_frame.width - 120) // 2, ball1_frame.y + (ball1_frame.height - 120) // 2))
        
        # Рамка 2 (слева снизу)
        pygame.draw.rect(screen, frame_color, ball2_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), ball2_frame, width=2, border_radius=10)
        if ball2_frame.collidepoint(mouse_pos) or selected_ball == "2":
            pygame.draw.rect(screen, (255, 255, 0), ball2_frame, width=4, border_radius=10)  # Желтая подсветка
        screen.blit(ball2, (ball2_frame.x + (ball2_frame.width - 120) // 2, ball2_frame.y + (ball2_frame.height - 120) // 2))
        
        # Рамка 3 (справа сверху)
        pygame.draw.rect(screen, frame_color, ball3_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), ball3_frame, width=2, border_radius=10)
        if ball3_frame.collidepoint(mouse_pos) or selected_ball == "3":
            pygame.draw.rect(screen, (255, 255, 0), ball3_frame, width=4, border_radius=10)  # Желтая подсветка
        screen.blit(ball3, (ball3_frame.x + (ball3_frame.width - 120) // 2, ball3_frame.y + (ball3_frame.height - 120) // 2))
        
        # Рамка 4 (справа снизу)
        pygame.draw.rect(screen, frame_color, ball4_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), ball4_frame, width=2, border_radius=10)
        if ball4_frame.collidepoint(mouse_pos) or selected_ball == "4":
            pygame.draw.rect(screen, (255, 255, 0), ball4_frame, width=4, border_radius=10)  # Желтая подсветка
        screen.blit(ball4, (ball4_frame.x + (ball4_frame.width - 120) // 2, ball4_frame.y + (ball4_frame.height - 120) // 2))
        
        # Кнопка применения мяча
        apply_ball_btn.update()
        apply_ball_btn.draw(screen)

    elif scen == SCENBG:
        pygame.draw.rect(screen, (50, 50, 50), frame_bg, border_radius=10)
        
        # Заголовок
        title_text = font.render("Select Background", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))
        
        bg_exit.update()
        bg_exit.draw(screen)
        
        # Получаем позицию мыши для подсветки
        mouse_pos = pygame.mouse.get_pos()
        
        # Рисуем рамки для фонов
        frame_color = (100, 100, 100)
        
        # Рамка 1 (слева сверху)
        pygame.draw.rect(screen, frame_color, bg1_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), bg1_frame, width=2, border_radius=10)
        if bg1_frame.collidepoint(mouse_pos) or selected_bg_1 == "bg_1":
            pygame.draw.rect(screen, (255, 255, 0), bg1_frame, width=4, border_radius=10)  # Желтая подсветка
        # Картинка по центру рамки
        screen.blit(bg1, (bg1_frame.x + (bg1_frame.width - 200) // 2, bg1_frame.y + (bg1_frame.height - 100) // 2))
        
        # Рамка 2 (слева снизу)
        pygame.draw.rect(screen, frame_color, bg2_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), bg2_frame, width=2, border_radius=10)
        if bg2_frame.collidepoint(mouse_pos) or selected_bg_1 == "bg_2":
            pygame.draw.rect(screen, (255, 255, 0), bg2_frame, width=4, border_radius=10)  # Желтая подсветка
        screen.blit(bg2, (bg2_frame.x + (bg2_frame.width - 200) // 2, bg2_frame.y + (bg2_frame.height - 100) // 2))
        
        # Рамка 3 (справа сверху)
        pygame.draw.rect(screen, frame_color, bg3_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), bg3_frame, width=2, border_radius=10)
        if bg3_frame.collidepoint(mouse_pos) or selected_bg_1 == "bg_3":
            pygame.draw.rect(screen, (255, 255, 0), bg3_frame, width=4, border_radius=10)  # Желтая подсветка
        screen.blit(bg3, (bg3_frame.x + (bg3_frame.width - 200) // 2, bg3_frame.y + (bg3_frame.height - 100) // 2))
        
        # Рамка 4 (справа снизу)
        pygame.draw.rect(screen, frame_color, bg4_frame, border_radius=10)
        pygame.draw.rect(screen, (120, 120, 120), bg4_frame, width=2, border_radius=10)
        if bg4_frame.collidepoint(mouse_pos) or selected_bg_1 == "bg_4":
            pygame.draw.rect(screen, (255, 255, 0), bg4_frame, width=4, border_radius=10)  # Желтая подсветка
        screen.blit(bg4, (bg4_frame.x + (bg4_frame.width - 200) // 2, bg4_frame.y + (bg4_frame.height - 100) // 2))
        
        # Кнопка применения (опущена ниже)
        apply_bg_btn.update()
        apply_bg_btn.draw(screen)

    elif scen == SCENMUSIC:
        pygame.draw.rect(screen, (50, 50, 50), frame_mizic, border_radius=10)
        
        # Обновляем текст кнопки в зависимости от состояния музыки
        if music_playing:
            music_btn_stop.text = font.render("Pause Music", True, (255, 255, 255))
            music_btn_stop.color_idle = (255, 0, 0)
            music_btn_stop.color_hover = (200, 0, 0)
        else:
            music_btn_stop.text = font.render("Play Music", True, (255, 255, 255))
            music_btn_stop.color_idle = (0, 255, 0)
            music_btn_stop.color_hover = (0, 200, 0)
        music_btn_stop.text_rect = music_btn_stop.text.get_rect(center=music_btn_stop.rect.center)
        
        exit_mizic.update()
        exit_mizic.draw(screen)
        music_btn_stop.update()
        music_btn_stop.draw(screen)

    pygame.display.update()
    clock.tick(60)

if start_game_flag:
    client.start_game()

# Останавливаем музыку при выходе
bg_sound.stop()
pygame.quit()