# Problem Set 4
# Name: Sandra Tang
# Collaborators: None
# Time Spent: 8 hours (estimated)
# Late Days Used: 0

import random
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from ps4_classes import BlackJackCard, CardDecks, Busted


#############
# PROBLEM 1 #
#############
class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """

    # Do not modify these three lines, they provide an interface for the tester!
    hit = 'hit'
    stand = 'stand'
    doubledown = 'doubledown'
    #########################

    def __init__(self, deck, initial_bet=1.0):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
               card deck (this deck itself contains one or more standard card decks)
        initial_bet - float, represents the initial bet/wager of the hand

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.current_bet - float, represents the current bet/wager of the hand
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck

        Important: You MUST deal out the first four cards in the following order:
            player, dealer, player, dealer
            
            You may find the deal_card function (and others) in ps4_classes.py helpful.
        """
        self.deck = deck
        self.current_bet = initial_bet
        self.player = []
        self.dealer = []

        #deal out player, dealer, player, dealer
        self.player.append(self.deck.deal_card())
        self.dealer.append(self.deck.deal_card())
        self.player.append(self.deck.deal_card())
        self.dealer.append(self.deck.deal_card())

    # Do not modify!
    def set_bet(self, new_bet):
        """
        Sets the player's current wager in the game.

        Parameters:
        new_bet - the floating point number representing the new wager for the game.

        Do not modify!
        """
        self.current_bet = new_bet

    # Do not modify!
    def get_bet(self):
        """
        Returns the player's current wager in the game.

        Returns:
        self.current_bet, the floating point number representing the current wager for the game

        Do not modify!
        """
        return self.current_bet
        
    # Do not modify this function!
    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        used for testing, DO NOT MODIFY
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    # You can call the method below like this:
    #   BlackJackHand.best_value(cards)
    @staticmethod
    def best_value(cards):
        """
        Finds the total value of the cards. All cards must contribute to the
        best sum; however, an Ace may contribute a value of 1 or 11.

        The best sum is the highest point total not exceeding 21 if possible.
        If it is not possible to keep the total value from exceeding 21, then
        the best sum is the lowest total value of the cards.

        Hint: If you have one Ace, give it a value of 11 by default. If the sum
        point total exceeds 21, then give it a value of 1. What should you do
        if cards has more than one Ace?

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        aces = 0
        total = 0
        for c in cards:
            if not c.get_val() == 11:
                total += c.get_val()
            else:
                aces += 1

        # CASE 0: no aces, return total
        if aces == 0:
            return total
        # CASE 1: one ace, return 11 or 1
        if aces == 1:
            if total + 11 <= 21:
                return total + 11
            else:
                return total + 1
        # CASE 2: two or more aces
        if aces > 1:
            if total + 11 + aces - 1 <= 21:
                return total + 11 + aces - 1
            else:
                return total + aces

    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.dealer[0]

    # Strategy 1
    def mimic_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        value = self.best_value(self.get_player_cards())
        if value >= 17:
            return "stand"
        else:
            return "hit"

    # Strategy 2
    def peek_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        p_value = self.best_value(self.get_player_cards())
        d_value = self.best_value(self.get_dealer_cards())
        if p_value < d_value:
            return "hit"
        else:
            return "stand"        

    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        value = self.best_value(self.get_player_cards())
        if value >= 17:
            return "stand"
        elif  self.get_dealer_upcard().get_val() >= 2 and self.get_dealer_upcard().get_val() <= 6 and value >= 12 and value <= 16:
            return "stand"
        else:
            return "hit"

    # Strategy 4
    def doubledown_strategy(self):
        """
        A playing strategy in which the player will
            - doubledown if the following is true:
                - the best value of the player's cards is 11
            - else they will fall back to using simple_strategy

        In our game, we allow "doubling down" on any turn, rather than just the first turn.

        The double down action indicates a special, somewhat risky, but possibly rewarding player
        action. It means the player wishes to double the current bet of the hand, hit one more time,
        and then immediately stand, ending their turn with whatever cards result. 

        This strategy simply consists of siginaling to that the calling function with the action
        BlackJackHand.doubledown when the sum of the players cards is 11, which is a very good 
        position in which to try to double one's bet while getting only one more card. Otherwise,
        the strategy falls back to using the simple_strategy to play normally.

        Returns:
        str, BlackJackHand.doubledown if player_best_score == 11,
             otherwise the return value of calling simple_strategy to play in the default way
        """
        if self.best_value(self.get_player_cards()) == 11:
            return "doubledown"
        else:
            return self.simple_strategy()

    def play_player_turn(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player (a hit). The player
        will be dealt a new card until they stand, bust, or doubledown. 

        When doubling down, the player doubles their bet, receive one final hit, and 
        then they stand. The hit when doubling down (like any hit) can cause the player to 
        go bust.

        The following will guide you through some design requirements for this function. 

        This function must _repeatedly_ query the strategy for the next action, until the action
        is to stand, or until their hand's best value is over 21, which should then raise a Busted
        exception (imported from ps4_classes.py) to signal this sad outcome to the caller.

        Remember, receiving the doubledown action from a strategy indicates: 
            - the player wishes to double their current bet,
            - the player receives one last hit,
            - the player then immediately stands, ending their turn

        Remember, 
            - Whenever hitting, always signal to the caller if the best value of the 
              player's hand becomes greater than 21 (because the player has busted).

        Parameter:
        strategy - function, one of the the 4 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy, BlackJackHand.double_down_strategy)

        Returns:          
        This function does not return anything.

        """
        #query the player
        decision = "hit"
        while decision == "hit":
            decision = strategy(self)
            if decision == "hit":
                self.player.append(self.deck.deal_card())
            if decision == "doubledown":
                self.player.append(self.deck.deal_card())
                self.current_bet *= 2
                decision = "stand"
            if self.best_value(self.get_player_cards()) > 21:
                decision = "stand"
                raise Busted

    def play_dealer_turn(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17. If they go over 21, they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the dealer's hand is greater than 21.
        """
        while self.best_value(self.get_dealer_cards()) < 17:
            self.dealer.append(self.deck.deal_card())
        if self.best_value(self.get_dealer_cards()) > 21:
            raise Busted

    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.

        Useful for debugging. DO NOT MODIFY. 
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

#############
# PROBLEM 2 #
#############


def play_hand(deck, strategy, initial_bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on the bet/wager of the hand.

    The player will get:

        - 2.5 times the bet of the hand if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.

        - 2 times the bet of the hand if the player wins by having a higher best value than 
          the dealer after the dealer's turn concludes

        - 2 times the bet of the hand if the dealer busts

        - the exact bet amount of the hand if the game ends in a tie. 
          If the player and dealer both get blackjack from their first two cards, 
          this is also a tie.

        - 0 if the dealer wins with a higher best value, or the player busts.

        Remember, the doubledown strategy doubles the current bet under certain conditions. 
        You do not have to worry about doubling the bet here for any doubledowns if 
        your doubledown strategy properly signals to alter the bet of the hand during the
        player's turn.

        Reminder of how the game flow works:

        1. Deal cards to player, then dealer, then player, then dealer.

        2. Check for initial blackjacks from either player. If at least one person has 
           blackjack, the game is over. Calculate how much the player receives.

        3. If no one has blackjack, then deal the player until they stand or bust 
           (use your play_player_turn function).

           If you catch a Busted exception from the player playing their turn,
           the player busted, and the game is over. Calculate how much the player receives.

        4. If the player has not bust, then deal the dealer until they stand or bust.
           (use your play_dealer_turn function).
           If the dealer busts, the game is over. Calculate how much the player receives.

        5. If no one has bust, determine the outcome of the game based on the
            best value of the player's cards and the dealer's cards.

    Parameters:
        deck - an instance of CardDeck
        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        initial_bet - float, the amount that the player initially bets (default=1.0)

    Returns:
        tuple (float, float): (amount_wagered, amount_won)
               amount_wagered, the current bet of the hand. Should use hand.get_bet().
               amount_won, the amount of money the player gets back. Should be 0 if they busted and lost.
    """
    # cards are dealt when initialized

    # check for blackjacks
    # (self.current_bet, self.current_bet) if both have blackjack
    # (self.current_bet, self.current_bet * 2.5) if player wins
    # (self.current_bet, 0) if dealer wins

    hand = BlackJackHand(deck, initial_bet)
    player_blackjack = hand.best_value(hand.get_player_cards()) == 21
    dealer_blackjack = hand.best_value(hand.get_dealer_cards()) == 21
    if player_blackjack and dealer_blackjack:
        return (hand.get_bet(), hand.get_bet())
    elif player_blackjack:
        return (hand.get_bet(), hand.get_bet()*2.5)
    elif dealer_blackjack:
        return (hand.get_bet(), 0)

    # play player's hand
    try:
        hand.play_player_turn(strategy)
    except Busted:
        # if player busts, return (self.current_bet, 0)
        return (hand.get_bet(), 0)
    # if player didn't bust, play dealer's hand
    try:
        hand.play_dealer_turn()
    except Busted:
        #if the dealer busts
        return (hand.get_bet(), hand.get_bet()*2)

    #outcomes
    player_value = hand.best_value(hand.get_player_cards())
    dealer_value = hand.best_value(hand.get_dealer_cards())

    # come in with the assumption that the player didn't bust

    # at this point, assume NEITHER have busted

    # if player has higher best value
    # (self.current_bet, self.current_bet * 2)

    if player_value > dealer_value:
        return (hand.get_bet(), hand.get_bet() * 2)

    # if dealer has higher best value
    if dealer_value > player_value:
        return (hand.get_bet(), 0)

    # if tie, (self.current_bet, self.current_bet)
    if dealer_value == player_value:
        return (hand.get_bet(), hand.get_bet())


#############
# PROBLEM 3 #
#############


def run_simulation(strategy, initial_bet=2.0, num_decks=8, num_hands=20, num_trials=4000, show_plot=False):
    """
    Runs a simulation and generates a normal distribution reflecting 
    the distribution of player's rates of return across all trials.

    The normal distribution is based on the mean and standard deviation of 
    the player's rates of return across all trials. 
    You should also plot the histogram of player's rates of return that 
    underlies the normal distribution. 
    For hints on how to do this, consider looking at 
        matplotlib.pyplot
        scipy.stats.norm.pdf

    For each trial:

        - instantiate a new CardDeck with the num_decks and type BlackJackCard
        - for each hand in the trial, call play_hand and keep track of how
          much money the player receives across all the hands in the trial
        - calculate the player's rate of return, which is
            100*(total money received-total money bet)/(total money bet)

    Parameters:

        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        initial_bet - float, the amount that the player initially bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials


    MORE PLOTTING HINTS:

    y_values = stats.norm.pdf(x_values, avg, std), This function returns the y-values of the normal distribution
    make sure x_values passed in are sorted. avg and std can be calculated using some numpy functions. 


    """

    returns = []
    for _ in range(num_trials):
        earnings_sum = 0
        bet_sum = 0
        deck = CardDecks(num_decks, BlackJackCard)
        #play_hand(deck, strategy, initial_bet=1.0)
        for _ in range(num_hands):
            result_tuple = play_hand(deck, strategy, initial_bet)
            earnings_sum += result_tuple[1]
            bet_sum += result_tuple[0]
        returns.append(100 * (earnings_sum - bet_sum) / bet_sum)

    # avg_returns = sum(returns) / num_trials

    #calculate standard deviation
    avg_returns = np.mean(returns)
    sdev = np.std(returns)
    # sigma = 0
    # mean = sum(returns) / len(returns)
    # for i in returns:
    #     sigma += (i - mean)**2
    # sdev = ((sigma)/len(returns))**0.5

    #plots
    #plot the distribution of rates of return using a normal distributions
    #x = np.arrange(0, 0);
    #y = stuff
    #plot.plot(x, y)
    if show_plot:
        x_values = range(-100, 110, 10)
        y_values = stats.norm.pdf(x_values, avg_returns, sdev)
        plt.title("Player ROI on playing " + str(num_hands) + " Hands (" + str(strategy.__name__) + ") \n (Mean = " + str(round(avg_returns, 2)) + "%, SD = " + str(round(sdev, 2)) + "%)")
        plt.xlabel("% Return")
        plt.legend()
        plt.hist(sorted(returns), bins=9, density=True)
        plt.plot(x_values, y_values)
        # plt.hist(y_values, bins=9)
        plt.show()

    return (returns, avg_returns, sdev)


def run_all_simulations(strategies):
    """
    Runs a simulation for each strategy in strategies and generates a single graph with normal 
    distribution plot for each strategy. No need to graph the underlying histogram. Each guassian 
    (another name for normal) distribution should reflect the distribution of rates of return 
    for each strategy.

    You might find scypi.stats (imported as stats) helpful.

    You might find matplotlib.pyplot (imported as plt) helpful.

    Make sure to label each plot with the name of the strategy and the x axis label.

    Parameters:

        strategies - list of strategies to simulate
    """

    for s in strategies:
        return_tuple = run_simulation(s) 
        x_values = sorted(return_tuple[0])
        y_values = []
        avg_returns = return_tuple[1]
        sdev = return_tuple[2]
        #how to add label?
        #ax.plot(x, np.sin(x), '-b', label='Sine')
        y_values = stats.norm.pdf(x_values, avg_returns, sdev)
        plt.plot(x_values, y_values, label=str(s.__name__))
    plt.title("Player ROI For Different Strategies")
    plt.xlabel("% Return")
    plt.legend()
    
    # plt.hist(y_values, bins=9)
    plt.show()


if __name__ == '__main__':
    #
    # You can uncomment pieces of the following to test each strategy separately.
    #
    # Default plots:
    #
#    run_simulation(BlackJackHand.mimic_dealer_strategy, show_plot=True)
#    run_simulation(BlackJackHand.peek_strategy, show_plot=True)
#    run_simulation(BlackJackHand.simple_strategy, show_plot=True)
#    run_simulation(BlackJackHand.doubledown_strategy, show_plot=True)
#
# Uncomment to run all simulations:
#
	run_all_simulations([BlackJackHand.mimic_dealer_strategy, BlackJackHand.peek_strategy, BlackJackHand.simple_strategy, BlackJackHand.doubledown_strategy])
#
# Copies of the student tester simulations are below to aid in debugging.
#
# Make sure you include the following line to use same random number generator as the tester!
#    random.seed(0)
#
#   Simulation used in test_29_run_simulation_mimic_dealer_strategy
#    run_simulation(BlackJackHand.mimic_dealer_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Simulation used in test_30_run_simulation_peek_strategy
#    run_simulation(BlackJackHand.peek_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Simulation used in test_31_run_simulation_simple_strategy
#    run_simulation(BlackJackHand.simple_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Simulation used in test_32_run_simulation_double_down_strategy
#    run_simulation(BlackJackHand.doubledown_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Use the following pass if you have no __main__ code enabled.
    # pass
