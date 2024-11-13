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
        Not to be used alone
        n_machines -> number of machines to be purchased
        '''
        # update total number of machines owned
        self.machines += n_machines
        # update capital
        self.capital -= 600 * n_machines

    # switch the machines on/off
    def machine_swith(self, swith):
        '''
        Not to be used alone
        switch -> on/off (str)
        '''
        pass

    # sell SDPA coin
    def sell_coins(self, n_coins):
        '''
        Not to be used alone
        n_coins -> numer of coins to be sold
        '''
        pass
    
    # switch mining type (solo/pooled)
    def mining_switch(self):
        '''
        Not to be used alone
        '''
        pass

    # bankruptcy check
    def bankrupt_check(self):
        '''
        Not to be used alone
        '''
        pass