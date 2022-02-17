import requests, time
import urllib3

urllib3.disable_warnings()

r = requests.get("https://ds.widedigital.com.br/datetime.php", verify=False)

print(r.content.decode("utf-8"))
