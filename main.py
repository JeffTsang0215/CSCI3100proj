import pygame, os, math, random
import cardList
import shared
import menu


#pygame.init handled by shared.py

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


running = True

cardDim = [shared.WIDTH/20, shared.WIDTH/20*4/3] # x:y = 3:4
cardDimEnlarged = [shared.WIDTH/10, shared.WIDTH/10*4/3]
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
        self.cardSet["myCard"] = [Card(1, 2, 5, pygame.image.load(shared.path + "image/cardTemp.png")), Card(6, 1, 1, pygame.image.load(shared.path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(shared.path + "image/cardTemp.png"))]
        self.cardSet["aiCard"] = [Card(1, 1, 6, pygame.image.load(shared.path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(shared.path + "image/cardTemp.png"))]
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
            self.cardSet["myHandCard"].append(Card(temp[0], temp[1], temp[2], pygame.image.load(shared.path + "image/cardTemp.png")))
        if(turn == "ai"):
            temp = self.cardSet["aiSetCard"][sys.aiCardOrder.pop(0)]
            self.cardSet["aiHandCard"].append(Card(temp[0], temp[1], temp[2], pygame.image.load(shared.path + "image/cardTemp.png")))

    def draw(self):
        #middle line

        #box indicate turn
        if self.isPlayerTurn:
            pygame.draw.lines(shared.screen, (0, 0, 255), True, [(0, shared.HEIGHT/2),(shared.WIDTH, shared.HEIGHT/2), (shared.WIDTH, shared.HEIGHT), (0, shared.HEIGHT)], 5)
        else:
            pygame.draw.lines(shared.screen, (255, 0, 0), True, [(0, 0),(shared.WIDTH, 0), (shared.WIDTH, shared.HEIGHT/2), (0, shared.HEIGHT/2)], 5)

        #card graphic me
        left = shared.WIDTH/2 - (len(self.cardSet["myCard"])*(cardDim[0] + shared.WIDTH/80) - shared.WIDTH/80)/2
        top = shared.HEIGHT*0.55

        for card in self.cardSet["myCard"]:
            shared.screen.blit(card.image, [left, top])
            card.rect = pygame.Rect(left, top, cardDim[0], cardDim[1])
            # pygame.draw.rect(shared.screen, (10, 10, 10), [left, top, cardDim[0], cardDim[1]])
            # shared.text(shared.screen, "Card Tmp", (255, 255, 255), int(shared.WIDTH/96), [left+cardDim[0]/2, top+cardDim[1]/2], "center")

            pygame.draw.circle(shared.screen, (200, 200, 100), [left, top+cardDim[1]], shared.WIDTH/150)  #attack
            shared.text(shared.screen, str(card.atk), (0, 0, 0), int(shared.WIDTH/128), [left, top+cardDim[1]], "center")

            pygame.draw.circle(shared.screen, (0, 181, 172), [left, top], shared.WIDTH/150)  # cost
            shared.text(shared.screen, str(card.cost), (0, 0, 0), int(shared.WIDTH/128), [left, top], "center")

            pygame.draw.circle(shared.screen, (242, 89, 0), [left+cardDim[0], top+cardDim[1]], shared.WIDTH/150)  #health
            shared.text(shared.screen, str(card.hp), (0, 0, 0), int(shared.WIDTH/128), [left+cardDim[0], top+cardDim[1]], "center")

            left += cardDim[0] + shared.WIDTH/80
        pygame.draw.circle(shared.screen, (238, 255, 48), [shared.WIDTH/2, shared.HEIGHT*0.9], shared.HEIGHT*0.05)  #me
        pygame.draw.circle(shared.screen, (242, 89, 0), [shared.WIDTH/2+shared.HEIGHT*0.05, shared.HEIGHT*0.9+shared.HEIGHT*0.05], shared.HEIGHT*0.025)
        shared.text(shared.screen, str(self.myhp), (0, 0, 0), int(shared.WIDTH/64), [shared.WIDTH/2+shared.HEIGHT*0.05, shared.HEIGHT*0.9+shared.HEIGHT*0.05], "center")

        #my hand card
        angle = -45
        for card in self.cardSet["myHandCard"]:
            rotated_image, rect = rotate(card.image, angle, [shared.WIDTH*0.9, shared.HEIGHT*0.9], pygame.math.Vector2(0, -cardDim[1]))
            shared.screen.blit(rotated_image, rect)
            if(len(self.cardSet["myHandCard"]) > 10):
                angle += 90/(len(self.cardSet["myHandCard"])-1)
            else:
                angle += 9



        #card graphic ai
        left = shared.WIDTH/2 - (len(self.cardSet["aiCard"])*(cardDim[0] + shared.WIDTH/80) - shared.WIDTH/80)/2
        top = shared.HEIGHT*0.30

        for card in self.cardSet["aiCard"]:
            shared.screen.blit(card.image, [left, top])
            card.rect = pygame.Rect(left, top, cardDim[0], cardDim[1])

            pygame.draw.circle(shared.screen, (200, 200, 100), [left, top+cardDim[1]], shared.WIDTH/150)  #attack
            shared.text(shared.screen, str(card.atk), (0, 0, 0), int(shared.WIDTH/128), [left, top+cardDim[1]], "center")

            pygame.draw.circle(shared.screen, (0, 181, 172), [left, top], shared.WIDTH/150)  # cost
            shared.text(shared.screen, str(card.cost), (0, 0, 0), int(shared.WIDTH/128), [left, top], "center")

            pygame.draw.circle(shared.screen, (242, 89, 0), [left+cardDim[0], top+cardDim[1]], shared.WIDTH/150)  #health
            shared.text(shared.screen, str(card.hp), (0, 0, 0), int(shared.WIDTH/128), [left+cardDim[0], top+cardDim[1]], "center")

            left += cardDim[0] + shared.WIDTH/80
        pygame.draw.circle(shared.screen, (238, 255, 48), [shared.WIDTH/2, shared.HEIGHT*0.1], shared.HEIGHT*0.05)  #ai
        pygame.draw.circle(shared.screen, (242, 89, 0), [shared.WIDTH/2+shared.HEIGHT*0.05, shared.HEIGHT*0.1+shared.HEIGHT*0.05], shared.HEIGHT*0.025)
        shared.text(shared.screen, str(self.aihp), (0, 0, 0), int(shared.WIDTH/64), [shared.WIDTH/2+shared.HEIGHT*0.05, shared.HEIGHT*0.1+shared.HEIGHT*0.05], "center")

        #ai hand card
        angle = -45
        for card in self.cardSet["aiHandCard"]:
            rotated_image, rect = rotate(card.image, angle, [shared.WIDTH*0.1, shared.HEIGHT*0.25], pygame.math.Vector2(0, -cardDim[1]))
            shared.screen.blit(rotated_image, rect)
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
            pygame.draw.polygon(shared.screen, (255, 0, 0), [pointA, pointB, (pointB[0]+shared.WIDTH/100*math.cos(angle_going-math.pi+math.pi/6), pointB[1]+shared.WIDTH/100*math.sin(angle_going-math.pi+math.pi/6)), (pointB[0]+shared.WIDTH/100*math.cos(angle_going-math.pi-math.pi/6), pointB[1]+shared.WIDTH/100*math.sin(angle_going-math.pi-math.pi/6)), pointB], 5)
        
        # end turn button
        pygame.draw.circle(shared.screen, (0, 0, 0), [shared.WIDTH*0.95, shared.HEIGHT/2], shared.WIDTH/24)
        pygame.draw.rect(shared.screen, (0, 0, 0), [shared.WIDTH*0.94, shared.HEIGHT/2-shared.WIDTH/24, 2*shared.WIDTH/24, 2*shared.WIDTH/24])
        pygame.draw.circle(shared.screen, (255, 255, 255), [shared.WIDTH*0.95, shared.HEIGHT/2], shared.WIDTH/25)
        pygame.draw.rect(shared.screen, (255, 255, 255), [shared.WIDTH*0.95, shared.HEIGHT/2-shared.WIDTH/25, 2*shared.WIDTH/25, 2*shared.WIDTH/25])
        shared.text(shared.screen, "End Turn", (0, 0, 0), int(shared.WIDTH/55), [shared.WIDTH*0.96, shared.HEIGHT/2], "center")

        #after I clicked my hand card
        if(sys.checking):
            my_surface = pygame.Surface((shared.WIDTH, shared.HEIGHT))
            my_surface = my_surface.convert_alpha()
            my_surface.fill((0, 0, 0, 64))
            shared.screen.blit(my_surface, [0, 0])

            left = shared.WIDTH/2 - (len(self.cardSet["myHandCard"])*(cardDimEnlarged[0] + shared.WIDTH/40) - shared.WIDTH/40)/2
            top = shared.HEIGHT*0.35
            for card in self.cardSet["myHandCard"]:
                shared.screen.blit(pygame.transform.smoothscale(card.image, cardDimEnlarged), [left, top])
                card.rect = pygame.Rect(left, top, cardDimEnlarged[0], cardDimEnlarged[1])

                pygame.draw.circle(shared.screen, (200, 200, 100), [left, top+cardDimEnlarged[1]], shared.WIDTH/75)  #attack
                shared.text(shared.screen, str(card.atk), (0, 0, 0), int(shared.WIDTH/64), [left, top+cardDimEnlarged[1]], "center")

                pygame.draw.circle(shared.screen, (0, 181, 172), [left, top], shared.WIDTH/75)  # cost
                shared.text(shared.screen, str(card.cost), (0, 0, 0), int(shared.WIDTH/64), [left, top], "center")

                pygame.draw.circle(shared.screen, (242, 89, 0), [left+cardDimEnlarged[0], top+cardDimEnlarged[1]], shared.WIDTH/75)  #health
                shared.text(shared.screen, str(card.hp), (0, 0, 0), int(shared.WIDTH/64), [left+cardDimEnlarged[0], top+cardDimEnlarged[1]], "center")

                left += cardDimEnlarged[0] + shared.WIDTH/40

    def checkHandCard(self):
        sys.checking = True
sys = Sys()



while running:

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    #Use to track mouse position
    print([round(100*mouse_pos[0]/shared.WIDTH), round(100*mouse_pos[1]/shared.HEIGHT)])
    ###
    if shared.game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.clickTimer += 1

                # exit checking !!!!!!!!!put in keyup
                if (sys.checking):
                    if 0 <= mouse_pos[1] <= shared.HEIGHT*0.3 or shared.HEIGHT*0.7 <= mouse_pos[1] <= shared.HEIGHT:
                        sys.checking = False

                #clicking my card
                sys.clickedCard = -1
                if(sys.isPlayerTurn and not(sys.checking)):
                    # user clicked hand card !!!!!!!!!put in keyup
                    if(shared.WIDTH*0.8 <= mouse_pos[0] <= shared.WIDTH and shared.HEIGHT*0.7 <= mouse_pos[1] <= shared.HEIGHT*0.9):
                        sys.checkHandCard()

                    # user clicked game board card
                    for i in range(len(sys.cardSet["myCard"])):
                        if sys.cardSet["myCard"][i].rect.collidepoint(mouse_pos) and sys.cardSet["myCard"][i].attacked == False:
                            sys.clickedCard = i
                            break

                # switchTurn (!!!!!!!!!!!!!!need put inside player turn after ai is done!!!!!!!!!!)
                if not(sys.checking):
                    if click_circle(mouse_pos, [shared.WIDTH*0.95, shared.HEIGHT/2], shared.WIDTH/24) or (shared.WIDTH*0.94 <= mouse_pos[0] <= shared.WIDTH*0.94+2*shared.WIDTH/24  and shared.HEIGHT/2-shared.WIDTH/24 <= mouse_pos[1] <= shared.HEIGHT/2-shared.WIDTH/24+2*shared.WIDTH/24):
                        sys.switchTurn()

                
                
    
            if event.type == pygame.MOUSEBUTTONUP:
                sys.releasedCard = -1
                if(sys.isPlayerTurn):
                    for i in range(len(sys.cardSet["aiCard"])):
                        if sys.cardSet["aiCard"][i].rect.collidepoint(mouse_pos):
                            sys.releasedCard = i
                            break
                if click_circle(mouse_pos, [shared.WIDTH/2, shared.HEIGHT*0.1], shared.HEIGHT*0.05):
                    sys.releasedCard = 99
                #attack
                if (sys.clickedCard != -1 and sys.releasedCard != -1):
                    sys.attack(sys.clickedCard, sys.releasedCard)
                    sys.cardSet["myCard"][sys.clickedCard].attacked = True
                    sys.checkAlive()

                sys.clickTimer = 0

        shared.screen.fill((105, 77, 0))

        sys.draw()
        

        pygame.display.update()
        shared.clock.tick(shared.fps)
    elif shared.game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        menu.menu_main(mouse_pos, mouse_click)
        pygame.display.update()
        shared.clock.tick(shared.fps)
    
    elif shared.game_state == "inventory":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        shared.screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        shared.clock.tick(shared.fps)
    
    elif shared.game_state == "option":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        shared.screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        shared.clock.tick(shared.fps)

    elif shared.game_state == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        shared.screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        shared.clock.tick(shared.fps)

    elif shared.game_state == "lost":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        shared.screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        shared.clock.tick(shared.fps)