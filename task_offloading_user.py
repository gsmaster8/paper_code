from location import Location

class TOUser:
    def __init__(self, num = 0, cj = 0, bj = 0, pj = 0, hj = 0, fj = 0):
        self.num = num  # 编号
        self.channel_num = -1
        self.c_j = cj  # 计算量
        self.b_j = bj  # 数据量
        self.p_j = pj  # 功率
        self.h_j = hj  # 信道增益
        self.f_j = fj  # 本地计算资源
        self.w_j = 0
        self.n_j = 0
        self.offloading_bs = True
        self.location = Location()
        self.location.random_locaton()
    
    def offloading_local(self):
        self.offloading_bs = False
    
    def offloading_bs(self):
        self.offloading_bs = True
    
    def calculate_delay_ed(self, f_m_j):
        return round(self.c_j / f_m_j, 2)

    def calculate_delay_tr(self, r_m_j):
        return round(self.b_j / r_m_j, 2)
    
    def calculate_delay_lo(self):
        return round(self.c_j / self.f_j, 2)
    
    def show(self):
        print(f"No.{self.num}", "TOUser channel num is ", self.channel_num)
        print(f"No.{self.num}", "TOUser c_j is ", self.c_j)
        print(f"No.{self.num}", "TOUser b_j is ", self.b_j)
        print(f"No.{self.num}", "TOUser p_j is ", self.p_j)
        print(f"No.{self.num}", "TOUser h_j is ", self.h_j)
        print(f"No.{self.num} lcoation:")
        self.location.show()


if __name__ == '__main__':
    user0 = TOUser(0, 1, 2, 3, 4)
    user0.show()
