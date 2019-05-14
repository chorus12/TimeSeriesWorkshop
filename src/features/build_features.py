# -*- coding: utf-8 -*-
from os import listdir, path
from pandas import read_csv, DataFrame, concat
from pathlib import Path
from datetime import datetime
import sys
from glob import glob
from sklearn.preprocessing import OneHotEncoder

def build_features_for_a_file(filename, sep='\t'):
    """ Builds a dataset with full-feature-set for one input file
        Parameters:
            filename - name of a file to read the input data
            sep - separator in the CSV-file (tab by default)
        Output:
            returns a feature-rich dataframe
    """
    print("Processing file %s"%filename)
    df = read_csv(filename, sep=SEP, parse_dates=['datetime'])
    df['weekday'] = df['datetime'].apply(lambda x: x.weekday())
    df['hour'] = df['datetime'].apply(lambda x: x.hour)
    # Переведем данные о дне недели и часе в отдельные признаки
    # через OneHotEncoder
    onehotencoder = OneHotEncoder(sparse=False, categories='auto', dtype=int)
    weekday_hour_encoded = onehotencoder.fit_transform(df[['weekday', 'hour']])
    weekday_columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hour_columns = ['hour_'+str(item) for item in range(0, 24)]
    df = concat([df, DataFrame(weekday_hour_encoded, columns=weekday_columns + hour_columns)], axis=1)

    # сделаем тоже самое с погодой
    onehotencoder_weather = OneHotEncoder(sparse=False, categories='auto', dtype=int)
    weather_encoded = onehotencoder_weather.fit_transform(df[['weather']])
    weather_columns = ['weather_1', 'weather_2', 'weather_3']
    df = concat([df, DataFrame(weather_encoded, columns = weather_columns)], axis=1)
    print(df.info())
    return(df)

def main():
    """ Runs feature-generation scripts to turn interim data from (../interim) into
        feature-rich data ready to be analyzed (saved in ../processed).
    """
    files = glob(path.join(project_dir, 'data/interim/*.csv'))

    for file in files:
        df = build_features_for_a_file(file, SEP)
        file_name = path.splitext(path.basename(file))[0]+'_with_features.csv'
        # save data to the output file
        df.to_csv(path.join(project_dir, 'data/processed/', file_name), sep=SEP, index=False)


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    # separator  for the CSV-file
    SEP = '\t'

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables

    main()
