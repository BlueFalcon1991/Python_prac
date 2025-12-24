# import requests
# import pandas as pd

# url = 'https://www.nseindia.com/'  # Replace with actual API/endpoint
# # response = requests.get(url)

# headers = {"User-Agent": "Scraping101 (+your_email@example.com)"}

# resp = requests.get(url, headers=headers, timeout=20)
# print("Status:", resp.status_code)
# data = response.json()
# df = pd.DataFrame(data)
# print(df)
# df.to_csv('nifty50_daily.csv', index=False)=


import pandas as pd

# Create DataFrame
data = {'Name': ['A', 'B', 'C'], 'Age': [24, 27, 22], 'Score': [85, 90, 88]}
df = pd.DataFrame(data)

# Create Series
s = pd.Series([10, 20, 30], name='Marks')
print(df.shape)
# print(s)
