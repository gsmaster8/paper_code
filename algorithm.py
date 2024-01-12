import os

def package_algorithm(task_service_num, task_service_value, task_service_weight,
                      content_num, content_value, content_weight, total_weight):
    result = [[[] for _ in range(total_weight + 1)] for _ in range(task_service_num + content_num)]
    state_arg = [[0] * (total_weight + 1) for _ in range(task_service_num + content_num)]
    for i in range(task_service_num):
        for j in range(total_weight + 1):
            if i == 0:
                if j < task_service_weight[i]:
                    state_arg[i][j] = 0
                    result[i][j].append(0)
                    # print(i, j, result[i][j], state_arg[i][j])
                else:
                    state_arg[i][j] = task_service_value[i]
                    result[i][j].append(1)
                    # print(i, j, result[i][j], state_arg[i][j])
            else:
                if j < task_service_weight[i]:
                    state_arg[i][j] = state_arg[i - 1][j]
                    result[i][j] = result[i - 1][j].copy()
                    result[i][j].append(0)
                    # print(i, j, result[i][j], state_arg[i][j])
                else:
                    if state_arg[i - 1][j] > state_arg[i - 1][j - task_service_weight[i]] + task_service_value[i]:
                        state_arg[i][j] = state_arg[i - 1][j]
                        result[i][j] = result[i - 1][j].copy()
                        result[i][j].append(0)
                        # print(i, j, result[i][j], state_arg[i][j])
                    else:
                        state_arg[i][j] = state_arg[i - 1][j - task_service_weight[i]] + task_service_value[i]
                        result[i][j] = result[i - 1][j - task_service_weight[i]].copy()
                        result[i][j].append(1)
                        # print(i, j, result[i][j], state_arg[i][j])
    for i in range(content_num):
        for j in range(total_weight + 1):
            if j < content_weight[i]:
                state_arg[i + task_service_num][j] = state_arg[i + task_service_num - 1][j]
                result[i + task_service_num][j] = result[i + task_service_num - 1][j].copy()
                result[i + task_service_num][j].append(0)
                # print(i + task_service_num, j, result[i + task_service_num][j], state_arg[i + task_service_num][j])
            else:
                if state_arg[i + task_service_num - 1][j] > state_arg[i + task_service_num - 1][j - content_weight[i]] + content_value[i]:
                    state_arg[i + task_service_num][j] = state_arg[i + task_service_num - 1][j]
                    result[i + task_service_num][j] = result[i + task_service_num - 1][j].copy()
                    result[i + task_service_num][j].append(0)
                    # print(i + task_service_num, j, result[i + task_service_num][j], state_arg[i + task_service_num][j])
                else:
                    state_arg[i + task_service_num][j] = state_arg[i + task_service_num - 1][j - content_weight[i]] + content_value[i]
                    result[i + task_service_num][j] = result[i + task_service_num - 1][j - content_weight[i]].copy()
                    result[i + task_service_num][j].append(1)
                    # print(i + task_service_num, j, result[i + task_service_num][j], state_arg[i + task_service_num][j])
    print("max value:", state_arg[task_service_num + content_num - 1][total_weight])
    return result[task_service_num + content_num -1][total_weight]

def bnb_algorithm(bs):
    # Step1. 根据服务缓存拿到可以卸载的x列表
    # Step2. 计算upper bound
    upper_bound = 0
    # Step3. 剪枝计算结果
    result = []
    branch_and_bound(bs.to_user, result, upper_bound)
    return result

def branch_and_bound(to_user, result, delay, upper_bound):
    if len(result) == len(to_user):
        return
    lo_result = result.copy().append(0)
    ed_result = result.copy().append(1)
    lo_delay = to_user[len(result)].calculate_delay_lo()
    ed_delay = to_user[len(result)].calculate_delay_ed()
    lo_total_delay = 0
    ed_total_delay = 0
    if lo_delay + delay <= upper_bound:
        lo_total_delay = lo_delay + delay + branch_and_bound(to_user, lo_result, delay + lo_delay, upper_bound)
    if ed_delay + delay <= upper_bound:
        ed_total_delay = ed_delay + delay + branch_and_bound(to_user, ed_result, delay + ed_delay, upper_bound)
    if len(lo_result) == len(to_user) and len(ed_result) == len(to_user):
        if lo_total_delay < ed_total_delay:
            result = lo_result.copy()
        else:
            result = ed_result.copy()
    elif len(lo_result) == len(to_user):
        result = lo_result.copy()
    else:
        result = ed_result.copy()
    return





if __name__ == '__main__':
    task_service_value = [58, 56, 92, 22]
    task_service_weight = [5, 4, 6, 3]
    content_value = [33, 58, 12, 41]
    content_weight = [5, 5, 3, 2]
    result = package_algorithm(len(task_service_value), task_service_value, task_service_weight, len(content_value), content_value, content_weight, 15)
    print(result)
