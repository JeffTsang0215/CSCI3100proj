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
        
        self.rect = []

myCard = [Card(5, 2, 2, pygame.image.load(path + "image/cardTemp.png")), Card(6, 1, 1, pygame.image.load(path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(path + "image/cardTemp.png"))]
aiCard = [Card(6, 1, 1, pygame.image.load(path + "image/cardTemp.png")), Card(6, 6, 5, pygame.image.load(path + "image/cardTemp.png"))]
myHandCard = []
aiHamdCard = []
myhp = 30
aihp = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                myHandCard.append(Card(5, 2, 2, pygame.image.load(path + "image/cardTemp.png")))
            if event.key == pygame.K_DOWN:
                myHandCard.pop()
    screen.fill((105, 77, 0))

    #card graphic me
    left = WIDTH/2 - (len(myCard)*(cardDim[0] + WIDTH/80) - WIDTH/80)/2
    top = HEIGHT*0.55

    for card in myCard:
        screen.blit(card.image, [left, top])
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
    text(screen, str(myhp), (0, 0, 0), int(WIDTH/64), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.9+HEIGHT*0.05], "center")

    angle = -45
    for card in myHandCard:
        rotated_image, rect = rotate(card.image, angle, [WIDTH*0.9, HEIGHT*0.9], pygame.math.Vector2(0, -cardDim[1]))
        screen.blit(rotated_image, rect)
        if(len(myHandCard) > 10):
            angle += 90/(len(myHandCard)-1)
        else:
            angle += 9

    #pygame.draw.circle(screen, (255, 0, 0), [WIDTH*0.9, HEIGHT*0.9], 10)


    #card graphic ai
    left = WIDTH/2 - (len(aiCard)*(cardDim[0] + WIDTH/80) - WIDTH/80)/2
    top = HEIGHT*0.30

    for card in aiCard:
        screen.blit(card.image, [left, top])
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
    text(screen, str(aihp), (0, 0, 0), int(WIDTH/64), [WIDTH/2+HEIGHT*0.05, HEIGHT*0.1+HEIGHT*0.05], "center")
    

    pygame.display.update()
    clock.tick(fps)

