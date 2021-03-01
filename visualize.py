import pandas as pd
import matplotlib.pyplot as plt

name_of_sneaker_model='Nike SB'

def clean_stockx_dataframe(df):
    # drop duplicates
    df = df.drop_duplicates()

    # clean average_sale_price
    df = df[df['average_sale_price'].notna()]
    df['average_sale_price'] = df['average_sale_price'].str[1:]
    df['average_sale_price'] = df['average_sale_price'].str.replace(',','')
    df['average_sale_price'] = df['average_sale_price'].astype(int)
    df = df[df['average_sale_price'] < 1000]

    # clean retail_price
    df = df[df['retail_price'].notna()]
    df['retail_price'] = df['retail_price'].str[1:]
    df['retail_price'] = df['retail_price'].str.replace(',','')
    df['retail_price'] = df['retail_price'].astype(int)
    return df

df = pd.read_csv('../StockX-Scraper/data/sneakers/nike/sb/nikesb.csv')
df = clean_stockx_dataframe(df)

print(df)
print(df['average_sale_price'])


fig = plt.figure(figsize=(14,9))
n, bins, patches = plt.hist(x=df['average_sale_price'], bins='auto', color='#0504aa',
                            alpha=.7,rwidth=.85,range=[0,df['average_sale_price'].max()])
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Mean Resale Price of Different ' + name_of_sneaker_model + ' Releases (in $USD)')
plt.ylabel('Frequency')
plt.title('Resale Prices of ' + name_of_sneaker_model + ' Sneakers (n='+str(len(df['average_sale_price']))+')')


mu = df['average_sale_price'].mean()
std = df['average_sale_price'].std()

# Mean resale price line
plt.vlines(x=mu,ymin=0,ymax=n.max()+10,colors=['red'])
plt.text(mu+5, n.max()+7, r'$\mu='+'{0:.2f}'.format(mu)+'$  $\sigma=$'+'{0:.2f}'.format(std))

# Mean Retail Price line
plt.vlines(x=df['retail_price'].mean(),ymin=0,ymax=n.max()+10,colors=['orange'])
plt.text(df['retail_price'].mean()+5, n.max()+2, r'Mean Retail Price:' + '{0:.2f}'.format(df['retail_price'].mean()))

#plt.show()
plt.draw()
plt.savefig('output.png')
