from PIL import Image, ImageFont, ImageDraw
import numpy as np
import random

class Bubble:
    """Game bubble"""

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.sprite_num = 0
        self.dead_time = 1

    def detect_collision(self, coord):
        return (self.x-coord[0])**2 + (self.y-coord[1])**2 < self.r**2

class Renderer:
    """Renders game"""

    def __init__(self, gm):
        self.fnt = ImageFont.truetype('assets/UbuntuMono-R.ttf', 40)
        self.bubble_imgs = [
            Image.open('assets/taco.png'),
            Image.open('assets/taco2.png'),
        ]
        self.bubble_pop_imgs = [
            Image.open('assets/taco.png'),
            Image.open('assets/taco2.png'),
        ]

        self.game_manager = gm

    def render(self):
        base = Image.new("RGB", (self.game_manager.dim[0], self.game_manager.dim[1]))
        pix = base.load()

        # render player
        for p in self.game_manager.player:
            pix[int(p[0]), int(p[1])] = (255,255,255)

        # render bubbles
        for b in self.game_manager.bubbles:
            if b.y > 0 and b.y < self.game_manager.dim[1]:
                b.sprite_num = (b.sprite_num + 1) % len(self.bubble_imgs)
                base.paste(self.bubble_imgs[b.sprite_num], (int(b.x - b.r/2),int(b.y - b.r/2)))

        for b in self.game_manager.dead_bubbles:
            if b.y > 0 and b.y < self.game_manager.dim[1]:
                b.sprite_num = min(b.sprite_num + 1, len(self.bubble_pop_imgs)-1)
                base.paste(self.bubble_pop_imgs[b.sprite_num], (int(b.x - b.r/2),int(b.y - b.r/2)))


        # render score
        scoreboard = Image.new("RGB", (300, 50), "white")
        context = ImageDraw.Draw(scoreboard)
        context.text((10,0), "Score: " + str(self.game_manager.player_points), font=self.fnt, fill=(0,0,255))
        scoreboard = scoreboard.transpose(Image.FLIP_LEFT_RIGHT)
        base.paste(scoreboard, (self.game_manager.dim[0]-310, self.game_manager.dim[1] - 60))

        base = base.resize(( int(base.size[0]*1.5), int(base.size[1]*1.5) ), Image.NEAREST)
        return np.array(base)

class GameManager:
    """Runs game"""

    def __init__(self, dim):
        self.player = []
        self.bubbles = beatmap2bubbles('assets/beatmap.csv')
        self.dead_bubbles = []
        self.player_points = 0
        self.dim = dim

    def update(self, points, time_step):
        self.player = points

        # move bubbles down
        for b in self.bubbles:
            b.y += 100 * time_step # SPEED

            if b.y > 0 and b.y < self.dim[1]:
                for p in self.player:
                    if b.detect_collision(p):
                        self.player_points = min(self.player_points + 1, 999999)
                        b.sprite_num = 0
                        self.dead_bubbles.append(b)
                        self.bubbles.remove(b)
                        break

        # process popped bubbles
        for b in self.dead_bubbles:
            b.dead_time -= time_step
            if b.dead_time < 0:
                self.dead_bubbles.remove(b)

    def reset(self):
        self.player_points = 0

# === Helpers ===

def generate_bubbles(n):
    """Generate random bubbles for testing"""
    bubbles = []
    for i in range(n):
        b = Bubble(random.randint(0, 800), i * -100, 10)
        bubbles.append(b)
    return bubbles

def beatmap2bubbles(fname):
    """Convert beatmap to bubbles"""
    bubbles = []
    with open(fname, 'r') as f:
        data = f.read().split('\n')

        for d in data:
            line = d.split(',')
            for i in range(1, 5):
                if line[i]:
                    bubbles.append(Bubble(20 + 150 * i - 75, int(float(line[0]) * -190 + 400), 10))
    return bubbles
