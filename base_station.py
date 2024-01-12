from location import Location
import math
from task_offloading_user import TOUser
from content_request_user import CRUser

BS_RADIUS = 100

class BS:
    def __init__(self, num = 0, fm = 0, wm = 0, pm = 0):
        self.num = num  # 编号
        self.f_m = fm  # 计算资源
        self.w_m = wm  # 通信资源
        self.p_m = pm  # 功率
        self.location = Location()
        self.location.random_locaton()
        self.to_user = []
        self.cr_user = []
        self.to_user_channel_dict = {}
        self.cr_user_channel_dict = {}
    
    def show(self):
        print(f"No.{self.num}", "BS f_m is", self.f_m)
        print(f"No.{self.num}", "BS w_m is", self.w_m)
        print(f"No.{self.num}", "BS p_m is", self.p_m)
        print(f"No.{self.num}", "BS to user num:", len(self.to_user))
        print(f"No.{self.num}", "BS cr user num:", len(self.cr_user))
        print(f"No.{self.num} lcoation:")
        self.location.show()

    def show_user(self):
        for to_user in self.to_user:
            to_user.show()
        for cr_user in self.cr_user:
            cr_user.show()

    def generate_to_user(self, num):
        for i in range(num):
            to_user = TOUser(i, 1, 2, 3, 4)
            to_user.location.random_location_with_circle(self.location, BS_RADIUS)
            to_user.show()
            self.to_user.append(to_user)

    def generate_cr_user(self, num):
        for i in range(num):
            cr_user = CRUser(i, 1, 2, 3)
            cr_user.location.random_location_with_circle(self.location, BS_RADIUS)
            cr_user.show()
            self.cr_user.append(cr_user)

    def update_user_state(self):
        to_user_channel_num = 0
        cr_user_channel_num = 0
        self.to_user_channel_dict.clear()
        self.cr_user_channel_dict.clear()
        for to_user in self.to_user:
            if to_user.offloading_bs:
                to_user.channel_num = to_user_channel_num
                self.to_user_channel_dict[to_user_channel_num] = to_user
                print("insert to user", to_user_channel_num, to_user.num)
                to_user_channel_num += 1
        for cr_user in self.cr_user:
            if cr_user.request_bs:
                cr_user.channel_num = cr_user_channel_num
                self.cr_user_channel_dict[cr_user_channel_num] = cr_user
                print("insert cr user", cr_user_channel_num, cr_user.num)
                cr_user_channel_num += 1

    def calculate_to_user_channel_delay(self, target_user, bs_vec):
        # 共道干扰
        channel_co = 0
        if target_user.channel_num in self.cr_user_channel_dict:
            channel_co = self.cr_user_channel_dict[target_user.channel_num].p_i * self.cr_user_channel_dict[target_user.channel_num].h_i
        # 内间干扰
        channel_in = 0
        for bs in bs_vec:
            if bs.num == self.num:
                continue
            bs.update_user_state()
            if target_user.channel_num in bs.to_user_channel_dict:
                channel_in += bs.to_user_channel_dict[target_user.channel_num].p_j * bs.to_user_channel_dict[target_user.channel_num].h_j
            if target_user.channel_num in bs.cr_user_channel_dict:
                channel_in += bs.cr_user_channel_dict[target_user.channel_num].p_i * bs.cr_user_channel_dict[target_user.channel_num].h_i
        # si干扰
        channel_si = target_user.p_j
        # sinr
        sinr = (target_user.p_j * target_user.h_j) / (channel_co + channel_in + channel_si)
        # n
        target_user.n_j = math.log2(1 + sinr)

    def calculate_all_to_user_channel_delay(self, bs_vec):
        for to_user in self.to_user:
            self.calculate_to_user_channel_delay(to_user, bs_vec)

    def calculate_cr_user_channel_delay(self, target_user, bs_vec):
        # 共道干扰
        channel_co = 0
        if target_user.channel_num in self.to_user_channel_dict:
            channel_co = self.to_user_channel_dict[target_user.channel_num].p_j * self.to_user_channel_dict[target_user.channel_num].h_j
        # 内间干扰
        channel_in = 0
        for bs in bs_vec:
            if bs.num == self.num:
                continue
            bs.update_user_state()
            if target_user.channel_num in bs.to_user_channel_dict:
                channel_in += bs.to_user_channel_dict[target_user.channel_num].p_j * bs.to_user_channel_dict[target_user.channel_num].h_j
            if target_user.channel_num in bs.cr_user_channel_dict:
                channel_in += bs.cr_user_channel_dict[target_user.channel_num].p_i * bs.cr_user_channel_dict[target_user.channel_num].h_i
        # sinr
        sinr = (target_user.p_i * target_user.h_i) / (channel_co + channel_in)
        # n
        target_user.n_i = math.log2(1 + sinr)

    def calculate_all_cr_user_channel_delay(self, bs_vec):
        for cr_user in self.cr_user:
            self.calculate_cr_user_channel_delay(cr_user, bs_vec)

    def calculate_all_to_user_delay(self, bs_vec):
        all_delay = 0
        self.update_user_state()
        self.calculate_all_to_user_channel_delay(bs_vec)
        for to_user in self.to_user:
            if to_user.offloading_bs:
                # process delay
                f_m_j = self.get_f_m_j(to_user)
                if f_m_j == 0:
                    continue
                all_delay += to_user.calculate_delay_ed(f_m_j)
                # trans delay
                r_m_j = self.get_r_m_j(to_user)
                if r_m_j == 0:
                    continue
                all_delay += to_user.calculate_delay_tr(r_m_j)
            else:
                all_delay += to_user.calculate_delay_lo()
        return all_delay
    
    def calculate_all_cr_user_delay(self, bs_vec):
        all_delay = 0
        self.update_user_state()
        self.calculate_all_cr_user_channel_delay(bs_vec)
        for cr_user in self.cr_user:
            if cr_user.request_bs:
                # w_i 等于 同信道的 w_j
                cr_user.w_i = self.to_user_channel_dict[cr_user.channel_num].w_j
                all_delay += cr_user.calculate_delay_tr()
            else:
                all_delay += cr_user.calculate_delay_lo()
        return all_delay

    def get_f_m_j(self, target_user):
        numerator = 0
        denominator = 0
        numerator = self.f_m * math.sqrt(target_user.c_j)
        for to_user in self.to_user:
            if to_user.offloading_bs:
                denominator += math.sqrt(to_user.c_j)
        if denominator == 0:
            return 0
        return round(numerator / denominator, 2)
    
    def get_r_m_j(self, target_user):
        # w
        w_j_numerator = self.w_m * math.sqrt(target_user.b_j / target_user.n_j)
        w_j_denominator = 0
        for to_user in self.to_user:
            if to_user.offloading_bs:
                w_j_denominator += math.sqrt(to_user.b_j / to_user.n_j)
        target_user.w_j = w_j_numerator / w_j_denominator
        return round(target_user.w_j * target_user.n_j, 2)


if __name__ == '__main__':
    bs0 = BS(0, 1, 2, 3)
    bs0.show()
    bs0.generate_to_user(15)
    bs0.generate_cr_user(10)
    bs0.update_user_state()
    bs0.show()
    bs0.show_user()
    
