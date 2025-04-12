import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Jogo Platformer"
MAP_WIDTH = 4000

game_state = "menu"
camera_x = 0
music_on = True

MAX_LIFE = 3
life = MAX_LIFE


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


enemy = Actor("zombie/zombie_idle", (1820, HEIGHT - 110))
enemy.direction = 1
enemy.speed = 1
enemy.range = 200
enemy.start_x = enemy.x
enemy.walk_frames = ["zombie/zombie_walk1", "zombie/zombie_walk2"]
enemy.walk_index = 0
enemy.timer = 0
enemy.flip_x = enemy.direction < 0

spider = Actor("spider/spider", (1100, HEIGHT - 77))
spider.direction = 1
spider.speed = 1
spider.range = 200
spider.start_x = spider.x
spider.walk_frames = ["spider/spider_walk1", "spider/spider_walk2"]
spider.walk_index = 0
spider.time = 0
spider.flip_x = spider.direction < 0


END_OF_MAPA_X = MAP_WIDTH - 110
END_OF_MAPA_Y = HEIGHT - 50 - 16 

flag = Actor("items/flag_win")
flag.pos = (END_OF_MAPA_X, END_OF_MAPA_Y)


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


spikes = [
    Actor("items/thorns_plat", (3550 + 60, HEIGHT - 310 - 20)),
    Actor("items/thorns_plat", (700 + 75, HEIGHT - 300 - 20)),
    Actor("items/thorns_plat", (1300 + 100, HEIGHT - 250 - 20)),
    Actor("items/thorns_plat", (3050 + 75, HEIGHT - 170 - 20)),
]


keys = [
    Actor("items/key_plat", (250, HEIGHT - 170)),
    Actor("items/key_plat", (420, HEIGHT - 240)),
    Actor("items/key_plat", (720, HEIGHT - 320)),
    Actor("items/key_plat", (920, HEIGHT - 390)),
    Actor("items/key_plat", (1320, HEIGHT - 270)),
    Actor("items/key_plat", (1820, HEIGHT - 90)),
    Actor("items/key_plat", (2320, HEIGHT - 200)),
    Actor("items/key_plat", (2850, HEIGHT - 120)),
    Actor("items/key_plat", (1100, HEIGHT - 100))
]
for key in keys:
    key.width *= 1.5
    key.height *= 1.5
    key.collected = False

collected_keys = 0
TOTAL_KEYS = len(keys)


buttons = {
    "start": Rect((WIDTH//2 - 100, 200), (200, 50)),
    "music": Rect((WIDTH//2 - 100, 270), (200, 50)),
    "exit": Rect((WIDTH//2 - 100, 340), (200, 50))
}

def update_camera():
    global camera_x
    camera_x = max(0, min(player.x - WIDTH // 2, MAP_WIDTH - WIDTH))

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
            screen.draw.filled_rect(Rect((plat.x - camera_x, plat.y), plat.size), "brown")

        
        original_flag_x = flag.x
        flag.x -= camera_x
        flag.draw()
        flag.x = original_flag_x

        original_spider_x = spider.x
        spider.x -= camera_x
        spider.draw()
        spider.x = original_spider_x



        original_enemy_x = enemy.x
        enemy.x -= camera_x
        enemy.draw()
        enemy.x = original_enemy_x

        for spike in spikes:
            original_x = spike.x
            spike.x -= camera_x
            spike.draw()
            spike.x = original_x

        for key in keys:
            if not key.collected:
                original_x = key.x
                key.x -= camera_x
                key.draw()
                key.x = original_x

        screen.blit(player.image, (player.x - player.width / 2 - camera_x, player.y - player.height / 2))
        screen.draw.text(f"Chaves: {collected_keys}/{TOTAL_KEYS}", topleft=(10, 10), fontsize=30, color="white")

        for i in range(life):
            screen.blit("items/heart", (10 + 40 * i, 50))


def update():
    global collected_keys, game_state, life
    if game_state != "game":
        return

    if keyboard.left or keyboard.a:
        player.vx = -5
        player.facing = "left"
    elif keyboard.right or keyboard.d:
        player.vx = 5
        player.facing = "right"
    else:
        player.vx = 0

    if (keyboard.up or keyboard.w or keyboard.space) and player.on_ground:
        player.vy = -15
        player.on_ground = False
        if hasattr(sounds, "jump"): sounds.jump.play()

    player.vy += 0.5
    player.x += player.vx
    player.y += player.vy
    player.x = max(player.width/2, min(player.x, MAP_WIDTH - player.width/2))

    if player.y > HEIGHT - 50 - player.height / 2:
        player.y = HEIGHT - 50 - player.height / 2
        player.vy = 0
        player.on_ground = True

    player_rect = Rect((player.x - player.width / 2, player.y - player.height / 2), (player.width, player.height))

    for plat in platforms:
        if player_rect.colliderect(plat) and player.vy > 0:
            if player_rect.bottom - player.vy <= plat.top:
                player.y = plat.top - player.height / 2
                player.vy = 0
                player.on_ground = True

    for spike in spikes:
        spike_rect = Rect(spike.x - 20, spike.y, 40, 20)
        if player_rect.colliderect(spike_rect):
            if hasattr(sounds, "hit"): sounds.hit.play()
            lose_life()
            return

    spider_rect = Rect(spider.x - 20, spider.y - 20, 40, 40)
    if player_rect.colliderect(spider_rect):
        if hasattr(sounds, "hit"): sounds.hit.play()
        lose_life()
        return



    enemy_rect = Rect(enemy.x - 20, enemy.y - 40, 40, 80)
    if player_rect.colliderect(enemy_rect):
        if hasattr(sounds, "hit"): sounds.hit.play()
        lose_life()
        return

    for key in keys:
        if not key.collected:
            key_rect = Rect((key.x - 10, key.y - 10), (20, 20))
            if player_rect.colliderect(key_rect):
                key.collected = True
                collected_keys += 1
                if hasattr(sounds, "coin"): sounds.coin.play()

        flag_rect = Rect((flag.x - flag.width / 2, flag.y - flag.height / 2), (flag.width, flag.height))
        if player_rect.colliderect(flag_rect):
            if collected_keys == TOTAL_KEYS:
                
                if hasattr(sounds, "win"): sounds.win.play()
                game_state = "menu"
                reset_game()


    update_animation()
    update_enemy()
    update_spider()
    update_camera()

def update_enemy():
    enemy.x += enemy.direction * enemy.speed
    if abs(enemy.x - enemy.start_x) >= enemy.range:
        enemy.direction *= -1
        enemy.flip_x = not enemy.flip_x

    enemy.timer += 1
    if enemy.timer >= 10:
        enemy.timer = 0
        enemy.walk_index = (enemy.walk_index + 1) % len(enemy.walk_frames)
        enemy.image = enemy.walk_frames[enemy.walk_index]
    enemy._flip_x = enemy.flip_x

def update_spider():
    spider.x += spider.direction * spider.speed
    if abs(spider.x - spider.start_x) >= spider.range:
        spider.direction *= -1
        spider.flip_x = not spider.flip_x

    spider.time += 1
    if spider.time >= 10:
        spider.time = 0
        spider.walk_index = (spider.walk_index + 1) % len(spider.walk_frames)
        spider.image = spider.walk_frames[spider.walk_index]
    spider._flip_x = spider.flip_x


    spider.time += 1
    if spider.time >= 10:
        spider.time = 0
        spider.walk_index = (spider.walk_index + 1) % len(spider.walk_frames)
        spider.image = spider.walk_frames[spider.walk_index]
    spider._flip_x = spider.flip_x



def reset_player_position():
    player.x = 100
    player.y = HEIGHT - 100
    player.vx = 0
    player.vy = 0
    player.on_ground = True

def reset_game():
    global collected_keys, life
    life = MAX_LIFE
    collected_keys = 0
    for key in keys:
        key.collected = False
    reset_player_position()

def lose_life():
    global life, game_state
    life -= 1
    if life <= 0:
        game_state = "menu"
        reset_game()
    else:
        reset_player_position()

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
            reset_game()
            player.image = "player/player_idle"
        elif buttons["music"].collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play("background")
                music.set_volume(0.3)
            else:
                music.stop()
        elif buttons["exit"].collidepoint(pos):
            exit()

def on_start():
    if music_on:
        music.play("background")
        music.set_volume(0.2)

    if hasattr(sounds, "coin"):
        sounds.coin.set_volume(0.2)
    if hasattr(sounds, "jump"):
        sounds.jump.set_volume(0.2)
    if hasattr(sounds, "hit"):
        sounds.hit.set_volume(0.2)
    if hasattr(sounds, "win"):
        sounds.win.set_volume(0.4)

on_start()
pgzrun.go()