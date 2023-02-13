import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from configuration_discribe import Configuration

config_shizi = {'module_adjacency':
                    [[0, 3, 0, 0, 0, 0, 0],
                     [1, 0, 2, 3, 4, 0, 0],
                     [0, 4, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 3, 0],
                     [0, 4, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 3],
                     [0, 0, 0, 0, 0, 3, 0]],
                'module_edges': [(0, 1), (1, 2), (1, 3), (1, 4), (3, 5), (5, 6)],
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
             'module_edges': [(0, 1), (1, 2), (2, 3), (2, 5), (3, 4), (5, 6)],
             'module_num': 7,
             }


class ConfigurationMapping:
    def __init__(self, init_config, goal_config):
        self.init_adjacency = init_config.get('module_adjacency')  # 组成构型的各模块连接关系
        self.goal_adjacency = goal_config.get('module_adjacency')
        self.init_edges = init_config.get('module_edges')
        self.goal_edges = goal_config.get('module_edges')
        self.init_config = Configuration(init_config)
        self.goal_config = Configuration(goal_config)

    def plot_goal_config(self):
        edge_attr = {}
        x = np.array(self.goal_adjacency)
        modules_num = len(x)
        rootnode = self.goal_config.find_root()
        # g = nx.Graph()
        g = nx.from_numpy_matrix(x)
        # g.add_nodes_from(range(0, modules_num), color='blue')
        # g.add_edges_from(self.goal_edges)
        # g.add_node(rootnode[0], color='red')
        #
        # print(nx.get_node_attributes(g, 'color'))
        print(list(nx.bfs_edges(g, rootnode[0])))  # 从根节点开始以bfs方式向叶搜索边
        nx.draw(g, with_labels=True)
        plt.show()


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
# mapping = ConfigurationMapping(config_shizi, config_shizi)
mapping = ConfigurationMapping(config_tu, config_tu)
mapping.plot_goal_config()
