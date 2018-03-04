#Card Dimensions - TilesetA = 243.2 x 167.615384615, TilesetB = 108.4 x 74.6153846154, TilesetC = 98 x 73
#Suit Order - TilesetA = Clubs,Diamonds,Hearts,Spades , TilesetB = Clubs,Diamonds,Hearts,Spades , TilesetC = Clubs,Spades,Hearts,Diamonds

import pygame, sys, math, time, os, random, copy
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)
cs_red = (150,0,0)
cs_green = (0,150,0)

cardW, cardH = 73, 98
screenW, screenH = 1000, 800

pygame.init()
screen=pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Cardgame')

holding = False
lastDeck = ""
holdOffset = (0,0)
saveNo = 0
autoSaves = []

images = []
tileset = pygame.image.load("tilesetC.png")

class Mode():
    def __init__(self,decks,undo):
        self.decks = {}
        self.deckList = decks
        self.undo = undo


modes = {"SolitaireTest":    Mode([
                                [(917,128),(0,1),[("13","0"),("12","0"),("11","0"),("10","0"),("9","0"),("8","0"),("7","0"),("6","0"),("5","0"),("4","0"),("3","0"),("2","0")],25,"MB7",False],
                                [(824,128),(0,1),[("13","1"),("12","1"),("11","1"),("10","1"),("9","1"),("8","1"),("7","1"),("6","1"),("5","1"),("4","1"),("3","1")],25,"MB6",False],
                                [(731,128),(0,1),[("13","2"),("12","2"),("11","2"),("10","2"),("9","2"),("8","2"),("7","2"),("6","2"),("5","2"),("4","2"),("3","2"),],25,"MB5",False],
                                [(638,128),(0,1),[("13","3"),("12","3"),("11","3"),("10","3"),("9","3"),("8","3"),("7","3"),("6","3"),("5","3"),("4","3"),("3","3"),("2","3")],25,"MB4",False],
                                [(545,128),(0,1),[],25,"MB3",False],
                                [(452,128),(0,1),[],25,"MB2",False],
                                [(359,128),(0,1),[],25,"MB1",False],
                                [(10,10),(0,0),[("2","1"),("2","2")],15,"Deck",False],
                                [(103,10),(1,0),[],15,"Discard",False],
                                [(917,10),(0,0),[("1","0")],15,"Stack4",False],
                                [(824,10),(0,0),[("1","1")],15,"Stack3",False],
                                [(731,10),(0,0),[("1","2")],15,"Stack2",False],
                                [(638,10),(0,0),[("1","3")],15,"Stack1",False],
                                [(-1000,-1000),(0,1),[],15,"Hand",False]
                                ],True),
            
            "Klondike":        Mode([
                                [(917,128),(0,1),[],25,"MB7",False],
                                [(824,128),(0,1),[],25,"MB6",False],
                                [(731,128),(0,1),[],25,"MB5",False],
                                [(638,128),(0,1),[],25,"MB4",False],
                                [(545,128),(0,1),[],25,"MB3",False],
                                [(452,128),(0,1),[],25,"MB2",False],
                                [(359,128),(0,1),[],25,"MB1",False],
                                [(10,10),(0,0),[("Fill","1")],15,"Deck",True],
                                [(103,10),(1,0),[],15,"Discard",False],
                                [(917,10),(0,0),[],15,"Stack1",False],
                                [(824,10),(0,0),[],15,"Stack2",False],
                                [(731,10),(0,0),[],15,"Stack3",False],
                                [(638,10),(0,0),[],15,"Stack4",False],
                                [(-1000,-1000),(0,1),[],15,"Hand",False]
                                     ],True),
            "Spider1Suit":        Mode([
                                [(917,128),(0,1),[],25,"MB10",False],
                                [(829,128),(0,1),[],25,"MB9",False],
                                [(741,128),(0,1),[],25,"MB8",False],
                                [(653,128),(0,1),[],25,"MB7",False],
                                [(565,128),(0,1),[],25,"MB6",False],
                                [(477,128),(0,1),[],25,"MB5",False],
                                [(389,128),(0,1),[],25,"MB4",False],
                                [(301,128),(0,1),[],25,"MB3",False],
                                [(213,128),(0,1),[],25,"MB2",False],
                                [(125,128),(0,1),[],25,"MB1",False],
                                [(10,10),(0,0),[("Spades","8")],15,"Deck",True],
                                [(917,10),(0,0),[],15,"Stack8",False],
                                [(824,10),(0,0),[],15,"Stack7",False],
                                [(731,10),(0,0),[],15,"Stack6",False],
                                [(638,10),(0,0),[],15,"Stack5",False],
                                [(545,10),(0,0),[],15,"Stack4",False],
                                [(452,10),(0,0),[],15,"Stack3",False],
                                [(359,10),(0,0),[],15,"Stack2",False],
                                [(266,10),(0,0),[],15,"Stack1",False],
                                [(-1000,-1000),(0,1),[],15,"Hand",False]
                                     ],True),
         
            "Spider2Suit":        Mode([
                                [(917,128),(0,1),[],25,"MB10",False],
                                [(829,128),(0,1),[],25,"MB9",False],
                                [(741,128),(0,1),[],25,"MB8",False],
                                [(653,128),(0,1),[],25,"MB7",False],
                                [(565,128),(0,1),[],25,"MB6",False],
                                [(477,128),(0,1),[],25,"MB5",False],
                                [(389,128),(0,1),[],25,"MB4",False],
                                [(301,128),(0,1),[],25,"MB3",False],
                                [(213,128),(0,1),[],25,"MB2",False],
                                [(125,128),(0,1),[],25,"MB1",False],
                                [(10,10),(0,0),[("Spades","4"),("Diamonds","4")],15,"Deck",True],
                                [(917,10),(0,0),[],15,"Stack8",False],
                                [(824,10),(0,0),[],15,"Stack7",False],
                                [(731,10),(0,0),[],15,"Stack6",False],
                                [(638,10),(0,0),[],15,"Stack5",False],
                                [(545,10),(0,0),[],15,"Stack4",False],
                                [(452,10),(0,0),[],15,"Stack3",False],
                                [(359,10),(0,0),[],15,"Stack2",False],
                                [(266,10),(0,0),[],15,"Stack1",False],
                                [(-1000,-1000),(0,1),[],15,"Hand",False]
                                     ],True),
         
            "Spider":        Mode([
                                [(917,128),(0,1),[],25,"MB10",False],
                                [(829,128),(0,1),[],25,"MB9",False],
                                [(741,128),(0,1),[],25,"MB8",False],
                                [(653,128),(0,1),[],25,"MB7",False],
                                [(565,128),(0,1),[],25,"MB6",False],
                                [(477,128),(0,1),[],25,"MB5",False],
                                [(389,128),(0,1),[],25,"MB4",False],
                                [(301,128),(0,1),[],25,"MB3",False],
                                [(213,128),(0,1),[],25,"MB2",False],
                                [(125,128),(0,1),[],25,"MB1",False],
                                [(10,10),(0,0),[("Fill","2")],15,"Deck",True],
                                [(917,10),(0,0),[],15,"Stack8",False],
                                [(824,10),(0,0),[],15,"Stack7",False],
                                [(731,10),(0,0),[],15,"Stack6",False],
                                [(638,10),(0,0),[],15,"Stack5",False],
                                [(545,10),(0,0),[],15,"Stack4",False],
                                [(452,10),(0,0),[],15,"Stack3",False],
                                [(359,10),(0,0),[],15,"Stack2",False],
                                [(266,10),(0,0),[],15,"Stack1",False],
                                [(-1000,-1000),(0,1),[],15,"Hand",False]
                                     ],True),
            "Pyramid":        Mode([
                                [(917,128),(0,1),[],25,"R11",False],
                                [(829,128),(0,1),[],25,"R21",False],
                                [(741,128),(0,1),[],25,"R22",False],
                                [(653,128),(0,1),[],25,"R31",False],
                                [(565,128),(0,1),[],25,"R32",False],
                                [(477,128),(0,1),[],25,"R33",False],
                                [(389,128),(0,1),[],25,"R41",False],
                                [(301,128),(0,1),[],25,"R42",False],
                                [(213,128),(0,1),[],25,"R43",False],
                                [(125,128),(0,1),[],25,"R44",False],
                                [(824,128),(0,0),[],15,"R51",False],
                                [(731,128),(0,0),[],15,"R52",False],
                                [(638,128),(0,0),[],15,"R53",False],
                                [(545,128),(0,0),[],15,"R54",False],
                                [(452,128),(0,0),[],15,"R55",False],
                                [(359,128),(0,0),[],15,"R61",False],
                                [(266,128),(0,0),[],15,"R62",False],
                                [(266,128),(0,0),[],15,"R63",False],
                                [(266,128),(0,0),[],15,"R64",False],
                                [(266,128),(0,0),[],15,"R65",False],
                                [(266,128),(0,0),[],15,"R66",False],
                                [(266,128),(0,0),[],15,"R71",False],
                                [(266,128),(0,0),[],15,"R72",False],
                                [(266,128),(0,0),[],15,"R73",False],
                                [(266,128),(0,0),[],15,"R74",False],
                                [(266,128),(0,0),[],15,"R75",False],
                                [(266,128),(0,0),[],15,"R76",False],
                                [(266,128),(0,0),[],15,"R77",False],
                                [(10,10),(0,0),[("Fill","2")],15,"Deck",True],
                                [(917,10),(0,0),[],15,"Discard",False],
                                     ],True),
            
            "Menu":             Mode([],False)
                }
for j in range(5):
    for i in range(13):
       surf = pygame.Surface((cardW-2, cardH-2))
       surf.blit(tileset,(-i*cardW-1,-j*cardH-1))
       images.append(surf)
       if j == 4:
          break
        
undoImage = pygame.image.load("undo.png")
undoButton = (undoImage,(10,110))

class Card():
    def __init__(self, val, suit):
       self.val = val
       self.hidden = True
       self.suit = suit
       self.color = suit//2
       self.imgIndex = suit*13+val

class Deck():
    global modes
    def __init__(self,pos,direction,cardVals,spacing,ID,shuffle):
        
        self.cards = []
        if cardVals == []:
            self.cards = []
            
        elif cardVals[0][0] == "Fill":
            for x in range(int(cardVals[0][1])):
                for i in range(4):
                    for j in range(13):
                        self.cards.append(Card(j,i))

        elif cardVals[0][0] == "Random":
            rand = random.randint(0,3)
            for x in range(int(cardVals[0][1])):
                for j in range(13):
                    self.cards.append(Card(j,rand))
                    
        else:
            for x in range(len(cardVals)):
                skip = False
                if cardVals[x][0] == "Clubs":
                    for i in range(int(cardVals[x][1])):
                        for j in range(13):
                            self.cards.append(Card(j,0))
                    skip = True
                        
                elif cardVals[x][0] == "Spades":
                    for i in range(int(cardVals[x][1])):
                        for j in range(13):
                            self.cards.append(Card(j,1))
                    skip = True
                                   
                elif cardVals[x][0] == "Hearts":
                    for i in range(int(cardVals[x][1])):
                        for j in range(13):
                            self.cards.append(Card(j,2))
                    skip = True
                        
                elif cardVals[x][0] == "Diamonds":
                    for i in range(int(cardVals[x][1])):
                        for j in range(13):
                            self.cards.append(Card(j,3))
                    skip = True

                if skip != True:
                            
                    if cardVals[x][1] == "Clubs" or cardVals[x][1] == "0":
                        j = 0
                    elif cardVals[x][1] == "Spades" or cardVals[x][1] == "1":
                        j = 1
                    elif cardVals[x][1] == "Hearts" or cardVals[x][1] == "2":
                        j = 2
                    elif cardVals[x][1] == "Diamonds" or cardVals[x][1] == "3":
                        j = 3
                        
                    if cardVals[x][0] == "King":
                        i = 12
                    elif cardVals[x][0] == "Queen":
                        i = 11
                    elif cardVals[x][0] == "Jack":
                        i = 10
                    elif cardVals[x][0] == "Ace":
                        i = 0
                    elif int(cardVals[x][0]) <= 13 and int(cardVals[x][0]) >= 1:
                        i = int(cardVals[x][0])-1

                    self.cards.append(Card(i,j))

        
        self.pos = pos
        self.ID = ID
        self.direction = direction
        self.spacing = spacing
        self.mainrect = Rect(pos[0],pos[1],cardW,cardH)
        if shuffle:
            self.shuffle()
        modes[mode].decks[ID] = self
        self.updateMainRect()
   
    def draw(self):
        if len(self.cards) > 0:
            if self.direction != (0,0):
                for i in range(len(self.cards)):
                    if self.cards[i].hidden == False:
                        screen.blit(images[self.cards[i].imgIndex],(self.pos[0]+self.direction[0]*self.spacing*i,self.pos[1]+self.direction[1]*i*self.spacing))
                    else:
                        screen.blit(images[52],(self.pos[0]+self.direction[0]*self.spacing*i,self.pos[1]+self.direction[1]*i*self.spacing))
            else:
                if self.cards[-1].hidden == False:
                    screen.blit(images[self.cards[-1].imgIndex],(self.pos))
                else:
                    screen.blit(images[52],(self.pos))
        else:
            pygame.draw.rect(screen, (0,130,0),Rect(self.pos[0],self.pos[1],cardW,cardH),0)

    def updateMainRect(self):
        if len(self.cards) > 0:
            self.mainrect=Rect(self.pos[0]-1,self.pos[1]-1,cardW+(len(self.cards)-1)*self.spacing*self.direction[0],cardH+(len(self.cards)-1)*self.spacing*self.direction[1])
        else:
            self.mainrect=Rect(self.pos[0]-1,self.pos[1]-1,cardW+2,cardH+2)
          
    def shuffle(self):
        if len(self.cards) > 0:
            random.shuffle(self.cards)

    def popCard(d1,d2,addUnder = False):
        global modes
        if len(modes[mode].decks[d1].cards) > 0:
            card = modes[mode].decks[d1].cards[-1]
            modes[mode].decks[d1].cards.remove(modes[mode].decks[d1].cards[-1])
            
            if addUnder:
               modes[mode].decks[d2].cards.insert(0,card)
            else:
                modes[mode].decks[d2].cards.append(card)
        modes[mode].decks[d1].updateMainRect()
        modes[mode].decks[d2].updateMainRect()


def initializeGame():
    if len(modes[mode].deckList) > 0:
        for i in range(len(modes[mode].deckList)):
            data = modes[mode].deckList[i]
            Deck(data[0],data[1],data[2],data[3],data[4],data[5])
        autoSaves = []
        saveNo = 0
            
    if mode == "Klondike":
        for i in range(7):
            i = 7-i
            for j in range(i):
                Deck.popCard("Deck","MB"+str(6-j+1))

        for deck in modes[mode].decks:
            if modes[mode].decks[deck].ID[:2] == "MB":
                if len(modes[mode].decks[deck].cards) > 0:
                    modes[mode].decks[deck].cards[-1].hidden = False
                    
    elif mode == "Spider1Suit" or mode == "Spider2Suit" or mode == "Spider":
        for i in range(6):
            for j in range(4):
                Deck.popCard("Deck","MB"+str(j+1))
                
        for i in range(5):
            for j in range(6):
                Deck.popCard("Deck","MB"+str(j+5))

        for deck in modes[mode].decks:
            if modes[mode].decks[deck].ID[:2] == "MB":
                if len(modes[mode].decks[deck].cards) > 0:
                    modes[mode].decks[deck].cards[-1].hidden = False
            
    elif mode == "SolitaireTest":
        for deck in modes[mode].decks:
            if modes[mode].decks[deck].ID[:2] == "MB":
                if len(modes[mode].decks[deck].cards) > 0:
                    for i in range(len(modes[mode].decks[deck].cards)):
                        modes[mode].decks[deck].cards[i].hidden = False
                        
            if modes[mode].decks[deck].ID[:5] == "Stack":
                if len(modes[mode].decks[deck].cards) > 0:
                    for i in range(len(modes[mode].decks[deck].cards)):
                        modes[mode].decks[deck].cards[i].hidden = False

def handleHand():
    global modes
    m = pygame.mouse.get_pos()
    if holding:
       modes[mode].decks["Hand"].pos = (m[0]-holdOffset[0],m[1]-holdOffset[1])

def getInput():
    global holding, holdOffset, lastDeck, saveNo, autoSaves, modes

    if won == False:
        m = pygame.mouse.get_pos()
        if mode == "SolitaireTest" or mode == "Klondike":
            for deck in modes[mode].decks:
               if modes[mode].decks[deck].mainrect.collidepoint(m) or modes[mode].decks[deck].mainrect.colliderect(modes[mode].decks["Hand"].pos[0],modes[mode].decks["Hand"].pos[1],cardW,cardH):
                  if len(modes[mode].decks[deck].cards)>0:
                     if modes[mode].decks[deck].ID != "Deck":
                        if pygame.mouse.get_pressed()[0] and not holding:
                            for i in range(len(modes[mode].decks[deck].cards)):
                               if i < len(modes[mode].decks[deck].cards)-1:
                                  if modes[mode].decks[deck].ID != "Discard":
                                     if Rect(modes[mode].decks[deck].pos[0] + i*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0],modes[mode].decks[deck].pos[1] + i*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1],cardW,modes[mode].decks[deck].spacing).collidepoint(m):
                                        if not modes[mode].decks[deck].cards[i].hidden:
                                            save()
                                            for j in range(len(modes[mode].decks[deck].cards)-i):
                                               Deck.popCard(modes[mode].decks[deck].ID,"Hand",addUnder = True)
                                            holding = True
                                            lastDeck = modes[mode].decks[deck].ID
                                            holdOffset = (m[0]-modes[mode].decks[deck].pos[0] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0]*len(modes[mode].decks[deck].cards)-2,m[1]-modes[mode].decks[deck].pos[1] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1]*len(modes[mode].decks[deck].cards)-2)
                                            break
                               else:
                                  if Rect(modes[mode].decks[deck].pos[0]+(len(modes[mode].decks[deck].cards)-1)*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0],modes[mode].decks[deck].pos[1]+(len(modes[mode].decks[deck].cards)-1)*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1],cardW,cardH).collidepoint(m):
                                     save()
                                     Deck.popCard(modes[mode].decks[deck].ID,"Hand",addUnder = True)
                                     holding = True
                                     lastDeck = modes[mode].decks[deck].ID
                                     holdOffset = (m[0]-modes[mode].decks[deck].pos[0] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0]*len(modes[mode].decks[deck].cards)-2,m[1]-modes[mode].decks[deck].pos[1] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1]*len(modes[mode].decks[deck].cards)-2)
                  if not holding or deck[:2] == "MB" or deck[:5] == "Stack":
                     if len(modes[mode].decks[deck].cards) > 0 or holding:
                        pygame.draw.rect(screen,white,modes[mode].decks[deck].mainrect,3)
                        
        elif mode == "Spider1Suit" or mode == "Spider2Suit" or mode == "Spider":
            for deck in modes[mode].decks:
                if modes[mode].decks[deck].mainrect.collidepoint(m) or modes[mode].decks[deck].mainrect.colliderect(modes[mode].decks["Hand"].pos[0],modes[mode].decks["Hand"].pos[1],cardW,cardH):
                  if len(modes[mode].decks[deck].cards)>0:
                     if modes[mode].decks[deck].ID != "Deck":
                        if pygame.mouse.get_pressed()[0] and not holding:
                            for i in range(len(modes[mode].decks[deck].cards)):
                               if i < len(modes[mode].decks[deck].cards)-1:
                                 if Rect(modes[mode].decks[deck].pos[0] + i*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0],modes[mode].decks[deck].pos[1] + i*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1],cardW,modes[mode].decks[deck].spacing).collidepoint(m):
                                    if not modes[mode].decks[deck].cards[i].hidden:
                                        counter = 0
                                        target = len(modes[mode].decks[deck].cards)-i-1
                                        for j in range(target):
                                            if modes[mode].decks[deck].cards[j+i].val == modes[mode].decks[deck].cards[j+i+1].val+1:
                                                counter += 1
                                        if counter != target:
                                            break
                                        
                                        else:
                                            save()
                                            for j in range(len(modes[mode].decks[deck].cards)-i):
                                               Deck.popCard(modes[mode].decks[deck].ID,"Hand",addUnder = True)
                                            holding = True
                                            lastDeck = modes[mode].decks[deck].ID
                                            holdOffset = (m[0]-modes[mode].decks[deck].pos[0] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0]*len(modes[mode].decks[deck].cards)-2,m[1]-modes[mode].decks[deck].pos[1] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1]*len(modes[mode].decks[deck].cards)-2)
                                            break
                               else:
                                  if Rect(modes[mode].decks[deck].pos[0]+(len(modes[mode].decks[deck].cards)-1)*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0],modes[mode].decks[deck].pos[1]+(len(modes[mode].decks[deck].cards)-1)*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1],cardW,cardH).collidepoint(m):
                                     save()
                                     Deck.popCard(modes[mode].decks[deck].ID,"Hand",addUnder = True)
                                     holding = True
                                     lastDeck = modes[mode].decks[deck].ID
                                     holdOffset = (m[0]-modes[mode].decks[deck].pos[0] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0]*len(modes[mode].decks[deck].cards)-2,m[1]-modes[mode].decks[deck].pos[1] - modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1]*len(modes[mode].decks[deck].cards)-2)
                  if not holding or deck[:2] == "MB" or deck[:5] == "Stack":
                     if len(modes[mode].decks[deck].cards) > 0 or holding:
                        pygame.draw.rect(screen,white,modes[mode].decks[deck].mainrect,3)
                        
            
        changed = False
        if not pygame.mouse.get_pressed()[0] and holding:
            holding=False
            if mode == "Klondike" or mode == "SolitaireTest":
               for deck in modes[mode].decks:
                  if deck!=lastDeck:
                     if modes[mode].decks[deck].mainrect.colliderect(modes[mode].decks["Hand"].pos[0],modes[mode].decks["Hand"].pos[1],cardW,cardH) or modes[mode].decks[deck].mainrect.collidepoint(m):
                        if modes[mode].decks[deck].ID!="Deck" and modes[mode].decks[deck].ID!="Discard":
                            if modes[mode].decks[deck].ID=="Stack1" or modes[mode].decks[deck].ID=="Stack2" or modes[mode].decks[deck].ID=="Stack3" or modes[mode].decks[deck].ID=="Stack4":
                               if len(modes[mode].decks["Hand"].cards) == 1:
                                  if len(modes[mode].decks[deck].cards)>0:
                                     if modes[mode].decks[deck].cards[-1].suit==modes[mode].decks["Hand"].cards[0].suit and modes[mode].decks["Hand"].cards[0].val==modes[mode].decks[deck].cards[-1].val+1:
                                        if len(modes[mode].decks[lastDeck].cards)>0:
                                            modes[mode].decks[lastDeck].cards[-1].hidden=False
                                        lastDeck=deck
                                        changed = True
                                  else:
                                     if modes[mode].decks["Hand"].cards[0].val==0:
                                        if len(modes[mode].decks[lastDeck].cards)>0:
                                            modes[mode].decks[lastDeck].cards[-1].hidden=False
                                        lastDeck=deck
                                        changed = True
                        if modes[mode].decks[deck].ID=="MB1" or modes[mode].decks[deck].ID=="MB2" or modes[mode].decks[deck].ID=="MB3" or modes[mode].decks[deck].ID=="MB4" or modes[mode].decks[deck].ID=="MB5" or modes[mode].decks[deck].ID=="MB6" or modes[mode].decks[deck].ID=="MB7":
                            if len(modes[mode].decks[deck].cards)>0:
                               if modes[mode].decks[deck].cards[-1].color!=modes[mode].decks["Hand"].cards[0].color:
                                  if modes[mode].decks[deck].cards[-1].val==modes[mode].decks["Hand"].cards[0].val+1:
                                     if len(modes[mode].decks[lastDeck].cards)>0:
                                        modes[mode].decks[lastDeck].cards[-1].hidden=False
                                     lastDeck=deck
                                     changed = True
                            elif modes[mode].decks["Hand"].cards[0].val == 12:
                               if len(modes[mode].decks[lastDeck].cards)>0:
                                  modes[mode].decks[lastDeck].cards[-1].hidden=False
                               lastDeck=deck
                               changed = True
                               
            elif mode == "Spider1Suit" or mode == "Spider2Suit" or mode == "Spider":
                for deck in modes[mode].decks:
                    if deck!=lastDeck:
                        if modes[mode].decks[deck].mainrect.colliderect(modes[mode].decks["Hand"].pos[0],modes[mode].decks["Hand"].pos[1],cardW,cardH) or modes[mode].decks[deck].mainrect.collidepoint(m):
                            if modes[mode].decks[deck].ID!="Deck":
                                if modes[mode].decks[deck].ID=="Stack1" or modes[mode].decks[deck].ID=="Stack2" or modes[mode].decks[deck].ID=="Stack3" or modes[mode].decks[deck].ID=="Stack4" or modes[mode].decks[deck].ID=="Stack5" or modes[mode].decks[deck].ID=="Stack6" or modes[mode].decks[deck].ID=="Stack7" or modes[mode].decks[deck].ID=="Stack8":
                                    if len(modes[mode].decks["Hand"].cards) == 13:
                                        suit = modes[mode].decks["Hand"].cards[0].suit
                                        invalid = False
                                        for i in range(13):
                                            if modes[mode].decks["Hand"].cards[i].suit != suit:
                                                invalid = True
                                                break
                                        if invalid == False:    
                                            if len(modes[mode].decks[deck].cards) == 0:
                                                if len(modes[mode].decks[lastDeck].cards)>0:
                                                    modes[mode].decks[lastDeck].cards[-1].hidden=False
                                                lastDeck=deck
                                                changed = True
                         
                                if modes[mode].decks[deck].ID=="MB1" or modes[mode].decks[deck].ID=="MB2" or modes[mode].decks[deck].ID=="MB3" or modes[mode].decks[deck].ID=="MB4" or modes[mode].decks[deck].ID=="MB5" or modes[mode].decks[deck].ID=="MB6" or modes[mode].decks[deck].ID=="MB7" or modes[mode].decks[deck].ID=="MB8" or modes[mode].decks[deck].ID=="MB9" or modes[mode].decks[deck].ID=="MB10":
                                    if len(modes[mode].decks[deck].cards)>0:
                                        if (modes[mode].decks[deck].cards[-1].val==modes[mode].decks["Hand"].cards[0].val+1):
                                            if len(modes[mode].decks[lastDeck].cards)>0:
                                                modes[mode].decks[lastDeck].cards[-1].hidden=False
                                            lastDeck=deck
                                            changed = True
                                    else:
                                        if len(modes[mode].decks[lastDeck].cards)>0:
                                            modes[mode].decks[lastDeck].cards[-1].hidden=False
                                        lastDeck=deck
                                        changed = True
                               
            for i in range(len(modes[mode].decks["Hand"].cards)):
                modes[mode].decks[lastDeck].cards.append(modes[mode].decks["Hand"].cards[i])
                if changed == False:
                    if len(autoSaves)>0:
                        autoSaves.remove(autoSaves[-1])
                        saveNo -=1
            modes[mode].decks[lastDeck].updateMainRect()
            modes[mode].decks["Hand"].cards=[]
            modes[mode].decks["Hand"].pos=(-1000,-1000)

def save():
    global autoSaves, saveNo
    autoSaves.append(copy.deepcopy(modes[mode].decks))
    saveNo+=1

mode = "Menu"
initializeGame()
won = False
three = True
clock = pygame.time.Clock()
wt = 0
font = pygame.font.Font(None,200)
text = font.render("Menu",True,cs_red)

while 1:

    
    handleHand()
    screen.fill(cs_green)
    getInput()

    if mode == "Menu":
        screen.blit(text,(300,230))

    if mode == "Klondike" or mode == "SolitaireTest":
        if won == False:
            screen.blit(undoButton[0],undoButton[1])
            for deck in modes[mode].decks:
                modes[mode].decks[deck].draw()

            if len(modes[mode].decks["Deck"].cards) == 0 and len(modes[mode].decks["Discard"].cards) == 0 and not holding:
                hiddenCard = False
                for deck in modes[mode].decks:
                    if hiddenCard != True:
                        if deck[:2] == "MB":
                            for card in modes[mode].decks[deck].cards:
                                if card.hidden:
                                    hiddenCard = True
                                    break
                if hiddenCard == False:
                    if len(modes[mode].decks["Stack1"].cards) > 0 and len(modes[mode].decks["Stack2"].cards) > 0 and len(modes[mode].decks["Stack3"].cards) > 0 and len(modes[mode].decks["Stack4"].cards) > 0:
                        if modes[mode].decks["Stack1"].cards[-1].val != 12 or modes[mode].decks["Stack2"].cards[-1].val != 12 or modes[mode].decks["Stack3"].cards[-1].val != 12 or modes[mode].decks["Stack4"].cards[-1].val != 12:
                            checkBreak = False
                            for deck in modes[mode].decks:
                                if checkBreak == False:
                                    if deck[:2] == "MB":
                                        for i in range(1,5):
                                            if len(modes[mode].decks[deck].cards) > 0 and len(modes[mode].decks["Stack"+str(i)].cards) > 0:
                                                if modes[mode].decks[deck].cards[-1].val == modes[mode].decks["Stack"+str(i)].cards[-1].val+1 and modes[mode].decks[deck].cards[-1].suit == modes[mode].decks["Stack"+str(i)].cards[-1].suit:
                                                    Deck.popCard(deck,"Stack"+str(i))
                                                    pygame.time.wait(50)
                                                    checkBreak = True
                                                    break

            if len(modes[mode].decks["Stack1"].cards) > 0 and len(modes[mode].decks["Stack2"].cards) > 0 and len(modes[mode].decks["Stack3"].cards) > 0 and len(modes[mode].decks["Stack4"].cards) > 0:
                if modes[mode].decks["Stack1"].cards[-1].val == 12 and modes[mode].decks["Stack2"].cards[-1].val == 12 and modes[mode].decks["Stack3"].cards[-1].val == 12 and modes[mode].decks["Stack4"].cards[-1].val == 12:
                    print("You Win")
                    modes[mode].decks = {}
                    font = pygame.font.Font(None,200)
                    text = font.render("You Win",True,cs_red)
                    won = True
                    
    if mode == "Spider1Suit" or mode == "Spider2Suit" or mode == "Spider":
        if won == False:
            screen.blit(undoButton[0],undoButton[1])
            for deck in modes[mode].decks:
                modes[mode].decks[deck].draw()

            if len(modes[mode].decks["Stack1"].cards) > 0 and len(modes[mode].decks["Stack2"].cards) > 0 and len(modes[mode].decks["Stack3"].cards) > 0 and len(modes[mode].decks["Stack4"].cards) > 0 and len(modes[mode].decks["Stack5"].cards) > 0 and len(modes[mode].decks["Stack6"].cards) > 0 and len(modes[mode].decks["Stack7"].cards) > 0 and len(modes[mode].decks["Stack8"].cards) > 0:
                print("You Win")
                modes[mode].decks = {}
                font = pygame.font.Font(None,200)
                text = font.render("You Win",True,cs_red)
                won = True

    if won:
        wt+=clock.get_time()
        if wt < 3000:
            screen.blit(text,(250,250))
        else:
            mode = "Menu"
            initializeGame()
            text = font.render("Menu",True,cs_red)
            won = False

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if mode == "Klondike":
                if event.key == K_SPACE:
                    if three:
                        three = False
                    else:
                        three = True
                        
            if mode == "Menu":
                if event.key ==  K_1:
                    mode = "Klondike"
                    initializeGame()
                elif event.key == K_2:
                    mode = "SolitaireTest"
                    initializeGame()
                elif event.key == K_3:
                    mode = "Spider1Suit"
                    initializeGame()
                elif event.key == K_4:
                    mode = "Spider2Suit"
                    initializeGame()
                elif event.key == K_5:
                    mode = "Spider"
                    initializeGame()
                    
        if event.type == MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:

                if mode == "Klondike" or mode == "SolitaireTest":
                        
                    if Rect(10,110,73,73).collidepoint(m):
                        if saveNo > 0:
                            print("Undo")
                            for deck in modes[mode].decks:
                                modes[mode].decks = autoSaves[saveNo-1]
                            saveNo-=1
                            autoSaves.remove(autoSaves[-1])
                            if won:
                                won = False

                    elif Rect(modes[mode].decks["Deck"].pos[0],modes[mode].decks["Deck"].pos[1],cardW,cardH).collidepoint(m):
                        save()
                        if three:
                            if len(modes[mode].decks["Deck"].cards) >= 3:
                                for i in range(3):
                                    Deck.popCard("Deck","Discard")
                                    modes[mode].decks["Discard"].cards[-1].hidden=False
                            elif len(modes[mode].decks["Deck"].cards) == 2:
                                for i in range(20):
                                    Deck.popCard("Deck","Discard")
                                    modes[mode].decks["Discard"].cards[-1].hidden=False
                            elif len(modes[mode].decks["Deck"].cards) == 1:
                                Deck.popCard("Deck","Discard")
                                modes[mode].decks["Discard"].cards[-1].hidden=False
                            else:
                                for i in range(len(modes[mode].decks["Discard"].cards)):
                                    Deck.popCard("Discard","Deck")
                                    modes[mode].decks["Deck"].cards[-1].hidden=True
                        else:
                            if len(modes[mode].decks["Deck"].cards) > 0:
                                Deck.popCard("Deck","Discard")
                                modes[mode].decks["Discard"].cards[-1].hidden=False
                            
                            else:
                                for i in range(len(modes[mode].decks["Discard"].cards)):
                                    Deck.popCard("Discard","Deck")
                                    modes[mode].decks["Deck"].cards[-1].hidden=True
            
                elif mode == "Spider1Suit" or mode == "Spider2Suit" or mode == "Spider":
                    if Rect(10,110,73,73).collidepoint(m):
                        if saveNo > 0:
                            print("Undo")
                            for deck in modes[mode].decks:
                                modes[mode].decks = autoSaves[saveNo-1]
                            saveNo-=1
                            autoSaves.remove(autoSaves[-1])
                            if won:
                                won = False
                    
                    elif Rect(modes[mode].decks["Deck"].pos[0],modes[mode].decks["Deck"].pos[1],cardW,cardH).collidepoint(m):
                        save()
                    
                        if len(modes[mode].decks["Deck"].cards) > 0:
                            empty = False
                            for i in range(10):
                                if len(modes[mode].decks["MB"+str(i+1)].cards) == 0:
                                    empty = True
                                    
                            if empty == False:
                                for i in range(10):
                                    Deck.popCard("Deck","MB"+str(i+1))
                                    modes[mode].decks["MB"+str(i+1)].cards[-1].hidden=False


            if pygame.mouse.get_pressed()[2]:

                if mode == "Klondike" or mode == "SolitaireTest":
                    for deck in modes[mode].decks:
                        if Rect(modes[mode].decks[deck].pos[0]+len(modes[mode].decks[deck].cards)*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[0],modes[mode].decks[deck].pos[1]+len(modes[mode].decks[deck].cards)*modes[mode].decks[deck].spacing*modes[mode].decks[deck].direction[1],cardW,cardH).collidepoint(m):
                            for i in range(4):
                                i = i+1
                                if len(modes[mode].decks[deck].cards) > 0 and len(modes[mode].decks["Stack"+str(i)].cards) > 0:
                                    if modes[mode].decks[deck].cards[-1].val == modes[mode].decks["Stack"+str(i)].cards[-1].val+1 and modes[mode].decks[deck].cards[-1].suit == modes[mode].decks["Stack"+str(i)].cards[-1].suit:
                                        save()
                                        Deck.popCard(deck,"Stack"+str(i))
                                        if len(modes[mode].decks[deck].cards)>0:
                                            modes[mode].decks[deck].cards[-1].hidden = False
                                        break
                                elif len(modes[mode].decks[deck].cards) > 0 and len(modes[mode].decks["Stack"+str(i)].cards) == 0:
                                    if modes[mode].decks[deck].cards[-1].val == 0:
                                        save()
                                        Deck.popCard(deck,"Stack"+str(i))
                                        if len(modes[mode].decks[deck].cards)>0:
                                            modes[mode].decks[deck].cards[-1].hidden = False
                                        break
           
    pygame.display.update()
    pygame.display.flip()
    clock.tick()
