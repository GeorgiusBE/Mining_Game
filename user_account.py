import math

# UserAccount class
class UserAccount:

    def __init__(self, name, capital = 50000):
        '''
        name -> name of the user
        capital -> the starting cash capital fo0r the user
        '''
        # name of the user
        self.name = name
        # intial capital
        self.capital = capital
        # intial number of SDPA coin
        self.sdpa_balance = 0
        # intial number of machines
        self.machines = 0
        # initial machine status
        self.machine_status = 'off'
        # initial mining type
        self.mining_type = 'solo'
        # bankruptcy status
            # 'yes' to indicate bankruptcy, otherwise 'no'
        self.bankrupt_status = 'no'
    
    def reset_daily_machine_purchases(self):
        '''
        Resets the object that tracks the number of machines purchased per day.
        '''
        self.day_machines = 0
    
    # purchase new machines
    def buy_machines(self, n_machines, machine_price = 600):
        '''
        Not to be used alone
        n_machines -> (str) number of machines to be purchased
        machine_price -> (float) price for 1 unit of ASIC machine
        '''
        try:
            # ensure that the input is a positive integer (i.e. preventing negative numbers, non-integer, letters, and characters)
            if not n_machines.isdigit():
                raise ValueError('Invalid input: Only positive integer values are accepted. (Enter "0" to cancel purchase and go back to main menu.)')

            # convert data type to integer
            n_machines = int(n_machines)

            # ensure that the number of machines purchased per day does not exceed 10
            if self.day_machines + n_machines > 10:
                raise ValueError(f'Invalid quantitiy: 10 is the daily limit on the purchase of ASIC machines. {self.day_machines} units has been purchased today. (Enter "0" to cancel purchase and go back to main menu.)')

            # compute total cost
            total_cost = machine_price * n_machines
            
            # ensure that the user has sufficient capital to purchase the machines
            if total_cost > self.capital:
                raise ValueError(f'invalid quantity: Insufficient capital to purchase {n_machines} units of ASIC machines. (Enter "0" to cancel purchase and go back to main menu.)')
            
            # store the number of machines purchased
            self.n_machines = n_machines
            # update daily purchase tracker
            self.day_machines += n_machines
            # update total number of machines owned
            self.machines += n_machines
            # update capital
            self.capital -= total_cost
            # update valid indicator
            self.valid_indicator = 1

        except ValueError as err:
            print(err)

    # sell SDPA coin
    def sell_sdpa(self, n_coins):
        '''
        Not to be used alone
        n_coins -> number of coins to be sold
        '''
        try:
            # ensure that the input is a postiive numeric value (including decimal, but exclude negative number)
            if not n_coins.replace('.', '', 1).isdigit():
                raise ValueError('Invalid quantitiy: Please enter a positive numeric value. (Enter "0" to cancel SDPA coins sale and go back to main menu.)')
            
            # covert data type to float
            n_coins = float(n_coins)

            # prevent short-selling
            if n_coins > self.sdpa_balance:
                raise ValueError(f'Insufficient balance: Short-selling is not allowed. You currently own {self.sdpa_balance} SDPA coins. (Enter "0" to cancel SDPA coins sale and go back to main menu.)')

            # update SDPA coin balance
            self.sdpa_balance -= n_coins

            # update capital
            self.capital += self.sdpa_price * n_coins

            # update valid indicator
            self.valid_indicator = 1

            # store the number of coins to be sold
            self.n_coins = n_coins

        # print error message
        except ValueError as err:
            print(err)
            
    # switch the machines on/off
    def machine_swith(self):
        '''
        Not to be used alone
        '''
        try:
            # prevent changes to machine status if the user owns 0 machines
            if self.machines == 0:
                raise ValueError("No machines owned: Cannot switch machine status without owning any machines.")
            
            # turn off the machines if the machines are currently on
            if self.machine_status == 'on':
                self.machine_status = 'off'
            # turn on the machines if the machines are currently off
            elif self.machine_status == 'off':
                self.machine_status = 'on'

        # print error message
        except ValueError as err:
            print(err)

    # switch mining type (solo/pooled)
    def change_mining_type(self):
        '''
        Not to be used alone
        '''
        try:
            # prevent changes to mining type if the user owns 0 machines
            if self.machines == 0:
                raise ValueError("No machines owned: Cannot switch mining type without owning any machines.")

             # change mining type to pooled if current mining type is solo
            if self.mining_type == 'solo':
                self.mining_type = 'pooled'
            # change mining type to solo if current mining type is pooled
            elif self.mining_type == 'pooled':
                self.mining_type = 'solo'

        # print error message
        except ValueError as err:
            print(err)

    # query user to pick an action
    def action_query(self, action, sdpa_price, current_day, user_activity_log):
        '''
        action -> which action to make (int) [1,2,3,4,5]
        sdpa_price -> the market price of the SDPA coin
        current_day -> the current day (int)
        user_activity_log -> a blank template to record users' activity log. It should have the data structure of ...
        day_machines -> the number of machines that has been purchased in the same day
        '''
        # set the current day
        self.current_day = current_day
        # store today's SDPA price
        self.sdpa_price = sdpa_price
        # store the users activity log
        self.user_activity_log = user_activity_log

        # if choose to buy mining machines
        if action == 1:
            # an indicator to keep track when a valid input has been provided
            self.valid_indicator = 0
            while self.valid_indicator == 0:
                # query for the number of machines to purchase
                n_machines = input('Enter number of ASIC machines to buy: ')
                # update total machines owned and capital
                self.buy_machines(n_machines)
                
            # update activity log
            user_activity_log[self.name][f'Day {current_day}']['Action 1'].append(self.n_machines)

        # if choose to sell SDPA coins
        elif action == 2:
            # an indicator to keep track when a valid input has been provided
            self.valid_indicator = 0

            while self.valid_indicator == 0:
                # query for the number of coins to be sold
                sdpa_sold = input('Enter the number of SDPA coins to be sold: ')

                # update SDPA coin balance and capital
                self.sell_sdpa(sdpa_sold)

            # update activity log
            user_activity_log[self.name][f'Day {current_day}']['Action 2'].append(self.n_coins)

        # if choose to switch ASIC machine (on/off)
        elif action == 3:
            # update the machine status
            self.machine_swith()

            # update activity log
            user_activity_log[self.name][f'Day {current_day}']['Action 3'].append(self.machine_status)

        # if choose to mining type
        elif action == 4:
            # update mining type
            self.change_mining_type()

            # update activity log
            user_activity_log[self.name][f'Day {current_day}']['Action 4'].append(self.mining_type)
    
    # charging electricity bill    
    def electricity_bill(self, electricity_unit_price, current_day):
        '''
        electricity_unit_price -> the price for 1 unit of electricity (use the electricity price generated from Market class)
        current_day -> current day (Note that this is purposefully redefined, and not using the current_day
                       defined in the action_query method. This is because when action 5 is chosen, action_query
                       does not get called, and thus the self.current day does not get updated. -> refer to the
                       "if action == 5: break" line of code in the main.py file.)
        '''
        # only charge electricity bill when the machines are on
        if self.machine_status == 'on':
            # compute total bill
            self.total_bill = self.machines * electricity_unit_price
            # update user's capital
            self.capital -= self.total_bill
            # update activity log
            self.user_activity_log[self.name][f'Day {current_day}']['Electricity'] = self.total_bill
        else:
            pass

    # check for bankruptcy
    def bankrupt_check(self, current_day, bankruptcy_log):
        '''
        current_day -> current day (Note that this is purposefully redefined, and not using the current_day
                       defined in the action_query method. This is because when action 5 is chosen, action_query
                       does not get called, and thus the self.current day does not get updated. -> refer to the
                       "if action == 5: break" line of code in the main.py file.)
        '''
        # check for negative capital
        if self.capital < 0:
            # the required number of coins to be sold to address negative capital
            sdpa_auto_sale = (self.capital * -1)/self.sdpa_price
            # round up to 2 decimal places
            sdpa_auto_sale = math.ceil(sdpa_auto_sale * 100) / 100

            # check whether the user owns enough SDPA coin
            if sdpa_auto_sale <= self.sdpa_balance:
                # sell the required amount of SDPA coin
                self.sell_sdpa(sdpa_auto_sale)
                print(f'{sdpa_auto_sale} SDPA coins belonging to {self.name.capitalize()} were automatically sold to resolve the negative capital balance.')

                # update activity log
                self.user_activity_log[self.name][f'Day {current_day}']['Action 2'].append(sdpa_auto_sale)

            # declare bakruptcy
            else:
                # update bankruptcy log
                bankruptcy_log[self.name] = current_day

                # update bankruptcy status
                self.bankrupt_status = 'yes'
                print(f"{self.name.capitalize()} has declared bankruptcy. All of {self.name.capitalize()}'s ASIC machines will be taken offline.")

                # update activity log
                self.user_activity_log[self.name][f'Day {current_day}']['Bankrupt'] = self.bankrupt_status
        # do nothing when capital is positive
        else:
            pass