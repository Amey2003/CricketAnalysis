import pandas as pd
import json

with open('t20_json-files/t20_wc_match_results.json') as f:
    data = json.load(f)
df_match = pd.DataFrame(data[0]['matchSummary'])
#print(df_match)
#print(df_match.shape)

df_match.rename({'scorecard': 'match_id'}, axis=1, inplace=True)
#print(df_match)

match_ids_dict = {}
for index, row in df_match.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']

    match_ids_dict[key1] = row['match_id']
    match_ids_dict[key2] = row['match_id']

#print(match_ids_dict)
    
df_match.to_csv('fact_match.csv', index=False)

#Batting Summary
with open('t20_json-files/t20_wc_batting_summary.json') as f:
    data = json.load(f)

    all_records = []
    for record in data:
        all_records.extend(record['battingSummary'])

df_batting = pd.DataFrame(all_records)
#print(df_batting.tail())

df_batting['out/not-out'] = df_batting.dismissal.apply(lambda x: 'out' if len(x)>0 else 'not-out')
#print(df_batting['batsmanName'].head(11))

df_batting.drop(columns=['dismissal'],inplace=True)

df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('â€',''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('\xa0',''))

df_batting['match_id'] = df_batting['match'].map(match_ids_dict)
#print(df_batting.head(2))

df_batting.to_csv('fact_batting_summary.csv', index=False)


with open('t20_json-files/t20_wc_bowling_summary.json') as f:
    data = json.load(f)

    all_records = []
    for record in data:
        all_records.extend(record['bowlingSummary'])

df_bowling = pd.DataFrame(all_records)
#print(df_bowling.head(5))

df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)
#print(df_bowling.head(2))

df_bowling.to_csv('fact_bowling_summary.csv', index=False)
print('Success')
