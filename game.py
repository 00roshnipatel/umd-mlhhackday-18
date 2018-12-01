from PIL import Image
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
        pass

class GameManager:
    """Runs game"""

    def __init__(self):
        self.player = []
        self.bubbles = [
            Bubble(80, 0, 10),
        ]
        self.player_points = 0

    def update(self, points, time_step):
        self.player = points

        # move bubbles down
        for b in self.bubbles:
            #b.y -= 1
            for p in self.player:
                if b.detect_collision(p):
                    self.player_points += 1
                    self.bubbles.remove(b)
                    print("score!")
                    break

    def reset(self):
        self.player_points = 0

class Track:
    """Track info for songs"""

    def __init__(self):
        self.song
        self.beat_data = []
