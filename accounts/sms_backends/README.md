# BDSMS API
Link: [BD Bulk SMS API](https://bdbulksms.net/bd-bulk-sms-api.php)

```python
import requests 
greenweburl = "http://api.greenweb.com.bd/api.php"
https_greenweburl = "https://sms.greenweb.com.bd/api.php"

# your token code here 
token = "d7b8a552f6c00b66408a47c00c1191bf"

# sms receivers number here (separated by comma) 
to = '+880178364552m' 

data = {
    'token': token, 
	'to': to, 
	'message':'test sms'
} 
 
# responses = requests.post(url=greenweburl, data=data) 
# responses = requests.post(url=https_greenweburl, data=data) 

# # response 
# response = responses.text 
# print(response) 
# print(responses)

## BALANCE CHECK
URL = "http://api.greenweb.com.bd/g_api.php"
URL_FOR_BALANCE = f"{URL}?token={token}&balance"
URL_FOR_SMS_RATE = f"{URL}?token={token}&rate"
URL_FOR_SMS_TOTAL = f"{URL}?token={token}&tokensms"
URL_FOR_SMS_TOTAL_USER = f"{URL}?token={token}&totalsms"
URL_FOR_SMS_EXPIRY = f"{URL}?token={token}&expiry"
URL_FOR_ALL = f"{URL}?token={token}&expiry&rate&tokensms&totalsms"

res = requests.get(url=URL_FOR_ALL)
print(res.text)
```