import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600

# Configurações do jogo
game_state = "menu"

# Menu
button_start = Rect((WIDTH//2-100, 200), (200, 50))
button_sound = Rect((WIDTH//2-100, 300), (200, 50))
button_quit = Rect((WIDTH//2-100, 400), (200, 50))

sound_enabled = True

# Player
player = Actor("player_idle", (100, 500))
player.vx = 0
player.vy = 0
player.on_ground = False
player.facing = "right"

# Animação
player.walk_images = ["player_walk1", "player_walk2"]
player.walk_index = 0
player.animation_timer = 0

# Física
GRAVITY = 0.5
JUMP_STRENGTH = -12
WALK_SPEED = 4

# Câmera
camera_x = 0
MAP_WIDTH = 3000

# Música
music.set_volume(0.3)
if sound_enabled:
    music.play("background")

def update_camera():
    global camera_x
    target_x = player.x - WIDTH//2
    camera_x = max(0, min(target_x, MAP_WIDTH - WIDTH))

def draw():
    screen.clear()
    
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()

def draw_menu():
    screen.draw.text("Platformer Game", center=(WIDTH//2, 100), fontsize=50, color="white")
    screen.draw.filled_rect(button_start, "dodgerblue")
    screen.draw.text("Start Game", center=button_start.center, color="white")
    screen.draw.filled_rect(button_sound, "green" if sound_enabled else "red")
    screen.draw.text("Sound: ON" if sound_enabled else "Sound: OFF", center=button_sound.center, color="white")
    screen.draw.filled_rect(button_quit, "gray")
    screen.draw.text("Exit", center=button_quit.center, color="white")

def draw_game():
    # Fundo
    screen.fill((70, 70, 120))
    
    # Desenhar jogador
    draw_x = player.x - camera_x
    draw_y = player.y
    player.pos = (draw_x, draw_y)  # Posição temporária para desenho
    player.draw()
    player.pos = (player.x, player.y)  # Restaura posição real

def update(dt):
    global game_state
    
    if game_state == "game":
        update_player()
        update_camera()

def update_player():
    # Movimento horizontal
    player.vx = 0
    if keyboard.left or keyboard.a:
        player.vx = -WALK_SPEED
        player.facing = "left"
    elif keyboard.right or keyboard.d:
        player.vx = WALK_SPEED
        player.facing = "right"
    
    player.x += player.vx
    
    # Gravidade
    player.vy += GRAVITY
    player.y += player.vy
    
    # Limites do mapa
    player.x = max(10, min(player.x, MAP_WIDTH - 10))

    # Verifica se está no chão (alcançou o limite inferior da tela)
    if player.y >= HEIGHT - 60:  # valor ajustado para o sprite
        player.y = HEIGHT - 60
        player.vy = 0
        player.on_ground = True
    else:
        player.on_ground = False

    # Atualizar animação
    update_animation()

def update_animation():
    if not player.on_ground:
        player.image = "player_jump" if player.vy < 0 else "player_fall"
    else:
        if abs(player.vx) > 0.5:
            player.animation_timer += 1
            if player.animation_timer >= 8:
                player.animation_timer = 0
                player.walk_index = (player.walk_index + 1) % len(player.walk_images)
                player.image = player.walk_images[player.walk_index]
        else:
            player.image = "player_idle"
    
    # Orientação
    player._flip_x = (player.facing == "left")

def on_mouse_down(pos):
    global game_state, sound_enabled
    
    if game_state == "menu":
        if button_start.collidepoint(pos):
            game_state = "game"
        elif button_sound.collidepoint(pos):
            sound_enabled = not sound_enabled
            if sound_enabled:
                music.play("background")
            else:
                music.stop()
        elif button_quit.collidepoint(pos):
            exit()

def on_key_down(key):
    if game_state == "game":
        if (key == keys.SPACE or key == keys.UP or key == keys.W) and player.on_ground:
            player.vy = JUMP_STRENGTH
            player.on_ground = False
            if sound_enabled:
                sounds.jump.play()

pgzrun.go()
