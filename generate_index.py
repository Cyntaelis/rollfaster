import pandas as pd

CSV_FILE = "tome_raid.csv"
INDEX = "index.md"
README = "README.md"
PRESCRIPT = """
# Updated for patch 7.05
## ⬜ = Raid Gear is BiS 
## 🔳 = Something else is BiS 
### It's probably aug tome gear idk I don't play jobs with PIE/TEN

"""
POSTSCRIPT = """

I use [etro.gg](https://etro.gg/) for data, go support them if you found this useful.
"""

df = pd.read_csv(CSV_FILE)
df.replace(False, "🔳", inplace=True)
df.replace(True, "⬜", inplace=True)
df = df.apply(lambda col: col.str.replace("|","\|"))

md_table = df.to_markdown(index=False)
md_table=md_table.replace("-|",":|")

for x in (INDEX, README):
    with open(x, 'w') as file:
        file.write(PRESCRIPT)
        file.write(md_table)
        file.write(POSTSCRIPT)

