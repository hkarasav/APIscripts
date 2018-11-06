import urllib
import urllib.request
import urllib.parse
import json
import sys
import colorama
from colorama import Fore
from colorama import Style
from colorama import init

init()   # For colorama
# print(Fore.MAGENTA + "Hello World")
# print(Style.RESET_ALL)


'''
0)Coinmarketcap will CHANGE their API by the end of the year??...
1)WIP...Καλό feature θα ήταν να δίνεις και τιμή που το αγόρασες (μέσο όρο.. ενδεικτικά αν δε ξερεις) και να σου λέει πόσο % Πάνω είσαι...κάτι τέτοιο. 
2)WIP...Na deixnei metavoli timis % gia 24h i 7days....uparxei idi sto json apo coinmarketcap
3)DONE!! Another feature would be to ask for important coins and color them
4)DONE!! Another feature would be to ask a base coin and add a separator line above/below the base coin
'''


null = 0

debug=1
currency="EUR"
coin=""
price=0
coinId=""
circSupply=0
percentageOfCircSupply=0
totalSupply=0
percentageOfTotalSupply=0
maxSupply=0
percentageOfMaxSupply=0
#total_value=0

# Used for clearer understanding of indeces in lists
CONST_COINS_NUMBER   =0
CONST_PURCH_PRICE    =1
CONST_PRICE          =2
CONST_PRC_PURCH_PRICE=3
CONST_PRC_24H_CHANGE =4
CONST_TOTAL_VALUE    =5
CONST_CIRC_SUPPLY    =6
CONST_PRC_CIRC_SUPPLY=7
CONST_TOT_SUPPLY     =8
CONST_PRC_TOT_SUPPLY =9
CONST_MAX_SUPPLY     =10
CONST_PRC_MAX_SUPPLY =11



keys_to_sort=["purchaseprice","price","prcpurchase","prc24h","totalvalue","circsuppply","prccircsupply","totalsupply","prctotalsupply","maxsupply","prcmaxsupply"]
attributes_to_print=[]    # A list of the attributes of each coin to be printed so that the report fits in the console

marked_coins=[]    # A list of the coins to be marked with Magenta

# Coin name must be exactly as it is in coinmarketcap page: https://coinmarketcap.com
coins_dict = {
    'Ethereum': [50,0.2],
    'Bitcoin': [0.5,0],
    'Aeternity': [1800,0.3],
    'Stellar': [8800,0.15],
    'PIVX': [1450,0.4],
    'EOS': [249.8,0],
    'Dash': [7.5,90],
    'Lisk': [390,0.6],
    'Tezos': [600,0.6],
    'Basic Attention Token': [2592.1,0.25],
    'Waves': [211.3,0.4],
    'Ethereum Classic': [43.8,0],
    'SONM': [6300,0],
    'Particl': [155,0],
    'TaaS': [400,1],
    }

def myconsoleprint(text1,text2="",text3=""):
   if debug==1:
       print(text1,text2,text3)

def initialize(dictofcoins):
   for coin in dictofcoins:
#      dictofcoins[coin]=[dictofcoins[coin]]
      dictofcoins[coin].extend(['price','prcpurchase','prc24h','totalvalue','circsuppply','prccircsupply','totalsupply','prctotalsupply','maxsupply','prcmaxsupply'])
   myconsoleprint(dictofcoins)

def sort_based_on(dictionary,index):
   list_to_sort=sorted(dictionary.items(), key=lambda e: e[1][index])          # Sorted return a list of Tupples
   list_to_sort.reverse()                                                      # Keep it as tupple and reverse it so that greater numbers come at the top       
   return dict(list_to_sort)                                                   # Convert back to dictionary

def get_coinmarketcap_ID(coin):
   for dictentry in range(0,len(coin_ids['data'])+1):
      if coin_ids['data'][dictentry]['name'] == coin:
         return coin_ids['data'][dictentry]['id']

def calculate_percentage_change(coin_purchase_price,coin_current_price):
   if coin_purchase_price != 0:
      return int((coin_current_price-coin_purchase_price)/coin_purchase_price) #*100
   else:
      return int(0)

def print_attributes(attr,list_of_coins):
    global total_value
    total_value = 0
    print(Fore.CYAN + "Currency: " + currency)
    print(Style.RESET_ALL)
    print("{:<21}|".format("Name"), end="")
    for i in attr:
       if i == CONST_COINS_NUMBER   : print("{:^7}|".format("Coins"), end="")
       if i == CONST_PRICE          : print("{:^9}|".format("Price"), end="")
       if i == CONST_PRC_24H_CHANGE : print("{:^6}|".format("%24h"), end="")
       if i == CONST_PURCH_PRICE    : print("{:^8}|".format("PPrice"), end="")
       if i == CONST_PRC_PURCH_PRICE: print("{:^9}|".format("%PPrice"), end="")
       if i == CONST_TOTAL_VALUE    : print("{:^8}|".format("Value"), end="")
       if i == CONST_CIRC_SUPPLY    : print("{:^15}|".format("Circ supply"), end="")
       if i == CONST_PRC_CIRC_SUPPLY: print("{:^11}|".format("%Cir supply"), end="")
       if i == CONST_TOT_SUPPLY     : print("{:^15}|".format("Tot supply"), end="")
       if i == CONST_PRC_TOT_SUPPLY : print("{:^11}|".format("%Tot supply"), end="")
       if i == CONST_MAX_SUPPLY     : print("{:^15}|".format("Max supply"), end="")
       if i == CONST_PRC_MAX_SUPPLY : print("{:^11}".format("%Max supply"))
    print("\n"+"-"*145)
    for coin in list_of_coins:
       if coin in marked_coins: print(Fore.MAGENTA, end="")
       if coin == base_coin: print(Fore.YELLOW, end="")
       print("{:<21}|".format(coin), end="")
       for i in attr:
          if i == CONST_COINS_NUMBER   : print("{:>7}|".format(sorted_list[coin][CONST_COINS_NUMBER]), end="")
          if i == CONST_PRICE          : print("{:>9,.3f}|".format(sorted_list[coin][CONST_PRICE]), end="")
          if i == CONST_PRC_24H_CHANGE : print("{:>6.1%}|".format(sorted_list[coin][CONST_PRC_24H_CHANGE]), end="")
          if i == CONST_PURCH_PRICE    : print("{:>8,}|".format(sorted_list[coin][CONST_PURCH_PRICE]), end="")
          if i == CONST_PRC_PURCH_PRICE: print("{:>9,.0%}|".format(int(sorted_list[coin][CONST_PRC_PURCH_PRICE])), end="")
          if i == CONST_TOTAL_VALUE    : print("{:>8,}|".format(sorted_list[coin][CONST_TOTAL_VALUE]), end="")
          if i == CONST_CIRC_SUPPLY    : print("{:>15,.0f}|".format(sorted_list[coin][CONST_CIRC_SUPPLY]), end="")
          if i == CONST_PRC_CIRC_SUPPLY: print("{:>11.8%}|".format(sorted_list[coin][CONST_PRC_CIRC_SUPPLY]), end="")
          if i == CONST_TOT_SUPPLY     : print("{:>15,.0f}|".format(sorted_list[coin][CONST_TOT_SUPPLY]), end="")
          if i == CONST_PRC_TOT_SUPPLY : print("{:>11.8%}|".format(sorted_list[coin][CONST_PRC_TOT_SUPPLY]), end="")
          if i == CONST_MAX_SUPPLY     : print("{:>15,.0f}|".format(sorted_list[coin][CONST_MAX_SUPPLY]), end="")
          if i == CONST_PRC_MAX_SUPPLY : print("{:>11.8%}".format(sorted_list[coin][CONST_PRC_MAX_SUPPLY]))
       print(Style.RESET_ALL)
       total_value=total_value+sorted_list[coin][5]

def handle_base_and_mark(dictionary_with_coins):
   global base_coin
   base_coin=""
   base_is_set=0

   for coin in dictionary_with_coins:
      print(coin,": ", end="")
      action = input("")
      if action=="end":
         myconsoleprint("action is \"end\"")
         myconsoleprint(marked_coins)
         break
      if action=="":
         myconsoleprint("action is \"\"")
         myconsoleprint(marked_coins)
      elif action=="mark":
         myconsoleprint("action is \"mark\"")
         marked_coins.append(coin)
         myconsoleprint(marked_coins)
      elif action=="base":
         myconsoleprint("action is \"base\"")
         if base_is_set==1:
             print("Error: You can only have one base coin")
             break
         base_coin=coin
         base_is_set=1
         myconsoleprint("Base coin: ", base_coin)
         myconsoleprint(marked_coins)

   myconsoleprint(marked_coins)
   check=input("Are all the settings correct?")

def get_user_input(list_of_keys_to_sort):
   global key_to_sort
   global attributes_to_print
   for key in list_of_keys_to_sort:
      print(list_of_keys_to_sort.index(key)+1,")",key)

   print("-"*25)
   key_to_sort = input("Please choose the key to use for descending sorting: ")   # This returns string in Python 3
   key_to_sort = int(key_to_sort)                                                 # This is the index of the key in the list "keys_to_sort"

   attributes_to_print = input("Enter attributes to print. Example \"1,5,8\": ")
   attributes_to_print = attributes_to_print.split(",")
   attributes_to_print = set(attributes_to_print)        # Unordered list with unique elements
   attributes_to_print = list(attributes_to_print)
   attributes_to_print.sort()
   for i in range(0,len(attributes_to_print)):
         attributes_to_print[i]=int(attributes_to_print[i])
   myconsoleprint(attributes_to_print)


print("For each coin declare if you want to mark it with Magenta color by writing \"mark\"")
print("For one coin only declare if you want it as base coin by writing \"base\". Base is used as separator in the report when you use sorting")
print("You do not have to use either \"mark\" or \"base\". You can skip any coin configuration with the enter key")
print("You can end the setup with \"end\"")

initialize(coins_dict)
handle_base_and_mark(coins_dict)
get_user_input(keys_to_sort)

print("\n"*1)
print("Reading...")
print("\n"*1)

# https://api.coinmarketcap.com/v2/ticker/?convert=EUR&start=1&sort=rank&limit=100
# https://api.coinmarketcap.com/v2/global/

request="https://api.coinmarketcap.com/v2/listings/"
coin_ids=json.loads(urllib.request.urlopen(request).read())                    # Convert (.loads) from Python string when read, to dictionary

for coin in coins_dict:
   coinId=get_coinmarketcap_ID(coin)
   
   CoinDataCoinmarketcap="https://api.coinmarketcap.com/v2/ticker/"+str(coinId)+"/?convert=EUR"
# Turn the string returned from urllib.request.urlopen to python dictionary with .loads method
   coinData=json.loads(urllib.request.urlopen(CoinDataCoinmarketcap).read())

   circSupply=coinData['data']['circulating_supply']
   totalSupply=coinData['data']['total_supply']
   maxSupply=coinData['data']['max_supply']

   price=format(coinData['data']['quotes']['EUR']['price'],'.3f')
   price_change_24h=float(coinData['data']['quotes']['EUR']['percent_change_24h'])
   initial_purchased_price=format(float(coins_dict[coin][CONST_PURCH_PRICE]),'.3f')

   coins_dict[coin][CONST_PRICE]          =float(price)                                                          # "Price"
   coins_dict[coin][CONST_PRC_24H_CHANGE] =float(price_change_24h)/100                                           # "Prc24h"
   coins_dict[coin][CONST_PURCH_PRICE]    =float(initial_purchased_price)                                        # "purchaseprice"
   coins_dict[coin][CONST_PRC_PURCH_PRICE]=calculate_percentage_change(float(coins_dict[coin][CONST_PURCH_PRICE]),float(coins_dict[coin][CONST_PRICE]))  # "% purchase"
   coins_dict[coin][CONST_TOTAL_VALUE]    =int(float(coins_dict[coin][0])*float(price))                          # "Value"


   if circSupply != None:
      coins_dict[coin][CONST_CIRC_SUPPLY]    =float(circSupply)                                           # "Circ supply"
      percentageOfCircSupply                 =coins_dict[coin][CONST_COINS_NUMBER]/circSupply
      coins_dict[coin][CONST_PRC_CIRC_SUPPLY]=float(format(percentageOfCircSupply, '.10f'))               # "% Circ supply"
   else:
      coins_dict[coin][CONST_CIRC_SUPPLY]    =0
      coins_dict[coin][CONST_PRC_CIRC_SUPPLY]=0
  
   if totalSupply != None:
      coins_dict[coin][CONST_TOT_SUPPLY]    =float(totalSupply)                                          # "Tot supply"
      percentageOfTotalSupply               =coins_dict[coin][0]/totalSupply
      coins_dict[coin][CONST_PRC_TOT_SUPPLY]=float(format(percentageOfTotalSupply, '.10f'))              # "% Tot supply"
   else:
      coins_dict[coin][CONST_TOT_SUPPLY]    =0
      coins_dict[coin][CONST_PRC_TOT_SUPPLY]=0

   if maxSupply != None:
      coins_dict[coin][CONST_MAX_SUPPLY]    =float(maxSupply)                                            # "Max supply"
      percentageOfMaxSupply                 =coins_dict[coin][0]/maxSupply
      coins_dict[coin][CONST_PRC_MAX_SUPPLY]=float(format(percentageOfMaxSupply, '.10f'))                # "% Max supply"
   else:
      coins_dict[coin][CONST_MAX_SUPPLY]    =0
      coins_dict[coin][CONST_PRC_MAX_SUPPLY]=0

# myconsoleprint(coins_dict)
sorted_list=sort_based_on(coins_dict,key_to_sort)
# myconsoleprint(sorted_list)
print_attributes(attributes_to_print,sorted_list)

print("-"*145)
print("Total value: {:>39} euros".format(total_value))
