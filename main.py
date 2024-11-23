# import libraries and classes
from market import Market
from user_account import UserAccount
from blockchain import BlockChain

# a function to compute and print daily summary results
def daily_summary(user_activity_log, oper_users, sdpa_price_tdy, current_day, machine_price=600):
    '''
    Compute daily paper profit and daily net spending

    user_activity_log -> (dict) activity log of all users; created in the BlockChain class
    oper_users -> A list of UserAccount class object for users who are still operational (i.e. not bankrupt)
    sdpa_price_tdy -> (float) today's SDPA coin price
    current_day -> (int) the current day
    machine_price -> (float) price of 1 unit of ASIC mahcines
    '''
    # list of user names who are still operational
    oper_user_names = [user.name for user in oper_users]

    # iterate through each operational users
    for user_name in oper_user_names:
        # access the user's actions stored in user_activity_log
        user_actions = user_activity_log[user_name][f'Day {current_day}']
        
        # number of machines purchased
        user_purchase = sum(user_actions['Action 1']) if user_actions['Action 1'] else 0
        # number of coins sold
        user_sold = sum(user_actions['Action 2']) if user_actions['Action 2'] else 0
        # electricity bill paid
        user_elec = user_actions.get('Electricity', 0)
        # prize received
        user_prize = user_actions.get('Prize', 0)

        # compute daily net spending
        user_net_spending = user_sold * sdpa_price_tdy - user_purchase * machine_price - user_elec

        # compute daily paper profit (assuming no depreciation expense from the ASIC machines)
        user_paper_profit = user_prize * sdpa_price_tdy - user_elec

        # print out the daily summary
        print(user_name.capitalize() + ':')
        print(f'    - Paper profit is {user_paper_profit} GBP.')
        print(f'    - Net spending is {user_net_spending} GBP.')
        print(f'    - Prize received is {user_prize} SDPA coins.')
        print(f'    - Number of SDPA coins sold is {user_sold} units.')
        print(f'    - Electrcity bill paid is {user_elec} GBP.')
        print(f'    - Number of ASIC machines purchased is {user_purchase} units.')


# function to print out key actions taken in the simulation
def print_actions(user_activity_log, user_name, action_messages):
    '''
    user_activity_log -> (dict) activity log of all users; created in the BlockChain class
    user_name -> the name of the user
    action_messages -> (dict) key-value pair is represented by the action name and the corresponsing message
    '''
    for day, actions in user_activity_log[user_name].items():
        # print the day
        print(f'    {day}:')

        # track wheter any action is perfomed on the day
        action_indicator = False

        # iterate through the actions and parameters
        for action, param in actions.items():
            # get the message from action_messages
            message = action_messages[action](param)
            # only print when the action was performed
            if message:
                print(message)
                action_indicator = True # update the indicator when action/s are performed on the day
        
        # print message when no actions are performed on the day
        if not action_indicator:
            print('    - No actions performed today.')
        
        # break the loop once the user went bankrupt
        if actions.get('Bankrupt', None) == 'yes':
            break

# function to compute total coins mined and electricity bill of a user in activity log
def total_mined_and_bill(user_activity_log, user_name):
    '''
    user_activity_log -> (dict) activity log that records all events for all users; created in the BlockChain class
    user_name -> name of the user the total is computed for
    '''
    # store total values
    user_mined_coins = 0 # total coins mined
    user_total_bill = 0 # total electricity bill
    # search for the specified user in the log
    for day, actions in user_activity_log[user_name].items():
        # update the total
        user_mined_coins += actions.get('Prize', 0)
        user_total_bill += actions.get('Electricity', 0)
    
    return user_mined_coins, user_total_bill

# function to print user's summary
def print_user_summary(user, sdpa_price_tdy, total_mined_coins, user_activity_log, bankruptcy_log, action_messages, machine_price=600):
    '''
    user -> UserAccount object representing a user
    sdpa_price_tdy -> today's SDPA coin price
    total_mined_coins -> total coin mined by all users and the pool throughout the whole simulation
    user_activity_log -> (dict) activity log that records all events for all users; created in the BlockChain class
    bankruptcy_log -> (dict) a log that records when users went bankrupt; created in the BlockChain class
    action_messages -> (dict) key-value pair is represented by the action name and the corresponsing message
    machine_price -> the price for 1 unit of machine
    '''
    # print user's name
    print(user.name.capitalize() + ':')

    # for users that declared bankruptcy
    if user.bankrupt_status == 'yes':
        # print bankruptcy status
        print(f'- {user.name.capitalize()} went bankrupt on day {bankruptcy_log[user.name]}')

        # print final number of ASIC machines owned
        print(f'- ASIC machines count = {user.machines}')

        # copmute the total coins mined and electricity bill
        user_mined_coins, user_total_bill = total_mined_and_bill(user_activity_log, user.name)

        # print the total number of coins mined
        print(f'- Total coins mined = {user_mined_coins} coins')

        # print mining performance
        mine_performance = user_mined_coins/total_mined_coins * 100
        print(f'- Mining performance (%) = {mine_performance}%')

        # print total electricity bill
        print(f'- Total electricity bill = {user_total_bill} GBP.')

        # print actions summary
        print('- Key actions performed,')
        print_actions(user_activity_log, user.name, action_messages)

    # for users who remain oprational
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
        total_assets = user.capital + dollar_sdpa_balance + user.machines * machine_price
        print(f'- Total GBP value of all assets = {total_assets}')

        # print investment return
            # GBP investment return
        int_ret_gbp = total_assets - initial_capital
        print(f'- Investment return (GBP) = {round(int_ret_gbp, 2)} GBP')
            # % investment return
        inv_ret_pct = (int_ret_gbp)/initial_capital * 100
        print(f'- Investment return (%) = {round(inv_ret_pct, 2)}%')
        
        # copmute the total coins mined and electricity bill
        user_mined_coins, user_total_bill = total_mined_and_bill(user_activity_log, user.name)

        # print the total number of coins mined
        print(f'- Total coins mined = {user_mined_coins} coins')

        # print mining performance
        mine_performance = user_mined_coins/total_mined_coins * 100
        print(f'- Mining performance (%) = {mine_performance}%')

        # print total electricity bill
        print(f'- Total electricity bill = {user_total_bill} GBP.')

        # print actions summary
        print('- Key actions performed,')
        print_actions(user_activity_log, user.name, action_messages)

##################################################################################################################

# indicator to keep track when valid input for the number of days has been provided
n_days_ind = True

# function to obtain valid input
def get_valid_input(prompt, min_val):
    '''
    A function to get an input that is a postiive integer greater than or equal to min_val

    prompt -> (str) Message prompted to the user.
    min_val -> (int) The desired minimum value.

    returns
    -------
    (int) Returns the valid input
    '''
    while True:
        try:
            # query the user
            user_input = input(prompt)

            # ensure the input is user_input >= min_val and is a positive integer
            if user_input.isdigit() and int(user_input) >= min_val:
                return int(user_input)
            # raise error
            else:
                raise ValueError(f'Invalid input: Only positive integer values greater than or equal to {min_val} are accepted.')
        except ValueError as err:
            print(err)

# query for number of days
n_days = get_valid_input('Enter number of days in the simulation (Minimum: 7): ', 7)

# query for number of users
n_users = get_valid_input('Enter number of users in the simulation (Minimum: 2): ', 2)

# set the price for 1 unit of ASIC machine
machine_price = 600
# set intial cash capital
initial_capital = 50000

# list of all users
lst_users = []
for i in range(n_users):
    # query for user names
    name = input(f'Enter the name of User {i + 1}: ')
    # create user object
    user = UserAccount(name, initial_capital)
    lst_users.append(user)

# create Market object
market = Market()
# create BlockChain object
sdpa_blockchain = BlockChain(n_days)
# create winners log, user activity log, and user electricity bill log
user_activity_log, bankruptcy_log = sdpa_blockchain.create_logs(lst_users)

# list of operational (non-bankrupt) users
oper_users = lst_users.copy()

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
        # resets the tracker for daily machine purchases
        user.reset_daily_machine_purchases()

        # prompt the user with the query until action 5 is chosen
        while True:
            # print user status when machines owned is not zero
            if user.machines != 0:
                print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}; mining status = ({user.machine_status}, {user.mining_type}).')
            # print user status when user owns zero machine
            else:
                print(f'{user.name}\'s current balance = {user.capital} GBP; number of SDPA coins = {user.sdpa_balance}; number of ASIC = {user.machines}.')
            
            # query the user with list of actions
            action = input('''Select which action to make,
1. Purchase mining machines
2. Sell SDPA coins
3. Switch ASIC on/off
4. Switch solo/pooled mining
5. End action
Enter action number: ''')

            try:
                # raise error if the input 
                if action not in ['1','2','3','4','5']:
                    raise ValueError('Invalid input: To select the action, please enter 1, 2, 3, 4, or 5.')
                
                # convert the input into integer
                action = int(action)
                
                # break the loop if the user chooses to end action
                if action == 5:
                    break
                
                # perform the specified action
                user.action_query(action, sdpa_price_tdy, current_day, user_activity_log)
            
            except ValueError as err:
                print(err)
    
        # electricity bill payment
        user.electricity_bill(elec_price_tdy, current_day)

    # determine the day's winners
    base_pooled_mach = 1000 # base number of machines in mining pool
    total_prize = 100 # SDPA coins distributed per day
    day_winners = sdpa_blockchain.winner(oper_users, current_day, base_pooled_mach, total_prize)
    
    # print total number of machines today
    print(f'Total number of ASIC machines: {sdpa_blockchain.total_machines}')

    # print end-of-day winner/s and the prize distributed
    print(f'{day_winners.capitalize()} wins PoW mining.')

    # check for bankruptcy
    for user in oper_users.copy():
        user.bankrupt_check(current_day, bankruptcy_log)
        # remove bankrupt users from list of operational users
        if user.bankrupt_status == 'yes':
            oper_users.remove(user)

    # print daily summary
    daily_summary(user_activity_log, oper_users, sdpa_price_tdy, current_day, machine_price=600)

    # stop the loop when all users are bankrupt
    if not oper_users:
        break

# total coins mined by everyone during the simulation
total_mined_coins = total_prize * current_day

# action messages template
action_messages = {
    'Action 1': lambda param: f'    - Purchased {sum(param)} ASIC machines.' if param and sum(param)!=0 else None,
    'Action 2': lambda param: f'    - Sold {sum(param)} SDPA coins.' if param and sum(param)!=0 else None,
    'Action 3': lambda param: f'    - ASIC machines are turned {param[-1]}.' if param else None,
    'Action 4': lambda param: f'    - Changed mining type to {param[-1]}.' if param else None,
    'Prize': lambda param: f'    - Received {param} SDPA coins from mining activity.' if param else None,
    'Electricity': lambda param: f'    - Paid {param} GBP on electricity bill.' if param else None,
    'Bankrupt': lambda param: f'    - Went bankrupt'
}

# print out the simulation summary result
print('''
Simulation Summary
-----------------''')
for user in lst_users:
    print_user_summary(user,
                       sdpa_price_tdy,
                       total_mined_coins,
                       user_activity_log,
                       bankruptcy_log,
                       action_messages,
                       600)



# print the user activity log
print(user_activity_log)

# print bankruptcy log
print(bankruptcy_log)