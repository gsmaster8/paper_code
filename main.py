import os
from task_offloading_user import TOUser
from content_request_user import CRUser
from base_station import BS
from base_station import BS_RADIUS

def init_bs_location(bs_vec, bs):
    init_succ = False
    while not init_succ:
        bs.location.random_locaton()
        init_succ = True
        for bs_n in bs_vec:
            if bs.location.in_circle_range(bs_n.location, BS_RADIUS):
                init_succ = False
                break

def start(bs_num):
    bs_vec = []
    # 初始化基站
    for i in range(bs_num):
        bs = BS(i, 1, 2, 3)
        init_bs_location(bs_vec, bs)
        bs_vec.append(bs)
    # 基站范围内生成to_user cr_user
    for bs in bs_vec:
        bs.generate_to_user(20)
        bs.generate_cr_user(10)
        # 计算to用户的时延
        to_user_delay = bs.calculate_all_to_user_delay(bs_vec)
        # 计算cr用户的时延
        cr_user_delay = bs.calculate_all_cr_user_delay(bs_vec)

