import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


def parse_two_fifteen_loved_dreaded(filepath):
    columns_to_use = ['Current Lang & Tech: Android', 'Current Lang & Tech: Arduino',
                      'Current Lang & Tech: AngularJS', 'Current Lang & Tech: C',
                      'Current Lang & Tech: C++', 'Current Lang & Tech: C++11',
                      'Current Lang & Tech: C#', 'Current Lang & Tech: Cassandra',
                      'Current Lang & Tech: CoffeeScript', 'Current Lang & Tech: Cordova',
                      'Current Lang & Tech: Clojure', 'Current Lang & Tech: Cloud',
                      'Current Lang & Tech: Dart', 'Current Lang & Tech: F#',
                      'Current Lang & Tech: Go', 'Current Lang & Tech: Hadoop',
                      'Current Lang & Tech: Haskell', 'Current Lang & Tech: iOS',
                      'Current Lang & Tech: Java', 'Current Lang & Tech: JavaScript',
                      'Current Lang & Tech: LAMP', 'Current Lang & Tech: Matlab',
                      'Current Lang & Tech: MongoDB', 'Current Lang & Tech: Node.js',
                      'Current Lang & Tech: Objective-C', 'Current Lang & Tech: Perl',
                      'Current Lang & Tech: PHP', 'Current Lang & Tech: Python',
                      'Current Lang & Tech: R', 'Current Lang & Tech: Redis',
                      'Current Lang & Tech: Ruby', 'Current Lang & Tech: Rust',
                      'Current Lang & Tech: Salesforce', 'Current Lang & Tech: Scala',
                      'Current Lang & Tech: Sharepoint', 'Current Lang & Tech: Spark',
                      'Current Lang & Tech: SQL', 'Current Lang & Tech: SQL Server',
                      'Current Lang & Tech: Swift', 'Current Lang & Tech: Visual Basic',
                      'Current Lang & Tech: Windows Phone', 'Current Lang & Tech: Wordpress',
                      'Current Lang & Tech: Write-In', 'Future Lang & Tech: Android',
                      'Future Lang & Tech: Arduino', 'Future Lang & Tech: AngularJS',
                      'Future Lang & Tech: C', 'Future Lang & Tech: C++',
                      'Future Lang & Tech: C++11', 'Future Lang & Tech: C#',
                      'Future Lang & Tech: Cassandra', 'Future Lang & Tech: CoffeeScript',
                      'Future Lang & Tech: Cordova', 'Future Lang & Tech: Clojure',
                      'Future Lang & Tech: Cloud', 'Future Lang & Tech: Dart',
                      'Future Lang & Tech: F#', 'Future Lang & Tech: Go',
                      'Future Lang & Tech: Hadoop', 'Future Lang & Tech: Haskell',
                      'Future Lang & Tech: iOS', 'Future Lang & Tech: Java',
                      'Future Lang & Tech: JavaScript', 'Future Lang & Tech: LAMP',
                      'Future Lang & Tech: Matlab', 'Future Lang & Tech: MongoDB',
                      'Future Lang & Tech: Node.js', 'Future Lang & Tech: Objective-C',
                      'Future Lang & Tech: Perl', 'Future Lang & Tech: PHP',
                      'Future Lang & Tech: Python', 'Future Lang & Tech: R',
                      'Future Lang & Tech: Redis', 'Future Lang & Tech: Ruby',
                      'Future Lang & Tech: Rust', 'Future Lang & Tech: Salesforce',
                      'Future Lang & Tech: Scala', 'Future Lang & Tech: Sharepoint',
                      'Future Lang & Tech: Spark', 'Future Lang & Tech: SQL',
                      'Future Lang & Tech: SQL Server', 'Future Lang & Tech: Swift',
                      'Future Lang & Tech: Visual Basic', 'Future Lang & Tech: Windows Phone',
                      'Future Lang & Tech: Wordpress', 'Future Lang & Tech: Write-In']
    df = pd.read_csv(filepath, usecols=columns_to_use, header=1)
    # TODO: Calculate loved/dreaded language ratios
    df = df.notna() * 1
    df.columns = df.columns.str.replace("Current Lang & Tech: ", "current ")
    df.columns = df.columns.str.replace("Future Lang & Tech: ", "future ")
    num_columns = df.shape[1]
    print(num_columns)

    df_first_half = df.iloc[:, :int(num_columns / 2)]
    df_first_half.columns = df_first_half.columns.str.replace("current ", "")
    df_second_half = df.iloc[:, int(num_columns / 2):]
    # Renaming columns to match the first half so we can do some magic
    df_second_half.columns = df_first_half.columns
    # logical and
    loved = (df_first_half + df_second_half) > 1
    # no 
    wanted = df_first_half < df_second_half
    # nonlogical
    dreaded = df_first_half > df_second_half

    # users nums
    users_who_use = df_first_half.sum(axis=0)
    users_who_dont_use = df_second_half.sum(axis=0)

    loved = loved.sum(axis=0) / users_who_use
    wanted = wanted.sum(axis=0) / users_who_dont_use
    dreaded = dreaded.sum(axis=0) / users_who_use

    loved = loved.T
    wanted = wanted.T
    dreaded = dreaded.T

    new_cols = ['loved', 'wanted', 'dreaded']
    new_df = pd.concat([loved, wanted, dreaded], axis=1)
    new_df.columns = new_cols

    return new_df


def parse_two_sixteen_loved_dreaded(filepath):
    columns_to_use = ['tech_do', 'tech_want']
    df = pd.read_csv(filepath, usecols=columns_to_use)
    df.dropna(inplace=True)
    # df.reset_index(inplace=True)
    df.tech_do = df.tech_do.str.split('; ')
    df.tech_want = df.tech_want.str.split('; ')

    mlb = MultiLabelBinarizer(sparse_output=True)

    mlb.fit(df['tech_do'])
    # mlb.fit(df['tech_want'])
    transformed = mlb.transform(df['tech_do'])

    do = pd.DataFrame.sparse.from_spmatrix(
            transformed,
            index=df.index,
            columns=mlb.classes_) * 1

    want = pd.DataFrame.sparse.from_spmatrix(
            mlb.transform(df['tech_want']),
            index=df.index,
            columns=mlb.classes_) * 1
    # logical and
    loved = (do + want) > 1
    # no
    wanted = (do < want) * 1
    # nonlogical
    dreaded = (do > want) * 1

    # users nums
    users_who_use = do.sum(axis=0)
    users_who_dont_use = want.sum(axis=0)

    loved = loved.sum(axis=0) / users_who_use
    wanted = wanted.sum(axis=0) / users_who_dont_use
    dreaded = dreaded.sum(axis=0) / users_who_use

    loved = loved.T
    wanted = wanted.T
    dreaded = dreaded.T

    new_cols = ['loved', 'wanted', 'dreaded']
    new_df = pd.concat([loved, wanted, dreaded], axis=1)
    new_df.columns = new_cols

    return new_df

def parse_two_seventeen_loved_dreaded(filepath):
    columns_to_use = ['HaveWorkedLanguage', 'WantWorkLanguage']
    df = pd.read_csv(filepath, usecols=columns_to_use)
    df.dropna(inplace=True)
    df.rename(columns={'HaveWorkedLanguage': 'tech_do', 'WantWorkLanguage': 'tech_want'}, inplace=True)
    # df.reset_index(inplace=True)
    df.tech_do = df.tech_do.str.split('; ')
    df.tech_want = df.tech_want.str.split('; ')

    mlb = MultiLabelBinarizer(sparse_output=True)

    mlb.fit(df['tech_do'])
    # mlb.fit(df['tech_want'])
    transformed = mlb.transform(df['tech_do'])

    do = pd.DataFrame.sparse.from_spmatrix(
            transformed,
            index=df.index,
            columns=mlb.classes_) * 1

    want = pd.DataFrame.sparse.from_spmatrix(
            mlb.transform(df['tech_want']),
            index=df.index,
            columns=mlb.classes_) * 1
    # logical and
    loved = (do + want) > 1
    # no
    wanted = (do < want) * 1
    # nonlogical
    dreaded = (do > want) * 1

    # users nums
    users_who_use = do.sum(axis=0)
    users_who_dont_use = want.sum(axis=0)

    loved = loved.sum(axis=0) / users_who_use
    wanted = wanted.sum(axis=0) / users_who_dont_use
    dreaded = dreaded.sum(axis=0) / users_who_use

    loved = loved.T
    wanted = wanted.T
    dreaded = dreaded.T

    new_cols = ['loved', 'wanted', 'dreaded']
    new_df = pd.concat([loved, wanted, dreaded], axis=1)
    new_df.columns = new_cols

    return new_df


def parse_two_eighteen_loved_dreaded(filepath):
    columns_to_use = ['LanguageWorkedWith', 'LanguageDesireNextYear']
    df = pd.read_csv(filepath, usecols=columns_to_use)
    df.dropna(inplace=True)
    df.rename(columns={'LanguageWorkedWith': 'tech_do', 'LanguageDesireNextYear': 'tech_want'}, inplace=True)
    # df.reset_index(inplace=True)
    df.tech_do = df.tech_do.str.split(';')
    df.tech_want = df.tech_want.str.split(';')

    mlb = MultiLabelBinarizer(sparse_output=True)

    mlb.fit(df['tech_do'])
    # mlb.fit(df['tech_want'])
    transformed = mlb.transform(df['tech_do'])

    do = pd.DataFrame.sparse.from_spmatrix(
            transformed,
            index=df.index,
            columns=mlb.classes_) * 1

    want = pd.DataFrame.sparse.from_spmatrix(
            mlb.transform(df['tech_want']),
            index=df.index,
            columns=mlb.classes_) * 1
    # logical and
    loved = (do + want) > 1
    # no
    wanted = (do < want) * 1
    # nonlogical
    dreaded = (do > want) * 1

    # users nums
    users_who_use = do.sum(axis=0)
    users_who_dont_use = want.sum(axis=0)

    loved = loved.sum(axis=0) / users_who_use
    wanted = wanted.sum(axis=0) / users_who_dont_use
    dreaded = dreaded.sum(axis=0) / users_who_use

    loved = loved.T
    wanted = wanted.T
    dreaded = dreaded.T

    new_cols = ['loved', 'wanted', 'dreaded']
    new_df = pd.concat([loved, wanted, dreaded], axis=1)
    new_df.columns = new_cols

    return new_df

def main():
    two_fifteen_datapath = './2015/2015 Stack Overflow Developer Survey Responses.csv'
    two_fifteen_data = parse_two_fifteen_loved_dreaded(two_fifteen_datapath)
    two_fifteen_data.to_csv('2015_loved_dreaded.csv')
    print(two_fifteen_data.head())

    two_sixteen_datapath = './2016/2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Responses.csv'
    two_sixteen_data = parse_two_sixteen_loved_dreaded(two_sixteen_datapath)
    two_sixteen_data.to_csv('2016_loved_dreaded.csv')
    print(two_sixteen_data.head())

    two_seventeen_datapath = './2017/survey_results_public.csv'
    two_seventeen_data = parse_two_seventeen_loved_dreaded(two_seventeen_datapath)
    two_seventeen_data.to_csv('2017_loved_dreaded.csv')
    print(two_seventeen_data.head())

    two_eighteen_datapath = './2018/survey_results_public.csv'
    two_eighteen_data = parse_two_eighteen_loved_dreaded(two_eighteen_datapath)
    two_eighteen_data.to_csv('2018_loved_dreaded.csv')
    print(two_eighteen_data.head())


if __name__ == '__main__':
    main()
