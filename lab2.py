import json
import urllib.request
import pandas as pd
import boto3
import matplotlib.pyplot as plt

dollar_rates, euro_rates = [], []
for i in ["usd", "eur"]:
    data = urllib.request.urlopen(f"https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode={i}&sort=exchangedate&order=asc&json").read()
    output = json.loads(data)
    for j in output:
        if j["cc"] == "USD":
            dollar_rates.append({"date": j["exchangedate"], "USD": j["rate"]})
        else:
            euro_rates.append({"date": j["exchangedate"], "EUR": j["rate"]})

df_dollar = pd.DataFrame(dollar_rates).set_index("date")
df_euro = pd.DataFrame(euro_rates).set_index("date")


# df = pd.concat([df_dollar, df_euro], axis=1)
# df.to_csv("parsed_data.csv")
df = pd.concat([df_dollar, df_euro], axis=1)
df.to_csv("parsed_data.csv", sep=";")

access_key = "Not defined:)"
access_key_secret = "not defined:)"

s3_client = boto3.client('s3', aws_access_key_id=access_key,aws_secret_access_key=access_key_secret)


def upload( file, bucket_name):
    s3_client.upload_file(file, bucket_name, file)


def download(file, bucket_name):
    s3_client.download_file(bucket_name, file, file)

ax = df.plot(figsize=(15, 7), title="UAH currency", fontsize=12)
ax.set_xlabel("date")
ax.set_ylabel("Exchange rate")
plt.savefig('plot.png')

upload("parsed_data.csv", "kortarbucket")
download("parsed_data.csv", "kortarbucket")

upload("plot.png", "kortarbucket")
download("plot.png", 'kortarbucket')
