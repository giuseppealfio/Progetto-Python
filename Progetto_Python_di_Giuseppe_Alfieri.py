import requests
import json
import datetime
from pprint import pprint

class Report:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '0355b413-3dbf-426d-8c1a-259d2f496caf',
        }

    def fetchCurrenciesData(self): #Funzione per creare una lista di criptovalute da Coinmarketcap
        database = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return database['data']

    def largest_volume(self): #La criptovaluta con il volume maggiore (in $) delle ultime 24 ore
        resultsReport = Report()
        currencies = resultsReport.fetchCurrenciesData()
        currency_name = []
        currency_volume = 0
        for currency in currencies:
            if currency ['quote']['USD']['volume_24h'] > currency_volume:
                currency_volume = currency ['quote']['USD']['volume_24h']
                currency_name = currency['name']
        return currency_name, currency_volume

    def best_and_wrost_percent_change_24h(self): #Le migliori e le peggiori criptovalute (per incremento in percentuale delle ultime 24 ore)
        resultsReport = Report()
        currencies = resultsReport.fetchCurrenciesData()
        currency_name = []
        percent_change_24h = []
        for currency in currencies:
            currency_name.append(currency['name'])
            percent_change_24h.append(currency['quote']['USD']['percent_change_24h'])

        dictionary = dict(zip(currency_name, percent_change_24h))
        best_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        worst_dictionary = sorted(dictionary.items(), key=lambda x: x[1])

        best_10 = list(best_dictionary[:10])
        worst_10 = list(worst_dictionary[:10])
        return best_10, worst_10

    def purchase_first_20(self):  #La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute
        resultsReport = Report()
        currencies = resultsReport.fetchCurrenciesData()
        market_cap = {}
        best_20_market_cap = []
        money_needed = 0

        for currency in currencies:
            market_cap[currency['quote']['USD']['market_cap']] = currency['name']

        for element in sorted(market_cap.keys(), reverse=True):
            if len(best_20_market_cap) < 20:
                best_20_market_cap.append((market_cap[element], element))

        for currency in currencies:
            for y in range(20):
                if best_20_market_cap[y][0] == currency['name']:
                    money_needed += currency['quote']['USD']['price']
        return market_cap, best_20_market_cap, money_needed

    def purchase_bestCurrencies(self): #La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
        resultsReport = Report()
        currencies = resultsReport.fetchCurrenciesData()
        bestCurrencies_volume_24h = []
        volume_24h_start = 76000000
        money_needed_2 = 0
        for currency in currencies:
            if currency['quote']['USD']['volume_24h'] > volume_24h_start:
                bestCurrencies_volume_24h.append(currency['name'])
                money_needed_2 += currency['quote']['USD']['price']
        return bestCurrencies_volume_24h, volume_24h_start, money_needed_2

    def gain_loss_percentage(self): #La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata)
        resultsReport = Report()
        currencies = resultsReport.fetchCurrenciesData()

        market_cap = {}
        best_20 = []
        total_price = 0
        previous_total_price = 0

        for currency in currencies:
            market_cap[currency['quote']['USD']['market_cap']] = currency['name']
        for element in sorted(market_cap.keys(), reverse=True):
            if len(best_20) < 20:
                best_20.append((market_cap[element], element))

        for currency in currencies:
            for x in range(20):
                if best_20[x][0] == currency['name']:
                    total_price += currency['quote']['USD']['price']
                    previous_total_price += currency['quote']['USD']['price'] - ((currency['quote']['USD']['price'] * currency['quote']['USD']['percent_change_24h'])/100)

        main_gain_loss = ((previous_total_price * 100) - (total_price * 100)) / -total_price
        return best_20, total_price, previous_total_price, main_gain_loss

    def printer(self):
        currency_name, currency_volume = Report.largest_volume(self)
        best_10, worst_10 = Report.best_and_wrost_percent_change_24h(self)
        market_cap, best_20_market_cap, money_needed = Report.purchase_first_20(self)
        bestCurrencies_volume_24h, volume_24h_start, money_needed_2 = Report.purchase_bestCurrencies(self)
        best_20, total_price, previous_total_price, main_gain_loss = Report.gain_loss_percentage(self)

        #Richiesta 1
        print(f"\n{currency_name} è la criptovaluta con il volume maggiore delle ultime 24 ore.\n"
               f"Il suo volume corrisponde a: {currency_volume} $")

        #Richiesta 2
        print(f"\n\nLe migliori 10 criptovalute (per incremento in percentuale delle ultime 24 ore):")
        for x in best_10:
            print(x)

        print(f"\nLe peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore):")
        for x in worst_10:
            print(x)

        #Richiesta 3
        print(f"\n\nLista delle {len(best_20_market_cap)} criptovalute per capitalizzazione di mercato:")
        for x in best_20_market_cap:
            print(x)

        print(f"\nDenaro necessario per comprare ognuna delle {len(best_20_market_cap)} criptovalute: {money_needed} $")

        #Richiesta 4
        print(f"\n\nNumero criptovalute con volume superiore a {volume_24h_start}$ nelle ultime 24 ore: {len(bestCurrencies_volume_24h)}")
        print(f"Denaro necessario per acquistare una unità di queste {len(bestCurrencies_volume_24h)} criptovalute: {money_needed_2} $")
        print(f"\nLista delle {len(bestCurrencies_volume_24h)} criptovalute:")
        for currency in bestCurrencies_volume_24h:
            print(currency)

        #Richiesta5
        print(f"\n\nAnalisi prezzo totale di acquisto tra ieri ed oggi sulle migliori {len(best_20)} criptovalute per capitalizzazione:")
        print(f"- prezzo totale (ieri): {previous_total_price} $")
        print(f"- prezzo totale (oggi): {total_price} $")

        if total_price > previous_total_price:
            print(f"- Percentuale di guadagno: {main_gain_loss} %")
        else:
            print(f"- Percentuale di perdita: {main_gain_loss} %")

        #File JSON
        data = {}
        data['request_1'] = []
        data['request_1'].append({
            'name': currency_name,
            'volume': currency_volume
        })
        data['request_2'] = []
        data['request_2'].append({
            "best_10_percent_change_24h" : best_10,
            'wrost_10_percent_change_24h' : worst_10
        })
        data['request_3'] = []
        data['request_3'].append({
            'best_20_market_cap' : best_20_market_cap,
            'money_needed' : money_needed
        })
        data['request_4'] = []
        data['request_4'].append({
            'best_currencies_volume_24' : len(bestCurrencies_volume_24h),
            'money_needed' : money_needed_2
        })
        data['request_5'] = []
        data['request_5'].append({
            'previuos_total_price': previous_total_price,
            'total_price': total_price,
            'main_gain_loss': main_gain_loss
        })


        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        with open(timestamp+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

results = Report()
results.printer()