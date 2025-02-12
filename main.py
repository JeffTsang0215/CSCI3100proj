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
            sys.aiCard[target].hp -= sys.myCard[attacker].atk
            print(sys.aiCard[target].hp)
        
    def draw(self):
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

        #pygame.draw.circle(screen, (255, 0, 0), [WIDTH*0.9, HEIGHT*0.9], 10)


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
        pygame.draw.circle(screen, (238, 255, 48), [WIDTH/2, HEIGHT*0.1], HEIGHT*0.05)  #me
        pygame.draw.circle(screen, (242, 89, 0), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.1+HEIGHT*0.05], HEIGHT*0.025)
        text(screen, str(self.aihp), (0, 0, 0), int(WIDTH/64), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.1+HEIGHT*0.05], "center")

        


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
            for i in range(len(sys.myCard)):
                if sys.myCard[i].rect.collidepoint(mouse_pos):
                    sys.clickedCard = i
                    break
            
 
        if event.type == pygame.MOUSEBUTTONUP:
            sys.releasedCard = -1
            for i in range(len(sys.aiCard)):
                if sys.aiCard[i].rect.collidepoint(mouse_pos):
                    sys.releasedCard = i
                    break
            if (sys.clickedCard != -1 and sys.releasedCard != -1):
                sys.attack(sys.clickedCard, sys.releasedCard)
                print([sys.clickedCard, sys.releasedCard])
                print(sys.aiCard[sys.releasedCard].hp)
            sys.clickTimer = 0

    screen.fill((105, 77, 0))

    sys.draw()
    

    pygame.display.update()
    clock.tick(fps)

