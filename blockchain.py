import random

class BlockChain:
    def __init__(self, user_config):
        '''
        user_config -> (Dict of lists) user_name(str) : [machine status ('on'/'off'),
                                                         mining_type(str of either 'solo' or 'pooled'),
                                                         number of machines]
        '''

        # create a dictionary to store the (mining) players
        self.mining_players = {'pooled':1000}
        for user_name,config in user_config.items():
            # users with machines switched off
            if config[0] == 'off':
                # no participation
                self.mining_players[user_name] = 0
            # users with solo mining type
            elif config[1] == 'solo':
                # participate as an individual player
                self.mining_players[user_name] = config[2]
            # users with pooled mining type
            elif config[1] == 'pooled':
                # participate as part of a group
                self.mining_players['pooled'] += config[2]

    # determine the end-of-day winner
    def winner(self):
        # daily prize for block chain winner
        prize = 100

        # compute the total number of machines
        total_machines = 0
        for player_name, mining_power in self.mining_players.items():
            total_machines += mining_power

        # store proportion of mining power
        self.players_proportion = {}

        # compute the proportion of mining power
        for player_name, mining_power in self.mining_players.items():
            self.players_proportion[player_name] = mining_power/total_machines
        
        # store cumulative proportion of mining power
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
            # determine the winning player
            if rng > prev_cum_prop and rng < cum_prop:
                player_winner = player_name
                return player_winner
            
            # update prev_cum_prop
            prev_cum_prop = cum_prop