

import pandas as pd
import Conv_Niederschlag
import Conv_Wasserstand
import matplotlib.pyplot as plt
import statsmodels.api as sm
import Create_lag_df



cant_list = ['AFI', 'AFT', 'ALW', 'AMW', 'ARB', 'ARI', 'BAM', 'BAS', 'BEZ', 'BNU', 'BUE', 'BUS', 'DIE', 'DIT', 'EFF', 'EPT', 'ESZ', 'FRF', 'FRI', 'GUT', 'HAI', 'HAU', 'HIW', 'HLL', 'KUE', 'LAF', 'LEI', 'LFB', 'LGA', 'LOH', 'MOE', 'MUR', 'NIE', 'OED', 'OPF', 'OTE', 'PFA', 'REG', 'REH', 'RUE', 'SHA', 'SMA', 'SNG', 'STE', 'TAE', 'UBB', 'UNK', 'UST', 'WAE', 'WAG', 'WBR', 'WIN', 'ZHBID', 'ZHMON', 'ZHNIE', 'ZHTUR', 'ZHWIN', 'ZHZEL', 'ZWK' ]

#Here the best set of precipitation measurement stations is givan but could be changed, as well as lag.
df = Create_lag_df.create_df_shift(['ARB', 'LFB', 'RUE', 'UST'], 20, "rre150d0", "Data_Precipitation/Precip_1990-2020_day_all/order_ARB_rre150d0_1_data.txt")
print("dfn:\n", df)

df_waterlts = Conv_Wasserstand.convert_waterlevel("Data_Waterlevel/2116_Pegel_Stundenmittel_1974-01-01_2020-03-01.csv", "days")[1]


#time frame func for ts
def datex(df,date_start, date_end): #format 'yyyy-mm-dd'
    maskx = (df.index > date_start) & (df.index <= date_end)
    return df.loc[maskx]

df_ts_wl = datex(df_waterlts,'1992-02-01', '2019-11-01')
df_tf = datex(df,'1992-02-01', '2019-11-01')

#now we try to fit a linReg for the chosen frame
Xi = df_tf.iloc[:].reset_index(drop=True)
Yi = df_ts_wl.Wert.reset_index(drop=True)

#add constant for linreg
Xic = sm.add_constant(Xi)
print("Xic:\n",Xic)
model = sm.OLS(endog=Yi, exog=Xic)
results = model.fit()

#Show the summary
print("Model performance:\n",results.summary())

#predict
Yp = results.predict()
plt.scatter(Xi.iloc[:,0],Yp, color = 'blue', s = 3)
plt.title("Predicted waterlevels")
plt.xlabel("Precipitation")
plt.ylabel("Waterlevel")
plt.show()

#print(results.predict(Xic.iloc[Yi.idxmax(),:].values.tolist()))
print("Real highest waterlevel:\n",Yi[Yi.idxmax()])
print("Predicted highest waterlevel:\n",results.predict().max())
#print(Xic.iloc[Yi.idxmax():])

print("Real lowest waterlevel:\n",Yi[Yi.idxmin()])
print("Predicted lowest waterlevel:\n",results.predict(Xic.iloc[Yi.idxmin(),:].values.tolist()))