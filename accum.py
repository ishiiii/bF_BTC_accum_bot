#毎朝定時に定額のBTC(ETH)をBFから購入するプログラム
import ccxt 
import requests
import schedule
import time

#ccxtライブラリでBFのAPIを使用
bitflyer = ccxt.bitflyer()
bitflyer.apiKey = 'XXXXXXXXXXXX'#bitFlyerのプライベートapi_key
bitflyer.secret = 'XXXXXXXXXXXX'#bitFlyerのプライベートapi_secret


#LineNotifyで購入状況を通知
def Line_Notify():
   
    ticker = bitflyer.fetch_ticker('BTC/JPY', params = { "product_code" : "BTC_JPY" })
     
    try:
        order = bitflyer.create_order(
            symbol = 'BTC/JPY',
            type = 'market',
            side = 'buy',
            amount = '',#bFのBTC現物最小購入額は0.001なのでそれ以上を入力
            params = {'product_code' : 'BTC_JPY'})
    except:
        msg = 'BTCの現在価格は' + str(ticker['last']) + 'です。\n' + 'エラーが発生したため、BTCを購入できませんでした。' #エラーが返ってきた場合購入できていないのでこの文言を送信
    else:
        msg = 'BTCの現在価格は' + str(ticker['last']) + 'です。\n' + str(ticker['last'] / 1000) + '円で0.001BTCを購入しました'#エラー以外ならば購入しているのでこの文言を送信
    
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
