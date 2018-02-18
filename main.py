import pygame, time, random

#initialise pygame
pygame.init()
pygame.font.init()

#define fonts
font = pygame.font.SysFont('Arial', 75)
smallfont = pygame.font.SysFont('Arial', 30)
largefont = pygame.font.SysFont('Arial', 115)

#display size
display_width = 600
display_height = 800

#square size of snake and food (x&y)
squaresize = 20

#colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)

#create window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


def text_objects(text,font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(x, y, xi, yi, text, font, colour):

    btnSurf, btnRect = text_objects(text, font)
    btnRect.center = (xi,y+yi/2)
    pygame.draw.rect(gameDisplay, colour, [x, y,xi, yi])
    gameDisplay.blit(btnSurf, btnRect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (x+xi) > mouse[0] > x and (y+yi) > mouse[1] > y:
        if click[0] == 1:
            return(1)


def game_intro():
    global intro
    intro = True

    #White bg
    gameDisplay.fill(white)
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #Snake text
        TextSurf, TextRect = text_objects("Snake", largefont)
        TextRect.center = ((display_width/2),((display_height/3)))
        gameDisplay.blit(TextSurf, TextRect)

        if button(150, 400, 300, 100, 'Play', font, green) == 1:
            intro = False

        pygame.display.update()
        clock.tick(15)

    play_game()


def play_game():
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [0, 0, display_width, display_height], 1)

    xposes = display_width/squaresize
    yposes = display_height/squaresize
    centrepos = [int(xposes/2), (yposes/2)]
    print(centrepos)

    #variables
    gameExit = False
    length = 4
    global food_location
    food_location = [0,0]
    snakesquares = []
    score = 344

    for num in range(length):
        snakesquares.append([centrepos[0], centrepos[0]-num])

    def new_food(snakesquares):
        x = random.randint(0, xposes-1)
        y = random.randint(0, yposes-1)

        for snakesquare in snakesquares:
            if x == snakesquare[0] and y ==snakesquare[1]:
                new_food(snakesquares)
        
        pygame.draw.rect(gameDisplay, red, [x*20, y*20, 20, 20])
        food_location = [x,y]
        print(food_location)

    new_food(snakesquares)


    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        for snakesquare in snakesquares:
            pygame.draw.rect(gameDisplay, green, [snakesquare[0]*20, snakesquare[1]*20,20, 20])



        scoreSurf, scoreRect = text_objects(str(score), smallfont)
        scoreRect.bottomright = (display_width-10,display_height-5)
        gameDisplay.blit(scoreSurf, scoreRect)
            
        pygame.display.update()
        clock.tick(1)
    

game_intro()