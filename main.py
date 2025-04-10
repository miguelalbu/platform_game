import pgzrun

# Configurações básicas
WIDTH = 800
HEIGHT = 600
TITLE = "Jogo Platfomer"
MAP_WIDTH = 3000

# Estado do jogo
game_state = "menu"
camera_x = 0
music_on = True  # Estado da música

# Jogador
player = Actor("player_idle", (100, HEIGHT - 100))
player.vx = 0
player.vy = 0
player.on_ground = True
player.facing = "right"
player.walk_frames = ["player_walk1", "player_walk2"]
player.walk_index = 0
player.animation_timer = 0

# Plataformas
platforms = [
    Rect((300, HEIGHT - 150), (200, 20)),
    Rect((700, HEIGHT - 200), (200, 20)),
    Rect((1200, HEIGHT - 250), (200, 20)),
    Rect((1800, HEIGHT - 300), (200, 20)),
    Rect((2500, HEIGHT - 200), (200, 20))
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
            label = "Música: ON" if name == "music" and music_on else "Música: OFF" if name == "music" else name.capitalize()
            screen.draw.text(label, center=rect.center, fontsize=32, color="black")
    
    elif game_state == "game":
        screen.fill((50, 50, 80))
        screen.draw.filled_rect(Rect((0 - camera_x, HEIGHT - 50), (MAP_WIDTH, 50)), "green")
        
        for plat in platforms:
            screen.draw.filled_rect(Rect((plat.x - camera_x, plat.y), plat.size), "brown")
        
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
            sounds.jump.play()  # Toca som de pulo
            
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
        
        update_animation()
        update_camera()

def update_animation():
    if player.on_ground:
        if abs(player.vx) > 0.5:
            player.animation_timer += 1
            if player.animation_timer >= 10:
                player.animation_timer = 0
                player.walk_index = (player.walk_index + 1) % len(player.walk_frames)
                player.image = player.walk_frames[player.walk_index]
        else:
            player.image = "player_idle"
    else:
        player.image = "player_jump" if player.vy < 0 else "player_fall"
    
    player._flip_x = (player.facing == "left")

def on_mouse_down(pos):
    global game_state, music_on
    
    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            game_state = "game"
            player.x = 100
            player.y = HEIGHT - 100
            player.vx = 0
            player.vy = 0
            player.on_ground = True
            player.facing = "right"
            player.image = "player_idle"
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

# Toca música de fundo assim que o jogo iniciar, se estiver ligada
def on_start():
    if music_on:
        music.play("background")
        music.set_volume(0.3)

on_start()
pgzrun.go()
