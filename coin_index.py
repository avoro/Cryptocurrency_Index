"""
Cryptocurrency Index
Creates an index for top n cryptocurrencies.
The index is price weighted - similar to DJIA.
Library: coinmarketcap
https://coinmarketcap.com/api/
"""
import json
import re
import time
from time import gmtime, strftime
import numpy as np
import datetime
import matplotlib.pyplot as plt
from coinmarketcap import Market
market = Market()

# list of cryptocurrencies (names) included in the index
coin_lib = []

# list of corresponding prices
coin_prices = []

# tracking index price
index_prices = []

# track time
index_time_tracking = []

# obtains coin ids for easy JSON parsing
# returns a list of coin ids
def get_current_coin_ids(market, n):
    # list of coin ids (used for JSON parsing)
    coin_ids = []
    # find which coins are top n and get their ids
    while n != 0:
        # load coin data
        coin_data = market.ticker(start=n, limit=1)
        # collect coin ids which change in their position
        raw_coin_id = str(coin_data["data"]).split()[0]
        coin_id = re.findall("\d+", raw_coin_id)
        # process coin
        coin_ids.append(coin_id)
        n -= 1
    return coin_ids

# builds a price-weighted index
# returns current index price
def build_index(market, coin_ids, n, coin_lib, coin_prices, index_prices, index_time_tracking):
    total = 0
    base = n
    for id in coin_ids:
        coin_data = market.ticker(start=n, limit=1)
        c_id = ''.join(id)
        coin_lib.append(coin_data['data'][c_id]['name'])
        price = coin_data['data'][c_id]['quotes']['USD']['price']
        coin_prices.append(price)
        total += price
        n -= 1
    # add index to the list of index prices
    index_prices.append(total/base)
    # index_time_tracking.append((datetime.datetime.now().time()).isoformat())
    # add unix timestamp to the list of index time tracking
    index_time_tracking.append(strftime("%H:%M", gmtime()))
    return (total/base)

# display index composition in console
def display_index_composition(n):
    print("The current index is composed of " + str(n) + " crypto-assets: ")
    for coin in coin_lib:
        print(coin + " ")

# display index composition as a bar graph
def build_graph(coin_lib, coin_prices, current_index):
    plt.ion()
    y_pos = np.arange(len(coin_lib))
    plt.bar(y_pos, coin_prices, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, coin_lib)
    plt.ylabel("Price")
    plt.xlabel("Crypto Asset")
    plt.title("Index Composition of $" + str(current_index))
    plt.pause(5)

# prompt the user for displaying index composition through the bar graph
def prompt_display(coin_lib, coin_prices, index):
    to_display = raw_input("Would you like to display the composition: (Y/N) ")
    while to_display != ("Y") and to_display != ("N"):
        print("Please enter your answer in a form of (Y/N): ")
        to_display = raw_input("Would you like to display the composition: (Y/N) ")
    if to_display == ("Y"):
        build_graph(coin_lib, coin_prices, index)

# display graph for tracking the index
def build_graph_index(index_time_tracking, index_prices):
    plt.ion()
    plt.plot(index_time_tracking, index_prices, color = "red", marker = 'o')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Index Price', fontsize=14)
    plt.title("Cryptocurrency Index", fontsize=14)
    plt.grid(True)
    plt.pause(5)


# Prompt user for the number of cryptocurrencies to include
base = input("Enter the number of cryptocurrencies to include in the index: ")

while(base < 3 or base > 20):
    print("The number of cryptocurrencies to be included in the index must be greater than 2 and less than 21.")
    base = input("Enter the number of cryptocurrencies to include in the index: ")

print("Calculating the price-weighted index of " +  str(base) +  " cryptocurrencies")

# Get the index composition data
# load coin ids (used for parsing JSON)
init_coin_ids = get_current_coin_ids(market, base)
# compose the index
init_index = build_index(market, init_coin_ids, base, coin_lib, coin_prices, index_prices, index_time_tracking)
# display the composition
display_index_composition(base)
print("The current price for the index is: $" + str(init_index))

# Display the composition in a bar chart form
prompt_display(coin_lib, coin_prices, init_index)

# Keep track of index
# close existing graphs
plt.close()
i = 0
# track for one hour
while i != 19:
    # wait 3 minutes before updating the index
    time.sleep(180)
    # load coin ids
    cur_coin_ids = get_current_coin_ids(market, base)
    # coin ids match
    if init_coin_ids == cur_coin_ids:
        # compose the index
        coin_prices[:] = []
        coin_lib[:] = []
        cur_index = build_index(market, cur_coin_ids, base, coin_lib, coin_prices, index_prices, index_time_tracking)
        print("Now tracking index movement")
        print("The current price for the index is: $" + str(cur_index))
        # print(index_prices)
        # print(index_time_tracking)
        build_graph_index(index_time_tracking, index_prices)
    else:
        # index composition has changed so it needs to be reconfigured
        print("IMPORTANT: The index composition has changed")
        print("Reconfiguring the index")
        coin_prices[:] = []
        coin_lib[:] = []
        init_coin_ids = cur_coin_ids
    i += 1










