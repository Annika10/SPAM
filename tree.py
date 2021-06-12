from ete3 import Tree


def create_tree_visualisation(nodes):
    dict_levels = dict()
    nodes = list(nodes)
    for element in nodes:
        print("element", element)
        tmp_element = element.replace('[', '')
        tmp_element = tmp_element.replace(']', '')
        tmp_element = tmp_element.replace(',', '')
        print("tmp_element", tmp_element)
        length_of_element = len(tmp_element)
        print("length_of_element", length_of_element)
        if length_of_element in dict_levels:
            print("go here")
            print("before", dict_levels)
            old_list = dict_levels[length_of_element]
            print("old_list", old_list)
            old_list.append(element)
            print("old", old_list)
            dict_levels[length_of_element] = old_list
            print("after", dict_levels)
        else:
            print("or here")
            print("before1", dict_levels)
            dict_levels[length_of_element] = [element]
            print("after1", dict_levels)
    print(dict_levels)

    # build string
    list_nodes = dict_levels[1]
    whole_tree_string = ''
    for node in list_nodes:
        list_node_tree = list()
        list_node_tree = get_child_nodes(node, dict_levels, list_node_tree)
        print("string_tree + node", node, list_node_tree)

        current_lengths = float('inf')
        for list_node_occurence in list_node_tree:
            child_node = list_node_occurence[0]
            lenght_child_node = list_node_occurence[1]

            print("child_node here", child_node)
            print("lenght_child_node", lenght_child_node)
            print("current_lengths", current_lengths)
            print("whole_tree_string", whole_tree_string)

            if lenght_child_node != current_lengths:
                whole_tree_string = whole_tree_string + ')' + '(' + child_node
                current_lengths = lenght_child_node
            elif lenght_child_node == current_lengths:
                whole_tree_string = whole_tree_string + ',' + child_node

            print("whole_tree_string", whole_tree_string)


        print("whole_tree_string", whole_tree_string)

    # TODO: check format
    t = Tree("([a][b],[a,c]);", format=1)
    #t = Tree("((((H,K)D,(F,I)G)B,E)A,((L,(N,Q)O)J,(P,S)M)C);", format=1)
    #t.show()


def get_child_nodes(node, dict_levels, list_node_tree):
    search_term = node[:-1]
    print("search_term", search_term)
    for key, value in dict_levels.items():
        for child_node in value:
            print("search_term + child_node", search_term, child_node)
            # TODO: get all first items of list items for check child_node
            if child_node.startswith(search_term) and child_node != node and child_node not in list_node_tree:
                print("child_node", child_node)
                get_child_nodes(child_node, dict_levels, list_node_tree)
                tmp_child_node = child_node.replace('[', '')
                tmp_child_node = tmp_child_node.replace(']', '')
                tmp_child_node = tmp_child_node.replace(',', '')
                lenght_child_node = len(tmp_child_node)
                list_node_tree.append([child_node, lenght_child_node])

    return list_node_tree
