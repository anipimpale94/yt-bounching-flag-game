import pygame
import random
from math import sqrt, atan2, sin, cos, radians, pi
from config import g, fps, centx, centy, bigr, GAP_SEGMENT_DEG, JERK_ANGLE_DEG
from utils import dot, angle_in_gap

from game_object import GameObject

class Balls(GameObject):
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


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius, self.thicc)
    
    def collision_handling(self, ring_angle):
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
            try:
                # Use absolute path or relative to CWD if running from there?
                # The original code assumed CWD is correct.
                # However, repeated sound loading might be heavy. Ideally load once.
                # But for now keeping original logic roughly (load on fly if not loaded?)
                # original: pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))
                pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))
            except Exception:
                pass # Fail silently if audio missing

            while sqrt((x-self.posx)**2 + (y-self.posy)**2) > (bigr - self.radius):
                step = 0.2
                # moving the ball backwawrds in dir of velocity by small steps
                safe_vel = vel if vel != 0 else 0.1
                self.posx += -self.velx*step/safe_vel
                self.posy -= -self.vely*step/safe_vel
                
            normal = ballx - x, bally - y
            normal_mag = center_to_ball #sqrt(normal[0]**2 + normal[1]**2)
            if normal_mag == 0: normal_mag = 1 # avoid div/0
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

    def update(self, frames):

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

# Helper for accessing frames count or we need to pass frames to motion?
# In original code, `frames` was a global variable incremented in main loop.
# `motion` used `frames`.
# I need to handle `frames` dependency.
# Option 1: Pass `frames` to `motion`.
# Option 2: Use a getter from checking time or similar? No, frames is a counter.
# I will Refactor `motion` to accept `frames`.

# Wait - I already wrote the file content above. 
# `frames` is used in `motion`.
# I need to update `motion` signature to `motion(self, frames)`.
# Let me correct the content before writing, or I will need to edit it.
# The tool call above has `frames_count()` placeholder which I need to define or replace.
# I'll restart the write_to_file with `motion(self, frames)`
