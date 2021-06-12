import pydot


def create_tree_visualisation(nodes):
    dict_levels = get_dict_levels(nodes)
    dict_successors = get_dict_successors(dict_levels)

    graph = pydot.Dot('my_graph', graph_type='graph')

    root = pydot.Node('root')
    for first_nodes in dict_levels[1]:
        graph.add_edge(pydot.Edge(root, first_nodes))

    # Add nodes
    for node in nodes:
        graph.add_node(pydot.Node(node))
        # Add edges
        for successors in dict_successors[node]:
            graph.add_edge(pydot.Edge(node, successors))


    graph.write_raw('tree.dot')
    #graph.write_png('output.png')


def get_dict_levels(nodes):
    dict_levels = dict()
    nodes = list(nodes)
    for element in nodes:
        counter_level = element.count('[')
        counter_level = counter_level + element.count(',')
        if counter_level in dict_levels:
            old_list = dict_levels[counter_level]
            old_list.append(element)
            dict_levels[counter_level] = old_list
        else:
            dict_levels[counter_level] = [element]

    print("dict_levels", dict_levels)
    return dict_levels


def get_dict_successors(dict_levels):
    dict_successors = dict()

    level = 1
    max_level = max(dict_levels.keys())

    while level < max_level:
        for node in dict_levels[level]:
            successor_list = list()
            for child_node in dict_levels[level+1]:
                if child_node.startswith(node[:-1]):
                    successor_list.append(child_node)
            dict_successors[node] = successor_list

        level += 1

    # leaf nodes
    for node in dict_levels[max_level]:
        dict_successors[node] = list()

    print("dict_successors", dict_successors)
    return dict_successors