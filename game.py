import pgzrun
import math
from pgzero.actor import Actor
from pygame import Rect

# ----- CONSTANTES BÁSICAS -----

TILE_SIZE = 64

# ----- TILE MAP -----

CAVE_MAP = [
    "############",
    "#....##....#",
    "#..#....#..#",
    "####....#..#",
    "#....##....#",
    "#..######..#",
    "#..........#",
    "############",
]

WIDTH = len(CAVE_MAP[0]) * TILE_SIZE
HEIGHT = len(CAVE_MAP) * TILE_SIZE

TITLE_SIZE = 64

tile_actors = []
decor_actors = []


def tile_center(col, row):
    return (
        col * TILE_SIZE + TILE_SIZE / 2,
        row * TILE_SIZE + TILE_SIZE / 2,
    )


def create_map():
    global tile_actors, decor_actors
    tile_actors = []
    decor_actors = []

    for row, line in enumerate(CAVE_MAP):
        for col, char in enumerate(line):
            x, y = tile_center(col, row)

            if char == "#":
                wall = Actor("wall_stone_1", (x, y))
                tile_actors.append(wall)
            elif char == ".":
                floor = Actor("floor_stone_1", (x, y))
                decor_actors.append(floor)


# ----- ESTADOS DO JOGO -----

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

game_state = STATE_MENU
music_enabled = True


# ----- CONTROLE DE MÚSICA E SONS -----

def play_music():
    if music_enabled:
        music.play("background_music")
        music.set_volume(0.4)


play_music()


# ----- CLASSE BUTTON -----

class Button:
    def __init__(self, text, center, width=200, height=60):
        self.text = text
        self.rect = Rect(0, 0, width, height)
        self.rect.center = center

    def draw(self):
        screen.draw.filled_rect(self.rect, "darkblue")
        screen.draw.rect(self.rect, "white")
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=32,
            color="white",
        )

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


# ----- CLASSE HERO  -----

class Hero:
    def __init__(self, x, y):
        start_x = round(x / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
        start_y = round(y / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2

        self.actor = Actor("hero_idle_1")
        self.actor.pos = (start_x, start_y)

        self.speed = 200

        # animação
        self.idle_frames = ["hero_idle_1", "hero_idle_2"]
        self.walk_frames = ["hero_walk_1", "hero_walk_2", "hero_walk_3"]
        self.current_frame = self.idle_frames
        self.frame_index = 0
        self.animation_timer = 0.0
        self.animation_duration = 0.15

        # movimento
        self.is_moving = False
        self.target_x = self.actor.x
        self.target_y = self.actor.y

    def can_move_to(self, new_x, new_y):
        col = int(new_x // TILE_SIZE)
        row = int(new_y // TILE_SIZE)

        if 0 <= row < len(CAVE_MAP) and 0 <= col < len(CAVE_MAP[row]):
            return CAVE_MAP[row][col] == "."
        return False

    def update(self, dt):
        if self.is_moving:
            dx = self.target_x - self.actor.x
            dy = self.target_y - self.actor.y
            distance = math.hypot(dx, dy)

            step = self.speed * dt

            if distance <= step:
                self.actor.x = self.target_x
                self.actor.y = self.target_y
                self.is_moving = False
            else:
                self.actor.x += dx / distance * step
                self.actor.y += dy / distance * step

        else:
            dx_cells = 0
            dy_cells = 0

            if keyboard.left:
                dx_cells = -1
            elif keyboard.right:
                dx_cells = 1

            if keyboard.up:
                dy_cells = -1
            elif keyboard.down:
                dy_cells = 1

            if dx_cells != 0 or dy_cells != 0:
                new_x = self.actor.x + dx_cells * TILE_SIZE
                new_y = self.actor.y + dy_cells * TILE_SIZE

                min_x = TILE_SIZE / 2
                max_x = WIDTH - TILE_SIZE / 2
                min_y = TILE_SIZE / 2
                max_y = HEIGHT - TILE_SIZE / 2

                new_x = max(min_x, min(max_x, new_x))
                new_y = max(min_y, min(max_y, new_y))

                if self.can_move_to(new_x, new_y):
                    self.target_x = new_x
                    self.target_y = new_y
                    self.is_moving = True

        if self.is_moving:
            self.current_frame = self.walk_frames
        else:
            self.current_frame = self.idle_frames

        # Atualizar animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_duration:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frame)
            self.actor.image = self.current_frame[self.frame_index]

    def draw(self):
        self.actor.draw()

    @property
    def rect(self):
        return Rect(self.actor.x - 16, self.actor.y - 16, 32, 32)


# ----- CLASSE ENEMY -----

class Enemy:
    def __init__(self, x, y, speed=1):
        self.actor = Actor("slime_idle_1")
        self.actor.pos = (x, y)
        self.speed = speed
        self.direction = 1

        self.idle_frames = ["slime_idle_1", "slime_idle_2"]
        self.walk_frames = ["slime_walk_1", "slime_walk_2"]
        self.current_frame = self.idle_frames
        self.frame_index = 0
        self.frame_time = 0.0
        self.frame_duration = 0.2

    def can_move_to(self, new_x, new_y):
        col = int(new_x // TILE_SIZE)
        row = int(new_y // TILE_SIZE)
        if 0 <= row < len(CAVE_MAP) and 0 <= col < len(CAVE_MAP[row]):
            return CAVE_MAP[row][col] == "."
        return False

    def update(self, dt):
        dx = self.speed * self.direction
        new_x = self.actor.x + dx

        if not self.can_move_to(new_x, self.actor.y):
            self.direction *= -1
        else:
            self.actor.x = new_x

        # animação
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frame)
            self.actor.image = self.current_frame[self.frame_index]

    @property
    def rect(self):
        return Rect(self.actor.x - 16, self.actor.y - 16, 32, 32)

    def draw(self):
        self.actor.draw()


hero = Hero(*tile_center(1, 6))

enemies = [
    Enemy(*tile_center(5, 2), speed=1.0),
    Enemy(*tile_center(9, 3), speed=1.5),
    Enemy(*tile_center(3, 5), speed=0.8),
    Enemy(*tile_center(7, 6), speed=1.2),
]

treasure = Actor("treasure")
treasure.pos = tile_center(1, 1)

exit_door = Actor("exit")
exit_door.pos = tile_center(10, 6)

create_map()

play_button = Button("Play", (WIDTH // 2, 250))
music_button = Button("Music: ON", (WIDTH // 2, 340))
exit_button = Button("Exit", (WIDTH // 2, 430))

buttons = [play_button, music_button, exit_button]


def draw():
    screen.clear()

    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_PLAYING:
        draw_game()
    elif game_state == STATE_GAME_OVER:
        draw_game_over()
    elif game_state == STATE_VICTORY:
        draw_victory()


def update(dt):
    if game_state == STATE_PLAYING:
        update_game(dt)


def draw_menu():
    screen.fill((20, 20, 40))
    screen.draw.text(
        "Dungeon Slimes",
        center=(WIDTH // 2, 120),
        fontsize=TITLE_SIZE,
        color="white",
    )

    for button in buttons:
        button.draw()


def draw_game():
    screen.fill((100, 100, 100))

    for tile in tile_actors:
        tile.draw()

    for decor in decor_actors:
        decor.draw()

    treasure.draw()
    exit_door.draw()
    hero.draw()
    for enemy in enemies:
        enemy.draw()


def draw_game_over():
    screen.fill((15, 0, 0))

    for tile in tile_actors:
        tile.draw()
    for decor in decor_actors:
        decor.draw()
    exit_door.draw()
    treasure.draw()
    hero.draw()

    panel_width = 520
    panel_height = 220
    panel_rect = Rect(
        WIDTH // 2 - panel_width // 2,
        HEIGHT // 2 - panel_height // 2,
        panel_width,
        panel_height,
    )

    screen.draw.filled_rect(panel_rect, (0, 0, 0))
    screen.draw.rect(panel_rect, (200, 0, 0))

    screen.draw.text(
        "GAME OVER",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=60,
        color="red",
    )

    screen.draw.text(
        "Você foi atingido pelos slimes!",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize=32,
        color="white",
    )

    screen.draw.text(
        "Pressione ENTER para voltar ao menu",
        center=(WIDTH // 2, HEIGHT // 2 + 50),
        fontsize=26,
        color="red",
    )


def draw_victory():
    screen.fill((10, 10, 20))

    for tile in tile_actors:
        tile.draw()
    for decor in decor_actors:
        decor.draw()
    exit_door.draw()
    treasure.draw()
    hero.draw()

    panel_width = 520
    panel_height = 240
    panel_rect = Rect(
        WIDTH // 2 - panel_width // 2,
        HEIGHT // 2 - panel_height // 2,
        panel_width,
        panel_height,
    )

    screen.draw.filled_rect(panel_rect, (0, 0, 0))
    screen.draw.rect(panel_rect, "yellow")

    screen.draw.text(
        "VOCÊ VENCEU!",
        center=(WIDTH // 2, HEIGHT // 2 - 60),
        fontsize=60,
        color="yellow",
    )

    screen.draw.text(
        "Tesouro encontrado e resgatado!",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize=32,
        color="white",
    )

    screen.draw.text(
        "Pressione ENTER para voltar ao menu",
        center=(WIDTH // 2, HEIGHT // 2 + 60),
        fontsize=26,
        color="yellow",
    )


def update_game(dt):
    global game_state

    hero.update(dt)
    for enemy in enemies:
        enemy.update(dt)

    for enemy in enemies:
        if hero.rect.colliderect(enemy.rect):
            if music_enabled:
                sounds.slime_hit.play()
            game_state = STATE_GAME_OVER

    treasure_rect = Rect(treasure.x - 16, treasure.y - 16, 32, 32)
    exit_rect = Rect(exit_door.x - 16, exit_door.y - 16, 32, 32)

    if hero.rect.colliderect(treasure_rect):
        if music_enabled:
            sounds.treasure_pickup.play()
        treasure.pos = (-100, -100)

    if treasure.pos == (-100, -100) and hero.rect.colliderect(exit_rect):
        if music_enabled:
            sounds.victory.set_volume(0.3)
            sounds.victory.play()
        game_state = STATE_VICTORY


# ----- ENTRADA DO MOUSE / TECLADO -----

def on_mouse_down(pos):
    global game_state, music_enabled

    if game_state == STATE_MENU:
        if play_button.is_hovered(pos):
            reset_game()
            game_state = STATE_PLAYING
        elif music_button.is_hovered(pos):
            music_enabled = not music_enabled
            music_button.text = "Music: ON" if music_enabled else "Music: OFF"

            if music_enabled:
                play_music()
            else:
                music.stop()
        elif exit_button.is_hovered(pos):
            quit()


def on_key_down(key):
    global game_state
    if (game_state == STATE_GAME_OVER or game_state == STATE_VICTORY) and key == keys.RETURN:
        reset_game()


def reset_game():
    global game_state, hero, enemies, treasure, exit_door

    hero = Hero(*tile_center(1, 6))

    enemies = [
        Enemy(*tile_center(5, 2), speed=1.0),
        Enemy(*tile_center(9, 3), speed=1.5),
        Enemy(*tile_center(1, 5), speed=0.8),
        Enemy(*tile_center(7, 6), speed=1.2),
    ]

    treasure.pos = tile_center(1, 1)
    exit_door.pos = tile_center(10, 6)

    create_map()
    game_state = STATE_MENU


pgzrun.go()
