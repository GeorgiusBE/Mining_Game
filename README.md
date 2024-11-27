# PS24737_SEMTM0028
## Part 1 (Blockchain Simulation)
### Project Overview
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

## Part 2 (Data Analysis on NVDA stock data)
