# import libraries and classes
import random
from market import Market
from user_account import UserAccount

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

    # loop through each defined users
    for u in range(n_users):
        user = lst_users[u]
        # print current status of user
        print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}.')

        # prompt the user with the query until action 5 is chosen
        while True:
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

            # short selling is not allowed
            elif (user.sdpa_balance == 0 and action == 2):
                # ######################## [TBC enter error message] ###############################################
                pass

            # perform the specified action
            user.action_query(action, sdpa_price_tdy)
            
            # print current status of user
            if user.machines != 0:
                print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}; mining status = ({user.machine_status}, {user.mining_type}).')
            elif user.machines == 0:
                print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}.')


        
