import urllib
import urllib.request
import urllib.parse
import json
import sys

'''
0)Coinmarketcap will CHANGE their API by the end of the year??...
1)Καλό feature θα ήταν να δίνεις και τιμή που το αγόρασες (μέσο όρο.. ενδεικτικά αν δε ξερεις) και να σου λέει πόσο % Πάνω είσαι...κάτι τέτοιο. 
2)Na deixnei metavoli timis % gia 24h i 7days....uparxei idi sto json apo coinmarketcap
3)Another feature would be to ask for important coins and color them
4)Another feature would be to ask a base coin and add a separator line above/below the base coin
'''


null = 0

currency=""
coin=""
price=0
coinId=""
circSupply=0
totalSupply=0
maxSupply=0

total_value=0

global keys_to_sort
keys_to_sort=["price","totalvalue","circsuppply","prccircsupply","totalsupply","prctotalsupply","maxsupply","prcmaxsupply"]

# Coin name must be exactyl as it is in coinmarketcap page: https://coinmarketcap.com
coins_list = {
    'Ethereum': 50,
    'Bitcoin': 0.5,
    'Aeternity': 1800,
    'Stellar': 8800,
    'PIVX': 1450,
    'EOS': 249.8,
    'Dash': 7.5,
    'Lisk': 390,
    'Tezos': 600,
    'Basic Attention Token': 2592.1,
    'Waves': 211.3,
    'Ethereum Classic': 43.8,
    'SONM': 6300,
    'Particl': 155,
    'TaaS': 400,
    }

def initialize(dictofcoins):
   for coin in dictofcoins:
      dictofcoins[coin]=[dictofcoins[coin]]
      dictofcoins[coin].extend(['price','totalvalue','circsuppply','prccircsupply','totalsupply','prctotalsupply','maxsupply','prcmaxsupply'])
initialize(coins_list)

def sort_based_on(dictionary,index):
   list_to_sort=sorted(dictionary.items(), key=lambda e: e[1][index])          # Sorted return a list of Tupples
   list_to_sort.reverse()                                                      # Keep it as tupple and reverse it so that greater numbers come at the top                                         
   return dict(list_to_sort)                                                   # Convert back to dictionary

# Ask user which is the key to sort
for key in keys_to_sort:
   print(keys_to_sort.index(key)+1,")",key)

print("-"*25)
key_to_sort = input("Please choose the key to use for descending sorting: ")   # This returns string in Python 3
key_to_sort = int(key_to_sort)                                                 # This is the index of the key in the list "keys_to_sort"
print("\n"*1)
print("Reading...")
print("\n"*1)

# https://api.coinmarketcap.com/v2/ticker/?convert=EUR&start=1&sort=rank&limit=100
# https://api.coinmarketcap.com/v2/global/

request="https://api.coinmarketcap.com/v2/listings/"
coin_ids=json.loads(urllib.request.urlopen(request).read())                    # Convert (.loads) from Python string when read, to dictionary

def getcoinmarketcapID(coin):
   for dictentry in range(0,len(coin_ids['data'])+1):
      if coin_ids['data'][dictentry]['name'] == coin:
         return coin_ids['data'][dictentry]['id']

print("{:<21} {:^8}  {:^8}  {:^12} {:^16} {:^16} {:^16} {:^16} {:^16} {:^16}".format("Name","Coins","Price","Value(EUR)","Circ supply","% Circ supply","Tot supply","% Tot supply","Max supply","% Max supply"))
print("-"*155)

for coin in coins_list:
   coinId=getcoinmarketcapID(coin)
   
   CoinDataCoinmarketcap="https://api.coinmarketcap.com/v2/ticker/"+str(coinId)+"/?convert=EUR"
   # Turn the string returned from urllib.request.urlopen to python dictionary with .loads method
   coinData=json.loads(urllib.request.urlopen(CoinDataCoinmarketcap).read())

   circSupply=coinData['data']['circulating_supply']
   totalSupply=coinData['data']['total_supply']
   maxSupply=coinData['data']['max_supply']

   price=format(coinData['data']['quotes']['EUR']['price'],'.3f')

   coins_list[coin][0]                                                                # "Coin"
   coins_list[coin][1]=float(price)                                                   # "Price"
   coins_list[coin][2]=int(float(coins_list[coin][0])*float(price))                   # "Value"
   
   if circSupply != None:
      coins_list[coin][3]=float(circSupply)                                           # "Circ supply"
      percentageOfCircSupply=coins_list[coin][0]/circSupply
      coins_list[coin][4]=float(format(percentageOfCircSupply, '.10f'))               # "% Circ supply"
   else:
      coins_list[coin][3] = 0
      coins_list[coin][4] = 0
  
   if totalSupply != None:
      coins_list[coin][5]=float(totalSupply)                                          # "Tot supply"
      percentageOfTotalSupply=coins_list[coin][0]/totalSupply
      coins_list[coin][6]=float(format(percentageOfTotalSupply, '.10f'))              # "% Tot supply"
   else:
      coins_list[coin][5] = 0
      coins_list[coin][6] = 0

   if maxSupply != None:
      coins_list[coin][7]=float(maxSupply)                                            # "Max supply"
      percentageOfMaxSupply=coins_list[coin][0]/maxSupply
      coins_list[coin][8]=float(format(percentageOfMaxSupply, '.10f'))                # "% Max supply"
   else:
      coins_list[coin][7] = 0
      coins_list[coin][8] = 0

# "Name",["Coins","Price","Value","Circ supply","% Circ supply","Tot supply","% Tot supply","Max supply","% Max supply"]

sorted_list=sort_based_on(coins_list,key_to_sort)

for coin in sorted_list:
    print("{:<21}| {:>8}| {:>9,.3f}| {:>8,}| {:>16,.0f}| {:>14.8%}| {:>17,.0f}| {:>14.8%}| {:>17,.0f}| {:<14.8%}".format(coin,sorted_list[coin][0],sorted_list[coin][1],sorted_list[coin][2],sorted_list[coin][3],sorted_list[coin][4],sorted_list[coin][5],sorted_list[coin][6],sorted_list[coin][7],sorted_list[coin][8])) 
    total_value=total_value+sorted_list[coin][2]    

print("-"*155)
print("Total value: {:>39} euros".format(total_value))
