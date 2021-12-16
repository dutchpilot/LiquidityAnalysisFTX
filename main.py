import requests

api_endpoint_futures = "https://ftx.com/api/markets"
json_data = requests.get(api_endpoint_futures).json()

list = []
count = 0

for instrument in json_data['result']:
    name = instrument['name']
    if (instrument['type'] == 'spot') and (not "EDGE" in name)\
    and (not "BULL" in name) and (not "BEAR" in name)and (not "HALF" in name)\
    and ("/USD" in name):
        count += 1

        position = -1
        ticker = name.split("/")[0]
        for i in range(0, len(list)):
            if list[i][0] == ticker:
                position = i

        api_endpoint_orderbook = "https://ftx.com/api/markets/" + name + "/orderbook?depth=100"
        json_data = requests.get(api_endpoint_orderbook).json()
        print(str(count) + ") " + name, end=' ')
        orderbook = json_data['result']['bids']
        sum = 0
        for item in orderbook:
            sum += item[0] * item[1]

        if position == -1:
            list.append([ticker, sum])
        else:
            list[position][1] += sum
            list[position][0] = "*" + list[position][0]

list.sort(key=lambda x: x[1], reverse=True)
for item in list:
    print(item[0].ljust(13) + str(float('{:.1f}'.format(item[1]))))

########################################################################################################################

api_endpoint_futures = "https://ftx.com/api/futures"
json_data = requests.get(api_endpoint_futures).json()

list = []
count = 0

for instrument in json_data['result']:
    if (instrument['expiryDescription'] == 'Perpetual'):
        count += 1
        name = instrument['name']
        api_endpoint_orderbook = "https://ftx.com/api/markets/" + name + "/orderbook?depth=100"
        json_data = requests.get(api_endpoint_orderbook).json()
        print(str(count) + ") " + name, end=' ')
        orderbook = json_data['result']['bids']
        sum = 0
        for item in orderbook:
            sum += item[0] * item[1]

        list.append([name, sum])

list.sort(key=lambda x: x[1], reverse=True)
for item in list:
    print(item[0].ljust(13) + str(float('{:.1f}'.format(item[1]))))