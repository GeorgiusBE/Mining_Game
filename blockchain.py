class BlockChain:
    def __init__(self, user_config):
        '''
        user_config -> (Dict of lists) user_name(str) : [mining_type(str of either 'solo' or 'pooled'), number of machines]
        '''
        self.user_config = user_config

        # create a distionary to store the mining players
        self.mining_players = {'pooled':1000}
        for user,config in user_config:
            # users with solo mining type
            if config[0] == 'solo':
                self.mining_players[user] = config[1]
            # users with pooled mining type
            elif config[0] == 'pooled':
                self.mining_players['pooled'] += config[1]
