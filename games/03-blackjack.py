import random

# Global variables
playing = True
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three" : 3, "Four" : 4, "Five" : 5, "Six" : 6, "Seven" : 7, "Eight" : 8, "Nine" : 9, "Ten" : 10, "Jack" : 10, "Queen" : 10, "King" : 10, "Ace" : 11}

# Card Class
class Card():

    # Create a card
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # Print a card
    def __str__(self):
        return self.rank + " of " + self.suit

# Deck Class
class Deck():

    # Create the deck
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    # Print the deck
    def __str__(self):
        deck_cards = ""
        for card in self.deck:
            deck_cards += "\n" + card.__str__()

        return "The deck has: " + deck_cards
    
    # Other functions
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()

        return single_card

# Hand Class
class Hand():
    
    # Create a hand
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    # Other functions
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        # Also track aces to determine a value of 11 or 1
        if (card.rank == "Ace"):
            self.aces += 1

    def adjust_for_ace(self):
        while (self.value > 21 and self.aces > 0):
            self.value -= 10
            self.aces -= 1


# Chip Class
class Chips():

    # Create a chip
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    # Other functions
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# Static Functions
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input(f"How many chips would you like to bet? ({chips.total}): "))
        except ValueError:
            print("Please provide an integer!")
        else:
            if (chips.bet > chips.total):
                print(f"Not enough chips... (You have {chips.total})")
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("Hit or Stand? Enter 'h' or 's' : ")
        
        if (x[0].lower() == 'h'):
            hit(deck, hand)
        elif(x[0].lower() == 's'):
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        
        break

def show_some(player, dealer):
    print("\n")
    print("\tDEALERS HAND:")
    print("\tone card hidden!")
    print(f"\t{dealer.cards[1]} ({values[dealer.cards[1].rank]})")
    print("\n")
    print("\tPLAYERS HAND:")
    for card in player.cards:
        print(f"\t{card} ({values[card.rank]})")
    print("\n")

def show_all(player, dealer):
    print("\tDEALERS HAND:")
    for card in dealer.cards:
        print(f"\t{card} ({values[card.rank]})")
    print("\n")
    print("\tPLAYERS HAND:")
    for card in player.cards:
        print(f"\t{card} ({values[card.rank]})")
    print("\n")

def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("BUST DEALER!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie! PUSH")


#################### GAME #####################

chips = 100
print("Welcome to BlackJack!")
while True:
    
    # Create deck
    deck = Deck()
    deck.shuffle()

    # Create player and dealer hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Give chips to player
    player_chips = Chips(chips)

    # Ask player for his bet
    take_bet(player_chips)

    # Show dealer card
    show_some(player_hand, dealer_hand)

    # Let user play
    while playing:
        
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if (player_hand.value > 21):
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # Dealer's turn
    if (player_hand.value <= 21):

        # Dealer only hits until 17
        while (dealer_hand.value < 17):
            hit(deck, dealer_hand)
        
        # Show other cards
        show_all(player_hand, dealer_hand)

        # Evaluate
        if (dealer_hand.value > 21):
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif (dealer_hand.value > player_hand.value):
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif (dealer_hand.value < player_hand.value):
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    # Replay?
    if (player_chips.total == 0):
        print("GAME OVER!")
        break

    print(f"\nPlayer total chips are at {player_chips.total}")
    new_game = input("New Game? [Y/N]: ")

    if (new_game[0].lower() == 'y'):
        playing = True
        chips = player_chips.total
        continue
    else:
        print("\nThank you for playing")
        break
