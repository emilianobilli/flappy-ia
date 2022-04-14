import pygame, sys, math
from random import randrange
from pygame.locals import *

# Start pygame
pygame.init()


class Pipes(object):

    # Class Var
    width = 20
    start_position = 600
    gap = 170
    height_min_range = 210
    speed = -15 #10

    # Randomize pipe location
    def __init__(self, ground_level):
        self.height = randrange(self.height_min_range, ground_level - 10)
        self.position = Pipes.start_position
        self.replaced = False
        self.scored = False
        self.distance = ()

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

    def __init__(self, position, bird_color, bid, brain):
        self.bird_color = bird_color
        self.position   = position
        self.id = bid
        self.brain = brain
        self.score = 0
        self.distance = ()
        self.die = False
        self.speed = 0
        self.gravity = 1
        

    def draw(self, surface):
        x, y = self.position
        position = ( int(math.floor(x)), int(math.floor(y)) )
        pygame.draw.circle(surface, self.bird_color, position, self.radius)


    def move(self):
        x, y = self.position
        mx, my = (0,self.speed)

        if( (y + my + self.radius) < self.ground_level ):
            self.position = (x + mx, y + my)
            return True #Return if we successfuly moved
        self.position = (x, self.ground_level - self.radius)
        return False

    def collision(self, pipe):
        x, y = self.position
        collide_width  = ( pipe.position < x + self.radius and x - self.radius < pipe.position + pipe.width)
        collide_top    = ( pipe.height - pipe.gap > y - self.radius )
        collide_bottom = ( y + self.radius > pipe.height )
        if ( collide_width and ( collide_top or collide_bottom)):
            return True
        return False

    def calculate_distance(self, pipe):
        if not self.die:
            distance_x = pipe.position - self.position[0] #+ self.bird.radius
            distance_y = (pipe.height - pipe.gap / 2) - self.position[1]
            self.distance = (distance_x,distance_y)
            print(self.id, self.distance)

    def compute(self):
        result = self.brain(self.distance)[0]
        print(self.id, result)
        if result == 1:
            self.speed = -10

        self.speed = self.speed + self.gravity

        if (self.move() == False):
            self.die = True
        

class Game(object):
    bird_color = None
    ground_color = None
    ground_level = None
    collide_color = None
    background_color = None
    font_color = None
    font_object = None
    brain = None

    def __init__(self, anns):
        self.window_object = pygame.display.set_mode( ( 640, 480) )
        self.score = 0
        self.pipes = [Pipes(self.ground_level)]
        self.bird  = [] 
        for ann in anns:
            self.bird.append(Bird((self.window_object.get_width() / 4 , self.window_object.get_height() / 2), self.bird_color, ann.ann_id, ann.brain))
        
    #    self.gravity = 1
    #    self.speed = 0
        

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
        
        distance_x = self.pipes[0].position - self.bird[0].position[0] + self.bird[0].radius
        distance_y = (self.pipes[0].height - self.pipes[0].gap / 2) - self.bird[0].position[1]

        for bird in self.bird:
            bird.distance = (distance_x,distance_y)

        while True:

            self.window_object.fill(self.background_color)

            # Check for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.__pause_game()

            for bird in self.bird:
                bird.compute()

            n = False
            for pipe in self.pipes:
                if not pipe.replaced and pipe.position < self.window_object.get_width() / 2 :
                    self.pipes[len(self.pipes):] = [Pipes(self.ground_level)]
                    pipe.replaced = True
                pipe.draw(self.window_object, self.ground_color, self.ground_level)

                for bird in self.bird:
                    if (not bird.die and bird.collision(pipe)):
                        self.window_object.fill(self.collide_color)
                        bird.die = True

                if not pipe.scored: 
                    need_score = False
                    for bird in self.bird:
                        if bird.die == False and pipe.position + pipe.width < bird.position[0] + bird.radius:
                            bird.score = bird.score + 1
                            need_score = True
                
                    if need_score:
                        pipe.scored = True
    
                if( not pipe.move(pipe.speed) ):
                    del pipe
                else:
                    if not pipe.scored and not n:
                        n = True
                        for bird in self.bird:
                            print('Recalculando')
                            bird.calculate_distance(pipe)

            # Draw stuff
            #if self.brain:
            #    score_surface = self.font_object.render( 'Score: %d High: %d - Dx: %d Dy: %d - Ind: %d Gen: %d' % (self.score, self.high_score, distance_x, distance_y,self.ind, self.generation), False, self.font_color)
            #else:
            #    score_surface = self.font_object.render( 'Score: %d High: %d - Dx: %d Dy: %d' % (self.score, self.high_score, distance_x, distance_y), False, self.font_color)

            #score_rect    = score_surface.get_rect()
            #score_rect.topleft = (self.window_object.get_height() / 2 , 10)
            #self.window_object.blit(score_surface, score_rect)
            pygame.draw.rect(self.window_object, self.ground_color, (0, self.ground_level, self.window_object.get_width(), self.window_object.get_height()) )

            die_all = True

            for bird in self.bird:
                if not bird.die:
                    die_all = False
                    bird.draw(self.window_object)
        
            if die_all:
                ret = []
                for bird in self.bird:
                    ret.append({'ann_id': bird.id, 'fitness': bird.score})
                return ret
                
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
Pipes.gap   = 170

# Bird Configuration
Bird.radius = 10
Bird.ground_level = Game.ground_level

if __name__ == '__main__':
    while True:
        mg = Game(high_score)
        score = mg.start()
        if score > high_score:
            high_score = score