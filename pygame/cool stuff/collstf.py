import pygame
import sys
import random
import math
pygame.init()

WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Mega Arcade")

BLACK = (8, 8, 15)
WHITE = (240, 240, 240)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 60, 180)
NEON_GREEN = (0, 255, 120)
NEON_YELLOW = (255, 255, 120)
RED = (255, 80, 80)
ORANGE = (255, 150, 50)
CYAN = (80, 220, 255)

clock = pygame.time.Clock()

def draw_text(surface, text, size, color, x, y, center=True):
    font = pygame.font.SysFont("consolas", size)
    t = font.render(text, True, color)
    r = t.get_rect()
    if center:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    surface.blit(t, r)

# =========================================================
# 1) SKYBOUND GLIDER – physics flight
# =========================================================
def game_skybound_glider():
    glider = pygame.Rect(WIDTH//2, HEIGHT//2, 60, 20)
    vel_x, vel_y = 0, 0
    gravity = 0.15
    lift = -0.4
    wind_timer = 0
    wind_force = 0
    score = 0
    rings = []
    for _ in range(5):
        rings.append(pygame.Rect(random.randint(100, WIDTH-100),
                                 random.randint(50, HEIGHT-200), 40, 40))
    running = True
    while running:
        clock.tick(60)
        WIN.fill((20, 40, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            vel_y += lift
        vel_y += gravity

        wind_timer += 1
        if wind_timer > 120:
            wind_timer = 0
            wind_force = random.uniform(-0.2, 0.2)
        vel_x += wind_force
        vel_x *= 0.99

        glider.x += int(vel_x)
        glider.y += int(vel_y)

        if glider.y < 0:
            glider.y = 0
            vel_y = 0
        if glider.y > HEIGHT-50:
            glider.y = HEIGHT-50
            vel_y *= -0.3

        if glider.x < 0:
            glider.x = 0
            vel_x *= -0.3
        if glider.x > WIDTH-60:
            glider.x = WIDTH-60
            vel_x *= -0.3

        for r in rings[:]:
            pygame.draw.ellipse(WIN, NEON_YELLOW, r, 3)
            if glider.colliderect(r):
                rings.remove(r)
                score += 10
                rings.append(pygame.Rect(random.randint(100, WIDTH-100),
                                         random.randint(50, HEIGHT-200), 40, 40))

        pygame.draw.polygon(WIN, WHITE, [
            (glider.x, glider.y+glider.height//2),
            (glider.x+glider.width, glider.y),
            (glider.x+glider.width, glider.y+glider.height)
        ])

        draw_text(WIN, f"Score: {score}", 26, WHITE, 10, 10, center=False)
        draw_text(WIN, "SPACE to gain lift | ESC to return", 20, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "FLIGHT OVER", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1000)

# =========================================================
# 2) DUNGEON CHEF – gather + cook
# =========================================================
def game_dungeon_chef():
    player = pygame.Rect(10000, HEIGHT-100, 40, 40)
    speed = 4
    ingredients = []
    monsters = []
    for _ in range(5):
        ingredients.append(pygame.Rect(random.randint(100, WIDTH-100),
                                       random.randint(100, HEIGHT-200), 20, 20))
    for _ in range(4):
        monsters.append(pygame.Rect(random.randint(200, WIDTH-100),
                                    random.randint(100, HEIGHT-200), 35, 35))
    kitchen = pygame.Rect(WIDTH-120, HEIGHT-120, 80, 80)
    bag = 0
    meals = 0
    running = True
    while running:
        clock.tick(60)
        WIN.fill((40, 20, 20))

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

        for m in monsters:
            dx = player.x - m.x
            dy = player.y - m.y
            dist = max(1, math.hypot(dx, dy))
            m.x += int(dx/dist * 1.2)
            m.y += int(dy/dist * 1.2)
            if m.colliderect(player):
                running = False

        for ing in ingredients[:]:
            if player.colliderect(ing):
                ingredients.remove(ing)
                bag += 1
                ingredients.append(pygame.Rect(random.randint(50, WIDTH-150),
                                               random.randint(50, HEIGHT-200), 20, 20))

        if player.colliderect(kitchen) and bag > 0:
            meals += bag
            bag = 0

        pygame.draw.rect(WIN, ORANGE, kitchen)
        for ing in ingredients:
            pygame.draw.rect(WIN, NEON_GREEN, ing)
        for m in monsters:
            pygame.draw.rect(WIN, RED, m)
        pygame.draw.rect(WIN, WHITE, player)

        draw_text(WIN, f"Ingredients: {bag}  Meals cooked: {meals}", 24, WHITE, 10, 10, center=False)
        draw_text(WIN, "Bring ingredients to kitchen | ESC to return", 20, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "YOU WERE CAUGHT!", 40, RED, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1000)

# =========================================================
# 3) ROBO-FACTORY TYCOON – tiny automation
# =========================================================
def game_robo_factory():
    grid_size = 40
    cols = WIDTH // grid_size
    rows = HEIGHT // grid_size
    belts = {}   # (x,y) -> direction
    resources = []
    products = 0
    cursor = [cols//2, rows//2]
    output_cell = (cols-2, rows//2)

    for _ in range(5):
        resources.append([1, random.randint(1, rows-2)])

    running = True
    while running:
        clock.tick(10)
        WIN.fill((15, 15, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w: cursor[1] = max(0, cursor[1]-1)
                if event.key == pygame.K_s: cursor[1] = min(rows-1, cursor[1]+1)
                if event.key == pygame.K_a: cursor[0] = max(0, cursor[0]-1)
                if event.key == pygame.K_d: cursor[0] = min(cols-1, cursor[0]+1)
                if event.key == pygame.K_1:
                    belts[tuple(cursor)] = (1, 0)
                if event.key == pygame.K_2:
                    belts[tuple(cursor)] = (0, 1)
                if event.key == pygame.K_3:
                    belts[tuple(cursor)] = (-1, 0)
                if event.key == pygame.K_4:
                    belts[tuple(cursor)] = (0, -1)

        for r in resources:
            cell = (r[0], r[1])
            if cell in belts:
                dx, dy = belts[cell]
                r[0] += dx
                r[1] += dy
            if (r[0], r[1]) == output_cell:
                products += 1
                r[0], r[1] = 1, random.randint(1, rows-2)
            r[0] = max(0, min(cols-1, r[0]))
            r[1] = max(0, min(rows-1, r[1]))

        for x in range(cols):
            for y in range(rows):
                pygame.draw.rect(WIN, (30, 30, 40), (x*grid_size, y*grid_size, grid_size, grid_size), 1)

        for (x, y), (dx, dy) in belts.items():
            cx = x*grid_size + grid_size//2
            cy = y*grid_size + grid_size//2
            pygame.draw.circle(WIN, NEON_BLUE, (cx, cy), 10, 2)
            pygame.draw.line(WIN, NEON_BLUE, (cx, cy),
                             (cx+dx*10, cy+dy*10), 2)

        for r in resources:
            pygame.draw.circle(WIN, NEON_YELLOW,
                               (r[0]*grid_size+grid_size//2, r[1]*grid_size+grid_size//2), 8)

        ox, oy = output_cell
        pygame.draw.rect(WIN, NEON_GREEN, (ox*grid_size+5, oy*grid_size+5, grid_size-10, grid_size-10), 2)

        pygame.draw.rect(WIN, NEON_PINK,
                         (cursor[0]*grid_size+2, cursor[1]*grid_size+2, grid_size-4, grid_size-4), 2)

        draw_text(WIN, f"Products: {products}", 24, WHITE, 10, 10, center=False)
        draw_text(WIN, "1-4 place belt directions | ESC to return", 18, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "FACTORY SHUTDOWN", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1000)

# =========================================================
# 4) SHADOW SWAP – two dimensions
# =========================================================
def game_shadow_swap():
    player = pygame.Rect(80, HEIGHT-100, 40, 40)
    speed = 4
    gravity = 0.4
    vel_y = 0
    on_ground = False
    world = 0  # 0 = light, 1 = shadow

    platforms_light = [
        pygame.Rect(0, HEIGHT-40, WIDTH, 40),
        pygame.Rect(150, 500, 150, 20),
        pygame.Rect(400, 400, 150, 20),
        pygame.Rect(650, 300, 150, 20)
    ]
    platforms_shadow = [
        pygame.Rect(0, HEIGHT-40, WIDTH, 40),
        pygame.Rect(100, 450, 150, 20),
        pygame.Rect(350, 350, 150, 20),
        pygame.Rect(600, 250, 150, 20)
    ]
    exit_rect = pygame.Rect(WIDTH-80, 200, 40, 40)

    running = True
    while running:
        clock.tick(60)
        WIN.fill((10, 10, 20) if world == 0 else (5, 0, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and on_ground:
                    vel_y = -9
                if event.key == pygame.K_TAB:
                    world = 1-world

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: player.x -= speed
        if keys[pygame.K_d]: player.x += speed

        vel_y += gravity
        player.y += int(vel_y)
        on_ground = False

        plats = platforms_light if world == 0 else platforms_shadow
        for p in plats:
            if player.colliderect(p) and vel_y >= 0:
                player.bottom = p.top
                vel_y = 0
                on_ground = True

        if player.colliderect(exit_rect):
            draw_text(WIN, "LEVEL COMPLETE!", 40, NEON_GREEN, WIDTH//2, HEIGHT//2)
            pygame.display.update()
            pygame.time.wait(1000)
            running = False

        for p in platforms_light:
            pygame.draw.rect(WIN, (80, 80, 120), p, 0 if world == 0 else 1)
        for p in platforms_shadow:
            pygame.draw.rect(WIN, (120, 40, 160), p, 0 if world == 1 else 1)

        pygame.draw.rect(WIN, NEON_GREEN, exit_rect)
        pygame.draw.rect(WIN, WHITE, player)

        draw_text(WIN, "TAB swap worlds | A/D move | SPACE jump | ESC return", 18, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "DIMENSION SHIFTED", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(800)

# =========================================================
# 5) GALACTIC COURIER – space delivery
# =========================================================
def game_galactic_courier():
    ship = pygame.Rect(WIDTH//2, HEIGHT-100, 40, 40)
    vel_x, vel_y = 0, 0
    thrust = 0.4
    friction = 0.98
    fuel = 100
    money = 0
    target = pygame.Rect(random.randint(50, WIDTH-100), 60, 40, 40)
    asteroids = []
    for _ in range(8):
        asteroids.append(pygame.Rect(random.randint(0, WIDTH-40),
                                     random.randint(100, HEIGHT-200), 30, 30))

    running = True
    while running:
        clock.tick(60)
        WIN.fill((5, 5, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if fuel > 0:
            if keys[pygame.K_w]:
                vel_y -= thrust; fuel -= 0.2
            if keys[pygame.K_s]:
                vel_y += thrust; fuel -= 0.2
            if keys[pygame.K_a]:
                vel_x -= thrust; fuel -= 0.2
            if keys[pygame.K_d]:
                vel_x += thrust; fuel -= 0.2

        vel_x *= friction
        vel_y *= friction
        ship.x += int(vel_x)
        ship.y += int(vel_y)
        ship.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        for a in asteroids:
            pygame.draw.circle(WIN, (120, 120, 120), (a.x+15, a.y+15), 15)
            if ship.colliderect(a):
                running = False

        if ship.colliderect(target):
            money += 50
            fuel = min(100, fuel+30)
            target.x = random.randint(50, WIDTH-100)
            target.y = random.randint(50, HEIGHT-200)

        pygame.draw.rect(WIN, NEON_GREEN, target)
        pygame.draw.polygon(WIN, NEON_BLUE, [
            (ship.x+20, ship.y),
            (ship.x, ship.y+40),
            (ship.x+40, ship.y+40)
        ])

        draw_text(WIN, f"Fuel: {int(fuel)}  Money: {money}", 24, WHITE, 10, 10, center=False)
        draw_text(WIN, "WASD thrust | Deliver to green | ESC return", 18, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "SHIP LOST", 40, RED, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1000)

# =========================================================
# 6) MONSTER MUSICIAN – rhythm battle
# =========================================================
def game_monster_musician():
    beat_time = 600
    last_beat = pygame.time.get_ticks()
    beat_index = 0
    pattern = ["a", "s", "d", "a", "d", "s", "a", "d"]
    hp_player = 5
    hp_monster = 8
    feedback = ""
    running = True
    while running:
        clock.tick(60)
        now = pygame.time.get_ticks()
        WIN.fill((10, 0, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                key = pygame.key.name(event.key)
                if key in ["a", "s", "d"]:
                    diff = now - last_beat
                    if abs(diff) < 200 and key == pattern[beat_index]:
                        hp_monster -= 1
                        feedback = "HIT!"
                    else:
                        hp_player -= 1
                        feedback = "MISS!"

        if now - last_beat > beat_time:
            last_beat = now
            beat_index = (beat_index+1) % len(pattern)

        if hp_player <= 0 or hp_monster <= 0:
            running = False

        pygame.draw.rect(WIN, RED, (100, 100, 200, 30))
        pygame.draw.rect(WIN, NEON_GREEN, (100, 100, 200*hp_player/5, 30))
        pygame.draw.rect(WIN, RED, (WIDTH-300, 100, 200, 30))
        pygame.draw.rect(WIN, NEON_PINK, (WIDTH-300, 100, 200*hp_monster/8, 30))

        draw_text(WIN, "Player", 20, WHITE, 200, 80)
        draw_text(WIN, "Monster", 20, WHITE, WIDTH-200, 80)

        draw_text(WIN, f"Next beat: {pattern[beat_index].upper()}", 40, NEON_YELLOW, WIDTH//2, HEIGHT//2)
        draw_text(WIN, feedback, 30, WHITE, WIDTH//2, HEIGHT//2+60)
        draw_text(WIN, "Press A/S/D on beat | ESC return", 18, WHITE, WIDTH//2, 20)

        pygame.display.update()
    result = "YOU WON!" if hp_monster <= 0 else "YOU LOST!"
    draw_text(WIN, result, 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1000)

# =========================================================
# 7) ARCTIC SURVIVAL – temperature management
# =========================================================
def game_arctic_survival():
    player = pygame.Rect(WIDTH//2, HEIGHT-100, 40, 40)
    speed = 4
    temp = 100
    fires = [pygame.Rect(150, HEIGHT-80, 40, 40)]
    wolves = []
    for _ in range(4):
        wolves.append(pygame.Rect(random.randint(0, WIDTH-40),
                                  random.randint(100, HEIGHT-200), 35, 35))
    running = True
    while running:
        clock.tick(60)
        WIN.fill((200, 220, 255))

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

        temp -= 0.1
        near_fire = False
        for f in fires:
            if player.centerx in range(f.x-80, f.x+120) and player.centery in range(f.y-80, f.y+120):
                near_fire = True
        if near_fire:
            temp = min(100, temp+0.4)

        for w in wolves:
            dx = player.x - w.x
            dy = player.y - w.y
            dist = max(1, math.hypot(dx, dy))
            w.x += int(dx/dist * 1.2)
            w.y += int(dy/dist * 1.2)
            if w.colliderect(player):
                running = False

        if temp <= 0:
            running = False

        for f in fires:
            pygame.draw.rect(WIN, ORANGE, f)
        for w in wolves:
            pygame.draw.rect(WIN, (120, 120, 120), w)
        pygame.draw.rect(WIN, (0, 0, 80), player)

        pygame.draw.rect(WIN, RED, (10, 10, 200, 20))
        pygame.draw.rect(WIN, NEON_BLUE, (10, 10, 200*temp/100, 20))
        draw_text(WIN, "Temp", 18, BLACK, 220, 10, center=False)
        draw_text(WIN, "Stay near fire, avoid wolves | ESC return", 18, BLACK, WIDTH//2, 20)

        pygame.display.update()
    draw_text(WIN, "YOU FROZE...", 40, BLUE if (BLUE:= (0,0,150)) else BLUE, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(1000)

# =========================================================
# 8) TIME LOOP DETECTIVE – tiny loop
# =========================================================
def game_time_loop_detective():
    suspect_positions = [(200, 300), (400, 300), (600, 300)]
    culprit_index = random.randint(0, 2)
    time_limit = 60000
    start_time = pygame.time.get_ticks()
    chosen = None
    info = ""
    running = True
    while running:
        clock.tick(60)
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        if elapsed > time_limit:
            start_time = now
            info = "Time loop reset. Try again."

        WIN.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    chosen = event.key - pygame.K_1
                    if chosen == culprit_index:
                        info = "You found the culprit!"
                    else:
                        info = "Wrong suspect. Loop continues."

        for i, (x, y) in enumerate(suspect_positions):
            pygame.draw.rect(WIN, NEON_PINK if i == culprit_index else NEON_BLUE,
                             (x-30, y-40, 60, 80), 2)
            draw_text(WIN, str(i+1), 24, WHITE, x, y+60)

        remaining = max(0, (time_limit - (now-start_time))//1000)
        draw_text(WIN, f"Time left in loop: {remaining}s", 24, WHITE, WIDTH//2, 40)
        draw_text(WIN, "Press 1/2/3 to accuse | ESC return", 18, WHITE, WIDTH//2, 20)
        draw_text(WIN, info, 22, NEON_YELLOW, WIDTH//2, HEIGHT-60)

        pygame.display.update()
    draw_text(WIN, "CASE CLOSED?", 40, NEON_GREEN, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(800)

# =========================================================
# 9) NEON DRIFT ARENA – car combat
# =========================================================
def game_neon_drift_arena():
    car = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 20)
    angle = 0
    speed = 0
    bullets = []
    enemies = []
    for _ in range(5):
        enemies.append(pygame.Rect(random.randint(50, WIDTH-50),
                                   random.randint(50, HEIGHT-50), 40, 20))
    running = True
    while running:
        clock.tick(60)
        WIN.fill((5, 5, 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    bx = car.centerx + math.cos(angle)*20
                    by = car.centery + math.sin(angle)*20
                    bullets.append([bx, by, angle])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: angle -= 0.08
        if keys[pygame.K_d]: angle += 0.08
        if keys[pygame.K_w]: speed += 0.2
        if keys[pygame.K_s]: speed -= 0.2
        speed *= 0.96
        car.x += int(math.cos(angle)*speed)
        car.y += int(math.sin(angle)*speed)
        car.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        for e in enemies[:]:
            dx = car.x - e.x
            dy = car.y - e.y
            dist = max(1, math.hypot(dx, dy))
            e.x += int(dx/dist * 1.0)
            e.y += int(dy/dist * 1.0)
            if e.colliderect(car):
                running = False

        for b in bullets[:]:
            b[0] += math.cos(b[2])*10
            b[1] += math.sin(b[2])*10
            pygame.draw.circle(WIN, NEON_YELLOW, (int(b[0]), int(b[1])), 4)
            if b[0] < 0 or b[0] > WIDTH or b[1] < 0 or b[1] > HEIGHT:
                bullets.remove(b)
                continue
            for e in enemies[:]:
                if e.collidepoint(b[0], b[1]):
                    enemies.remove(e)
                    if b in bullets:
                        bullets.remove(b)
                    break

        if not enemies:
            running = False

        car_points = []
        for offset in [(-20, -10), (20, 0), (-20, 10)]:
            ox, oy = offset
            rx = car.centerx + ox*math.cos(angle) - oy*math.sin(angle)
            ry = car.centery + ox*math.sin(angle) + oy*math.cos(angle)
            car_points.append((rx, ry))
        pygame.draw.polygon(WIN, NEON_BLUE, car_points)

        for e in enemies:
            pygame.draw.rect(WIN, NEON_PINK, e)

        draw_text(WIN, "W/S accel, A/D steer, SPACE shoot | ESC return", 18, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "ARENA OVER", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(800)

# =========================================================
# 10) ROBO-PAINTER – creative sandbox
# =========================================================
def game_robo_painter():
    robot = pygame.Rect(WIDTH//2, HEIGHT//2, 30, 30)
    speed = 5
    color_index = 0
    colors = [NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW, CYAN, ORANGE]
    painting = True
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((0, 0, 0))

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_c:
                    color_index = (color_index+1) % len(colors)
                if event.key == pygame.K_p:
                    painting = not painting
                if event.key == pygame.K_r:
                    canvas.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: robot.y -= speed
        if keys[pygame.K_s]: robot.y += speed
        if keys[pygame.K_a]: robot.x -= speed
        if keys[pygame.K_d]: robot.x += speed
        robot.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        if painting:
            pygame.draw.circle(canvas, colors[color_index], robot.center, 8)

        WIN.blit(canvas, (0, 0))
        pygame.draw.rect(WIN, WHITE, robot, 2)
        pygame.draw.rect(WIN, colors[color_index], robot.inflate(-10, -10))

        draw_text(WIN, "WASD move | C color | P toggle paint | R clear | ESC return", 18, WHITE, WIDTH//2, 20)
        pygame.display.update()
    draw_text(WIN, "ROBO-PAINT OFFLINE", 40, NEON_PINK, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.wait(800)

# =========================================================
# ARCADE MENU
# =========================================================
def main_menu():
    while True:
        clock.tick(60)
        WIN.fill(BLACK)
        draw_text(WIN, "NEON MEGA ARCADE", 50, NEON_BLUE, WIDTH//2, 80)
        draw_text(WIN, "1 - Skybound Glider", 26, WHITE, WIDTH//2, 170)
        draw_text(WIN, "2 - Dungeon Chef", 26, WHITE, WIDTH//2, 210)
        draw_text(WIN, "3 - Robo-Factory Tycoon", 26, WHITE, WIDTH//2, 250)
        draw_text(WIN, "4 - Shadow Swap", 26, WHITE, WIDTH//2, 290)
        draw_text(WIN, "5 - Galactic Courier", 26, WHITE, WIDTH//2, 330)
        draw_text(WIN, "6 - Monster Musician", 26, WHITE, WIDTH//2, 370)
        draw_text(WIN, "7 - Arctic Survival", 26, WHITE, WIDTH//2, 410)
        draw_text(WIN, "8 - Time Loop Detective", 26, WHITE, WIDTH//2, 450)
        draw_text(WIN, "9 - Neon Drift Arena", 26, WHITE, WIDTH//2, 490)
        draw_text(WIN, "0 - Robo-Painter", 26, WHITE, WIDTH//2, 530)
        draw_text(WIN, "ESC - Quit", 22, NEON_PINK, WIDTH//2, 580)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_1:
                    game_skybound_glider()
                if event.key == pygame.K_2:
                    game_dungeon_chef()
                if event.key == pygame.K_3:
                    game_robo_factory()
                if event.key == pygame.K_4:
                    game_shadow_swap()
                if event.key == pygame.K_5:
                    game_galactic_courier()
                if event.key == pygame.K_6:
                    game_monster_musician()
                if event.key == pygame.K_7:
                    game_arctic_survival()
                if event.key == pygame.K_8:
                    game_time_loop_detective()
                if event.key == pygame.K_9:
                    game_neon_drift_arena()
                if event.key == pygame.K_0:
                    game_robo_painter()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
