



SIZE_OF_ALPHABET = 63

def get_alphanumeric_order(letter):
    """
    Convert a given alpahnumeric character in to ascii format
    :param letter: alphanumeric letter
    :return: ascii value for the input character
    """

    # Convert to ascii
    ascii = ord(letter)

    # Convert the dollar sign to ascii
    if ascii == 36:
        return 62
    # Convert numeric part to ascii
    elif ascii >= 48 and ascii <= 57:
        return ascii - 48
    # Convert upper case characters to respective index value
    elif ascii >= 65 and ascii <= 90:
        return ascii - 55
    # Convert lower case characters to respective index value
    elif ascii >= 97 and ascii <= 122:
        return ascii - 61
    # Return error of non alpha numeric letter is provided
    else:
        raise Exception("Unsupported Character")

def get_string(order):
    """
    Convert a given alpahnumeric character in to ascii format
    :param letter: alphanumeric letter
    :return: ascii value for the input character
    """

    # Convert the dollar sign to ascii
    if order == 62:
        return chr(36)
    # Convert numeric part to ascii
    elif order >= 0 and order <= 9:
        return chr(order + 48)
    # Convert upper case characters to respective index value
    elif order >= 10 and order <= 35:
        return chr(order + 55)
    # Convert lower case characters to respective index value
    elif order >= 36 and order <= 61:
        return chr(order + 61)
    # Return error of non alpha numeric letter is provided
    else:
        raise Exception("Unsupported Order")


class Node:
    '''
    Node class for each suffix node in the suffix tree
    '''
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.children = [None] * SIZE_OF_ALPHABET

        self.suffix_id = None
        self.suffix_link = None

    def __str__(self):


        edges = " ["
        for i in range(len(self.children)):
            if self.children[i] != None:
                edges += get_string(i) + "::" + str(self.children[i]) + " "
        edges += "] "

        return str(self.start) + " -> " + str(self.end) + "" + str(edges)


class GlobalI():
    '''
    Wrapper class to generate the global i for the global i implementation trick
    '''
    def __init__(self,value):
        '''
        Initialize the global variable using the value passed in as the initial value
        :param value: initial value to be stored in the global variable
        '''
        self.i = value

    def __str__(self):
        '''
        Return the i value as a string
        :return: string with value
        '''
        return str(self.i)

class ActivePointers():
    '''
    Class to maintain the active pointers to aid in ukkonen implementation
    '''
    def __init__(self, node, edge, length):
        self.active_node = node
        self.active_edge = edge
        self.active_length = length

def ukkonen(text):

    global_i = GlobalI(-1)

    j = 0

    root = Node(0, global_i)

    active_pointers = ActivePointers(root, -1, 0)

    while global_i.i < len(text) - 1:

        # Reseting the last created node
        last_created_node = None

        # Incrementing the global i which will in turn apply rule 1
        global_i.i += 1

        # Loop until all extensions are done
        while j <= global_i.i:

            # Check if the active length is 0
            if active_pointers.active_length == 0:

                # Get the child from the active node
                child = active_pointers.active_node.children[get_alphanumeric_order(text[global_i.i])]

                if child != None:

                    print(str(global_i.i) + " " + str(j) + " Rule 3")

                    active_pointers.active_edge = child.start

                    active_pointers.active_length+=1

                    break

                else:

                    print("NOCHILD " + text[global_i.i])
                    print(str(global_i.i) + " " + str(j) + " Rule 2b")

                    # Create the new node
                    active_pointers.active_node.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)

                    # Increase j by 1
                    j += 1

            else:

                next_char  = skip_count(global_i.i, text, active_pointers)



                print("TRAVERSE " + str(next_char))
                if next_char == -1 :

                    print("NOCHILD " + text[global_i.i])

                    print(str(global_i.i) + " " + str(j) + " Rule 2b")

                    node = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    node.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)

                    if last_created_node != None:

                        last_created_node.suffix_link = node

                    last_created_node = node

                    if active_pointers.active_node != root:
                        active_pointers.active_node = active_pointers.active_node.suffix_link

                    else:
                        active_pointers.active_edge = active_pointers.active_edge + 1
                        active_pointers.active_length -= 1

                    j += 1

                    continue


                if next_char == text[global_i.i]:
                    print("MATCH " + next_char + " == " + text[global_i.i])
                    print(str(global_i.i) + " " + str(j) + " Rule 3")

                    if last_created_node != None:
                        last_created_node.suffix_link = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]


                    node = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    difference = node.end.i - node.start

                    if difference < active_pointers.active_length:

                        active_pointers.active_node = node
                        active_pointers.active_length = active_pointers.active_length - difference
                        active_pointers.active_edge = node.children[get_alphanumeric_order(text[global_i.i])].start

                    else:

                        active_pointers.active_length += 1

                    # Show stopper
                    break

                else:

                    print("MISMATCH " + next_char + " == " + text[global_i.i])

                    print(str(global_i.i) + " " + str(j) + " Rule 2a")

                    node = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    old_start = node.start

                    node.start = node.start + active_pointers.active_length

                    # Create new middle node
                    new_middle_node = Node(old_start, GlobalI(old_start + active_pointers.active_length - 1))

#                   # Create new leaf node
                    new_leaf_node = Node(global_i.i, global_i)

                    new_middle_node.children[get_alphanumeric_order(text[new_middle_node.start + active_pointers.active_length])] = node

                    new_middle_node.children[get_alphanumeric_order(text[global_i.i])] = new_leaf_node

                    # new_middle_node =

                    active_pointers.active_node.children[get_alphanumeric_order(text[new_middle_node.start])] = new_middle_node

                    # Set the new node for suffix link
                    last_created_node = new_middle_node

                    # Default the suffix link to root
                    new_middle_node.suffix_link = root


                    if active_pointers.active_node != root:
                        active_pointers.active_node = active_pointers.active_node.suffix_link

                    else:
                        active_pointers.active_edge = active_pointers.active_edge + 1
                        active_pointers.active_length -= 1

                    j += 1

    return root

def skip_count(i, text, active):

    node = active.active_node.children[get_alphanumeric_order(text[active.active_edge])]

    difference = node.end.i - node.start

    if difference >= active.active_length:
        return text[active.active_node.children[get_alphanumeric_order(text[active.active_edge])].start + active.active_length]

    if difference + 1 == active.active_length:

        if node.children[get_alphanumeric_order(text[i])] != None:

            return text[i]


    else:
        active.active_node = node
        active.active_length = active.active_length - difference - 1
        active.active_edge = active.active_edge + difference + 1

        return skip_count(i,text, active)

    return -1


def lcps(root, index1, index2, text):

    deepest_node_with_branch = None

    count = 0

    if text[index1] != text[index2]:
        return 0

    current_node = root.children[get_alphanumeric_order(text[index1])]

    difference = current_node.end.i - current_node.start + 1

    count += difference



    while index1 + count < len(text) and index2 + count < len(text) and text[index1 + count] == text[index2 + count]:


        current_node = current_node.children[get_alphanumeric_order(text[index1 + count])]

        difference = current_node.end.i - current_node.start + 1

        count += difference


    return count






if __name__ == "__main__":
    # print(ukkonens_algorithm("aaaaab"))

    tree = ukkonen("mississippi$")
    print()
    print(tree)

    print(lcps(tree, 7, 10, "mississippi"))

    print(lcps(tree, 1, 4, "mississippi"))

    print(lcps(tree, 0, 4, "mississippi"))

    print(lcps(tree, 5, 2, "mississippi"))


    # *adeacdade
    # *abcabxabcd
    # *abcdefabxybcdmnabcdex
    # *abcadak
    # *dedododeodo
    # *abcabxabcd
    # *mississippi
    # *banana
    # *ooooooooo