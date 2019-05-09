# Simulate adding from left to right onto the stack (only print reversed)
# Empty stack returns epsilon ($)


class Stack(list):

    def __init__(self):
        super().__init__(self)

    def __repr__(self):
        return "$" if self.is_empty() else "".join(self)[::-1]

    def push_left(self, item):
        for s in item[::-1]:
            if s != "$":
                self.append(s)
            else:
                return

    def pop_left(self):
        return self.pop()

    def is_empty(self):
        return len(self) == 0


"""Getting input from console."""


def get_input_data():
    data = input().split("|")
    for i in range(len(data)):
        data[i] = list(data[i].split(","))
    return data


def get_input_transitions():
    """
    Get all Delta functions for PDA.

    :return: dictionary of transitions, consists of tuples
    """
    transitions = dict()
    while True:
        try:
            function = input()
            if function == "\n" or function == "":
                break
            else:
                pass
            function = function.split("->")
            transitions[tuple(function[0].split(","))] = tuple(function[1].split(","))
        except Exception as e:
            break
    return transitions


"""Logging to console."""


def log_fail():
    # PDA not in acceptable state after fail
    print("fail|0")


def log_pair(state, stack):
    print("%s#%s|" % (state, stack), end="")


"""Automaton input and definition."""
INPUT_DATA = get_input_data()                   # Input data (mix of alphabet symbols)
ALL_STATES = input().split(",")                 # Q
SYMBOLS = input().split(",")                    # Alphabet symbols (sigma) UNION epsilon
STACK_ALPHABET = input().split(",")             # Finite stack alphabet
ACCEPTABLE_STATES = input().split(",")          # F is a subset of Q
START_STATE = input()                           # PDA in this state before making any transitions
START_SYMBOL = input()                          # Stack consists of one instance of this symbol
TRANSITIONS = get_input_transitions()           # Transition functions (delta)


for data in INPUT_DATA:
    stack = Stack()
    fail_detected = False

    # start from starting states
    Q = START_STATE
    Z = START_SYMBOL
    log_pair(Q, Z)

    for symbol in data:

        # epsilon
        while TRANSITIONS.get((Q, "$", Z)) is not None:
            (Q, Z) = TRANSITIONS.get((Q, "$", Z))
            stack.push_left(Z)
            log_pair(Q, stack)
            if not stack.is_empty():
                Z = stack.pop_left()
            else:
                fail_detected = True
                break

        # stack not empty, check if transition exists
        if not fail_detected and TRANSITIONS.get((Q, symbol, Z)) is not None:
            (Q, Z) = TRANSITIONS.get((Q, symbol, Z))
            stack.push_left(Z)
            log_pair(Q, stack)
            if not stack.is_empty():
                Z = stack.pop_left()
            else:
                fail_detected = True
        else:
            fail_detected = True

        # stack empty
        if fail_detected:
            log_fail()
            break
        else:
            pass

    # epsilon
    if not fail_detected:
        while TRANSITIONS.get((Q, "$", Z)) is not None and Q not in ACCEPTABLE_STATES:
            (Q, Z) = TRANSITIONS.get((Q, "$", Z))
            stack.push_left(Z)
            log_pair(Q, stack)
            if not stack.is_empty():
                Z = stack.pop_left()
            else:
                break
        print(1 if Q in ACCEPTABLE_STATES else 0, end="\n")
    else:
        pass
