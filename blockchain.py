# Georgius Benedikt Ermanta
# Fintech
# This module defines the `BlockChain` class which is used to simulate blockchain mining.

'''
blockchain.py
---------------
A module to simulate blockchain mining.

This module defines the `Blockchain` class. Users can get involved in mining activity as either a solo miner or as part
of a mining pool. The winner will be determined randomly, where probability of winning is proportional to the
computational power of the users, and the winner will receive the prize.
Moreover, logs are initialized to record all users activities.

Class
-----
BlockChain
    A class to determine the daily winners and distribute daily prize, as well as to generate user activity log and bankruptcy log.

'''

# import libraries
import random

class BlockChain:
    '''
    A class used to determine and distribute daily prize to the winning users;
    as well as to record users' actions in a log.
    ...

    Attributes
    ----------
    n_days : int
        Number of days in the simulation.

    Methods
    -------
    create_logs(lst_users)
        Creates 2 logs:
            - Stores users key actions.
            - Stores users that went benkrupt.
    winner(list_operational_users, current_day, base_pooled_mach = 1000, total_prize = 100)
        Determines the daily winners and the prize distributed to those winners.
    '''

    def __init__(self, n_days):
        '''
        Parameters
        ----------
        n_days : int
            Number of days in the simulation.
        '''

        # store the number of days in the simulation
        self.n_days = n_days

    # create logs
    def create_logs(self, lst_users):
        '''
        Creates 2 logs:
        1. User activity log: Stores users key actions during the simulation.
        2. Bankruptcy log: Stores name of users who went benkrupt and the corresponding day of bankruptcy.
        
        Parameters
        ----------
        lst_users : list
            A list of `UserAccount` objects of all users.
        
        Attributes
        ----------
        user_activity_log : dict
            A nested dictionary to stores users key actions in the simulation.
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
                    The type of action performed.
                - param
                    The specified parameter for the action performed.
        bankruptcy_log : dict
            Stores the user names of users that went bankrupt, along with their respective day of bankruptcy.
        
        Returns
        -------
        tuple
            A tuple containing 2 elements:
            - dict: The user activity log.
            - dict: The bankruptcy log.
        '''

        # create activity log
        self.user_activity_log = {}
        for user in lst_users:
            self.user_activity_log[user.name] = {f'Day {n}': {f'Action {i}': [] for i in range(1,5)} for n in range(1, self.n_days+1)}
        
        # create bankruptcy log
        self.bankruptcy_log = {}

        return self.user_activity_log, self.bankruptcy_log

    # determine the end-of-day winner
    def winner(self, list_operational_users, current_day, base_pooled_mach = 1000, total_prize = 100):
        '''
        Determine the daily winner and distrbute the daily prize to the winners.
        
        The daily winner is chosen at ranodm, with the probabilty of winning is proportional to the their mining power.
        - If a user with solo mining type wins, they will receive the whole daily prize.
        - If the pool wins, users in the pool will be receive a portion of the total daily prize, based on their mining
        power relative to the aggregate mining power in the pool.

        Parameters
        ----------
        list_operational_users : list
            A list of `UserAccount` objects of all users that are operational (i.e. they have not gone bankrupt).
        current_day :int
            The current day.
        base_pooled_mach : int, optional
            The base number of machines in the pool (default is 1000).
        total_prize : int or float, optional
            The total daily SDPA prize to be awarded to the winning player/s at the end of the day (default is 100). 
        
        Attributes
        ----------
        base_pooled_mach : int
            The base number of machines in the pool.
        list_operational_users : list
            A list of `UserAccount` class objects of all users that are operational (i.e. they have not gone bankrupt).
        total_machines : int
            The total number of machines (including active (on) and inactive (off) machines).
        mining_players : dict
            Stores the user names of users who have their machines turned on, along with
            their respective computing power (i.e. the number of machines owned).
            Note:
                - Users with `pooled` mining type are aggregated under the `pooled` key.
        active_machines : int
            Total number of active (on) machines across all operational users.
        players_proportion : dict
            Stores the user names with their respective proportional mining power, relative to the number of active machines.
        players_cum_prop : dict
            Stores the cumulative sum of the proportion mining power of each users.
        
        Returns
        -------
        str
            The name of the winning user. If the pooled mining group wins, 'pooled' is returned, instead of the users
            involved in the mining pool.

        Restrictions
        ------------
        - This method can only be called after the `create_logs` method has been called, as the
        `user_activity_log` attribute is initialized in the `create_logs` method.
        '''

        # base number of machines in the pool
        self.base_pooled_mach = base_pooled_mach
        # an attribute for the list of UserAccount objects of opeartional users
        self.list_operational_users = list_operational_users

        # store the total number of machines (including active and inactive machines)
        self.total_machines = self.base_pooled_mach
        # create a dictionary to store the players (i.e. users with machines that are turned on) with their respective computing power
        self.mining_players = {'pooled': self.base_pooled_mach}
        for user in list_operational_users:
            # update the total number of machines
            self.total_machines += user.machines

            # users with machines switched off
            if user.machine_status == 'off':
                # ignore the user
                pass
            # active users with solo mining type
            elif user.mining_type == 'solo':
                # participate as an individual player
                self.mining_players[user.name] = user.machines
            # active users with pooled mining type
            elif user.mining_type == 'pooled':
                # participate as part of a mining pool
                self.mining_players['pooled'] += user.machines

        # compute the total number of active machines (turned 'on')
        self.active_machines = 0
        for user_name, n_machines in self.mining_players.items():
            self.active_machines += n_machines

        # store proportion of players mining power
        self.players_proportion = {}
        # compute the proportion of players mining power
        for player_name, n_machines in self.mining_players.items():
            self.players_proportion[player_name] = n_machines/self.active_machines

        # store cumulative proportion of players mining power
        self.players_cum_prop = {}
        # compute the cumulative proportion of mining power
        running_prop = 0
        for player_name, prop in self.players_proportion.items():
            running_prop += prop
            self.players_cum_prop[player_name] = running_prop

        # random number generator U ~ (0,1)
        rng = random.uniform(0,1)

        # declare the winner
        prev_cum_prop = 0
        for player_name, cum_prop in self.players_cum_prop.items():
            if rng > prev_cum_prop and rng < cum_prop:
                # define the winning player
                player_winner = player_name

                # total daily prize
                total_prize = 100

                # distribute prize when mining pool wins
                if player_winner == 'pooled':
                    # players and their respective active machines in the pool
                    pooled_players = {}
                    
                    # avoid the loop when there are no active users in the pool (to improve performance)
                    if self.mining_players['pooled'] == self.base_pooled_mach:
                        pass
                    else:
                        # extract the number of active machines for each pooled players 
                        for user in self.list_operational_users:
                            if user.mining_type == 'pooled' and user.machine_status == 'on':
                                pooled_players[user.name] = user.machines

                    # distribute prize to the players in the pool
                    for player_name, n_machines in pooled_players.items():
                        # compute the prize attributable to player
                        partial_prize = n_machines/self.mining_players['pooled'] * total_prize

                        # update users' SDPA balance
                        for user in self.list_operational_users:
                            if user.name == player_name:
                                # update user's SDPA balance 
                                user.sdpa_balance += partial_prize
                                # update activity log
                                self.user_activity_log[user.name][f'Day {current_day}']['Prize'] = partial_prize

                # distribute prize when solo miner wins
                else:
                    # update user's SDPA balance
                    for user in self.list_operational_users:
                        if user.name == player_winner:
                            user.sdpa_balance += total_prize

                    # update activity log
                    self.user_activity_log[player_name][f'Day {current_day}']['Prize'] = total_prize

                # return the winner and prize
                return player_winner
            
            else:
                # update prev_cum_prop
                prev_cum_prop = cum_prop