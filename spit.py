""""Main game logic"""
import os
import constants

from typing import List, Dict

from random import shuffle, seed
import numpy as np
import pygame
from pygame.locals import RLEACCEL, KEYDOWN, K_ESCAPE, K_SPACE, QUIT
from pygame.sprite import Sprite, Group
from pygame import Surface, USEREVENT
DEBUG = False

def dprint(s): print(s) if DEBUG else None
        
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
    flipped_path = os.path.join(constants.PNG_CARD_DIRECTORY,'carddown.png')
    def __init__(self, value, suite):
        super(Card, self).__init__()
        # card value
        self.flipped = False
        self.value = value
        self.suite = suite
        self.coord = (0, 0)
        self.current_path = ""
        self.card_path = os.path.join(constants.PNG_CARD_DIRECTORY, f'card{suite}{value}.png')
        if not os.path.exists(self.card_path):
            print(f"card{suite}{value}.png not found")
            return
        print(f"Card {self.__str__()} found at {self.card_path}")
        self.set_image(self.card_path)
    def set_image(self, path):
        if self.current_path == path:
            return
        self.current_path = path
        self.surf : pygame.Surface = pygame.image.load(path)
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect()
        
    @property
    def surf(self) -> Surface:
        return self._surf

    @surf.setter
    def surf(self, surf):
        self._surf = surf

    def flip_up(self):
        self.flipped = True
        self.set_image(self.card_path)
        return self

    def flip_down(self):
        self.set_image(Card.flipped_path)
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
            return f"{str(value_dict[self.value])[:3]}{suite_dict[self.suite][0]}{'u' if self.flipped else 'd'}"
        return f"{value_dict[self.value]} of {suite_dict[self.suite]}"

class Player(Sprite):
    def __init__(self, cards, id):
        super(Player, self).__init__()
        self.surf : pygame.Surface = pygame.Surface((75, 75))
        self.cards : List[Card] = cards
        self.shuffle()
        self.id = id
        self.deck = Deck()

    def shuffle(self):
        shuffle(self.cards)

    def set_cards(self):
        self.deck = Deck().distribute_player(self)

    def collect_cards(self, stack_collected):
        self.deck.sprite_group.empty()
        self.cards.extend(stack_collected)
        self.cards.extend(self.deck.stock)
        del self.deck.stock[:]
        del stack_collected[:]
        for pile in self.deck.piles:
            self.cards.extend(self.deck.piles[pile])
            del self.deck.piles[pile][:]
class Deck():
    scale = 0.05
    def __init__(self):
        self.piles : Dict[List[Card]] = {
            1 : [],
            2 : [],
            3 : [],
            4 : [],
            5 : [],
            6 : []
        }
        self.stock = []
        self.sprite_group = Group()
    def distribute_player(self, player : Player ):
        self.sprite_group.empty()
        num_cards = 15 if len(player.cards) >= 15 else len(player.cards)
        tot_cards = 0
        exit_loop = False
        base_pos = (0, 0)
        if player.id == 1:
            base_pos = (100,500)
            direction = 1
        elif player.id == 2:
            base_pos = (1180, 220)
            direction = -1
        for i in range(1,6):
            if exit_loop or tot_cards + 1 > num_cards:
                break
            for j in range(0,i):
                if(tot_cards + 1 > num_cards):
                    exit_loop = True
                    break
                if j == i-1:
                    card = player.cards.pop().flip_up()
                    card.coord = np.add(base_pos, (i*60 * direction,  j* 5 * direction ))
                    self.piles[i].append(card)
                    self.sprite_group.add(card)
                else:
                    card = player.cards.pop().flip_down()
                    card.coord = np.add(base_pos,(i*60 * direction,  j* 5 * direction ))
                    

                    self.piles[i].append(card)
                    self.sprite_group.add(card)
                tot_cards += 1
        for card in player.cards:
            self.stock.append(card)
            self.sprite_group.add(card)
        del player.cards[:]
        return self

    def normalize(self):
        pass

    def move(self,from_pile : int, to_pile : int) -> bool:
        if self.can_move(from_pile, to_pile):
            self.piles[to_pile].append(self.piles[from_pile].pop())
        else:
            return False
        if len(self.piles[from_pile]) != 0:
            self.piles[from_pile][-1].flip_up()
        return True

    def can_move(self,from_pile : int, to_pile : int) -> bool:
        if len(self.piles[from_pile]) == 0:
            return False
        from_card : Card = self.piles[from_pile][-1]
        if to_pile == 6 and from_card.value != 0:
            return False
        elif len(self.piles[to_pile]) == 0:
            return True
        to_card : Card = self.piles[to_pile][-1]
        if from_card.value == to_card.value:
            return True
        return False

    def __str__(self):
        return self.str_table()

    def str_table(self):
        output = ""
        for i in range(0,5):
            for pile in self.piles:
                output += f'{self.piles[pile][i] if i < len(self.piles[pile]) else "x"}\t'
            if i != 4:
                output += "\n"
        return output

class Game():
    player1 : Player = None
    player2 : Player = None
    
    stacks = {
        0 : [],
        1 : []
    }
    cards = None
    def __init__(self):
        super(Game, self).__init__()
        self.create_cards()
        self.create_players()

    def create_cards(self):
        self.cards = []
        for i in range(4):
            for j in range(13):
                self.cards.append(Card(j,i))

    def create_players(self):
        if self.cards is None:
            raise RuntimeError("Cards not initialized.")
        self.player1 = Player(self.cards[0:26],1)
        self.player2 = Player(self.cards[26:52], 2)

    def init_round(self):
        self.pile1 = []
        self.pile2 = []
        self.player1.set_cards()
        self.player2.set_cards()

    def flip_cards(self) -> bool:
        if len(self.player1.cards) != 0:
            self.stacks[0].append(self.player1.cards.pop().flip_up())
        if len(self.player2.cards) != 0:
            self.stacks[1].append(self.player2.cards.pop().flip_up())
    def place_card(self, player : Player, from_pile : int, to_stack : int) -> bool:
        if self.can_place_card(player, from_pile, to_stack):
            self.stacks[to_stack].append(player.deck.piles[from_pile].pop())
        else:
            return False
        if len(player.deck.piles[from_pile]) != 0:
            player.deck.piles[from_pile].flip_up()
        return True
    def can_place_card(self, player : Player, from_pile : int, to_stack : int) -> bool:
        if len(self.stacks[to_stack]) == 0:
            return False
        if len(player.deck.piles[from_pile]) == 0 or len(self.stacks[to_stack]) == 0:
            return False
        from_card = player.deck.piles[from_pile][-1]
        stack_card = self.stacks[to_stack][-1]
        return from_card.value == stack_card.value + 1\
            or  from_card.value == stack_card.value - 1\
            or (from_card.value == 12 and stack_card.value == 0)\
            or (from_card.value == 0 and stack_card.value == 12)

    def __str__(self):
        return f"*\t{self.stacks[0][-1]}\t{self.stacks[1][-1]}\t*"

    def get_top_card(self, pile_no) -> Card:
        return None if len(self.stacks[pile_no]) == 0 else self.stacks[pile_no][-1]

    def get_top_cards(self) -> List[str]:
        return_list : List[str]= []
        for stack in self.stacks:
            top_card = self.get_top_card(stack)
            if top_card is not None:
                return_list.append(top_card)
            else:
                return_list.append("x")
        return return_list
NEWCARD = USEREVENT + 1
Card.debug = True

def print_round_info():
    top_cards = game.get_top_cards()
    print(f"\tPile1:\tPile2:\n\t  {top_cards[0]}\t  {top_cards[1]}")
    print(f"Player1:\n{game.player1.deck.str_table()}")
    print(f"Player2:\n{game.player2.deck.str_table()}")

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    game = Game()

    clock = pygame.time.Clock()
    running = True
    counter = 0
    ROUND_START = True
    while running:
        if ROUND_START:
            game.init_round()
            ROUND_START = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    counter = (counter +1) % 52
                    print(counter)
                    entity = game.cards[counter]
            elif event.type == QUIT:
                running = False
        screen.fill((255, 255, 255))
        for entity in game.player1.deck.sprite_group:
            entity.rect.center = entity.coord
            screen.blit(entity.surf,  entity.rect)
        pygame.display.flip()

        clock.tick(60)


seed(12)
game = Game()

user_input = ""
ROUND_START = True
while user_input.lower() != "exit":
    if ROUND_START:
        game.init_round()
        ROUND_START = False
    print_round_info()
    user_input = input("Move[xPFT\\xMFT\\FLIP\\xSPITT\\STACKT\\HELP]:")
    player = None
    from_pile = 0
    to_pile = 0
    if len(user_input) not in [4,6]:
        print("Move command not formatted correctly.")
        continue
    if user_input == 'HELP':
        print("""HELP:
                x = Player number (1,2)
                M = Move card from one pile to another 
                P = Place card from one pile to game stack
                F = Pile to take from (1-5)
                T = Pile / Stack to move/place/spit to (1-5(move)1-2(place/spit))
                FLIP = Flip over card if no legal move can be made
                SPIT =  Spit card
                STACK = Print a game stack""")
        continue
    elif user_input[:-1] == 'STACK':
        if user_input[-1].isdigit():
            stack_to_check = int(user_input[-1]) - 1
            print(game.stacks[stack_to_check], sep="\n")
        else:
            print("Stack to print must be a number")
        continue
    elif user_input == 'FLIP':
        player1_can_go = False
        player2_can_go = False

        for pile in game.player1.deck.piles:
            if game.can_place_card(game.player1, pile, 0):
                player1_can_go = True
                print(f"Player 1 can place {game.player1.deck.piles[pile][-1]} on stack 1 (1P{pile}1)")
            if game.can_place_card(game.player1, pile, 1):
                player1_can_go = True
                print(f"Player 1 can place {game.player1.deck.piles[pile][-1]} on stack 2 (1P{pile}2)")
        for pile in game.player2.deck.piles:
            if game.can_place_card(game.player2, pile, 0):
                player2_can_go = True
                print(f"Player 2 can place {game.player2.deck.piles[pile][-1]} on stack 1 (2P{pile}1)")
            if game.can_place_card(game.player2, pile, 1):
                print(f"Player 2 can place {game.player2.deck.piles[pile][-1]} on stack 2 (2P{pile}2)")
                player2_can_go = True
        if player1_can_go:
            print("Cannot flip card as player 1 can go.")
        if player2_can_go:
            print("Cannot flip card as player 2 can go.")
        if not player1_can_go and not player2_can_go:
            print("Neither player can move, flipping cards.")
            game.flip_cards()
        continue
    if user_input[0].isdigit():
        player = game.player1 if int(user_input[0]) == 1 else game.player2
    else:
        print("Player number not formatted correctly.")
        continue
    if user_input[1:-1] == 'SPIT':
        if user_input[5].isdigit():
            to_pile = int(user_input[5])
        else: continue
        player1_has_cards = False
        player2_has_cards = False
        for pile in game.player1.deck.piles:
            if len(game.player1.deck.piles[pile]) != 0:
                player1_has_cards = True
                print("Player 1 still has cards.")
        for pile in game.player2.deck.piles:
            if len(game.player2.deck.piles[pile]) != 0:
                player2_has_cards = True
                print("Player 2 still has cards.")
        if not player1_has_cards or not player2_has_cards:
            to_pile -= 1
            print(f"Player {user_input[0]} selected pile {to_pile}. Cards from pile {to_pile} added to player {user_input[0]}, cards from other pile added to other player")
            # TODO DO THE LOGIC TO DISTRIBUTE PILES AND REMAINING CARDS - INDICATE ROUND END EVENT
            selected_pile = game.stacks[to_pile]
            remaining_pile = game.stacks[(to_pile +1)% 2]
            loser_player = game.player1 if player is game.player2 else game.player2
            player.collect_cards(selected_pile)
            loser_player.collect_cards(remaining_pile)
            print(f"Player 1 has {len(game.player1.cards)} cards and Player 2 has {len(game.player2.cards)} cards")
            ROUND_START = True
        continue
    if user_input[2].isdigit() and user_input[3].isdigit():
        from_pile = int(user_input[2])
        to_pile = int(user_input[3])
    else:
        print("Piles and stacks must be identified via number.")
    if user_input[1] == 'P':
        to_pile -= 1
        if len(player.deck.piles[from_pile]) != 0:
            card1 = str(player.deck.piles[from_pile][-1])
        else:
            card1 = "no card"
        if len(player.deck.piles[from_pile]) != 0:
            card2 = str(game.stacks[to_pile][-1])
        else:
            card2 = "no card"
        if game.place_card(player,from_pile,to_pile):
            print(f"Moved player {user_input[0]}'s top card from pile {from_pile} {card1} to game stack {to_pile} {card2}")
        else:
            print(f"Could not move player {user_input[0]}'s top card from pile {from_pile} {card1} to {to_pile} {card2}")

    elif user_input[1] == 'M':
        if len(player.deck.piles[from_pile]) != 0:
            card1 = str(player.deck.piles[from_pile][-1])
        else:
            card1 = "no card"
        if len(player.deck.piles[to_pile]) != 0:
            card2 = str(player.deck.piles[to_pile][-1])
        else:
            card2 = "no card"
        if player.deck.move(from_pile,to_pile):
            print(f"Moved player {user_input[0]}'s top card from pile {from_pile} {card1} to own pile {to_pile} {card2}")
        else:
            print(f"Could not move player {user_input[0]}'s top card from pile {from_pile} {card1} to own pile {to_pile} {card2}")

