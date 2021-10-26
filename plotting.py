import numpy
import matplotlib.pyplot as plt
import networkx as nx

import env
import configuration_discribe as cd

ic = ((1, 1), (2, 1), (3, 1), (2, 2), (2, 3))  # 初始构型模块位置
gc = (())  # 目标构型


class Plotting:
    def __init__(self):
        self.env = env.Env()

    def plot_map(self):
        robot_location_x = list(map(lambda x: x[0], ic))
        robot_location_y = list(map(lambda x: x[1], ic))
        plt.rc('grid', linestyle='-', color='black')
        plt.grid(True)
        # plt.scatter(robot_location_x, robot_location_y, s=300, marker='s')
        plt.xticks(range(0, self.env.map_x))
        plt.yticks(range(0, self.env.map_y))
        plt.gca().set_aspect(1)  # 设置横纵坐标缩放比，形成正方形网格
        plt.show()

    def plot_config(self, config):
        g = nx.Graph()
        module = [x for x in range(config.module_num)]
        g.add_nodes_from(module)
        position = {}
        count = 0
        for i in config.module_location:
            position[count] = i
            count += 1
        edge_list = ((0, 1), (1, 2), (1, 3), (3, 4))
        g.add_edges_from(edge_list)
        nx.draw_networkx_nodes(g, position, nodelist=module, node_color="r")
        nx.draw_networkx_edges(g, position, width=3)
        nx.draw_networkx_labels(g, position)
        # plt.show()


config_T = {'config': 'config_T',
            'module_num': 5,
            'module_location': ((1, 1), (2, 1), (3, 1), (2, 2), (2, 3)),
            'module_adjacency':
                [[0, 1, 0, 0, 0],
                 [1, 0, 1, 1, 0],
                 [0, 1, 0, 0, 0],
                 [0, 1, 0, 0, 1],
                 [0, 0, 0, 1, 0]]
            }
plot = Plotting()
t = cd.Configuration(config_T)
plot.plot_config(t)
plot.plot_map()
