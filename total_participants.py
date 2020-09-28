import pandas as pd
import datetime
import csv
from collections import Counter 

def do_magic(fileName1, fileName2, fileName3, fileName4):
    df1 = pd.read_csv(fileName1)
    df2 = pd.read_csv(fileName2)
    df3 = pd.read_csv(fileName3)
    df4 = pd.read_csv(fileName4)
    final_participants = {}
    count = 0
    
    for index, row in df1.iterrows():
        if row['Email'] in final_participants:
            final_participants[row['Email']].append('marvel')
        else:
            final_participants[row['Email']] = ['marvel']
    
    for index, row in df2.iterrows():
        if row['Email'] in final_participants:
            final_participants[row['Email']].append('india')
        else:
            final_participants[row['Email']] = ['india']

    for index, row in df3.iterrows():
        if row['Email'] in final_participants:
            final_participants[row['Email']].append('dc')
        else:
            final_participants[row['Email']] = ['dc']

    for index, row in df4.iterrows():
        if row['Email'] in final_participants:
            final_participants[row['Email']].append('maths')
        else:
            final_participants[row['Email']] = ['maths']
    
    
    # df = pd.DataFrame(final_participants)
    # df = df.transpose()
    # df.to_csv('testing.csv')

    # with open("testing.csv", "wb") as outfile:
    #     writer = csv.writer(outfile)
    #     writer.writerow(final_participants.keys())
    #     writer.writerows(zip(*final_participants.values()))

    df = pd.DataFrame({key: pd.Series(value) for key, value in final_participants.items()})
    # df = df.transpose()
    df.to_csv('participants.csv', encoding='utf-8', index=False)


def main():
    fileName1 = 'marvel_results.csv'
    fileName2 = 'test.csv'
    fileName3 = 'dc_results.csv'
    fileName4 = 'maths.csv'
    do_magic(fileName1, fileName2, fileName3, fileName4)


if __name__ == "__main__":
    main()