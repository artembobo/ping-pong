

from pygame import *
import socket
import json
from threading import Thread

game_over = False
winner = None
you_winner = None
game_state = {}
buffer = ""

def start_game():
    global game_state, buffer
    
    mixer.init()

    WIDTH, HEIGHT = 800, 600
    init()
    screen = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()
    display.set_caption("Пінг-Понг")
    with open("data_bg.txt", "r") as f:
        bg_name = f.read().strip()
        print(bg_name)

    with open("data.txt", "r") as f:
        ball_name = f.read().strip()   
        print(ball_name) 

    ball_image = image.load(f"images/ball_{ball_name}.png")
    ball_image = transform.scale(ball_image, (20, 20))
    ball_radius = 10 

    ext = ".png" if bg_name == "bg_3" else ".jpg"
    bg_image = image.load(f"images/{bg_name}{ext}")
    bg_image = transform.scale(bg_image, (WIDTH, HEIGHT))

    # ---СЕРВЕР ---
    def connect_to_server():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8080))
        my_id = int(client.recv(24).decode())
        return my_id, client


    def receive():
        global buffer, game_state, game_over
        while not game_over:
            try:
                data = client.recv(1024).decode()
                buffer += data
                while "\n" in buffer:
                    packet, buffer = buffer.split("\n", 1)
                    if packet.strip():
                        game_state = json.loads(packet)
            except:
                game_state["winner"] = -1
                break

    # --- ШРИФТИ ---
    font_win = font.Font(None, 72)
    game_font = font.Font("font.ttf", 26)
    # --- ЗОБРАЖЕННЯ ----

    # --- ЗВУКИ ---

    hit_wall = mixer.Sound("mizic\pingpongbat.ogg")
    hit_pratfrom = mixer.Sound("mizic\ping_pong_8bit_plop.ogg")
    fon = None

    # --- ГРА ---

    game_over = False
    winner = None
    you_winner = None
    try:
        my_id, client = connect_to_server()
        Thread(target=receive, daemon=True).start()
    except:
        game_state["winner"] = -1
        my_id = None
        client = None
    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()

        screen.blit(bg_image, (0, 0))

        if "countdown" in game_state and game_state["countdown"] > 0:
            screen.fill((0, 0, 0))
            countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
            screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
            display.update()
            continue  # Не малюємо гру до завершення відліку

        if "winner" in game_state and game_state["winner"] is not None:
            screen.blit(bg_image, (0, 0))

            if you_winner is None:  # Встановлюємо тільки один раз
                if game_state["winner"] == my_id:
                    you_winner = True
                else:
                    you_winner = False

            if you_winner:
                text = "Ти переміг!"
            else:
                text = "Пощастить наступним разом!"

            win_text = font_win.render(text, True, (255, 215, 0))
            text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(win_text, text_rect)

            text = font_win.render('К - рестарт', True, (255, 215, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            screen.blit(text, text_rect)

            display.update()
            continue  # Блокує гру після перемоги

        if game_state:
            screen.blit(bg_image, (0, 0))
            draw.rect(screen, (0, 255, 0), (20, game_state['paddles']['0'], 20, 100))
            draw.rect(screen, (255, 0, 255), (WIDTH - 40, game_state['paddles']['1'], 20, 100))
            screen.blit(ball_image, (game_state['ball']['x'] - ball_radius, game_state['ball']['y'] - ball_radius))
            score_text = game_font.render(f"{game_state['scores'][0]} : {game_state['scores'][1]}", True, (255, 255, 255))
            screen.blit(score_text, (WIDTH // 2 -25, 20))

            if game_state['sound_event']:
                if game_state['sound_event'] == 'wall_hit':
                    hit_wall.play()

                if game_state['sound_event'] == 'platform_hit':
                    hit_pratfrom.play()
        else:
            wating_text = game_font.render(f"Waiting for players...", True, (255, 255, 255))
            screen.blit(wating_text, (WIDTH // 2 -120, HEIGHT // 2 - 20))

        display.update()
        clock.tick(60)

        keys = key.get_pressed()
        if keys[K_w] and client:
            client.send(b"UP")
        elif keys[K_s] and client:
            client.send(b"DOWN")

        if "winner" in game_state and game_state["winner"] is not None and keys[K_k]:
            # рестарт
            game_over = False
            winner = None
            you_winner = None
            game_state = {}
            buffer = ""
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('localhost', 8080))
                my_id = int(client.recv(24).decode())
                Thread(target=receive, daemon=True).start()
            except:
                game_state["winner"] = -1
                my_id = None
                client = None
