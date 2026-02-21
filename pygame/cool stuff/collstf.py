import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Arcade")

BLACK = (8, 8, 15)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 60, 180)
NEON_GREEN = (0, 255, 120)
NEON_YELLOW = (255, 255, 120)
WHITE = (240, 240, 240)
RED = (255, 80, 80)

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 26)
big_font = pygame.font.SysFont("consolas", 40)

# ---------- COMMON UTILS ----------
def draw_text(surface, text, size_font, color, x, y, center=True):
    f = pygame.font.SysFont("consolas", size_font)
    t = f.render(text, True, color)
    rect = t.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(t, rect)

def wait_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# ---------- PARTICLE ----------
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.randint(3, 6)
        self.color = color
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.life = 20

    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.size *= 0.9
        self.life -= 1

    def draw(self, win):
        if self.life > 0:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), int(self.size))

# =========================================================
# 1) CYBER DASH ARENA
# =========================================================
class DashPlayer:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 40
        self.speed = 4
        self.color = NEON_BLUE
        self.particles = []
        self.dash_cooldown = 0
        self.dash_power = 18

    def move(self, keys):
        dx = dy = 0
        if keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_s]: dy += self.speed
        if keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_d]: dx += self.speed

        self.x += dx
        self.y += dy

        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(0, min(self.y, HEIGHT - self.size))

        self.particles.append(Particle(self.x + self.size/2, self.y + self.size/2, self.color))

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

    def dash(self, keys):
        if self.dash_cooldown == 0 and keys[pygame.K_SPACE]:
            mx, my = pygame.mouse.get_pos()
            angle = math.atan2(my - self.y, mx - self.x)
            self.x += math.cos(angle) * self.dash_power
            self.y += math.sin(angle) * self.dash_power
            self.dash_cooldown = 60

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        for p in self.particles[:]:
            p.update()
            p.draw(win)
            if p.life <= 0:
                self.particles.remove(p)

class DashEnemy:
    def __init__(self):
        self.size = 35
        self.x = random.choice([0, WIDTH])
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1.5, 3.5)
        self.color = NEON_PINK

    def update(self, player):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

class DashOrb:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.size = 15
        self.color = NEON_GREEN

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size)

def game_cyber_dash():
    player = DashPlayer()
    enemies = []
    orbs = [DashOrb()]
    score = 0
    spawn_timer = 0

    running = True
    while running:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.dash(keys)
        player.draw(WIN)

        spawn_timer += 1
        if spawn_timer > 40:
            enemies.append(DashEnemy())
            spawn_timer = 0

        for e in enemies[:]:
            e.update(player)
            e.draw(WIN)
            if (player.x < e.x + e.size and
                player.x + player.size > e.x and
                player.y < e.y + e.size and
                player.y + player.size > e.y):
                running = False

        for o in orbs[:]:
            o.draw(WIN)
            if math.dist((player.x, player.y), (o.x, o.y)) < 40:
                score += 5
                orbs.remove(o)
                orbs.append(DashOrb())

        draw_text(WIN, f"Score: {score}", 26, NEON_YELLOW, 10, 10, center=False)
        draw_text(WIN, "ESC to return", 20, WHITE, WIDTH-10, 10, center=False)

        pygame.display.update()

    draw_text(WIN, "GAME OVER", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1200)

# =========================================================
# 2) TOP-DOWN SHOOTER
# =========================================================
class ShooterPlayer:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.size = 30
        self.speed = 5
        self.color = NEON_GREEN

    def move(self, keys):
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed
        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(0, min(self.y, HEIGHT - self.size))

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle
        self.size = 6
        self.color = NEON_YELLOW

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.size)

class ShooterEnemy:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH-self.size)
        self.y = -self.size
        self.speed = random.uniform(1.5, 3)
        self.color = NEON_PINK

    def update(self):
        self.y += self.speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

def game_topdown_shooter():
    player = ShooterPlayer()
    bullets = []
    enemies = []
    spawn_timer = 0
    score = 0

    running = True
    while running:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                angle = math.atan2(my - (player.y+player.size/2), mx - (player.x+player.size/2))
                bullets.append(Bullet(player.x+player.size/2, player.y+player.size/2, angle))

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw(WIN)

        spawn_timer += 1
        if spawn_timer > 40:
            enemies.append(ShooterEnemy())
            spawn_timer = 0

        for e in enemies[:]:
            e.update()
            e.draw(WIN)
            if e.y > HEIGHT:
                enemies.remove(e)
            if (player.x < e.x + e.size and
                player.x + player.size > e.x and
                player.y < e.y + e.size and
                player.y + player.size > e.y):
                running = False

        for b in bullets[:]:
            b.update()
            b.draw(WIN)
            if b.x < 0 or b.x > WIDTH or b.y < 0 or b.y > HEIGHT:
                bullets.remove(b)
                continue
            for e in enemies[:]:
                if (e.x < b.x < e.x+e.size and
                    e.y < b.y < e.y+e.size):
                    enemies.remove(e)
                    if b in bullets:
                        bullets.remove(b)
                    score += 1
                    break

        draw_text(WIN, f"Score: {score}", 26, NEON_YELLOW, 10, 10, center=False)
        draw_text(WIN, "Click to shoot | ESC to return", 20, WHITE, WIDTH//2, 20)

        pygame.display.update()

    draw_text(WIN, "GAME OVER", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1200)

# =========================================================
# 3) PORTAL PUZZLE (simple prototype)
# =========================================================
def game_portal_puzzle():
    player = pygame.Rect(100, HEIGHT-80, 40, 40)
    portal_a = pygame.Rect(150, 150, 40, 40)
    portal_b = pygame.Rect(WIDTH-200, 200, 40, 40)
    exit_rect = pygame.Rect(WIDTH-80, 40, 40, 40)
    speed = 4

    running = True
    while running:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= speed
        if keys[pygame.K_s]: player.y += speed
        if keys[pygame.K_a]: player.x -= speed
        if keys[pygame.K_d]: player.x += speed

        player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        if player.colliderect(portal_a):
            player.center = portal_b.center
        elif player.colliderect(portal_b):
            player.center = portal_a.center

        pygame.draw.rect(WIN, NEON_BLUE, player)
        pygame.draw.rect(WIN, NEON_PINK, portal_a, 2)
        pygame.draw.rect(WIN, NEON_PINK, portal_b, 2)
        pygame.draw.rect(WIN, NEON_GREEN, exit_rect)

        draw_text(WIN, "Reach the green exit | ESC to return", 22, WHITE, WIDTH//2, 20)

        if player.colliderect(exit_rect):
            draw_text(WIN, "LEVEL COMPLETE!", 40, NEON_GREEN, WIDTH//2, HEIGHT//2)
            pygame.display.update()
            pygame.time.wait(1200)
            running = False

        pygame.display.update()

# =========================================================
# 4) DRIFT RACER (very simple)
# =========================================================
def game_drift_racer():
    car = pygame.Rect(WIDTH//2-20, HEIGHT-120, 40, 70)
    lane_x = [WIDTH//2-150, WIDTH//2-50, WIDTH//2+50, WIDTH//2+150]
    obstacles = []
    speed = 6
    drift = 0
    score = 0
    spawn_timer = 0

    running = True
    while running:
        clock.tick(60)
        WIN.fill((10, 10, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: drift -= 0.5
        if keys[pygame.K_d]: drift += 0.5
        drift *= 0.9
        car.x += drift
        car.x = max(100, min(car.x, WIDTH-140))

        spawn_timer += 1
        if spawn_timer > 40:
            lane = random.choice(lane_x)
            obstacles.append(pygame.Rect(lane, -80, 40, 80))
            spawn_timer = 0

        for o in obstacles[:]:
            o.y += speed
            if o.y > HEIGHT:
                obstacles.remove(o)
                score += 1

        for o in obstacles:
            if car.colliderect(o):
                running = False

        pygame.draw.rect(WIN, NEON_BLUE, car)
        for o in obstacles:
            pygame.draw.rect(WIN, NEON_PINK, o)

        pygame.draw.line(WIN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

        draw_text(WIN, f"Score: {score}", 26, NEON_YELLOW, 10, 10, center=False)
        draw_text(WIN, "A/D to drift | ESC to return", 20, WHITE, WIDTH//2, 20)

        pygame.display.update()

    draw_text(WIN, "CRASHED!", 40, RED, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1200)

# =========================================================
# 5) ZOMBIE SURVIVAL (simple)
# =========================================================
class Zombie:
    def __init__(self):
        self.size = 30
        self.x = random.choice([0, WIDTH])
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 2)
        self.color = (120, 255, 120)

    def update(self, player_rect):
        angle = math.atan2(player_rect.centery - self.y, player_rect.centerx - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

def game_zombie_survival():
    player = pygame.Rect(WIDTH//2, HEIGHT//2, 35, 35)
    zombies = []
    bullets = []
    spawn_timer = 0
    score = 0
    speed = 4

    running = True
    while running:
        clock.tick(60)
        WIN.fill((5, 5, 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                angle = math.atan2(my - player.centery, mx - player.centerx)
                bullets.append([player.centerx, player.centery, angle])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= speed
        if keys[pygame.K_s]: player.y += speed
        if keys[pygame.K_a]: player.x -= speed
        if keys[pygame.K_d]: player.x += speed
        player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        spawn_timer += 1
        if spawn_timer > 30:
            zombies.append(Zombie())
            spawn_timer = 0

        for z in zombies[:]:
            z.update(player)
            z.draw(WIN)
            if player.colliderect(pygame.Rect(z.x, z.y, z.size, z.size)):
                running = False

        for b in bullets[:]:
            b[0] += math.cos(b[2]) * 10
            b[1] += math.sin(b[2]) * 10
            pygame.draw.circle(WIN, NEON_YELLOW, (int(b[0]), int(b[1])), 5)
            if b[0] < 0 or b[0] > WIDTH or b[1] < 0 or b[1] > HEIGHT:
                bullets.remove(b)
                continue
            for z in zombies[:]:
                if (z.x < b[0] < z.x+z.size and
                    z.y < b[1] < z.y+z.size):
                    zombies.remove(z)
                    if b in bullets:
                        bullets.remove(b)
                    score += 1
                    break

        pygame.draw.rect(WIN, NEON_BLUE, player)
        draw_text(WIN, f"Score: {score}", 26, NEON_GREEN, 10, 10, center=False)
        draw_text(WIN, "WASD move, click shoot | ESC to return", 20, WHITE, WIDTH//2, 20)

        pygame.display.update()

    draw_text(WIN, "EATEN!", 40, RED, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1200)

# =========================================================
# 6) MAGIC SPELLCASTER (simple arena)
# =========================================================
def game_magic_spellcaster():
    player = pygame.Rect(WIDTH//2, HEIGHT//2, 35, 35)
    orbs = []
    enemies = []
    spawn_timer = 0
    score = 0
    speed = 4

    running = True
    while running:
        clock.tick(60)
        WIN.fill((15, 5, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                angle = math.atan2(my - player.centery, mx - player.centerx)
                orbs.append([player.centerx, player.centery, angle, 0])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= speed
        if keys[pygame.K_s]: player.y += speed
        if keys[pygame.K_a]: player.x -= speed
        if keys[pygame.K_d]: player.x += speed
        player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        spawn_timer += 1
        if spawn_timer > 40:
            enemies.append(pygame.Rect(random.randint(0, WIDTH-30), -30, 30, 30))
            spawn_timer = 0

        for e in enemies[:]:
            e.y += 2
            pygame.draw.rect(WIN, NEON_PINK, e)
            if e.y > HEIGHT:
                enemies.remove(e)
            if player.colliderect(e):
                running = False

        for o in orbs[:]:
            o[0] += math.cos(o[2]) * 8
            o[1] += math.sin(o[2]) * 8
            o[3] += 1
            radius = 8 + o[3]//3
            pygame.draw.circle(WIN, NEON_BLUE, (int(o[0]), int(o[1])), radius, 2)
            if o[0] < 0 or o[0] > WIDTH or o[1] < 0 or o[1] > HEIGHT or o[3] > 60:
                orbs.remove(o)
                continue
            for e in enemies[:]:
                if e.collidepoint(o[0], o[1]):
                    enemies.remove(e)
                    if o in orbs:
                        orbs.remove(o)
                    score += 2
                    break

        pygame.draw.rect(WIN, NEON_GREEN, player)
        draw_text(WIN, f"Score: {score}", 26, NEON_YELLOW, 10, 10, center=False)
        draw_text(WIN, "WASD move, click cast | ESC to return", 20, WHITE, WIDTH//2, 20)

        pygame.display.update()

    draw_text(WIN, "DEFEATED!", 40, RED, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1200)

# =========================================================
# 7) RETRO ROGUELIKE (tiny prototype)
# =========================================================
def game_retro_roguelike():
    tile = 40
    cols = WIDTH // tile
    rows = HEIGHT // tile
    player = [cols//2, rows//2]
    enemies = [[random.randint(0, cols-1), random.randint(0, rows-1)] for _ in range(5)]
    score = 0

    running = True
    while running:
        clock.tick(10)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w: player[1] -= 1
                if event.key == pygame.K_s: player[1] += 1
                if event.key == pygame.K_a: player[0] -= 1
                if event.key == pygame.K_d: player[0] += 1

        player[0] = max(0, min(cols-1, player[0]))
        player[1] = max(0, min(rows-1, player[1]))

        for e in enemies:
            if random.random() < 0.5:
                e[0] += random.choice([-1, 0, 1])
                e[1] += random.choice([-1, 0, 1])
                e[0] = max(0, min(cols-1, e[0]))
                e[1] = max(0, min(rows-1, e[1]))

        for e in enemies[:]:
            if e == player:
                running = False
            if abs(e[0]-player[0]) + abs(e[1]-player[1]) == 1:
                enemies.remove(e)
                score += 1

        for x in range(cols):
            for y in range(rows):
                pygame.draw.rect(WIN, (20, 20, 20), (x*tile, y*tile, tile, tile), 1)

        pygame.draw.rect(WIN, NEON_GREEN, (player[0]*tile+5, player[1]*tile+5, tile-10, tile-10))
        for e in enemies:
            pygame.draw.rect(WIN, NEON_PINK, (e[0]*tile+5, e[1]*tile+5, tile-10, tile-10))

        draw_text(WIN, f"Score: {score}", 24, NEON_YELLOW, 10, 10, center=False)
        draw_text(WIN, "WASD move, touch enemies to kill | ESC to return", 18, WHITE, WIDTH//2, 20)

        pygame.display.update()

    draw_text(WIN, "YOU DIED", 40, RED, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1200)

# =========================================================
# ARCADE MENU
# =========================================================
def main_menu():
    while True:
        clock.tick(60)
        WIN.fill(BLACK)

        draw_text(WIN, "NEON ARCADE", 50, NEON_BLUE, WIDTH//2, 80)
        draw_text(WIN, "1 - Cyber Dash Arena", 26, WHITE, WIDTH//2, 180)
        draw_text(WIN, "2 - Top-Down Shooter", 26, WHITE, WIDTH//2, 220)
        draw_text(WIN, "3 - Portal Puzzle", 26, WHITE, WIDTH//2, 260)
        draw_text(WIN, "4 - Drift Racer", 26, WHITE, WIDTH//2, 300)
        draw_text(WIN, "5 - Zombie Survival", 26, WHITE, WIDTH//2, 340)
        draw_text(WIN, "6 - Magic Spellcaster", 26, WHITE, WIDTH//2, 380)
        draw_text(WIN, "7 - Retro Roguelike", 26, WHITE, WIDTH//2, 420)
        draw_text(WIN, "ESC - Quit", 24, NEON_PINK, WIDTH//2, 480)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_1:
                    game_cyber_dash()
                if event.key == pygame.K_2:
                    game_topdown_shooter()
                if event.key == pygame.K_3:
                    game_portal_puzzle()
                if event.key == pygame.K_4:
                    game_drift_racer()
                if event.key == pygame.K_5:
                    game_zombie_survival()
                if event.key == pygame.K_6:
                    game_magic_spellcaster()
                if event.key == pygame.K_7:
                    game_retro_roguelike()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
