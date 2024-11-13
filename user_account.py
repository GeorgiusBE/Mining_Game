# UserAccount class
class UserAccount:

    def __init__(self, name):
        '''
        name -> name of the user 
        '''
        # name of the user
        self.name = name
        # intial capital
        self.capital = 50000
        # intial number of SDPA coin
        self.sdpa_balance = 0
        # intial number of machines
        self.machines = 0
    
    # purchase new machines
    def buy_machines(self, n_machines):
        '''
        n_machines -> number of machines to be purchased
        '''
        pass

    # switch the machines on/off
    def machine_swith(self, swith):
        '''
        switch -> on/off (str)
        '''
        pass

    # sell SDPA coin
    def sell_coins(self, n_coins):
        '''
        n_coins -> numer of coins to be sold
        '''
        pass

    # bankruptcy check
    def bankrupt_check(self):
        pass