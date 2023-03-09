import requests
import csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_as_json= response.json()

for item in data_as_json:
    only_rates = item.get('rates')

with open('names.csv', 'w', encoding="utf-8", newline='') as csvfile:
    fieldnames = ['currency','code','bid','ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
    writer.writeheader()
    for rate in only_rates:
        writer.writerow({'currency':rate.get('currency'),'code':rate.get('code'),
        'bid':rate.get('bid'),'ask':rate.get('ask')})