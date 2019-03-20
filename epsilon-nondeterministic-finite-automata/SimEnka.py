# Non-deterministic finite automata with epsilon transitions
# Epsilon is represented with symbol $
# Epsilon stands for empty symbols
# Empty set is represented by # symbol


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


def getInputData():
    """
    Split what must be split
    :return: properly formatted input data
    """
    data = input().split("|")
    for i in range(len(data)):
        data[i] = list(data[i].split(","))
    return data


# Definition
# Input format
INPUT_DATA = getInputData()                                     # Input data (mix of alphabet symbols)
ALL_STATES = set(input().split(","))                            # Q
SYMBOLS = sorted(set(set(input().split(",")) | set("$")))       # Alphabet symbols (sigma) UNION epsilon
ACCEPTABLE_STATES = set(input().split(","))                     # F is a subset of Q
STARTING_STATE = input()                                        # F0 (zero state)
TRANSITIONS = getInputTransitions()                             # Transition functions (delta)


def getTransitions(state, symbol):
    """
    Get set of next states from transitions table
    If state does not exist in transitions table, empty set is returned
    NOTE: empty set is not actually empty, rather presented with # symbol
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


def cleanSet(states):
    """
    Add # to the set if it is empty
    Remove # from set if other elements are present in the set
    None values are handled in getTransitions function
    :param states: set of states
    :return: set of states
    """
    if len(states) > 1 and "#" in states:
        states.remove("#")
    elif len(states) == 0:
        states.add("#")
    return states


def nextStates(state, symbol):
    """
    Get set of next states from current state and symbol
    Including epsilon environment
    :param state: current state
    :param symbol: alphabet symbol
    :return: set of possible next states
    """
    # Grab next states from transitions table
    all_next_states = getTransitions(state, symbol)
    # No new epsilon states at the moment, therefore zero
    size = 0
    # New states will be found and set size will increase
    # If it does not happen, all states are already found
    while len(all_next_states) > size:
        # Update size to match total number of found states
        size = len(all_next_states)
        # Find epsilon environment for all states from transitions table
        next_states = set()
        for s in all_next_states:
            next_states.update(getTransitions(s, "$"))
        # Epsilon states also count into total number of possible next states
        all_next_states.update(next_states)
    return cleanSet(all_next_states)


def main():
    # Streams are divided by | sign in input
    for stream in INPUT_DATA:
        # Starting state is always the first state of the machine
        # Also check epsilon for starting state
        STATES = set([STARTING_STATE])
        STATES.update(nextStates(STARTING_STATE, "$"))
        STATES = cleanSet(STATES)
        print(",".join(sorted(STATES)), end="")

        for symbol in stream:
            # Each symbol in stream must be valid (symbol shall be in defined symbols)
            if symbol in SYMBOLS:
                # Set of all possible next states from current states and symbol
                NEXT_STATES = set()
                for state in STATES:
                    # Possible next states are calculated from
                    # state and symbol combination in transition table
                    NEXT_STATES.update(nextStates(state, symbol))

                # Clean and sort set of states for print
                STATES = cleanSet(NEXT_STATES)
                print("|" + ",".join(sorted(STATES)), end="")

        # Print new line for next stream in input data
        print()


if __name__ == "__main__":
    main()

