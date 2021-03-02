import pandas as pd
import matplotlib.pyplot as plt

name_of_sneaker_model='Nike SB'

def myround(x, base=5):
    return base * round(x/base)

def clean_stockx_dataframe(df):
    # drop duplicates
    df = df.drop_duplicates()

    # clean average_sale_price
    df = df[df['average_sale_price'].notna()]
    df['average_sale_price'] = df['average_sale_price'].str[1:]
    df['average_sale_price'] = df['average_sale_price'].str.replace(',','')
    df['average_sale_price'] = df['average_sale_price'].astype(int)
#    df = df[df['average_sale_price'] < 1000]

    # clean retail_price
    df = df[df['retail_price'].notna()]
    df['retail_price'] = df['retail_price'].str[1:]
    df['retail_price'] = df['retail_price'].str.replace(',','')
    df['retail_price'] = df['retail_price'].astype(int)
    return df

def plot_profit_histogram(df, binwidth=50):
    df['profit'] = df['average_sale_price'] - df['retail_price']

    print(df['profit'])

    fig = plt.figure(figsize=(14,9))
    ax = fig.add_subplot
    n, bins, patches = plt.hist(x=df['profit'], bins=range(myround(df['profit'].min(),binwidth//2), myround(df['profit'].max() + binwidth,binwidth//2), binwidth), color='#0504aa',
                                alpha=.7,range=[df['profit'].min(),df['profit'].max()], edgecolor='black')
    plt.grid(axis='y', alpha=0.75, zorder=10)
    plt.title ('Frequency of Net Profit Values For ' + name_of_sneaker_model + ' Sneaker Releases (n='+str(len(df['profit']))+')')
    plt.xlabel('Average Net Profit (Difference Between Mean Resale Price and Retail Price) in $USD')
    plt.ylabel('Frequency')
    plt.xticks(range(myround(df['profit'].min(),binwidth//2), myround(df['profit'].max() + binwidth,binwidth//2), binwidth),
        [get_numeric_string(x) for x in range(myround(df['profit'].min(),binwidth//2), myround(df['profit'].max() + binwidth,binwidth//2), binwidth)])

    plt.draw()
    plt.savefig('profit' + name_of_sneaker_model + '.png')

# converts a number into a string with a - in front if it's negative and a + in front if it's positive
def get_numeric_string(val):
    if val <= 0:
        return str(val)
    else:
        return "+" + str(val)

df = pd.read_csv('../StockX-Scraper/data/sneakers/nike/sb/nikesb.csv')
df = clean_stockx_dataframe(df)

#jack_plot(df)
plot_profit_histogram(df)
#plot_mean_resale_histogram(df)


