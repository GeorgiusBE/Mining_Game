'''
user_account.py
---------------
A module to store and manage user data in blockchain simulation

This module focuses on user data management. Based on the user's chosen action, user data gets updated.
It also logs all actions that the user performs.

Classes 
-------
UserAccount
    A class that represents the user's account, storing and managing user's data.

'''


# import libraries
import math

# UserAccount class
class UserAccount:
    '''
    A class to store and manage user data in blockchain simulation.

    This module stores user information, including name, capital, SDPA coins balance,
    number of machines owned, machines status, and mining type.
    Moreover, user data will be updated based on the user's chosen action.
    ...

    Attributes
    ----------
    name : str
        The user's name.
    capital : float
        The cash capital of the user.
    sdpa_balance : float
        The number of SDPA coins the user owns.
    machines : int
        The total number of machines the user owns.
    machine_status : str
        The machine status can be turned on or off.
    mining_type : str
        Users can either be a solo miner or part of a mining pool.
    bankrupt_status : str
        Indicates whether the user is bankrupt ('yes' or 'no').
    
    Methods
    -------
    reset_daily_machine_purchases()
        To reset the count of the number of machines purchased for the day.
    buy_machines(n_machines, machine_price = 600)
        Updates the number of machines owned and capital balance for the purchase of machines.
    sell_sdpa(n_coins)
        Updates the capital and SDPA coin balance for the sale of SPDA coins.
    machine_switch()
        Toggles machine status between 'off' or 'on'.
    change_mining_type()
        Toggles mining type between 'solo' or 'pooled'
    action_query(action, sdpa_price, current_day, user_activity_log)
        Handles user's chosen action and updates the logs.
    electricity_bill(electricity_unit_price, current_day)
        Update the capital balance for electricity bill payment.
    bankrupt_check(current_day, bankruptcy_log)
        Performs automatic sale of SDPA coins if capital turns negative; otherwise delcare bankruptcy.
    '''

    def __init__(self, name, capital = 50000):
        '''
        Parameters
        ----------
        name : str
            Name of the user.
        capital : int or float, optional
            The starting cash capital of the user (default = 50000).
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
        To reset the count of the number of machines purchased for the day.
        This is intended to ensure that the daily purchase limit of the machines is honored.

        Attributes
        ----------
        day_machines : int
            The total number of machines that has been purchased in a trading day.
        '''
        self.day_machines = 0
    
    # purchase new machines
    def buy_machines(self, n_machines, machine_price = 600):
        '''
        Manages the purchase of mining machines.
        
        Handles the purchase of ASIC mining machines by updating the number of machines owned and
        the capital balance. Moreover, it ensure that the user is within the purchase limit and
        have sufficient capital.

        Parameters
        ----------
        n_machines : str
            The number machines to be purchased. Only accepts a positive integer as a string.
        machine_price : int or float, optional
            The cost of 1 ASIC machine (default = 600).

        Raises
        ------
        ValueError
            If `n_machines` is not a positive integer, exceeds the daily purchase limit of 10, or
            insufficient capital to complete the purchase.

        Restrictions
        ------------
        - This method can only be called after the `reset_daily_machine_purchases` method has been
        called, as the `day_machines` attribute is initialized in the `reset_daily_machine_purchases`
        method.
        
        Note
        ----
        - This method is intended to be called within the `action_query` method.
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
        Handles the sale of SDPA coins by updating the SDPA coin balance and capital.

        Parameters
        ----------
        n_coins : str
            The number of coins to be sold. Only accepts positive number as a string.

        Raises
        ------
        ValueError
            If `n_coins` is not a positive number or if the user attempts to short-sell.

        Notes
        -----
        - This method is intended to be called within the `action_query` method.
        '''

        try:
            # ensure that the input is a postive numeric value (including decimal, but exclude negative number)
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
        Toggles the machine status between 'on' and 'off'.
        
        Raises
        ------
        ValueError
            If the user attempts to change maching status when they own 0 machines.

        Notes
        -----
        - This method is intended to be called within the `action_query` method.
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
        Toggles the mining type between 'solo' and 'pooled'.

        Raises
        ------
        ValueError
            If the user attempts to change mining type when they own 0 machines.

        Notes
        -----
        - This method is intended to be called within the `action_query` method.
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

    # process user's chosen action
    def action_query(self, action, sdpa_price, current_day, user_activity_log):
        '''
        Excecutes user's chosen actions.

        Links user's chosen action to the relevant method, and records chosen action to the user activity log.
        
        Parameters
        ----------
        action : int
            The user's chosen action is repsented as an integer.
            1: Purchase mining machines, 2: Sell SDPA coins, 3: Switch ASIC on/off, 4: Switch solo/pooled mining.
        sdpa_price : float
            The market price of the SDPA coin.
        current_day : int
            The current day.
        user_activity_log : dict
            A nested dictionary that stores user's key actions.
            This log is generated by the `create_logs` method of the BlockChain class.
            The data structure is,
                {
                    user_name: {
                        day: {
                            action: [param]
                        }
                    }
                }
            where:
                - user_name : str
                    The user name.
                - day : str
                    The day during the simulation (e.g. 'Day 1').
                - action : str
                    The type of action performed (e.g. 'Action 1').
                - param
                    The specified parameter for the action performed.


        Attributes
        ----------
        current_day : int
            The current day.
        sdpa_price : float
            The market price of the SDPA coin.
        user_activity_log : dict
            A nested dictionary that stores user's key actions.
        valid_indicator : int
            An indicator to keep track when a valid user input has been provided.

        Notes
        -----
        - This method assumes that the correct data structure has been provided for the `user_activity_log`
        parameter. For convenience, use the `BlockChain` class' `create_logs` method to generate this log. 

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
        Charge electricity bill.

        Computes total electricity bill based on the number of active machines and the market price
        of electricity. Deducts the user's capital balance and record the electricity expense to the
        user activity log. 
        
        Parameters
        ----------
        electricity_unit_price : float
            The per unit price of electricity.
        current_day : int
            The current day.

        Attributes
        ----------
        total_bill
            The total electricity bill the user is charged for the day.

        Restrictions
        ------------
        - This method can only be called after the `action_query` method has been called, as the
        `user_activity_log` attribute is defined in the `action_query` method.
        
        Notes
        -----
        - `current_day` parameter is purposefully redefined because the `current_day` attribute defined
        in the action_query method may not always be 'up-to-date'. For example, if Action 5 (i.e. End Action)
        is the only chosen action by the user, `action_query` method does not get called, and thus the
        `current_day` attribute does not get updated.
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
        Check for bankruptcy.

        When the user's capital is detected to be negative, SDPA coins will be automatically sold, such that
        the capital is no longer negative. If the user has insufficient SDPA coins, the user will be declared
        bankrupt.
        Updates the user activity and bankruptcy log.  

        Parameters
        ----------
        current_day : int
            The current day
        bankruptcy_log : dict
            A log that stores name of users who went benkrupt and the corresponding day of bankruptcy.

        Restrictions
        ------------
        - This method can only be called after the `action_query` method has been called, as the
        `user_activity_log` attribute is defined in the `action_query` method.
        
        Notes
        -----
        - `current_day` parameter is purposefully redefined because the `current_day` attribute defined
        in the action_query method may not always be 'up-to-date'. For example, if Action 5 (i.e. End Action)
        is the only chosen action by the user, `action_query` method does not get called, and thus the
        `current_day` attribute does not get updated.
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
                self.sell_sdpa(str(sdpa_auto_sale))
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