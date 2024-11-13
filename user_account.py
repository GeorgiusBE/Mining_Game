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
        # initial machine status
        self.machine_status = 'off'
    
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
    def machine_swith(self, switch):
        '''
        Not to be used alone
        switch -> it accepts either 'on' or 'off' (str)
        '''
        try:
            # turn on the machines
            if switch == 'on':
                self.machine_status = 'on'
            # turn off the machines
            elif switch == 'off':
                self.machine_status = 'off'
            # raise error if any other values are entered
            else:
                raise ValueError("Invalid value: It only accepts 'on' or 'off'")

        # print error message    
        except ValueError as err:
            print(err)

    # sell SDPA coin
    def sell_sdpa(self, n_coins, sdpa_price):
        '''
        Not to be used alone
        n_coins -> number of coins to be sold
        sdpa_price -> the market price of SDPA coin
        '''
        try:
            # short-selling is not allowed
            if n_coins > self.sdpa_balance:
                raise ValueError("Insufficient balance: Cannot sell more SDPA coins than currently owned. Short-selling is not allowed.")
            # update SDPA coin balance
            self.sdpa_balance -= n_coins

            # update capital
            self.capital += sdpa_price * n_coins

        # print error message
        except ValueError as err:
            print(err)

    
    # switch mining type (solo/pooled)
    def mining_type(self):
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

        # if choose to sell SDPA coins
        elif action == 2:
            # query for the number of coins to be sold
            sdpa_sold = int(input('Enter number of SDPA coins to be sold: '))
            # update SDPA coin balance and capital
            self.sell_sdpa(sdpa_sold, sdpa_price)

        # if choose to switch ASIC machine (on/off)
        elif action == 3:
            try:
                # prevent any change to machine status if the user owns 0 machines
                if self.machines == 0:
                    raise ValueError("No machines owned: Cannot switch machine status without owning any machines.")

                # query for on/off instruction
                switch = input("Enter 'on' to turn on the machines or 'off' to turn them off: ")
                # update the machine status
                self.machine_swith(switch)

            # print error message
            except ValueError as err:
                print(err)
