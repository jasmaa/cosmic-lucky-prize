import math
import pandas as pd
import matplotlib.pyplot as plt

print("=== ColdFeet ===")

df_1 = pd.DataFrame(data={"prob": [1], "num_jades": [700]})

avg = sum(df_1["prob"] * df_1["num_jades"])
var = sum(df_1["prob"] * df_1["num_jades"] ** 2) - avg**2
sd = math.sqrt(var)

print(f"Mean: {avg}")
print(f"SD: {sd}")

# Calculate for ReachForTheStars

print("=== ReachForTheStars ===")

ps = []
vs = []
for k in range(8):
    p = math.comb(7, k) * 0.1**k * 0.9 ** (7 - k)
    v = 600 * k + 50 * (7 - k)

    ps.append(p)
    vs.append(v)

    print(f"k = {k}")
    print(f"\tp = {round(p, 5)}")
    print(f"\tv = {v}")

df_2 = pd.DataFrame(data={"prob": ps, "num_jades": vs})

avg = sum(df_2["prob"] * df_2["num_jades"])
var = sum(df_2["prob"] * df_2["num_jades"] ** 2) - avg**2
sd = math.sqrt(var)

print(f"Mean: {avg}")
print(f"SD: {sd}")

df_2.plot(
    kind="bar",
    x="num_jades",
    y="prob",
    title="Probability of Earning Jades",
    xlabel="Num Jades",
    ylabel="Probability",
    legend=None,
)
plt.savefig("gambler.png", bbox_inches="tight")
