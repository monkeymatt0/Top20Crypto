from datetime import datetime
from operator import itemgetter

import requests
from pprint import pprint
import json


# La criptovaluta con il volume maggiore (in $) delle ultime 24 ore
def maxVolCripto24H(criptoCurrencies) -> tuple:
    symbol = ""
    vol24h = 0

    for criptoCurrency in criptoCurrencies:
        if criptoCurrency['quote']['USD']['volume_24h'] > vol24h:
            symbol = criptoCurrency['symbol']  # Identifica la cripto con il suo simbolo
            vol24h = criptoCurrency['quote']['USD']['volume_24h']  # Identifica la capitalizzazione di mercato

    return symbol, vol24h


# Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)
def bestAndWorst10CriptoCurrencies(criptoCurrencies) -> dict:
    currenciesSymbolVariation = []

    for currency in criptoCurrencies:
        currenciesSymbolVariation.append((currency['symbol'], currency['quote']['USD']['percent_change_24h']))

    currenciesSymbolVariation.sort(key=itemgetter(1), reverse=True)

    bestCurrencies = currenciesSymbolVariation[0:11]
    worstCurrencies = currenciesSymbolVariation[len(currenciesSymbolVariation) - 10:len(currenciesSymbolVariation)]
    worstCurrencies.reverse()

    return {'best10': bestCurrencies, 'worst10': worstCurrencies}


# La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute*
def sumToBuyUnitOfEach20TopCrypto(criptoCurrencies) -> float:
    ret = 0.0

    for t in criptoCurrencies:
        ret += float(t['quote']['USD']['price'])

    return ret


# La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
def sumToBuyBy24HVolume(criptoCurrencies) -> float:
    ret = 0.0

    for criptoCurrency in criptoCurrencies:
        if criptoCurrency['quote']['USD']['volume_24h'] > 76000000:
            ret += criptoCurrency['quote']['USD']['price']

    return ret


# La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca
# non sia cambiata)
def possibleProfit(criptoCurrencies) -> float:
    ret = 0.0

    for currency in criptoCurrencies:
        ret += currency['quote']['USD']['percent_change_24h']

    return ret


def saveIntoJsonFile(data) -> str:

    filename = f"{datetime.now()}.json"
    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

    return filename


# Url per contattare l'API e recuperare le informazioni sulle currencies
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

params = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}

header = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '7aceed3f-6204-4bab-802a-a16bb60d5b49'
}

currencies = requests.get(url=url, headers=header, params=params).json()
pprint(currencies['data'][:20])  # Stampa delle valute ottenute

MaxVolCripto24H = maxVolCripto24H(currencies['data'])  # Recupero la valuta che ha il volume maggiore nelle ultime 24 ore
print(f"max volume in 24h: {MaxVolCripto24H}\n\n")

BestAndWorst10Currencies = bestAndWorst10CriptoCurrencies(currencies['data'])
print(f"best 10 crypto: {BestAndWorst10Currencies['best10']}\n\n")
print(f"worst 10 crypto: {BestAndWorst10Currencies['worst10']}\n\n")

SumToBuyUnitOfEach20TopCrypto = sumToBuyUnitOfEach20TopCrypto(currencies['data'][:20])
print(f"Sum to buy one of each best 20 crypto: {SumToBuyUnitOfEach20TopCrypto}$\n\n")

SumToBuyBy24HVolume = sumToBuyBy24HVolume(currencies['data'])
print(f"Sum to buy one of each cripto with more then 76000000$ of market cap in the last 24h: {SumToBuyBy24HVolume}\n\n")

PossibleProfit = possibleProfit(currencies['data'][:20])
print(f"Possible profit: {PossibleProfit}%")

data = {
    'max volume in 24h': MaxVolCripto24H,
    'best 10 crypto:': BestAndWorst10Currencies['best10'],
    'worst 10 crypto:': BestAndWorst10Currencies['worst10'],
    'Sum to buy one of each best 20 crypto': SumToBuyUnitOfEach20TopCrypto,
    'Sum to buy one of each cripto with more then 76000000$ of market cap in the last 24h': SumToBuyBy24HVolume,
    'Possible profit (%)': PossibleProfit
}

filename = saveIntoJsonFile(data) # Inserimento all'interno del file json
print(f"**************** REPORT SALVATO IN {filename} ****************")
