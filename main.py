import pygame, os, math
pygame.init()

path = os.path.dirname(os.path.abspath(__file__)) + '/'
WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
print(WIDTH, HEIGHT)
if WIDTH > HEIGHT:
    HEIGHT *= 3/4
    WIDTH *= 3/4
else:
    HEIGHT = HEIGHT/WIDTH
    WIDTH *= 3/4
    HEIGHT = WIDTH/HEIGHT

def text(screen, text, color, size, pos, align="left"):
    text = text.encode("utf-8").decode("utf-8")
    try:
        my_font = pygame.font.SysFont(pygame.font.get_fonts()[2], size)
    except Exception:
        my_font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = my_font.render(text, True, color)
    if align == "left":
        screen.blit(text_surface, pos)
    elif align == "center" or align == "centre":
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def click_circle(mouse_pos, center, radius):
    return(mouse_pos[0] - center[0])**2 + (mouse_pos[1] - center[1])**2 <= radius**2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60
running = True

cardDim = [WIDTH/20, WIDTH/20*4/3] # x:y = 3:4

#ext:
#  type:
#    skill
#    soldier
#  skill:
#    summon n
#    fullAtk
#    freeze n
#    draw n
#    cure n 
#  n: int
#  atk: int
class Card:
    def __init__(self, hp, atk, cost,image = None, ext=[]):
        self.hp = hp
        self.atk = atk
        self.cost = cost
        self.ext = ext
        self.attacked = False
        self.image = image.convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, cardDim)
        
        self.rect = None

class Sys:
    def __init__(self):
        self.isPlayerTurn = True

        self.clickTimer = 0
        self.clickedCard = -1
        self.releasedCard = -1

        self.myCard = [Card(5, 2, 2, pygame.image.load(path + "image/cardTemp.png")), Card(6, 1, 1, pygame.image.load(path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(path + "image/cardTemp.png"))]
        self.aiCard = [Card(6, 1, 1, pygame.image.load(path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(path + "image/cardTemp.png"))]
        self.myHandCard = []
        self.aiHamdCard = []
        self.myhp = 30
        self.aihp = 30

    def attack(self, attacker, target, turn = "player"):
        if turn == "player":
            if target != 99:
                sys.aiCard[target].hp -= sys.myCard[attacker].atk
                print(sys.aiCard[target].hp)
            else:
                sys.aihp -= sys.myCard[attacker].atk
        if turn == "ai":
            if target != 99:
                sys.myCard[target].hp -= sys.aiCard[attacker].atk
                print(sys.myCard[target].hp)
            else:
                sys.myhp -= sys.aiCard[attacker].atk

    def checkAlive(self):
        temp = []
        for i in range(len(self.myCard)):
            if self.myCard[i].hp <= 0:
                temp.append(i)
        for i in reversed(temp):
            self.myCard.pop(i)
        temp = []
        for i in range(len(self.aiCard)):
            if self.aiCard[i].hp <= 0:
                temp.append(i)
        for i in reversed(temp):
            self.aiCard.pop(i)

    def switchTurn(self):
        if (self.isPlayerTurn):
            self.isPlayerTurn = False
        else:
            self.isPlayerTurn = True
        for card in sys.myCard:
            card.attacked = False
        for card in sys.aiCard:
            card.attacked = False

    def draw(self):
        #middle line

        #box indicate turn
        if self.isPlayerTurn:
            pygame.draw.lines(screen, (0, 0, 255), True, [(0, HEIGHT/2),(WIDTH, HEIGHT/2), (WIDTH, HEIGHT), (0, HEIGHT)], 5)
        else:
            pygame.draw.lines(screen, (255, 0, 0), True, [(0, 0),(WIDTH, 0), (WIDTH, HEIGHT/2), (0, HEIGHT/2)], 5)

        #card graphic me
        left = WIDTH/2 - (len(self.myCard)*(cardDim[0] + WIDTH/80) - WIDTH/80)/2
        top = HEIGHT*0.55

        for card in self.myCard:
            screen.blit(card.image, [left, top])
            card.rect = pygame.Rect(left, top, cardDim[0], cardDim[1])
            # pygame.draw.rect(screen, (10, 10, 10), [left, top, cardDim[0], cardDim[1]])
            # text(screen, "Card Tmp", (255, 255, 255), int(WIDTH/96), [left+cardDim[0]/2, top+cardDim[1]/2], "center")

            pygame.draw.circle(screen, (200, 200, 100), [left, top+cardDim[1]], WIDTH/150)  #attack
            text(screen, str(card.atk), (0, 0, 0), int(WIDTH/128), [left, top+cardDim[1]], "center")

            pygame.draw.circle(screen, (0, 181, 172), [left, top], WIDTH/150)  # cost
            text(screen, str(card.cost), (0, 0, 0), int(WIDTH/128), [left, top], "center")

            pygame.draw.circle(screen, (242, 89, 0), [left+cardDim[0], top+cardDim[1]], WIDTH/150)  #health
            text(screen, str(card.hp), (0, 0, 0), int(WIDTH/128), [left+cardDim[0], top+cardDim[1]], "center")

            left += cardDim[0] + WIDTH/80
        pygame.draw.circle(screen, (238, 255, 48), [WIDTH/2, HEIGHT*0.9], HEIGHT*0.05)  #me
        pygame.draw.circle(screen, (242, 89, 0), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.9+HEIGHT*0.05], HEIGHT*0.025)
        text(screen, str(self.myhp), (0, 0, 0), int(WIDTH/64), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.9+HEIGHT*0.05], "center")

        angle = -45
        for card in self.myHandCard:
            rotated_image, rect = rotate(card.image, angle, [WIDTH*0.9, HEIGHT*0.9], pygame.math.Vector2(0, -cardDim[1]))
            screen.blit(rotated_image, rect)
            if(len(self.myHandCard) > 10):
                angle += 90/(len(self.myHandCard)-1)
            else:
                angle += 9



        #card graphic ai
        left = WIDTH/2 - (len(self.aiCard)*(cardDim[0] + WIDTH/80) - WIDTH/80)/2
        top = HEIGHT*0.30

        for card in self.aiCard:
            screen.blit(card.image, [left, top])
            card.rect = pygame.Rect(left, top, cardDim[0], cardDim[1])
            # pygame.draw.rect(screen, (10, 10, 10), [left, top, cardDim[0], cardDim[1]])
            # text(screen, "Card Tmp", (255, 255, 255), int(WIDTH/96), [left+cardDim[0]/2, top+cardDim[1]/2], "center")

            pygame.draw.circle(screen, (200, 200, 100), [left, top+cardDim[1]], WIDTH/150)  #attack
            text(screen, str(card.atk), (0, 0, 0), int(WIDTH/128), [left, top+cardDim[1]], "center")

            pygame.draw.circle(screen, (0, 181, 172), [left, top], WIDTH/150)  # cost
            text(screen, str(card.cost), (0, 0, 0), int(WIDTH/128), [left, top], "center")

            pygame.draw.circle(screen, (242, 89, 0), [left+cardDim[0], top+cardDim[1]], WIDTH/150)  #health
            text(screen, str(card.hp), (0, 0, 0), int(WIDTH/128), [left+cardDim[0], top+cardDim[1]], "center")

            left += cardDim[0] + WIDTH/80
        pygame.draw.circle(screen, (238, 255, 48), [WIDTH/2, HEIGHT*0.1], HEIGHT*0.05)  #ai
        pygame.draw.circle(screen, (242, 89, 0), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.1+HEIGHT*0.05], HEIGHT*0.025)
        text(screen, str(self.aihp), (0, 0, 0), int(WIDTH/64), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.1+HEIGHT*0.05], "center")

        # draw arrow
        if (sys.clickedCard != -1 and sys.clickTimer > 0):
            pointA = (sys.myCard[sys.clickedCard].rect[0]+cardDim[0]/2, sys.myCard[sys.clickedCard].rect[1]+cardDim[1]/2)
            pointB = pygame.mouse.get_pos()
            angle_going = math.atan((pointB[1]-pointA[1])/(pointB[0]-pointA[0]+1e-10))
            if(pointB[0] < pointA[0]):
                angle_going += math.pi
            pygame.draw.polygon(screen, (255, 0, 0), [pointA, pointB, (pointB[0]+WIDTH/100*math.cos(angle_going-math.pi+math.pi/6), pointB[1]+WIDTH/100*math.sin(angle_going-math.pi+math.pi/6)), (pointB[0]+WIDTH/100*math.cos(angle_going-math.pi-math.pi/6), pointB[1]+WIDTH/100*math.sin(angle_going-math.pi-math.pi/6)), pointB], 5)
        
        # end turn button
        pygame.draw.circle(screen, (0, 0, 0), [WIDTH*0.95, HEIGHT/2], WIDTH/24)
        pygame.draw.rect(screen, (0, 0, 0), [WIDTH*0.94, HEIGHT/2-WIDTH/24, 2*WIDTH/24, 2*WIDTH/24])
        pygame.draw.circle(screen, (255, 255, 255), [WIDTH*0.95, HEIGHT/2], WIDTH/25)
        pygame.draw.rect(screen, (255, 255, 255), [WIDTH*0.95, HEIGHT/2-WIDTH/25, 2*WIDTH/25, 2*WIDTH/25])
        text(screen, "End Turn", (0, 0, 0), int(WIDTH/55), [WIDTH*0.96, HEIGHT/2], "center")
        


sys = Sys()

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sys.myHandCard.append(Card(5, 2, 2, pygame.image.load(path + "image/cardTemp.png")))
            if event.key == pygame.K_DOWN:
                sys.myHandCard.pop()

        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.clickTimer += 1
            
            #clicking my card
            sys.clickedCard = -1
            if(sys.isPlayerTurn):
                for i in range(len(sys.myCard)):
                    if sys.myCard[i].rect.collidepoint(mouse_pos) and sys.myCard[i].attacked == False:
                        sys.clickedCard = i
                        break
            
            # switchTurn
            if click_circle(mouse_pos, [WIDTH*0.95, HEIGHT/2], WIDTH/24) or (WIDTH*0.94 <= mouse_pos[0] <= WIDTH*0.94+2*WIDTH/24  and HEIGHT/2-WIDTH/24 <= mouse_pos[1] <= HEIGHT/2-WIDTH/24+2*WIDTH/24):
                sys.switchTurn()
            
 
        if event.type == pygame.MOUSEBUTTONUP:
            sys.releasedCard = -1
            if(sys.isPlayerTurn):
                for i in range(len(sys.aiCard)):
                    if sys.aiCard[i].rect.collidepoint(mouse_pos):
                        sys.releasedCard = i
                        break
            if click_circle(mouse_pos, [WIDTH/2, HEIGHT*0.1], HEIGHT*0.05):
                sys.releasedCard = 99
            #attack
            if (sys.clickedCard != -1 and sys.releasedCard != -1):
                sys.attack(sys.clickedCard, sys.releasedCard)
                sys.myCard[sys.clickedCard].attacked = True
                sys.checkAlive()

            sys.clickTimer = 0

    screen.fill((105, 77, 0))

    sys.draw()
    

    pygame.display.update()
    clock.tick(fps)

