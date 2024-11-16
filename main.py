# import libraries and classes
import random
from market import Market
from user_account import UserAccount
from blockchain import BlockChain

# query for number of days
n_days = int(input('Enter number of days in the simulation: '))
# query for number of users
n_users = int(input('Enter number of users in the simulation: '))

# list of all users
lst_users = []
for i in range(n_users):
    # query for user names
    name = input(f'Enter the name of User {i + 1}: ')
    user = UserAccount(name)
    lst_users.append(user)

# create Market object
market = Market()

# list of operational (non-bankrupt) users
oper_users = lst_users

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
    for user in oper_users:
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
        
    # create BlockChain object
    sdpa_blockchain = BlockChain(oper_users)

    # print total number of machines today
    print(f'Total number of ASIC machines: {sdpa_blockchain.total_machines}')

    # print end-of-day winner/s and the prize distributed
    day_winners = sdpa_blockchain.winner()
    print(f'{day_winners[0].capitalize()} wins PoW mining.')
    
    # distribute prize to the winner/s
    print('Prize distribution:')
    if not day_winners[1]: # if there is no winner (i.e. the pool wins with no players in the pool)
        print('No SDPA coins were distributed to users.')
    else: # if there is a winning player/s
        for player, prize in day_winners[1].items():
            # print the distributed prize)
            print(f'{player.capitalize()} receives {prize} SDPA coins.')

    # electricity bill record
    all_bills = {}
    # record electricity bill
    for user in oper_users:
        # update electricity bill record
        all_bills[user.name] = user.electricity_bill(elec_price_tdy)

    # print electricity bill
    print('Electricity bill:')
    if all([value is None for value in all_bills.values()]): # when no 
        print('No electricity bill.')
    else:
        for user, bill in all_bills.items():
            print(f'{user.capitalize()} pays {bill} GBP.')

    # check for bankruptcy
    for user in oper_users.copy():
        user.bankrupt_check(sdpa_price_tdy)
        # remove bankrupt users from list of operational users
        if user.bankrupt_status == 'yes':
            oper_users.remove(user)

    # stop the loop when all users are bankrupt
    if not oper_users:
        break