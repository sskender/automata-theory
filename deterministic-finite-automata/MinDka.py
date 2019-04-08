

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
            transitions[tuple(function[0].split(","))] = function[1]
        except:
            break
    return transitions









class DFA(object):


    def __init__(self, all_states, symbols, acceptable_states, starting_state, transitions):
        """
        """
        self.ALL_STATES = all_states
        self.SYMBOLS = symbols
        self.ACCEPTABLE_STATES = acceptable_states
        self.STARTING_STATE = starting_state
        self.TRANSITIONS = transitions

        self.REACHABLE_STATES = self.getReachableStates()


    def getTransitions(self, state, symbol):
        """
        Get next state from transitions table. If state does not exist in transitions table, None is returned.

        :param state: automata state
        :param symbol: alphabet symbol
        :return: state or None
        """
        return self.TRANSITIONS.get((state, symbol))


    def getReachableStates(self):
        """
        Extract only reachable states from set of states.

        :return: set of states
        """
        reachable_states = set([self.STARTING_STATE])

        for symbol in self.SYMBOLS:
            possible_state = self.getTransitions(self.STARTING_STATE, symbol)
            if possible_state != None:
                reachable_states.add(possible_state)

        size = 0
        while len(reachable_states) > size:
            size = len(reachable_states)
            new_states = set()
            for state in reachable_states:
                for symbol in self.SYMBOLS:
                    possible_state = self.getTransitions(state, symbol)
                    if possible_state != None:
                        new_states.add(possible_state)
            reachable_states.update(new_states)

        return reachable_states


    def removeUnreachableStates(self):
        """
        Removes unreachable states and all links to them in transitions table.
        """
        self.ALL_STATES = set(state for state in self.ALL_STATES if state in self.REACHABLE_STATES)
        self.ACCEPTABLE_STATES = set(state for state in self.ACCEPTABLE_STATES if state in self.REACHABLE_STATES)
        self.TRANSITIONS = {k:v for k, v in self.TRANSITIONS.items() if k[0] in self.REACHABLE_STATES}


    def createMatrix(self):
        """
        """
        matrix = dict()
        all_states = sorted(self.ALL_STATES)

        for i in range(len(all_states) - 1):
            for j in range(i + 1, len(all_states)):
                # This is already cleaned transitions table
                matrix[(all_states[i], all_states[j])] = ((all_states[i] in self.ACCEPTABLE_STATES) ^ (all_states[j] in self.ACCEPTABLE_STATES))

        return matrix


    def sortTuple(self, a, b):
        """
        """
        return (a, b) if a < b else (b, a)


    def getValueFromDict(self, dictionary, key):
        """
        Resolve KeyError issue. Returns None if key is not in dict.

        :param dictionary: dictionary
        :param key: key
        :return: found value or None
        """
        return dictionary.get(key)


    def nemamPojmaKajOvoRadi(self, matrix):
        """
        jebeno radi
        """
        # koji je ovo k
        list_of_states = dict()


        all_states = sorted(self.ALL_STATES)

        for i in range(len(all_states) - 1):
            for j in range(i + 1, len(all_states)):

                for symbol in self.SYMBOLS:
                    transition1 = self.getTransitions(all_states[i], symbol)
                    transition2 = self.getTransitions(all_states[j], symbol)

                    if (transition1 != None) and (transition2 != None):
                        matrixBoolean = matrix.get(self.sortTuple(transition1, transition2))

                        if (matrixBoolean == True):
                            matrix[self.sortTuple(all_states[i], all_states[j])] = True
                        else:
                            list_of_states[self.sortTuple(transition1, transition2)] = self.sortTuple(all_states[i], all_states[j])


        return matrix, list_of_states



    def checkForX(self, matrix, list_of_states):
        flag = True
        count = 0

        while (flag and count != 0):
            for item in list_of_states.items():

                if matrix.get(item):
                    matrix[list_of_states.get(item)] = True
                    count += 1

            if count > len(list_of_states)*4:
                flag = False

        return matrix, list_of_states



    def findSameStates(self, matrix):
        """
        """
        newSetDict = list()
        all_states = sorted(self.ALL_STATES)

        for i in range(len(all_states) - 1):
            for j in range(i + 1, len(all_states)):
                matrixBool = matrix.get(self.sortTuple(all_states[i], all_states[j]))
                #print(matrixBool)
                if matrixBool == False:
                    newSetDict.append(self.sortTuple(all_states[i], all_states[j]))

        return newSetDict


    def doMinimize(self, same_states):
        for state in same_states:
            for symbol in self.SYMBOLS:

                try:
                    del self.TRANSITIONS[(state[1], symbol)]
                except:
                    None

                try:
                    self.ALL_STATES.remove(state[1])
                except:
                    None

                try:
                    self.ACCEPTABLE_STATES.remove(state[1])
                except:
                    None

                if state[1] == self.STARTING_STATE:
                    self.STARTING_STATE = state[0]


        for item in self.TRANSITIONS.keys():
            for state in same_states:

                if self.TRANSITIONS.get(item) == state[1]:
                    self.TRANSITIONS[item] = state[0]

        return





    def printDFA(self):
        """
        Print minimized DFA
        """
        print(",".join(sorted(self.ALL_STATES)))
        print(",".join(sorted(self.SYMBOLS)))
        print(",".join(sorted(self.ACCEPTABLE_STATES)))
        print(self.STARTING_STATE)
        for item in sorted(self.TRANSITIONS.items()):
            print("{},{}->{}".format(item[0][0], item[0][1], item[1]))










    # ovo i gornje se moze spojti s onim while jednim
    def checkMatrix(self, matrix):
        """
        """
        flag = True
        sorted_all_states = sorted(self.ALL_STATES)
        
        while flag:
            flag = False

            for i, item1 in enumerate(sorted_all_states):
                for item2 in sorted_all_states[i+1:]:

                    if matrix[self.sortTuple(item1, item2)]: continue

                    # Check distinguishable
                    for symbol in self.SYMBOLS:
                        transition1 = self.getTransitions(item1, symbol)
                        transition2 = self.getTransitions(item2, symbol)

                        if transition1 != None and transition2 != None: # and transition1 != transition2:
                            marked = matrix.get(self.sortTuple(transition1, transition2))
                            flag = flag or marked
                            matrix[self.sortTuple(item1, item2)] = marked

                            if marked:
                                break

        set_to_remove = set()
        for k, v in matrix.items():
            if not v:
                # Keep the first state in lexicographic order
                # Discard others, therefore add those to set to be removed
                set_to_remove.add(k[1])

        return set_to_remove






    def minimize(self):
        """
        """
        self.removeUnreachableStates()
        # bleh
        # bleh
        # no print here

        matrix = self.createMatrix()

        """
        for item in matrix.items():
            print(item)

        print(len(matrix))
        print("\n\n")
        """





        new_matrix, some_states = self.nemamPojmaKajOvoRadi(matrix)

        #print(len(matrix))
        new_matrix, some_states = self.checkForX(matrix, some_states)

        #print(len(matrix))


        """
        for item in new_matrix.items():
            print(item)
        print("\n\n")

        for item in some_states.items():
            print(item)
        print("\n\n")
        """



        same_states = self.findSameStates(new_matrix)
        #print(same_states)


        self.doMinimize(same_states)















# Definition
# Input format
ALL_STATES = set(input().split(","))                        # Q
SYMBOLS = set(input().split(","))                           # Alphabet symbols (sigma)
ACCEPTABLE_STATES = set(input().split(","))                 # F is a subset of Q
STARTING_STATE = input()                                    # Q0
TRANSITIONS = getInputTransitions()                         # Transition functions (delta)






myDFA = DFA(ALL_STATES, SYMBOLS, ACCEPTABLE_STATES, STARTING_STATE, TRANSITIONS)

myDFA.minimize()   

myDFA.printDFA()

"""
print("lol")
for item in myDFA.TRANSITIONS.items():

    print(item)
"""