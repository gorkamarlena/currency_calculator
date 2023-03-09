import requests, datetime, csv
from flask import Flask
from flask import request, render_template

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_as_json= response.json()

app = Flask(__name__)

for item in data_as_json:
    only_rates = item.get('rates')
    current_date = item.get('effectiveDate')

codes_list = []
for rate in only_rates:
    cc = rate['code']
    codes_list.append(cc)

with open('names.csv', 'w', encoding="utf-8", newline='') as csvfile:
    fieldnames = ['currency','code','bid','ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
    writer.writeheader()
    for rate in only_rates:
        writer.writerow({'currency':rate.get('currency'),'code':rate.get('code'),
        'bid':rate.get('bid'),'ask':rate.get('ask')})

@app.route('/calculator', methods=['GET', 'POST'])
def rates_calculator():  
    if  request.method == 'GET':
        print("We received GET")
        return render_template("calculator.html", codes_list=codes_list)

    elif request.method == 'POST':
        print("We received POST")
        if current_date != datetime.date.today():
            response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
            data_as_json= response.json()
            for item in data_as_json:
                only_rates = item.get('rates')

        d = request.form
        quantity_form=d.get('quantity')
        curr_selected_form=d.get('currencies')
        for rate in only_rates:
            if curr_selected_form ==rate.get('code'):
                result=float(rate.get('ask'))*float(quantity_form)
                print(result)
        return f'{quantity_form} {curr_selected_form} cost {result:0.2f} PLN.'

if __name__ == "__main__":
   app.run(debug=True)