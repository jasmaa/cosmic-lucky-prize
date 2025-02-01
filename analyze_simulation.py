import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv").sort_values(by="agent_type")

# Filter outliers
q = df["num_jades"].quantile(0.99)
df = df[df["num_jades"] < q]

# Graph all

print("All:")
print("\tMean:", df["num_jades"].mean())
print("\tSD:", df["num_jades"].std())

df["num_jades"].plot(
    kind="hist",
    range=[0, 3000],
    density=True,
    bins=50,
    title="Distribution of Jades Earned",
    xlabel="Num Jades",
    ylabel="Percentage",
)
plt.savefig("simulation_all.png")

# Graph by agent type
fig, axes = plt.subplots(nrows=2, ncols=3, sharey=True)
fig.set_size_inches(12, 8)
fig.suptitle("Distributions of Jades Earned by Different Agent Types")

for ax, (name, subdf) in zip(axes.flatten(), df.groupby("agent_type")):
    subdf.hist("num_jades", ax=ax, range=[0, 3000], density=True, bins=50)
    ax.set_title(name)
    ax.set_xlabel("Num Jades")
    ax.set_ylabel("Percentage")

    print(name)
    print("\tMean:", subdf["num_jades"].mean())
    print("\tSD:", subdf["num_jades"].std())

plt.savefig("simulation_by_agent.png")
