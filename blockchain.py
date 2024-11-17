import random

class BlockChain:
    def __init__(self, n_days):
        # create winners log
        '''
        n_days -> total number of days
        '''
        # store the number of days in the simulation
        self.n_days = n_days
        # template for winners log
        self.winners_log = {f'Day {n}' : {} for n in range(1, n_days+1)}

   # create activity log
    def create_user_activity_log(self, lst_users):
        '''
        n_days -> total number of days
        lst_users -> list of UserAccount objects
        '''
        # blank activity log
        self.user_activity_log = {}
        for user in lst_users:
            self.user_activity_log[user.name] = {f'Day {n}': {f'Action {i}': [] for i in range(1,5)} for n in range(1, self.n_days+1)}
        return self.user_activity_log
    
    # determine the end-of-day winner
    def winner(self, list_operational_users, current_day):
        '''
        list_operational_users -> list of users (in the form of UserAccount class objects) that are operational (not bankrupt).
        current_day -> the current day (int)
        '''
        # base number of machines in the pool
        self.base_pooled_mach = 1000
        # create an attribute for the list of UserAccount objects
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

                    # store the winner's name their prize
                    dist_prize = {}
                    # distribute prize to the players in the pool
                    for player_name, n_machines in pooled_players.items():
                        # compute the prize attributable to player
                        partial_prize = n_machines/self.mining_players['pooled'] * total_prize
                        
                        # update dist_prize
                        dist_prize[player_name] = partial_prize

                        # update users' SDPA balance
                        for user in self.list_operational_users:
                            if user.name == player_name:
                                user.sdpa_balance += partial_prize
                    
                    # update winners log
                    self.winners_log[f'Day {current_day}'] = dist_prize

                # distribute prize when solo miner wins
                else:
                    # update user's SDPA balance
                    for user in self.list_operational_users:
                        if user.name == player_winner:
                            user.sdpa_balance += total_prize
                    # store the winner's name their prize
                    dist_prize = {player_winner:total_prize}

                # return the winner and prize 
                return player_winner, dist_prize
            
            else:
                # update prev_cum_prop
                prev_cum_prop = cum_prop