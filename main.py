import pgzrun

# Configurações da janela
WIDTH = 1200
HEIGHT = 800

# Configurações do jogo
game_state = "menu"

# Menu
button_start = Rect((WIDTH // 2 - 100, 300), (200, 50))
button_sound = Rect((WIDTH // 2 - 100, 400), (200, 50))
button_quit = Rect((WIDTH // 2 - 100, 500), (200, 50)) 

sound_enabled = True

# Player
player = Actor("player_idle", (100, HEIGHT - 100)) 
player.vx = 0
player.vy = 0
player.on_ground = True
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
MAP_WIDTH = 10000
GROUND_HEIGHT = HEIGHT - 50

# Plataformas
platforms = [
    Rect((300, GROUND_HEIGHT - 100), (200, 20)),
    Rect((600, GROUND_HEIGHT - 150), (150, 20)),
    Rect((1000, GROUND_HEIGHT - 200), (250, 20)),
]

# Música
music.set_volume(0.2)
if sound_enabled:
    music.play("background")

def update_camera():
    global camera_x
    target_x = player.x - WIDTH // 2
    camera_x = max(0, min(target_x, MAP_WIDTH - WIDTH))

def draw():
    screen.clear()
    
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()

def draw_menu():
    screen.draw.text("Platformer Game", center=(WIDTH // 2, 150), fontsize=70, color="white")
    screen.draw.filled_rect(button_start, "dodgerblue")
    screen.draw.text("Start Game", center=button_start.center, color="white")
    screen.draw.filled_rect(button_sound, "green" if sound_enabled else "red")
    screen.draw.text("Sound: ON" if sound_enabled else "Sound: OFF", center=button_sound.center, color="white")
    screen.draw.filled_rect(button_quit, "gray")
    screen.draw.text("Exit", center=button_quit.center, color="white")

def draw_game():
    screen.fill((70, 70, 120))

    # Desenhar chão
    screen.draw.filled_rect(Rect((0 - camera_x, GROUND_HEIGHT), (MAP_WIDTH, HEIGHT - GROUND_HEIGHT)), "green")
    
    # Desenhar plataformas
    for plat in platforms:
        draw_rect = Rect((plat.x - camera_x, plat.y), plat.size)
        screen.draw.filled_rect(draw_rect, "brown")
    
    # Desenhar jogador
    draw_x = player.x - camera_x
    draw_y = player.y
    player.pos = (draw_x, draw_y)
    player.draw()
    player.pos = (player.x, player.y)

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
    player.x = max(10, min(player.x, MAP_WIDTH - 10))
    
    # Gravidade
    player.vy += GRAVITY
    player.y += player.vy
    player.on_ground = False

    # Verificar colisão com o chão
    if player.y >= GROUND_HEIGHT - 30:
        player.y = GROUND_HEIGHT - 30
        player.vy = 0
        player.on_ground = True

    # Verificar colisão com plataformas
    player_rect = Rect((player.x - player.width // 2, player.y - player.height // 2), (player.width, player.height))

    for plat in platforms:
        if player_rect.colliderect(plat):
            # Colisão por cima
            if player.vy > 0 and player_rect.bottom - player.vy < plat.top + 5:
                player.y = plat.top - 60
                player.vy = 0
                player.on_ground = True
            # Colisão por baixo
            elif player.vy < 0 and player_rect.top - player.vy > plat.bottom - 5:
                player.y = plat.bottom
                player.vy = 0
            # Colisão lateral esquerda
            elif player.vx > 0 and player_rect.right - player.vx < plat.left + 5:
                player.x = plat.left - 15
            # Colisão lateral direita
            elif player.vx < 0 and player_rect.left - player.vx > plat.right - 5:
                player.x = plat.right + 15

    # Animação
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
    
    player._flip_x = (player.facing == "left")

def on_mouse_down(pos):
    global game_state, sound_enabled
    if game_state == "menu":
        if button_start.collidepoint(pos):
            game_state = "game"
            player.x = 100
            player.y = GROUND_HEIGHT - 30
            player.vx = 0
            player.vy = 0
            player.on_ground = True
        elif button_sound.collidepoint(pos):
            sound_enabled = not sound_enabled
            if sound_enabled:
                music.play("background")
            else:
                music.stop()
        elif button_quit.collidepoint(pos):
            quit()

def on_key_down(key):
    if game_state == "game":
        if (key == keys.SPACE or key == keys.UP or key == keys.W) and player.on_ground:
            player.vy = JUMP_STRENGTH
            player.on_ground = False
            if sound_enabled:
                sounds.jump.play()

pgzrun.go()