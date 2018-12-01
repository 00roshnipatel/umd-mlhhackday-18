from PIL import Image
import numpy as np
import random
#from scipy import wavfile

class Bubble:
    """Game bubble"""

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def detect_collision(self, coord):
        return (self.x-coord[0])**2 + (self.y-coord[1])**2 < self.r**2

class Renderer:
    """Renders game"""

    def __init__(self, gm):
        self.bubble_img = Image.open('assets/taco.png')

        self.game_manager = gm

    def render(self):
        base = Image.new("RGB", (800, 800))
        pix = base.load()

        # render player
        for p in self.game_manager.player:
            pix[int(p[0]), int(p[1])] = (255,255,255)

        # render bubbles
        for b in self.game_manager.bubbles:
            if b.y > 0:
                #base.paste(self.bubble_img, (b.x,b.y))
                pass

        return np.array(base)

class GameManager:
    """Runs game"""

    def __init__(self):
        self.player = []
        self.bubbles = generate_bubbles(10)
        self.player_points = 0

    def update(self, points, time_step):
        self.player = points

        # move bubbles down
        for b in self.bubbles:
            b.y += 1
            for p in self.player:
                if b.detect_collision(p):
                    self.player_points += 1
                    self.bubbles.remove(b)
                    print("score!")
                    break

    def reset(self):
        self.player_points = 0

# Helpers

def generate_bubbles(n):
    bubbles = []
    for i in range(n):
        b = Bubble(random.randint(0, 800), i * -100, 10)
        bubbles.append(b)
    return bubbles
