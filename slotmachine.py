import pygame,random,sys

#Initialize Pygame
pygame.init()

#Initialize sound
pygame.mixer.pre_init()


#Various Settings
TITLE = "Sully's Slots"
WIDTH = 760
HEIGHT = 640
FPS = 60
GRID_SIZE = 64


#Control Shortcuts
ENTER = pygame.K_RETURN
SPACE = pygame.K_SPACE


#Colors
WHITE = (230,230,230)
DARK_BLUE = (16,86,103)
BLACK = (0,0,0)
GOLD = (218,165,32)

#Fonts
FONT = pygame.font.Font("assets/minya_nouvelle_bd.ttf",48)


def load_image(file_path):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img,(GRID_SIZE,GRID_SIZE))

    return img

def play_sound(sound):
    sound.play(0,0,0)

def play_music():
    pygame.mixer.music.play(-1)


#images
CAKE = load_image("assets/cake.png")
CANDY = load_image("assets/candy.png")
LOLLIPOP = load_image("assets/lollipop.png")
BREAD = load_image("assets/bread.png")

images = [CANDY, LOLLIPOP, CAKE, BREAD]

#Sounds


class Game():

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH,HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.done = False

        self.rollTime = 3 * FPS
        self.rollActive = False
        self.first = True

        self.topLimit = 55
        self.botLimit = 424 - 64

        self.games = 0
        self.checked = False

        self.active_layer = pygame.Surface([WIDTH,HEIGHT],pygame.SRCALPHA,32)

        #ugh
        self.loops = 0
        self.random1 = 0
        self.random2 = 0
        self.random3 = 0

        self.middle = (self.topLimit + self.botLimit) / 2

        self.y1 = self.middle
        self.y2 = self.y1
        self.y3 = self.y1
        self.x1 = 156 + 32
        self.x2 = 316 + 32
        self.x3 = 476 + 32
 
        self.img1 = CANDY
        self.img2 = BREAD
        self.img3 = CAKE
       
        self.speed1 = random.randint(5,10)
        self.speed2 = random.randint(5,10)
        self.speed3 = random.randint(5,10)

        self.winnings = 0
        
        self.start = self.topLimit

    def display_message(self,surface,text,x,y):

        text = FONT.render(text,1,BLACK)
        surface.blit(line, (x,y))

    def get_text(self):
        pass

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == ENTER or event.key == SPACE:
                    if not self.rollActive:
                        self.makeNew()
                        self.games = self.games + 1
                        self.checked = False
                    self.rollActive = True
                    
        


    def roll(self):
        if self.first:
            self.makeNew()
        self.first = False
        if self.loops == 5:
            self.speed /= 2
            self.loops += 1
        if self.loops == 7:
            self.speed /= 2
            self.loops += 1
        if self.loops == 9:
            self.speed = self.speed / 2 + 0.5
            self.loops += 1
            
          
        self.newspeed += self.speed
        self.y1 = self.start + self.newspeed
        self.y2 = self.y1
        self.y3 = self.y1
        
        
        
        if self.y1 >= self.botLimit:
            self.img1 = images[random.randint(0,3)]

            self.img2 = images[random.randint(0,3)]

            self.img3 = images[random.randint(0,3)]

            self.newspeed = 0
            self.loops += 1
            self.y1 = self.start

        if self.loops == 10 and self.y1 >= self.middle:
           self.y1 = self.middle
           self.y2 = self.y1
           self.y3 = self.y1
           self.rollActive = False
            
        self.active_layer.blit(self.img1 , (self.x1, self.y1))
        self.active_layer.blit(self.img2, (self.x2, self.y1))
        self.active_layer.blit(self.img3, (self.x3, self.y1))
        
        
        

    
    def makeNew(self):
        self.random1 = random.randint(0,3)
        self.random2 = random.randint(0,3)
        self.random3 = random.randint(0,3)
 
        self.img1 = images[self.random1]
        self.img2 = images[self.random2]
        self.img3 = images[self.random3]
       
        self.speed=20

        self.newspeed = 0

        self.loops = 0

    def checkWinnings(self):
        if self.img1 == self.img2 == self.img3:
            if self.img1 == CANDY:
                self.winnings += 1
            if self.img1 == LOLLIPOP:
                self.winnings += 2
            if self.img1 == CAKE:
                self.winnings += 3
            if self.img1 == BREAD:
                self.winnings += 250
            
            self.checked = True

        
    def draw(self):
        self.active_layer.fill(GOLD)
        pygame.draw.rect(self.active_layer, WHITE, [156,55, 128,360])
        pygame.draw.rect(self.active_layer, WHITE, [316,55, 128,360])
        pygame.draw.rect(self.active_layer, WHITE, [476,55, 128,360])

        
        if self.rollActive:
            self.roll()
        else:
            if not self.checked:
                self.checkWinnings()
            self.active_layer.blit(self.img1 , (self.x1, self.y1))
            self.active_layer.blit(self.img2, (self.x2, self.y1))
            self.active_layer.blit(self.img3, (self.x3, self.y1))
            
        pygame.draw.rect(self.active_layer,GOLD, [156, 360, 448, 64])
        pygame.draw.rect(self.active_layer,GOLD, [156, 55, 448, 64])

        games_text = FONT.render("Games Played: " + str(self.games), 1, BLACK)
        winnings_text = FONT.render("Total Winnings: " + str(self.winnings),1, BLACK)

        
        
        self.window.blit(self.active_layer, [0,0])
        self.window.blit(games_text, (WIDTH / 2 - games_text.get_width() /2, 450))
        self.window.blit(winnings_text,(WIDTH / 2 - winnings_text.get_width() /2, 514))
        

        pygame.display.flip()

        
    def loop(self):
        while not self.done:
            self.process_events()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.loop()
    pygame.quit()
    sys.exit()




    
        
