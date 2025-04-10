import pgzrun
from pygame import Rect

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
    Rect((3050, HEIGHT - 170), (150, 20)),  # Nova plataforma difícil
    Rect((3300, HEIGHT - 240), (120, 20)),
    Rect((3550, HEIGHT - 310), (120, 20)),  # Com espinho
]

# Espinhos (relacionados às plataformas de dificuldade)
spikes = [
    Actor("items/thorns_plat", (3550 + 60, HEIGHT - 310 - 20)),  # Centralizado sobre a plataforma
]

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

        for plat in platforms:
            plat_color = "red" if plat in [platforms[-1]] else "brown"
            screen.draw.filled_rect(Rect((plat.x - camera_x, plat.y), plat.size), plat_color)

        for spike in spikes:
            original_x = spike.x
            spike.x -= camera_x
            spike.draw()
            spike.x = original_x

        screen.blit(player.image, (player.x - player.width/2 - camera_x, player.y - player.height/2))

def update():
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
                sounds.hit.play()
                reset_player()

        update_animation()
        update_camera()

def reset_player():
    player.x = 100
    player.y = HEIGHT - 100
    player.vx = 0
    player.vy = 0
    player.on_ground = True

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
