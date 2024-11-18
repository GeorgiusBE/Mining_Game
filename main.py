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
    # set intial cash capital
    intial_capital = 50000
    # create user object
    user = UserAccount(name, intial_capital)
    lst_users.append(user)

# create Market object
market = Market()
# create BlockChain object
sdpa_blockchain = BlockChain(n_days)
# create user activity log
user_activity_log = sdpa_blockchain.create_user_activity_log(lst_users)

# list of operational (non-bankrupt) users
oper_users = lst_users

# iterate through each day
for i in range(n_days):
    current_day = i + 1
    print(f'''Trading Day {current_day}
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
            user.action_query(action, sdpa_price_tdy, current_day, user_activity_log)
  
    # determine the day's winners
    base_pooled_mach = 1000 # base number of machines in mining pool
    total_prize = 100 # SDPA coins distributed per day
    day_winners = sdpa_blockchain.winner(oper_users, current_day, base_pooled_mach, total_prize)
    
    # print total number of machines today
    print(f'Total number of ASIC machines: {sdpa_blockchain.total_machines}')

    # print end-of-day winner/s and the prize distributed
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
        all_bills[user.name] = user.electricity_bill(elec_price_tdy, current_day)

    # print electricity bill
    print('Electricity bill:')
    if all([value is None for value in all_bills.values()]): # when no 
        print('No electricity bill.')
    else:
        for user, bill in all_bills.items():
            if bill:
                print(f'{user.capitalize()} pays {bill} GBP.')

    # check for bankruptcy
    for user in oper_users.copy():
        user.bankrupt_check(current_day)
        # remove bankrupt users from list of operational users
        if user.bankrupt_status == 'yes':
            oper_users.remove(user)

    # stop the loop when all users are bankrupt
    if not oper_users:
        break

# total coins mined by everyone during the simulation
total_prize = total_mined_coins * current_day
print(total_prize + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# summarize simulation results
for user in lst_users:
    # print user's name
    print(user.name + ':')

    # for users that declared bankruptcy
    if user.bankrupt_status == 'yes':
        # print bankruptcy status
        print(f'- {user.name} went bankrupt on day [ENTER DAY!!!!!!!!!!!!!]') #################################
    
    # for users that remian oprational
    else:
        # print final (cash) capital balance
        print(f'- Cash capital balance = {user.capital}')

        # print final SDPA coin balance
        print(f'- SDPA coin balance = {user.sdpa_balance}')
        
        # print dollar value of final SDPA coin balance
        dollar_sdpa_balance = user.sdpa_balance * sdpa_price_tdy
        print(f'- GBP value of SDPA coin balance = {dollar_sdpa_balance}')
        
        # print final number of ASIC machines owned
        print(f'- ASIC machines count = {user.machines}')
        
        # print total GBP value of all assets (assuming the machines' value do not depreciate)
        machine_price = 600 # Price for 1 unit of ASIC machine
        total_assets = user.capital + dollar_sdpa_balance + user.machines * machine_price
        print(f'- Total GBP value of all assets = {total_assets}')

        # print investment return
        init_capital = 50000 # Initial cash capital balance per user
        int_ret_gbp = total_assets - init_capital # GBP investment return
        print(f'- Investment return (GBP) = {round(int_ret_gbp, 2)} GBP')
        inv_ret_pct = (int_ret_gbp)/init_capital * 100 # % investment return
        print(f'- Investment return (%) = {round(inv_ret_pct, 2)}%')

        # total number of coins mined by the user
        user_mined_coins = 0
        for day, winners in sdpa_blockchain.winners_log.items():
            for winner_name, coins in winners.items():
                if winner_name == user.name:
                    user_mined_coins += coins
        # print total number of coins mined by the user
        print(f'- Total coins mined = {user_mined_coins} coins')

        # print mining performance
        mine_performance = user_mined_coins/total_prize * 100
        print(f'- Mining performance (%) = {mine_performance}%')

        # print event summary
        for day, actions in user_activity_log[user.name].items():
            # print the day
            print(day + ':')
            
            for action, param in actions.items():
                # skip the action that was not performed
                if not param:
                    continue
                # print the total number of machines purchased
                elif action == 'Action 1':
                    print(f'- Purchased {sum(param)} ASIC machines.')
                # print the total number of SDPA coin sold
                elif action == 'Action 2':
                    print(f'- Sold {sum(param)} SDPA coins.')
                # print the change in machine status [on/off]
                elif action == 'Action 3':
                    print(f'- ASIC machines are turned {param[-1]}.')
                # print the change in mining type
                elif action == 'Action 4':
                    print(f'- Changed mining type to {param[-1]}.')
                # print the prize distributed
                elif action == 'Prize':
                    print(f'- Received {param} SDPA coins from mining activity.')
                # print elecrticity bill paid
                elif action == 'Electricity':
                    print(f'- Paid {param} GBP on electricity bill.')
                


# print the user activity log
print(user_activity_log)

# print the log of the distributed prize
print(sdpa_blockchain.winners_log)