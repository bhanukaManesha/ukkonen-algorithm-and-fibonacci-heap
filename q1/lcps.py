
# def ukkonens_algorithm(string):
#
#     I = GlobalI(0)
#     j = 0
#     root = Node(None, I)
#     root.links[ord(string[j]) - 96] = Node(j, I)
#
#     I.global_i += 1
#     j = I.global_i
#
#
#     while I.global_i <= len(string) - 2 :
#         current_node = root
#         while j <= I.global_i and I.global_i <= len(string) - 1:
#             if j - 1 >= root.end.global_i:
#                 I.global_i += 1
#                 break
#             else:
#                 if current_node.links[ord(string[j]) - 96] == None:
#                     current_node.links[ord(string[j]) - 96] = Node(j, I)
#
#                     if current_node != root:
#                         # Suffix Link
#                         current_node = root
#                     else:
#                         I.global_i += 1
#                         j = I.global_i
#                         break
#
#                 elif (I.global_i - j <= current_node.links[ord(string[j]) - 96].end.global_i - current_node.links[ord(string[j]) - 96].start):
#                     break_point = current_node.links[ord(string[j]) - 96].start + (I.global_i - j)
#                     if string[j] == string[break_point]:
#                         # Rule 3
#                         I.global_i += 1
#                         j = I.global_i
#                     else:
#                         old_start = current_node.links[ord(string[j]) - 96].start
#                         old_end = current_node.links[ord(string[j]) - 96].end
#
#                         new_intermediate_node = Node(old_start, GlobalI(break_point - 1))
#
#                         current_node.links[ord(string[j]) - 96].start = break_point
#
#                         new_intermediate_node.links[ord(string[j]) - 96] = current_node.links[ord(string[j]) - 96]
#
#
#                         new_leaf = Node(j + 1, old_end)
#
#
#                         new_intermediate_node.links[ord(string[current_node.links[ord(string[j]) - 96].end.global_i]) - 96] = new_leaf
#
#                         current_node.links[ord(string[j]) - 96] = new_intermediate_node
#
#                         j += 1
#                 else:
#                     current_node = current_node.links[ord(string[j]) - 96]
#                     j += 1
#
#     return root


# if global_i.i == active_node.end.i:
#     print("i: " + str(global_i.i) + " j:" + str(j) + " c:" + str(j) + "  Rule 1")
#     # Rule 1
#     # active_node.end += 1
#     j += 1
#     active_node = root
#
#     # j += 1


# def ukkonen(txt):
#     n = len(txt)
#
#     global_i = GlobalI(0)
#
#     root = Node(0, 0)
#
#     active_length = 0
#     active_node = root
#
#     j = 0
#     while global_i.i <= n - 1:
#         global_i.i += 1
#         # j = 0
#         while j < global_i.i and global_i.i <= n:
#
#             active_node = root
#
#             if active_node.links[get_alphanumeric_order(txt[j])] == None:
#                 print("i: " + str(global_i.i) + " j:" + str(j) + " c:" + str(j) + "  Rule 2")
#                 new_node = Node(j,global_i)
#                 active_node.links[get_alphanumeric_order(txt[j])] = new_node
#                 j += 1
#                 break
#
#
#
#             while j < len(txt) and active_node.links[get_alphanumeric_order(txt[j])] != None :
#
#                 if global_i.i <= active_node.links[get_alphanumeric_order(txt[j])].end.i:
#                     # Rule 3
#                     if txt[active_length] == txt[active_node.links[get_alphanumeric_order(txt[j])].end.i - 1]:
#                         print("i: " + str(global_i.i) + " j:" + str(j) + " c:" + str(j) + "  Rule 3" )
#                         global_i.i += 1
#                         active_length += 1
#                         break
#
#                     else:
#                         print("i: " + str(global_i.i) + " j:" + str(j) + " c:" + str(j) + "  Rule 2" )
#
#
#                         sep = active_node.links[get_alphanumeric_order(txt[j])].end.i - 1
#
#                         active_node.links[get_alphanumeric_order(txt[j])].start = sep
#
#
#                         new_middle_node = Node(sep - 1,sep)
#                         new_middle_node.links[get_alphanumeric_order(txt[j])] = active_node.links[get_alphanumeric_order(txt[j])]
#
#                         new_left_node = Node(global_i.i, global_i)
#
#                         new_middle_node.links[get_alphanumeric_order(txt[active_length])] = new_left_node
#
#                         active_node.links[get_alphanumeric_order(txt[j])] = new_middle_node
#
#
#                         # suffix link
#                         active_node = root
#                         j += 1
#                         break
#
#
#                 elif global_i.i > active_node.end.i :
#                     print("Next Node")
#                     j += 1
#                     active_node = active_node.links[get_alphanumeric_order(txt[j])]
#
#
#     # global_i.i -= 1
#     return root



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
    def __init__(self,value):
        self.i = value

    def __str__(self):
        return str(self.i)


def ukkonen(text):

    global_i = GlobalI(-1)

    j = 0

    root = Node(0, global_i)

    active_node = root
    active_length = 0
    active_edge = -1

    while global_i.i < len(text) - 1:

        # Reseting the last created node
        last_created_node = None

        # Incrementing the global i which will in turn apply rule 1
        global_i.i += 1

        # Loop until all extensions are done
        while j <= global_i.i:

            # Check if the active length is 0
            if active_length == 0:

                # Get the child from the active node
                child = active_node.children[get_alphanumeric_order(text[global_i.i])]

                if child != None:

                    print("Rule 3")

                    active_edge = child.start

                    active_length+=1

                    break

                else:

                    print("Rule 2")

                    # Create the new node
                    active_node.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)

                    # Increase j by 1
                    j += 1

            else:

                next_char = skip_count(global_i.i,
                                       text,
                                       active_length,
                                       active_node,
                                       active_edge
                                       )

                if next_char == -1 :

                    print("Rule 2")

                    node = active_node.children[get_alphanumeric_order(text[active_edge])]

                    node.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)

                    if last_created_node != None:
                        last_created_node.suffix_link = node

                    last_created_node = node

                    if active_node != root:
                        active_node = active_node.suffix_link

                    else:
                        active_edge = active_edge + 1
                        active_length -= 1

                    j += 1

                    break

                print("Comparing " + next_char + " == " + text[global_i.i])
                if next_char == text[global_i.i]:

                    print("Rule 3")

                    if last_created_node != None:
                        last_created_node.suffix_link = active_node.children[get_alphanumeric_order(text[active_edge])]


                    node = active_node.children[get_alphanumeric_order(text[active_edge])]

                    difference = node.end.i - node.start

                    if difference < active_length:

                        active_node = node
                        active_length = active_length - difference
                        active_edge = node.children[get_alphanumeric_order(text[global_i.i])].start

                    else:

                        active_length += 1

                    break

                else:

                    print("Rule 2")

                    node = active_node.children[get_alphanumeric_order(text[active_edge])]

                    old_start = node.start

                    node.start = node.start + active_length

                    # Create new middle node
                    new_middle_node = Node(old_start, GlobalI(old_start + active_length - 1))

#                   # Create new leaf node
                    new_leaf_node = Node(global_i.i, global_i)

                    new_middle_node.children[get_alphanumeric_order(text[new_middle_node.start + active_length])] = node

                    new_middle_node.children[get_alphanumeric_order(text[global_i.i])] = new_leaf_node

                    # new_middle_node =

                    active_node.children[get_alphanumeric_order(text[new_middle_node.start])] = new_middle_node

                    # Set the new node for suffix link
                    last_created_node = new_middle_node

                    # Default the suffix link to root
                    new_middle_node.suffix_link = root


                    if active_node != root:
                        active_node = active_node.suffix_link

                    else:
                        active_edge = active_edge + 1
                        active_length -= 1

                    j += 1

    return root

def skip_count(i, text, active_length, active_node, active_edge):

    node = active_node.children[get_alphanumeric_order(text[active_edge])]

    difference = node.end.i - node.start

    if difference >= active_length:
        return text[active_node.children[get_alphanumeric_order(text[active_edge])].start + active_length]

    if difference + 1 == active_length:

        if node.children[get_alphanumeric_order(text[i])] != None:

            return text[i]


    else:
        active_node = node
        active_length = active_length - difference - 1
        active_edge = active_edge + difference + 1

        return skip_count(i,
                          text,
                          active_length,
                          active_node,
                          active_edge
                          )


    return -1


# def test_ukkonen(root, text, index, current):
#
#     if root == None:
#         raise Exception()
#
#     node = root.children[get_alphanumeric_order(text[current])]
#
#     if node == None:
#         print("failed")
#
#     j = 0
#
#     for i in range(node.end.i):
#         if text[current + j] != text[i]:
#             print("Mistmatch")
#



if __name__ == "__main__":
    # print(ukkonens_algorithm("aaaaab"))

    tree = ukkonen("mississippi$")
    print()
    print(tree)

    # *adeacdade
    # *abcabxabcd
    # *abcdefabxybcdmnabcdex
    # *abcadak
    # *dedododeodo
    # *abcabxabcd
    # *mississippi
    # *banana
    # *ooooooooo