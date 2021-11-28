```py
dataList = [{'lead_id': 'fa3f69c1-ca76-4d91-92ad-5625b23f0e9d', 'purchase_date': '2021-11-27 16:45:47.009749'}
, {'lead_id': '22e08a79-2192-4ede-b965-d2f589143995', 'purchase_date': '2021-11-27 16:45:47.010744'}]
for index in range(len(dataList)):
    print('new one')
    for key in dataList[index]:
        print(key)
        print(dataList[index][key])
```

```py
for index in range(len(dataList)):
    for key in dataList[index]:
        lead_id = dataList[index]['lead_id']
        purchase_date = dataList[index]['purchase_date']
    print(lead_id)
    print(purchase_date)
```
