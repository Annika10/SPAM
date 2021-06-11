from ete3 import Tree


def create_tree_visualisation(nodes):
    level = 1
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
    string_tree = ''
    for node in list_nodes:
        list_node_tree = list()
        list_node_tree = get_child_nodes(node, dict_levels, list_node_tree, string_tree)
        print("string_tree + node", node, list_node_tree)
        print(string_tree)
        # string_tree = node
        # current_lenghts = 2
        # for child_node in list_node_tree:
        #     tmp_child_node = child_node.replace('[', '')
        #     tmp_child_node = tmp_child_node.replace(']', '')
        #     tmp_child_node = tmp_child_node.replace(',', '')

    #t = Tree("((((H,K)D,(F,I)G)B,E)A,((L,(N,Q)O)J,(P,S)M)C);", format=1)
    #t.show()


def get_child_nodes(node, dict_levels, list_node_tree, string_tree):
    search_term = node[:-1]
    print("search_term", search_term)
    for key, value in dict_levels.items():
        for child_node in value:
            print("search_term + child_node", search_term, child_node)
            print(child_node[:-2])
            print(child_node[:-3])
            if child_node.startswith(search_term) and child_node != node:
                print("child_node", child_node)
                get_child_nodes(child_node, dict_levels, list_node_tree, string_tree)
                list_node_tree.append(child_node)
                string_tree = string_tree + child_node

    return list_node_tree
