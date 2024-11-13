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
    def sell_sdpa(self, n_coins, sdpa_price):
        '''
        Not to be used alone
        n_coins -> numer of coins to be sold
        sdpa_price -> the market price of SDPA coin
        '''
        # update SDPA coin balance
        self.sdpa_balance -= n_coins
        # update capital
        self.capital += sdpa_price * n_coins
        
    
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

    # query user to pick an action
    def action_query(self, action, sdpa_price):
        '''
        sdpa_price -> the market price of the SDPA coin
        '''
        
        # if choose to buy mining machines
        if action == 1:
            # query for the number of machines to purchase
            n_machines = int(input('Enter number of ASIC machines to buy: '))
            # update total machines owned and capital
            self.buy_machines(n_machines)
            # print current status of user


        # if choose to sell SDPA coins
        elif action == 2:
            # query for the number of coins to be sold
            sdpa_sold = int(input('Enter number of SDPA coins to be sold: '))
            # update SDPA coin balance and capital
            self.sell_sdpa(sdpa_sold, sdpa_price)
