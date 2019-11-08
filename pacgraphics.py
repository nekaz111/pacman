#Jeremiah Hsieh AI Pac Man Final Project
#basic display and movement of pacman


import math
import pygame as pg 
import random

#class for pellet objects using pg sprites to draw
class Pellet(pg.sprite.Sprite):
    #initialize default to 255,255,255 which is white, 
    def __init__(self, x, y, r = 10, rgb = (255, 255, 255)):
        pg.sprite.Sprite.__init__(self)
        #x is x coordinate of pellet
        self.x = x
        #y is y coordinate
        self.y = y
        #r is radius of pellet
        self.r = r
        #rgb is color although technically python uses BGR (?) although that's may only be for opencv images
        self.rgb = rgb
        
#pacman sprite class        
class Pacman(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pacman
        self.rect = self.image.get_rect(center=pos)

#ghost sprite class
class Ghost(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = ghost
        self.rect = self.image.get_rect(center=pos)
   
#creates pellet object, sets paremeters
def spawnPellet(x = 100, y = 100):
    #create pellet object
    pellet = Pellet(x, y)
    return pellet


#redraws window and updates values on a clock timer
def redraw(array):
    arrayX = len(array)
    arrayY = len(array[0])
    #refill background first so that previously drawn objects don't stay on screen, 0 0 0 is black 
    win.fill((0,0,0))
    #draw maze bounding box
    pg.draw.rect(win, (0, 0, 255), (20, 20, arrayY * 40, arrayX * 40), 2)
    #window, color, starting position and size
#    pg.draw.rect(win, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))
    pellet_list.draw(win)
    #draw maze features
    #loop thorugh maze array
    for x in range(arrayX):
        for y in range(arrayY):  
            #draw pellet if 1 is encountered
            if array[x][y] == 1:
                #remember 0,0 is top left of window not bottom right like on a graph (hence why x and y are reversed?)
                pg.draw.circle(win, (255, 255, 255), [(y+1)*40, (x+1)*40], 10)
#                pg.draw.rect(win, (255, 0, 0), (((y+1)*40)-20, ((x+1)*40)-20, 40, 40), 2)
            #draw wall if 2 is encountered
            elif array[x][y] == 2:
                pg.draw.rect(win, (0, 0, 255), (((y+1)*40)-20, ((x+1)*40)-20, 40, 40))
            #draw pacman sprite where 3 is in array
            elif array[x][y] == 3:
#                sprites_list.draw(win)
                #blit to draw image at coordinates
                win.blit(pacman, (((y+1)*40)-15, ((x+1)*40)-15))
#                print(pacman.center)
#                pg.draw.rect(win, (255, 0, 0), (((y+1)*40)-10, ((x+1)*40)-10, 20, 20), 2)
            elif array[x][y] == 4:
                win.blit(ghost, (((y+1)*40)-15, ((x+1)*40)-15))
    #60 updates per second (equivalent to 5 fps) since it only checks and updates what is seen on screen 5 times per second 
    clock.tick(6)
    pg.display.update()       
#    pg.display.flip()
 
    
def drawWindow():
    #draw window
    win = pg.display.set_mode((600,600))
    #window name
    pg.display.set_caption("Pac-man")
    return win

#modified version for group partner code
def otherRedraw(win, array, coin_coords, ghost_coords, power_coords, wall_list, score):
    
    #load ghost file
    ghost = pg.image.load('ghost2.png').convert_alpha()
    arrayX = len(array)
    arrayY = len(array[0])
    #refill background first so that previously drawn objects don't stay on screen, 0 0 0 is black 
    win.fill((0,0,0))
    #draw maze bounding box
    pg.draw.rect(win, (0, 0, 255), (10, 10, arrayY * 20, arrayX * 20), 1)
    #window, color, starting position and size
#    pg.draw.rect(win, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))
#    pellet_list.draw(win)
#    #draw maze features
#    #loop thorugh maze array
#    for x in range(arrayX):
#        for y in range(arrayY):  
#            #draw pellet if 1 is encountered
#            if array[x][y] == "O":
#                #remember 0,0 is top left of window not bottom right like on a graph (hence why x and y are reversed?)
#                pg.draw.circle(win, (255, 255, 255), [(y+1)*20, (x+1)*20], 5)
##                pg.draw.rect(win, (255, 0, 0), (((y+1)*40)-20, ((x+1)*40)-20, 40, 40), 2)
#            #draw wall if 2 is encountered
#            elif array[x][y] == "|":
#                pg.draw.rect(win, (0, 0, 255), (((y+1)*20)-10, ((x+1)*20)-10, 20, 20))
#            #draw pacman sprite where 3 is in array
#            elif array[x][y] == ".":
##                sprites_list.draw(win)
#                #blit to draw image at coordinates
#                win.blit(pacman, (((y+1)*20)-7, ((x+1)*20)-7))
##                print(pacman.center)
##                pg.draw.rect(win, (255, 0, 0), (((y+1)*40)-10, ((x+1)*40)-10, 20, 20), 2)
#            elif array[x][y] == "X":
#                win.blit(ghost, (((y+1)*20)-7, ((x+1)*20)-7))
        
    #modified rendering        
    for x in coin_coords:
        pg.draw.circle(win, (255, 255, 255), [(x[1]+1)*20, (x[0]+1)*20], 5)
    for x in ghost_coords:
        win.blit(ghost, (((x[1]+1)*20)-7, ((x[0]+1)*20)-7))
    for x in wall_list:
        pg.draw.rect(win, (0, 0, 255), (((x[1]+1)*20)-10, ((x[0]+1)*20)-10, 20, 20))
    
    #draw score on window
    
    #60 updates per second (equivalent to 5 fps) since it only checks and updates what is seen on screen 5 times per second 
#    clock.tick(10)
    pg.display.update()       
#    pg.display.flip() 
    
    
#print lose text and quit game loop
def loseGame():
    #make font type
    font = pg.font.Font('freesansbold.ttf', 32) 
    #make text and draw on rectangle
    text = font.render('Game Over', True, (0, 255, 0), (0, 0, 0)) 
    #get rectange values
    textRect = text.get_rect() 
    #set location values
    textRect.center = (((mazey * 40) // 2) + 20, ((mazex * 40) // 2)+20) 
    #draw on window
    win.blit(text, textRect)
    #update window
    pg.display.update()   
    #return true to pause game
    return True
    
    
############################program main############################
if __name__ == "__main__":
    #initialize pygame module
    pg.init()
    #window size variables
    winx = 600
    winy = 600
    #fps is frames per second for clock tick speed
    fps = 30
    
    #list of all sprites in game
    sprites_list = pg.sprite.Group()
    
    
    #maze is array of numbers which stores the maze state to be rendered
    #basic implementation - 0 is nothing, 1 is pellet, 2 is wall (currently only implemented pellets), 3 is pacman, 4 is ghost for now
    maze = [[0, 3, 0, 0, 2, 1],
            [0, 1, 0, 1, 2, 0],
            [1, 1, 2, 0, 2, 1],
            [2, 2, 2, 0, 2, 4],
            [1, 0, 0, 1, 1, 0]]
    
    #maze x y sizes
    mazex = len(maze)
    mazey = len(maze[0])
    #pacman x y coordinate, maybe automate it to read from maze array?
    pacx = 0
    pacy = 1
    
    #gamestate timer
    clock = pg.time.Clock()
        
    #set window parameters
    win = pg.display.set_mode((winx,winy))
    #window name
    pg.display.set_caption("Pac-man")
    
    #load pacman image sprite
    pacman = pg.image.load('pacman2.png').convert_alpha()
    ghost = pg.image.load('ghost.png').convert_alpha()
    #make pacman class object for player
    player = Pacman([200, 200])
    enemy = Ghost([200, 200])
    #add to list of sprites to render
    sprites_list.add(player)
    
    #initialize pygame object storage
    pellet_list = pg.sprite.Group()
    #game loop variable, loops until condition is false which stops game
    run = True
    pause = False
    
    
    #window loop to render objects
    while run == True:    
        #check for user input
        #unlike key.getpressed it won't repeat automatically
        for event in pg.event.get():
            #exit program by clicking x
            if event.type == pg.QUIT:
                #stop loop
                run = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_w:
                #check if pacman is against edge of maze (or wall but not implemented yet)
                if pacx > 0 and maze[pacx-1][pacy] != 2:
                    #lazy ghost check
                    if maze[pacx-1][pacy] == 4:
                        pause = loseGame()
                    #move location of pacman in array
                    #make original space empty
                    maze[pacx][pacy] = 0
                    #move "up" one
                    pacx -= 1
                    maze[pacx][pacy] = 3
            elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                #check if pacman is against edge of maze (or wall but not implekented yet)
                if pacx < mazex - 1 and maze[pacx+1][pacy] != 2:
                    if maze[pacx+1][pacy] == 4:
                        pause = loseGame()
                    #move location of pacman in array
                    #make original space empty
                    maze[pacx][pacy] = 0
                    #move "down" one
                    pacx += 1
                    maze[pacx][pacy] = 3            
            elif event.type == pg.KEYDOWN and event.key == pg.K_a:
                #check if pacman is against edge of maze (or wall but not implekented yet)
                if pacy > 0 and maze[pacx][pacy-1] != 2:
                    if maze[pacx][pacy-1] == 4:
                        pause = loseGame()
                    #move location of pacman in array
                    #make original space empty
                    maze[pacx][pacy] = 0
                    #move "left" one
                    pacy -= 1
                    maze[pacx][pacy] = 3  
            elif event.type == pg.KEYDOWN and event.key == pg.K_d:
                #check if pacman is against edge of maze (or wall but not implekented yet)
                if pacy < mazey - 1 and maze[pacx][pacy+1] != 2:
                    if  maze[pacx][pacy+1] == 4:
                        pause = loseGame()
                    #move location of pacman in array
                    #make original space empty
                    maze[pacx][pacy] = 0
                    #move "right" one
                    pacy += 1
                    maze[pacx][pacy] = 3    
                    
                    
        #check for keypresses (continuous)
        keys = pg.key.get_pressed()
        #keyboard presses to move pacman
        if keys[pg.K_UP]:
            #check if pacman is against edge of maze (or wall but not implemented yet)
            if pacx > 0 and maze[pacx-1][pacy] != 2:
                if maze[pacx-1][pacy] == 4:
                        pause = loseGame()
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "up" one
                pacx -= 1
                maze[pacx][pacy] = 3
               
        if keys[pg.K_DOWN]:
            #check if pacman is against edge of maze (or wall but not implekented yet)
            if pacx < mazex - 1 and maze[pacx+1][pacy] != 2:
                if maze[pacx+1][pacy] == 4:
                        pause = loseGame()
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "down" one
                pacx += 1
                maze[pacx][pacy] = 3
            
        if keys[pg.K_LEFT]:
            #check if pacman is against edge of maze (or wall but not implekented yet)
            if pacy > 0 and maze[pacx][pacy-1] != 2:
                if maze[pacx][pacy-1] == 4:
                        pause =loseGame()
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "left" one
                pacy -= 1
                maze[pacx][pacy] = 3            
            
        if keys[pg.K_RIGHT]:
            #check if pacman is against edge of maze (or wall but not implekented yet)
            if pacy < mazey - 1 and maze[pacx][pacy+1] != 2:
                if maze[pacx][pacy+1] == 4:
                        pause = loseGame()
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "right" one
                pacy += 1
                maze[pacx][pacy] = 3          
                
                
        #clock tick controls how many time the game is updated per second, higher = more frames        
    #    clock.tick (fps)
        
        if pause == False:
            #draw sprites onto window 
            redraw(maze)
    
    
    #stop pygame     
    pg.quit()