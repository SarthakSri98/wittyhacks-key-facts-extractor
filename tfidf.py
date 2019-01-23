import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize , sent_tokenize
import math
from operator import attrgetter

nltk.download('punkt')


text = """Sport (British English) or sports (American English) includes all forms of competitive physical activity or games which,[1] through casual or organised participation, aim to use, maintain or improve physical ability and skills while providing enjoyment to participants, and in some cases, entertainment for spectators.[2] Hundreds of sports exist, from those between single contestants, through to those with hundreds of simultaneous participants, either in teams or competing as individuals. In certain sports such as racing, many contestants may compete, simultaneously or consecutively, with one winner; in others, the contest (a match) is between two sides, each attempting to exceed the other. Some sports allow a "tie" or "draw", in which there is no single winner; others provide tie-breaking methods to ensure one winner and one loser. A number of contests may be arranged in a tournament producing a champion. Many sports leagues make an annual champion by arranging games in a regular sports season, followed in some cases by playoffs."""


def remove_string_special_characters(s):
    #Replace special characters with ' '
    stripped =re.sub('[^\w\s]','',s)
    stripped = re.sub('_','',stripped)

    #change any whitespace to one space
    stripped=re.sub('\s+',' ',stripped)

    #remove start and end white spaces
    stripped =stripped.strip()

    return stripped

def get_doc(sent):

    doc_info =[]
    i=0
    for sent in text_sents_clean:
         i+=1
         count =count_words(sent)
         temp = {'doc_id': i, 'doc_length': count}
         doc_info.append(temp)
    return doc_info

def count_words(sent):
    count =0
    words =word_tokenize(sent)
    for word in words:
       count+=1
    return count

def create_freq_dict(sents):
    i=0
    freqDict_list = []
    for sent in sents:
        i += 1
        freq_dict = {}
        words = word_tokenize(sent)
        for word in words:
            word=word.lower()
            if word in freq_dict:
                freq_dict[word] +=1
            else:
                freq_dict[word] =1
            temp= {'doc_id' : i,'freq_dict':freq_dict}
        freqDict_list.append(temp)

    return freqDict_list

def computeTF(doc_info,freqDict_list):
    """
    tf =(frequency of the term in the doc/total number of terms in the doc
    :param doc_info:
    :param freqDict_list:
    :return:
    """
    TF_scores =[]
    for tempDict in freqDict_list:
        id = tempDict['doc_id']
        for k in tempDict['freq_dict']:
            temp ={'doc_id' :id,
                   'TF_score' : tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                   'key' :k
                   }
            TF_scores.append(temp)

    return TF_scores


def computeIDF(doc_info,freqDict_list):
    """
    idf=ln(total number of docs/number of docs with term in it)
    :param doc_info:
    :param freqDict_list:
    :return:
    """
    IDF_scores =[]
    counter =0
    for dict in freqDict_list:
        counter +=1
        for k in dict['freq_dict'].keys():
            count =sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp ={'doc_id' : counter, 'IDF_score' : math.log(len(doc_info)/count),'key':k}

            IDF_scores.append(temp)
    return IDF_scores

def computeTFIDF(TF_scores,IDF_scores):
    TFIDF_scores = []
    for j in IDF_scores:
        for i in TF_scores:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id' : j['doc_id'],'TFIDF_score' : j['IDF_score']*i['TF_score'],'key' : i['key']}
        TFIDF_scores.append(temp)
    return TFIDF_scores

text_sents = sent_tokenize(text)
text_sents_clean =[remove_string_special_characters(s) for s in text_sents ]
doc_info = get_doc(text_sents_clean)

freqDict_list=create_freq_dict(text_sents_clean)
TF_scores =computeTF(doc_info,freqDict_list)
IDF_scores = computeIDF(doc_info,freqDict_list)
TFIDF_scores = computeTFIDF(TF_scores,IDF_scores)

# print(text_sents)
#
# print(text_sents_clean)
#
print(doc_info)
#
# print(freqDict_list)

# print(TF_scores)
#
# print(IDF_scores)

print(TFIDF_scores)
a=1
sum=0
sum1=[]

for i in TFIDF_scores:
    if i["doc_id"] == a:
        sum = sum + i["TFIDF_score"]
    else:
        a = a+1
        sum1.append(sum)
        sum=0

# print(sum1)
z=len(doc_info)


data_list=[]
for i in range(0, z):
    temp1 = {'score': sum1[i-1], 'content': text_sents_clean[i-1]}
    print(temp1)
    data_list.append(temp1)

for i in range(0,z-1):
    for j in range(i+1,z-1):
        if (data_list[i]["score"])<(data_list[j]["score"]):
            data_list[i],data_list[j] = data_list[j],data_list[i]
            # print("hello")



print(data_list)