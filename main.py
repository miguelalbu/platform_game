import pgzrun
from pygame import Rect
import pygame  # Necessário para o transform.scale funcionar

# Configurações
WIDTH = 800
HEIGHT = 600
TITLE = "Jogo Platformer"
MAP_WIDTH = 4000

# Estado do jogo
game_state = "menu"
camera_x = 0
music_on = True

# Jogador
player = Actor("player/player_idle", (100, HEIGHT - 100))
player.vx = 0
player.vy = 0
player.on_ground = True
player.facing = "right"
player.walk_frames = ["player/player_walk1", "player/player_walk2"]
player.walk_index = 0
player.animation_timer = 0
player.idle_frames = ["player/player_idle", "player/player_duck", "player/player_idle", "player/player_stand"]
player.idle_index = 0
player.idle_timer = 0
player.idle_speed = 30

# Inimigo (zumbi) patrulhando perto da chave no chão
enemy = Actor("zombie/zombie_idle", (1820, HEIGHT - 110))
enemy.direction = 1
enemy.speed = 1
enemy.range = 200
enemy.start_x = enemy.x
enemy.walk_frames = ["zombie/zombie_walk1", "zombie/zombie_walk2"]
enemy.walk_index = 0
enemy.timer = 0
enemy.flip_x = enemy.direction < 0

# Plataformas
platforms = [
    Rect((0, HEIGHT - 50), (MAP_WIDTH, 50)),
    Rect((200, HEIGHT - 150), (150, 20)),
    Rect((400, HEIGHT - 220), (150, 20)),
    Rect((700, HEIGHT - 300), (150, 20)),
    Rect((900, HEIGHT - 370), (150, 20)),
    Rect((1300, HEIGHT - 250), (200, 20)),
    Rect((1550, HEIGHT - 320), (150, 20)),
    Rect((1800, HEIGHT - 390), (150, 20)),
    Rect((2050, HEIGHT - 450), (150, 20)),
    Rect((2300, HEIGHT - 180), (120, 20)),
    Rect((2500, HEIGHT - 250), (120, 20)),
    Rect((2700, HEIGHT - 320), (120, 20)),
    Rect((2850, HEIGHT - 100), (100, 20)),
    Rect((3050, HEIGHT - 170), (150, 20)),
    Rect((3300, HEIGHT - 240), (120, 20)),
    Rect((3550, HEIGHT - 310), (120, 20)),
]

# Espinhos
spikes = [
    Actor("items/thorns_plat", (3550 + 60, HEIGHT - 310 - 20)),
    Actor("items/thorns_plat", (700 + 75, HEIGHT - 300 - 20)),
    Actor("items/thorns_plat", (1300 + 100, HEIGHT - 250 - 20)),
    Actor("items/thorns_plat", (3050 + 75, HEIGHT - 170 - 20)),
]

# Chaves colecionáveis
keys = [
    Actor("items/key", (250, HEIGHT - 170)),
    Actor("items/key", (420, HEIGHT - 240)),
    Actor("items/key", (720, HEIGHT - 320)),
    Actor("items/key", (920, HEIGHT - 390)),
    Actor("items/key", (1320, HEIGHT - 270)),
    Actor("items/key", (1820, HEIGHT - 90)),
    Actor("items/key", (2320, HEIGHT - 200)),
    Actor("items/key", (2850, HEIGHT - 120))
]

collected_keys = 0
TOTAL_KEYS = len(keys)

# Botões do menu
buttons = {
    "start": Rect((WIDTH//2 - 100, 200), (200, 50)),
    "music": Rect((WIDTH//2 - 100, 270), (200, 50)),
    "exit": Rect((WIDTH//2 - 100, 340), (200, 50))
}

def update_camera():
    global camera_x
    camera_x = player.x - WIDTH // 2
    camera_x = max(0, min(camera_x, MAP_WIDTH - WIDTH))

def draw():
    screen.clear()

    if game_state == "menu":
        screen.fill((30, 30, 50))
        screen.draw.text("PLATFORMER", center=(WIDTH//2, 100), fontsize=60, color="white")

        for name, rect in buttons.items():
            screen.draw.filled_rect(rect, "orange")
            label = "Music: ON" if name == "music" and music_on else "Music: OFF" if name == "music" else name.capitalize()
            screen.draw.text(label, center=rect.center, fontsize=32, color="black")

    elif game_state == "game":
        screen.fill((50, 50, 80))
        screen.draw.filled_rect(Rect((0 - camera_x, HEIGHT - 50), (MAP_WIDTH, 50)), "green")

        # Inimigo
        original_enemy_x = enemy.x
        enemy.x -= camera_x
        enemy.draw()
        enemy.x = original_enemy_x

        for plat in platforms:
            plat_color = "red" if plat in [platforms[-1]] else "brown"
            screen.draw.filled_rect(Rect((plat.x - camera_x, plat.y), plat.size), plat_color)

        for spike in spikes:
            original_x = spike.x
            spike.x -= camera_x
            spike.draw()
            spike.x = original_x

        for key in keys:
            if not hasattr(key, "collected") or not key.collected:
                original_x = key.x
                original_y = key.y
                key.x -= camera_x

                key_img = key._surf
                scaled_img = pygame.transform.scale(key_img, (int(key.width * 1.8), int(key.height * 1.8)))
                screen.blit(scaled_img, (key.x - scaled_img.get_width() // 2, key.y - scaled_img.get_height() // 2))

                key.x = original_x
                key.y = original_y

        screen.blit(player.image, (player.x - player.width/2 - camera_x, player.y - player.height/2))
        screen.draw.text(f"Chaves: {collected_keys}/{TOTAL_KEYS}", topleft=(10, 10), fontsize=30, color="white")

def update():
    global collected_keys, game_state

    if game_state == "game":
        if keyboard.left:
            player.vx = -5
            player.facing = "left"
        elif keyboard.right:
            player.vx = 5
            player.facing = "right"
        else:
            player.vx = 0

        if keyboard.up and player.on_ground:
            player.vy = -15
            player.on_ground = False
            if hasattr(sounds, "jump"):
                sounds.jump.play()

        player.vy += 0.5
        player.x += player.vx
        player.y += player.vy

        player.x = max(player.width/2, min(player.x, MAP_WIDTH - player.width/2))

        if player.y > HEIGHT - 50 - player.height/2:
            player.y = HEIGHT - 50 - player.height/2
            player.vy = 0
            player.on_ground = True

        player_rect = Rect((player.x - player.width/2, player.y - player.height/2),
                           (player.width, player.height))

        for plat in platforms:
            if player_rect.colliderect(plat) and player.vy > 0:
                if player_rect.bottom - player.vy <= plat.top:
                    player.y = plat.top - player.height/2
                    player.vy = 0
                    player.on_ground = True

        for spike in spikes:
            spike_rect = Rect((spike.x, spike.y), spike.size)
            if player_rect.colliderect(spike_rect):
                if hasattr(sounds, "hit"):
                    sounds.hit.play()
                reset_player()

        for key in keys:
            if not hasattr(key, "collected") or not key.collected:
                key_rect = Rect((key.x - key.width/2, key.y - key.height/2), (key.width, key.height))
                if player_rect.colliderect(key_rect):
                    key.collected = True
                    collected_keys += 1
                    if hasattr(sounds, "coin"):
                        sounds.coin.play()

        if collected_keys == TOTAL_KEYS and player.x >= MAP_WIDTH - 100:
            print("Parabéns! Você coletou todas as chaves e finalizou o jogo!")
            game_state = "menu"

        update_animation()
        update_enemy()
        update_camera()

def update_enemy():
    # Movimento do inimigo
    enemy.x += enemy.direction * enemy.speed

    # Verifica se ultrapassou o limite de patrulha
    if abs(enemy.x - enemy.start_x) >= enemy.range:
        enemy.direction *= -1  # Inverte direção
        enemy.flip_x = not enemy.flip_x  # Vira o sprite visualmente

    # Animação do inimigo
    enemy.timer += 1
    if enemy.timer >= 10:
        enemy.timer = 0
        enemy.walk_index = (enemy.walk_index + 1) % len(enemy.walk_frames)
        enemy.image = enemy.walk_frames[enemy.walk_index]

    enemy._flip_x = enemy.flip_x  # Aplica a virada visual


def reset_player():
    global collected_keys
    player.x = 100
    player.y = HEIGHT - 100
    player.vx = 0
    player.vy = 0
    player.on_ground = True
    collected_keys = 0
    for key in keys:
        key.collected = False

def update_animation():
    if player.on_ground:
        if abs(player.vx) > 0.5:
            player.animation_timer += 1
            if player.animation_timer >= 10:
                player.animation_timer = 0
                player.walk_index = (player.walk_index + 1) % len(player.walk_frames)
                player.image = player.walk_frames[player.walk_index]
        else:
            player.idle_timer += 1
            if player.idle_timer >= player.idle_speed:
                player.idle_timer = 0
                player.idle_index = (player.idle_index + 1) % len(player.idle_frames)
                player.image = player.idle_frames[player.idle_index]
    else:
        player.image = "player/player_jump" if player.vy < 0 else "player/player_fall"

    player._flip_x = (player.facing == "left")

def on_mouse_down(pos):
    global game_state, music_on

    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            game_state = "game"
            reset_player()
            player.image = "player/player_idle"
        elif buttons["music"].collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play("background")
                music.set_volume(0.3)
            else:
                music.stop()
        elif buttons["exit"].collidepoint(pos):
            print("Saindo do jogo...")
            exit()

def on_start():
    if music_on:
        music.play("background")
        music.set_volume(0.3)

on_start()
pgzrun.go()
