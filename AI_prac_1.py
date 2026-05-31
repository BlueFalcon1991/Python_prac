# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# %%
# Experience (years) and corresponding salaries (₹ thousands/month)
experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
              11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

salary     = [18, 22, 28, 35, 40, 45, 50, 58, 62, 68,
              72, 76, 80, 85, 90, 94, 97, 101, 106, 110]

# Put into a DataFrame — your SAS dataset equivalent
df = pd.DataFrame({
    "experience": experience,
    "salary": salary
})

print(df.head(5))   # Show first 5 rows

# %%
# Draw a scatter plot — visualise the relationship
plt.figure(figsize=(8, 5))
plt.scatter(df["experience"], df["salary"],
            color="steelblue", s=80, label="Actual data")

plt.xlabel("Experience (years)")
plt.ylabel("Salary (₹ thousands/month)")
plt.title("Experience vs Salary")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


