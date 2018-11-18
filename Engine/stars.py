"""
The following code is taken and modified from 
http://codeNtronix.com
http://twitter.com/codentronix

            3D Starfield Simulation
            Developed by Leonel Machava <leonelmachava@gmail.com>

            http://codeNtronix.com
            http://twitter.com/codentronix
"""
from random import randrange

class BackGround:
    def __init__(self, screen , resolution = (600,600), num_stars=200, max_depth=32):
        self.screen = screen
        self.num_stars  = num_stars
        self.max_depth  = max_depth
        self.resolution = resolution
        self.origin_x = self.resolution[0] / 2
        self.origin_y = self.resolution[1] / 2
        
        self.init_stars()

    def init_stars(self):
        """ Create the starfield """
        self.stars = []
        for i in range(self.num_stars):
            # A star is represented as a list with this format: [X,Y,Z]
            star = [randrange(-25,25), randrange(-25,25), randrange(1, self.max_depth)]
            self.stars.append(star)

    def move_and_draw_stars(self):
        """ Move and draw the stars """

        for star in self.stars:
            # The Z component is decreased on each frame.
            star[2] -= 0.19

            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star[2] <= 0:
                star[0] = randrange(-25,25)
                star[1] = randrange(-25,25)
                star[2] = self.max_depth

            # Convert the 3D coordinates to 2D using perspective projection.
            k = 128.0 / star[2]
            x = int(star[0] * k + self.origin_x)
            y = int(star[1] * k + self.origin_y)

            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < self.resolution[0] and 0 <= y < self.resolution[1]:
                size = (1 - float(star[2]) / self.max_depth) * 5
                shade = (1 - float(star[2]) / self.max_depth) * 255
                self.screen.fill((shade,shade,shade),(x,y,size,size))

