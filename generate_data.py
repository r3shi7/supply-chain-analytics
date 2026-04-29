import pandas as pd
import numpy as np

#set random seed so data is reproducible
np.random.seed(42)

#Number of records
n = 500

#List of vendors names
vendors = [
    "Bharat Forge", "Motherson Sumi", "Minda Industries",
    "Sandhar Technologies", "Uno Minda", "Endurance Tech",
    "Varroc Engineering", "Samvardhana Motherson", "Spark Minda",
    "Lumax Industries"
]

regions = ["North", "South", "East", "West"]

#create a data frame 
df = pd.DataFrame({
    "vendor_id": ["V" + str(i).zfill(3) for i in np.random.randint(1, 11, n)],
    "vendor_name": np.random.choice(vendors, n),
    "region": np.random.choice(regions,n)
})

#Generate order dates in 2003
order_dates = pd.date_range(start='2023-01-01', periods=n, freq ="D")
df['order_date'] = np.random.choice(order_dates, n)
df["order_date"] =  pd.to_datetime(df["order_date"])

df["promised_days"] = np.random.randint(5, 15, n)
df["actual_days"] = df["promised_days"] + np.random.randint(-2, 8, n)

df["defect_rate"] = np.random.uniform(0, 10, n)
df["order_value"] = np.random.uniform(10000, 500001, n)

df["payment_days"] = np.random.randint(30, 91, n)


df.to_csv("data/vendors.csv", index = False)
print(f"Dataset saved! Shape: {df.shape}")
#print(df.head())