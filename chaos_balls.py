from pygame.gfxdraw import circle
# from reflection import arrow, yellow
import pygame
import os
import time as t
from math import acos, atan2, sin, cos, sqrt, pi, radians
import random
# import math
from test import dot, simul

# Game presets
start_time = t.time()
fps = 120
width, height = 800, 600

# Centers window
x, y = 1360 - width, 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing balls")
clock = pygame.time.Clock()

background = pygame.image.load("img/start_img.png")

# initialize pygame mixer and load audio file
pygame.mixer.init()
# pygame.mixer.music.load('audio/golf_ball.wav')  # audio options [golfball, ground_impact, metalmicrowave, golf_ball]

# font = pygame.font.Font('freesansbold.ttf', 15)

white        = (255, 255, 255)
whitest      = (204, 234, 234)
# grey       = (45 ,  45,  45)
grey         = ( 27,  27,  27)
black        = (  0,   0,   0)
blackcoral   = ( 39,  22,  16)
deepblue     = (  0,   4,  30)
red          = (225,  40,  40)
green        = ( 10, 200,  27)
yellowish    = (191, 202,  37)
orange       = (255,  72,   0)
velvet       = (232,  20,  20)
bluish_white = (179, 255, 251)
blue         = (17 , 200, 251)
tastyellow   = (255, 230,   0)
arrow_color  = (255, 255, 255)
golden       = (255, 166,  32)
golden       = (245, 170,  10)
algeablue    = (7  , 197,  70)
magenta      = (255,  13, 130)
magenta2     = (214,   0, 100)
bg = deepblue

# 27 balls: (name, (r,g,b))
BALL_CONFIGS = [
    ("Golden", (245, 170, 10)), ("Red", (225, 40, 40)), ("Green", (10, 200, 27)), ("Blue", (17, 200, 251)),
    ("Orange", (255, 72, 0)), ("Yellow", (255, 230, 0)), ("Cyan", (0, 200, 200)), ("Magenta", (255, 13, 130)),
    ("Lime", (50, 255, 50)), ("Teal", (0, 128, 128)), ("Navy", (0, 0, 128)), ("Purple", (128, 0, 128)),
    ("Coral", (255, 127, 80)), ("Pink", (255, 192, 203)), ("Brown", (139, 69, 19)), ("Olive", (128, 128, 0)),
    ("Maroon", (128, 0, 0)), ("Turquoise", (64, 224, 208)), ("Violet", (238, 130, 238)), ("Crimson", (220, 20, 60)),
    ("Silver", (192, 192, 192)), ("Sky", (135, 206, 235)), ("Salmon", (250, 128, 114)), ("Plum", (221, 160, 221)),
    ("Mint", (152, 255, 152)), ("Cream", (255, 253, 208)), ("Lavender", (230, 230, 250)),
]

# g = -0.1
g = -9.81
RING_MARGIN = 50  # space between ring outer edge and screen edge
bigr = min(width, height)//2 - RING_MARGIN  # radius of ring
centx, centy = width//2, height//2  # center of circle
SPAWN_RADIUS = 25  # small circle around center where balls respawn
frames = 0
ring_angle = 0  # rotation of outer ring (degrees)
RING_SPIN_SPEED = 0.5  # degrees per frame (slower spin)
JERK_ANGLE_DEG = 6  # random direction change on ring bounce (degrees, ±this)
# Escape zone must match visual gap exactly: [ring_angle, ring_angle + GAP_SEGMENT_DEG)
class Balls():
    trail = False  # set True to show ball path
    balls = list()
    def __init__(self, name, color, radius, thicc, posx, posy, sound="metalmicrowave.wav"):
        Balls.balls.append(self)
        
        self.name   = name
        self.color  = color
        self.radius = radius
        self.thicc  = thicc
        self.posx   = posx
        self.posy   = posy
        self.sound  = f"audio/{sound}"
        self.velx   = 0
        self.vely   = 0
        self.acc    = g/fps
        self.track  = list()
        self.escaped = False
        self.wins = 0


    def drawball(self):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius, self.thicc)
    
    def collision_handling(self):
        vel = sqrt(self.velx**2 + self.vely**2)
        # vel = 2 if vel >= 2 else vel

        x,y = centx, centy # center of cirlce
        ballx, bally = self.posx, self.posy
        velx, vely = self.velx, self.vely
        # center to ball is the distance between ball's center and the ring's center
        center_to_ball = sqrt((x-ballx)**2 + (y-bally)**2)
        


        if center_to_ball >= (bigr - self.radius):
            # Ball angle must use same convention as pygame.draw.arc: 0=right, 90=up (math convention, y-up)
            ball_angle_rad = atan2(y - bally, ballx - x)
            if angle_in_gap(ball_angle_rad, ring_angle, GAP_SEGMENT_DEG):
                self.escaped = True
                return
            # play bounce sound effect
            pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))

            while sqrt((x-self.posx)**2 + (y-self.posy)**2) > (bigr - self.radius):
                step = 0.2
                # moving the ball backwawrds in dir of velocity by small steps
                self.posx += -self.velx*step/vel
                self.posy -= -self.vely*step/vel

                
            normal = ballx - x, bally - y
            normal_mag = center_to_ball #sqrt(normal[0]**2 + normal[1]**2)
            n = normal[0]/normal_mag, normal[1]/normal_mag
            nx, ny = n[0], n[1]

            d = velx, -vely # incident
            dx, dy = d[0], d[1]

            reflected = dx-2*dot(n,d)*nx, dy-2*dot(n,d)*ny

            self.velx = reflected[0]
            self.vely = -reflected[1]

            # little jerk on ring hit: rotate velocity by random angle, keep speed
            speed = sqrt(self.velx**2 + self.vely**2)
            if speed > 1e-6:
                angle = atan2(-self.vely, self.velx)
                jerk_rad = radians(random.uniform(-JERK_ANGLE_DEG, JERK_ANGLE_DEG))
                self.velx = speed * cos(angle + jerk_rad)
                self.vely = -speed * sin(angle + jerk_rad)

            # a shitty fix to speed's gradual loss

            # r_size = sqrt(self.velx**2 + self.vely**2)
            # self.velx = reflected[0]*vel/r_size
            # self.vely = -reflected[1]*vel/r_size


    def motion(self):

        self.velx += 0
        self.vely += self.acc

        self.posx += self.velx
        self.posy -= self.vely

        every   = 2
        period  = 5
        if frames % every == 0 and Balls.trail:
            self.track.append((self.posx, self.posy))
        if Balls.trail is False:
            self.track.clear()
        elif len(self.track) > fps*period/every : #240:
            self.track.pop(0)
        


def draw_cricle(color, radius, thicc, posx, posy):
    pygame.draw.circle(screen, color, (posx, posy), radius, thicc)


def angle_in_gap(ball_angle_rad, gap_start_deg, gap_span_deg):
    """True iff ball angle lies in [gap_start_deg, gap_start_deg + gap_span_deg) — same convention as draw_arc."""
    ball_deg = (ball_angle_rad * 180 / pi) % 360.0
    start = gap_start_deg % 360.0
    end = (gap_start_deg + gap_span_deg) % 360.0
    if start < end:
        return start <= ball_deg < end
    # gap wraps (e.g. [350°, 10°))
    return ball_deg >= start or ball_deg < end


GAP_SEGMENT_DEG = 30  # angular width of the single escape hole (degrees)


def draw_spinning_ring(radius, cx, cy, angle_deg, color_bright, color_dim, gap_half_deg=None, num_segments=24, thickness=2):
    """Draw the ring as one arc that skips exactly one gap. Angles in [0, 2*pi) to avoid wrap seam."""
    rect = (cx - radius, cy - radius, 2 * radius, 2 * radius)
    # Gap: angle_deg to angle_deg + GAP_SEGMENT_DEG. Draw the rest: from (angle_deg + GAP_SEGMENT_DEG) to angle_deg (counter‑clockwise).
    start_rad = radians((angle_deg + GAP_SEGMENT_DEG) % 360)
    end_rad = radians(angle_deg % 360)
    # Arc goes counter‑clockwise; when start > end we wrap (e.g. 35°→360°→20°). Never pass end > 2*pi.
    pygame.draw.arc(screen, color_bright, rect, start_rad, end_rad, thickness)



# 4 balls with different colors, random start directions
speed = 4
# Create 27 balls, spread on spawn circle at startup
for i, (name, color) in enumerate(BALL_CONFIGS):
    angle = 2 * pi * i / len(BALL_CONFIGS)
    px = centx + SPAWN_RADIUS * cos(angle)
    py = centy - SPAWN_RADIUS * sin(angle)
    Balls(name, color, 8, 0, px, py, "golf_ball.wav")

def reset_round():
    """Respawn each ball at a different spot in the spawn circle (90° apart + jitter), random direction."""
    for i, ball in enumerate(Balls.balls):
        ball.escaped = False
        ball.track.clear()
        # Different location per ball: 4 base angles (0°, 90°, 180°, 270°) + random jitter
        base_angle = 2 * pi * i / len(Balls.balls) + random.uniform(-0.15, 0.15)
        r = random.uniform(SPAWN_RADIUS * 0.4, SPAWN_RADIUS)
        ball.posx = centx + r * cos(base_angle)
        ball.posy = centy - r * sin(base_angle)
        # Random direction (different for each ball)
        vel_angle = random.uniform(0, 2 * pi)
        ball.velx = speed * cos(vel_angle)
        ball.vely = speed * sin(vel_angle)
        ball.acc = 0


for ball in Balls.balls:
    angle = random.uniform(0, 2 * pi)
    ball.velx = speed * cos(angle)
    ball.vely = speed * sin(angle)
    ball.acc = 0   # no gravity, straight lines between bounces


pause = False
start_sim = False 


while start_sim is False:
    screen.fill(bg)
    # Centered content only (no background image to avoid overlapping text)
    try:
        title_font = pygame.font.Font(None, 72)
        hint_font = pygame.font.Font(None, 40)
        title = title_font.render("Bouncing Balls", True, whitest)
        hint = hint_font.render("Press TAB to start", True, bluish_white)
        tr_title = title.get_rect(center=(width // 2, height // 2 - 35))
        tr_hint = hint.get_rect(center=(width // 2, height // 2 + 25))

        screen.blit(title, tr_title)
        screen.blit(hint, tr_hint)
    except Exception:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                start_sim = True

    pygame.display.update()
    clock.tick(fps)


while True:

    # draw_cricle(yellow, 2, 0, width//2, height//2)
    # draw(red, height//3, 3, width//2, height//2)
    

    screen.fill(bg)
    # Top 3 score card at top
    try:
        counter_font = pygame.font.Font(None, 36)
        top3 = sorted(Balls.balls, key=lambda b: b.wins, reverse=True)[:3]
        parts = [f"{b.name}: {b.wins}" for b in top3]
        counter_text = counter_font.render("  |  ".join(parts), True, whitest)
        tr_counter = counter_text.get_rect(midtop=(width // 2, 12))
        screen.blit(counter_text, tr_counter)
    except Exception:
        pass

    draw_spinning_ring(bigr, centx, centy, ring_angle, whitest, grey, num_segments=24, thickness=2)
    if not pause:
        ring_angle = (ring_angle + RING_SPIN_SPEED) % 360

    active_balls = [b for b in Balls.balls if not b.escaped]
    if len(active_balls) <= 1:
        if len(active_balls) == 1:
            active_balls[0].wins += 1
        reset_round()
        active_balls = list(Balls.balls)
    for ball in active_balls:
        if len(ball.track) > 2 and Balls.trail:
            pygame.draw.aalines(screen, ball.color, False, ball.track, 2)
    for ball in active_balls:
        ball.drawball()
        if not pause:
            ball.collision_handling()
            ball.motion()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_t:
                Balls.trail = not Balls.trail
                # if trail is False:
                #     for ball in Balls.balls:
                #         ball.track.clear()
    

    pygame.display.update()
    clock.tick(fps)
    frames += 1


























# vel = redball.vel
# arrow(arrow_color, arrow_color, (redball.posx, redball.posy), (redball.posx+vel*10*cos(redball.theta), redball.posy-vel*10*sin(redball.theta)), 1)
# rect = [redball.posx - 15 ,redball.posy-15, 30,30]
# pygame.draw.line(screen, orange, (redball.posx, redball.posy), (redball.posx +25, redball.posy), 2 )
# pygame.draw.rect(screen, yellow, rect, 4)
# draw_cricle(red, 2, 0, redball.posx-15, redball.posy-15)
# pygame.draw.arc(screen, white, rect, 0, redball.theta, 2)
# arrow(arrow_color, arrow_color, (greenball.posx, greenball.posy), (greenball.posx+vel*10*cos(greenball.theta), greenball.posy-vel*10*sin(greenball.theta)), 1)
    
    