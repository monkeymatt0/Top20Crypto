from datetime import datetime
from operator import itemgetter

import requests
from pprint import pprint


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
    worstCurrencies = currenciesSymbolVariation[len(currenciesSymbolVariation)-10:len(currenciesSymbolVariation)]
    worstCurrencies.reverse()

    return {'best10': bestCurrencies, 'worst10': worstCurrencies}


# La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute*
def sumToBuyUnitOfEach20TopCrypto(criptoCurrencies) -> float:
    pass


# La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
def sumToBuyBy25HVolume(criptoCurrencies) -> float:
    pass


# La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata)
def overview():
    pass


# Per evitare che il vostro programma sovrascriva lo stesso file JSON, denominatelo con la data del momento in cui il programma viene eseguito.

# *Le prime 20 criptovalute secondo la classifica predefinita di CoinMarketCap, quella visibile sul sito, dunque ordinate per capitalizzazione.

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
pprint(currencies)  # Stampa delle valute ottenute

MaxVolCripto24H = maxVolCripto24H(currencies['data'])  # Recupero la valuta che ha il volume maggiore nelle ultime 24 ore
print(f"max volume in 24h: {MaxVolCripto24H}")

BestAndWorst10Currencies = bestAndWorst10CriptoCurrencies(currencies['data'])
print(f"best 10 crypto: {BestAndWorst10Currencies['best10']}\n\n")
print(f"worst 10 crypto: {BestAndWorst10Currencies['worst10']}")
