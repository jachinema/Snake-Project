import pygame as pg
import random

# initialization of pygame, screen, and base background
pg.init()
window = pg.display.set_mode((1920, 1080))
window.fill((7, 18, 7))
pg.display.update()


class Snake:  # core snake class
    def __init__(self, x, y, direction='right', parent=False):
        self.parent = self
        self.is_head = parent

        self.x = x
        self.y = y

        self.direction = direction

        self.segments = [self]
        self.color = (13, 97, 13)

    def add(self):  # add a new snake segment
        table = {
            'right': (self.segments[-1].x-1, self.y),
            'left': (self.segments[-1].x+1, self.y),
            'up': (self.x, self.segments[-1].y+1),
            'down': (self.x, self.segments[-1].y-1)
        }  # dictionsry to quickly and easily figure out and grab the correct coordinates for the situation

        child = Snake(*table[self.direction], self.direction)
        child.parent = self.segments[-1]
        self.segments.append(child)

    def draw(self): # simple method to draw head and all segments
        if self.is_head:
            window.fill((7, 18, 7))

        pg.draw.rect(window, self.color, (self.x*24, self.y*24, 18, 18))
        if self.is_head:
            for segment in self.segments[1:]:
                segment.draw()

            pg.display.update()

    def move(self):  # move the snake in the direction it is facing

        for segment in self.segments[::-1]:  # shift the coordinates of all segments to the coordinates of their parents
            segment.x, segment.y = segment.parent.x, segment.parent.y

        if self.is_head:  # shift the head's coordinates accordingly
            table = {
                self.direction == 'right': (1, 0),
                self.direction == 'left': (-1, 0),
                self.direction == 'up': (0, -1),
                self.direction == 'down': (0, 1)
            }
            nx, ny = table[True]
            self.x, self.y = self.x + nx, self.y + ny

        self.draw()  # draw all segments


def is_overlap(s):  # check if snake is overlapping with itself
    seen = set()
    for segment in s.segments:
        if (segment.x, segment.y) in seen:
            return True
        seen.add((segment.x, segment.y))
    return False


def gen_apple(s):  # safely generate an apple to avoid graphical artifacts and apples spawning on spaces taken by snake
    xs = {segment.x for segment in s.segments}
    ys = {segment.y for segment in s.segments}
    x, y = random.randint(0, 80), random.randint(0, 45)
    if x in xs:
        x += (-1)**(x == 0)
    if y in ys:
        y += (-1)**(y == 0)

    return x, y


def controller(snake):
    # map controls to a function to provide an access point for simulated controls by overwriting
    # __module_controller__
    keys = pg.key.get_pressed()

    if keys[pg.K_w] and snake.direction != 'down':
        snake.direction = 'up'

    elif keys[pg.K_a] and snake.direction != 'right':
        snake.direction = 'left'

    elif keys[pg.K_s] and snake.direction != 'up':
        snake.direction = 'down'

    elif keys[pg.K_d] and snake.direction != 'left':
        snake.direction = 'right'

    if is_overlap(snake):
        pg.quit()
        exit()


# hook controller to default function
__module_controller__ = controller

# create and draw snake
snake = Snake(5, 5, parent=True)
snake.add()
snake.draw()

# create and draw apple
apple = (9, 5)
pg.draw.rect(window, (161, 8, 8), (apple[0]*24, apple[1]*24, 18, 18))
pg.display.update()

# set up framerate
frame = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    if frame == 6000:
        # check if frame is an "active" frame, to avoid super-fast movement without halting all calculations
        snake.move()  # snake is moved regardless of input to match original game.
        pg.draw.rect(window, (161, 8, 8), (apple[0]*24, apple[1]*24, 18, 18))
        pg.display.update()
        frame = 0

        if (snake.x, snake.y) == apple:  # check if snake has reached an apple
            snake.add()
            apple = gen_apple(snake)
            pg.draw.rect(window, (161, 8, 8), (apple[0]*24, apple[1]*24, 18, 18))
            pg.display.update()
            # note: we dont need to redraw the apple conviently because "running over it" will do that implicitly.

    __module_controller__(snake) # listen for input from whatever controller is connected

    frame += 1 # advance framerate
