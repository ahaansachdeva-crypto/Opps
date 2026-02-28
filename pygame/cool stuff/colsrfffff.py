"""
╔═══════════════════════════════════════════════════════════════════╗
║             ⚡ NEON ARCADE ULTIMATE - 10 GAME HUB ⚡              ║
║                                                                   ║
║  1. GRAVITY FLUX      - Reverse-gravity platformer               ║
║  2. CHROMATIC HUNT    - Color-matching reflex game               ║
║  3. ORBIT DEFENDER    - Circular space defense                   ║
║  4. PIXEL SNAKE RAVE  - Neon snake with powerups                 ║
║  5. MEMORY MATRIX     - Pattern recall challenge                 ║
║  6. REACTION BLITZ    - Reaction time tester                     ║
║  7. NEON TYPER        - Typing speed test                        ║
║  8. ASTEROID DODGE    - Weave through asteroid fields            ║
║  9. BOUNCE WARS       - Pong-style with powerups                 ║
║ 10. RHYTHM PULSE      - Music-free rhythm game                   ║
╚═══════════════════════════════════════════════════════════════════╝

Requirements: pip install pygame
Run: python neon_arcade_ultimate.py
"""

import pygame
import sys
import math
import random
import time
import string
from collections import deque

# ─── INIT ───────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚡ NEON ARCADE ULTIMATE ⚡")
clock = pygame.time.Clock()

# ─── COLORS ─────────────────────────────────────────────────
BLACK        = (0, 0, 0)
WHITE        = (255, 255, 255)
NEON_PINK    = (255, 16, 120)
NEON_BLUE    = (0, 200, 255)
NEON_GREEN   = (57, 255, 20)
NEON_PURPLE  = (180, 0, 255)
NEON_ORANGE  = (255, 165, 0)
NEON_YELLOW  = (255, 255, 0)
NEON_RED     = (255, 50, 50)
NEON_CYAN    = (0, 255, 220)
NEON_LIME    = (180, 255, 0)
NEON_MAGENTA = (255, 0, 180)
DARK_BG      = (6, 6, 18)
DARK_PANEL   = (12, 12, 30)
GRID_COLOR   = (18, 18, 45)

ALL_NEONS = [NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_ORANGE,
             NEON_YELLOW, NEON_RED, NEON_CYAN, NEON_LIME, NEON_MAGENTA]

# ─── FONTS ──────────────────────────────────────────────────
def load_font(name, size, bold=False):
    for fn in [name, "consolas", "courier new", "monospace", "dejavusansmono"]:
        try:
            f = pygame.font.SysFont(fn, size, bold=bold)
            if f:
                return f
        except:
            pass
    return pygame.font.Font(None, size)

font_title    = load_font("consolas", 54, bold=True)
font_subtitle = load_font("consolas", 30, bold=True)
font_medium   = load_font("consolas", 22)
font_small    = load_font("consolas", 17)
font_tiny     = load_font("consolas", 13)
font_huge     = load_font("consolas", 76, bold=True)
font_game     = load_font("consolas", 18)
font_mega     = load_font("consolas", 100, bold=True)
font_typing   = load_font("consolas", 26)
font_typing_sm= load_font("consolas", 20)


# ─── SHARED UTILITY FUNCTIONS ───────────────────────────────
def draw_text_centered(text, font, color, y, surface=None, x=None):
    surf = surface or screen
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x or WIDTH // 2, y))
    surf.blit(rendered, rect)
    return rect

def draw_text(text, font, color, x, y, surface=None):
    surf = surface or screen
    rendered = font.render(text, True, color)
    surf.blit(rendered, (x, y))
    return rendered.get_rect(topleft=(x, y))

def draw_text_right(text, font, color, x, y, surface=None):
    surf = surface or screen
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(topright=(x, y))
    surf.blit(rendered, rect)
    return rect

def glow_circle(surface, color, center, radius, intensity=3):
    for i in range(intensity, 0, -1):
        s = pygame.Surface((radius * 4 + 20, radius * 4 + 20), pygame.SRCALPHA)
        alpha = max(8, 55 // i)
        pygame.draw.circle(s, (*color[:3], alpha),
                           (radius * 2 + 10, radius * 2 + 10), radius + i * 5)
        surface.blit(s, (center[0] - radius * 2 - 10, center[1] - radius * 2 - 10))
    pygame.draw.circle(surface, color, center, radius)

def draw_grid_bg():
    screen.fill(DARK_BG)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)

def draw_scanlines(alpha=12):
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y), 1)

def pulse_color(base, t, speed=3, amount=60):
    f = (math.sin(t * speed) + 1) / 2
    return tuple(min(255, max(0, int(c + amount * f))) for c in base)

def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def hsv_to_rgb(h, s, v):
    c = pygame.Color(0)
    c.hsva = (h % 360, s, v, 100)
    return (c.r, c.g, c.b)

def draw_neon_rect(surface, color, rect, width=2):
    gs = pygame.Surface((rect[2] + 16, rect[3] + 16), pygame.SRCALPHA)
    pygame.draw.rect(gs, (*color[:3], 25), (0, 0, rect[2] + 16, rect[3] + 16), border_radius=10)
    surface.blit(gs, (rect[0] - 8, rect[1] - 8))
    pygame.draw.rect(surface, color, rect, width, border_radius=6)

def draw_hud_bar(x, y, w, h, ratio, color, bg=(30, 30, 50)):
    pygame.draw.rect(screen, bg, (x, y, w, h), border_radius=4)
    bw = max(0, int(w * max(0, min(1, ratio))))
    if bw > 0:
        pygame.draw.rect(screen, color, (x, y, bw, h), border_radius=4)

def particle_burst(particles, x, y, color, count=15):
    for _ in range(count):
        a = random.uniform(0, math.pi * 2)
        sp = random.uniform(1, 6)
        particles.append({
            'x': x, 'y': y,
            'vx': math.cos(a) * sp, 'vy': math.sin(a) * sp,
            'life': random.randint(20, 55),
            'color': color, 'size': random.uniform(2, 5)
        })

def update_particles(particles):
    for p in particles[:]:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += 0.03
        p['life'] -= 1
        p['size'] = max(0.5, p['size'] - 0.04)
        if p['life'] <= 0:
            particles.remove(p)
        else:
            a = min(255, p['life'] * 5)
            c = tuple(min(255, int(ch * (p['life'] / 55))) for ch in p['color'][:3])
            pygame.draw.circle(screen, c, (int(p['x']), int(p['y'])), max(1, int(p['size'])))

def draw_stars(stars, t):
    for s in stars:
        s['y'] += s['speed']
        if s['y'] > HEIGHT:
            s['y'] = 0
            s['x'] = random.randint(0, WIDTH)
        b = int(80 + 60 * math.sin(t * 2 + s['x'] * 0.1))
        pygame.draw.circle(screen, (b, b, b + 40),
                           (int(s['x']), int(s['y'])), s['size'])

def make_stars(n=100):
    return [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT),
             'speed': random.uniform(0.15, 1.2), 'size': random.randint(1, 3)} for _ in range(n)]

def draw_hud_bg(h=45):
    hud = pygame.Surface((WIDTH, h), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 140))
    screen.blit(hud, (0, 0))

def game_over_screen(title, stats_lines, particles):
    """Generic game over overlay."""
    draw_grid_bg()
    # Darken
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    draw_text_centered(title, font_huge, NEON_RED, HEIGHT // 2 - 80)
    for i, (txt, col) in enumerate(stats_lines):
        draw_text_centered(txt, font_subtitle, col, HEIGHT // 2 - 10 + i * 45)
    draw_text_centered("[R] Restart  [ESC] Menu", font_small, (150, 150, 180), HEIGHT // 2 + 80 + len(stats_lines) * 20)
    update_particles(particles)
    draw_scanlines(6)
    pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  TYPING TEST WORD LISTS
# ═══════════════════════════════════════════════════════════
WORD_POOL = [
    "neon", "arcade", "quantum", "pixel", "cyber", "glitch", "matrix", "pulse",
    "vector", "binary", "nexus", "vortex", "plasma", "photon", "laser", "turbo",
    "synth", "orbit", "warp", "flux", "grid", "spark", "blaze", "storm", "drift",
    "echo", "prism", "surge", "phantom", "chrome", "hologram", "cipher", "nova",
    "zenith", "omega", "alpha", "delta", "sigma", "theta", "gamma", "epsilon",
    "python", "django", "flask", "react", "swift", "kotlin", "neural", "tensor",
    "rocket", "comet", "nebula", "quasar", "pulsar", "cosmos", "astral", "lunar",
    "sonic", "hyper", "ultra", "mega", "giga", "nano", "micro", "macro",
    "the", "and", "for", "are", "but", "not", "you", "all", "can", "her",
    "was", "one", "our", "out", "day", "get", "has", "him", "his", "how",
    "its", "may", "new", "now", "old", "see", "way", "who", "did", "let",
    "say", "she", "too", "use", "run", "fly", "sky", "big", "red", "blue",
    "fast", "code", "data", "fire", "wave", "dark", "star", "moon", "gold",
    "rise", "fall", "jump", "dash", "glow", "fade", "spin", "beam", "edge",
    "loop", "node", "core", "chip", "byte", "link", "sync", "hack", "boot",
    "render", "compile", "execute", "debug", "deploy", "iterate", "refactor",
    "algorithm", "framework", "interface", "protocol", "database", "pipeline",
    "function", "variable", "constant", "operator", "sequence", "parallel",
    "spectrum", "frequency", "amplitude", "resonance", "velocity", "momentum"
]

SENTENCES_POOL = [
    "the quick brown fox jumps over the lazy dog",
    "neon lights flicker in the cyberpunk cityscape",
    "quantum algorithms process data at light speed",
    "pixels dance across the glowing arcade screen",
    "binary stars orbit in the vast cosmic void",
    "electric pulses surge through the neural network",
    "holographic displays shimmer with vibrant colors",
    "the matrix unfolds infinite digital landscapes",
    "plasma waves ripple across the dark horizon",
    "virtual reality blurs the line between worlds",
    "photon beams pierce through the crystal prism",
    "synthetic melodies echo in the neon corridor",
    "gravity bends time in the quantum realm",
    "laser grids protect the ancient data vault",
    "turbo engines ignite beneath the chrome hull",
    "code compiles flawlessly on the first attempt",
    "starlight reflects off the orbital station",
    "warp drives fold spacetime like origami",
    "the cipher unlocks secrets of the cosmos",
    "parallel threads weave through the processor",
]


# ═══════════════════════════════════════════════════════════
#  MAIN MENU  (10 Games with scrolling + page system)
# ═══════════════════════════════════════════════════════════
def main_menu():
    games = [
        {"name": "GRAVITY FLUX",    "desc": "Flip gravity to survive platforms",      "icon": "▲▼",  "color": NEON_PINK},
        {"name": "CHROMATIC HUNT",   "desc": "Click the correct color targets",       "icon": "◉◎",  "color": NEON_BLUE},
        {"name": "ORBIT DEFENDER",   "desc": "Defend your core from space threats",    "icon": "◎⊕",  "color": NEON_GREEN},
        {"name": "PIXEL SNAKE",      "desc": "Neon snake with rainbow powerups",      "icon": "≋≋",  "color": NEON_PURPLE},
        {"name": "MEMORY MATRIX",    "desc": "Memorize and recall the pattern",       "icon": "▦▣",  "color": NEON_ORANGE},
        {"name": "REACTION BLITZ",   "desc": "Test your reaction time in ms",         "icon": "⚡",  "color": NEON_YELLOW},
        {"name": "NEON TYPER",       "desc": "Typing speed & accuracy challenge",     "icon": "⌨▮",  "color": NEON_CYAN},
        {"name": "ASTEROID DODGE",   "desc": "Weave through deadly asteroid fields",  "icon": "✦☄",  "color": NEON_RED},
        {"name": "BOUNCE WARS",      "desc": "Pong with powerups and chaos",          "icon": "◆◇",  "color": NEON_LIME},
        {"name": "RHYTHM PULSE",     "desc": "Hit the beats in the rhythm lane",      "icon": "♫♪",  "color": NEON_MAGENTA},
    ]

    selected = 0
    t = 0
    particles = []
    stars = make_stars(100)
    scroll_y = 0
    target_scroll = 0

    while True:
        dt = clock.tick(60) / 1000.0
        t += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 10
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 10
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return selected
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i in range(10):
                    card_y = 195 + i * 52 - scroll_y
                    if 180 < mx < 920 and card_y < my < card_y + 46:
                        return i
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                for i in range(10):
                    card_y = 195 + i * 52 - scroll_y
                    if 180 < mx < 920 and card_y < my < card_y + 46:
                        selected = i

        # Auto-scroll to keep selected visible
        card_top = 195 + selected * 52 - scroll_y
        if card_top < 180:
            target_scroll = max(0, scroll_y - 52)
        elif card_top + 52 > HEIGHT - 40:
            target_scroll = scroll_y + 52
        scroll_y += (target_scroll - scroll_y) * 0.15

        # ─── DRAW ───
        draw_grid_bg()
        draw_stars(stars, t)

        # Title
        tc = pulse_color(NEON_CYAN, t, 2, 35)
        draw_text_centered("⚡ NEON ARCADE ULTIMATE ⚡", font_title, tc, 55)

        # Subtitle lines
        sub_c = pulse_color((80, 80, 130), t, 1.5, 25)
        draw_text_centered("10 GAMES  •  USE ↑↓ + ENTER  •  CLICK TO PLAY", font_tiny, sub_c, 95)

        # Decorative animated lines
        lx = int(180 + 80 * math.sin(t * 1.2))
        pygame.draw.line(screen, (*NEON_CYAN[:3],), (lx, 115), (WIDTH - lx, 115), 1)
        pygame.draw.line(screen, (*NEON_PINK[:3],), (lx + 15, 119), (WIDTH - lx - 15, 119), 1)

        # Clipping region for cards
        clip_rect = pygame.Rect(0, 130, WIDTH, HEIGHT - 170)
        screen.set_clip(clip_rect)

        # Game cards
        for i, game in enumerate(games):
            card_y = 195 + i * 52 - int(scroll_y)
            if card_y < 120 or card_y > HEIGHT - 10:
                continue

            is_sel = i == selected
            card_rect = (185, card_y, 730, 46)

            if is_sel:
                # Glow bg
                gs = pygame.Surface((750, 56), pygame.SRCALPHA)
                pygame.draw.rect(gs, (*game['color'][:3], 22), (0, 0, 750, 56), border_radius=10)
                screen.blit(gs, (180, card_y - 5))

                bc = pulse_color(game['color'], t, 5, 40)
                pygame.draw.rect(screen, bc, card_rect, 2, border_radius=7)

                # Animated arrow
                ao = int(3 * math.sin(t * 7))
                draw_text("►", font_medium, game['color'], 190 + ao, card_y + 10)

                # Selection dot
                glow_circle(screen, game['color'], (175, card_y + 23), 4)
            else:
                pygame.draw.rect(screen, (28, 28, 55), card_rect, 1, border_radius=7)

            nc = game['color'] if is_sel else (100, 100, 140)
            draw_text(game['icon'], font_game, game['color'], 215, card_y + 12)
            draw_text(game['name'], font_medium if is_sel else font_small, nc, 260, card_y + (10 if is_sel else 13))
            draw_text(game['desc'], font_tiny, (70, 70, 100), 460, card_y + 17)

            # Number circle
            badge_c = game['color'] if is_sel else (35, 35, 60)
            bx = 895
            pygame.draw.circle(screen, badge_c, (bx, card_y + 23), 14, 2 if not is_sel else 0)
            num_c = BLACK if is_sel else badge_c
            draw_text_centered(str(i + 1), font_tiny, num_c, card_y + 23, x=bx)

        screen.set_clip(None)

        # Scroll indicator
        total_h = 10 * 52
        visible_h = HEIGHT - 200
        if total_h > visible_h:
            bar_h = max(30, int(visible_h * (visible_h / total_h)))
            bar_y = int(135 + (scroll_y / max(1, total_h - visible_h)) * (visible_h - bar_h))
            pygame.draw.rect(screen, (40, 40, 70), (WIDTH - 20, 135, 6, visible_h), border_radius=3)
            pygame.draw.rect(screen, NEON_CYAN, (WIDTH - 20, bar_y, 6, bar_h), border_radius=3)

        # Footer
        draw_text_centered("ESC to quit  •  MOUSE or KEYBOARD  •  R to restart in-game",
                           font_tiny, (50, 50, 75), HEIGHT - 22)

        # Ambient particles
        update_particles(particles)
        if random.random() < 0.06:
            particle_burst(particles, random.randint(0, WIDTH),
                           random.randint(0, HEIGHT), random.choice(ALL_NEONS), 2)

        draw_scanlines(6)
        pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 1: GRAVITY FLUX
# ═══════════════════════════════════════════════════════════
def game_gravity_flux():
    px, py = 100, HEIGHT // 2
    pw, ph = 22, 22
    vy = 0
    gravity = 0.45
    gdir = 1
    speed = 4.5
    score = 0
    particles = []
    t = 0
    trail = deque(maxlen=25)
    camera_x = 0
    alive = True
    flip_cd = 0

    platforms = []
    for i in range(20):
        platforms.append({'x': 150 + i * 140, 'y': random.randint(140, HEIGHT - 140),
                          'w': random.randint(70, 170), 'h': 10,
                          'color': random.choice(ALL_NEONS)})

    orbs = []
    for i in range(12):
        orbs.append({'x': random.randint(200, 2500), 'y': random.randint(80, HEIGHT - 80), 'collected': False,
                     'pulse': random.uniform(0, 6.28)})

    while True:
        dt = clock.tick(60) / 1000.0
        t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_SPACE and flip_cd <= 0 and alive:
                    gdir *= -1; vy = -3.5 * gdir; flip_cd = 0.25
                    particle_burst(particles, int(px - camera_x), int(py),
                                   NEON_PINK if gdir == 1 else NEON_BLUE, 20)
                if event.key == pygame.K_r and not alive:
                    return game_gravity_flux()

        if not alive:
            game_over_screen("GRAVITY FLUX", [(f"Score: {score}", NEON_YELLOW)], particles)
            continue

        flip_cd -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: px += speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: px -= speed

        vy += gravity * gdir
        vy = max(-11, min(11, vy))
        py += vy

        for p in platforms:
            if px + pw > p['x'] and px < p['x'] + p['w']:
                if gdir == 1 and py + ph >= p['y'] and py + ph <= p['y'] + 18 and vy > 0:
                    py = p['y'] - ph; vy = 0
                elif gdir == -1 and py <= p['y'] + p['h'] and py >= p['y'] - 10 and vy < 0:
                    py = p['y'] + p['h']; vy = 0

        if py < -60 or py > HEIGHT + 60: alive = False

        for orb in orbs:
            if not orb['collected'] and math.hypot(px + 11 - orb['x'], py + 11 - orb['y']) < 25:
                orb['collected'] = True; score += 100
                particle_burst(particles, int(orb['x'] - camera_x), int(orb['y']), NEON_YELLOW, 25)

        camera_x = px - 200
        trail.append((px, py, gdir))

        mx = max(p['x'] for p in platforms)
        while mx - camera_x < WIDTH + 300:
            mx += random.randint(90, 190)
            platforms.append({'x': mx, 'y': random.randint(140, HEIGHT - 140),
                              'w': random.randint(70, 170), 'h': 10, 'color': random.choice(ALL_NEONS)})
            if random.random() < 0.4:
                orbs.append({'x': mx + 50, 'y': random.randint(80, HEIGHT - 80),
                             'collected': False, 'pulse': random.uniform(0, 6.28)})
        score += 1

        # DRAW
        draw_grid_bg()
        for i, (tx, ty, td) in enumerate(trail):
            a = i / len(trail)
            c = NEON_PINK if td == 1 else NEON_BLUE
            tc2 = tuple(int(ch * a * 0.5) for ch in c)
            pygame.draw.circle(screen, tc2, (int(tx - camera_x + 11), int(ty + 11)), int(3 + a * 7))

        for p in platforms:
            sx = p['x'] - camera_x
            if -200 < sx < WIDTH + 200:
                gs = pygame.Surface((p['w'] + 8, 18), pygame.SRCALPHA)
                pygame.draw.rect(gs, (*p['color'][:3], 35), (0, 0, p['w'] + 8, 18), border_radius=4)
                screen.blit(gs, (sx - 4, p['y'] - 4))
                pygame.draw.rect(screen, p['color'], (sx, p['y'], p['w'], p['h']), border_radius=3)

        for orb in orbs:
            if not orb['collected']:
                sx = orb['x'] - camera_x
                if -50 < sx < WIDTH + 50:
                    ps = 8 + 3 * math.sin(t * 4 + orb['pulse'])
                    glow_circle(screen, NEON_YELLOW, (int(sx), int(orb['y'])), int(ps))

        psx = int(px - camera_x)
        pc = NEON_PINK if gdir == 1 else NEON_BLUE
        glow_circle(screen, pc, (psx + 11, int(py) + 11), 13)
        ao = int(4 * math.sin(t * 7))
        if gdir == 1:
            pygame.draw.polygon(screen, pc, [(psx+11, int(py)-8+ao), (psx+5, int(py)-2+ao), (psx+17, int(py)-2+ao)])
        else:
            pygame.draw.polygon(screen, pc, [(psx+11, int(py)+ph+8-ao), (psx+5, int(py)+ph+2-ao), (psx+17, int(py)+ph+2-ao)])

        draw_hud_bg()
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 20, 12)
        gt = "▼ DOWN" if gdir == 1 else "▲ UP"
        gc = NEON_PINK if gdir == 1 else NEON_BLUE
        draw_text(f"GRAVITY: {gt}", font_game, gc, WIDTH - 230, 12)
        draw_text("[SPACE] Flip  [A/D] Move  [ESC] Menu", font_tiny, (80, 80, 120), WIDTH//2-150, 14)

        update_particles(particles)
        draw_scanlines(5)
        pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 2: CHROMATIC HUNT
# ═══════════════════════════════════════════════════════════
def game_chromatic_hunt():
    color_pool = [(NEON_PINK,"PINK"),(NEON_BLUE,"BLUE"),(NEON_GREEN,"GREEN"),
                  (NEON_PURPLE,"PURPLE"),(NEON_ORANGE,"ORANGE"),(NEON_YELLOW,"YELLOW")]
    score = 0; lives = 5; level = 1; t = 0; particles = []; targets = []
    target_idx = 0; combo = 0; max_combo = 0; time_left = 30.0; active = True; spawn_t = 0

    def spawn():
        targets.append({'x': random.randint(50, WIDTH-50), 'y': random.randint(80, HEIGHT-80),
                        'size': random.randint(22, 48), 'ci': random.randint(0, len(color_pool)-1),
                        'life': random.uniform(2.0, max(1.2, 4.0-level*0.2)),
                        'ml': random.uniform(2.0, 4.0), 'vx': random.uniform(-1,1)*level,
                        'vy': random.uniform(-1,1)*level})
    def new_round():
        nonlocal target_idx, targets, spawn_t
        target_idx = random.randint(0, len(color_pool)-1); targets.clear()
        for _ in range(5+level*2): spawn()
        spawn_t = 0
    new_round()

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and not active: return game_chromatic_hunt()
            if event.type == pygame.MOUSEBUTTONDOWN and active:
                mx, my = event.pos
                for tg in targets[:]:
                    if math.hypot(mx-tg['x'], my-tg['y']) < tg['size']:
                        if tg['ci'] == target_idx:
                            score += 50*(1+combo); combo += 1; max_combo = max(max_combo, combo)
                            particle_burst(particles, int(tg['x']), int(tg['y']), color_pool[tg['ci']][0], 20)
                        else:
                            lives -= 1; combo = 0
                            particle_burst(particles, int(tg['x']), int(tg['y']), NEON_RED, 15)
                            if lives <= 0: active = False
                        targets.remove(tg); break

        if active:
            time_left -= dt
            if time_left <= 0: level += 1; time_left = 30.0; new_round()
            spawn_t += dt
            if spawn_t > max(0.4, 2.0-level*0.12): spawn(); spawn_t = 0
            for tg in targets[:]:
                tg['life'] -= dt; tg['x'] += tg['vx']; tg['y'] += tg['vy']
                if tg['x'] < 20 or tg['x'] > WIDTH-20: tg['vx'] *= -1
                if tg['y'] < 65 or tg['y'] > HEIGHT-20: tg['vy'] *= -1
                if tg['life'] <= 0: targets.remove(tg)

        draw_grid_bg()
        if not active:
            game_over_screen("GAME OVER", [(f"Score: {score}", NEON_YELLOW),
                                           (f"Max Combo: {max_combo}x", NEON_GREEN)], particles)
            continue

        draw_hud_bg(55)
        tc, tn = color_pool[target_idx]
        draw_text("HUNT:", font_game, WHITE, 20, 8)
        pygame.draw.circle(screen, pulse_color(tc, t, 5, 40), (95, 18), 12)
        draw_text(tn, font_subtitle, pulse_color(tc, t, 5, 40), 115, 2)
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 320, 8)
        draw_text(f"COMBO: {combo}x", font_game, NEON_GREEN if combo else (70,70,70), 500, 8)
        draw_text(f"LVL {level}", font_game, NEON_PURPLE, 670, 8)
        for i in range(5):
            pygame.draw.circle(screen, NEON_RED if i < lives else (35,35,35), (800+i*22, 18), 7)
        draw_hud_bar(20, 42, WIDTH-40, 7, time_left/30.0,
                     NEON_GREEN if time_left > 10 else NEON_ORANGE if time_left > 5 else NEON_RED)

        for tg in targets:
            c = color_pool[tg['ci']][0]; lr = tg['life']/tg['ml']; sz = int(tg['size']*(0.5+0.5*lr))
            if tg['ci'] == target_idx:
                glow_circle(screen, c, (int(tg['x']), int(tg['y'])), sz+2)
            else:
                pygame.draw.circle(screen, c, (int(tg['x']), int(tg['y'])), sz)
                pygame.draw.circle(screen, c, (int(tg['x']), int(tg['y'])), sz, 2)
            a = lr * math.pi * 2
            if a > 0.1:
                pygame.draw.arc(screen, WHITE, (int(tg['x']-sz-4), int(tg['y']-sz-4), (sz+4)*2, (sz+4)*2),
                                -math.pi/2, -math.pi/2+a, 2)

        update_particles(particles); draw_scanlines(5); pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 3: ORBIT DEFENDER
# ═══════════════════════════════════════════════════════════
def game_orbit_defender():
    cx, cy = WIDTH//2, HEIGHT//2; orad = 130; pangle = 0; pspeed = 3.8
    score = 0; lives = 3; t = 0; particles = []; bullets = []; enemies = []
    wave = 1; spawn_t = 0; active = True; shield = 100

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_SPACE and active:
                    bx = cx + math.cos(pangle)*orad; by = cy + math.sin(pangle)*orad
                    bullets.append({'x':bx,'y':by,'vx':math.cos(pangle)*9,'vy':math.sin(pangle)*9,'life':55})
                if event.key == pygame.K_r and not active: return game_orbit_defender()

        if not active:
            game_over_screen("CORE DESTROYED", [(f"Score: {score}", NEON_YELLOW),
                                                 (f"Wave: {wave}", NEON_GREEN)], particles)
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: pangle -= pspeed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: pangle += pspeed * dt

        spawn_t += dt
        sr = max(0.25, 1.8 - wave*0.12)
        if spawn_t > sr:
            a = random.uniform(0, math.pi*2); d = 420+random.randint(0,80)
            et = random.choice(['n','n','f','b'])
            enemies.append({'x':cx+math.cos(a)*d,'y':cy+math.sin(a)*d,
                            'speed':(0.9+wave*0.12)*(1.5 if et=='f' else 0.55 if et=='b' else 1),
                            'type':et,'hp':1 if et!='b' else 3,'size':8 if et=='f' else 20 if et=='b' else 12})
            spawn_t = 0

        for b in bullets[:]:
            b['x']+=b['vx']; b['y']+=b['vy']; b['life']-=1
            if b['life']<=0: bullets.remove(b)

        for e in enemies[:]:
            dx,dy = cx-e['x'], cy-e['y']; d = math.hypot(dx,dy)
            if d > 0: e['x']+=(dx/d)*e['speed']; e['y']+=(dy/d)*e['speed']
            if d < 28:
                shield -= 20; enemies.remove(e)
                particle_burst(particles, int(e['x']), int(e['y']), NEON_RED, 15)
                if shield <= 0: lives -= 1; shield = 100
                if lives <= 0: active = False
                continue
            for b in bullets[:]:
                if math.hypot(b['x']-e['x'],b['y']-e['y']) < e['size']+5:
                    e['hp']-=1
                    if b in bullets: bullets.remove(b)
                    if e['hp']<=0:
                        score += 10*(3 if e['type']=='b' else 2 if e['type']=='f' else 1)
                        ec = NEON_GREEN if e['type']=='n' else NEON_ORANGE if e['type']=='f' else NEON_PURPLE
                        particle_burst(particles, int(e['x']), int(e['y']), ec, 20)
                        if e in enemies: enemies.remove(e)
                    break
        if score > wave*250: wave += 1

        # DRAW
        draw_grid_bg()
        rc = pulse_color((35,35,70), t, 2, 15)
        pygame.draw.circle(screen, rc, (cx, cy), orad, 1)
        glow_circle(screen, pulse_color(NEON_BLUE, t, 3, 25), (cx, cy), 24)
        sa = (shield/100)*math.pi*2
        if sa > 0.1:
            sc2 = NEON_GREEN if shield > 50 else NEON_ORANGE if shield > 25 else NEON_RED
            pygame.draw.arc(screen, sc2, (cx-34, cy-34, 68, 68), -math.pi/2, -math.pi/2+sa, 3)

        ppx = int(cx+math.cos(pangle)*orad); ppy = int(cy+math.sin(pangle)*orad)
        glow_circle(screen, NEON_PINK, (ppx, ppy), 11)
        ax = int(ppx+math.cos(pangle)*28); ay = int(ppy+math.sin(pangle)*28)
        pygame.draw.line(screen, NEON_PINK, (ppx, ppy), (ax, ay), 2)

        for b in bullets:
            pygame.draw.circle(screen, NEON_YELLOW, (int(b['x']),int(b['y'])), 4)
        for e in enemies:
            ec2 = NEON_RED if e['type']=='n' else NEON_ORANGE if e['type']=='f' else NEON_PURPLE
            pygame.draw.circle(screen, ec2, (int(e['x']),int(e['y'])), e['size'])
            pygame.draw.circle(screen, WHITE, (int(e['x']),int(e['y'])), e['size'], 1)
            if e['type']=='b':
                draw_text_centered(str(e['hp']), font_tiny, WHITE, int(e['y']), x=int(e['x']))

        draw_hud_bg()
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 20, 12)
        draw_text(f"WAVE: {wave}", font_game, NEON_GREEN, 200, 12)
        draw_text(f"SHIELD: {shield}%", font_game, NEON_GREEN if shield>50 else NEON_RED, 360, 12)
        for i in range(3):
            pygame.draw.circle(screen, NEON_PINK if i<lives else (35,35,35), (WIDTH-70+i*22, 22), 7)
        draw_text("[←→] Orbit [SPACE] Shoot", font_tiny, (80,80,120), 560, 14)

        update_particles(particles); draw_scanlines(5); pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 4: PIXEL SNAKE RAVE
# ═══════════════════════════════════════════════════════════
def game_pixel_snake():
    CELL = 20; COLS = WIDTH//CELL; ROWS = (HEIGHT-55)//CELL
    snake = deque([(COLS//2, ROWS//2)]); dir_ = (1,0); ndir = (1,0)
    score = 0; t = 0; particles = []; active = True
    mt = 0; ms = 0.1; rainbow = False; rt = 0

    def place_food():
        while True:
            f = (random.randint(0,COLS-1), random.randint(0,ROWS-1))
            if f not in snake:
                return {'x':f[0],'y':f[1],'type':random.choice(['n','n','n','r','s']),'p':0}
    food = place_food()

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and not active: return game_pixel_snake()
                if event.key in (pygame.K_UP,pygame.K_w) and dir_!=(0,1): ndir=(0,-1)
                if event.key in (pygame.K_DOWN,pygame.K_s) and dir_!=(0,-1): ndir=(0,1)
                if event.key in (pygame.K_LEFT,pygame.K_a) and dir_!=(1,0): ndir=(-1,0)
                if event.key in (pygame.K_RIGHT,pygame.K_d) and dir_!=(-1,0): ndir=(1,0)

        if not active:
            game_over_screen("SNAKE CRASHED", [(f"Score: {score}", NEON_YELLOW),
                                                (f"Length: {len(snake)}", NEON_GREEN)], particles)
            continue

        if rainbow: rt -= dt
        if rt <= 0: rainbow = False

        mt += dt
        if mt >= ms:
            mt = 0; dir_ = ndir; h = snake[0]
            nh = ((h[0]+dir_[0])%COLS, (h[1]+dir_[1])%ROWS)
            if nh in snake:
                active = False
                particle_burst(particles, nh[0]*CELL+CELL//2, nh[1]*CELL+55+CELL//2, NEON_RED, 30)
            else:
                snake.appendleft(nh)
                if nh == (food['x'], food['y']):
                    if food['type']=='r': rainbow=True; rt=5.0; score+=50
                    elif food['type']=='s': ms=max(0.04,ms-0.008); score+=30
                    else: score+=10
                    particle_burst(particles, food['x']*CELL+CELL//2, food['y']*CELL+55+CELL//2, NEON_YELLOW, 15)
                    food = place_food()
                else:
                    snake.pop()

        draw_grid_bg()
        for i, (sx,sy) in enumerate(snake):
            r = 1-(i/max(len(snake),1))
            if rainbow:
                c = hsv_to_rgb((t*200+i*30)%360, 100, 100)
            else:
                c = (int(NEON_GREEN[0]*r), int(NEON_GREEN[1]*(0.5+r*0.5)), int(NEON_GREEN[2]*r))
            rect = (sx*CELL+1, sy*CELL+56, CELL-2, CELL-2)
            pygame.draw.rect(screen, c, rect, border_radius=4)
            if i==0:
                gs = pygame.Surface((CELL+8, CELL+8), pygame.SRCALPHA)
                pygame.draw.rect(gs, (*c[:3], 50), (0, 0, CELL+8, CELL+8), border_radius=5)
                screen.blit(gs, (sx*CELL-3, sy*CELL+52))

        fx, fy = food['x']*CELL+CELL//2, food['y']*CELL+55+CELL//2
        fp = 8+3*math.sin(t*5)
        if food['type']=='r': fc = hsv_to_rgb((t*150)%360, 100, 100)
        elif food['type']=='s': fc = NEON_ORANGE
        else: fc = NEON_YELLOW
        glow_circle(screen, fc, (fx, fy), int(fp))

        draw_hud_bg(50)
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 20, 8)
        draw_text(f"LENGTH: {len(snake)}", font_game, NEON_GREEN, 180, 8)
        draw_text(f"SPEED: {int(1/ms)}", font_game, NEON_ORANGE, 370, 8)
        if rainbow:
            draw_text(f"★ RAINBOW {rt:.1f}s ★", font_game, pulse_color(NEON_PINK,t,8,50), 530, 8)
        draw_text("[WASD] Move", font_tiny, (80,80,120), 20, 32)

        update_particles(particles); draw_scanlines(5); pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 5: MEMORY MATRIX
# ═══════════════════════════════════════════════════════════
def game_memory_matrix():
    level = 1; score = 0; t = 0; particles = []; lives = 3
    pattern = []; player_in = []; phase = 'show'; show_t = 0; result_t = 0; success = False
    gs = 4; cell_c = {}

    def new_pat():
        nonlocal pattern, player_in, phase, show_t, gs, cell_c
        gs = min(4+level//3, 7); cnt = min(3+level, gs*gs-1)
        pattern = random.sample([(r,c) for r in range(gs) for c in range(gs)], cnt)
        player_in = []; phase = 'show'; show_t = max(1.0, 3.0-level*0.12)
        cell_c = {p: random.choice(ALL_NEONS) for p in pattern}
    new_pat()

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and lives<=0: return game_memory_matrix()
            if event.type == pygame.MOUSEBUTTONDOWN and phase == 'input':
                mx, my = event.pos
                cs2 = 78 if gs<=5 else 60
                ox = (WIDTH-gs*(cs2+6))//2; oy = 145
                for r in range(gs):
                    for c in range(gs):
                        cx2 = ox+c*(cs2+6); cy2 = oy+r*(cs2+6)
                        if cx2<mx<cx2+cs2 and cy2<my<cy2+cs2:
                            cell = (r,c)
                            if cell not in player_in:
                                player_in.append(cell)
                                if cell in pattern:
                                    particle_burst(particles, cx2+cs2//2, cy2+cs2//2, NEON_GREEN, 10)
                                else:
                                    particle_burst(particles, cx2+cs2//2, cy2+cs2//2, NEON_RED, 10)
                                    phase='result'; success=False; result_t=2.0; lives-=1
                                if len([p for p in player_in if p in pattern])==len(pattern):
                                    phase='result'; success=True; result_t=1.5; score+=level*50

        if phase=='show':
            show_t -= dt
            if show_t<=0: phase='input'
        if phase=='result':
            result_t -= dt
            if result_t<=0:
                if lives<=0: phase='over'
                elif success: level+=1; new_pat()
                else: new_pat()

        draw_grid_bg()
        cs2 = 78 if gs<=5 else 60
        ox = (WIDTH-gs*(cs2+6))//2; oy = 145

        draw_hud_bg(50)
        draw_text(f"LVL: {level}", font_game, NEON_PURPLE, 20, 8)
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 160, 8)
        draw_text(f"GRID: {gs}×{gs}", font_game, NEON_BLUE, 340, 8)
        draw_text(f"CELLS: {len(pattern)}", font_game, NEON_GREEN, 500, 8)
        for i in range(3):
            pygame.draw.circle(screen, NEON_PINK if i<lives else (35,35,35), (WIDTH-70+i*22, 25), 7)

        if phase=='over':
            game_over_screen("MEMORY OVERLOAD", [(f"Score: {score}", NEON_YELLOW),
                                                  (f"Level: {level}", NEON_GREEN)], particles)
            continue

        if phase=='show':
            bw = int((show_t/max(1,3-level*0.12))*300)
            draw_text_centered("MEMORIZE THE PATTERN", font_subtitle, pulse_color(NEON_YELLOW,t,5,40), 90)
            draw_hud_bar(WIDTH//2-150, 115, 300, 8, show_t/max(1,3-level*0.12), NEON_YELLOW)
        elif phase=='input':
            found = len([p for p in player_in if p in pattern])
            draw_text_centered(f"CLICK THE CELLS ({found}/{len(pattern)})", font_subtitle, NEON_BLUE, 95)
        elif phase=='result':
            draw_text_centered("✓ PERFECT!" if success else "✗ WRONG!", font_subtitle,
                               NEON_GREEN if success else NEON_RED, 95)

        for r in range(gs):
            for c in range(gs):
                cx2=ox+c*(cs2+6); cy2=oy+r*(cs2+6); cell=(r,c)
                ip = cell in pattern; ic = cell in player_in
                if phase=='show' and ip:
                    cc = pulse_color(cell_c.get(cell, NEON_BLUE), t, 4, 30)
                    pygame.draw.rect(screen, cc, (cx2,cy2,cs2,cs2), border_radius=8)
                elif phase=='input':
                    if ic and ip: pygame.draw.rect(screen, NEON_GREEN, (cx2,cy2,cs2,cs2), border_radius=8)
                    elif ic: pygame.draw.rect(screen, NEON_RED, (cx2,cy2,cs2,cs2), border_radius=8)
                    else:
                        pygame.draw.rect(screen, (22,22,45), (cx2,cy2,cs2,cs2), border_radius=8)
                        pygame.draw.rect(screen, (45,45,75), (cx2,cy2,cs2,cs2), 2, border_radius=8)
                elif phase=='result' and ip:
                    pygame.draw.rect(screen, NEON_GREEN if success else cell_c.get(cell, NEON_BLUE),
                                     (cx2,cy2,cs2,cs2), border_radius=8)
                else:
                    pygame.draw.rect(screen, (22,22,45), (cx2,cy2,cs2,cs2), border_radius=8)
                    pygame.draw.rect(screen, (45,45,75), (cx2,cy2,cs2,cs2), 2, border_radius=8)

        update_particles(particles); draw_scanlines(5); pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 6: REACTION BLITZ ⚡
# ═══════════════════════════════════════════════════════════
def game_reaction_blitz():
    """Test your reaction time across 5 rounds with visual flair."""
    t = 0; particles = []; stars = make_stars(60)
    state = 'intro'  # intro, wait, ready, too_early, result, summary
    round_num = 0; max_rounds = 5; results = []
    wait_start = 0; wait_dur = 0; flash_time = 0
    bg_color = DARK_BG; circle_size = 0

    def start_round():
        nonlocal state, wait_start, wait_dur, bg_color, circle_size
        state = 'wait'; wait_start = time.time()
        wait_dur = random.uniform(1.5, 5.0)
        bg_color = DARK_BG; circle_size = 0

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and state == 'summary': return game_reaction_blitz()

                if state == 'intro' and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    round_num = 0; results = []; start_round()

                elif state == 'wait':
                    # Clicked too early
                    state = 'too_early'

                elif state == 'ready':
                    reaction_ms = int((time.time() - flash_time) * 1000)
                    results.append(reaction_ms)
                    state = 'result'
                    particle_burst(particles, WIDTH//2, HEIGHT//2, NEON_GREEN, 40)

                elif state == 'too_early':
                    start_round()  # Retry same round

                elif state == 'result':
                    round_num += 1
                    if round_num >= max_rounds:
                        state = 'summary'
                    else:
                        start_round()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == 'intro':
                    round_num = 0; results = []; start_round()
                elif state == 'wait':
                    state = 'too_early'
                elif state == 'ready':
                    reaction_ms = int((time.time() - flash_time)*1000)
                    results.append(reaction_ms)
                    state = 'result'
                    particle_burst(particles, WIDTH//2, HEIGHT//2, NEON_GREEN, 40)
                elif state == 'too_early':
                    start_round()
                elif state == 'result':
                    round_num += 1
                    if round_num >= max_rounds: state = 'summary'
                    else: start_round()

        # State transitions
        if state == 'wait' and time.time() - wait_start >= wait_dur:
            state = 'ready'; flash_time = time.time()

        # Growing circle animation
        if state == 'ready':
            circle_size = min(350, circle_size + dt * 500)

        # ─── DRAW ───
        draw_grid_bg()
        draw_stars(stars, t)

        if state == 'intro':
            draw_text_centered("⚡ REACTION BLITZ ⚡", font_title, NEON_YELLOW, 180)
            draw_text_centered("Test your reaction speed!", font_medium, (150,150,180), 240)
            draw_text_centered("When the screen turns GREEN →", font_small, (120,120,150), 310)
            draw_text_centered("CLICK or press ANY KEY as fast as you can!", font_small, NEON_GREEN, 345)
            draw_text_centered(f"5 Rounds  •  Don't click during RED!", font_small, NEON_RED, 395)
            # Pulsing start button
            bw, bh = 260, 55
            bx, by = WIDTH//2-bw//2, 460
            bc = pulse_color(NEON_CYAN, t, 3, 40)
            draw_neon_rect(screen, bc, (bx, by, bw, bh))
            draw_text_centered("CLICK TO START", font_medium, bc, by + bh//2)

        elif state == 'wait':
            # Red pulsing screen
            elapsed = time.time() - wait_start
            pulse_v = 0.4 + 0.3 * math.sin(elapsed * 4)
            # Danger rings
            for i in range(3):
                ring_r = int(50 + elapsed * 40 + i * 80)
                if ring_r < 500:
                    alpha = max(5, int(40 - ring_r * 0.08))
                    rs = pygame.Surface((ring_r*2, ring_r*2), pygame.SRCALPHA)
                    pygame.draw.circle(rs, (255, 30, 30, alpha), (ring_r, ring_r), ring_r, 3)
                    screen.blit(rs, (WIDTH//2-ring_r, HEIGHT//2-ring_r))

            draw_text_centered("WAIT...", font_huge, pulse_color(NEON_RED, t, 6, 80), HEIGHT//2 - 30)
            draw_text_centered("Don't click yet!", font_medium, (200, 80, 80), HEIGHT//2 + 50)
            draw_text_centered(f"Round {round_num+1}/{max_rounds}", font_small, (120,120,150), HEIGHT//2 + 100)

        elif state == 'ready':
            # GREEN flash with expanding circle
            gs2 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            gs2.fill((0, 255, 50, 25))
            screen.blit(gs2, (0, 0))
            if circle_size > 5:
                glow_circle(screen, NEON_GREEN, (WIDTH//2, HEIGHT//2), int(circle_size))
            draw_text_centered("NOW!", font_mega, WHITE, HEIGHT//2 - 20)
            draw_text_centered("CLICK / PRESS ANY KEY!", font_medium, NEON_GREEN, HEIGHT//2 + 60)
            elapsed_ms = int((time.time() - flash_time)*1000)
            draw_text_centered(f"{elapsed_ms} ms", font_subtitle, (200,255,200), HEIGHT//2 + 110)

        elif state == 'too_early':
            draw_text_centered("TOO EARLY!", font_huge, NEON_ORANGE, HEIGHT//2 - 30)
            draw_text_centered("Click to try this round again", font_medium, (200,150,80), HEIGHT//2 + 50)

        elif state == 'result':
            ms = results[-1]
            if ms < 200: grade = "INSANE!"; gc = NEON_CYAN
            elif ms < 250: grade = "AMAZING!"; gc = NEON_GREEN
            elif ms < 300: grade = "GREAT!"; gc = NEON_LIME
            elif ms < 400: grade = "GOOD"; gc = NEON_YELLOW
            elif ms < 500: grade = "OK"; gc = NEON_ORANGE
            else: grade = "SLOW"; gc = NEON_RED

            draw_text_centered(f"{ms} ms", font_mega, gc, HEIGHT//2 - 50)
            draw_text_centered(grade, font_title, gc, HEIGHT//2 + 40)
            draw_text_centered(f"Round {round_num+1}/{max_rounds}  •  Click for next",
                               font_small, (150,150,180), HEIGHT//2 + 100)

            # Mini results bar
            for i, r in enumerate(results):
                bx = WIDTH//2 - len(results)*30//2 + i*30
                bh2 = min(80, r // 4)
                bc2 = NEON_GREEN if r<250 else NEON_YELLOW if r<400 else NEON_RED
                pygame.draw.rect(screen, bc2, (bx, HEIGHT//2+140-bh2, 22, bh2), border_radius=3)
                draw_text_centered(str(i+1), font_tiny, (120,120,150), HEIGHT//2+155, x=bx+11)

        elif state == 'summary':
            avg = sum(results) // len(results)
            best = min(results)
            worst = max(results)

            if avg < 220: rating = "SUPERHUMAN"; rc = NEON_CYAN
            elif avg < 270: rating = "EXCELLENT"; rc = NEON_GREEN
            elif avg < 320: rating = "VERY GOOD"; rc = NEON_LIME
            elif avg < 400: rating = "AVERAGE"; rc = NEON_YELLOW
            elif avg < 500: rating = "BELOW AVG"; rc = NEON_ORANGE
            else: rating = "NEEDS WORK"; rc = NEON_RED

            draw_text_centered("⚡ RESULTS ⚡", font_title, NEON_YELLOW, 100)

            draw_text_centered(f"Average: {avg} ms", font_huge, rc, 210)
            draw_text_centered(rating, font_subtitle, rc, 270)

            draw_text_centered(f"Best: {best} ms  •  Worst: {worst} ms", font_medium, (170,170,200), 330)

            # Result bars
            bar_start_x = WIDTH//2 - max_rounds * 55 // 2
            for i, r in enumerate(results):
                bx2 = bar_start_x + i * 55
                bh3 = min(150, r // 3)
                bc3 = NEON_GREEN if r<250 else NEON_YELLOW if r<400 else NEON_ORANGE if r<500 else NEON_RED
                pygame.draw.rect(screen, bc3, (bx2, 480-bh3, 40, bh3), border_radius=5)
                draw_text_centered(f"{r}", font_tiny, bc3, 490, x=bx2+20)
                draw_text_centered(f"R{i+1}", font_tiny, (100,100,130), 508, x=bx2+20)

            # Percentile estimate
            if avg < 200: pct = "Top 1%"
            elif avg < 250: pct = "Top 10%"
            elif avg < 300: pct = "Top 30%"
            elif avg < 350: pct = "Top 50%"
            else: pct = "Keep practicing!"
            draw_text_centered(pct, font_medium, (140,140,170), 560)

            draw_text_centered("[R] Play Again  [ESC] Menu", font_small, (120,120,150), 620)

        update_particles(particles)
        draw_scanlines(5)
        pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 7: NEON TYPER ⌨️
# ═══════════════════════════════════════════════════════════
def game_neon_typer():
    """Full typing speed test with WPM, accuracy, and visual feedback."""
    t = 0; particles = []; stars = make_stars(50)
    state = 'mode_select'  # mode_select, countdown, playing, results
    mode = 'words'  # 'words' or 'sentences'
    duration = 30  # seconds

    text_to_type = ""
    typed_chars = []
    cursor_pos = 0
    total_correct = 0
    total_typed = 0
    start_time = 0
    time_left = 0
    wpm_history = []
    countdown_val = 3
    countdown_start = 0

    word_list = []
    current_word_idx = 0

    def generate_text():
        nonlocal text_to_type, word_list
        if mode == 'words':
            word_list = random.sample(WORD_POOL, min(60, len(WORD_POOL)))
            text_to_type = ' '.join(word_list)
        else:
            chosen = random.sample(SENTENCES_POOL, min(5, len(SENTENCES_POOL)))
            text_to_type = '  '.join(chosen)

    def reset_game():
        nonlocal typed_chars, cursor_pos, total_correct, total_typed, wpm_history
        typed_chars = []; cursor_pos = 0; total_correct = 0; total_typed = 0; wpm_history = []
        generate_text()

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return

                if state == 'mode_select':
                    if event.key == pygame.K_1: mode='words'; duration=30; state='countdown'; countdown_start=time.time(); reset_game()
                    elif event.key == pygame.K_2: mode='words'; duration=60; state='countdown'; countdown_start=time.time(); reset_game()
                    elif event.key == pygame.K_3: mode='sentences'; duration=30; state='countdown'; countdown_start=time.time(); reset_game()
                    elif event.key == pygame.K_4: mode='sentences'; duration=60; state='countdown'; countdown_start=time.time(); reset_game()

                elif state == 'playing':
                    if event.key == pygame.K_BACKSPACE:
                        if cursor_pos > 0:
                            cursor_pos -= 1
                            if typed_chars:
                                typed_chars.pop()
                    elif event.key == pygame.K_TAB:
                        pass
                    elif event.unicode and len(event.unicode) == 1 and cursor_pos < len(text_to_type):
                        ch = event.unicode
                        correct = (ch == text_to_type[cursor_pos])
                        typed_chars.append({'char': ch, 'correct': correct, 'expected': text_to_type[cursor_pos]})
                        cursor_pos += 1
                        total_typed += 1
                        if correct:
                            total_correct += 1
                            if ch == ' ':
                                particle_burst(particles, WIDTH//2, 320, NEON_BLUE, 5)
                        else:
                            particle_burst(particles, WIDTH//2, 320, NEON_RED, 8)

                elif state == 'results':
                    if event.key == pygame.K_r: return game_neon_typer()

            if event.type == pygame.MOUSEBUTTONDOWN and state == 'mode_select':
                mx, my = event.pos
                for idx, (bx, by, bw2, bh2) in enumerate([
                    (WIDTH//2-280, 340, 250, 60), (WIDTH//2+30, 340, 250, 60),
                    (WIDTH//2-280, 420, 250, 60), (WIDTH//2+30, 420, 250, 60)
                ]):
                    if bx<mx<bx+bw2 and by<my<by+bh2:
                        modes = [('words',30),('words',60),('sentences',30),('sentences',60)]
                        mode, duration = modes[idx]
                        state='countdown'; countdown_start=time.time(); reset_game()

        # Countdown
        if state == 'countdown':
            elapsed = time.time() - countdown_start
            countdown_val = 3 - int(elapsed)
            if countdown_val <= 0:
                state = 'playing'; start_time = time.time(); time_left = duration

        # Timer
        if state == 'playing':
            time_left = max(0, duration - (time.time() - start_time))
            # Track WPM over time
            elapsed = time.time() - start_time
            if elapsed > 0 and total_typed > 0:
                words = total_correct / 5
                current_wpm = int(words / (elapsed / 60))
                if len(wpm_history) == 0 or int(elapsed) > len(wpm_history):
                    wpm_history.append(current_wpm)

            if time_left <= 0:
                state = 'results'
                particle_burst(particles, WIDTH//2, HEIGHT//2, NEON_YELLOW, 40)

        # ─── DRAW ───
        draw_grid_bg()
        draw_stars(stars, t)

        if state == 'mode_select':
            draw_text_centered("⌨ NEON TYPER ⌨", font_title, NEON_CYAN, 120)
            draw_text_centered("Choose your challenge", font_medium, (150,150,180), 180)

            options = [
                ("WORDS 30s", NEON_GREEN, "1"),
                ("WORDS 60s", NEON_BLUE, "2"),
                ("SENTENCES 30s", NEON_ORANGE, "3"),
                ("SENTENCES 60s", NEON_PURPLE, "4"),
            ]
            positions = [(WIDTH//2-280, 340), (WIDTH//2+30, 340), (WIDTH//2-280, 420), (WIDTH//2+30, 420)]
            for i, ((label, color, key), (bx2,by2)) in enumerate(zip(options, positions)):
                draw_neon_rect(screen, color, (bx2, by2, 250, 60))
                draw_text_centered(f"[{key}] {label}", font_medium, color, by2+30, x=bx2+125)

            draw_text_centered("Press 1-4 or click to select", font_small, (100,100,140), 520)

        elif state == 'countdown':
            cs2 = max(0, countdown_val)
            c_colors = [NEON_RED, NEON_YELLOW, NEON_GREEN]
            cc = c_colors[min(cs2, 2)] if cs2 > 0 else NEON_GREEN
            draw_text_centered(str(max(1, cs2 + 1)), font_mega, pulse_color(cc, t, 8, 60), HEIGHT//2)
            draw_text_centered("Get ready...", font_medium, (150,150,180), HEIGHT//2 + 80)

        elif state == 'playing':
            # HUD
            draw_hud_bg(50)
            elapsed = time.time() - start_time
            words_typed = total_correct / 5
            wpm = int(words_typed / (elapsed / 60)) if elapsed > 0 else 0
            acc = int(total_correct / max(1, total_typed) * 100)

            draw_text(f"WPM: {wpm}", font_subtitle, NEON_GREEN, 30, 8)
            draw_text(f"ACC: {acc}%", font_game, NEON_CYAN if acc > 90 else NEON_YELLOW if acc > 70 else NEON_RED, 220, 14)
            tl_color = NEON_GREEN if time_left > 10 else NEON_ORANGE if time_left > 5 else NEON_RED
            draw_text(f"TIME: {int(time_left)}s", font_subtitle, tl_color, WIDTH - 200, 8)
            draw_hud_bar(400, 20, 280, 10, time_left/duration, tl_color)
            # Mode label
            draw_text(f"{'WORDS' if mode=='words' else 'SENTENCES'}  •  {duration}s",
                      font_tiny, (80,80,110), 400, 5)

            # Text display area
            text_area_y = 120
            text_area_h = 400
            # Dark panel
            panel = pygame.Surface((WIDTH-60, text_area_h), pygame.SRCALPHA)
            panel.fill((10, 10, 25, 200))
            screen.blit(panel, (30, text_area_y))
            draw_neon_rect(screen, (40, 40, 80), (30, text_area_y, WIDTH-60, text_area_h), 1)

            # Render text with coloring
            margin = 50
            line_height = 38
            x_pos = margin
            y_pos = text_area_y + 20
            chars_per_line = 0

            # Calculate visible window around cursor
            visible_start = max(0, cursor_pos - 200)
            visible_end = min(len(text_to_type), cursor_pos + 300)

            for i in range(visible_start, visible_end):
                ch = text_to_type[i]
                if ch == '\n':
                    x_pos = margin; y_pos += line_height
                    continue

                # Determine color
                if i < len(typed_chars):
                    if typed_chars[i]['correct']:
                        color = NEON_GREEN
                    else:
                        color = NEON_RED
                elif i == cursor_pos:
                    color = WHITE
                else:
                    color = (60, 60, 90)

                char_surf = font_typing.render(ch if ch != ' ' else '·', True, color)
                cw = char_surf.get_width()

                if x_pos + cw > WIDTH - margin:
                    x_pos = margin; y_pos += line_height

                if y_pos > text_area_y + text_area_h - 20:
                    break

                screen.blit(char_surf, (x_pos, y_pos))

                # Cursor
                if i == cursor_pos:
                    cursor_blink = math.sin(t * 8) > 0
                    if cursor_blink:
                        pygame.draw.rect(screen, NEON_CYAN, (x_pos, y_pos, 2, 28))

                x_pos += cw + 1

            # Progress text
            progress = cursor_pos / max(1, len(text_to_type))
            draw_text_centered(f"{cursor_pos}/{len(text_to_type)} chars  •  {int(progress*100)}%",
                               font_tiny, (80,80,120), text_area_y + text_area_h + 20)

            # Live WPM mini-graph
            if len(wpm_history) > 1:
                graph_x, graph_y, graph_w, graph_h = 30, HEIGHT - 100, WIDTH - 60, 60
                pygame.draw.rect(screen, (15, 15, 35), (graph_x, graph_y, graph_w, graph_h), border_radius=5)
                max_wpm = max(max(wpm_history), 1)
                for j in range(1, len(wpm_history)):
                    x1 = graph_x + int((j-1) / max(1, len(wpm_history)-1) * graph_w)
                    x2 = graph_x + int(j / max(1, len(wpm_history)-1) * graph_w)
                    y1 = graph_y + graph_h - int(wpm_history[j-1]/max_wpm * (graph_h-10))
                    y2 = graph_y + graph_h - int(wpm_history[j]/max_wpm * (graph_h-10))
                    pygame.draw.line(screen, NEON_GREEN, (x1,y1), (x2,y2), 2)
                draw_text("WPM", font_tiny, (60,60,90), graph_x+5, graph_y+2)

        elif state == 'results':
            elapsed = duration
            words_typed = total_correct / 5
            final_wpm = int(words_typed / (elapsed / 60)) if elapsed > 0 else 0
            final_acc = int(total_correct / max(1, total_typed) * 100)
            errors = total_typed - total_correct

            if final_wpm >= 100: rating = "LEGENDARY"; rc2 = NEON_CYAN
            elif final_wpm >= 80: rating = "BLAZING"; rc2 = NEON_GREEN
            elif final_wpm >= 60: rating = "FAST"; rc2 = NEON_LIME
            elif final_wpm >= 40: rating = "GOOD"; rc2 = NEON_YELLOW
            elif final_wpm >= 25: rating = "AVERAGE"; rc2 = NEON_ORANGE
            else: rating = "KEEP PRACTICING"; rc2 = NEON_RED

            draw_text_centered("⌨ TYPING RESULTS ⌨", font_title, NEON_CYAN, 80)

            draw_text_centered(f"{final_wpm} WPM", font_mega, rc2, 190)
            draw_text_centered(rating, font_subtitle, rc2, 255)

            # Stats grid
            stats = [
                (f"Accuracy: {final_acc}%", NEON_CYAN if final_acc>95 else NEON_YELLOW if final_acc>85 else NEON_RED),
                (f"Characters: {total_typed}", (170,170,200)),
                (f"Correct: {total_correct}", NEON_GREEN),
                (f"Errors: {errors}", NEON_RED if errors > 5 else NEON_ORANGE if errors > 0 else NEON_GREEN),
                (f"Duration: {duration}s", (170,170,200)),
                (f"Mode: {'Words' if mode=='words' else 'Sentences'}", (170,170,200)),
            ]
            for i, (txt, col) in enumerate(stats):
                row = i // 3; col_idx = i % 3
                sx = 150 + col_idx * 280
                sy = 320 + row * 40
                draw_text(txt, font_game, col, sx, sy)

            # WPM graph
            if len(wpm_history) > 1:
                gx, gy, gw, gh = 100, 430, WIDTH-200, 120
                pygame.draw.rect(screen, (15,15,35), (gx,gy,gw,gh), border_radius=8)
                draw_neon_rect(screen, (40,40,80), (gx,gy,gw,gh), 1)
                mw = max(max(wpm_history),1)
                for j in range(1, len(wpm_history)):
                    x1 = gx+int((j-1)/(len(wpm_history)-1)*gw)
                    x2 = gx+int(j/(len(wpm_history)-1)*gw)
                    y1 = gy+gh-10-int(wpm_history[j-1]/mw*(gh-20))
                    y2 = gy+gh-10-int(wpm_history[j]/mw*(gh-20))
                    pygame.draw.line(screen, NEON_GREEN, (x1,y1),(x2,y2), 2)
                    pygame.draw.circle(screen, NEON_GREEN, (x2,y2), 3)
                draw_text("WPM over time", font_tiny, (80,80,110), gx+10, gy+5)
                draw_text(f"Peak: {max(wpm_history)}", font_tiny, NEON_YELLOW, gx+gw-100, gy+5)

            draw_text_centered("[R] Play Again  [ESC] Menu", font_small, (120,120,150), HEIGHT-40)

        update_particles(particles)
        draw_scanlines(5)
        pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 8: ASTEROID DODGE
# ═══════════════════════════════════════════════════════════
def game_asteroid_dodge():
    px, py = WIDTH//2, HEIGHT - 80
    pw, ph = 18, 18
    speed = 6
    score = 0; t = 0; particles = []; active = True
    asteroids = []; spawn_t = 0; level = 1
    invuln = 0; shield_count = 0
    trail = deque(maxlen=15)

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and not active: return game_asteroid_dodge()

        if not active:
            game_over_screen("DESTROYED", [(f"Score: {score}", NEON_YELLOW),
                                            (f"Level: {level}", NEON_GREEN)], particles)
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: px = max(10, px - speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: px = min(WIDTH-10, px + speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]: py = max(50, py - speed * 0.6)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: py = min(HEIGHT-10, py + speed * 0.6)

        invuln = max(0, invuln - dt)
        trail.append((px, py))

        # Spawn asteroids
        spawn_t += dt
        sr = max(0.08, 0.5 - level * 0.03)
        if spawn_t > sr:
            sz = random.randint(8, 25 + level * 2)
            ax = random.randint(20, WIDTH - 20)
            a_speed = random.uniform(1.5, 3 + level * 0.4)
            # Some asteroids have horizontal drift
            adx = random.uniform(-1.5, 1.5)
            is_powerup = random.random() < 0.03
            asteroids.append({'x': ax, 'y': -sz, 'size': sz, 'speed': a_speed,
                              'dx': adx, 'rot': random.uniform(0, 360),
                              'rot_speed': random.uniform(-3, 3),
                              'powerup': is_powerup})
            spawn_t = 0

        # Update
        for a in asteroids[:]:
            a['y'] += a['speed']; a['x'] += a['dx']; a['rot'] += a['rot_speed']
            if a['y'] > HEIGHT + 50:
                asteroids.remove(a); score += 1
                continue
            # Collision
            if not a['powerup'] and invuln <= 0:
                if math.hypot(px - a['x'], py - a['y']) < a['size'] + 10:
                    if shield_count > 0:
                        shield_count -= 1; asteroids.remove(a)
                        particle_burst(particles, int(a['x']), int(a['y']), NEON_BLUE, 20)
                    else:
                        active = False
                        particle_burst(particles, int(px), int(py), NEON_RED, 40)
            elif a['powerup']:
                if math.hypot(px-a['x'], py-a['y']) < a['size'] + 15:
                    shield_count += 1; asteroids.remove(a)
                    particle_burst(particles, int(a['x']), int(a['y']), NEON_CYAN, 25)
                    invuln = 0.5

        level = 1 + score // 50

        # DRAW
        draw_grid_bg()

        # Trail
        for i, (tx2, ty2) in enumerate(trail):
            a = i / max(len(trail), 1) * 0.4
            c2 = tuple(int(ch * a) for ch in NEON_CYAN)
            pygame.draw.circle(screen, c2, (int(tx2), int(ty2)), int(3 + a * 5))

        # Asteroids
        for a in asteroids:
            if a['powerup']:
                glow_circle(screen, NEON_CYAN, (int(a['x']), int(a['y'])), a['size'])
                draw_text_centered("S", font_tiny, WHITE, int(a['y']), x=int(a['x']))
            else:
                # Rotate-draw asteroid
                pts = []
                for j in range(6):
                    ang = a['rot'] + j * (math.pi * 2 / 6)
                    r2 = a['size'] * (0.7 + 0.3 * math.sin(j * 2.5))
                    pts.append((int(a['x'] + math.cos(ang)*r2), int(a['y'] + math.sin(ang)*r2)))
                pygame.draw.polygon(screen, (150, 120, 80), pts)
                pygame.draw.polygon(screen, (200, 170, 100), pts, 2)

        # Player
        if invuln > 0 and int(t * 15) % 2 == 0:
            pass  # Blink
        else:
            glow_circle(screen, NEON_CYAN, (int(px), int(py)), 12)
            if shield_count > 0:
                pygame.draw.circle(screen, (*NEON_BLUE[:3],), (int(px), int(py)), 20, 2)

        # HUD
        draw_hud_bg()
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 20, 12)
        draw_text(f"LVL: {level}", font_game, NEON_GREEN, 200, 12)
        draw_text(f"SHIELDS: {shield_count}", font_game, NEON_CYAN, 350, 12)
        draw_text("[WASD/Arrows] Dodge", font_tiny, (80,80,120), WIDTH-250, 14)

        update_particles(particles); draw_scanlines(5); pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 9: BOUNCE WARS (Pong with powerups)
# ═══════════════════════════════════════════════════════════
def game_bounce_wars():
    # Player paddle
    p_y = HEIGHT//2; p_h = 90; p_w = 12; p_speed = 7
    # AI paddle
    ai_y = HEIGHT//2; ai_h = 90; ai_speed = 4.5
    # Ball
    bx, by = WIDTH//2, HEIGHT//2
    bvx, bvy = 5 * random.choice([-1, 1]), random.uniform(-3, 3)
    b_size = 8
    # Scores
    p_score = 0; ai_score = 0; max_score = 7
    t = 0; particles = []; active = True
    trail_b = deque(maxlen=20)
    # Powerups
    powerups = []; pw_timer = 0
    p_big = 0; ai_big = 0  # Big paddle timers
    speed_mult = 1

    def reset_ball(direction=1):
        nonlocal bx, by, bvx, bvy, speed_mult
        bx, by = WIDTH//2, HEIGHT//2
        bvx = 5 * direction; bvy = random.uniform(-3, 3); speed_mult = 1; trail_b.clear()

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and not active: return game_bounce_wars()

        if not active:
            winner = "YOU WIN!" if p_score >= max_score else "AI WINS!"
            wc = NEON_GREEN if p_score >= max_score else NEON_RED
            game_over_screen(winner, [(f"{p_score} - {ai_score}", NEON_YELLOW)], particles)
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]: p_y = max(50, p_y - p_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: p_y = min(HEIGHT - 10, p_y + p_speed)

        # AI
        target_y = by + bvy * 10
        if ai_y < target_y - 15: ai_y += ai_speed
        elif ai_y > target_y + 15: ai_y -= ai_speed

        # Paddle sizes
        cur_ph = p_h + (40 if p_big > 0 else 0)
        cur_ah = ai_h + (40 if ai_big > 0 else 0)
        p_big = max(0, p_big - dt); ai_big = max(0, ai_big - dt)

        # Ball
        trail_b.append((bx, by))
        bx += bvx * speed_mult; by += bvy * speed_mult

        # Top/bottom walls
        if by - b_size < 45: by = 45 + b_size; bvy = abs(bvy)
        if by + b_size > HEIGHT - 5: by = HEIGHT - 5 - b_size; bvy = -abs(bvy)

        # Player paddle
        if bx - b_size < 40 + p_w and p_y - cur_ph//2 < by < p_y + cur_ph//2 and bvx < 0:
            bvx = abs(bvx) * 1.05; bvy += (by - p_y) * 0.08
            speed_mult = min(2.5, speed_mult + 0.05)
            particle_burst(particles, 40 + p_w, int(by), NEON_GREEN, 10)

        # AI paddle
        if bx + b_size > WIDTH - 40 - p_w and ai_y - cur_ah//2 < by < ai_y + cur_ah//2 and bvx > 0:
            bvx = -abs(bvx) * 1.05; bvy += (by - ai_y) * 0.08
            speed_mult = min(2.5, speed_mult + 0.05)
            particle_burst(particles, WIDTH - 40 - p_w, int(by), NEON_RED, 10)

        # Scoring
        if bx < -20:
            ai_score += 1; particle_burst(particles, 0, int(by), NEON_RED, 25)
            if ai_score >= max_score: active = False
            else: reset_ball(1)
        if bx > WIDTH + 20:
            p_score += 1; particle_burst(particles, WIDTH, int(by), NEON_GREEN, 25)
            if p_score >= max_score: active = False
            else: reset_ball(-1)

        # Powerup spawning
        pw_timer += dt
        if pw_timer > 8 and len(powerups) < 2:
            powerups.append({'x': random.randint(200, WIDTH-200), 'y': random.randint(100, HEIGHT-100),
                             'type': random.choice(['big', 'speed']), 'life': 6})
            pw_timer = 0

        for pw in powerups[:]:
            pw['life'] -= dt
            if pw['life'] <= 0: powerups.remove(pw); continue
            if math.hypot(bx - pw['x'], by - pw['y']) < 20:
                # Who benefits? Whoever hit it last
                if bvx > 0:  # Moving toward AI = player hit
                    if pw['type'] == 'big': p_big = 8
                    else: speed_mult *= 1.5
                else:
                    if pw['type'] == 'big': ai_big = 8
                    else: speed_mult *= 1.5
                particle_burst(particles, int(pw['x']), int(pw['y']), NEON_YELLOW, 15)
                powerups.remove(pw)

        # DRAW
        draw_grid_bg()

        # Center line
        for y in range(50, HEIGHT, 20):
            pygame.draw.rect(screen, (30, 30, 60), (WIDTH//2-1, y, 2, 10))

        # Ball trail
        for i, (tx3, ty3) in enumerate(trail_b):
            a = i / max(len(trail_b), 1) * 0.6
            c3 = tuple(int(ch * a) for ch in NEON_YELLOW)
            pygame.draw.circle(screen, c3, (int(tx3), int(ty3)), int(2 + a * b_size))

        # Ball
        glow_circle(screen, NEON_YELLOW, (int(bx), int(by)), b_size)

        # Player paddle
        pc2 = NEON_GREEN
        if p_big > 0: pc2 = pulse_color(NEON_CYAN, t, 6, 40)
        pygame.draw.rect(screen, pc2, (30, int(p_y - cur_ph//2), p_w, cur_ph), border_radius=4)
        gs2 = pygame.Surface((p_w+8, cur_ph+8), pygame.SRCALPHA)
        pygame.draw.rect(gs2, (*pc2[:3], 30), (0, 0, p_w+8, cur_ph+8), border_radius=5)
        screen.blit(gs2, (26, int(p_y-cur_ph//2)-4))

        # AI paddle
        ac = NEON_RED
        if ai_big > 0: ac = pulse_color(NEON_MAGENTA, t, 6, 40)
        pygame.draw.rect(screen, ac, (WIDTH-30-p_w, int(ai_y-cur_ah//2), p_w, cur_ah), border_radius=4)

        # Powerups
        for pw in powerups:
            pc3 = NEON_CYAN if pw['type']=='big' else NEON_ORANGE
            glow_circle(screen, pc3, (int(pw['x']), int(pw['y'])), 12)
            label = "B" if pw['type']=='big' else "S"
            draw_text_centered(label, font_tiny, WHITE, int(pw['y']), x=int(pw['x']))

        # HUD
        draw_hud_bg()
        draw_text_centered(f"{p_score}  -  {ai_score}", font_subtitle, WHITE, 25)
        draw_text("YOU", font_game, NEON_GREEN, 30, 10)
        draw_text_right("CPU", font_game, NEON_RED, WIDTH-30, 10)
        draw_text_centered(f"First to {max_score}", font_tiny, (80,80,120), 42)
        spd_text = f"×{speed_mult:.1f}"
        draw_text_centered(spd_text, font_tiny, NEON_ORANGE if speed_mult>1.5 else (80,80,100), HEIGHT-20)

        update_particles(particles); draw_scanlines(5); pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  GAME 10: RHYTHM PULSE
# ═══════════════════════════════════════════════════════════
def game_rhythm_pulse():
    """Hit notes as they reach the strike zone. No audio needed - visual rhythm."""
    lanes = 4
    lane_keys = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
    lane_labels = ["D", "F", "J", "K"]
    lane_colors = [NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_YELLOW]
    lane_w = 80
    total_w = lanes * lane_w
    start_x = (WIDTH - total_w) // 2
    strike_y = HEIGHT - 120
    note_speed = 4
    score = 0; combo = 0; max_combo = 0; t = 0; particles = []; active = True
    misses = 0; max_misses = 20; hits = 0; perfects = 0; greats = 0; goods = 0

    # Generate rhythm pattern
    notes = []
    patterns = []
    bpm = 120
    beat_interval = 60 / bpm

    # Pre-generate notes for 60 seconds
    current_beat = 0
    for i in range(200):
        current_beat += beat_interval * random.choice([0.5, 0.5, 1, 1, 1, 0.25])
        lane = random.randint(0, lanes - 1)
        # Occasionally double notes
        if random.random() < 0.15 and i > 10:
            lane2 = (lane + random.randint(1, 3)) % lanes
            notes.append({'lane': lane2, 'time': current_beat, 'hit': False, 'missed': False})
        notes.append({'lane': lane, 'time': current_beat, 'hit': False, 'missed': False})

    game_start = time.time()
    lane_flash = [0] * lanes
    hit_feedback = []  # (text, color, y_offset, timer)

    while True:
        dt = clock.tick(60)/1000.0; t += dt
        elapsed = time.time() - game_start

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r and not active: return game_rhythm_pulse()

                for li, lk in enumerate(lane_keys):
                    if event.key == lk and active:
                        lane_flash[li] = 0.15
                        # Check for hit
                        best_note = None; best_dist = 999
                        for n in notes:
                            if n['lane'] == li and not n['hit'] and not n['missed']:
                                note_y = strike_y - (n['time'] - elapsed) * 300
                                dist = abs(note_y - strike_y)
                                if dist < best_dist and dist < 80:
                                    best_dist = dist; best_note = n

                        if best_note:
                            best_note['hit'] = True; hits += 1
                            nx = start_x + li * lane_w + lane_w // 2
                            if best_dist < 15:
                                score += 300; perfects += 1
                                hit_feedback.append(("PERFECT", NEON_CYAN, 0, 0.8))
                                particle_burst(particles, nx, strike_y, NEON_CYAN, 20)
                            elif best_dist < 35:
                                score += 200; greats += 1
                                hit_feedback.append(("GREAT", NEON_GREEN, 0, 0.7))
                                particle_burst(particles, nx, strike_y, NEON_GREEN, 12)
                            else:
                                score += 100; goods += 1
                                hit_feedback.append(("GOOD", NEON_YELLOW, 0, 0.6))
                                particle_burst(particles, nx, strike_y, NEON_YELLOW, 8)
                            combo += 1; max_combo = max(max_combo, combo)
                            score += combo * 5  # Combo bonus
                        else:
                            combo = 0

        if not active:
            total_notes = hits + misses
            acc = int(hits / max(1, total_notes) * 100)
            if acc >= 95: grade = "S+"; gc2 = NEON_CYAN
            elif acc >= 90: grade = "S"; gc2 = NEON_GREEN
            elif acc >= 80: grade = "A"; gc2 = NEON_LIME
            elif acc >= 70: grade = "B"; gc2 = NEON_YELLOW
            elif acc >= 60: grade = "C"; gc2 = NEON_ORANGE
            else: grade = "D"; gc2 = NEON_RED

            draw_grid_bg()
            draw_text_centered("♫ SONG COMPLETE ♫", font_title, NEON_MAGENTA, 80)
            draw_text_centered(f"Grade: {grade}", font_huge, gc2, 170)
            draw_text_centered(f"Score: {score}", font_subtitle, NEON_YELLOW, 240)
            draw_text_centered(f"Max Combo: {max_combo}x", font_medium, NEON_GREEN, 290)
            draw_text_centered(f"Perfect: {perfects}  Great: {greats}  Good: {goods}  Miss: {misses}",
                               font_game, (170,170,200), 340)
            draw_text_centered(f"Accuracy: {acc}%", font_medium,
                               NEON_GREEN if acc>90 else NEON_YELLOW if acc>70 else NEON_RED, 385)
            draw_text_centered("[R] Play Again  [ESC] Menu", font_small, (120,120,150), 450)
            update_particles(particles); draw_scanlines(5); pygame.display.flip()
            continue

        # Update lane flash
        for i in range(lanes):
            lane_flash[i] = max(0, lane_flash[i] - dt)

        # Check missed notes
        for n in notes:
            if not n['hit'] and not n['missed']:
                note_y = strike_y - (n['time'] - elapsed) * 300
                if note_y > strike_y + 60:
                    n['missed'] = True; misses += 1; combo = 0
                    hit_feedback.append(("MISS", NEON_RED, 0, 0.5))
                    if misses >= max_misses:
                        active = False

        # End condition: ran out of notes
        remaining = sum(1 for n in notes if not n['hit'] and not n['missed'])
        if remaining == 0 and elapsed > 3:
            active = False

        # Update feedback
        for fb in hit_feedback[:]:
            fb_list = list(fb)
            fb_list[2] -= dt * 60
            fb_list[3] -= dt
            hit_feedback[hit_feedback.index(fb)] = tuple(fb_list)
            if fb_list[3] <= 0:
                hit_feedback.remove(tuple(fb_list))

        # ─── DRAW ───
        draw_grid_bg()

        # Lane backgrounds
        for i in range(lanes):
            lx = start_x + i * lane_w
            # Lane bg
            ls = pygame.Surface((lane_w - 4, HEIGHT), pygame.SRCALPHA)
            ls.fill((20, 20, 40, 80))
            screen.blit(ls, (lx + 2, 0))
            # Lane border
            pygame.draw.line(screen, (35, 35, 65), (lx, 0), (lx, HEIGHT), 1)

            # Flash
            if lane_flash[i] > 0:
                fs = pygame.Surface((lane_w-4, HEIGHT), pygame.SRCALPHA)
                fa = int(lane_flash[i] / 0.15 * 40)
                fs.fill((*lane_colors[i][:3], fa))
                screen.blit(fs, (lx+2, 0))

        # Right border
        pygame.draw.line(screen, (35, 35, 65), (start_x + total_w, 0), (start_x + total_w, HEIGHT), 1)

        # Strike zone
        sz_h = 10
        for i in range(lanes):
            lx = start_x + i * lane_w
            szr = (lx + 4, strike_y - sz_h//2, lane_w - 8, sz_h)
            pygame.draw.rect(screen, (*lane_colors[i][:3],), szr, 2, border_radius=3)
            # Glow on press
            if lane_flash[i] > 0:
                pygame.draw.rect(screen, lane_colors[i], szr, border_radius=3)

        # Strike zone line
        pygame.draw.line(screen, (80, 80, 120), (start_x, strike_y), (start_x + total_w, strike_y), 1)

        # Notes
        for n in notes:
            if n['hit'] or n['missed']:
                continue
            note_y = strike_y - (n['time'] - elapsed) * 300
            if note_y < -50 or note_y > HEIGHT + 50:
                continue
            lx = start_x + n['lane'] * lane_w
            nc = lane_colors[n['lane']]
            nr = (lx + 10, int(note_y) - 10, lane_w - 20, 20)
            # Glow
            gs2 = pygame.Surface((lane_w, 36), pygame.SRCALPHA)
            pygame.draw.rect(gs2, (*nc[:3], 40), (0, 0, lane_w, 36), border_radius=8)
            screen.blit(gs2, (lx, int(note_y) - 18))
            pygame.draw.rect(screen, nc, nr, border_radius=6)
            # Inner highlight
            inner = (lx + 15, int(note_y) - 5, lane_w - 30, 10)
            pygame.draw.rect(screen, WHITE, inner, border_radius=3)

        # Key labels
        for i in range(lanes):
            lx = start_x + i * lane_w
            lc = lane_colors[i] if lane_flash[i] > 0 else (80, 80, 120)
            draw_text_centered(lane_labels[i], font_subtitle, lc, HEIGHT - 40, x=lx + lane_w//2)

        # HUD
        draw_hud_bg(50)
        draw_text(f"SCORE: {score}", font_game, NEON_YELLOW, 20, 5)
        draw_text(f"COMBO: {combo}x", font_subtitle if combo > 10 else font_game,
                  pulse_color(NEON_CYAN, t, 6, 40) if combo > 20 else NEON_GREEN if combo > 0 else (70,70,70),
                  20, 25)
        draw_text(f"MISSES: {misses}/{max_misses}", font_game,
                  NEON_RED if misses > max_misses*0.7 else NEON_ORANGE if misses > max_misses*0.4 else (120,120,150),
                  WIDTH - 220, 5)
        # Miss bar
        draw_hud_bar(WIDTH-220, 30, 180, 8, misses/max_misses,
                     NEON_RED if misses > max_misses*0.7 else NEON_ORANGE)

        acc2 = int(hits / max(1, hits+misses) * 100)
        draw_text(f"ACC: {acc2}%", font_game,
                  NEON_GREEN if acc2 > 90 else NEON_YELLOW if acc2 > 70 else NEON_RED,
                  WIDTH//2 - 40, 5)

        # Hit feedback floating text
        for fb_text, fb_color, fb_y_off, fb_timer in hit_feedback:
            fa = min(255, int(fb_timer / 0.8 * 255))
            fc2 = tuple(min(255, int(c * (fa/255))) for c in fb_color[:3])
            draw_text_centered(fb_text, font_medium, fc2, int(strike_y - 50 + fb_y_off))

        update_particles(particles)
        draw_scanlines(5)
        pygame.display.flip()


# ═══════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════
def main():
    game_funcs = [
        game_gravity_flux,
        game_chromatic_hunt,
        game_orbit_defender,
        game_pixel_snake,
        game_memory_matrix,
        game_reaction_blitz,
        game_neon_typer,
        game_asteroid_dodge,
        game_bounce_wars,
        game_rhythm_pulse,
    ]

    while True:
        sel = main_menu()
        game_funcs[sel]()


if __name__ == "__main__":
    main()