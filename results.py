import pandas as pd
import datetime
import csv
from collections import Counter 

MY_DICT_INDIA = {'Q1': '30 June 1948',
 'Q2': 'India, that is Bharat',
 'Q3': 'Prime Minister alone',
 'Q4': 'He was at Noakhalli in Bengal trying to pacify bloody communal violence due to partition.',
 'Q5': 'To vote in Lok Sabha and Vidhan Sabha elections',
 'Q6': 'Shah-Jahan',
 'Q7': 'Labour Party',
 'Q8': 'Name for the British government\'s rule over India.',
 'Q9': 'Both I and II',
 'Q10': 'Rajasthan'}

MY_DICT_MARVEL = {'Q1': 'Scarlet Witch and Quicksilver',
 'Q2': 'Heart-Shaped Herb',
 'Q3': 'The Black Order',
 'Q4': 'Vibranium',
 'Q5': 'I am Groot',
 'Q6': 'The Collector',
 'Q7': 'Peggy Carter',
 'Q8': 'Loki',
 'Q9': 'Eye of Agamotto',
 'Q10': 'Queens'}

def calculate_scores(fileName, quiz_name):
    df = pd.read_csv(fileName)
    df['start_time'] = df['start_time'].astype('datetime64[ns]') 
    df['end_time'] = df['end_time'].astype('datetime64[ns]')
    all_scores = {}
    if quiz_name == 'marvel':
        quiz_answers = MY_DICT_MARVEL
    elif quiz_name == 'india':
        quiz_answers = MY_DICT_INDIA
    for index, row in df.iterrows():
        player_score = 0
        correct_answers = 0
        wrong_answers = 0
        answers = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10']
        for answer in answers:
            if(row[answer]==quiz_answers[answer]):
                correct_answers += 1
                player_score += 10
            else:
                wrong_answers += 1
        all_scores[row['Name']] = {}
        all_scores[row['Name']]['score'] = player_score
        all_scores[row['Name']]['correct_answers'] = correct_answers
        all_scores[row['Name']]['wrong_answers'] = wrong_answers
        elapsed_time = row['end_time'] - row['start_time']
        all_scores[row['Name']]['time'] = elapsed_time.total_seconds()
    return all_scores

def write_to_csv(scores, quiz):
    df = pd.DataFrame(scores)
    df = df.transpose()
    df.sort_values(by=['score','time'], inplace=True, ascending = False)
    print(df)
    if (quiz=='marvel'):
        fileName = 'scores_marvel.csv'
    elif quiz == 'india':
        fileName = 'scores_india.csv'
    else: 
        fileName = 'cumulative_scores.csv'
    df.to_csv(fileName)

def get_cumulative(marvel, india):
    cumulative_scores = {}
    for key in marvel:
        cumulative_scores[key] = {}
        if key in india:
            cumulative_scores[key]['score'] = marvel[key]['score'] + india[key]['score']
            cumulative_scores[key]['correct_answers'] = marvel[key]['correct_answers'] + india[key]['correct_answers']
            cumulative_scores[key]['wrong_answers'] = marvel[key]['wrong_answers'] + india[key]['wrong_answers']
            cumulative_scores[key]['time'] = marvel[key]['time'] + india[key]['time']
        else:
            cumulative_scores[key]['score'] = marvel[key]['score']
            cumulative_scores[key]['correct_answers'] = marvel[key]['correct_answers']
            cumulative_scores[key]['wrong_answers'] = marvel[key]['wrong_answers']
            cumulative_scores[key]['time'] = marvel[key]['time']
    for key in india: 
        if key not in cumulative_scores:
            cumulative_scores[key] = {}
            cumulative_scores[key]['score'] = india[key]['score']
            cumulative_scores[key]['correct_answers'] = india[key]['correct_answers']
            cumulative_scores[key]['wrong_answers'] = india[key]['wrong_answers']
            cumulative_scores[key]['time'] = india[key]['time']

    return cumulative_scores

        
    

def main():
    fileName1 = 'marvel_results.csv'
    fileName2 = 'test.csv'
    marvel_scores = calculate_scores(fileName1, 'marvel')
    india_scores = calculate_scores(fileName2, 'india')
    cumulative_scores = get_cumulative(marvel_scores, india_scores)
    write_to_csv(marvel_scores, 'marvel')
    write_to_csv(india_scores, 'india')
    write_to_csv(cumulative_scores, 'cumulative')


if __name__ == "__main__":
    main()