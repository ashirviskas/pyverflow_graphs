import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import pandas as pd
import matplotlib.ticker as mtick


def transform_data_year_only(data, column_name, year):
    data.columns = ['Technology', 'loved', 'wanted', 'dreaded']
    data.set_index('Technology', inplace=True)
    data = data[[column_name]]
    data.columns = [f'{year}']
    return data


def merge_rows(data, rowname_a, rowname_b):
    # TODO: Do it properly
    data = data.T
    data[rowname_a] = data[rowname_a].fillna(data[rowname_b])
    data = data.T
    data = data.drop(rowname_b)
    return data


def main():
    data_2015 = pd.read_csv('2015_loved_dreaded.csv')
    data_2015 = transform_data_year_only(data_2015, 'loved', 2015)
    data_2016 = pd.read_csv('2016_loved_dreaded.csv')
    data_2016 = transform_data_year_only(data_2016, 'loved', 2016)
    data_2017 = pd.read_csv('2017_loved_dreaded.csv')
    data_2017 = transform_data_year_only(data_2017, 'loved', 2017)
    data_2018 = pd.read_csv('2018_loved_dreaded.csv')
    data_2018 = transform_data_year_only(data_2018, 'loved', 2018)
    data_2019 = pd.read_csv('2019_loved_dreaded.csv')
    data_2019 = transform_data_year_only(data_2019, 'loved', 2019)
    data_2020 = pd.read_csv('2020_loved_dreaded.csv')
    data_2020 = transform_data_year_only(data_2020, 'loved', 2020)
    data_2021 = pd.read_csv('2021_loved_dreaded.csv')
    data_2021 = transform_data_year_only(data_2021, 'loved', 2021)

    # Join the dataframes
    data = pd.merge(data_2015, data_2016, how='outer', left_index=True, right_index=True)
    data = pd.merge(data, data_2017, how='outer', left_index=True, right_index=True)
    data = pd.merge(data, data_2018, how='outer', left_index=True, right_index=True)
    data = pd.merge(data, data_2019, how='outer', left_index=True, right_index=True)
    data = pd.merge(data, data_2020, how='outer', left_index=True, right_index=True)
    data = pd.merge(data, data_2021, how='outer', left_index=True, right_index=True)

    # Plot the data
    data = merge_rows(data, 'Bash/Shell', 'Bash/Shell/PowerShell')
    data = data.dropna(thresh=data.shape[1] * 0.3, how='all', axis=0)
    print(f'Data points: {len(data)}')

    data.reset_index(level=0, inplace=True)
    data = data.sort_values(by=[str(i) for i in range(2021, 2015, -1)], ascending=False)
    ax = parallel_coordinates(data, 'Technology', colormap=plt.get_cmap('gist_ncar'), linewidth=3, alpha=0.8)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    plt.show()


if __name__ == '__main__':
    main()
