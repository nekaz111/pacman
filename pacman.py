#Jeremiah Hsieh AI Pac Man Final Project
#basic display and movement of pacman


import math
import pygame as pg 

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
    
#creates pellet object, sets paremeters
def spawnPellet(x = 100, y = 100):
    #create pellet object
    pellet = Pellet(x, y)
    return pellet


#redraws window and updates values on a clock timer
def redraw(mouse = 1):
    #refill background first so that previously drawn objects don't stay on screen, 0 0 0 is black 
    win.fill((0,0,0))
    #draw maze bounding box
    pg.draw.rect(win, (0, 0, 255), (20, 20, mazey * 40, mazex * 40), 2)
    #window, color, starting position and size
#    pg.draw.rect(win, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))
    pellet_list.draw(win)
    #draw maze features
    #loop thorugh maze array
    for x in range(mazex):
        for y in range(mazey):  
            #draw pellet if 1 is encountered
            if maze[x][y] == 1:
                #remember 0,0 is top left of window not bottom right like on a graph (hence why x and y are reversed?)
                pg.draw.circle(win, (255, 255, 255), [(y+1)*40, (x+1)*40], 10)
#                pg.draw.rect(win, (255, 0, 0), (((y+1)*40)-20, ((x+1)*40)-20, 40, 40), 2)
            #draw wall if 2 is encountered
            elif maze[x][y] == 2:
                pg.draw.rect(win, (0, 0, 255), (((y+1)*40)-20, ((x+1)*40)-20, 40, 40))
            #draw pacman sprite where 3 is in array
            elif maze[x][y] == 3:
#                sprites_list.draw(win)
                #blit to draw image at coordinates
                win.blit(pacman, (((y+1)*40)-15, ((x+1)*40)-15))
#                print(pacman.center)
#                pg.draw.rect(win, (255, 0, 0), (((y+1)*40)-10, ((x+1)*40)-10, 20, 20), 2)

    #60 updates per second (equivalent to 5 fps) since it only checks and updates what is seen on screen 5 times per second 
    clock.tick(6)
    pg.display.update()       
#    pg.display.flip()
    
    
    
    
    
############################program main############################
#initialize pygame module
pg.init()
#window size variables
winx = 800
winy = 800
#fps is frames per second for clock tick speed
fps = 30

#list of all sprites in game
sprites_list = pg.sprite.Group()


#maze is array of numbers which stores the maze state to be rendered
#basic implementation - 0 is nothing, 1 is pellet, 2 is wall (currently only implemented pellets), 3 is pacman
maze = [[0, 3, 0, 0, 2, 1],
        [0, 1, 0, 1, 2, 0],
        [1, 1, 2, 0, 2, 1],
        [2, 2, 2, 0, 2, 0],
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
#make pacman class object for player
player = Pacman([200, 200])
#add to list of sprites to render
sprites_list.add(player)

#initialize pygame object storage
pellet_list = pg.sprite.Group()
#game loop variable, loops until condition is false which stops game
run = True



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
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "up" one
                pacx -= 1
                maze[pacx][pacy] = 3
        elif event.type == pg.KEYDOWN and event.key == pg.K_s:
            #check if pacman is against edge of maze (or wall but not implekented yet)
            if pacx < mazex - 1 and maze[pacx+1][pacy] != 2:
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "down" one
                pacx += 1
                maze[pacx][pacy] = 3            
        elif event.type == pg.KEYDOWN and event.key == pg.K_a:
            #check if pacman is against edge of maze (or wall but not implekented yet)
            if pacy > 0 and maze[pacx][pacy-1] != 2:
                #move location of pacman in array
                #make original space empty
                maze[pacx][pacy] = 0
                #move "left" one
                pacy -= 1
                maze[pacx][pacy] = 3  
        elif event.type == pg.KEYDOWN and event.key == pg.K_d:
            #check if pacman is against edge of maze (or wall but not implekented yet)
            if pacy < mazey - 1 and maze[pacx][pacy+1] != 2:
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
            #move location of pacman in array
            #make original space empty
            maze[pacx][pacy] = 0
            #move "up" one
            pacx -= 1
            maze[pacx][pacy] = 3
           
    if keys[pg.K_DOWN]:
        #check if pacman is against edge of maze (or wall but not implekented yet)
        if pacx < mazex - 1 and maze[pacx+1][pacy] != 2:
            #move location of pacman in array
            #make original space empty
            maze[pacx][pacy] = 0
            #move "down" one
            pacx += 1
            maze[pacx][pacy] = 3
        
    if keys[pg.K_LEFT]:
        #check if pacman is against edge of maze (or wall but not implekented yet)
        if pacy > 0 and maze[pacx][pacy-1] != 2:
            #move location of pacman in array
            #make original space empty
            maze[pacx][pacy] = 0
            #move "left" one
            pacy -= 1
            maze[pacx][pacy] = 3            
        
    if keys[pg.K_RIGHT]:
        #check if pacman is against edge of maze (or wall but not implekented yet)
        if pacy < mazey - 1 and maze[pacx][pacy+1] != 2:
            #move location of pacman in array
            #make original space empty
            maze[pacx][pacy] = 0
            #move "right" one
            pacy += 1
            maze[pacx][pacy] = 3          
            
            
    #clock tick controls how many time the game is updated per second, higher = more frames        
#    clock.tick (fps)
    
    #draw sprites onto window 
    redraw()


#stop pygame     
pg.quit()