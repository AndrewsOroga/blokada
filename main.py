from level import level
from pygame import *

width, height = 1280, 720
win = display.set_mode((width, height))
display.set_caption("Blokada")

class Settings(sprite.Sprite):
    def __init__(self,  x,y,w,h,speed, img):
        super().__init__()
        self.w = w
        self.h = h
        self.speed = speed
        self.image = transform.scale(image.load(img), (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(Settings):
    def r_l(self):
        keys = key.get_pressed()
        if keys [K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
            
        
        
    def u_d(self):
        keys = key.get_pressed()
        if keys [K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        
class Enemy(Settings):
    def __init__(self, x,y,w,h,speed, img, direction):
            Settings.__init__(self, x,y,w,h,speed,img)
            
            self.direction = direction
            
    def update(self):
        global direction
        if self.direction == "right":
            self.rect.x -= self.speed
        if self.direction == "left":
            self.rect.x += self.speed

            
class Camera():
        def __init__(self, camera_func, width, height):
            self.camera_func = camera_func
            self.state = Rect(0,0,width, height)
            
        def apply(self, target):
            return target.rect.move(self.state.topleft)

        def update(self, target):
            self.state = self.camera_func(self.state, target.rect)
        
def camera_config(camera, target_rect):
    l,t,_,_ = target_rect
    _,_,w, h = camera
    l, t = -l+width//2,-t + height//2
    
    l =min(0,l)
    l = max(-(camera.width - width ), l)
    t = max(-(camera.height - height ), t)
    t = min(0,t)
    return Rect(l,t,w,h)
        

#TODO  IMAGES
bg = transform.scale(image.load('images/bgr.png'), (width, height))

hero_r = "images/sprite1_r.png"
hero_l = "images/sprite1.png"

cyborg_1 = "images/cyborg.png"
cyborg_r = "images/cyborg.png"

coin = "images/coin.png"
door  = "images/door.png"
key_img = "images/key.png"
chest_o  = "images/cst_open.png"
chest_c = "images/cst_close.png"
cyborg = "images/cyborg.png"
stair= "images/stair.png"
port= "images/portal.png"
platform = "images/platform.png"
nothing = "images/nothing.png"
power = "images/mana.png"



#TODO  SOUNDS
mixer.init()
fire_ = mixer.Sound
fire = mixer.Sound('sounds/fire.ogg')
kick =mixer.Sound('sounds/kick.ogg')
k_up=mixer.Sound('sounds/k_coll.wav')
c_coll=mixer.Sound('sounds/c_coll.wav')
d_o=mixer.Sound('sounds/lock.wav')
tp=mixer.Sound('sounds/teleport.ogg')
click=mixer.Sound('sounds/click.wav')
cst_o=mixer.Sound('sounds/chest.wav')


#TODO  FONTS
font.init()
text1 = font.SysFont(("font/ariblk.ttf"), 200)
text2 = font.SysFont(("font/ariblk.ttf"), 60)
text3 = font.SysFont(("font/calibrib.ttf"), 45)
text4 = font.SysFont(("font/ariblk.ttf"), 150)

g_name = text1.render("Blokada", True, (106,90,205),(250,235,215))
e_tap = text2.render("press 'E'", True, (255,0,255))
k_need = text2.render("You need a key to open", True, (255,0,255))
space = text2.render("Press [SPACE] to kill the enemy", True, (255,0,255))
wasd_b = text3.render("WASD - move buttons. You can only go up and down the stair", True, (255,0,0))
space_b = text3.render("SPACE - shot button. You are a wizard who only knows one spell", True, (255,0,0))
e_b = text3.render("E - interaction button. Open doors, collect keys, activate portals", True, (255,0,0))

done = text4.render('level comleted', True, (0,255,0),(255,100,0))
lose = text4.render('Game over', True, (255,0,0),(245,222,179))
pause = text4.render('PAUSE', True, (255,0,0),(245,222,179))
#TODO SPRITES
player =  Player(300,650,50,50,5,hero_l)

enemy1 = Enemy(400, 480, 50, 50, 3, cyborg_l, 'left')
enemy2 = Enemy(230, 320, 50, 50, 3, cyborg_l, 'left')

door = Settings( 1000, 580, 40, 120, 0, door)
                
key1 = Settings( 160, 350, 50, 20, 0, key_img)
                
key2 = Settings(1500, 350, 50, 20, 0, key_img)
                
portal = Settings(2700, 600, 100, 100, 0, port)
                  
chest = Settings(450, 130, 80, 80, 0, chest_c)

blocks_r = [] 
blocks_l = []                         
coins = []         
stairs = []            
platforms = []           
             
                
items = sprite.Group()


game = True
win.blit(bg,(0,0))

level_width = len(level[0])*40
level_height = len(level[0])*40

camera = Camera(camera_config, level_width, level_height)



x = y = 0
for row in level:
    for col in row:
        if col == "r":
            r1 = Settings(x,y,40,40,0,nothing)
            items.add(r1)
            
        
        
        if col == "1":
            r2 = Settings(x,y,40,40,0,nothing)
            items.add(r2)
            
        if col == "/":
            r3 = Settings(x,y-40,40,180,0,stair)
            items.add(r3)
            
            
        if col == "°":
            r4 = Settings(x,y,40,40,0,coin)
            items.add(r4)
            
        if col == "-":
            r5 = Settings(x,y,40,40,0,platform)
            items.add(r5)
            
        if col == "*":
            r6 = Settings(x,y,40,40,0,port)
            items.add(r6)
            
        if col == ">":
            r7 = Settings(x,y-40,80,80,0,chest_c)
            items.add(r7)
            
        x += 40
    y += 40
    x = 0
    
  


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
    player.u_d()
    player.r_l()
    player.reset()
    camera.update(player)
    for i in items:
        win.blit(i.image, camera.apply(i))
    display.update()