import pygame, time, random
from pygame.locals import *

### USER VARIABLES ###

FPS = 60
DISPLAY_FPS = False
INITIAL_SPEED = 15
SPEED_INCREMENT = 0.5
INITIAL_LENGTH = 5
SCORE_INCREMENT = 100

PASS_EDGES = True

display_width = 600
display_height = 800

squaresize = 20 #square size of snake and food (x&y)

### USER VARIABLES END ###

#initialise pygame
pygame.init()
pygame.font.init()

#colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)

#define fonts
font = pygame.font.SysFont('Arial', 75)
smallfont = pygame.font.SysFont('Arial', 30)
largefont = pygame.font.SysFont('Arial', 115)

#create window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

global score
score = 0

#calculates the number of horizontal and vertical positions (like a grid) and finds the centre position
xposes = display_width/squaresize
yposes = display_height/squaresize
centrepos = [int(xposes/2), (yposes/2)]


class Snake(object):
        def __init__(self):
            self.x = centrepos[0]
            self.y = centrepos[1]
            self.speed = INITIAL_SPEED
            self.timer = 1/self.speed

            self.direction = 'up'
            self.length = INITIAL_LENGTH

            self.positions = []
            for point in range(self.length):
                self.positions.append([centrepos[0], centrepos[1]+point])


        def move(self, dt):
            self.timer -= dt
            if self.timer > 0:
                return
            else:
                if self.direction == 'up':
                    self.up()

                elif self.direction == 'down':
                    self.down()

                elif self.direction == 'right':
                    self.right()

                elif self.direction == 'left':
                    self.left()

                self.x = self.positions[0][0]
                self.y = self.positions[0][1]
                self.timer = 1/self.speed

        def up(self):
            if PASS_EDGES:
                if self.positions[0][1] == 0:
                    newpiece = [self.positions[0][0], yposes-1]
                else:
                    newpiece = [self.positions[0][0], (self.positions[0][1])-1]
            else:
                newpiece = [self.positions[0][0], (self.positions[0][1])-1]

            if self.positions[1][1] != newpiece[1]:
                self.positions = self.positions[:-1]
                self.positions = [newpiece] + self.positions
            else:
                self.direction = 'down'
                self.down()

        def down(self):
            if PASS_EDGES:
                if self.positions[0][1] == yposes-1:
                    newpiece = [self.positions[0][0], 0]
                else:
                    newpiece = [self.positions[0][0], (self.positions[0][1])+1]
            else:
                newpiece = [self.positions[0][0], (self.positions[0][1])+1]

            if self.positions[1][1] != newpiece[1]:
                self.positions = self.positions[:-1]
                self.positions = [newpiece] + self.positions
            else:
                self.direction = 'up'
                self.up()

        def right(self):
            if PASS_EDGES:
                if self.positions[0][0] == xposes-1:
                    newpiece = [0, self.positions[0][1]]
                else:
                    newpiece = [(self.positions[0][0])+1, self.positions[0][1]]
            else:
                newpiece = [(self.positions[0][0]) + 1, self.positions[0][1]]

            if self.positions[1][0] != newpiece[0]:
                self.positions = self.positions[:-1]
                self.positions = [newpiece] + self.positions
            else:
                self.direction = 'left'
                self.left()

        def left(self):
            if PASS_EDGES:
                if self.positions[0][0] == 0:
                    newpiece = [xposes-1, self.positions[0][1]]
                else:
                    newpiece = [(self.positions[0][0])-1, self.positions[0][1]]
            else:
                newpiece = [(self.positions[0][0]) - 1, self.positions[0][1]]

            if self.positions[1][0] != newpiece[0]:
                self.positions = self.positions[:-1]
                self.positions = [newpiece] + self.positions
            else:
                self.direction = 'right'
                self.right()


        def draw(self, surface):
            for point in self.positions:
                pygame.draw.rect(surface, green, [point[0] * squaresize, point[1] * squaresize, squaresize, squaresize])

        def grow(self):
            self.speed += SPEED_INCREMENT #increases speed by the set increment
            self.length += 1

            #takes the last two positions of the snake and finds the x,y coordinates for an additional piece added on the end
            last = self.positions[-1]
            secondlast = self.positions[-2]

            #finds the x coordinate
            if last[0] == secondlast[0]:
                xpos = last[0]
            elif last[0]-secondlast[0] == 1:
                xpos = last[0]+1
            elif last[0]-secondlast[0] == -1:
                xpos = last[0]-1

            #finds the y coordinate
            if last[1] == secondlast[1]:
                ypos = last[1]
            elif last[1]-secondlast[1] == 1:
                ypos = last[1]+1
            elif last[1]-secondlast[1] == -1:
                ypos = last[1]-1
            
            self.positions.append([xpos, ypos])

        def detect(self, food):
            #detects if the snake head is over the food
            if self.x == food.x and self.y == food.y:
                food.new(self) #generates a new piece of food
                global score
                score += SCORE_INCREMENT #increases the player's score
                self.grow()


            #check is snake is within the screen
            if not PASS_EDGES:
                if self.x*squaresize < 0 or (self.x*squaresize)+squaresize > display_width or self.y*squaresize < 0 or (self.y*squaresize)+squaresize > display_height:
                    return True
               
            #checks if the head is crossing any other parts of the snake body
            positions = iter(self.positions)
            next(positions)
            for position in positions:
                if position == self.positions[0]:
                    return True

            return False


#food class
class Food(object):
    def __init__(self, snake):
        self.x = random.randint(0, xposes-1)
        self.y = random.randint(0, yposes-1)

        for square in snake.positions:
            if self.x != square[0] and self.y !=square[1]:
                pass
            else:
                self.new(snake)

    def draw(self, surface):
        pygame.draw.rect(surface, red, [self.x*squaresize, self.y*squaresize, squaresize, squaresize])

    def new(self, snake):
        self.x = random.randint(0, xposes-1)
        self.y = random.randint(0, yposes-1)

        for square in snake.positions:
            if self.x != square[0] and self.y !=square[1]:
                pass
            else:
                self.new(snake)
        
class Text(object):
    def __init__(self, x, y, text, font, colour):
        self.x = x
        self.y = y
        self.font = font
        self.colour = colour

        self.surf = self.font.render(str(text), True, self.colour)
        self.rect = self.surf.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, text):
        self.surf = self.font.render(str(text), True, self.colour)
        self.rect = self.surf.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)


class Button(object):
    def __init__(self, x, y, xi, yi, text, font, bgcolour):
        self.x = x
        self.y = y
        self.width = xi
        self.height = yi
        self.text = str(text)
        self.font = font
        self.bgcolour = bgcolour

        #uses the Text class to render out the btnText and position
        self.btn = Text(self.width, self.y + self.height / 2, self.text, self.font, black)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bgcolour, [self.x, self.y, self.width, self.height])
        surface.blit(self.btn.surf, self.btn.rect)

    def detect(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (self.x + self.width) > mouse[0] > self.x and (self.y + self.height) > mouse[1] > self.y:
            if click[0] == 1:
                return True


#game menu
def game_intro():
    global intro
    intro = True
    gameDisplay.fill(white) #White bg

    button = Button(150, 400, 300, 100, 'Play', font, green)
    button.draw(gameDisplay)

    # Snake text
    title = Text((display_width / 2), (display_height / 3), 'Snake', largefont, black)
    title.draw(gameDisplay)

    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if button.detect():
            intro = False

        pygame.display.update()
        clock.tick(FPS)

    play_game()

def play_game():
    snake = Snake() #creates a new snake object
    food = Food(snake) #creates a new food object
    #variables
    lostGame = False
    global score
    score = 0

    while not lostGame:
        dt = clock.tick(FPS) / 1000.0 #fps to seconds
        gameDisplay.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #detects if WASD or arrows have been pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    snake.direction = 'up'
                elif event.key == K_DOWN or event.key == K_s:
                    snake.direction = 'down'
                elif event.key == K_LEFT or event.key == K_a:
                    snake.direction = 'left'
                elif event.key == K_RIGHT or event.key == K_d:
                    snake.direction = 'right'

        
        snake.move(dt) #moves the snake passing the clock value in seconds
        snake.draw(gameDisplay) #draws the updated snake to the display

        if snake.detect(food): #detects if the snake have eaten any food
            lostGame = True

        food.draw(gameDisplay) #draws the food piece to the display

        #render the score to the screen
        score_text = Text(0, 0, score, smallfont, black)
        score_text.rect.bottomright = (display_width-10,display_height-5)
        score_text.draw(gameDisplay)

        #display fps counter
        if DISPLAY_FPS:
            fps_text = Text(0, 0, 'fps ' + str(round(1/dt)), smallfont, black)
            fps_text.rect.topleft = (5, 5)
            fps_text.draw(gameDisplay)
   
        pygame.draw.rect(gameDisplay, black, [0, 0, display_width, display_height], 1) #draws an outline around the play area
        pygame.display.update()
    
    lost(score) #run the lost game function passing the final score
        

def lost(score):
    lost = True
    gameDisplay.fill(white)
    #retry button
    button = Button(150, 400, 300, 100, 'Try again', font, red)
    button.draw(gameDisplay)

    # Lost text
    lost = Text((display_width / 2), (display_height / 3), 'You lost!', font, black)
    lost.draw(gameDisplay)

    # score text
    score = Text((display_width / 2), (display_height / 2.3), "Score: " + str(score), smallfont, black)
    score.draw(gameDisplay)
    
    while lost:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #retry button
        if button.detect():
            lost = False

        pygame.display.update()

    play_game()

game_intro()
