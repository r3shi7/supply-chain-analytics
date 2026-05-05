import pandas as pd
import numpy as np

#set random seed so data is reproducible
np.random.seed(42)

#Number of records
n = 5000

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

#inject missing values (real data  has gaps)
df.loc[df.sample(frac=0.03).index, "defect_rate"] = np.nan
df.loc[df.sample(frac=0.02).index, "payment_days"] = np.nan
df.loc[df.sample(frac=0.01).index, "region"] = np.nan

#inject outliers (data entry errors / genuine anomlies)
outliers_idx =df.sample(frac=0.01).index
df.loc[outliers_idx, "order_value"] = df.loc[outliers_idx, "order_value"] * 10

#Add vendor-specific patterns (some vendors are genuinely worse) 
problem_vendors = ["Lumax Industries","Spark Minda"]
mask = df["vendor_name"].isin(problem_vendors)
df.loc[mask, "defect_rate"] = df.loc[mask,"defect_rate"] * 1.5
df.loc[mask, "actual_days"] = df.loc[mask, "actual_days"] + np.random.randint(2,6, mask.sum())

#add a delivery_status column derived from actual vs promiesd
df["delivery_status"] =  np.where(
    df["actual_days"] <=  df["promised_days"], "on-Time",
    np.where(df["actual_days"] <= df["promised_days"] + 3, "Slight Delay", "Major Delay")
)

#Inconsistent tet formatting (real data has this extra spaces, case issues)
df.loc[df.sample(frac=0.05).index, "vendor_name"] =  df["vendor_name"].str.upper()
df.loc[df.sample(frac=0.03).index,  "region"] = df["region"].str.lower()


df.to_csv("data/raw/vendors.csv", index = False)
print(f"Dataset saved! Shape: {df.shape}")
#print(df.head())