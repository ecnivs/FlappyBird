class Bird:
    def __init__(self, x, y , shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.counter = 0
        self.index = 0
        self.images = ["graphics/bird1.gif", "graphics/bird2.gif", "graphics/bird3.gif"]

    def update(self):
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.shape = self.images[self.index]

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.color(self.color)
        pen.shape(self.shape)
        pen.stamp()
