from location import Location

class CRUser:
    def __init__(self, num = 0, ai = 0, pi = 0, hi = 0):
        self.num = num  # 编号
        self.channel_num = -1
        self.a_i = ai  # 内容量
        self.p_i = pi  # 功率
        self.h_i = hi  # 信道增益
        self.w_i = 0
        self.n_i = 0
        self.request_bs = True
        self.location = Location()
        self.location.random_locaton()

    def request_cloud(self):
        self.request_bs = False
    
    def request_bs(self):
        self.request_bs = True

    def calculate_delay_tr(self):
        return round(self.a_i / (self.w_i * self.n_i), 2)
    
    def calculate_delay_lo(self):
        return round(self.c_j / self.f_j, 2)
    
    def show(self):
        print(f"No.{self.num}", "CRUser channel num is ", self.channel_num)
        print(f"No.{self.num}", "CRUser a_i is ", self.a_i)
        print(f"No.{self.num}", "CRUser p_i is ", self.p_i)
        print(f"No.{self.num}", "CRUser h_i is ", self.h_i)
        print(f"No.{self.num} lcoation:")
        self.location.show()

if __name__ == '__main__':
    user0 = CRUser(0, 1, 2, 3)
    user0.show()
