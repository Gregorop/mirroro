import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("test_results.csv")
#thickness
#result
#min_r

df = df[df["success for 5 min"]==1]
df = df[df["min_r"]>8]
df.plot(x="thickness",y="result",kind="scatter",c="min_r",colormap='viridis')

plt.show()
