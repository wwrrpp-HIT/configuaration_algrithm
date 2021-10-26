import collections



def findMinHeightTrees( n: int, edges: list):
    if (n == 1):
        return [0]
    elif (n == 2):
        return [0, 1]

    # 计算叶结点
    count = [0] * n
    for edge in edges:
        count[edge[0]] += 1
        count[edge[1]] += 1

    # 计算叶结点到其他叶结点的最大距离
    max_length = 0
    max_path = []
    current = -1
    for i in range(n):
        if (count[i] != 1):
            continue
        current = i
        break
    pre = -1
    while (True):
        q = collections.deque()
        path = [current]
        q.append(path)
        vis = [False] * len(edges)
        while len(q) > 0:
            for _ in range(len(q)):
                v = q.popleft()
                node = v[-1]
                if (count[node] == 1 and node != current):
                    v1 = v.copy()
                    if (len(v1) == max_length):
                        max_path.append(v1)
                    elif (len(v1) > max_length):
                        max_path = [v1]
                        max_length = len(v1)
                else:
                    for j in range(len(edges)):
                        if (vis[j]):
                            continue
                        if (edges[j][0] == node):
                            v1 = v.copy()
                            v1.append(edges[j][1])
                            q.append(v1)
                            vis[j] = True
                        elif (edges[j][1] == node):
                            v1 = v.copy()
                            v1.append(edges[j][0])
                            q.append(v1)
                            vis[j] = True
        finish = False
        for path in max_path:
            if (pre == path[-1]):
                finish = True
                break
        if (finish):  # 如果从叶节点A到叶节点B是最长路径，从叶节点B到叶节点A也是最长路径
            break
        pre = current
        current = max_path[0][-1]

    # 取最大距离的路径的中间结果为结果
    result = set()
    for path in max_path:
        if len(path) % 2 == 1:
            result.add(path[len(path) // 2])
        else:
            result.add(path[len(path) // 2])
            result.add(path[len(path) // 2 - 1])

    return list(result)


n = 4
edges = [[0, 1], [1, 2], [1, 3]]

print(findMinHeightTrees( n, edges))
