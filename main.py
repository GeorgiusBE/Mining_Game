# import libraries and classes
import random
from market import Market
from user_account import UserAccount
from blockchain import BlockChain

# query for number of days
n_days = int(input('Enter number of days in the simulation: '))
# query for number of users
n_users = int(input('Enter number of users in the simulation: '))

# list of users
lst_users = []
for i in range(n_users):
    # query for user names
    name = input(f'Enter the name of User {i + 1}: ')
    user = UserAccount(name)
    lst_users.append(user)

# create Market object
market = Market()

# dictionary to users' configuration (to be used for the input in BlockChain class)
user_config = {}

# iterate through each day
for i in range(n_days):
    print(f'''Trading Day {i + 1}
------------- ''')
    # print SDPA price for the day
    if i == 0:
        # SDPA price is initially 50 GBP
        sdpa_price_tdy = market.sdpa_price
        print(f'Today\'s market price of SDPA coin is {sdpa_price_tdy} GBP')
    else:
        # SDPA price is updated based on yesterdays's price
        sdpa_price_tdy = market.new_sdpa_price()
        print(f'Today\'s market price of SDPA coin is {sdpa_price_tdy} GBP')
    
    # print electricity price for the day
    elec_price_tdy = market.new_elec_price()
    print(f'Today\'s unit price of electricity is {elec_price_tdy} GBP')

    # iterate through each defined users
    for u in range(n_users):
        user = lst_users[u]
        
        # prompt the user with the query until action 5 is chosen
        while True:
            # print user status when machines owned is not zero
            if user.machines != 0:
                print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}; mining status = ({user.machine_status}, {user.mining_type}).')
            # print user status when user owns zero machine
            else:
                print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}.')
            # query the user with list of actions
            action = int(input('''Select which action to make,
1. Purchase mining machines
2. Sell SDPA coins
3. Switch ASIC on/off
4. Switch solo/pooled mining
5. End action
Enter action number: '''))
            # break the loop if the user chooses to end action
            if action == 5:
                break

            # perform the specified action
            user.action_query(action, sdpa_price_tdy)
        
        # summarize user's status into a dictionary
        user_config[user.name] = [user.machine_status, user.mining_type, user.machines]
    
    # end-of-day winner
    sdpa_blockchain = BlockChain(user_config)
    day_winners = sdpa_blockchain.winner()

    # print end-of-day winner/s and the prize distributed
    print(f'{day_winners[0].capitalize()} wins PoW mining.')

    # update the winners' sdpa coin balance
    print('Prize distribution:')
    for player, prize in day_winners[1].items():
        # print the distributed prize)
        print(f'{player.capitalize()} receives {prize} SDPA coins.')
        
        for user in lst_users:
            # check for matching user name
            if user.name == player:
                # update sdpa balance
                user.sdpa_balance += prize
                break

    # print total number of machines
    print(f'Total number of ASIC machines: {sdpa_blockchain.total_machines}')

    # record electricity bill
    print('Electricity bill:')
    for user in lst_users:
        user_bill = user.electricity_bill(elec_price_tdy)
        if user_bill is not None:
            print(f'{user.name.capitalize()} pays {user_bill} GBP.')