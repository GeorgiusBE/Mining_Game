import random

class BlockChain:
    def __init__(self, user_config):
        '''
        user_config -> (Dict of lists) user_name(str) : [machine status ('on'/'off'),
                                                         mining_type(str of either 'solo' or 'pooled'),
                                                         number of machines]
        '''
        # base number of machines in the pool
        self.base_pooled_mach = 1000
        # users machine configurations
        self.user_config = user_config

        # compute total number of machines (including active and inactive machines)
        self.total_machines = self.base_pooled_mach
        # create a dictionary to store the players (i.e. users with machines that are turned on)
        self.mining_players = {'pooled': self.base_pooled_mach}
        for user_name,config in user_config.items():
            # update the total number of machines
            self.total_machines += config[2]

            # users with machines switched off
            if config[0] == 'off':
                # ignore the user
                pass
            # active users with solo mining type
            elif config[1] == 'solo':
                # participate as an individual player
                self.mining_players[user_name] = config[2]
            # active users with pooled mining type
            elif config[1] == 'pooled':
                # participate as part of a group
                self.mining_players['pooled'] += config[2]

    # determine the end-of-day winner
    def winner(self):
        # compute the total number of active machines
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
                # the winning player
                player_winner = player_name

                # total daily prize
                total_prize = 100

                # distribute prize for player/s in mining pool
                if player_winner == 'pooled':
                    # players and their respective active machines in the pool
                    pooled_players = {}
                    
                    # avoid the loop when there are no users in the pool (to improve performance)
                    if self.mining_players['pooled'] == self.base_pooled_mach:
                        pass
                    else:
                        # extract the number of active machines for each pooled players 
                        for user_name, config in self.user_config.items():
                            if config[1] == 'pooled' and config[0] == 'on':
                                # extract the number of machines of the pooled player
                                pooled_players[user_name] = config[2]
                
                    # store distributed prize
                    dist_prize = {}
                    # distribute prize to the players in the pool
                    for player_name, n_machines in pooled_players.items():
                        dist_prize[player_name] = n_machines/self.mining_players['pooled'] * total_prize


                # distribute prize for solo player
                else:
                    dist_prize = {player_winner:total_prize}

                # return the winner and prize 
                return player_winner, dist_prize
            
            else:
                # update prev_cum_prop
                prev_cum_prop = cum_prop