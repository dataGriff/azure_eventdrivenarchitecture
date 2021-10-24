import csv, uuid, random, datetime

directory = 'C:\\Users\\griff\\OneDrive\\Data\\sales' ## Write sales to one drive location for logic app to pickup
##number_of_sales = 5 ## Number of sales
##days_between_dates = 90 ## Date range for sales

print("Set constant values...")
partner_id = random.randint(1,25)
date =  datetime.date.today()
header = ['lead_guid', 'purchase_date']
print("Completed setting constant values.")

print("Start creating csv file...")
with open(f'{directory}/sale_partner{partner_id}_{uuid.uuid4()}.csv', 'w'
                , encoding='UTF8', newline='') as f:
    print("Start creating csv header...")
    writer = csv.writer(f)
    writer.writerow(header)
    print("Completed creating csv header.")

    r = 1
    print(f"Start inserting {number_of_sales} sales rows...")
    while r < number_of_sales:
        rand_guid = str(uuid.uuid4())
        rand_productid = random.randint(1,10)
        rand_brandid = random.randint(1,50)
        random_number_of_days = random.randrange(days_between_dates)
        rand_date = str(start_date - datetime.timedelta(days=random_number_of_days))
        data = [[rand_guid, rand_date,rand_productid,rand_brandid]]
        writer.writerows(data)
        r+=1
    print(f"Completed inserting {number_of_sales} sales rows.")
print("Completed creating csv file.")