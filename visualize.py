import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import sys

parser = argparse.ArgumentParser(description='Make visualizations using sneaker data')
parser.add_argument('--model', help='The name of the category/model of sneaker you are making visualizations of',
                        nargs='+', required=True)
parser.add_argument('--data', help='The .csv containing the data you want to visualize', required=True)
parser.add_argument('--visual', help='The visualization that gets made',
                        choices=['profit-hist'], default='profit-hist')
parser.add_argument('--context', help='Context for seaborn (leave default if you don\'t know what that is)',
                        choices=['paper', 'notebook', 'talk', 'poster'], default='notebook')

args = parser.parse_args(sys.argv[1:])


sns.set_theme()
sns.set(style='ticks',rc={'axes.grid':True})
sns.set_context(args.context)

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
    df = df[df['average_sale_price'] < 1000]

    # clean retail_price
    df = df[df['retail_price'].notna()]
    df['retail_price'] = df['retail_price'].str[1:]
    df['retail_price'] = df['retail_price'].str.replace(',','')
    df['retail_price'] = df['retail_price'].astype(int)
    return df

def plot_profit_histogram(df, binwidth=50):
    df['profit'] = df['average_sale_price'] - df['retail_price']

    fig = plt.figure(figsize=(14,9))
    ax = fig.add_subplot(1,1,1)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
#    ax.yaxis.grid(color='gray', linestyle='dashed')

    ax.axvline(0,0,1,color='red')
    n, bins, patches = plt.hist(x=df['profit'], bins=range(myround(df['profit'].min(),binwidth), myround(df['profit'].max() + binwidth,binwidth), binwidth), color='#0504aa',
                                alpha=.7,range=[df['profit'].min(),df['profit'].max()], edgecolor='black')

    plt.title ('Frequency of Net Profit Values For ' + name_of_sneaker_model + ' Sneaker Releases (n='+str(len(df['profit']))+')')
    plt.xlabel('Average Net Profit (Difference Between Mean Resale Price and Retail Price) in $USD')
    plt.ylabel('Frequency')
    plt.xticks(range(myround(df['profit'].min(),binwidth), myround(df['profit'].max() + binwidth,binwidth), binwidth),
        [get_numeric_string(x) for x in range(myround(df['profit'].min(),binwidth), myround(df['profit'].max() + binwidth,binwidth), binwidth)])
#    plt.vlines(0,ymin=0,ymax=n.max()+10,colors=['red'])

    plt.rcParams['axes.axisbelow'] = True

    plt.draw()
    plt.savefig('profit' + name_of_sneaker_model + '.png')

# converts a number into a string with a - in front if it's negative and a + in front if it's positive
def get_numeric_string(val):
    if val <= 0:
        return str(val)
    else:
        return "+" + str(val)

# dictionary for all plot functions
plot_dict={
    'profit-hist':plot_profit_histogram
}

# store arg values from parser
name_of_sneaker_model=' '.join(args.model)
path_to_data=args.data
plot_func=plot_dict[args.visual]

df = pd.read_csv(path_to_data)
df = clean_stockx_dataframe(df)
plot_func(df)

