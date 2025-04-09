import pgzrun

WIDTH = 800
HEIGHT = 600

def draw():
    screen.clear()
    screen.draw.text("Hello, Pygame Zero!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="white")

def update():  # ← Keeps the game running
    pass

pgzrun.go()