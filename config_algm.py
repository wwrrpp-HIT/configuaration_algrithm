config_T = {'config': 'config_T',
            'module_num': 5,
            'module_location': ((1, 1), (2, 1), (3, 1), (2, 2), (2, 3)),
            'module_connection':
                [[0, 1, 0, 0, 0],
                 [1, 0, 1, 1, 0],
                 [0, 1, 0, 0, 0],
                 [0, 1, 0, 0, 1],
                 [0, 0, 0, 1, 0]]
            }


def find_reaf(module_connection):
    sum_i = 0
    reaf_module = []
    for i in range(0, len(module_connection)):
        for j in module_connection[i]:
            sum_i += j
        if sum_i == 1:
            reaf_module.append(i)
            sum_i = 0
        else:
            sum_i = 0
    return reaf_module  # 构型描述中id 从0开始


find_reaf(config_T.get('module_connection'))
print(find_reaf(config_T.get('module_connection')))