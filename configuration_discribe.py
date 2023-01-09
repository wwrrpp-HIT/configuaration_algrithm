import copy

import numpy as np
import networkx as nx
from typing import List

import module as md

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


class Configuration:
    def __init__(self, config):
        self.config_name = config.get('config')
        self.module_num = config['module_num']  # 组成构型的模块数量
        self.module_location = config.get('module_location')  # 组成构型的各模块位置
        self.module_adjacency = config.get('module_adjacency')  # 组成构型的各模块连接关系
        self.module_edges = config.get('module_edges')
        self.generate_modules()

    def generate_modules(self):
        """构造参与构型的模块群"""
        modules = []
        for _ in range(self.module_num):
            module = md.Module()
            modules.append(module)
        return modules

    def find_root(self):
        """
        输出根序号及根对应高度，序号由0开始
        e.g. ([root1, root2], [height1, height2])
        """
        copy_edges = self.module_edges.copy()
        root = []
        height = []
        G = nx.Graph()
        G.add_edges_from(self.module_edges)  # 生成构型树，用于计算根节点到各节点距离
        for module_id in range(self.module_num):
            for edge in self.module_edges:
                if module_id in edge:
                    copy_edges.remove(edge)  # 去除边集合中与该节点相连的边
            g = nx.Graph()
            g.add_edges_from(copy_edges)  # 生成去掉当前节点后的树（森林），用于生成连通分量
            connect_components = [x for x in nx.connected_components(g)]  # 去掉某一节点后的连通分量
            connect_component_num = []
            for connect_component in connect_components:
                connect_component_num.append(len(connect_component))
            max_num_connect_components = max(connect_component_num)
            if max_num_connect_components <= self.module_num // 2:  # 除去某节点后，剩余最大的连通分量的节点数小于等于节点数的1/2,则
                # 该节点是root
                root.append(module_id)
                len_root2modules = nx.shortest_path_length(G, module_id)  # 根节点到各节点距离
                height.append(max(len_root2modules.values()))
                copy_edges = self.module_edges.copy()
            else:
                copy_edges = self.module_edges.copy()
        # return root, height
        # 只输出第一个根节点序号
        return [root[0]]

    def node_children_in_tree(self, root) -> (List[List[int]]):
        """输出以root为根的构型，各节点的子节点id。
            e.g. [[], [0, 2], [], [1], [3, 6], [], [5, 7], []]
        """
        neighbors = [list() for _ in range(self.module_num)]
        module_set = [x for x in range(self.module_num)]
        for start, end in self.module_edges:
            neighbors[start].append(end)
            neighbors[end].append(start)
        children = list(copy.deepcopy(neighbors))
        root_neighbors = neighbors[root]
        root_children = root_neighbors
        viewed_nodes = [root]
        module_set.remove(root)
        current_nodes = root_children
        res = []
        while module_set:
            for current_node in current_nodes:
                for viewed_node in viewed_nodes:
                    if viewed_node in children[current_node]:
                        children[current_node].remove(viewed_node)
                module_set.remove(current_node)
                viewed_nodes.append(current_node)
                if children[current_node]:
                    for i in children[current_node]:
                        res.append(i)
            current_nodes = res  # current_node的更新按照上一轮检测的顺序来的，可能会存在问题
        return children

    def _connect_position(self, module, root):
        """'module_location': [(1, 1), (1, 2), (1, 3), (2, 2), (3, 2), (4, 1), (4, 2), (4, 3)]"""
        connect_position = []

        module_location = self.module_location[module]

        children = self.node_children_in_tree(root)
        module_children = children[module]

        for child in module_children:
            if module_location[0] - self.module_location[child][0] != 0 and module_location[1] - \
                    self.module_location[child][1] != 0:
                return f"they are not neighbors，{module} and {child}"
            else:
                if module_location[0] - self.module_location[child][0] == 0 and module_location[1] - \
                        self.module_location[child][1] == 1:
                    connect_position.append(str('L'))
                elif module_location[0] - self.module_location[child][0] == 0 and module_location[1] - \
                        self.module_location[child][1] == -1:
                    connect_position.append('R')
                elif module_location[0] - self.module_location[child][0] == 1 and module_location[1] - \
                        self.module_location[child][1] == 0:
                    connect_position.append('F')
                elif module_location[0] - self.module_location[child][0] == -1 and module_location[1] - \
                        self.module_location[child][1] == 0:
                    connect_position.append('F')
        return connect_position

    def edges2adjacency(self):
        """由图生成邻接矩阵，初始化中可无邻接矩阵信息"""
        pass

    def find_min_height_trees(self) -> list:
        # base cases
        n = self.module_num
        edges = self.module_edges
        if n <= 2:
            return [i for i in range(n)]

        # Build the graph with the adjacency list
        neighbors = [set() for i in range(n)]
        for start, end in edges:
            neighbors[start].add(end)
            neighbors[end].add(start)

        # Initialize the first layer of leaves
        leaves = []
        for i in range(n):
            if len(neighbors[i]) == 1:
                leaves.append(i)

        # Trim the leaves until reaching the centroids
        remaining_nodes = n
        while remaining_nodes > 2:
            remaining_nodes -= len(leaves)
            new_leaves = []
            # remove the current leaves along with the edges
            while leaves:
                leaf = leaves.pop()
                # the only neighbor left for the leaf node
                neighbor = neighbors[leaf].pop()
                # remove the only edge left
                neighbors[neighbor].remove(leaf)
                if len(neighbors[neighbor]) == 1:
                    new_leaves.append(neighbor)

            # prepare for the next round
            leaves = new_leaves

        # The remaining nodes are the centroids of the graph
        return leaves


# t = Configuration(config_T)
# cross = Configuration(config_cross)
# h = Configuration(config_H)
# print(h.generate_modules())
# print(h.find_root())
# print(h.node_children_in_tree(4))
# h_children = h.node_children_in_tree(4)
# for i in range(h.module_num):
#     print(h._connect_position(i, 3), f'{i}')
