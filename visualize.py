import pandas as pd
import matplotlib.pyplot as plt

def clean_stockx_dataframe(df):
    df['average_sale_price'] = df['average_sale_price'].str[1:]
    df['average_sale_price'] = df['average_sale_price'].str.replace(',','')
    df['average_sale_price'] = df['average_sale_price'].astype(int)
    df = df[df['average_sale_price'] < 1000]

#    df['retail_price'] = df['retail_price'].str[1:]
#    df['retail_price'] = df['retail_price'].str.replace(',','')
#    df['retail_price'] = df['retail_price'].astype(int)
    return df

df = pd.read_csv('./air_jordan_1.csv')
df = clean_stockx_dataframe(df)

print(df)
print(df['average_sale_price'])



# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=df['average_sale_price'], bins='auto', color='#0504aa',
                            alpha=.7,rwidth=.85,range=[0,df['average_sale_price'].max()])
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Average Resale Price')
plt.ylabel('Frequency')
plt.title('Resale Prices of Jordan 1s (n='+str(len(df['average_sale_price']))+')')


mu = df['average_sale_price'].mean()
std = df['average_sale_price'].std()
plt.text(500, 100, r'$\mu='+'\${0:.2f}'.format(mu)+'$  $\sigma=$'+'{0:.2f}'.format(std))
#plt.text(-100, -12, 'Values > 1000 were removed')

plt.vlines(x=mu,ymin=0,ymax=n.max(),colors=['red'])

plt.show()
