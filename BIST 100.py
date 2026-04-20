import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



bist = pd.read_csv("C:/Users/duhan/Downloads/BIST 100 Historical Data (1).csv")
usd = pd.read_csv("C:/Users/duhan/Downloads/USD_TRY Historical Data (1).csv")
cpi = pd.read_excel("C:/Users/duhan/Downloads/EVDS_19-04-2026 (1) (1).xlsx")

bist = bist[["Date", "Price"]]
usd = usd[["Date", "Price"]]
cpi = cpi[["Tarih", "TP_GENENDEKS_T1"]]

bist.rename(columns={"Price": "BIST 100"}, inplace=True)
usd.rename(columns={"Price": "USDTRY"}, inplace=True)
cpi.rename(columns={"Tarih": "Date", "TP_GENENDEKS_T1": "CPI"}, inplace=True)
#since CPI is sourced from Turkish, I adjusted the names to ensure compatibility

bist["Date"] = pd.to_datetime(bist["Date"], errors="coerce")
usd["Date"] = pd.to_datetime(usd["Date"], errors="coerce")
cpi["Date"] = pd.to_datetime(cpi["Date"], errors="coerce")
#since the CPI data is in Turkish format, I'm setting the data to the same datetime format
#"coerce" converts non-transformable data to NaN.

bist = bist.dropna(subset=["Date"])
usd = usd.dropna(subset=["Date"])
cpi = cpi.dropna(subset=["Date"])
#I am deleting the NaN values

bist["BIST 100"] = bist["BIST 100"].astype(str).str.replace(",", "", regex=False )
usd["USDTRY"] = usd["USDTRY"].astype(str).str.replace(",", "", regex=False )
#I removed the commas from the string values

bist["BIST 100"] = pd.to_numeric(bist["BIST 100"], errors="coerce")
usd["USDTRY"] = pd.to_numeric(usd["USDTRY"], errors="coerce")
cpi["CPI"] = pd.to_numeric(cpi["CPI"], errors="coerce")
#I converted the string values to int or float
#"coerce" converts non-transformable data to NaN

bist = bist.dropna(subset=["BIST 100"])
usd = usd.dropna(subset=["USDTRY"])
cpi = cpi.dropna(subset=["CPI"])
#I am deleting the NaN values


bist["Date"] = bist["Date"].dt.to_period("M")
usd["Date"] = usd["Date"].dt.to_period("M")
cpi["Date"] = cpi["Date"].dt.to_period("M")
#To examine the datetime values on a monthly basis, I converted each data point to a monthly record

bist = bist.sort_values("Date")
usd = usd.sort_values("Date")
cpi = cpi.sort_values("Date")
#I sorted the data dates from smallest to largest


df = bist.merge(usd, on="Date", how="inner").merge(cpi, on="Date", how="inner")
#I combined the datasets and used how="inner" to examine the common data


#I calculate monthly returns using the percentage change formula // (P1-P0/P0)*100 -> P=Price
df["bist_return"] = df["BIST 100"].pct_change() * 100
df["usd_return"] = df["USDTRY"].pct_change() * 100
df["cpi_return"] = df["CPI"].pct_change() * 100
df["real_bist_return"] = df["bist_return"] - df["cpi_return"]

#pct_change sets the initial value to NaN
#Using it to remove the initial value.
df= df.dropna()

print(len(df))
print(df.head())
print(df.tail())

#correlation analysis
print(df[["bist_return", "usd_return", "cpi_return", "real_bist_return"]].corr())



df["Date"] = df["Date"].astype(str)
#Convert Date to a str type(to avoid problems in the drawings)

#LINECHART

fig, ax = plt.subplots(figsize=(14, 6))
plt.plot(df["Date"], df["bist_return"], label="BIST Return")
plt.plot(df["Date"], df["usd_return"], label="USD/TRY Change")
plt.plot(df["Date"], df["cpi_return"], label="Inflation Rate")
#label used for naming legend in graphics

plt.legend()

plt.title("Time Series of BIST 100 Returns, USD/TRY Changes and Inflation Rate (2022-2026)")

plt.xlabel("Date")
#used for naming axis x

plt.ylabel("Percentage Change (%)")
#used for naming axis y

plt.xticks(df["Date"][::3], rotation=45)
#dates will be displayed every 3 months and written at a 45-degree angle

#automatically configures graphic elements from being hidden
plt.tight_layout()
plt.savefig("line_chart.png", dpi=300, bbox_inches="tight")
plt.show()


#REAL RETURN GRAPHIC

plt.figure(figsize=(14, 5))

plt.plot(df["Date"], df["real_bist_return"], label="Real BIST Return")
plt.legend()

plt.title("Real BIST 100 Returns (Inflation Adjusted)")
plt.xlabel("Date")
plt.ylabel("Percentage Change (%)")

plt.xticks(df["Date"][::3], rotation=45)

plt.tight_layout()
plt.savefig("real_return.png", dpi=300, bbox_inches="tight")
plt.show()



#SCATTER PLOT
x = df["usd_return"]
y = df["bist_return"]

m, b = np.polyfit(x, y, 1)
#simple linear regression calculation

plt.figure(figsize=(8, 6))
plt.scatter(x, y, label="Data")
plt.plot(x, m*x + b, color="red", label="Trend Line")


plt.title("Relationship Between USD/TRY Changes and BIST 100 Returns")
plt.xlabel("USD/TRY Change (%)")
plt.ylabel("BIST Return (%)")

plt.tight_layout()
plt.savefig("scatter.png", dpi=300, bbox_inches="tight")
plt.show()



























