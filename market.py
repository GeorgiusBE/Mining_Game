# import libraries
import random

class market:

    def __init__(self):
        # price of sdpa on day 1
        self.sdpa_price = 50
        pass
    
    # generate new sdpa price
    def new_sdpa_price(self):
        self.sdpa_price *= (1 + random.gauss(0.01, 0.005))
        return self.sdpa_price