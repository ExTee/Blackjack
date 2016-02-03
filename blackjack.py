# Read README if you want to run it on your Desktop!

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome2 = ""
score = 0
handOver = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        
    def __str__(self):
        # return a string representation of a hand
        ans = "Hand contains "
        for i in range(len(self.hand)):
            ans += str(self.hand[i])
            ans += " "
        return ans
        
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        acePresent = False
        hand_value = 0
        
        for card in self.hand:
            hand_value += VALUES[card.rank]
            if card.rank == 'A':
                acePresent = True
                
        if not acePresent:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else: 
                return hand_value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.hand:
            card.draw(canvas, [pos[0] + i*CARD_SIZE[0], pos[1]])
            i += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        dealt_card = self.deck.pop()
        return dealt_card
    
    def __str__(self):
        # return a string representing the deck
        ans = "Deck contains "
        for i in range(len(self.deck)):
            ans += str(self.deck[i])
            ans += " "
        return ans

        
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, playerHand, dealerHand, outcome2, handOver, score
    outcome2 = ""
    if not handOver:
        score -= 1
        outcome2 = "You forfeit the previous hand!"
    deck = Deck()
    deck.shuffle()
    playerHand = Hand()
    dealerHand = Hand()
    i = 0
    while i < 2:
        playerHand.add_card(deck.deal_card())
        dealerHand.add_card(deck.deal_card())
        i += 1
    in_play = True
    outcome = "Hit or Stand?"
    handOver = False
    
def hit():
    global deck, playerHand, outcome, in_play, outcome2, score, handOver
    if playerHand.get_value() <= 21:
        if in_play and playerHand.get_value() <= 21:
            playerHand.add_card(deck.deal_card())
        if playerHand.get_value() > 21:
            outcome2 = "You have busted!"
            score -= 1
            outcome = "New Deal?"
            in_play = False
            handOver = True

    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global playerHand, dealerHand, deck, outcome, in_play, outcome2, score, handOver
    in_play = False
    if not handOver:
            
        if playerHand.get_value() > 21:
            outcome2 = "You have busted!"
            score -= 1
            handOver = True
        else:
            while dealerHand.get_value() < 17:
                dealerHand.add_card(deck.deal_card())
            
        if dealerHand.get_value() > 21:
            outcome2 = "Dealer busted! You win."
            score += 1
            handOver = True
        else:
            if playerHand.get_value() > dealerHand.get_value():
                outcome2 = "You win."
                score += 1
            else:
                outcome2 = "Dealer wins."
                score -= 1
            handOver = True
        outcome = "New Deal?"
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global playerHand, dealerHand
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK!", [185, 50], 40, "Black")
    canvas.draw_text(outcome, [200,260+CARD_SIZE[1]], 20, "Black")
    canvas.draw_text("Dealer:", [75,180], 20, "White")
    canvas.draw_text("Player:", [75, 260 + CARD_SIZE[1]], 20, "White")
    canvas.draw_text(outcome2, [200, 180], 20, "Black")
    canvas.draw_text("SCORE:", [400, 120], 30, "Yellow")
    canvas.draw_text(str(score), [520, 120], 30, "Yellow")
    dealerHand.draw(canvas, [75,200])
    playerHand.draw(canvas, [75, 280 + CARD_SIZE[1]])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [75+CARD_SIZE[0]/2,200+CARD_SIZE[1]/2], CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
