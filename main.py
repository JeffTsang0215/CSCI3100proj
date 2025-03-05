import pygame, os, math, random
import cardList
import cardcollection
import shared
import menu
import copy
from ai_system import AISystem

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
#    minion
#    spell
#  skill:
#    summon n
#    fullAtk
#    freeze n
#    draw n
#    cure n 
#  n: int
#  atk: int



class Card:
    def __init__(self, cost, atk, hp, image = None, ext={}):
        
        self.hp = hp
        self.atk = atk
        self.cost = cost
        self.ext = ext
        self.attacked = True
        self.round = 0

        if (image): 
            self.image = image.convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, cardDim)
        else:
            self.image = None
        
        self.rect = None
        self.rectEnlarged = None

    #for printing card objects during development
    def __repr__(self):
        return f"Card({self.cost}/{self.atk}/{self.hp})"
    
    def __deepcopy__(self, memo):
        # Create a copy WITHOUT copying the pygame.Surface
        new_card = Card(self.cost, self.atk, self.hp, self.image.copy() if self.image else None, copy.deepcopy(self.ext, memo))
        new_card.attacked = self.attacked
        new_card.round = self.round
        return new_card

class Sys:
    def __init__(self):
        self.ai = AISystem(self)
        self.isPlayerTurn = True
        self.checking = False
        self.placingCard = False

        self.myMaxMana = 1
        self.myMana = 1
        self.aiMaxMana = 0
        self.aiMana = 0
        self.manaFImg = pygame.transform.scale(pygame.image.load(shared.path + "image/ManaF.png").convert_alpha(), (int(shared.WIDTH*0.016), int(shared.WIDTH*0.016)))
        self.manaTImg = pygame.transform.scale(pygame.image.load(shared.path + "image/ManaT.png").convert_alpha(), (int(shared.WIDTH*0.016), int(shared.WIDTH*0.016)))

        self.clickTimer = 0
        self.clickedCard = -1
        self.releasedCard = -1
        self.placingIndex = -1
        self.pointing = [0, 0]
        self.cardSet = {}
        self.cardSet["myCard"] = []
        self.cardSet["aiCard"] = []
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

    def attack(self, attacker, target, isPlayerTurn = True):
        if isPlayerTurn:
            if target != 99:
                self.cardSet["aiCard"][target].hp -= self.cardSet["myCard"][attacker].atk
                self.cardSet["myCard"][attacker].hp -= self.cardSet["aiCard"][target].atk
            else:
                self.aihp -= self.cardSet["myCard"][attacker].atk
            
            self.cardSet["myCard"][attacker].attacked = True
        else:
            if target != 99:
                self.cardSet["myCard"][target].hp -= self.cardSet["aiCard"][attacker].atk
                self.cardSet["aiCard"][attacker].hp -= self.cardSet["myCard"][target].atk
            else:
                self.myhp -= self.cardSet["aiCard"][attacker].atk

            self.cardSet["aiCard"][attacker].attacked = True       

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
        if self.aihp <= 0:
            shared.game_state = "win"
        if self.myhp <= 0:
            shared.game_state = "lost"

    def switchTurn(self):
        self.draw()
        # player to ai
        if (self.isPlayerTurn):
            self.isPlayerTurn = False
            self.giveCard(False)
            for card in self.cardSet["aiCard"]:
                card.attacked = False
            for card in self.cardSet["myCard"]:
                card.round += 1
            if self.aiMaxMana < 10:
                self.aiMaxMana += 1
            self.aiMana = self.aiMaxMana
            #Creating AI system here:
            self.ai.execute_best_move()
        # ai to player
        else:
            self.isPlayerTurn = True
            self.giveCard(True)
            for card in self.cardSet["myCard"]:
                card.attacked = False
            for card in self.cardSet["aiCard"]:
                card.round += 1
            if self.myMaxMana < 10:
                self.myMaxMana += 1
            self.myMana = self.myMaxMana

    def giveCard(self, isPlayerTurn):
        if isPlayerTurn:
            if len(self.cardSet["mySetCard"]) > 0:
                temp = self.cardSet["mySetCard"][self.myCardOrder.pop(0)]
                if len(self.cardSet["myHandCard"]) <= 6:
                    temp = self.cardSet["mySetCard"][self.myCardOrder.pop(0)]
                self.cardSet["myHandCard"].append(Card(temp[0], temp[1], temp[2], pygame.image.load(shared.path + "image/cardBack.png") if temp[3] == None else pygame.image.load(shared.path + "image/" + temp[7]), temp[8]))
            else:
                self.myhp -= 1
        else:
            if len(self.cardSet["aiSetCard"]) > 0:
                temp = self.cardSet["aiSetCard"][self.aiCardOrder.pop(0)]
                if len(self.cardSet["aiHandCard"]) <= 6:
                    self.cardSet["aiHandCard"].append(Card(temp[0], temp[1], temp[2], pygame.image.load(shared.path + "image/cardBack.png") if temp[3] == None else pygame.image.load(shared.path + "image/" + temp[7]), temp[8]))
            else:
                self.aihp -= 1

    def draw(self):
        #bg
        shared.screen.blit(pygame.transform.scale(pygame.image.load(shared.path + "image/gameBoard_v2.jpg"), (shared.WIDTH, shared.HEIGHT)), (0, 0))

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
            tempImg = pygame.image.load(shared.path + "image/cardBack.png")

            rotated_image, rect = rotate(pygame.transform.scale(pygame.image.load(shared.path + "image/cardBack.png"), cardDim), angle, [shared.WIDTH*0.1, shared.HEIGHT*0.25-cardDim[1]], pygame.math.Vector2(0, cardDim[1]))
            shared.screen.blit(rotated_image, rect)
            if(len(self.cardSet["aiHandCard"]) > 10):
                angle += 90/(len(self.cardSet["aiHandCard"])-1)
            else:
                angle += 9

        # draw arrow
        if (self.clickedCard != -1 and self.clickTimer > 0):
            pointA = (self.cardSet["myCard"][self.clickedCard].rect[0]+cardDim[0]/2, self.cardSet["myCard"][self.clickedCard].rect[1]+cardDim[1]/2)
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

        # draw mana crystal
        for i in range(self.myMaxMana):
            shared.screen.blit(self.manaFImg, (int(shared.WIDTH*0.68+i*shared.WIDTH*0.016), shared.HEIGHT*0.96))
        for i in range(self.myMana):
            shared.screen.blit(self.manaTImg, (int(shared.WIDTH*0.68+i*shared.WIDTH*0.016), shared.HEIGHT*0.96))
        shared.text(shared.screen, str(self.myMana) + "/" + str(self.myMaxMana), (255, 255, 255), int(shared.WIDTH*0.016), (int(shared.WIDTH*0.65), int(shared.HEIGHT*0.96+shared.WIDTH*0.016/2)), "center")

        for i in range(self.aiMaxMana):
            shared.screen.blit(self.manaFImg, (int(shared.WIDTH*0.66+i*shared.WIDTH*0.016), shared.HEIGHT*0.08))
        for i in range(self.aiMana):
            shared.screen.blit(self.manaTImg, (int(shared.WIDTH*0.66+i*shared.WIDTH*0.016), shared.HEIGHT*0.08))
        shared.text(shared.screen, str(self.aiMana) + "/" + str(self.aiMaxMana), (255, 255, 255), int(shared.WIDTH*0.016), (int(shared.WIDTH*0.63), int(shared.HEIGHT*0.08+shared.WIDTH*0.016/2)), "center")

        shared.screen.blit(pygame.transform.scale(pygame.image.load(shared.path + "image/gameBoard_v2_up.png"), (shared.WIDTH, shared.HEIGHT)), (0, 0))


        #after I clicked my hand card
        if(self.checking):
            my_surface = pygame.Surface((shared.WIDTH, shared.HEIGHT))
            my_surface = my_surface.convert_alpha()
            my_surface.fill((0, 0, 0, 64))
            shared.screen.blit(my_surface, [0, 0])

            left = shared.WIDTH/2 - (len(self.cardSet["myHandCard"])*(cardDimEnlarged[0] + shared.WIDTH/40) - shared.WIDTH/40)/2
            top = shared.HEIGHT*0.35
            for card in self.cardSet["myHandCard"]:
                shared.screen.blit(pygame.transform.smoothscale(card.image, cardDimEnlarged), [left, top])
                card.rectEnlarged = pygame.Rect(left, top, cardDimEnlarged[0], cardDimEnlarged[1])

                pygame.draw.circle(shared.screen, (200, 200, 100), [left, top+cardDimEnlarged[1]], shared.WIDTH/75)  #attack
                shared.text(shared.screen, str(card.atk), (0, 0, 0), int(shared.WIDTH/64), [left, top+cardDimEnlarged[1]], "center")

                pygame.draw.circle(shared.screen, (0, 181, 172), [left, top], shared.WIDTH/75)  # cost
                shared.text(shared.screen, str(card.cost), (0, 0, 0), int(shared.WIDTH/64), [left, top], "center")

                pygame.draw.circle(shared.screen, (242, 89, 0), [left+cardDimEnlarged[0], top+cardDimEnlarged[1]], shared.WIDTH/75)  #health
                shared.text(shared.screen, str(card.hp), (0, 0, 0), int(shared.WIDTH/64), [left+cardDimEnlarged[0], top+cardDimEnlarged[1]], "center")

                left += cardDimEnlarged[0] + shared.WIDTH/40

        # draw arrow when placing card
            
        if(self.placingCard and self.isPlayerTurn):
            pygame.draw.rect(shared.screen, (255, 0, 0), [shared.WIDTH/2 - (shared.WIDTH/80*8 + cardDim[0]*7)/2, shared.HEIGHT*0.55, (shared.WIDTH/80*8 + cardDim[0]*7), cardDim[1]], width = int(shared.WIDTH/100))
            self.pointing = [0, 0]
            arrowSideLen = shared.HEIGHT/50
            mouse_pos = pygame.mouse.get_pos()
            if (shared.HEIGHT*0.55 <= mouse_pos[1] <= shared.HEIGHT*0.55+cardDim[1]):
                if len(self.cardSet["myCard"]) == 0:
                    self.pointing = [shared.WIDTH/2, shared.HEIGHT*0.55 + cardDim[1] +shared.HEIGHT/50]
                else:
                    for i in range(len(self.cardSet["myCard"])):
                        if self.cardSet["myCard"][i].rect.left-cardDim[0]/2-shared.WIDTH/80 <=  mouse_pos[0] < self.cardSet["myCard"][i].rect.left+cardDim[0]/2:
                            self.pointing = [self.cardSet["myCard"][i].rect.left-shared.WIDTH/160, self.cardSet["myCard"][i].rect.bottom+shared.HEIGHT/50]
                            break
                    if self.cardSet["myCard"][-1].rect.left+cardDim[0]/2 <=  mouse_pos[0] < self.cardSet["myCard"][-1].rect.right+shared.WIDTH/80+cardDim[0]/2:
                        self.pointing = [self.cardSet["myCard"][-1].rect.left+cardDim[0] + shared.WIDTH/160, self.cardSet["myCard"][-1].rect.bottom+shared.HEIGHT/50]
            elif (shared.WIDTH*0.8 <= mouse_pos[0] <= shared.WIDTH and shared.HEIGHT*0.7 <= mouse_pos[1] <= shared.HEIGHT*0.9):
                self.pointing = [shared.WIDTH*0.9, shared.HEIGHT*0.9]
            pygame.draw.polygon(shared.screen, (255, 0, 0), [
                self.pointing, 
                [self.pointing[0]+int(round(arrowSideLen*math.cos(-math.pi/2-math.pi/6))), self.pointing[1]-int(round(arrowSideLen*math.sin(-math.pi/2-math.pi/6)))], 
                [self.pointing[0]+int(round(arrowSideLen*math.cos(-math.pi/2+math.pi/6))), self.pointing[1]-int(round(arrowSideLen*math.sin(-math.pi/2+math.pi/6)))]
                    ])

    def ckeckingf(self):
        self.placingCard = False
        self.checking = True

    def placingCardf(self, i):
        self.checking = False
        self.placingCard = True
        self.placingIndex = i

    def placeCardTo(self, cardid, targetpos):
        if self.isPlayerTurn:
            temp = self.cardSet["myHandCard"].pop(cardid)
            if targetpos < len(self.cardSet["myCard"]):
                self.cardSet["myCard"] = self.cardSet["myCard"][:targetpos] + [temp] + self.cardSet["myCard"][targetpos:]
            else:
                self.cardSet["myCard"].append(temp)
            self.myMana -= temp.cost
        else:
            temp = self.cardSet["aiHandCard"].pop(cardid)
            if targetpos < len(self.cardSet["aiCard"]):
                self.cardSet["aiCard"] = self.cardSet["aiCard"][:targetpos] + [temp] + self.cardSet["aiCard"][targetpos:]
            else:
                self.cardSet["aiCard"].append(temp)
            self.aiMana -= temp.cost

sys = Sys()



while running:

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    #Use to track mouse position
    #print([round(100*mouse_pos[0]/shared.WIDTH), round(100*mouse_pos[1]/shared.HEIGHT)])
    #print(mouse_pos[0],mouse_pos[1])
    #print(shared.WIDTH,shared.HEIGHT)
    #color = shared.screen.get_at(mouse_pos)  # Get (R, G, B, A)
    #print(color[:3])
    ###

    if shared.renewed == False:
        sys = Sys()
        shared.renewed = True

    if shared.game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.clickTimer += 1

                #clicking my card
                sys.clickedCard = -1
                if(sys.isPlayerTurn and not(sys.checking or sys.placingCard)):
                    # user clicked game board card
                    for i in range(len(sys.cardSet["myCard"])):
                        if sys.cardSet["myCard"][i].rect.collidepoint(mouse_pos) and sys.cardSet["myCard"][i].attacked == False:
                            sys.clickedCard = i
                            break

                # switchTurn (!!!!!!!!!!!!!!need put inside player turn after ai is done!!!!!!!!!!)
                if not(sys.checking or sys.placingCard):
                    if click_circle(mouse_pos, [shared.WIDTH*0.95, shared.HEIGHT/2], shared.WIDTH/24) or (shared.WIDTH*0.94 <= mouse_pos[0] <= shared.WIDTH*0.94+2*shared.WIDTH/24  and shared.HEIGHT/2-shared.WIDTH/24 <= mouse_pos[1] <= shared.HEIGHT/2-shared.WIDTH/24+2*shared.WIDTH/24):
                        sys.switchTurn()

            if event.type == pygame.MOUSEBUTTONUP:
                sys.releasedCard = -1
                # switch checking
                if (sys.checking):
                    if (0 <= mouse_pos[1] <= shared.HEIGHT*0.3 or shared.HEIGHT*0.7 <= mouse_pos[1] <= shared.HEIGHT):
                        sys.checking = False
                elif(sys.isPlayerTurn and not(sys.placingCard or sys.checking) and len(sys.cardSet["myCard"]) < 7 and shared.WIDTH*0.8 <= mouse_pos[0] <= shared.WIDTH and shared.HEIGHT*0.7 <= mouse_pos[1] <= shared.HEIGHT*0.9):
                    sys.ckeckingf()
                                    
                # place card to desk
                if (sys.placingCard):
                    if (shared.HEIGHT*0.55 <= mouse_pos[1] <= shared.HEIGHT*0.55+cardDim[1]):
                        if len(sys.cardSet["myCard"]) == 0:
                            sys.placingCard = False
                            sys.placeCardTo(sys.placingIndex, 0)
                        else:
                            for i in range(len(sys.cardSet["myCard"])):
                                if (sys.cardSet["myCard"][i].rect.left-cardDim[0]/2-shared.WIDTH/80 <=  mouse_pos[0] < sys.cardSet["myCard"][i].rect.left+cardDim[0]/2):
                                    sys.placingCard = False
                                    sys.placeCardTo(sys.placingIndex, i)
                                    break
                            if (sys.cardSet["myCard"][-1].rect.left+cardDim[0]/2 <=  mouse_pos[0] < sys.cardSet["myCard"][-1].rect.right+shared.WIDTH/80+cardDim[0]/2):
                                    sys.placingCard = False
                                    sys.placeCardTo(sys.placingIndex, len(sys.cardSet["myCard"]))
                    elif (shared.WIDTH*0.8 <= mouse_pos[0] <= shared.WIDTH and shared.HEIGHT*0.7 <= mouse_pos[1] <= shared.HEIGHT*0.9):
                        sys.placingCard = False

                # to determine user want to attack who
                if(sys.isPlayerTurn and not(sys.checking or sys.placingCard)):
                    for i in range(len(sys.cardSet["aiCard"])):
                        if sys.cardSet["aiCard"][i].rect.collidepoint(mouse_pos):
                            sys.releasedCard = i
                            break
                if click_circle(mouse_pos, [shared.WIDTH/2, shared.HEIGHT*0.1], shared.HEIGHT*0.05):
                    sys.releasedCard = 99
                
                #attack
                if (sys.clickedCard != -1 and sys.releasedCard != -1):
                    sys.attack(sys.clickedCard, sys.releasedCard)
                    sys.checkAlive()
                
                # selecting card to place in checking mode
                try:
                    if(sys.isPlayerTurn and sys.checking):
                        for i in range(len(sys.cardSet["myHandCard"])):
                            if sys.cardSet["myHandCard"][i].rectEnlarged.collidepoint(mouse_pos):
                                if(sys.cardSet["myHandCard"][i].cost <= sys.myMana):
                                    sys.placingCardf(i)
                                break
                except:
                    pass
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
    
    elif shared.game_state == "card_collection":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cardcollection.cardcollection_main(mouse_pos, mouse_click)
        pygame.display.update()
        shared.clock.tick(shared.fps)
        

        pygame.display.update()
        shared.clock.tick(shared.fps)
    
    elif shared.game_state == "settings":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        shared.screen.fill((105, 77, 0))
        ## Your code

        pygame.display.update()
        shared.clock.tick(shared.fps)

    elif shared.game_state == "login":
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

        shared.text(shared.screen, "YOU WIN!!", (0, 0, 0), int(shared.HEIGHT/10), (shared.WIDTH/2, shared.HEIGHT/2), "center")
        ## Your code

        pygame.display.update()
        shared.clock.tick(shared.fps)

    elif shared.game_state == "lost":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        shared.screen.fill((105, 77, 0))
        ## Your code
        shared.text(shared.screen, "YOU LOST", (0, 0, 0), int(shared.HEIGHT/10), (shared.WIDTH/2, shared.HEIGHT/2), "center")

        pygame.display.update()
        shared.clock.tick(shared.fps)