from PIL import Image, ImageFont, ImageDraw
import numpy as np
import random
#from scipy import wavfile

SPEED = 5

class Bubble:
    """Game bubble"""

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.sprite_num = 0

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
                base.paste(self.bubble_imgs[b.sprite_num], (b.x,b.y))

        # render score
        scoreboard = Image.new("RGB", (300, 50), "white")
        context = ImageDraw.Draw(scoreboard)
        context.text((10,0), "Score: " + str(self.game_manager.player_points), font=self.fnt, fill=(0,0,255))
        scoreboard = scoreboard.transpose(Image.FLIP_LEFT_RIGHT)
        base.paste(scoreboard, (self.game_manager.dim[0]-310, 10))

        base = base.resize(( int(base.size[0]*1.5), int(base.size[1]*1.5) ), Image.NEAREST)
        return np.array(base)

class GameManager:
    """Runs game"""

    def __init__(self, dim):
        self.player = []
        self.bubbles = generate_bubbles(10000)
        self.player_points = 0
        self.dim = dim

    def update(self, points, time_step):
        self.player = points

        # move bubbles down
        for b in self.bubbles:
            b.y += SPEED

            if b.y > 0 and b.y < self.dim[1]:
                for p in self.player:
                    if b.detect_collision(p):
                        self.player_points += 1
                        self.bubbles.remove(b)
                        break

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
        data = f.split('\n')

        for d in data:
            line = d.split(',')
            if line[0] == 'L':
                bubbles.append(Bubble(20, float(line[1]) * -100, 10))
            elif line[0] == 'R':
                bubbles.append(Bubble(620, float(line[1]) * -100, 10))
    return bubbles
