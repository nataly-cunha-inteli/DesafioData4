import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Parse dates: indicar que as colunas que contêm dados de data e hora devem ser convertidas para o tipo datetime
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Valores fora do intervalo de 2.5% e 97.5% são considerados outliers
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Plotagem
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['value'], color='blue', linewidth=1)

    # Customização
    plt.title('Forum Page Views')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Salvamento da imagem
    plt.savefig('line_plot.png')
    return plt.gcf()

def draw_bar_plot():
    # Cópia do DataFrame
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()  # Captar os nomes dos meses

    # Agrupamento da média de anos e meses, e cálculo da média
    df_bar = df_bar.groupby(['year', 'month']).mean()['value'].unstack()
    
    # Reordem das colunas com base na ordem correta dos meses
    df_bar = df_bar[['January', 'February', 'March', 'April', 'May', 
                     'June', 'July', 'August', 'September', 
                     'October', 'November', 'December']]

    
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar.plot(kind='bar', ax=ax)

   
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views per Month')
    ax.legend(title='Months')  # Set legend title

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Abreviação de meses

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2,
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])  # Ordem dos meses
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

def main():
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()

main()