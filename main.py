import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import pandas as pd


def transform_data_year_only(data, column_name, year):
    data = data.pop(column_name)
    data.columns = [f'{year}']
    data = data.T
    return data


def main():
    data_2015 = pd.read_csv('2015_loved_dreaded.csv')
    transform_data_year_only(data_2015, 'loved', 2015)
    data_2016 = pd.read_csv('2016_loved_dreaded.csv')
    data_2017 = pd.read_csv('2017_loved_dreaded.csv')
    data_2018 = pd.read_csv('2018_loved_dreaded.csv')
    data_2019 = pd.read_csv('2019_loved_dreaded.csv')
    data_2020 = pd.read_csv('2020_loved_dreaded.csv')
    data_2021 = pd.read_csv('2021_loved_dreaded.csv')

    # Join the dataframes
    data = pd.concat([data_2015, data_2016, data_2017, data_2018, data_2019, data_2020, data_2021])
    
    parallel_coordinates(data, 'loved', colormap=plt.get_cmap("Set2"))
    plt.show()


if __name__ == '__main__':
    main()
