import coreapi
import pandas as pd

EQUIPMENT_VARS = ('head','body','hands','legs','feet','ears','neck','wrists')
RING_VARS = ('fingerL','fingerR')
RAID_GEAR_NAME = "Dark Horse"

cols = ["Job","Set"]
cols.extend(EQUIPMENT_VARS)
cols.append("ring")
cols = list(map(lambda x:x.title(),cols))
print(cols)

client = coreapi.Client()
schema = client.get("https://etro.gg/api/docs/")

bis_data = client.action(schema, ["gearsets","bis"])

datatable = []
cache = {}
for x in bis_data:
  row = [x["jobAbbrev"],x["name"]]
  for y in EQUIPMENT_VARS:
    if x[y] in cache:
      text = cache[x[y]]
    else:
      text = client.action(schema, ["equipment", "read"], params={"id":x[y]})["name"]
      cache[x[y]] = text
    row.append(RAID_GEAR_NAME in text)
  ring_needed = False
  for y in RING_VARS:
    if x[y] in cache:
      text = cache[x[y]]
    else:
      text = client.action(schema, ["equipment", "read"], params={"id":x[y]})["name"]
      cache[x[y]] = text
    if RAID_GEAR_NAME in text:
      ring_needed = True
      break
  row.append(ring_needed)
  datatable.append(row)
  print(row)
  
df = pd.DataFrame(datatable,columns=cols)
df = df[df["Job"]!="BLU"]

df.to_csv("tome_raid.csv",index=False)