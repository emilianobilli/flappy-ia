import pygame, sys, math
from random import randrange
from pygame.locals import *

# Start pygame
pygame.init()


class Pipes(object):

    # Class Var
    width = 20
    start_position = 600
    gap = 150
    height_min_range = 210
    speed = -15 #10

    # Randomize pipe location
    def __init__(self, ground_level):
        self.height = randrange(self.height_min_range, ground_level - 10)
        self.position = Pipes.start_position
        self.replaced = False
        self.scored = False

    # Moves the pipes along the ground, checks if they're off the screen
    def move(self, movement):
        self.position += movement
        if( self.position + self.width < 0 ):
            return False #Return false if we moved off the screen 
        return True

    # Handles drawing the pipes to the screen
    def draw(self, surface, ground_color, ground_level):
        pygame.draw.rect( surface, ground_color, (self.position, self.height, self.width, ground_level - self.height))
        pygame.draw.rect( surface, ground_color, (self.position, 0, self.width, self.height - self.gap))


class Bird(object):
    radius = 0
    ground_level = None

    def __init__(self, position, bird_color):
        self.bird_color = bird_color
        self.position   = position
        

    def draw(self, surface):
        x, y = self.position
        position = ( int(math.floor(x)), int(math.floor(y)) )
        pygame.draw.circle(surface, self.bird_color, position, self.radius)


    def move(self, movement, ground_level):
        x, y = self.position
        mx, my = movement

        if( (y + my + self.radius) < ground_level ):
            self.position = (x + mx, y + my)
            return True #Return if we successfuly moved
        self.position = (x, ground_level - self.radius)
        return False

    def collision(self, pipe):
        x, y = self.position
        collide_width  = ( pipe.position < x + self.radius and x - self.radius < pipe.position + pipe.width)
        collide_top    = ( pipe.height - pipe.gap > y - self.radius )
        collide_bottom = ( y + self.radius > pipe.height )
        if ( collide_width and ( collide_top or collide_bottom)):
            return True
        return False

class Game(object):
    bird_color = None
    ground_color = None
    ground_level = None
    collide_color = None
    background_color = None
    font_color = None
    font_object = None
    brain = None

    def __init__(self, high_score, ind=0, generation=0):
        self.window_object = pygame.display.set_mode( ( 640, 480) )
        self.score = 0
        self.pipes = [Pipes(self.ground_level)]
        self.bird  = Bird((self.window_object.get_width() / 4 , self.window_object.get_height() / 2), self.bird_color)
        self.gravity = 1
        self.speed = 0
        self.high_score = high_score
        self.ind = ind
        self.generation = generation

    def __quit(self):
        pygame.quit()
        sys.exit()

    def __pause_game(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__quit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pause = False
        return



    def start(self):
        
        distance_x = self.pipes[0].position - self.bird.position[0] + self.bird.radius
        distance_y = (self.pipes[0].height - self.pipes[0].gap / 2) - self.bird.position[1]

        while True:

            self.window_object.fill(self.background_color)

            # Check for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.__pause_game()

                    if self.brain is None:
                        self.speed = -10
                    

            if self.brain:
                result = self.brain((distance_x,distance_y))[0][0]
                print(result)
                if result > 0.5:
                    self.speed = -10

            self.speed = self.speed + self.gravity

            if (self.bird.move((0,self.speed), self.ground_level) == False):
                return self.score

            n = False
            for pipe in self.pipes:
                if not pipe.replaced and pipe.position < self.window_object.get_width() / 2 :
                    self.pipes[len(self.pipes):] = [Pipes(self.ground_level)]
                    pipe.replaced = True
                pipe.draw(self.window_object, self.ground_color, self.ground_level)
                if (self.bird.collision(pipe)):
                    self.window_object.fill(self.collide_color)
                    return self.score
                if ( not pipe.scored and pipe.position + pipe.width < self.bird.position[0] + self.bird.radius ):
                    self.score = self.score + 1
                    pipe.scored = True
    
                if( not pipe.move(pipe.speed) ):
                    del pipe
                else:
                    if not pipe.scored and not n:
                        n = True
                        distance_x = pipe.position - self.bird.position[0] #+ self.bird.radius
                        distance_y = (pipe.height - pipe.gap / 2) - self.bird.position[1]

            # Draw stuff
            if self.brain:
                score_surface = self.font_object.render( 'Score: %d High: %d - Dx: %d Dy: %d - Ind: %d Gen: %d' % (self.score, self.high_score, distance_x, distance_y,self.ind, self.generation), False, self.font_color)
            else:
                score_surface = self.font_object.render( 'Score: %d High: %d - Dx: %d Dy: %d' % (self.score, self.high_score, distance_x, distance_y), False, self.font_color)

            score_rect    = score_surface.get_rect()
            score_rect.topleft = (self.window_object.get_height() / 2 , 10)
            self.window_object.blit(score_surface, score_rect)
            pygame.draw.rect(self.window_object, self.ground_color, (0, self.ground_level, self.window_object.get_width(), self.window_object.get_height()) )

            self.bird.draw(self.window_object)
        
            pygame.display.update()
            self.fps_timer.tick(self.max_fps)

# Set up resolution
Game.fps_timer = pygame.time.Clock()
Game.max_fps = 30
Game.ground_level = 400
Game.background_color = pygame.Color('#abcdef')
Game.bird_color = pygame.Color('#222222')
Game.ground_color = pygame.Color('#993333')
Game.collide_color = pygame.Color('#230056')
Game.font_color = pygame.Color('#FFFFFF')
Game.font_object = pygame.font.Font('/System/Library/Fonts/Supplemental/Arial.ttf', 16)

# Pipes Configuration
#Pipes.ground_level = Game.ground_level
#Pipes.ground_color = Game.ground_color
Pipes.width = 30
Pipes.gap   = 150

# Bird Configuration
Bird.radius = 10
Bird.ground_level = Game.ground_level

if __name__ == '__main__':
    high_score = 0
    while True:
        mg = Game(high_score)
        score = mg.start()
        if score > high_score:
            high_score = score