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

MY_DICT_DC = {'Q1': 'Scarecrow',
'Q2': 'Paul Dano',
'Q3': 'Belle Reve Special Security Barracks',
'Q4': 'Darkseid',
'Q5': 'The Dark Knight Returns',
'Q6': 'Spider-Man',
'Q7': 'Alfred Pennyworth',
'Q8': 'Suprema',
'Q9': '1918',
'Q10': 'Tumbler'}

MY_DICT_MATHS = {
    'Q1': '719',
    'Q2': '4',
    'Q3': '29',
    'Q4':'264^{\circ}',
    'Q5': '157.7m',
    'Q6': '9^5',
    'Q7': "11-32+4\\times3-3=19",
    'Q8': '5',
    'Q9': "2,3,4,5,6,7",
    'Q10': '9',
    'Q11': '\\frac{320\sqrt{3}}{\sqrt{3}-1}',
    'Q12': 'x=39'
}

answer_key = {
        'marvel': MY_DICT_MARVEL,
        'dc': MY_DICT_DC,
        'india': MY_DICT_INDIA, 
        'maths': MY_DICT_MATHS
}

def calculate_scores(fileName, quiz_name):
    df = pd.read_csv(fileName)
    df['start_time'] = df['start_time'].astype('datetime64[ns]') 
    df['end_time'] = df['end_time'].astype('datetime64[ns]')
    all_scores = {}
    quiz_answers = answer_key[quiz_name]
    for index, row in df.iterrows():
        player_score = 0
        correct_answers = 0
        wrong_answers = 0
        if quiz_name == 'maths':
            answers = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10', 'Q11', 'Q12']
        else: 
            answers = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10']
        for answer in answers:
            if(str(row[answer])==quiz_answers[answer]):
                correct_answers += 1
                player_score += 10
            else:
                wrong_answers += 1
        all_scores[row['Email']] = {}
        all_scores[row['Email']]['score'] = player_score
        all_scores[row['Email']]['correct_answers'] = correct_answers
        all_scores[row['Email']]['wrong_answers'] = wrong_answers
        elapsed_time = row['end_time'] - row['start_time']
        all_scores[row['Email']]['time'] = elapsed_time.total_seconds()
    return all_scores

def write_to_csv(scores, quiz):
    df = pd.DataFrame(scores)
    df = df.transpose()
    df.sort_values(by=['score','time'], inplace=True, ascending = False)
    # print(df)
    if (quiz=='marvel'):
        fileName = 'results_marvel.csv'
    elif quiz == 'india':
        fileName = 'results_india.csv'
    elif quiz == 'dc':
        fileName = 'results_dc.csv'
    elif quiz == 'maths':
        fileName = 'results_maths.csv'
    else: 
        fileName = 'cumulative_scores.csv'
    df.to_csv(fileName)

def get_cumulative(list1, list2):
    cumulative_scores = {}
    for key in list1:
        cumulative_scores[key] = {}
        if key in list2:
            cumulative_scores[key]['score'] = list1[key]['score'] + list2[key]['score']
            cumulative_scores[key]['correct_answers'] = list1[key]['correct_answers'] + list2[key]['correct_answers']
            cumulative_scores[key]['wrong_answers'] = list1[key]['wrong_answers'] + list2[key]['wrong_answers']
            cumulative_scores[key]['time'] = list1[key]['time'] + list2[key]['time']
        else:
            cumulative_scores[key]['score'] = list1[key]['score']
            cumulative_scores[key]['correct_answers'] = list1[key]['correct_answers']
            cumulative_scores[key]['wrong_answers'] = list1[key]['wrong_answers']
            cumulative_scores[key]['time'] = list1[key]['time']
    for key in list2: 
        if key not in cumulative_scores:
            cumulative_scores[key] = {}
            cumulative_scores[key]['score'] = list2[key]['score']
            cumulative_scores[key]['correct_answers'] = list2[key]['correct_answers']
            cumulative_scores[key]['wrong_answers'] = list2[key]['wrong_answers']
            cumulative_scores[key]['time'] = list2[key]['time']

    return cumulative_scores

        
    

def main():
    fileName1 = 'marvel_results.csv'
    fileName2 = 'test.csv'
    fileName3 = 'dc_results.csv'
    fileName4 = 'maths.csv'
    marvel_scores = calculate_scores(fileName1, 'marvel')
    india_scores = calculate_scores(fileName2, 'india')
    dc_scores = calculate_scores(fileName3, 'dc')
    maths_scores = calculate_scores(fileName4, 'maths')
    cumulative_scores_initial = get_cumulative(marvel_scores, india_scores)
    cumulative_scores_initial2 = get_cumulative(cumulative_scores_initial, dc_scores)
    cumulative_scores_final = get_cumulative(cumulative_scores_initial2, maths_scores)
    print ('Number of participants = ', len(cumulative_scores_final))
    write_to_csv(marvel_scores, 'marvel')
    write_to_csv(india_scores, 'india')
    write_to_csv(dc_scores, 'dc')
    write_to_csv(maths_scores, 'maths')
    write_to_csv(cumulative_scores_final, 'cumulative')


if __name__ == "__main__":
    main()