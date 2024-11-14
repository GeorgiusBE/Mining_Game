class BlockChain:
    def __init__(self, user_config):
        '''
        user_config -> (Dict of lists) user_name(str) : [machine status ('on'/'off'), mining_type(str of either 'solo' or 'pooled'), number of machines]
        '''
        self.user_config = user_config

        # create a dictionary to store the (mining) players
        self.mining_players = {'pooled':1000}
        for user_name,config in user_config:
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