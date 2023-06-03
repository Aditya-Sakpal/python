#IMPORTING ALL THE FILES
import pandas as pd
from bs4 import BeautifulSoup
import requests
import glob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import openpyxl
from nltk.sentiment import SentimentIntensityAnalyzer
import string

#HERE I HAVE EXTENDED THE LIST OF STOPWORDS PROVIDED BY NLTK WITH THE STOPWORDS THAT YOU PROVIDED
file_paths=glob.glob('StopWords'+'/*.txt')
for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.read().split('\n')
            stop_words = []
            for word in words:
                 stop_words.extend(word.split('|')) 
                 stop_words.extend(set(stopwords.words('english')))

#FUNCTION FOR REMOVING THE STOP WORDS
def remove_stop_words(text,stop_words):
    words=word_tokenize(text)
    filtered_words=[word for word in words if word.casefold() not in stop_words]
    filtered_text=' '.join(filtered_words)
    return filtered_words
                 
#FUNCTION FOR EXTRACTING TEXT FROM THE URLS
def extraction(url,output_file):
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    p_tag=soup.find_all('p')                      
    try:
       title=soup.find('h1').get_text() 
       extracted_text=[p.get_text() for p in p_tag]
       extracted_text.insert(0,title)
       extracted_text='\n'.join(extracted_text)
       with open('text_files/'+output_file,'w',encoding='utf-8')as file:
           file.write(extracted_text)
    except Exception:
        extracted_text="Ooops... Error 404,Sorry, but the page you are looking for doesn't exist."
        with open('text_files/'+output_file,'w',encoding='utf-8')as file:
            file.write(extracted_text)
        print("Exception")    
           
#READING THE INPUT FILE
df=pd.read_excel('Input.xlsx')

#LOOP FOR EXTRACTING TEXT FROM THE URLS AND SAVING INTO TEXT FILES (URL_ID.TXT)
count=37
for i in df['URL']:
    print(count)
    extraction(i,str(count))
    count+=1


sia=SentimentIntensityAnalyzer()

#FUNCTION FOR COUNTING VOWEL IN A WORD
def count_vowels(word):
    vowels = "aeiou"
    count = 0
    if not word.endswith(("es", "ed")):  
        for char in word:
            if char.lower() in vowels:
                count += 1
    return count

#DEFINING LIST FOR STORING ALL THE RECORDS
positive_score_lst=['POSITIVE SCORE']
negative_score_lst=['NEGATIVE SCORE']
polarity_score_lst=['POLARITY SCORE']
subjectivity_score_lst=['SUBJECTIVITY SCORE']
avg_sentence_length_lst=['AVG SENTENCE LENGTH']
percentage_complex_words_lst=['PERCENTAGE OF COMPLEX WORDS']
fog_index_lst=['FOG INDEX']
avg_words_per_sentence_lst=['AVG NUMBER OF WORDS PER SENTENCE']
complex_word_count_lst=['COMPLEX WORD COUNT']
word_count_lst=['WORD COUNT']
syllable_per_word_lst=['SYLLABLE PER WORD']
personal_pronoun_count_lst=['PERSONAL PRONOUNS']
avg_word_length_lst=['AVG WORD LENGTH']

#LOOP FOR EVALUATING SCORES FOR EACH TEXT EXTRACTED FROM THE URLS AND STORING THEM INTO THE LISTS
count=37
for x in range(114):
    with open('text_files\\'+str(count),'r', encoding='utf-8')as file:
        text=file.read()
    sentences=nltk.sent_tokenize(text)
    sentence_lengths = [len(nltk.word_tokenize(sentence)) for sentence in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    avg_sentence_length_lst.append(avg_sentence_length)

    word_list=word_tokenize(text)    

    complex_words=len([word for word in word_list if word.lower() not in stop_words and
                             word.lower() not in string.punctuation])
    complex_word_count_lst.append(complex_words)

    percentage_complex_words=(complex_words/len(word_list))*100
    percentage_complex_words_lst.append(percentage_complex_words)

    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    fog_index_lst.append(fog_index)

    personal_pronouns = ['I', 'me', 'my', 'mine', 'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers',
                         'we', 'us', 'our', 'ours', 'they', 'them', 'their', 'theirs']
    personal_pronoun_count = sum(word.lower() in personal_pronouns for word in word_list)
    personal_pronoun_count_lst.append(personal_pronoun_count)

    avg_words_per_sentence = len(word_list) / len(sentences)
    avg_words_per_sentence_lst.append(avg_words_per_sentence)

    word_lengths = [len(word) for word in word_list]
    avg_word_length = sum(word_lengths) / len(word_lengths)
    avg_word_length_lst.append(avg_word_length)

    word_count = len(word_list)   
    word_count_lst.append(word_count)

    vowel_counts=0
    for j in word_list:
        vowel_counts += count_vowels(j)
    syllable_per_word=vowel_counts/word_count
    syllable_per_word_lst.append(syllable_per_word)

    filtered_words = [word for word in word_list if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_words)
    sentiment_scores=sia.polarity_scores(filtered_text)
    positive_score=sentiment_scores['pos']
    positive_score_lst.append(positive_score)

    negative_score=sentiment_scores['neg']
    negative_score_lst.append(negative_score)

    polarity_score=sentiment_scores['compound']
    polarity_score_lst.append(polarity_score)

    subjectivity_score=(negative_score+positive_score)/(len(filtered_words)+0.000001)
    subjectivity_score_lst.append(subjectivity_score)
    count+=1
    print(x,positive_score_lst)

#FUNCTION FOR INSERTING DATA INTO THE OUTPUT FILE
def write_to_excel(file_path, sheet_name, column, values):
   
    workbook = openpyxl.load_workbook(file_path)

   
    sheet = workbook[sheet_name]

    for i, value in enumerate(values, start=1):
        cell = sheet[column + str(i)]
        cell.value = value

    workbook.save(file_path)


file_path = 'output.xlsx'  
sheet_name = 'Sheet1'       

#INSERTING THE DATA INTO THEIR RESPECTIVE COLUMNS
column = 'C'                
write_to_excel(file_path, sheet_name, column,positive_score_lst)

column = 'D'                
write_to_excel(file_path, sheet_name, column,negative_score_lst)

column = 'E'                
write_to_excel(file_path, sheet_name, column,polarity_score_lst)

column = 'F'                
write_to_excel(file_path, sheet_name, column,subjectivity_score_lst)

column = 'G'                
write_to_excel(file_path, sheet_name, column,avg_sentence_length_lst)

column = 'H'                
write_to_excel(file_path, sheet_name, column,percentage_complex_words_lst)

column = 'I'                
write_to_excel(file_path, sheet_name, column,fog_index_lst)

column = 'J'                
write_to_excel(file_path, sheet_name, column,avg_words_per_sentence_lst)

column = 'K'                
write_to_excel(file_path, sheet_name, column,complex_word_count_lst)

column = 'L'                
write_to_excel(file_path, sheet_name, column,word_count_lst)

column = 'M'                
write_to_excel(file_path, sheet_name, column,syllable_per_word_lst)

column = 'N'                
write_to_excel(file_path, sheet_name, column,personal_pronoun_count_lst)

column = 'O'                
write_to_excel(file_path, sheet_name, column,avg_word_length_lst)



