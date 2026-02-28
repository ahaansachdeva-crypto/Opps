#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║           🎮  MEGA ARCADE  -  32 MINI-GAMES  🎮                ║
║     Stunning Neon Visuals  |  4 Categories  |  Pygame          ║
╚══════════════════════════════════════════════════════════════════╝

CATEGORIES & GAMES:
  🕹️ ARCADE    : Snake, Pong, Breakout, Asteroids, Space Invaders,
                  Tetris, Pac-Runner, Frogger
  🧩 PUZZLE    : Memory Match, Minesweeper, 2048, Sliding Puzzle,
                  Color Flood, Sudoku Mini, Connect Four, Tic-Tac-Toe
  🏃 ACTION    : Flappy Bird, Dodge Ball, Aim Trainer, Whack-a-Mole,
                  Reaction Test, Catch Fruit, Brick Smasher, Laser Dodge
  🎯 SKILL     : Tower Defense, Simon Says, Typing Speed, Math Blitz,
                  Color Match, Pattern Memory, Word Scramble, Rhythm Tap

INSTALL : pip install pygame
RUN     : python mega_arcade.py
"""

import pygame, sys, math, random, time, string
from collections import deque

pygame.init()
W, H = 1000, 700
FPS = 60
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("🎮 MEGA ARCADE - 32 Games")
clock = pygame.time.Clock()

# ═══════════════════ COLORS ═══════════════════
BG       = (10, 10, 25)
BG2      = (15, 15, 35)
CYAN     = (0, 220, 255)
PINK     = (255, 50, 150)
GREEN    = (0, 255, 130)
YELLOW   = (255, 220, 50)
ORANGE   = (255, 140, 30)
PURPLE   = (180, 80, 255)
RED      = (255, 60, 60)
BLUE     = (50, 120, 255)
WHITE    = (255, 255, 255)
GRAY     = (120, 120, 140)
DGRAY    = (40, 40, 60)
GOLD     = (255, 200, 50)
CAT_COLS = [CYAN, PURPLE, RED, GREEN]

# ═══════════════════ FONTS ═══════════════════
def F(s, b=False): return pygame.font.SysFont("segoeui,arial,helvetica,sans-serif", s, bold=b)
FH = F(48, True); FB = F(30, True); FM = F(22, True); FS = F(16); FT = F(13)
FG = F(28, True); FSC = F(20, True)

# ═══════════════════ PARTICLES ═══════════════════
particles = []
class P:
    __slots__ = ['x','y','vx','vy','life','ml','c','s']
    def __init__(s, x, y, c, vx=None, vy=None, life=35, sz=3):
        s.x=x; s.y=y; s.c=c; s.s=sz; s.life=life; s.ml=life
        s.vx = vx or random.uniform(-3,3); s.vy = vy or random.uniform(-3,3)
    def update(s):
        s.x+=s.vx; s.y+=s.vy; s.vy+=.05; s.life-=1
    def draw(s, surf):
        a = s.life/s.ml; r = max(1,int(s.s*a))
        pygame.draw.circle(surf, tuple(int(ch*a) for ch in s.c), (int(s.x),int(s.y)), r)

def emit(x, y, c, n=12, sp=4, life=35, sz=3):
    for _ in range(n):
        particles.append(P(x,y,c, random.uniform(-sp,sp), random.uniform(-sp,sp), life, sz))

def tick_particles(surf):
    for p in particles[:]:
        p.update(); p.draw(surf)
        if p.life<=0: particles.remove(p)

# ═══════════════════ STARS ═══════════════════
stars = [(random.randint(0,W), random.randint(0,H), random.uniform(.3,1.5), random.randint(1,2)) for _ in range(100)]
def draw_stars(s):
    for i,(x,y,sp,sz) in enumerate(stars):
        b = int(70+60*math.sin(time.time()*sp+i))
        pygame.draw.circle(s,(b,b,b+30),(x,y),sz)

# ═══════════════════ UI HELPERS ═══════════════════
def txt(s, t, f, c, y, x=None):
    r = f.render(t, True, c); rc = r.get_rect(center=(x or W//2, y)); s.blit(r, rc)

def neon_rect(s, r, c, w=2):
    gs = pygame.Surface((r.w+10,r.h+10), pygame.SRCALPHA)
    pygame.draw.rect(gs,(*c,25), gs.get_rect(), border_radius=12)
    s.blit(gs,(r.x-5,r.y-5))
    pygame.draw.rect(s, c, r, w, border_radius=8)

def hud(title, score, extra=""):
    pygame.draw.rect(screen,(15,15,40),(0,0,W,50))
    pygame.draw.line(screen, CYAN, (0,50),(W,50),2)
    txt(screen, title, FM, CYAN, 25, 160)
    txt(screen, f"Score: {score}", FSC, GOLD, 25, W-120)
    if extra: txt(screen, extra, FS, WHITE, 25, W//2)
    br = pygame.Rect(10,10,70,30)
    pygame.draw.rect(screen, PINK, br, 2, border_radius=6)
    txt(screen, "← BACK", FT, WHITE, 25, 45)
    return br

def game_over(score, hs, name):
    ov = pygame.Surface((W,H), pygame.SRCALPHA); ov.fill((0,0,0,160)); screen.blit(ov,(0,0))
    txt(screen, "GAME OVER", FH, RED, H//2-60)
    txt(screen, f"Score: {score}", FB, GOLD, H//2)
    best = hs.get(name, 0)
    if score > best:
        hs[name] = score
        txt(screen, "★ NEW HIGH SCORE! ★", FM, GREEN, H//2+40)
    else:
        txt(screen, f"Best: {best}", FM, GRAY, H//2+40)
    txt(screen, "SPACE = Retry  |  ESC = Menu", FS, GRAY, H//2+85)
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_SPACE: return "r"
                if ev.key==pygame.K_ESCAPE: return "m"

def check_back(ev):
    if ev.type==pygame.MOUSEBUTTONDOWN:
        br = pygame.Rect(10,10,70,30)
        if br.collidepoint(ev.pos): return True
    if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: return True
    return False

# ═══════════════════ GAME CATEGORY DATA ═══════════════════
CATS = [
    ("🕹️ ARCADE CLASSICS",
     ["Snake","Pong","Breakout","Asteroids","Space Invaders","Tetris","Pac-Runner","Frogger"]),
    ("🧩 PUZZLE & LOGIC",
     ["Memory Match","Minesweeper","2048","Sliding Puzzle","Color Flood","Sudoku Mini","Connect Four","Tic-Tac-Toe"]),
    ("🏃 ACTION & REFLEX",
     ["Flappy Bird","Dodge Ball","Aim Trainer","Whack-a-Mole","Reaction Test","Catch Fruit","Brick Smasher","Laser Dodge"]),
    ("🎯 SKILL & STRATEGY",
     ["Tower Defense","Simon Says","Typing Speed","Math Blitz","Color Match","Pattern Memory","Word Scramble","Rhythm Tap"]),
]

high_scores = {}
scroll_y = 0

# ═══════════════════════════════════════════════════════════════
#  GAME 1 : SNAKE
# ═══════════════════════════════════════════════════════════════
def g_snake():
    cs=20; cols=(W-40)//cs; rows=(H-100)//cs; ox=20; oy=70
    def rst():
        sn=deque([(cols//2,rows//2)]); return sn,(1,0),(random.randint(0,cols-1),random.randint(0,rows-1)),0,False
    sn,d,food,sc,dead=rst(); mt=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN and not dead:
                if ev.key==pygame.K_UP and d!=(0,1): d=(0,-1)
                elif ev.key==pygame.K_DOWN and d!=(0,-1): d=(0,1)
                elif ev.key==pygame.K_LEFT and d!=(1,0): d=(-1,0)
                elif ev.key==pygame.K_RIGHT and d!=(-1,0): d=(1,0)
        if not dead:
            mt+=dt
            if mt>max(50,120-sc*2):
                mt=0; h=(sn[-1][0]+d[0],sn[-1][1]+d[1])
                if h[0]<0 or h[0]>=cols or h[1]<0 or h[1]>=rows or h in sn:
                    dead=True; emit(ox+h[0]*cs+cs//2,oy+h[1]*cs+cs//2,RED,25)
                else:
                    sn.append(h)
                    if h==food:
                        sc+=10; emit(ox+food[0]*cs+cs//2,oy+food[1]*cs+cs//2,GREEN,12)
                        while food in sn: food=(random.randint(0,cols-1),random.randint(0,rows-1))
                    else: sn.popleft()
        screen.fill(BG2); draw_stars(screen)
        for r in range(rows+1): pygame.draw.line(screen,(20,20,40),(ox,oy+r*cs),(ox+cols*cs,oy+r*cs))
        for c in range(cols+1): pygame.draw.line(screen,(20,20,40),(ox+c*cs,oy),(ox+c*cs,oy+rows*cs))
        p2=abs(math.sin(time.time()*4))*6
        pygame.draw.circle(screen,(200,40,40),(ox+food[0]*cs+cs//2,oy+food[1]*cs+cs//2),int(cs//2+p2))
        pygame.draw.rect(screen,RED,(ox+food[0]*cs+2,oy+food[1]*cs+2,cs-4,cs-4),border_radius=4)
        for i,(sx,sy) in enumerate(sn):
            t=i/max(len(sn),1); c2=(int(50*t),int(200+55*t),int(80+50*t))
            pygame.draw.rect(screen,c2,(ox+sx*cs+1,oy+sy*cs+1,cs-2,cs-2),border_radius=5)
        tick_particles(screen); hud("SNAKE",sc,"Arrow Keys")
        if dead:
            r2=game_over(sc,high_scores,"Snake")
            if r2=="r": sn,d,food,sc,dead=rst()
            else: return
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 2 : PONG
# ═══════════════════════════════════════════════════════════════
def g_pong():
    pw,ph=12,80; p1=p2=H//2-ph//2; bx=by=0; bvx=bvy=0; s1=s2=0
    def rst(): return W//2,H//2,5*random.choice([-1,1]),3*random.choice([-1,1])
    bx,by,bvx,bvy=rst()
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w]: p1=max(55,p1-6)
        if keys[pygame.K_s]: p1=min(H-ph-5,p1+6)
        tgt=by-ph//2; p2+=(1 if p2<tgt else -1)*min(abs(p2-tgt),4); p2=max(55,min(H-ph-5,p2))
        bx+=bvx; by+=bvy
        if by<=55 or by>=H-5: bvy=-bvy
        if bx<=50+pw and p1<=by<=p1+ph: bvx=abs(bvx)+.2; emit(50+pw,int(by),CYAN,6)
        if bx>=W-50-pw and p2<=by<=p2+ph: bvx=-(abs(bvx)+.2); emit(W-50-pw,int(by),PINK,6)
        if bx<20: s2+=1; bx,by,bvx,bvy=rst()
        if bx>W-20: s1+=1; bx,by,bvx,bvy=rst()
        screen.fill(BG2); draw_stars(screen)
        for y in range(55,H,20): pygame.draw.rect(screen,DGRAY,(W//2-1,y,2,10))
        pygame.draw.rect(screen,CYAN,(40,p1,pw,ph),border_radius=4)
        pygame.draw.rect(screen,PINK,(W-40-pw,p2,pw,ph),border_radius=4)
        pygame.draw.circle(screen,WHITE,(int(bx),int(by)),7)
        tick_particles(screen); hud("PONG",s1,f"You {s1} - {s2} AI  |  W/S")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 3 : BREAKOUT
# ═══════════════════════════════════════════════════════════════
def g_breakout():
    pw2=100; bx=W//2; by=H-100; bvx=4; bvy=-4; sc=0; lives=3
    cols=[RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE]
    bw,bh=58,18
    def mk(): return [pygame.Rect(c*(bw+5)+40,r*(bh+4)+70,bw,bh) for r in range(6) for c in range(15)]
    bricks=mk()
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        px=max(0,min(W-pw2,pygame.mouse.get_pos()[0]-pw2//2))
        bx+=bvx; by+=bvy
        if bx<=5 or bx>=W-5: bvx=-bvx
        if by<=55: bvy=abs(bvy)
        if by>=H:
            lives-=1; bx,by,bvx,bvy=W//2,H-100,random.choice([-4,4]),-4
            if lives<=0:
                r2=game_over(sc,high_scores,"Breakout")
                if r2=="r": bricks=mk();sc=0;lives=3
                else: return
        pr=pygame.Rect(px,H-40,pw2,12)
        if pr.collidepoint(bx,by): bvy=-abs(bvy); bvx=(bx-(px+pw2/2))/(pw2/2)*5; emit(int(bx),int(by),CYAN,5)
        for b in bricks[:]:
            if b.collidepoint(bx,by):
                row=(b.y-70)//(bh+4); emit(b.centerx,b.centery,cols[row%6],8)
                bricks.remove(b); bvy=-bvy; sc+=10+row*5; break
        if not bricks: bricks=mk()
        screen.fill(BG2); draw_stars(screen)
        for b in bricks:
            row=(b.y-70)//(bh+4); pygame.draw.rect(screen,cols[row%6],b,border_radius=3)
        pygame.draw.rect(screen,CYAN,pr,border_radius=4)
        pygame.draw.circle(screen,WHITE,(int(bx),int(by)),6)
        tick_particles(screen); hud("BREAKOUT",sc,f"Lives: {lives}  |  Mouse")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 4 : ASTEROIDS
# ═══════════════════════════════════════════════════════════════
def g_asteroids():
    px=W//2;py=H//2;ang=0;vx=vy=0;sc=0;lives=3;buls=[];asts=[];scd=0
    def spa(sz=3,x=None,y=None):
        ax=x or random.choice([0,W]); ay=y or random.randint(60,H)
        a=random.uniform(0,6.28); sp=random.uniform(1,2.5)
        asts.append({"x":ax,"y":ay,"vx":math.cos(a)*sp,"vy":math.sin(a)*sp,"sz":sz,
            "r":sz*12+5,"pts":[(random.uniform(.7,1.3)*(sz*12+5),random.uniform(0,6.28)) for _ in range(8)]})
    for _ in range(5): spa()
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: ang-=4
        if keys[pygame.K_RIGHT]: ang+=4
        if keys[pygame.K_UP]:
            rd=math.radians(ang-90); vx+=math.cos(rd)*.15; vy+=math.sin(rd)*.15
        scd=max(0,scd-dt)
        if keys[pygame.K_SPACE] and scd<=0:
            rd=math.radians(ang-90); buls.append([px,py,math.cos(rd)*8,math.sin(rd)*8,60]); scd=200
        px=(px+vx)%W; py=max(55,(py+vy)%H); vx*=.99; vy*=.99
        for b in buls[:]:
            b[0]+=b[2];b[1]+=b[3];b[4]-=1
            if b[4]<=0: buls.remove(b)
        for a in asts:
            a["x"]=(a["x"]+a["vx"])%W; a["y"]=55+(a["y"]-55+a["vy"])%(H-55)
            if math.hypot(a["x"]-px,a["y"]-py)<a["r"]+10:
                lives-=1; px,py=W//2,H//2; vx=vy=0; emit(px,py,RED,20)
                if lives<=0:
                    r2=game_over(sc,high_scores,"Asteroids")
                    if r2=="r": sc=0;lives=3;asts.clear();buls.clear();[spa() for _ in range(5)]
                    else: return
        for b in buls[:]:
            for a in asts[:]:
                if math.hypot(a["x"]-b[0],a["y"]-b[1])<a["r"]:
                    emit(a["x"],a["y"],ORANGE,10); sc+=(4-a["sz"])*25
                    if a["sz"]>1: [spa(a["sz"]-1,a["x"],a["y"]) for _ in range(2)]
                    asts.remove(a)
                    if b in buls: buls.remove(b)
                    break
        if len(asts)<3: [spa() for _ in range(3)]
        screen.fill(BG2); draw_stars(screen)
        for a in asts:
            pts=[(a["x"]+math.cos(ag)*d,a["y"]+math.sin(ag)*d) for d,ag in a["pts"]]
            if len(pts)>=3: pygame.draw.polygon(screen,GRAY,pts,2)
        for b in buls: pygame.draw.circle(screen,YELLOW,(int(b[0]),int(b[1])),3)
        rd=math.radians(ang-90)
        tip=(px+math.cos(rd)*15,py+math.sin(rd)*15)
        lf=(px+math.cos(rd+2.5)*12,py+math.sin(rd+2.5)*12)
        rt=(px+math.cos(rd-2.5)*12,py+math.sin(rd-2.5)*12)
        pygame.draw.polygon(screen,CYAN,[tip,lf,rt],2)
        tick_particles(screen); hud("ASTEROIDS",sc,f"Lives:{lives} | Arrows+Space")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 5 : SPACE INVADERS
# ═══════════════════════════════════════════════════════════════
def g_invaders():
    px=W//2;buls=[];ebuls=[];sc=0;lives=3;edir=1;et=0;scd=0
    def mk():
        return [{"x":c*55+140,"y":r*38+80,"a":True} for r in range(4) for c in range(11)]
    ens=mk()
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: px=max(20,px-5)
        if keys[pygame.K_RIGHT]: px=min(W-20,px+5)
        scd=max(0,scd-dt)
        if keys[pygame.K_SPACE] and scd<=0: buls.append([px,H-60]);scd=300
        nonlocal_edir=edir
        et+=dt
        if et>max(200,800-sc):
            et=0; alive=[e for e in ens if e["a"]]
            if alive:
                md=False
                for e in alive:
                    if (e["x"]>W-60 and edir>0) or (e["x"]<60 and edir<0): md=True; break
                if md:
                    edir=-edir
                    for e in alive: e["y"]+=18
                else:
                    for e in alive: e["x"]+=edir*18
                if random.random()<.3:
                    sh=random.choice(alive); ebuls.append([sh["x"],sh["y"]])
        for b in buls[:]:
            b[1]-=8
            if b[1]<50: buls.remove(b); continue
            for e in ens:
                if e["a"] and abs(b[0]-e["x"])<16 and abs(b[1]-e["y"])<14:
                    e["a"]=False;sc+=30;emit(e["x"],e["y"],GREEN,8)
                    if b in buls: buls.remove(b)
                    break
        for b in ebuls[:]:
            b[1]+=5
            if b[1]>H: ebuls.remove(b); continue
            if abs(b[0]-px)<15 and abs(b[1]-(H-50))<15:
                lives-=1;ebuls.remove(b);emit(px,H-50,RED,12)
                if lives<=0:
                    r2=game_over(sc,high_scores,"Space Invaders")
                    if r2=="r": sc=0;lives=3;buls.clear();ebuls.clear();ens=mk()
                    else: return
        if not any(e["a"] for e in ens): ens=mk()
        screen.fill(BG2); draw_stars(screen)
        for e in ens:
            if e["a"]:
                pygame.draw.rect(screen,GREEN,(e["x"]-14,e["y"]-9,28,18),border_radius=4)
                pygame.draw.rect(screen,(0,180,80),(e["x"]-9,e["y"]-5,7,5))
                pygame.draw.rect(screen,(0,180,80),(e["x"]+2,e["y"]-5,7,5))
        pygame.draw.polygon(screen,CYAN,[(px,H-60),(px-14,H-42),(px+14,H-42)])
        for b in buls: pygame.draw.rect(screen,YELLOW,(b[0]-2,b[1],4,10))
        for b in ebuls: pygame.draw.rect(screen,RED,(b[0]-2,b[1],4,8))
        tick_particles(screen); hud("SPACE INVADERS",sc,f"Lives:{lives} | ←→+Space")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 6 : TETRIS
# ═══════════════════════════════════════════════════════════════
def g_tetris():
    C2,R2=10,20;CL=28;ox=W//2-C2*CL//2;oy=60
    SH=[[[1,1,1,1]],[[1,1],[1,1]],[[0,1,0],[1,1,1]],[[1,0,0],[1,1,1]],
        [[0,0,1],[1,1,1]],[[1,1,0],[0,1,1]],[[0,1,1],[1,1,0]]]
    CO=[CYAN,YELLOW,PURPLE,BLUE,ORANGE,GREEN,RED]
    grid=[[0]*C2 for _ in range(R2)]; sc=0; lv=1
    def np2():
        i=random.randint(0,6)
        return {"s":[r[:] for r in SH[i]],"c":CO[i],"x":C2//2-len(SH[i][0])//2,"y":0}
    def val(p,dx=0,dy=0):
        for r,row in enumerate(p["s"]):
            for c,v in enumerate(row):
                if v:
                    nx,ny=p["x"]+c+dx,p["y"]+r+dy
                    if nx<0 or nx>=C2 or ny>=R2: return False
                    if ny>=0 and grid[ny][nx]: return False
        return True
    def lock(p):
        for r,row in enumerate(p["s"]):
            for c,v in enumerate(row):
                if v and p["y"]+r>=0: grid[p["y"]+r][p["x"]+c]=p["c"]
    def clr():
        nonlocal sc,lv; ln=0
        for r in range(R2-1,-1,-1):
            if all(grid[r]): del grid[r]; grid.insert(0,[0]*C2); ln+=1
        sc+=[0,100,300,500,800][min(ln,4)]; lv=1+sc//500
    def rot(p):
        o=p["s"]; p["s"]=[list(r) for r in zip(*o[::-1])]
        if not val(p): p["s"]=o
    cur=np2(); nxt=np2(); ft=0; fast=False
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_LEFT and val(cur,-1,0): cur["x"]-=1
                if ev.key==pygame.K_RIGHT and val(cur,1,0): cur["x"]+=1
                if ev.key==pygame.K_UP: rot(cur)
                if ev.key==pygame.K_DOWN: fast=True
            if ev.type==pygame.KEYUP and ev.key==pygame.K_DOWN: fast=False
        ft+=dt; sp=max(50,500-lv*40) if not fast else 30
        if ft>sp:
            ft=0
            if val(cur,0,1): cur["y"]+=1
            else:
                lock(cur); clr(); cur=nxt; nxt=np2()
                if not val(cur):
                    r2=game_over(sc,high_scores,"Tetris")
                    if r2=="r": grid=[[0]*C2 for _ in range(R2)];sc=0;lv=1;cur=np2();nxt=np2()
                    else: return
        screen.fill(BG2); draw_stars(screen)
        pygame.draw.rect(screen,CYAN,(ox-2,oy-2,C2*CL+4,R2*CL+4),2,border_radius=2)
        for r in range(R2):
            for c in range(C2):
                rc=pygame.Rect(ox+c*CL,oy+r*CL,CL-1,CL-1)
                pygame.draw.rect(screen, grid[r][c] if grid[r][c] else (18,18,38), rc, border_radius=3)
        for r,row in enumerate(cur["s"]):
            for c,v in enumerate(row):
                if v: pygame.draw.rect(screen,cur["c"],(ox+(cur["x"]+c)*CL,oy+(cur["y"]+r)*CL,CL-1,CL-1),border_radius=3)
        # next preview
        nx=ox+C2*CL+30; txt(screen,"NEXT",FS,GRAY,oy+10,nx+35)
        for r,row in enumerate(nxt["s"]):
            for c,v in enumerate(row):
                if v: pygame.draw.rect(screen,nxt["c"],(nx+c*22,oy+30+r*22,20,20),border_radius=2)
        txt(screen,f"Lv:{lv}",FS,GREEN,oy+120,nx+35)
        hud("TETRIS",sc,"←→ ↑Rot ↓Fast")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 7 : PAC-RUNNER
# ═══════════════════════════════════════════════════════════════
def g_pacrunner():
    py2=H-120;vy2=0;og=True;sc=0;sp=5;obs=[];dots=[];dead=False
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN and ev.key==pygame.K_SPACE and og and not dead:
                vy2=-13;og=False
        if not dead:
            vy2+=.6;py2+=vy2
            if py2>=H-120: py2=H-120;vy2=0;og=True
            sc+=1;sp=5+sc//200
            if random.random()<.02:
                h=random.choice([30,50,70]); obs.append([W+20,H-90-h,25,h])
            for o in obs: o[0]-=sp
            obs=[o for o in obs if o[0]>-30]
            if random.random()<.05: dots.append([W+20,H-140])
            for d in dots: d[0]-=sp
            dots=[d for d in dots if d[0]>-20]
            pr=pygame.Rect(80,py2,30,30)
            for o in obs:
                if pr.colliderect(pygame.Rect(*o)): dead=True;emit(95,py2+15,YELLOW,25)
            for d in dots[:]:
                if pr.colliderect(pygame.Rect(d[0],d[1],10,10)): dots.remove(d);sc+=50;emit(d[0],d[1],YELLOW,5)
        screen.fill(BG2); draw_stars(screen)
        pygame.draw.line(screen,CYAN,(0,H-85),(W,H-85),2)
        for o in obs: pygame.draw.rect(screen,RED,o,border_radius=3)
        for d in dots: pygame.draw.circle(screen,YELLOW,(int(d[0]),int(d[1])),5)
        mouth=abs(math.sin(time.time()*8))*35
        pygame.draw.circle(screen,YELLOW,(95,int(py2)+15),15)
        mr=math.radians(mouth)
        pygame.draw.polygon(screen,BG2,[(95,int(py2)+15),(115,int(py2)+15-int(math.sin(mr)*15)),(115,int(py2)+15+int(math.sin(mr)*15))])
        tick_particles(screen); hud("PAC-RUNNER",sc,"SPACE to Jump")
        if dead:
            r2=game_over(sc,high_scores,"Pac-Runner")
            if r2=="r": py2=H-120;vy2=0;og=True;sc=0;sp=5;obs.clear();dots.clear();dead=False
            else: return
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 8 : FROGGER
# ═══════════════════════════════════════════════════════════════
def g_frogger():
    fx=W//2;fy=H-40;sc=0;lives=3
    lanes=[]
    for i in range(8):
        y=100+i*65; sp=random.choice([-2,-1.5,1.5,2,2.5,-2.5])*(1+i*.1)
        cars=[[random.randint(0,W),y,random.randint(50,80),25] for _ in range(random.randint(2,4))]
        lanes.append({"y":y,"sp":sp,"cars":cars,"c":random.choice([RED,ORANGE,PURPLE,PINK])})
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_UP: fy-=65
                if ev.key==pygame.K_DOWN: fy=min(H-40,fy+65)
                if ev.key==pygame.K_LEFT: fx=max(15,fx-40)
                if ev.key==pygame.K_RIGHT: fx=min(W-15,fx+40)
        for l in lanes:
            for c2 in l["cars"]:
                c2[0]+=l["sp"]
                if c2[0]>W+50: c2[0]=-c2[2]
                if c2[0]<-c2[2]-50: c2[0]=W
        fr=pygame.Rect(fx-12,fy-12,24,24)
        for l in lanes:
            for c2 in l["cars"]:
                if fr.colliderect(pygame.Rect(*c2)):
                    lives-=1;emit(fx,fy,RED,20);fx=W//2;fy=H-40
                    if lives<=0:
                        r2=game_over(sc,high_scores,"Frogger")
                        if r2=="r": sc=0;lives=3;fx=W//2;fy=H-40
                        else: return
        if fy<80: sc+=100;fx=W//2;fy=H-40;emit(W//2,60,GREEN,20)
        screen.fill(BG2); draw_stars(screen)
        pygame.draw.rect(screen,(20,50,20),(0,H-55,W,55))
        pygame.draw.rect(screen,(20,50,20),(0,55,W,35))
        txt(screen,"SAFE ZONE",FT,GREEN,72)
        for l in lanes:
            for c2 in l["cars"]: pygame.draw.rect(screen,l["c"],c2,border_radius=4)
        pygame.draw.circle(screen,GREEN,(int(fx),int(fy)),12)
        tick_particles(screen); hud("FROGGER",sc,f"Lives:{lives} | Arrows")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 9 : MEMORY MATCH
# ═══════════════════════════════════════════════════════════════
def g_memory():
    cl2,rw=6,4; cw,ch=80,90; mg=10
    ox=(W-cl2*(cw+mg))//2; oy=(H-rw*(ch+mg))//2+20
    syms=list("ABCDEFGHIJKL")[:cl2*rw//2]*2; random.shuffle(syms)
    rev=[False]*len(syms); mat=[False]*len(syms); sel=[]; sc=0; mv=0; wt=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and wt<=0 and len(sel)<2:
                mx,my=ev.pos
                for i in range(len(syms)):
                    r,c=divmod(i,cl2)
                    rx=ox+c*(cw+mg);ry=oy+r*(ch+mg)
                    if pygame.Rect(rx,ry,cw,ch).collidepoint(mx,my) and not mat[i] and i not in sel:
                        sel.append(i);rev[i]=True
                        if len(sel)==2:
                            mv+=1
                            if syms[sel[0]]==syms[sel[1]]:
                                mat[sel[0]]=mat[sel[1]]=True;sc+=100
                                for s in sel:
                                    r2,c2=divmod(s,cl2)
                                    emit(ox+c2*(cw+mg)+cw//2,oy+r2*(ch+mg)+ch//2,GREEN,8)
                                sel=[]
                            else: wt=700
        if wt>0:
            wt-=dt
            if wt<=0:
                for s in sel: rev[s]=False
                sel=[]
        screen.fill(BG2); draw_stars(screen)
        for i in range(len(syms)):
            r,c=divmod(i,cl2);rx=ox+c*(cw+mg);ry=oy+r*(ch+mg);rc=pygame.Rect(rx,ry,cw,ch)
            if mat[i]:
                pygame.draw.rect(screen,(20,60,30),rc,border_radius=8)
                txt(screen,syms[i],FB,GREEN,rc.centery,rc.centerx)
            elif rev[i]:
                pygame.draw.rect(screen,(40,40,80),rc,border_radius=8)
                txt(screen,syms[i],FB,WHITE,rc.centery,rc.centerx)
            else:
                pygame.draw.rect(screen,(25,25,55),rc,border_radius=8)
                pygame.draw.rect(screen,CYAN,rc,2,border_radius=8)
                txt(screen,"?",FB,CYAN,rc.centery,rc.centerx)
        if all(mat):
            sc+=max(0,1000-mv*20)
            r2=game_over(sc,high_scores,"Memory Match")
            if r2=="r": random.shuffle(syms);rev=[False]*len(syms);mat=[False]*len(syms);sel=[];sc=0;mv=0
            else: return
        tick_particles(screen); hud("MEMORY MATCH",sc,f"Moves:{mv}")
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 10 : MINESWEEPER
# ═══════════════════════════════════════════════════════════════
def g_minesweeper():
    C3,R3=12,8;MI=15;CL=42;ox=(W-C3*CL)//2;oy=80
    NC=[CYAN,GREEN,RED,PURPLE,ORANGE,YELLOW,PINK,BLUE]
    def init():
        bd=[[0]*C3 for _ in range(R3)]; rv=[[False]*C3 for _ in range(R3)]; fl=[[False]*C3 for _ in range(R3)]
        ms=set()
        while len(ms)<MI: ms.add((random.randint(0,R3-1),random.randint(0,C3-1)))
        for r,c in ms: bd[r][c]=-1
        for r in range(R3):
            for c in range(C3):
                if bd[r][c]!=-1:
                    bd[r][c]=sum(1 for dr in[-1,0,1] for dc in[-1,0,1] if 0<=r+dr<R3 and 0<=c+dc<C3 and bd[r+dr][c+dc]==-1)
        return bd,rv,fl,ms
    bd,rv,fl,ms=init();sc=0;dead=False
    def flood(r,c):
        if r<0 or r>=R3 or c<0 or c>=C3 or rv[r][c] or fl[r][c]: return
        rv[r][c]=True
        if bd[r][c]==0:
            for dr in[-1,0,1]:
                for dc in[-1,0,1]: flood(r+dr,c+dc)
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and not dead:
                mx,my=ev.pos;c2=(mx-ox)//CL;r2=(my-oy)//CL
                if 0<=r2<R3 and 0<=c2<C3:
                    if ev.button==3: fl[r2][c2]=not fl[r2][c2]
                    elif ev.button==1 and not fl[r2][c2]:
                        if bd[r2][c2]==-1: dead=True;rv[r2][c2]=True;emit(ox+c2*CL+CL//2,oy+r2*CL+CL//2,RED,20)
                        else: flood(r2,c2)
        safe=sum(1 for r in range(R3) for c in range(C3) if rv[r][c] and bd[r][c]!=-1);sc=safe*10
        screen.fill(BG2); draw_stars(screen)
        for r in range(R3):
            for c in range(C3):
                rc=pygame.Rect(ox+c*CL,oy+r*CL,CL-2,CL-2)
                if rv[r][c]:
                    if bd[r][c]==-1:
                        pygame.draw.rect(screen,(80,20,20),rc,border_radius=4)
                        txt(screen,"*",FM,WHITE,rc.centery,rc.centerx)
                    else:
                        pygame.draw.rect(screen,(30,30,55),rc,border_radius=4)
                        if bd[r][c]>0: txt(screen,str(bd[r][c]),FM,NC[bd[r][c]-1],rc.centery,rc.centerx)
                elif fl[r][c]:
                    pygame.draw.rect(screen,(60,40,20),rc,border_radius=4)
                    txt(screen,"F",FM,RED,rc.centery,rc.centerx)
                else:
                    pygame.draw.rect(screen,DGRAY,rc,border_radius=4)
        tick_particles(screen); hud("MINESWEEPER",sc,"L:Reveal R:Flag")
        if dead:
            for r,c in ms: rv[r][c]=True
            r2=game_over(sc,high_scores,"Minesweeper")
            if r2=="r": bd,rv,fl,ms=init();dead=False;sc=0
            else: return
        if safe>=R3*C3-MI:
            sc+=500
            r2=game_over(sc,high_scores,"Minesweeper")
            if r2=="r": bd,rv,fl,ms=init();dead=False;sc=0
            else: return
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME 11 : 2048
# ═══════════════════════════════════════════════════════════════
def g_2048():
    SZ=4;CL=100;PD=8;ox=(W-SZ*(CL+PD))//2;oy=100
    TC={0:(30,30,50),2:(60,60,90),4:(70,80,120),8:(200,120,50),16:(220,100,40),
        32:(230,70,50),64:(230,50,30),128:(220,190,60),256:(220,180,40),
        512:(220,170,20),1024:(200,150,0),2048:(255,200,50)}
    def nb():
        b=[[0]*SZ for _ in range(SZ)]; at(b);at(b); return b
    def at(b):
        e=[(r,c) for r in range(SZ) for c in range(SZ) if b[r][c]==0]
        if e: r,c=random.choice(e); b[r][c]=4 if random.random()<.1 else 2
    def sl(row):
        n=[x for x in row if x];m=[];sa=0;i=0
        while i<len(n):
            if i+1<len(n) and n[i]==n[i+1]: m.append(n[i]*2);sa+=n[i]*2;i+=2
            else: m.append(n[i]);i+=1
        return m+[0]*(SZ-len(m)),sa
    def mv(b,d):
        s=0;moved=False
        for i in range(SZ):
            if d=="l": row=b[i][:]; nr,sc2=sl(row);
            elif d=="r": row=b[i][::-1]; nr,sc2=sl(row); nr=nr[::-1]
            elif d=="u": row=[b[r][i] for r in range(SZ)]; nr,sc2=sl(row)
            else: row=[b[r][i] for r in range(SZ)][::-1]; nr,sc2=sl(row); nr=nr[::-1]
            s+=sc2
            if d in("l","r"):
                if nr!=b[i]: moved=True
                b[i]=nr
            else:
                orig=[b[r][i] for r in range(SZ)]
                if nr!=orig: moved=True
                for r in range(SZ): b[r][i]=nr[r]
        return s,moved
    def cm(b):
        for r in range(SZ):
            for c in range(SZ):
                if b[r][c]==0: return True
                if c+1<SZ and b[r][c]==b[r][c+1]: return True
                if r+1<SZ and b[r][c]==b[r+1][c]: return True
        return False
    bd=nb();sc=0
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                d=None
                if ev.key==pygame.K_LEFT: d="l"
                elif ev.key==pygame.K_RIGHT: d="r"
                elif ev.key==pygame.K_UP: d="u"
                elif ev.key==pygame.K_DOWN: d="d"
                if d:
                    s2,m2=mv(bd,d); sc+=s2
                    if m2: at(bd)
        if not cm(bd):
            r2=game_over(sc,high_scores,"2048")
            if r2=="r": bd=nb();sc=0
            else: return
        screen.fill(BG2); draw_stars(screen)
        for r in range(SZ):
            for c in range(SZ):
                x=ox+c*(CL+PD);y=oy+r*(CL+PD);v=bd[r][c]
                pygame.draw.rect(screen,TC.get(v,(180,140,0)),(x,y,CL,CL),border_radius=8)
                if v>0:
                    f2=FM if v<1000 else FS; tc=WHITE if v>=8 else GRAY
                    txt(screen,str(v),f2,tc,y+CL//2,x+CL//2)
        hud("2048",sc,"Arrow Keys"); pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAMES 12-16 : PUZZLE GAMES (Compact)
# ═══════════════════════════════════════════════════════════════
def g_sliding():
    SZ=4;CL=95;PD=5;ox=(W-SZ*(CL+PD))//2;oy=100
    t=list(range(1,SZ*SZ))+[0]
    for _ in range(300):
        z=t.index(0);r,c=divmod(z,SZ);ms=[]
        if r>0:ms.append(z-SZ)
        if r<SZ-1:ms.append(z+SZ)
        if c>0:ms.append(z-1)
        if c<SZ-1:ms.append(z+1)
        m=random.choice(ms);t[z],t[m]=t[m],t[z]
    mv=0
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN:
                mx,my=ev.pos;c2=(mx-ox)//(CL+PD);r2=(my-oy)//(CL+PD)
                if 0<=r2<SZ and 0<=c2<SZ:
                    idx=r2*SZ+c2;z=t.index(0);zr,zc=divmod(z,SZ)
                    if abs(r2-zr)+abs(c2-zc)==1: t[z],t[idx]=t[idx],t[z];mv+=1
        if t==list(range(1,SZ*SZ))+[0]:
            r2=game_over(max(0,2000-mv*10),high_scores,"Sliding Puzzle")
            if r2=="r":
                for _ in range(300):
                    z=t.index(0);r3,c3=divmod(z,SZ);ms=[]
                    if r3>0:ms.append(z-SZ)
                    if r3<SZ-1:ms.append(z+SZ)
                    if c3>0:ms.append(z-1)
                    if c3<SZ-1:ms.append(z+1)
                    m=random.choice(ms);t[z],t[m]=t[m],t[z]
                mv=0
            else: return
        screen.fill(BG2); draw_stars(screen)
        for i,v in enumerate(t):
            r4,c4=divmod(i,SZ);x=ox+c4*(CL+PD);y=oy+r4*(CL+PD)
            if v:
                hue=v/(SZ*SZ)*360; co=pygame.Color(0);co.hsva=(hue%360,60,80,100)
                pygame.draw.rect(screen,co,(x,y,CL,CL),border_radius=10)
                txt(screen,str(v),FB,WHITE,y+CL//2,x+CL//2)
            else: pygame.draw.rect(screen,(20,20,40),(x,y,CL,CL),border_radius=10)
        hud("SLIDING PUZZLE",mv,"Click to slide"); pygame.display.flip()

def g_colorflood():
    SZ=12;CL=38;ox=(W-SZ*CL)//2;oy=100
    FC=[RED,BLUE,GREEN,YELLOW,PURPLE,ORANGE]
    bd=[[random.randint(0,5) for _ in range(SZ)] for _ in range(SZ)];mv=0;mx2=25
    def ff(nc):
        old=bd[0][0]
        if old==nc: return
        stk=[(0,0)];vis=set()
        while stk:
            r,c=stk.pop()
            if (r,c) in vis or r<0 or r>=SZ or c<0 or c>=SZ or bd[r][c]!=old: continue
            vis.add((r,c));bd[r][c]=nc;stk.extend([(r+1,c),(r-1,c),(r,c+1),(r,c-1)])
    br=[pygame.Rect(ox+i*70,oy+SZ*CL+30,55,40) for i in range(6)]
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN:
                for i,rc in enumerate(br):
                    if rc.collidepoint(ev.pos): ff(i);mv+=1
        won=all(bd[r][c]==bd[0][0] for r in range(SZ) for c in range(SZ))
        if won or mv>=mx2:
            sc=max(0,(mx2-mv)*50) if won else 0
            r2=game_over(sc,high_scores,"Color Flood")
            if r2=="r": bd=[[random.randint(0,5) for _ in range(SZ)] for _ in range(SZ)];mv=0
            else: return
        screen.fill(BG2); draw_stars(screen)
        for r in range(SZ):
            for c in range(SZ):
                pygame.draw.rect(screen,FC[bd[r][c]],(ox+c*CL,oy+r*CL,CL-2,CL-2),border_radius=4)
        for i,rc in enumerate(br): pygame.draw.rect(screen,FC[i],rc,border_radius=8)
        hud("COLOR FLOOD",mx2-mv,f"Moves:{mv}/{mx2}"); pygame.display.flip()

def g_sudoku():
    CL=60;SZ=4;ox=(W-SZ*CL)//2;oy=120
    base=[[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]]
    sol=[r[:] for r in base];bk=set()
    while len(bk)<8: bk.add((random.randint(0,3),random.randint(0,3)))
    bd=[r[:] for r in sol]
    for r,c in bk: bd[r][c]=0
    sel=None;sc=0
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN and sel and sel in bk:
                r,c=sel
                for n in range(1,5):
                    if ev.key==getattr(pygame,f'K_{n}') or ev.key==getattr(pygame,f'K_KP{n}'):
                        bd[r][c]=n
            if ev.type==pygame.MOUSEBUTTONDOWN:
                mx,my=ev.pos;c2=(mx-ox)//CL;r2=(my-oy)//CL
                if 0<=r2<SZ and 0<=c2<SZ: sel=(r2,c2)
        screen.fill(BG2); draw_stars(screen)
        for r in range(SZ):
            for c in range(SZ):
                x=ox+c*CL;y=oy+r*CL;rc=pygame.Rect(x,y,CL-2,CL-2)
                bg=(40,40,70) if (r//2+c//2)%2==0 else (30,30,55)
                if sel==(r,c): bg=(60,60,100)
                pygame.draw.rect(screen,bg,rc,border_radius=4)
                if bd[r][c]>0:
                    co=GRAY if (r,c) not in bk else (GREEN if bd[r][c]==sol[r][c] else RED)
                    txt(screen,str(bd[r][c]),FB,co,rc.centery,rc.centerx)
        txt(screen,"Select cell, press 1-4",FS,GRAY,oy+SZ*CL+30)
        if all(bd[r][c]==sol[r][c] for r in range(SZ) for c in range(SZ)):
            r2=game_over(500,high_scores,"Sudoku Mini")
            if r2=="r":
                bk=set()
                while len(bk)<8: bk.add((random.randint(0,3),random.randint(0,3)))
                bd=[r[:] for r in sol]
                for r,c in bk: bd[r][c]=0
                sel=None
            else: return
        hud("SUDOKU 4x4",sc); pygame.display.flip()

def g_connect4():
    CL2,RW=7,6;CS=65;ox=(W-CL2*CS)//2;oy=100
    bd=[[0]*CL2 for _ in range(RW)];turn=1;win=0;sc=0
    def drop(col,p):
        for r in range(RW-1,-1,-1):
            if bd[r][col]==0: bd[r][col]=p;return r
        return -1
    def chk(p):
        for r in range(RW):
            for c in range(CL2):
                for dr,dc in[(0,1),(1,0),(1,1),(1,-1)]:
                    if all(0<=r+dr*i<RW and 0<=c+dc*i<CL2 and bd[r+dr*i][c+dc*i]==p for i in range(4)): return True
        return False
    def ai():
        for c in range(CL2):
            for r in range(RW-1,-1,-1):
                if bd[r][c]==0:
                    bd[r][c]=2
                    if chk(2): bd[r][c]=0;return c
                    bd[r][c]=0;break
        for c in range(CL2):
            for r in range(RW-1,-1,-1):
                if bd[r][c]==0:
                    bd[r][c]=1
                    if chk(1): bd[r][c]=0;return c
                    bd[r][c]=0;break
        v=[c for c in range(CL2) if bd[0][c]==0]
        return random.choice(v) if v else -1
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and win==0 and turn==1:
                col=(ev.pos[0]-ox)//CS
                if 0<=col<CL2 and bd[0][col]==0:
                    drop(col,1)
                    if chk(1): win=1;sc=500
                    else: turn=2
        if turn==2 and win==0:
            ac=ai()
            if ac>=0: drop(ac,2);
            if chk(2): win=2
            turn=1
        screen.fill(BG2); draw_stars(screen)
        pygame.draw.rect(screen,(20,20,60),(ox-5,oy-5,CL2*CS+10,RW*CS+10),border_radius=10)
        for r in range(RW):
            for c in range(CL2):
                cx=ox+c*CS+CS//2;cy=oy+r*CS+CS//2
                co=BG2 if bd[r][c]==0 else (RED if bd[r][c]==1 else YELLOW)
                pygame.draw.circle(screen,co,(cx,cy),CS//2-5)
        if win:
            r2=game_over(sc,high_scores,"Connect Four")
            if r2=="r": bd=[[0]*CL2 for _ in range(RW)];turn=1;win=0;sc=0
            else: return
        hud("CONNECT FOUR",sc,"Click column"); pygame.display.flip()

def g_tictactoe():
    CL=120;ox=(W-3*CL)//2;oy=130;bd=[[0]*3 for _ in range(3)];turn=1;win=0;sc=0
    def chk():
        for i in range(3):
            if bd[i][0]==bd[i][1]==bd[i][2]!=0: return bd[i][0]
            if bd[0][i]==bd[1][i]==bd[2][i]!=0: return bd[0][i]
        if bd[0][0]==bd[1][1]==bd[2][2]!=0: return bd[0][0]
        if bd[0][2]==bd[1][1]==bd[2][0]!=0: return bd[0][2]
        return 0
    def ai():
        e=[(r,c) for r in range(3) for c in range(3) if bd[r][c]==0]
        if not e: return
        for r,c in e:
            bd[r][c]=2;
            if chk()==2: bd[r][c]=0;return(r,c)
            bd[r][c]=0
        for r,c in e:
            bd[r][c]=1;
            if chk()==1: bd[r][c]=0;return(r,c)
            bd[r][c]=0
        if(1,1) in e: return(1,1)
        return random.choice(e)
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and win==0:
                mx,my=ev.pos;c2=(mx-ox)//CL;r2=(my-oy)//CL
                if 0<=r2<3 and 0<=c2<3 and bd[r2][c2]==0:
                    bd[r2][c2]=1;win=chk()
                    if win==0:
                        m=ai()
                        if m: bd[m[0]][m[1]]=2;win=chk()
        screen.fill(BG2); draw_stars(screen)
        for i in range(1,3):
            pygame.draw.line(screen,CYAN,(ox+i*CL,oy),(ox+i*CL,oy+3*CL),3)
            pygame.draw.line(screen,CYAN,(ox,oy+i*CL),(ox+3*CL,oy+i*CL),3)
        for r in range(3):
            for c in range(3):
                cx=ox+c*CL+CL//2;cy=oy+r*CL+CL//2
                if bd[r][c]==1:
                    pygame.draw.line(screen,CYAN,(cx-30,cy-30),(cx+30,cy+30),4)
                    pygame.draw.line(screen,CYAN,(cx+30,cy-30),(cx-30,cy+30),4)
                elif bd[r][c]==2: pygame.draw.circle(screen,PINK,(cx,cy),35,4)
        full=all(bd[r][c]!=0 for r in range(3) for c in range(3))
        if win or full:
            sc=300 if win==1 else(0 if win==2 else 50)
            r2=game_over(sc,high_scores,"Tic-Tac-Toe")
            if r2=="r": bd=[[0]*3 for _ in range(3)];win=0;sc=0
            else: return
        hud("TIC-TAC-TOE",sc,"Click to place X"); pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAMES 17-24 : ACTION GAMES
# ═══════════════════════════════════════════════════════════════
def g_flappy():
    by=H//2;bvy=0;sc=0;dead=False;pipes=[];pt=0;gap=160
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN and ev.key==pygame.K_SPACE and not dead: bvy=-7
            if ev.type==pygame.MOUSEBUTTONDOWN and not dead and ev.pos[1]>55: bvy=-7
        if not dead:
            bvy+=.4;by+=bvy;pt+=dt
            if pt>1800: pt=0;h=random.randint(80,H-gap-80);pipes.append([W,h])
            for p in pipes: p[0]-=3
            pipes=[p for p in pipes if p[0]>-60]
            br=pygame.Rect(100,by-12,24,24)
            for p in pipes:
                if br.colliderect(pygame.Rect(p[0],55,50,p[1]-55)) or br.colliderect(pygame.Rect(p[0],p[1]+gap,50,H-p[1]-gap)):
                    dead=True;emit(112,by,YELLOW,20)
            if by>H-5 or by<55: dead=True
            for p in pipes:
                if abs(p[0]-100)<2: sc+=1
        screen.fill(BG2); draw_stars(screen)
        for p in pipes:
            pygame.draw.rect(screen,GREEN,(p[0],55,50,p[1]-55),border_radius=4)
            pygame.draw.rect(screen,GREEN,(p[0],p[1]+gap,50,H-p[1]-gap),border_radius=4)
        pygame.draw.circle(screen,YELLOW,(112,int(by)),12)
        pygame.draw.circle(screen,WHITE,(118,int(by)-3),4)
        pygame.draw.circle(screen,(0,0,0),(119,int(by)-3),2)
        tick_particles(screen); hud("FLAPPY BIRD",sc,"SPACE/Click to flap")
        if dead:
            r2=game_over(sc,high_scores,"Flappy Bird")
            if r2=="r": by=H//2;bvy=0;sc=0;dead=False;pipes.clear()
            else: return
        pygame.display.flip()

def g_dodge():
    px=W//2;py=H//2;sc=0;dead=False;balls=[];st=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        if not dead:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: px=max(15,px-5)
            if keys[pygame.K_RIGHT]: px=min(W-15,px+5)
            if keys[pygame.K_UP]: py=max(65,py-5)
            if keys[pygame.K_DOWN]: py=min(H-15,py+5)
            sc+=1;st+=dt
            if st>max(200,800-sc//5):
                st=0;sd=random.randint(0,3)
                bx2=random.randint(0,W) if sd<2 else(0 if sd==2 else W)
                by2=55 if sd==0 else(H if sd==1 else random.randint(55,H))
                a=math.atan2(py-by2,px-bx2);sp=random.uniform(2,4+sc/500)
                balls.append([bx2,by2,math.cos(a)*sp,math.sin(a)*sp,random.randint(6,14),random.choice([RED,PINK,ORANGE])])
            for b in balls: b[0]+=b[2];b[1]+=b[3]
            balls=[b for b in balls if -20<b[0]<W+20 and 40<b[1]<H+20]
            for b in balls:
                if math.hypot(b[0]-px,b[1]-py)<b[4]+10: dead=True;emit(px,py,RED,30)
        screen.fill(BG2); draw_stars(screen)
        for b in balls: pygame.draw.circle(screen,b[5],(int(b[0]),int(b[1])),b[4])
        if not dead: pygame.draw.circle(screen,CYAN,(int(px),int(py)),12);pygame.draw.circle(screen,WHITE,(int(px),int(py)),6)
        tick_particles(screen); hud("DODGE BALL",sc,"Arrows to dodge")
        if dead:
            r2=game_over(sc,high_scores,"Dodge Ball")
            if r2=="r": px=W//2;py=H//2;sc=0;dead=False;balls.clear()
            else: return
        pygame.display.flip()

def g_aim():
    tgts=[];sc=0;miss=0;mx2=10;st=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN:
                hit=False
                for t in tgts[:]:
                    if math.hypot(ev.pos[0]-t[0],ev.pos[1]-t[1])<t[2]:
                        sc+=max(10,50-int(t[2]));emit(t[0],t[1],GREEN,10);tgts.remove(t);hit=True;break
                if not hit and ev.pos[1]>55: miss+=1
        st+=dt
        if st>600: st=0;tgts.append([random.randint(80,W-80),random.randint(100,H-80),random.randint(15,35),0])
        for t in tgts: t[3]+=dt
        for t in tgts[:]:
            if t[3]>3000: tgts.remove(t);miss+=1
        if miss>=mx2:
            r2=game_over(sc,high_scores,"Aim Trainer")
            if r2=="r": tgts.clear();sc=0;miss=0
            else: return
        screen.fill(BG2); draw_stars(screen)
        for t in tgts:
            a=1-t[3]/3000;co=(int(255*a),int(50*a),int(50*a))
            pygame.draw.circle(screen,co,(t[0],t[1]),t[2])
            pygame.draw.circle(screen,WHITE,(t[0],t[1]),t[2]//2)
            pygame.draw.circle(screen,RED,(t[0],t[1]),t[2]//4)
        mx,my=pygame.mouse.get_pos()
        pygame.draw.line(screen,GREEN,(mx-12,my),(mx+12,my),2)
        pygame.draw.line(screen,GREEN,(mx,my-12),(mx,my+12),2)
        tick_particles(screen); hud("AIM TRAINER",sc,f"Misses:{miss}/{mx2}")
        pygame.display.flip()

def g_whack():
    CL2,RW=4,3;CS=120;ox=(W-CL2*CS)//2;oy=110
    moles=[0]*(CL2*RW);sc=0;timer=30000;st=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN:
                mx,my=ev.pos
                for i in range(CL2*RW):
                    r,c=divmod(i,CL2);cx=ox+c*CS+CS//2;cy=oy+r*CS+CS//2
                    if math.hypot(mx-cx,my-cy)<40 and moles[i]>0:
                        sc+=25;moles[i]=0;emit(cx,cy,GREEN,10)
        timer-=dt
        if timer<=0:
            r2=game_over(sc,high_scores,"Whack-a-Mole")
            if r2=="r": sc=0;timer=30000;moles=[0]*(CL2*RW)
            else: return
        st+=dt
        if st>500: st=0;moles[random.randint(0,CL2*RW-1)]=1200
        for i in range(len(moles)):
            if moles[i]>0: moles[i]=max(0,moles[i]-dt)
        screen.fill(BG2); draw_stars(screen)
        for i in range(CL2*RW):
            r,c=divmod(i,CL2);x=ox+c*CS;y=oy+r*CS
            pygame.draw.ellipse(screen,(30,20,10),(x+10,y+CS-30,CS-20,25))
            if moles[i]>0:
                h=int(40*min(1,moles[i]/300 if moles[i]<300 else 1))
                pygame.draw.ellipse(screen,(139,90,43),(x+25,y+CS-30-h,CS-50,h+10))
                ey=y+CS-30-h+10
                pygame.draw.circle(screen,WHITE,(x+42,ey),5);pygame.draw.circle(screen,(0,0,0),(x+42,ey),2)
                pygame.draw.circle(screen,WHITE,(x+CS-42,ey),5);pygame.draw.circle(screen,(0,0,0),(x+CS-42,ey),2)
        tick_particles(screen); hud("WHACK-A-MOLE",sc,f"Time:{timer//1000}s")
        pygame.display.flip()

def g_reaction():
    st="wait";wt=random.randint(2000,5000);t=0;res=[];sc=0;rn=0;mx2=5
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN:
                if st=="wait": st="ready";t=0;wt=random.randint(2000,5000)
                elif st=="ready": st="wait"
                elif st=="go": res.append(t);rn+=1;st="result" if rn<mx2 else "final"
                elif st=="result": st="ready";t=0;wt=random.randint(2000,5000)
                elif st=="final":
                    avg=sum(res)/len(res) if res else 9999;sc=max(0,int(1000-avg*2))
                    r2=game_over(sc,high_scores,"Reaction Test")
                    if r2=="r": st="wait";res=[];rn=0
                    else: return
        t+=dt
        if st=="ready" and t>=wt: st="go";t=0
        screen.fill(BG2); draw_stars(screen)
        if st=="wait": txt(screen,"Click to Start",FB,CYAN,H//2)
        elif st=="ready":
            pygame.draw.rect(screen,(60,10,10),(100,100,W-200,H-200),border_radius=20)
            txt(screen,"Wait for GREEN...",FB,WHITE,H//2)
        elif st=="go":
            pygame.draw.rect(screen,(10,80,10),(100,100,W-200,H-200),border_radius=20)
            txt(screen,"CLICK NOW!",FH,WHITE,H//2-20)
            txt(screen,f"{int(t)} ms",FB,YELLOW,H//2+40)
        elif st=="result":
            txt(screen,f"{int(res[-1])} ms",FH,GREEN,H//2-20)
            txt(screen,"Click to continue",FM,GRAY,H//2+40)
        hud("REACTION TEST",rn,f"Round {rn+1}/{mx2}"); pygame.display.flip()

def g_catch():
    bx=W//2;sc=0;lives=5;fruits=[];st=0
    FC=[RED,ORANGE,YELLOW,PURPLE,PINK]
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        bx=max(40,min(W-40,pygame.mouse.get_pos()[0]))
        st+=dt
        if st>max(300,800-sc*2):
            st=0;idx=random.randint(0,4);fruits.append([random.randint(30,W-30),55,random.uniform(2,4+sc/100),idx])
        for f in fruits: f[1]+=f[2]
        for f in fruits[:]:
            if f[1]>H-50:
                if abs(f[0]-bx)<45: sc+=10;emit(f[0],f[1],FC[f[3]],6)
                else: lives-=1
                fruits.remove(f)
        if lives<=0:
            r2=game_over(sc,high_scores,"Catch Fruit")
            if r2=="r": sc=0;lives=5;fruits.clear()
            else: return
        screen.fill(BG2); draw_stars(screen)
        for f in fruits: pygame.draw.circle(screen,FC[f[3]],(int(f[0]),int(f[1])),12)
        pygame.draw.rect(screen,CYAN,(bx-40,H-45,80,20),border_radius=6)
        tick_particles(screen); hud("CATCH FRUIT",sc,f"Lives:{lives} | Mouse")
        pygame.display.flip()

def g_bricksmasher():
    pw=100;bx=W//2;by=H-100;bvx=4;bvy=-4;sc=0;lives=3
    cls=[RED,ORANGE,YELLOW,GREEN,BLUE]
    def mk(): return [pygame.Rect(c*70+65,r*25+70,65,20) for r in range(5) for c in range(12)]
    bricks=mk()
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        px=max(pw//2,min(W-pw//2,pygame.mouse.get_pos()[0]))
        bx+=bvx;by+=bvy
        if bx<=5 or bx>=W-5: bvx=-bvx
        if by<=55: bvy=abs(bvy)
        if by>=H:
            lives-=1;bx,by,bvx,bvy=W//2,H-100,4,-4
            if lives<=0:
                r2=game_over(sc,high_scores,"Brick Smasher")
                if r2=="r": bricks=mk();sc=0;lives=3
                else: return
        pr=pygame.Rect(px-pw//2,H-35,pw,12)
        if pr.collidepoint(bx,by): bvy=-abs(bvy);bvx=((bx-px)/(pw//2))*5
        for b in bricks[:]:
            if b.collidepoint(bx,by):
                row=(b.y-70)//25;emit(b.centerx,b.centery,cls[row%5],8)
                bricks.remove(b);bvy=-bvy;sc+=15;break
        if not bricks: bricks=mk()
        screen.fill(BG2); draw_stars(screen)
        for b in bricks:
            row=(b.y-70)//25;pygame.draw.rect(screen,cls[row%5],b,border_radius=3)
        pygame.draw.rect(screen,CYAN,pr,border_radius=4)
        pygame.draw.circle(screen,YELLOW,(int(bx),int(by)),6)
        tick_particles(screen); hud("BRICK SMASHER",sc,f"Lives:{lives}")
        pygame.display.flip()

def g_laser():
    px=W//2;py=H//2;sc=0;dead=False;lasers=[];lcd=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
        if not dead:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: px=max(15,px-5)
            if keys[pygame.K_RIGHT]: px=min(W-15,px+5)
            if keys[pygame.K_UP]: py=max(65,py-5)
            if keys[pygame.K_DOWN]: py=min(H-15,py+5)
            sc+=1;lcd+=dt
            if lcd>max(400,1500-sc//3):
                lcd=0
                if random.random()<.5: lasers.append({"t":"h","p":random.randint(60,H-10),"w":800,"l":300})
                else: lasers.append({"t":"v","p":random.randint(10,W-10),"w":800,"l":300})
            for l in lasers:
                if l["w"]>0: l["w"]-=dt
                else: l["l"]-=dt
            for l in lasers[:]:
                if l["l"]<=0 and l["w"]<=0: lasers.remove(l);continue
                if l["w"]<=0:
                    if l["t"]=="h" and abs(py-l["p"])<8: dead=True;emit(px,py,RED,25)
                    if l["t"]=="v" and abs(px-l["p"])<8: dead=True;emit(px,py,RED,25)
        screen.fill(BG2); draw_stars(screen)
        for l in lasers:
            if l["w"]>0:
                if l["t"]=="h": pygame.draw.line(screen,(80,0,0),(0,l["p"]),(W,l["p"]),1)
                else: pygame.draw.line(screen,(80,0,0),(l["p"],55),(l["p"],H),1)
            else:
                if l["t"]=="h": pygame.draw.line(screen,RED,(0,l["p"]),(W,l["p"]),4)
                else: pygame.draw.line(screen,RED,(l["p"],55),(l["p"],H),4)
        if not dead: pygame.draw.circle(screen,CYAN,(int(px),int(py)),10)
        tick_particles(screen); hud("LASER DODGE",sc,"Arrows to dodge")
        if dead:
            r2=game_over(sc,high_scores,"Laser Dodge")
            if r2=="r": px=W//2;py=H//2;sc=0;dead=False;lasers.clear()
            else: return
        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAMES 25-32 : SKILL & STRATEGY
# ═══════════════════════════════════════════════════════════════
def g_tower():
    path=[(0,350),(200,350),(200,150),(500,150),(500,500),(800,500),(800,250),(W,250)]
    towers=[];enemies=[];buls=[];sc=0;money=100;lives=10;wave=0;st=0;eq=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and money>=25:
                mx,my=ev.pos
                if my>55:
                    ok=True
                    for i in range(len(path)-1):
                        p1,p2=path[i],path[i+1]
                        if min(p1[0],p2[0])-30<mx<max(p1[0],p2[0])+30 and min(p1[1],p2[1])-30<my<max(p1[1],p2[1])+30:
                            ok=False
                    if ok: towers.append({"x":mx,"y":my,"cd":0,"rng":120});money-=25
        if eq<=0 and not enemies: wave+=1;eq=wave*3+5
        st+=dt
        if st>600 and eq>0:
            st=0;eq-=1;hp=30+wave*10
            enemies.append({"seg":0,"t":0.0,"hp":hp,"mhp":hp,"sp":1+wave*.1})
        for e in enemies[:]:
            if e["seg"]<len(path)-1:
                p1,p2=path[e["seg"]],path[e["seg"]+1]
                d=math.hypot(p2[0]-p1[0],p2[1]-p1[1])
                e["t"]+=e["sp"]/d
                if e["t"]>=1: e["t"]=0;e["seg"]+=1
            else: lives-=1;enemies.remove(e)
        for t in towers:
            t["cd"]-=dt
            if t["cd"]<=0:
                for e in enemies:
                    if e["seg"]<len(path)-1:
                        p1,p2=path[e["seg"]],path[e["seg"]+1]
                        ex=p1[0]+(p2[0]-p1[0])*e["t"];ey=p1[1]+(p2[1]-p1[1])*e["t"]
                        if math.hypot(ex-t["x"],ey-t["y"])<t["rng"]:
                            buls.append({"x":t["x"],"y":t["y"],"tx":ex,"ty":ey,"e":e});t["cd"]=500;break
        for b in buls[:]:
            dx=b["tx"]-b["x"];dy=b["ty"]-b["y"];d=math.hypot(dx,dy)
            if d<5:
                b["e"]["hp"]-=15;buls.remove(b)
                if b["e"]["hp"]<=0 and b["e"] in enemies:
                    enemies.remove(b["e"]);sc+=20;money+=10;emit(b["tx"],b["ty"],ORANGE,8)
            else: b["x"]+=dx/d*6;b["y"]+=dy/d*6
        if lives<=0:
            r2=game_over(sc,high_scores,"Tower Defense")
            if r2=="r": towers.clear();enemies.clear();buls.clear();sc=0;money=100;lives=10;wave=0;eq=0
            else: return
        screen.fill(BG2); draw_stars(screen)
        for i in range(len(path)-1):
            pygame.draw.line(screen,DGRAY,path[i],path[i+1],20)
            pygame.draw.line(screen,(50,50,70),path[i],path[i+1],2)
        for t in towers:
            pygame.draw.circle(screen,CYAN,(t["x"],t["y"]),15)
            pygame.draw.circle(screen,(0,150,200),(t["x"],t["y"]),t["rng"],1)
        for e in enemies:
            if e["seg"]<len(path)-1:
                p1,p2=path[e["seg"]],path[e["seg"]+1]
                ex=int(p1[0]+(p2[0]-p1[0])*e["t"]);ey=int(p1[1]+(p2[1]-p1[1])*e["t"])
                pygame.draw.circle(screen,RED,(ex,ey),8)
                bw=20;pygame.draw.rect(screen,(60,0,0),(ex-bw//2,ey-14,bw,4))
                pygame.draw.rect(screen,GREEN,(ex-bw//2,ey-14,int(bw*e["hp"]/e["mhp"]),4))
        for b in buls: pygame.draw.circle(screen,YELLOW,(int(b["x"]),int(b["y"])),3)
        tick_particles(screen); hud("TOWER DEFENSE",sc,f"Wave:{wave} $:{money} Lives:{lives}")
        pygame.display.flip()

def g_simon():
    colors=[RED,GREEN,BLUE,YELLOW]; rects=[pygame.Rect(W//2-130+i*70,250,60,60) for i in range(4)]
    seq=[];player=[];showing=True;si=0;st=0;sc=0;lv=1
    def next_round():
        nonlocal showing,si,st; seq.append(random.randint(0,3));showing=True;si=0;st=0
    next_round()
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and not showing:
                for i,rc in enumerate(rects):
                    if rc.collidepoint(ev.pos):
                        player.append(i);emit(rc.centerx,rc.centery,colors[i],8)
                        if player[-1]!=seq[len(player)-1]:
                            r2=game_over(sc,high_scores,"Simon Says")
                            if r2=="r": seq.clear();player.clear();sc=0;lv=1;next_round()
                            else: return
                        elif len(player)==len(seq):
                            sc+=lv*10;lv+=1;player.clear();next_round()
        if showing:
            st+=dt
            if st>600:
                st=0;si+=1
                if si>len(seq): showing=False;player=[]
        screen.fill(BG2); draw_stars(screen)
        txt(screen,f"Level {lv}",FB,GOLD,150)
        txt(screen,"Watch and repeat!" if showing else "Your turn!",FM,WHITE,190)
        for i,rc in enumerate(rects):
            bright = showing and si-1<len(seq) and si>0 and seq[si-1]==i
            co=tuple(min(255,c+80) for c in colors[i]) if bright else colors[i]
            pygame.draw.rect(screen,co,rc,border_radius=10)
        tick_particles(screen); hud("SIMON SAYS",sc,f"Level:{lv}")
        pygame.display.flip()

def g_typing():
    words=["python","arcade","gaming","pixel","level","score","power","magic","quest","cyber",
           "neon","turbo","hyper","ultra","super","flash","blitz","storm","force","blade",
           "swift","brave","light","spark","dream","frost","flame","shade","cloud","orbit"]
    current=random.choice(words);typed="";sc=0;timer=30000;wc=0
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_BACKSPACE: typed=typed[:-1]
                elif ev.unicode and ev.unicode.isalpha():
                    typed+=ev.unicode.lower()
                    if typed==current: sc+=len(current)*10;wc+=1;current=random.choice(words);typed=""
                    elif not current.startswith(typed): typed=""
        timer-=dt
        if timer<=0:
            r2=game_over(sc,high_scores,"Typing Speed")
            if r2=="r": sc=0;timer=30000;wc=0;typed="";current=random.choice(words)
            else: return
        screen.fill(BG2); draw_stars(screen)
        txt(screen,current,FH,CYAN,H//2-40)
        # show typed progress
        for i,ch in enumerate(current):
            co=GREEN if i<len(typed) and typed[i]==ch else(RED if i<len(typed) else GRAY)
            txt(screen,ch,FH,co,H//2+30,W//2-len(current)*14+i*28)
        txt(screen,f"Words: {wc}",FM,GOLD,H//2+90)
        hud("TYPING SPEED",sc,f"Time:{timer//1000}s"); pygame.display.flip()

def g_math():
    ops=['+','-','×']; a=b=0; op='+'; ans=0; inp=""; sc=0; timer=30000; streak=0
    def new_q():
        nonlocal a,b,op,ans
        op=random.choice(ops); a=random.randint(1,20); b=random.randint(1,20)
        if op=='+': ans=a+b
        elif op=='-': a,b=max(a,b),min(a,b);ans=a-b
        else: a=random.randint(1,12);b=random.randint(1,12);ans=a*b
    new_q()
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_BACKSPACE: inp=inp[:-1]
                elif ev.key==pygame.K_RETURN:
                    try:
                        if int(inp)==ans: sc+=10+streak*5;streak+=1;emit(W//2,H//2,GREEN,15)
                        else: streak=0;emit(W//2,H//2,RED,15)
                    except: streak=0
                    inp="";new_q()
                elif ev.unicode and (ev.unicode.isdigit() or ev.unicode=='-'): inp+=ev.unicode
        timer-=dt
        if timer<=0:
            r2=game_over(sc,high_scores,"Math Blitz")
            if r2=="r": sc=0;timer=30000;streak=0;inp="";new_q()
            else: return
        screen.fill(BG2); draw_stars(screen)
        txt(screen,f"{a} {op} {b} = ?",FH,CYAN,H//2-40)
        txt(screen,inp or "_",FB,WHITE,H//2+20)
        txt(screen,f"Streak: {streak}",FM,GOLD,H//2+70)
        tick_particles(screen); hud("MATH BLITZ",sc,f"Time:{timer//1000}s"); pygame.display.flip()

def g_colormatch():
    COLOR_NAMES=["RED","BLUE","GREEN","YELLOW","PURPLE","ORANGE"]
    COLOR_VALS=[RED,BLUE,GREEN,YELLOW,PURPLE,ORANGE]
    word_idx=0;color_idx=0;sc=0;timer=20000;lives=3
    def new_q():
        nonlocal word_idx,color_idx
        word_idx=random.randint(0,5);color_idx=random.randint(0,5)
    new_q()
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                match = word_idx==color_idx
                if ev.key==pygame.K_y:
                    if match: sc+=20;emit(W//2,H//2,GREEN,12)
                    else: lives-=1;emit(W//2,H//2,RED,12)
                    new_q()
                elif ev.key==pygame.K_n:
                    if not match: sc+=20;emit(W//2,H//2,GREEN,12)
                    else: lives-=1;emit(W//2,H//2,RED,12)
                    new_q()
        timer-=dt
        if timer<=0 or lives<=0:
            r2=game_over(sc,high_scores,"Color Match")
            if r2=="r": sc=0;timer=20000;lives=3;new_q()
            else: return
        screen.fill(BG2); draw_stars(screen)
        txt(screen,"Does the WORD match the COLOR?",FM,GRAY,H//2-80)
        txt(screen,COLOR_NAMES[word_idx],FH,COLOR_VALS[color_idx],H//2)
        txt(screen,"Y = Yes  |  N = No",FM,WHITE,H//2+70)
        tick_particles(screen); hud("COLOR MATCH",sc,f"Lives:{lives} Time:{timer//1000}s"); pygame.display.flip()

def g_pattern():
    grid_sz=4;cells=[[False]*grid_sz for _ in range(grid_sz)]
    pattern=[];player=[];showing=True;lv=1;sc=0;st=0;si=0
    CL=80;ox=(W-grid_sz*CL)//2;oy=150
    def new_round():
        nonlocal showing,si,st,pattern,player
        pattern=[]; player=[]
        for _ in range(lv+2):
            pattern.append((random.randint(0,grid_sz-1),random.randint(0,grid_sz-1)))
        showing=True;si=0;st=0
    new_round()
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.MOUSEBUTTONDOWN and not showing:
                mx,my=ev.pos
                for r in range(grid_sz):
                    for c in range(grid_sz):
                        rc=pygame.Rect(ox+c*CL,oy+r*CL,CL-4,CL-4)
                        if rc.collidepoint(mx,my):
                            player.append((r,c))
                            if player[-1]!=pattern[len(player)-1]:
                                r2=game_over(sc,high_scores,"Pattern Memory")
                                if r2=="r": sc=0;lv=1;new_round()
                                else: return
                            elif len(player)==len(pattern):
                                sc+=lv*20;lv+=1;new_round()
        if showing:
            st+=dt
            if st>500: st=0;si+=1
            if si>len(pattern): showing=False
        screen.fill(BG2); draw_stars(screen)
        txt(screen,f"Level {lv} - {'Watch!' if showing else 'Repeat!'}",FB,GOLD,100)
        for r in range(grid_sz):
            for c in range(grid_sz):
                rc=pygame.Rect(ox+c*CL,oy+r*CL,CL-4,CL-4)
                active=showing and 0<si<=len(pattern) and pattern[si-1]==(r,c)
                co=CYAN if active else DGRAY
                pygame.draw.rect(screen,co,rc,border_radius=8)
        tick_particles(screen); hud("PATTERN MEMORY",sc,f"Level:{lv}"); pygame.display.flip()

def g_wordscramble():
    words=["python","arcade","gaming","puzzle","logic","brain","quest","magic","cyber","neon",
           "turbo","ultra","super","flash","blitz","storm","pixel","power","dream","light"]
    def scramble(w):
        l=list(w); random.shuffle(l)
        while ''.join(l)==w: random.shuffle(l)
        return ''.join(l)
    current=random.choice(words);scram=scramble(current);inp="";sc=0;timer=45000
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_BACKSPACE: inp=inp[:-1]
                elif ev.key==pygame.K_RETURN:
                    if inp.lower()==current: sc+=50;emit(W//2,H//2,GREEN,15)
                    else: emit(W//2,H//2,RED,10)
                    current=random.choice(words);scram=scramble(current);inp=""
                elif ev.unicode and ev.unicode.isalpha(): inp+=ev.unicode.lower()
        timer-=dt
        if timer<=0:
            r2=game_over(sc,high_scores,"Word Scramble")
            if r2=="r": sc=0;timer=45000;current=random.choice(words);scram=scramble(current);inp=""
            else: return
        screen.fill(BG2); draw_stars(screen)
        txt(screen,"Unscramble:",FM,GRAY,H//2-60)
        # draw each letter as a tile
        for i,ch in enumerate(scram):
            x=W//2-len(scram)*25+i*50;y=H//2-20
            pygame.draw.rect(screen,PURPLE,(x,y,44,44),border_radius=8)
            txt(screen,ch.upper(),FB,WHITE,y+22,x+22)
        txt(screen,inp or "_",FB,CYAN,H//2+60)
        tick_particles(screen); hud("WORD SCRAMBLE",sc,f"Time:{timer//1000}s"); pygame.display.flip()

def g_rhythm():
    lanes=4;lw=60;ox=(W-lanes*lw)//2;target_y=H-80
    notes=[];sc=0;streak=0;timer=30000;st=0
    LANE_KEYS=[pygame.K_d,pygame.K_f,pygame.K_j,pygame.K_k]
    LANE_COLS=[RED,GREEN,BLUE,YELLOW]
    while True:
        dt=clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();sys.exit()
            if check_back(ev): return
            if ev.type==pygame.KEYDOWN:
                for i,k in enumerate(LANE_KEYS):
                    if ev.key==k:
                        hit=False
                        for n in notes[:]:
                            if n[0]==i and abs(n[1]-target_y)<30:
                                sc+=10+streak;streak+=1;notes.remove(n)
                                emit(ox+i*lw+lw//2,target_y,LANE_COLS[i],8);hit=True;break
                        if not hit: streak=0
        timer-=dt
        if timer<=0:
            r2=game_over(sc,high_scores,"Rhythm Tap")
            if r2=="r": sc=0;streak=0;timer=30000;notes.clear()
            else: return
        st+=dt
        if st>max(200,500-sc//10):
            st=0;notes.append([random.randint(0,lanes-1),55])
        for n in notes: n[1]+=4
        for n in notes[:]:
            if n[1]>H: notes.remove(n);streak=0
        screen.fill(BG2); draw_stars(screen)
        for i in range(lanes):
            x=ox+i*lw; pygame.draw.rect(screen,(20,20,40),(x,55,lw-2,H-55))
            pygame.draw.rect(screen,LANE_COLS[i],(x,target_y-15,lw-2,30),2,border_radius=4)
        for n in notes:
            x=ox+n[0]*lw; pygame.draw.rect(screen,LANE_COLS[n[0]],(x+5,n[1]-10,lw-12,20),border_radius=6)
        txt(screen,"D  F  J  K",FM,WHITE,H-30)
        tick_particles(screen); hud("RHYTHM TAP",sc,f"Streak:{streak} Time:{timer//1000}s"); pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  GAME FUNCTION MAP
# ═══════════════════════════════════════════════════════════════
GAME_FUNCS = {
    "Snake":g_snake,"Pong":g_pong,"Breakout":g_breakout,"Asteroids":g_asteroids,
    "Space Invaders":g_invaders,"Tetris":g_tetris,"Pac-Runner":g_pacrunner,"Frogger":g_frogger,
    "Memory Match":g_memory,"Minesweeper":g_minesweeper,"2048":g_2048,"Sliding Puzzle":g_sliding,
    "Color Flood":g_colorflood,"Sudoku Mini":g_sudoku,"Connect Four":g_connect4,"Tic-Tac-Toe":g_tictactoe,
    "Flappy Bird":g_flappy,"Dodge Ball":g_dodge,"Aim Trainer":g_aim,"Whack-a-Mole":g_whack,
    "Reaction Test":g_reaction,"Catch Fruit":g_catch,"Brick Smasher":g_bricksmasher,"Laser Dodge":g_laser,
    "Tower Defense":g_tower,"Simon Says":g_simon,"Typing Speed":g_typing,"Math Blitz":g_math,
    "Color Match":g_colormatch,"Pattern Memory":g_pattern,"Word Scramble":g_wordscramble,"Rhythm Tap":g_rhythm,
}

# ═══════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════
def main_menu():
    global scroll_y
    selected_cat = 0
    hover_game = -1

    while True:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        hover_game = -1

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEWHEEL:
                scroll_y -= ev.y * 30
                scroll_y = max(0, min(scroll_y, 300))
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # category tabs
                tab_w = W // len(CATS)
                for i in range(len(CATS)):
                    if pygame.Rect(i * tab_w, 100, tab_w, 40).collidepoint(mx, my):
                        selected_cat = i; scroll_y = 0
                # game cards
                cat_name, games = CATS[selected_cat]
                for gi, gname in enumerate(games):
                    row, col = divmod(gi, 4)
                    cw, ch = 210, 80
                    gx = 50 + col * (cw + 20)
                    gy = 170 + row * (ch + 15) - scroll_y
                    if pygame.Rect(gx, gy, cw, ch).collidepoint(mx, my) and gy > 130:
                        if gname in GAME_FUNCS:
                            GAME_FUNCS[gname]()

        # Draw
        screen.fill(BG)
        draw_stars(screen)

        # Title
        t = time.time()
        title_colors = [CYAN, PINK, GREEN, YELLOW, PURPLE]
        for i, ch in enumerate("MEGA ARCADE"):
            c = title_colors[i % len(title_colors)]
            off = math.sin(t * 3 + i * 0.5) * 5
            char_surf = FH.render(ch, True, c)
            screen.blit(char_surf, (W//2 - 160 + i * 30, 25 + off))

        txt(screen, "32 Games  |  4 Categories  |  Endless Fun", FS, GRAY, 80)

        # Category tabs
        tab_w = W // len(CATS)
        for i, (cname, _) in enumerate(CATS):
            rect = pygame.Rect(i * tab_w, 100, tab_w, 40)
            active = i == selected_cat
            if active:
                pygame.draw.rect(screen, (*CAT_COLS[i], 40) if len(CAT_COLS[i]) == 3 else CAT_COLS[i],
                                 rect)
                pygame.draw.line(screen, CAT_COLS[i], (rect.x, rect.bottom - 2), (rect.right, rect.bottom - 2), 3)
            txt(screen, cname, FM if active else FS, CAT_COLS[i] if active else GRAY, rect.centery, rect.centerx)

        # Game cards
        cat_name, games = CATS[selected_cat]
        cat_col = CAT_COLS[selected_cat]
        for gi, gname in enumerate(games):
            row, col = divmod(gi, 4)
            cw, ch = 210, 80
            gx = 50 + col * (cw + 20)
            gy = 170 + row * (ch + 15) - scroll_y

            if gy < 130 or gy > H: continue

            rect = pygame.Rect(gx, gy, cw, ch)
            hover = rect.collidepoint(mx, my)

            # card bg
            if hover:
                pygame.draw.rect(screen, (*cat_col[:3], 30) if len(cat_col) >= 3 else cat_col, rect, border_radius=10)
                hover_game = gi

            pygame.draw.rect(screen, cat_col, rect, 2 if hover else 1, border_radius=10)

            # game number
            txt(screen, f"#{gi+1}", FT, GRAY, gy + 20, gx + 20)
            # game name
            txt(screen, gname, FM, WHITE if hover else GRAY, gy + 45, rect.centerx)

            # high score if exists
            hs_val = high_scores.get(gname, 0)
            if hs_val:
                txt(screen, f"★ {hs_val}", FT, GOLD, gy + 68, rect.centerx)

        # Footer
        pygame.draw.rect(screen, (15, 15, 35), (0, H - 30, W, 30))
        txt(screen, "ESC = Back  |  Click a game to play  |  Mouse wheel to scroll", FT, GRAY, H - 15)

        pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main_menu()