# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import sys


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    df = pd.read_csv(os.path.join(project_dir, 'data/raw/bike_sharing_demand.csv'),
        parse_dates=['datetime'])
# adding date column with just the date
    df['date'] = df['datetime'].apply(lambda x: pd.to_datetime(datetime.date(x)))
# filter only data from march
    df_march = df[df['date'].isin(pd.date_range(start='2012-03-01', end='2012-03-31'))]
    df_march.drop('date', axis=1, inplace=True)
# write file to standard output
    df_march.to_csv(sys.stdout, sep='\t', index=False)


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables

    main()
