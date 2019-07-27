#毎朝定時に定額のBTC(ETH)をBFから購入するプログラム
import ccxt 
import requests
import schedule
import time
import pprint


#ccxtライブラリでBFのAPIを使用
bitflyer = ccxt.bitflyer()
bitflyer.apiKey = 'XXXXXXXXXXXX'#bitFlyerのプライベートapi_key
bitflyer.secret = 'XXXXXXXXXXXX'#bitFlyerのプライベートapi_secret

#ccxtでLiqudのAPIを使う
liquid = ccxt.liquid()
liquid.apiKey = "XXXXXXXXXXX"
liquid.secret = "XXXXXXXXXXX"

#ccxtでZaifのAPIを使う
zaif = ccxt.zaif()
zaif.apiKey = "XXXXXXXXXXX"
zaif.secret = "XXXXXXXXXXX"

#ccxtでコインチェックのAPIを使う
coincheck = ccxt.coincheck()
coincheck.apiKey = "XXXXXXXXXX"
coincheck.secret = "XXXXXXXXXX"


#ここからDefで定義
#取引所間の一番安い値段を取得

ticker_bf = bitflyer.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
ticker_liquid = liquid.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
ticker_zaif = zaif.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
ticker_cc = coincheck.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })

low_price = min((ticker_bf["last"]) , (ticker_liquid["last"]) , (ticker_zaif["last"]) , (ticker_cc["last"]))
if low_price == ticker_bf["last"]:
    print("bfが最安値です。" + str(low_price))

if low_price == ticker_liquid["last"]:
    print("liquidが最安値です" + str(low_price))

if low_price == ticker_zaif["last"]:
    print("zaif最安値です" + str(low_price))

if low_price == ticker_cc["last"]:
    print("ccが最安値です" + str(low_price))


#LineNotifyで購入状況を通知
def Line_Notify():
   
    ticker_bf = bitflyer.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
    ticker_liquid = liquid.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
    ticker_zaif = zaif.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
    ticker_cc = coincheck.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
    
#BFが安い場合の処理
    try:
        if low_price == ticker_bf["last"]:
            order = bitflyer.create_order(
                symbol = 'BTC/JPY',
                type  = 'market',
                side = 'buy',
                amount = '',#bFのBTC現物最小購入額は0.001なのでそれ以上を入力
                params = {'product_code' : 'BTC_JPY'})
    except:
        msg = 'bitFlyerのBTCの現在価格は' + str(ticker_bf["last"]) + 'です。\n' + 'エラーが発生したため、BTCを購入できませんでした。' #エラーが返ってきた場合購入できていないのでこの文言を送信
    else:
        msg = 'bitFlyerのBTCの現在価格は' + str(ticker_bf["last"]) + 'です。\n' + str(ticker['last'] / 1000) + '円で0.001BTCを購入しました'#エラー以外ならば購入しているのでこの文言を送信
    
#Liquidが安い場合の処理
    try:
        if low_price == ticker_liquid["last"]:
            order = liquid.create_order(
                symbol = 'BTC/JPY',
                type  = 'market',
                side = 'buy',
                amount = '',#bFのBTC現物最小購入額は0.001なのでそれ以上を入力
                params = {'product_code' : 'BTC_JPY'})
    except:
        msg = 'liquidのBTCの現在価格は' + str(ticker_liquid["last"]) + 'です。\n' + 'エラーが発生したため、BTCを購入できませんでした。' #エラーが返ってきた場合購入できていないのでこの文言を送信
    else:
        msg = 'liquidのBTCの現在価格は' + str(ticker_liquid["last"]) + 'です。\n' + str(ticker['last'] / 1000) + '円で0.001BTCを購入しました'#エラー以外ならば購入しているのでこの文言を送信

#zaifが安場合の処理
    try:
        if low_price == ticker_zaif["last"]:
            order = zaif.create_order(
                symbol = 'BTC/JPY',
                type  = 'market',
                side = 'buy',
                amount = '',#bFのBTC現物最小購入額は0.001なのでそれ以上を入力
                params = {'product_code' : 'BTC_JPY'})
    except:
        msg = 'zaifのBTCの現在価格は' + str(ticker_zaif["last"]) + 'です。\n' + 'エラーが発生したため、BTCを購入できませんでした。' #エラーが返ってきた場合購入できていないのでこの文言を送信
    else:
        msg = 'zaifのBTCの現在価格は' + str(ticker_zaif["last"]) + 'です。\n' + str(ticker['last'] / 1000) + '円で0.001BTCを購入しました'#エラー以外ならば購入しているのでこの文言を送信
    line_token = 'XXXXXXXXXXX'#個人で取得したLineNotify用のトークン
    line_api = 'https://notify-api.line.me/api/notify'

#ccが安い場合の処理
    try:
        if low_price == ticker_cc["last"]:
            order = coincheck.create_order(
                symbol = 'BTC/JPY',
                type  = 'market',
                side = 'buy',
                amount = '',#bFのBTC現物最小購入額は0.001なのでそれ以上を入力
                params = {'product_code' : 'BTC_JPY'})
    except:
        msg = 'CoincheckのBTCの現在価格は' + str(ticker_cc["last"]) + 'です。\n' + 'エラーが発生したため、BTCを購入できませんでした。' #エラーが返ってきた場合購入できていないのでこの文言を送信
    else:
        msg = 'CoincheckのBTCの現在価格は' + str(ticker_cc["last"]) + 'です。\n' + str(ticker['last'] / 1000) + '円で0.001BTCを購入しました'#エラー以外ならば購入しているのでこの文言を送信
    
    line_token = 'XXXXXXXXXXX'#個人で取得したLineNotify用のトークン
    line_api = 'https://notify-api.line.me/api/notify'

    print (msg)
    payload = {'message' : msg}
    headers = {'Authorization': 'Bearer ' + line_token}
    line_notify = requests.post(line_api, data = payload, headers = headers)

 
#時間指定してプログラムを起動
schedule.every().day.at("09:45").do(Line_Notify)#day.at()の中に何時に起動したいかを指定
while True:
    schedule.run_pending()
    time.sleep(1)