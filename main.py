import pygame, os, math, random
import cardList
pygame.init()

path = os.path.dirname(os.path.abspath(__file__)) + '/'
WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
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
cardDimEnlarged = [WIDTH/10, WIDTH/10*4/3]
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
    def __init__(self, cost, atk, hp, image = None, ext=[]):
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
        self.checking = False

        self.clickTimer = 0
        self.clickedCard = -1
        self.releasedCard = -1
        self.cardSet = {}
        self.cardSet["myCard"] = [Card(1, 2, 5, pygame.image.load(path + "image/cardTemp.png")), Card(6, 1, 1, pygame.image.load(path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(path + "image/cardTemp.png"))]
        self.cardSet["aiCard"] = [Card(1, 1, 6, pygame.image.load(path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(path + "image/cardTemp.png"))]
        self.cardSet["myHandCard"] = []
        self.cardSet["aiHandCard"] = []
        self.cardSet["mySetCard"] = cardList.card
        self.cardSet["aiSetCard"] = cardList.card
        self.myCardOrder = list(range(30))
        random.shuffle(self.myCardOrder)
        self.aiCardOrder = list(range(30))
        random.shuffle(self.aiCardOrder)
        self.myhp = 30
        self.aihp = 30

    def attack(self, attacker, target, turn = "player"):
        if turn == "player":
            if target != 99:
                sys.cardSet["aiCard"][target].hp -= sys.cardSet["myCard"][attacker].atk
            else:
                sys.aihp -= sys.cardSet["myCard"][attacker].atk
        if turn == "ai":
            if target != 99:
                sys.cardSet["myCard"][target].hp -= sys.cardSet["aiCard"][attacker].atk
            else:
                sys.myhp -= sys.cardSet["aiCard"][attacker].atk

    def checkAlive(self):
        temp = []
        for i in range(len(self.cardSet["myCard"])):
            if self.cardSet["myCard"][i].hp <= 0:
                temp.append(i)
        for i in reversed(temp):
            self.cardSet["myCard"].pop(i)
        temp = []
        for i in range(len(self.cardSet["aiCard"])):
            if self.cardSet["aiCard"][i].hp <= 0:
                temp.append(i)
        for i in reversed(temp):
            self.cardSet["aiCard"].pop(i)

    def switchTurn(self):
        if (self.isPlayerTurn):
            self.isPlayerTurn = False
            self.giveCard("ai")
        else:
            self.isPlayerTurn = True
            self.giveCard("player")

        for card in sys.cardSet["myCard"]:
            card.attacked = False
        for card in sys.cardSet["aiCard"]:
            card.attacked = False

    def giveCard(self, turn = "player"):
        if(turn == "player"):
            temp = self.cardSet["mySetCard"][sys.myCardOrder.pop(0)]
            self.cardSet["myHandCard"].append(Card(temp[0], temp[1], temp[2], pygame.image.load(path + "image/cardTemp.png")))
        if(turn == "ai"):
            temp = self.cardSet["aiSetCard"][sys.aiCardOrder.pop(0)]
            self.cardSet["aiHandCard"].append(Card(temp[0], temp[1], temp[2], pygame.image.load(path + "image/cardTemp.png")))

    def draw(self):
        #middle line

        #box indicate turn
        if self.isPlayerTurn:
            pygame.draw.lines(screen, (0, 0, 255), True, [(0, HEIGHT/2),(WIDTH, HEIGHT/2), (WIDTH, HEIGHT), (0, HEIGHT)], 5)
        else:
            pygame.draw.lines(screen, (255, 0, 0), True, [(0, 0),(WIDTH, 0), (WIDTH, HEIGHT/2), (0, HEIGHT/2)], 5)

        #card graphic me
        left = WIDTH/2 - (len(self.cardSet["myCard"])*(cardDim[0] + WIDTH/80) - WIDTH/80)/2
        top = HEIGHT*0.55

        for card in self.cardSet["myCard"]:
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

        #my hand card
        angle = -45
        for card in self.cardSet["myHandCard"]:
            rotated_image, rect = rotate(card.image, angle, [WIDTH*0.9, HEIGHT*0.9], pygame.math.Vector2(0, -cardDim[1]))
            screen.blit(rotated_image, rect)
            if(len(self.cardSet["myHandCard"]) > 10):
                angle += 90/(len(self.cardSet["myHandCard"])-1)
            else:
                angle += 9



        #card graphic ai
        left = WIDTH/2 - (len(self.cardSet["aiCard"])*(cardDim[0] + WIDTH/80) - WIDTH/80)/2
        top = HEIGHT*0.30

        for card in self.cardSet["aiCard"]:
            screen.blit(card.image, [left, top])
            card.rect = pygame.Rect(left, top, cardDim[0], cardDim[1])

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

        #ai hand card
        angle = -45
        for card in self.cardSet["aiHandCard"]:
            rotated_image, rect = rotate(card.image, angle, [WIDTH*0.1, HEIGHT*0.25], pygame.math.Vector2(0, -cardDim[1]))
            screen.blit(rotated_image, rect)
            if(len(self.cardSet["aiHandCard"]) > 10):
                angle += 90/(len(self.cardSet["aiHandCard"])-1)
            else:
                angle += 9

        # draw arrow
        if (sys.clickedCard != -1 and sys.clickTimer > 0):
            pointA = (sys.cardSet["myCard"][sys.clickedCard].rect[0]+cardDim[0]/2, sys.cardSet["myCard"][sys.clickedCard].rect[1]+cardDim[1]/2)
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

        #after I clicked my hand card
        if(sys.checking):
            my_surface = pygame.Surface((WIDTH, HEIGHT))
            my_surface = my_surface.convert_alpha()
            my_surface.fill((0, 0, 0, 64))
            screen.blit(my_surface, [0, 0])

            left = WIDTH/2 - (len(self.cardSet["myHandCard"])*(cardDimEnlarged[0] + WIDTH/40) - WIDTH/40)/2
            top = HEIGHT*0.35
            for card in self.cardSet["myHandCard"]:
                screen.blit(pygame.transform.smoothscale(card.image, cardDimEnlarged), [left, top])
                card.rect = pygame.Rect(left, top, cardDimEnlarged[0], cardDimEnlarged[1])

                pygame.draw.circle(screen, (200, 200, 100), [left, top+cardDimEnlarged[1]], WIDTH/75)  #attack
                text(screen, str(card.atk), (0, 0, 0), int(WIDTH/64), [left, top+cardDimEnlarged[1]], "center")

                pygame.draw.circle(screen, (0, 181, 172), [left, top], WIDTH/75)  # cost
                text(screen, str(card.cost), (0, 0, 0), int(WIDTH/64), [left, top], "center")

                pygame.draw.circle(screen, (242, 89, 0), [left+cardDimEnlarged[0], top+cardDimEnlarged[1]], WIDTH/75)  #health
                text(screen, str(card.hp), (0, 0, 0), int(WIDTH/64), [left+cardDimEnlarged[0], top+cardDimEnlarged[1]], "center")

                left += cardDimEnlarged[0] + WIDTH/40

    def checkHandCard(self):
        sys.checking = True
sys = Sys()

game_state = "playing"

while running:
    mouse_pos = pygame.mouse.get_pos()
    # print([round(100*mouse_pos[0]/WIDTH), round(100*mouse_pos[1]/HEIGHT)])
    if game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.clickTimer += 1

                # exit checking !!!!!!!!!put in keyup
                if (sys.checking):
                    if 0 <= mouse_pos[1] <= HEIGHT*0.3 or HEIGHT*0.7 <= mouse_pos[1] <= HEIGHT:
                        sys.checking = False

                #clicking my card
                sys.clickedCard = -1
                if(sys.isPlayerTurn and not(sys.checking)):
                    # user clicked hand card !!!!!!!!!put in keyup
                    if(WIDTH*0.8 <= mouse_pos[0] <= WIDTH and HEIGHT*0.7 <= mouse_pos[1] <= HEIGHT*0.9):
                        sys.checkHandCard()

                    # user clicked game board card
                    for i in range(len(sys.cardSet["myCard"])):
                        if sys.cardSet["myCard"][i].rect.collidepoint(mouse_pos) and sys.cardSet["myCard"][i].attacked == False:
                            sys.clickedCard = i
                            break

                # switchTurn (!!!!!!!!!!!!!!need put inside player turn after ai is done!!!!!!!!!!)
                if not(sys.checking):
                    if click_circle(mouse_pos, [WIDTH*0.95, HEIGHT/2], WIDTH/24) or (WIDTH*0.94 <= mouse_pos[0] <= WIDTH*0.94+2*WIDTH/24  and HEIGHT/2-WIDTH/24 <= mouse_pos[1] <= HEIGHT/2-WIDTH/24+2*WIDTH/24):
                        sys.switchTurn()

                
                
    
            if event.type == pygame.MOUSEBUTTONUP:
                sys.releasedCard = -1
                if(sys.isPlayerTurn):
                    for i in range(len(sys.cardSet["aiCard"])):
                        if sys.cardSet["aiCard"][i].rect.collidepoint(mouse_pos):
                            sys.releasedCard = i
                            break
                if click_circle(mouse_pos, [WIDTH/2, HEIGHT*0.1], HEIGHT*0.05):
                    sys.releasedCard = 99
                #attack
                if (sys.clickedCard != -1 and sys.releasedCard != -1):
                    sys.attack(sys.clickedCard, sys.releasedCard)
                    sys.cardSet["myCard"][sys.clickedCard].attacked = True
                    sys.checkAlive()

                sys.clickTimer = 0

        screen.fill((105, 77, 0))

        sys.draw()
        

        pygame.display.update()
        clock.tick(fps)
    elif game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        clock.tick(fps)
    
    elif game_state == "inventory":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        clock.tick(fps)
    
    elif game_state == "option":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        clock.tick(fps)

    elif game_state == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        clock.tick(fps)

    elif game_state == "lost":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        clock.tick(fps)