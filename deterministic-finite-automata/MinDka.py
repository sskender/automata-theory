global ALL_STATES, SYMBOLS, ACCEPTABLE_STATES, NOT_ACCEPTABLE_STATES, STARTING_STATE, TRANSITIONS


def getInputTransitions():
    """
    Get all transitions functions from input
    :return: Dictionary of transitions functions
    """
    transitions = dict()
    while True:
        try:
            function = input()
            if function == "\n" or function == "": break
            function = function.split("->")
            transitions[tuple(function[0].split(","))] = set(function[1].split(","))
        except:
            break
    return transitions


def getNotAcceptableStates():
    """
    Get all not acceptable states
    :return: set of not acceptable states
    """
    not_acceptable_states = set()
    for state in ALL_STATES:
        if state not in ACCEPTABLE_STATES:
            not_acceptable_states.add(state)
    return sorted(not_acceptable_states)


def getTransitions(state, symbol):
    """
    Get set of next states from transitions table
    If state does not exist in transitions table, empty set is returned
    :param state: automata state
    :param symbol: alphabet symbol
    :return: set of states
    """
    states = set()
    if TRANSITIONS.get((state, symbol)) != None:
        states.update(TRANSITIONS.get((state, symbol)))
    else:
        states.add("#")
    return states


def getReachableStates():
    """
    Extract only reachable states from set of states
    :return: set of states
    """
    reachable_states = set([STARTING_STATE])

    for symbol in SYMBOLS:
        reachable_states.update(getTransitions(STARTING_STATE, symbol))

    size = 0
    while len(reachable_states) > size:
        size = len(reachable_states)
        new_states = set()
        for state in reachable_states:
            for symbol in SYMBOLS:
                new_states.update(getTransitions(state, symbol))
        reachable_states.update(new_states)

    return sorted(reachable_states)


# Definition
# Input format
ALL_STATES = sorted(set(input().split(",")))                # Q
SYMBOLS = sorted(set(input().split(",")))                   # Alphabet symbols (sigma)
ACCEPTABLE_STATES = sorted(set(input().split(",")))         # F is a subset of Q
STARTING_STATE = input()                                    # Q0
TRANSITIONS = getInputTransitions()                         # Transition functions (delta)
NOT_ACCEPTABLE_STATES = getNotAcceptableStates()
REACHABLE_STATES = getReachableStates()

