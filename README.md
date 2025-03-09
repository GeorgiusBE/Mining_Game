## Blockchain Simulation
### Project overview
This project simulates a blockchain mining game of a cryptocurrency called SDPA coin. Users will start with an initial capital of 50,000 GBP, and they will be tasked to manage assets, handle market dynamics, and mine SDPA coins, with the ultimate goal of gaining as much returns as possible.

The simulation starts with setting up the simulation environment, where the number of users (minimum of 2), days in the simulation (minimum of 7), and the name of the users are specified. Then all users will be handed an initial capital of 50,000 GBP.

At the start of each day in the simulation, the market price of SDPA coin and per unit of electricity (i.e. the electricity cost of running an ASIC machine for the day) are generated.
- Market price of SDPA coin: It is based on a random walk with an initial price of 50 GBP, and the daily returns are drawn from Normal distribution with of mean 0.01 and std. 0.005.
- Market price of one unit of electricity: It is drawn from a Uniform distribution with a lower bound of 1.5 and an upper bound of 3.5.

After prices have been generated, each user is provided with a menu where they choose the actions they want to perform. There are 5 options to choose from,
1. Purchase mining machines
2. Sell SDPA coins
3. Switch ASIC on/off
4. Switch solo/pooled mining
5. End action

There are some rules that the users have to follow,
- The maximum number of machines to be purchased on any single day is 10.
- Short-selling is not allowed.

At the end of each day, prize is distributed to the winning user/s, users are charged with electricity bill, and users’ capital balance are checked.
- Prize distribution: The total daily prize is set at 100 SDPA coins, and the daily winner is chosen at random. The probability of winning is proportional to the mining power (i.e. the number of machines they own). A user can either be a solo miner or be a part of a mining pool, where there are 1000 active machines in the mining pool at any given day. If a user with solo mining type wins, they will receive the whole daily prize. If the pool wins, users in the pool will be receive a portion of the total daily prize, based on their mining power relative to the aggregate mining power in the pool.
- Electricity bill: It is only charged to users who have their machines turned on. The amount they pay is equal to the product of the number of machines they own and the per unit market price of electricity for the day.
- Capital balance check: After electricity bill has been charged and prize has been distributed, every user’s capital balance is checked to ensure that it is not negative. If it is found to be in deficit, the user’s SDPA coins will be automatically sold, such that the capital is no longer negative. If the user has insufficient SDPA coins, the user will be declared bankrupt. Bankrupt users (including their machines) will immediately be removed from the simulation.

Each action performed is stored in a log, enabling the creation of a daily summary that consolidates and reports the activities performed during the day. 
The simulation ends either when the pre-specified number of days have been reached or all users have gone bankrupt, whichever comes first. Then end-of-simulation summary will be printed, where users can learn about their performance during the whole simulation, including total assets value, investment returns, mining performance, and key actions performed.

### Instructions to run the simulation
1.	The `market.py`, `user_account.py`, and `blockchain.py` files need to be in the same directory as `main.py`.
2.	Open Command Prompt and change directory to where `main.py` is located.
3.	Run the `main.py` script in the Command Prompt by entering,
    > python main.py

### Description of code design
The project follows a modular and object-oriented design to ensure scalability and ease of understanding.
The key components of the code are as follows,
(The details on the content of the each files will be provided in later section.)
- Main Application (main.py file)

    It acts as the entry point that orchestrates all of the classes. It is responsible in initializing the application, managing the simulation loop, and dealing with user interactions.
- UserAccount Class (user_account.py file)

    All of user related functionality are centralized and encapsulated in this class. This includes processing actions and manage user’s data. It includes the `action_query` method that is used to route user’s chosen action to the appropriate method.
- Blockchain Class (blockchain.py file)

    The blockchain mining logic is encapsulated in this class. It contains the method to determine the winning miner and distribute prizes to the winners. Moreover, this class also stores all user actions, ensuring organized storage of all user actions during the simulation.
- Market Class (market.py file)

    It centralizes the generation of the market price of coin and electricity. This ensures consistent pricing mechanisms during the simulation.

Key features of the code design,
- Modularity, Encapsulation, and Centralization

Each core functionality, including user data management, price generation, and blockchain mining logic, is encapsulated in separate classes, and their internal details are hidden from the main.py file. This ensures a clear separation of concerns, maintains encapsulation, and centralization.
- Scalability

The design facilitates scalability by allowing easy extension of features. For example, new action types can be added by creating additional methods within the UserAccount class.
- Error Handling

Input validation and error handling mechanisms are implemented throughout the code to ensure the application can handle invalid actions or inputs. For example, error messages are raised when an invalid input is provided, and user will be guided to correct their invalid input.


### Description of files, classes, and method
**market.py**
This file contains the `Market` class. Its role is to randomly generate the market price of SDPA coin and electricity. These prices play a crucial role in users’ decision. For example, users would only turn on their machines when the electricity price is relatively cheap.
The `Market` class contains 3 methods,
- `__init__()`

    Initializes the `Market` class by setting the initial price of SDPA coin to 50 GBP.
- `new_sdpa_price()`

    Generates new SDPA market price. It does so by randomly generate the coin’s return from a normal distribution with N~(0.01, 0.005), and is then applied to yesterday’s market price. 
- `new_elec_price()`

    Generates the market price of one unit of electricity. The price is randomly generated from uniform distribution with U~(1.5, 3.5). 

**blockchain.py**
This file defines the `BlockChain` class. Its primary role is to simulate blockchain mining. It will determine the winning user/s and distribute the prize accordingly. Moreover, logs that are used to stored users’ activities are initialized in the `BlockChain` class.
The `BlockChain` class contains 3 methods,
- `__init__()`

    Initializes the `BlockChain` class. It defines an attribute to store the number of days in the simulation.
- `create_logs()`

    Generates 2 log: (i) User activity log: To record the activity of each user, separated by days, and (ii) Bankruptcy log: To record the names of users who went bankrupt and the day they went bankrupt.
- `winner()`

    Determines the daily winner/s and distribute the daily prize accordingly. As mentioned before, users can get involved in mining activity as either a solo miner or as part of a mining pool. This method computes the probability of winning for each solo miner and the mining pool, where the probability of winning is proportional to the mining power. After that, the winner is randomly selected based on the previously generated probabilities.
    The prize is then distributed to the winner/s. If a solo miner is the winner, that user will receive the full daily prize of 100 SPDA coins. If the mining pool wins, users in the pool will be receive a portion of the total daily prize, based on their mining power relative to the aggregate mining power in the pool.

**user_account.py**
This file contains the `UserAccount` class. Its main role is to store user data and update it based on the user’s chosen actions during the blockchain mining simulation.
The `UserAccount` class contains 9 methods, 
- `__init__()`

    Initializes the `UserAccount` class. It defines attributes to store user’s data. These include the user’s name, capital, SDPA coin balance, number of machines owned, mining status (on/off), mining type (solo/pooled), and bankruptcy status.
- `reset_daily_machine_purchases()`

    Resets the count of the number of machines purchased for the day. Its intented use is to ensure that the user does not exceed the daily purchase limit of 10 ASIC machines.
- `buy_machines()`

    Handles the purchase of ASIC machines. It ensures that the purchase quantity is a positive integer value, the user is within the daily purchase limit, and has sufficient capital to finance the purchase. Once it has been verified, the user’s capital balance and number of machines owned are updated.
- `sell_sdpa()`

    Handles the sale of SDPA coins. It ensures that the specified sale quantity is a positive numeric value and the user has sufficient SDPA coin balance for the specified sale quantity (i.e. prevent short-selling). Once it has been verified, the user’s SDPA coin balance and capital are updated.
- `machine_swith()`

    Toggles the machine status between 'on' and 'off'. It also prevents switching if no machines are owned.
- `change_mining_type()`

    Toggles the mining type between 'solo' and 'pooled'. It also prevents switching if no machines are owned.
- `action_query()`

    Links user’s chosen action to the relevant method and records the chosen action in the user activity log. For example, if a user chooses to purchase ASIC machines, this method routes the request to the `buy_machines()` method and logs the purchase activity.
- `electricity_bill()`

    Computes total electricity bill based on the number of active machines and the market price of electricity, then deducts the user's capital balance and record the electricity expense in the user activity log.
- `bankrupt_check()`

    Checks the user’s capital. If the capital is negative, SDPA coins will be automatically sold, such that the capital is no longer negative. If the user has insufficient SDPA coins, the user is declared bankrupt (i.e. the user and the user’s machines are taken out of the simulation).
    Then updates the user activity log for any automatic sale of SDPA coins and the bankruptcy log if the user has declared bankruptcy.

**main.py**
This file serves as the orchestrator between the market.py, user_account.py, and blockchain.py files, creating a simulation of SDPA coin mining where users are tasked to manage assets, handle market dynamics, mine SDPA coins, and ultimately to maximize returns.
This file contains 5 user-defined function,
- `get_valid_input()`

    Prompts user for an input and ensures that the input is a positive integer that is greater than a specified value (defined under the `min_val` parameter).
- `daily_summary()`

    Computes the daily paper profit and daily net spending for all users who are still operational (i.e. not bankrupt). For a given user, these two metrics are computed as follows,
    - Daily Paper Profit

        Assuming that the depreciation expense of the machines is zero,
        Daily Paper profit = Prize received * SDPA market price - Electricity bill
    - Net spending

        Net spending = Quantity of SDPA coins sold * SDPA market price - Quantity of machines purchased * Price of a machine - Electricity bill
        It also prints the daily summary results for all operational users. The summary includes: Paper profit (GBP), Net spending (GBP), Prize received (SDPA coins), Number of SDPA coins sold (SDPA coins), Electricity bill (GBP), and Number of ASIC machines purchased.
- `print_actions()`

    Utilizes data stored in the user activity log to print a user’s key actions taken throughout the simulation.
- `total_mined_and_bill()`

    Utilizes the data stored in the user activity log to aggregate the prizes won and electricity bill paid by a user.
- `print_user_summary()`

    Prints an end of simulation performance summary for a user. There are 2 different styles of summary are created,
    - For users who did not go bankrupt
        Prints the final cash capital balance, SDPA coin balance (in units and GBP terms), number of ASIC machines owned, total assets value, investment returns (in GBP terms and % terms), total coins mined, mining performance, total electricity bill, and key actions performed.
    - For users who went bankrupt
        Prints a similar summary to the above, except for cash capital balance, SDPA coin balance, total asset value and investment returns, as these values are either equal to zero or -100%.

### Design debates
- Routing users action requests

    When a user chooses an action, this action needs to be ‘delivered’ to the appropriate method. For example, if a user chooses to purchase ASIC machines, that request needs to be delivered to the buy_machines() method in the user_account.py file. The choice was to either write a code in the main.py file or create a new method within the UserAccount class to deliver the request. I decided with the latter because (i) it helps to reduce clutter in main.py file, (ii) it keeps main.py file focused on orchestrating high-level interactions between the classes while UserAccount class manages all user-specific behaviors, (iii) centralizing the logic within the UserAccount class helps to maintain and debug the code. (iv) Improves the scalability as it will be easier to add more functionalities in the future.

- Storing user data

    I debated on whether to store all user activity data in a single centralized "giant" log or to store different actions in separate logs. I ultimately decided to centralize the data in one log because it helps to simplify the management of user activity data, as it reduces the risk of inconsistencies. Moreover, a centralized log helps to facilitate future expansions. For example, if new actions are added, these actions can be integrated into the existing log structure, rather than needing to create new logs. 

- Charging electricity bill

    The appropriate logic is to receive the price first, and then followed by paying electricity bill. So in the case that the user wins, the user can avoid from having a negative capital balance all together.
    However, I do it the other way around. Pay for electricity, and followed by receiving the prize. But, due to my code design on how I check for bankruptcy / negative capital balance, it does not make a difference which one is performed first. This is because I created a method called bankrupt_check() in the user_account.py to check for negative balance, automatically sell SDPA coins (when appropriate), and declare bankruptcy (when appropriate). With a centralized check like this, a user can temporatily have a negative balance, but as long as they have sufficient SDPA coins, they won’t be declared bankrupt. In a nutshell, as long as charging electricity bill and prize distribution (regardless of the order) are performed before bankrupt_check(), I will get the desired result.
    The benefit of doing it this way is to improve the code performance and reduce clutter in the main.py file as I don’t need to create a `for` loop in the main.py file.
 
- Automatic sale of SDPA coins

    If electricity bill causes the balance of the user to turn negative, their SDPA holdings will automatically be sold at the end of the day at the day’s market price, just enough so that the person’s balance is no longer negative.  For example, if current balance is -$200 and the current price of SDPA coin is $60, the number of coins that needed to be sold is, 200/60 = 3.33 coins.
    If the user does not own enough SDPA coins to cover the negative capital. A message will be printed out that says that the person is bankrupt, as well as (i) the user will not be queried anymore and (ii) all of their machines will be taken offline.
