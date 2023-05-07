""""Main game logic"""
import os

import constants
import utilities
from typing import List, Dict
import pygame
from pygame.locals import RLEACCEL, KEYDOWN, K_ESCAPE, K_SPACE, QUIT
from pygame.sprite import Sprite

suite_dict = {
    0 : "Clubs",
    1 : "Diamonds",
    2 : "Hearts",
    3 : "Spades"
}
value_dict = {
    0 : "Ace",
    1 : "2",
    2 : "3",
    3 : "4",
    4 : "5",
    5 : "6",
    6 : "7",
    7 : "8",
    8 : "9",
    9 : "10",
    10 : "Jack",
    11 : "Queen",
    12 : "King"
}

class Card(Sprite):
    debug = False
    def __init__(self, value, suite):
        super(Card, self).__init__()
        # card value
        self.flipped = False
        self.value = value
        self.suite = suite

        self.card_path = os.path.join(constants.PNG_CARD_DIRECTORY, f'card{suite}{value}.png')
        if not os.path.exists(self.card_path):
            print(f"card{suite}{value}.png not found")
            return
        print(f"Card {self.__str__()} found at {self.card_path}")
        self.surf : pygame.Surface = pygame.image.load(self.card_path)
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect()
    def flip_up(self):
        self.flipped = True
        return self
    def flip_down(self):
        self.flipped = False
        return self
    def s(self) -> str:
        return f"{value_dict[self.value]}{suite_dict[self.suite][-1]}"
    @property
    def flipped(self) -> bool:
        return self._flipped
    @flipped.setter
    def flipped(self, flipped : bool):
        self._flipped = flipped
    @property
    def value(self) -> int:
        return self._value
    @value.setter
    def value(self, value : int):
        self._value = value
    @property
    def suite(self) -> int:
        return self._suite
    @suite.setter
    def suite(self, suite : int):
        self._suite = suite
    def __str__(self):
        if Card.debug:
            return f"{str(value_dict[self.value])[:3]}{suite_dict[self.suite][0]}"
        return f"{value_dict[self.value]} of {suite_dict[self.suite]}"

class Player(Sprite):
    def __init__(self, cards, id):
        super(Player, self).__init__()
        self.surf : pygame.Surface = pygame.Surface((75, 75))
        self.cards : List[Card] = cards
        self.id = id
        self.deck = Deck()
    def set_cards(self):
        self.deck = Deck().distribute_player(self)
class Deck():
    def __init__(self):
        self.piles : Dict[List[Card]] = {
            1 : [None],
            2 : [None,None],
            3 : [None,None,None],
            4 : [None,None,None,None],
            5 : [None,None,None,None,None]
            #,6 : [] 
        }
    def distribute_player(self, player : Player ):
        num_cards = 15 if len(player.cards) >= 15 else len(player.cards)
        tot_cards = 0
        exit_loop = False
        for i in range(1,6):
            if exit_loop or tot_cards + 1 > num_cards:
                break
            for j in range(0,i):
                if(tot_cards + 1 > num_cards):
                    exit_loop = True
                    break
                if j == i:
                    self.piles[i][0]=player.cards.pop().flip_up()
                else:
                    self.piles[i][j]= player.cards.pop().flip_down()
                tot_cards += 1
        return self
    def normalize(self):
        pass
    def move(self,from_pile : int, to_pile : int) -> bool:
        allowed = True
        from_card = self.piles[from_pile].pop()
        if self.can_move(from_pile, to_pile):
            self.piles[to_pile].push(self.piles[from_pile].pop())
        else:
            return False
        if len(self.piles[from_pile] is not 0):
            self.piles[from_pile][-1].flip_up()
    def can_move(self,from_pile : int, to_pile : int) -> bool:
        from_card = self.piles[from_pile].pop()
        if len(self.piles[to_pile]) == 0:
            return True
        to_card = self.piles[to_pile][-1]
        if from_card.value != to_card.value:
            return False
 
    def __str__(self):
        p = self.piles
        return f"""
        {p[1][0]}\t{p[2][0]}\t{p[3][0]}\t{p[4][0]}\t{p[5][0]}
        x\t{p[2][1]}\t{p[3][1]}\t{p[4][1]}\t{p[5][1]}
        x\tx\t{p[3][2]}\t{p[4][2]}\t{p[5][2]}
        x\tx\tx\t{p[4][3]}\t{p[5][3]}
        x\tx\tx\tx\t{p[5][4]}



        """
class Game():
    player1 : Player = None
    player2 : Player = None
    pile1 = None
    pile2 = None
    cards = None
    def __init__(self):
        super(Game, self).__init__()
        self.create_cards()
        self.create_players()
        self.init_round()
    def create_cards(self):
        self.cards = []
        for i in range(4):
            for j in range(13):
                self.cards.append(Card(j,i))
    def create_players(self):
        if self.cards is None: raise RuntimeError("Cards not initialized.")
        self.player1 = Player(self.cards[0:26],1)
        self.player2 = Player(self.cards[26:52], 2)
        print(len(self.player1.cards))
        print(len(self.player2.cards))
    def init_round(self):
        self.pile1 = []
        self.pile2 = []
        self.player1.set_cards()
        self.player2.set_cards()

        print(self.player1.deck)
NEWCARD = pygame.USEREVENT + 1

if __name__ == '1__main__':
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    game = Game()

    clock = pygame.time.Clock()
    running = True
    counter = 0
    entity = game.cards[counter]

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    counter = (counter+1) % 52
                    print(counter)
                    entity = game.cards[counter]
            elif event.type == QUIT:
                running = False
        screen.blit(entity.surf, entity.rect)

        screen.fill((255, 255, 255))
        #for entity in cards:
        #    screen.blit(entity.surf, entity.rect)
        # Flip everything to the display

        pygame.display.flip()

        # Ensure we maintain a 30 frames per second rate
        clock.tick(60)
Card.debug = True        
game = Game()