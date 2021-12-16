import sys

import requests

api_endpoint_futures = "https://ftx.com/api/markets"
f_spot = open("spot.txt", 'w')
json_data = requests.get(api_endpoint_futures).json()

list = []
count = 0
depths = [15, 50, 100]
max_range = 3

for instrument in json_data['result']:
    name = instrument['name']
    if (instrument['type'] == 'spot') and (not "EDGE" in name)\
    and (not "BULL" in name) and (not "BEAR" in name) and (not "HALF" in name)\
    and ("/USD" in name):
        count += 1
        # if count > 2:
        #     break
        print(str(count) + ")" + name, end=' ')
        position = -1
        ticker = name.split("/")[0]
        for i in range(0, len(list)):
            if list[i][0] == ticker:
                position = i

        sum_bids = [0,0,0]
        sum_asks = [0,0,0]
        for i in range(0, max_range):

            api_endpoint_orderbook = "https://ftx.com/api/markets/" + name + "/orderbook?depth="+str(depths[i])
            json_data = requests.get(api_endpoint_orderbook).json()

            orderbook = json_data['result']['bids']
            sum_bids[i] = 0
            for item in orderbook:
                sum_bids[i] += item[0] * item[1]

            orderbook = json_data['result']['asks']
            sum_asks[i] = 0
            for item in orderbook:
                sum_asks[i] += item[0] * item[1]

        if position == -1:
            list.append([ticker, sum_bids[0], sum_asks[0],
                                 sum_bids[1], sum_asks[1],
                                 sum_bids[2], sum_asks[2]])
        else:
            list[position][1] += sum_bids[0]
            list[position][2] += sum_asks[0]
            list[position][3] += sum_bids[1]
            list[position][4] += sum_asks[1]
            list[position][5] += sum_bids[2]
            list[position][6] += sum_asks[2]
            list[position][0] = "*" + list[position][0]

print("\n")
print("                               15       50      100")

list.sort(key=lambda x: x[1], reverse=False)
for item in list:
    st = item[0].ljust(13) + str(float('{:.1f}'.format(item[5] + item[6]))).ljust(14)

    bids_percents = [0, 0, 0]
    asks_percents = [0, 0, 0]
    st_percent = ""

    for i in range(0, max_range):
        sum_bids_asks = item[i*2+1] + item[i*2+2]
        if sum_bids_asks != 0:
            bids_percents[i] = int(item[i*2+1] * 100 / sum_bids_asks)
            asks_percents[i] = int(item[i*2+2] * 100 / sum_bids_asks)
        s = str(bids_percents[i]) + "/" + str(asks_percents[i])

        if bids_percents[i] < asks_percents[i]:
            s += "↓"
        elif bids_percents[i] > asks_percents[i]:
            s += "↑"

        if bids_percents[i] < 33 or bids_percents[i] > 66:
            s += "*"
        st_percent = st_percent + s.ljust(9)

    print(st + st_percent)
    f_spot.write(st + " " + st_percent.replace("↓","v").replace("↑","^") + "\n")
f_spot.close()
sys.exit(0)

########################################################################################################################

api_endpoint_futures = "https://ftx.com/api/futures"
json_data = requests.get(api_endpoint_futures).json()
f_perpetual = open("perpetual.txt", 'w')

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

print("\n")
list.sort(key=lambda x: x[1], reverse=True)
for item in list:
    st = item[0].ljust(13) + str(float('{:.1f}'.format(item[1])))
    print(st)
    f_perpetual.write(st+"\n")
f_perpetual.close()