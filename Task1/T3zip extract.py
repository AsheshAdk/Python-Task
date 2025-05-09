import ijson
import zipfile
import pandas as pd


records = []

with zipfile.ZipFile("/home/zaki/Downloads/data.zip", 'r') as zf:

    print('open file:')
    for name in zf.namelist():
        print(name)
        with zf.open(name, 'r') as f:
            for item in ijson.items(f, 'provider_references.item'):
                records.append(item)



rate_df = pd.DataFrame(records)

out_new = "/home/zaki/Downloads/Asheshprogram/task/home.json"
rate_df.to_json(out_new,orient='records',indent=4)
print(f'Wrote {len(rate_df)} rows to {out_new}')
print(rate_df)