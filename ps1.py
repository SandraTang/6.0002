################################################################################
# 6.0002 Fall 2019
# Problem Set 1
# Written By: yunb, mkebede
# Name: Sandra Tang
# Collaborators:
# Time: 12:30-47, 1:00-1:17, 2:30-3:10, 2 hours


# Problem 1
class State():
    """
    A class representing the election results for a given state. 
    Assumes there are no ties between dem and gop votes. The party with a 
    majority of votes receives all the Electoral College (EC) votes for 
    the given state.
    """

    def __init__(self, name, dem, gop, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        gop - number of Republican votes cast
        ec - number of EC votes a state has 

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.winner - str, the winner of the state, "dem" or "gop"
        self.margin - int, difference in votes cast between the two parties, a positive number
        self.ec - int, number of EC votes a state has
        """
        self.name = name
        if dem > gop:
            self.winner = "dem"
        else:
            self.winner = "gop"
        self.margin = abs(dem-gop)
        self.ec = ec

    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state  
        """
        return self.name

    def get_num_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has 
        """
        return self.ec

    def get_margin(self):
        """
        Returns: 
        int, difference in votes cast between the two parties, a positive number
        """
        return self.margin

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "gop"
        """
        return self.winner

    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """
        return "In " + self.get_name() + ", " + str(self.get_num_ecvotes()) + " EC votes were won by " + self.get_winner() + " by a " + str(self.get_margin()) + " vote margin."

    def __eq__(self, other):
        """
        Determines if two State instances are the same.
        They are the same if they have the same state name, winner, margin and ec votes.
        Be sure to check for instance type equality as well! 

        Note: 
        1. Allows you to check if State_1 == State_2
                2. Make sure to check for instance type (Hint: look up isinstance())

        Param:
        other - State object to compare against  

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        if not isinstance(other, State):
            return False
        #can do with less chars thru __str__()
        return self.get_name() == other.get_name() and self.get_num_ecvotes() == other.get_num_ecvotes() and self.get_margin() == other.get_margin() and self.get_winner() == other.get_winner()


# Problem 2
def load_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    states = []
    #open file and split by line
    with open(filename) as f:
        lines = f.read().splitlines()
    #split each line into a list of the data (so lines becomes a 2D array)
    for i in range(1, len(lines)):
        lines[i] = lines[i].split("\t")
        states.append(State(lines[i][0], int(lines[i][1]), int(lines[i][2]), int(lines[i][3])))
    return states

    
# Problem 3
def find_winner(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    dem_votes = 0
    gop_votes = 0
    #total up total number of votes for each category
    for state in election:
        if state.get_winner() == "dem":
            dem_votes += state.get_num_ecvotes()
        else:
            gop_votes += state.get_num_ecvotes()
    if dem_votes > gop_votes:
        return ("dem", "gop")
    else:
        return ("gop", "dem")


def get_winner_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances won by the winning candidate
    """
    #winner is at index 0 of result returned by find_winner
    winner = find_winner(election)[0]
    winner_states = []
    #if the state's winner matched the overall winner, append to list
    for state in election:
        if state.get_winner() == winner:
            winner_states.append(state)
    return winner_states
    


def ec_votes_reqd(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    winner_states = get_winner_states(election)
    winner_votes = 0
    #loop through list of winner states and add up all ec votes
    for states in winner_states:
        winner_votes += states.get_num_ecvotes()
    loser_votes = 538-winner_votes
    #538/2 = 269
    #need 270
    return 270 - loser_votes

def margin(x):
    return x.get_margin()

# Problem 4
def greedy_election(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. First chooses the states with the smallest 
    win margin, i.e. state that was won by the smallest difference in number of voters. 
    Continues to choose other states up until it meets or exceeds the ec_votes_needed. 
    Should only return states that were originally won by the winner in the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """

    #sort winner states based on margin, low to high
    ws_copy = sorted(winner_states, key = margin)
    relocation_states = []
    #add as many states as you can until ec_votes_needed is less than or equal to 0
    for i in range(len(ws_copy)):
        if ec_votes_needed > 0:
            relocation_states.append(ws_copy[i])
            ec_votes_needed -= ws_copy[i].get_num_ecvotes()
    return relocation_states


# Problem 5
def dp_move_max_voters(winner_states, ec_votes, memo=None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. 

    Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

        Hint: If using a top-down implementation, it may be helpful to create a helper function

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, number of EC votes (relocation should result in gain of AT MOST ec_votes)
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    The empty list, if every state has a # EC votes greater than ec_votes
    """

    #want to get largest num voters for least num ec

    if memo == None:
        memo = {}
    #if the combination of winner states and ec votes is already in memo, take it from memo instead of recomputing it
    if (len(winner_states), ec_votes) in memo:
        result = memo[(len(winner_states), ec_votes)]
    #base case
    #if there are no more states or "space" available for ec votes, result to base case
    elif winner_states == [] or ec_votes == 0:
        result = []
    #if the first winner state is too costly, don't take it
    elif winner_states[0].get_num_ecvotes() > ec_votes:
        #don't take the state and explore the possibility if you didn't take it
        result = dp_move_max_voters(winner_states[1:], ec_votes, memo)
    else:
        #the state can be "afforded"
        #you don't know if it's a good idea to take it so explore both options
        nextItem = winner_states[0]
        #explore possibility that you DO take the state
        withToTake = [nextItem] + dp_move_max_voters(winner_states[1:], ec_votes - nextItem.get_num_ecvotes(), memo)
        withVal = 0
        for i in withToTake:
            withVal += i.get_margin()
        #explore possibility that you DONT take the state
        withoutToTake = dp_move_max_voters(winner_states[1:], ec_votes, memo)
        withoutVal = 0
        for i in withoutToTake:
            withoutVal += i.get_margin()
        #figure out which possiblity is better
        if withVal > withoutVal:
            result = [nextItem] + dp_move_max_voters(winner_states[1:], ec_votes - nextItem.get_num_ecvotes(), memo)
        else:
            result = dp_move_max_voters(winner_states[1:], ec_votes, memo)
    #add to the memo so it can be used later
    memo[(len(winner_states), ec_votes)] = result
    return result

def move_min_voters(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of dp_move_max_voters

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    
    total_ec = 0
    #total up all ec votes
    for state in winner_states:
        total_ec += state.get_num_ecvotes()
    
    #find nonswing states
    nonswing = dp_move_max_voters(winner_states, total_ec - ec_votes_needed, memo=None)

    swing = []

    #get states that are swing states
    for i in range(len(winner_states)):
        if not winner_states[i] in nonswing:
            swing.append(winner_states[i])

    return swing


# Problem 6
def flip_election(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. 
    Moves voters from states that were won by the losing candidate (states not in winner_states), 
    to each of the states in swing_states.
    To win a swing state, you must move (margin + 1) new voters into that state. Any state that voters are
    moved from should still be won by the loser even after voters are moved.
    Reminder that you cannot move voters out of California, Washington, Texas, or Tennessee. 

    Also finds the number of EC votes gained by this rearrangement, as well as the minimum number of 
    voters that need to be moved.

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of move_min_voters or greedy_election)

    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple, (from_state, to_state), the 2 letter abbreviation of the State 
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
    None, if it is not possible to sway the election
    """
    
    #election = all states
    #find states the loser has won in
    #swing states = states the winner has won in that people need to move to

    #find out who the winner is
    winner = swing_states[0].get_winner()

    #make a list of the states the loser has won in
    loser_states = []
    forbidden_states = ["CA", "WA", "TX", "TN"]
    for state in election:
        if not state.get_name() in forbidden_states or not state.get_winner() == winner:
            loser_states.append(state)
    
    #dictionary (from_state, to_state): people being moved
    shuffling = {}

    #total num EC votes gained by moving voters
    gained_ec = 0

    #total number of voters being moved around
    moved_votes = 0

    #move people from state to state
    #move as many as needed from a state
    #from --> loser_states
    #to --> swing_states
    from_state = 0
    to_state = 0
    from_state_modify = 0
    to_state_modify = 0

    #loop ends when all swing states have been filled
    #loop also ends when all loser states have been gone thru
    while to_state < len(swing_states) and from_state < len(loser_states):
        #find number of votes the state won by the loser can afford to give away without losing or getting a tie
        loser_margin = loser_states[from_state].get_margin() - from_state_modify - 1
        #find number of votes the swing state needs to just barely win
        swing_margin = swing_states[to_state].get_margin() - to_state_modify + 1
        #case 0: from_state free votes = to_state needed votes
        if loser_margin == swing_margin:
            #transfer all from state votes to the to state
            shuffling[(loser_states[from_state].get_name(), swing_states[to_state].get_name())] = swing_margin
            gained_ec += swing_states[to_state].get_num_ecvotes()
            moved_votes += swing_margin
            #move onto next from and to state and reset an adjustments make for already given/recieved votes
            from_state += 1
            from_state_modify = 0
            to_state += 1
            to_state_modify = 0
        #case 1: from_state free votes < to_state needed votes --> give away all votes and move onto next from_state
        elif loser_margin < swing_margin:
            shuffling[(loser_states[from_state].get_name(), swing_states[to_state].get_name())] = loser_margin
            #no ec votes gained here because the to_state has not been flipped yet
            moved_votes += loser_margin
            from_state += 1
            from_state_modify = 0
            to_state_modify += loser_margin
        #case 2: from_state free votes > to_state needed votes --> give only as much votes as needed and move onto next to_state
        elif loser_margin > swing_margin:
            shuffling[(loser_states[from_state].get_name(), swing_states[to_state].get_name())] = swing_margin
            gained_ec += swing_states[to_state].get_num_ecvotes()
            moved_votes += swing_margin
            from_state_modify += swing_margin
            to_state += 1
            to_state_modify = 0
    #if gone through all the to states, that means they've all gotten enough voters to flip
    if to_state == len(swing_states):
        return (shuffling, gained_ec, moved_votes)
    #if you didn't fulfill the previous if statement AND gone through all the from states, there aren't enough voters to flip the election
    if from_state == len(loser_states):
        return None
    


if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

    # # tests Problem 1 
    # ma = State("MA", 100000, 20000, 8)
    # print(isinstance(ma, State))
    # print(ma)

    # # tests Problem 2 
    # year = 2012
    # election = load_election("%s_results.txt" % year)
    # print(len(election))
    # print(election[0])

    # # tests Problem 3
    # winner, loser = find_winner(election)
    # won_states = get_winner_states(election)
    # names_won_states = [state.get_name() for state in won_states]
    # ec_votes_needed = ec_votes_reqd(election)
    # print("Winner:", winner, "\nLoser:", loser)
    # print("States won by the winner: ", names_won_states)
    # print("EC votes needed:",ec_votes_needed, "\n")

    # # tests Problem 4
    # print("greedy_election")
    # greedy_swing = greedy_election(won_states, ec_votes_needed)
    # names_greedy_swing = [state.get_name() for state in greedy_swing]
    # voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
    # ecvotes_greedy = sum([state.get_num_ecvotes() for state in greedy_swing])
    # print("Greedy swing states results:", names_greedy_swing)
    # print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.\n")

    # # tests Problem 5: dp_move_max_voters
    # print("dp_move_max_voters")
    # total_lost = sum(state.get_num_ecvotes() for state in won_states)
    # move_max = dp_move_max_voters(won_states, total_lost-ec_votes_needed)
    # max_states_names = [state.get_name() for state in move_max]
    # max_voters_displaced = sum([state.get_margin()+1 for state in move_max])
    # max_ec_votes = sum([state.get_num_ecvotes() for state in move_max])
    # print("States with the largest margins:", max_states_names)
    # print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # # tests Problem 5: move_min_voters
    # print("move_min_voters")
    # swing_states = move_min_voters(won_states, ec_votes_needed)
    # swing_state_names = [state.get_name() for state in swing_states]
    # min_voters = sum([state.get_margin()+1 for state in swing_states])
    # swing_ec_votes = sum([state.get_num_ecvotes() for state in swing_states])
    # print("Complementary knapsack swing states results:", swing_state_names)
    # print("Min voters displaced:", min_voters, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # # tests Problem 6: flip_election
    # print("flip_election")
    # flipped_election = flip_election(election, swing_states)
    # print("Flip election mapping:", flipped_election)
