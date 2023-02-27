import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from configuration_discribe import Configuration

config_shizi = {'module_adjacency':
                    [[0, 3, 0, 0, 0, 0, 1],
                     [1, 0, 2, 3, 4, 0, 0],
                     [0, 4, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 3, 0],
                     [0, 4, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 3],
                     [1, 0, 0, 0, 0, 3, 0]],
                'module_edges': [(1, 0), (1, 2), (1, 3), (1, 4), (3, 5), (0, 6)],
                'module_num': 7,
                }
config_tu = {'module_adjacency':
                 [[0, 1, 0, 0, 0, 0, 0],
                  [1, 0, 3, 0, 0, 0, 0],
                  [0, 1, 0, 2, 0, 4, 0],
                  [0, 0, 4, 0, 3, 0, 0],
                  [0, 0, 0, 2, 0, 0, 0],
                  [0, 0, 2, 0, 0, 0, 3],
                  [0, 0, 0, 0, 0, 1, 0]],
             'module_edges': [(1, 0), (2, 1), (2, 3), (2, 5), (3, 4), (5, 6)],
             'module_num': 7,
             }
config_gong = {'config': 'config_gong',
               'module_num': 7,
               'module_adjacency':
                   [[0, 2, 0, 0, 0, 0, 0],
                    [3, 0, 1, 4, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 4, 0, 0],
                    [0, 0, 0, 2, 0, 3, 1],
                    [0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0]],
               'module_edges': [(1, 0), (1, 2), (3, 1), (3, 4), (4, 6), (4, 5)],
               }
config_T = {'config': 'config_T',
            'module_num': 5,
            'module_location': [(1, 1), (2, 1), (3, 1), (2, 2), (2, 3)],
            'module_adjacency':
                [[0, 1, 0, 0, 0],
                 [1, 0, 1, 1, 0],
                 [0, 1, 0, 0, 0],
                 [0, 1, 0, 0, 1],
                 [0, 0, 0, 1, 0]],
            'module_edges': [(0, 1), (1, 2), (1, 3), (3, 4)],
            }

config_cross = {'config': 'config_cross',
                'module_num': 7,
                'module_location': [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (0, 4), (1, 5)],
                'module_adjacency':
                    [[0, 1, 0, 0, 0, 0, 0],
                     [1, 0, 1, 0, 0, 0, 0],
                     [0, 1, 0, 1, 0, 0, 0],
                     [0, 0, 1, 0, 1, 1, 1],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0]],
                'module_edges': [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (3, 6)],
                }
config_H = {'config': 'config_H',
            'module_num': 8,
            'module_location': [(1, 1), (1, 2), (1, 3), (2, 2), (3, 2), (4, 1), (4, 2), (4, 3)],
            'module_adjacency':
                [[0, 1, 0, 0, 0, 0, 0, 0],
                 [1, 0, 1, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 0, 1],
                 [0, 0, 0, 0, 0, 0, 1, 0]],
            'module_edges': [(0, 1), (1, 2), (1, 3), (3, 4), (4, 6), (5, 6), (6, 7)],
            }


class ConfigurationMapping:
    def __init__(self, init_config, goal_config):
        self.init_adjacency = init_config.get('module_adjacency')  # 组成构型的各模块连接关系
        self.goal_adjacency = goal_config.get('module_adjacency')
        self.init_edges = init_config.get('module_edges')  # edges确保父前子后，即(parent_node, child_node),便于生成有向图
        self.goal_edges = goal_config.get('module_edges')
        self.init_config = Configuration(init_config)
        self.goal_config = Configuration(goal_config)

    def plot_goal_config(self):
        # x = np.array(self.goal_adjacency)
        # g = nx.from_numpy_matrix(x)
        g = nx.DiGraph()
        g.add_edges_from(self.goal_edges)
        rootnode = self.goal_config.find_root()
        bfs_edges = list(nx.bfs_edges(g, rootnode[0]))  # 从根节点开始以bfs方式向叶搜索边
        nx.set_edge_attributes(g, (0, 0), "connector")
        for edge in bfs_edges:
            connector_parent = self.goal_adjacency[edge[0]][edge[1]]
            connector_child = self.goal_adjacency[edge[1]][edge[0]]
            # print(edge, connector_parent, connector_child)
            g[edge[0]][edge[1]]["connector"] = (connector_parent, connector_child)
        # print(g.edges(data=True))
        node_color = {node: 'red' if node == rootnode[0] else 'green' for node in g.nodes}
        edge_labels = nx.get_edge_attributes(g, 'connector')
        pos = nx.spiral_layout(g)
        nx.draw(g, pos, with_labels=True, node_color=[node_color[node] for node in g.nodes])
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
        # plt.show()
        goal_config_with_connector = [rootnode[0], g.edges(data=True)]
        return rootnode[0], list(g.edges(data=True))

    def plot_init_config(self):
        # x = np.array(self.init_adjacency)
        # g = nx.from_numpy_matrix(x)
        g = nx.DiGraph()
        g.add_edges_from(self.init_edges)
        rootnode = self.init_config.find_root()
        bfs_edges = list(nx.bfs_edges(g, rootnode[0]))  # 从根节点开始以bfs方式向叶搜索边
        nx.set_edge_attributes(g, (0, 0), "connector")
        for edge in bfs_edges:
            connector_parent = self.init_adjacency[edge[0]][edge[1]]
            connector_child = self.init_adjacency[edge[1]][edge[0]]
            # print(edge, connector_parent, connector_child)
            g[edge[0]][edge[1]]["connector"] = (connector_parent, connector_child)
        # print(g.edges(data=True))
        node_color = {node: 'red' if node == rootnode[0] else 'green' for node in g.nodes}
        edge_labels = nx.get_edge_attributes(g, 'connector')
        pos = nx.spiral_layout(g)
        nx.draw(g, pos, with_labels=True, node_color=[node_color[node] for node in g.nodes])
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
        # plt.show()
        init_config_with_connector = [rootnode[0], g.edges(data=True)]
        return rootnode[0], list(g.edges(data=True))

    def dfs_common_edges(self, g1, g2, start_node_g1, start_node_g2):
        # Initialize the lists to store visited nodes and common edges
        g1_graph = nx.DiGraph()
        g1_graph.add_edges_from(g1)
        g2_graph = nx.DiGraph()
        g2_graph.add_edges_from(g2)
        visited_g1 = []
        visited_g2 = []
        common_edges = []

        # Initialize the DFS stack for both graphs
        stack_g1 = [start_node_g1]
        stack_g2 = [start_node_g2]
        u = []
        v = []

        # Loop until both stacks are empty
        while stack_g1 or stack_g2:
            # If stack_g1 is not empty, pop the last node from it and add it to visited_g1
            if stack_g1:
                current_node_g1 = stack_g1.pop()
                visited_g1.append(current_node_g1)
                # Check if the current node has any unvisited neighbors and add them to the stack_g1
                for neighbor in g1_graph.neighbors(current_node_g1):
                    if neighbor not in visited_g1:
                        stack_g1.append(neighbor)

            # If stack_g2 is not empty, pop the last node from it and add it to visited_g2
            if stack_g2:
                current_node_g2 = stack_g2.pop()
                visited_g2.append(current_node_g2)
                # Check if the current node has any unvisited neighbors and add them to the stack_g2
                for neighbor in g2_graph.neighbors(current_node_g2):
                    if neighbor not in visited_g2:
                        stack_g2.append(neighbor)

            # Check for common edges with the same 'connector' key value between g1 and g2
            for edge_g1 in g1_graph.edges(visited_g1[-1], data=True):
                for edge_g2 in g2_graph.edges(visited_g2[-1], data=True):
                    if edge_g1[2].get('connector') == edge_g2[2].get('connector'):
                        common_edges.append((edge_g1, edge_g2))
                        u.append(edge_g1[1])
                        v.append(edge_g2[1])
            # 此处若直接用stack_g1做for循环，当倒数第二个元素被remove后，最后一个元素将不会被遍历。
            # 需要注意的是，在循环过程中不能直接改变正在被遍历的列表，否则可能会导致循环出错。如果需要修改列表，建议先将其复制一份再进行修改，或者使用其他遍历方式，比如while循环。
            stack_g1_temp = stack_g1.copy()
            stack_g2_temp = stack_g2.copy()
            for node in stack_g1_temp:
                if node not in u:
                    visited_g1.append(node)
                    stack_g1.remove(node)
            for node in stack_g2_temp:
                if node not in v:
                    visited_g2.append(node)
                    stack_g2.remove(node)
        # return common_edges
        return print(common_edges)


# mapping = ConfigurationMapping(config_shizi, config_tu)
mapping = ConfigurationMapping(config_gong, config_tu)
init_config = mapping.plot_init_config()
goal_config = mapping.plot_goal_config()
mapping.dfs_common_edges(init_config[1], goal_config[1], init_config[0], goal_config[0])
