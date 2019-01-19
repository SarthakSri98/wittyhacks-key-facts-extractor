import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize , sent_tokenize
import math
nltk.download('punkt')


text = """Narendra Damodardas Modi (pronounced [ˈnəɾendrə dɑmodəɾˈdɑs ˈmodiː] (About this soundlisten); born 17 September 1950) is an Indian politician serving as the 14th and current Prime Minister of India since 2014. He was the Chief Minister of Gujarat from 2001 to 2014, and is the Member of Parliament for Varanasi. Modi is a member of the Bharatiya Janata Party (BJP) and the Rashtriya Swayamsevak Sangh (RSS).
Born to a Gujarati family in Vadnagar, Modi helped his father sell tea as a child and later ran his own stall. He was introduced to the RSS at the age of eight, beginning a long association with the organisation. He left home after graduating from school, partly because of an arranged marriage which he rejected. Modi travelled around India for two years and visited a number of religious centres. He returned to Gujarat and moved to Ahmedabad in 1969 or 1970. In 1971 he became a full-time worker for the RSS. During the state of emergency imposed across the country in 1975, Modi was forced to go into hiding. The RSS assigned him to the BJP in 1985, and he held several positions within the party hierarchy until 2001, rising to the rank of General Secretary.
Modi was appointed Chief Minister of Gujarat in 2001, due to Keshubhai Patel's failing health and poor public image following the earthquake in Bhuj. Modi was elected to the legislative assembly soon after. His administration has been considered complicit in the 2002 Gujarat riots,[a] or otherwise criticised for its handling of it; however, a Supreme Court-appointed Special Investigation Team (SIT) found no evidence to initiate prosecution proceedings against Modi personally.[b] His policies as chief minister, credited with encouraging economic growth, have received praise.[9] His administration has been criticised for failing to significantly improve health, poverty, and education indices in the state.[c]
Modi led the BJP in the 2014 general election, which gave the party a majority in the Lok Sabha, the first time a single party had achieved this since 1984. Modi himself was elected to parliament from Varanasi. Since taking office, Modi's administration has tried to raise foreign direct investment in the Indian economy, increased spending on infrastructure, and reduced spending on healthcare and social welfare programmes. Modi has attempted to improve efficiency in the bureaucracy, and centralised power by abolishing the planning commission and replacing it with the NITI Aayog. He has begun a high-profile sanitation campaign, and weakened or abolished environmental and labour laws. Credited with engineering a political realignment towards right-wing politics, Modi remains a figure of controversy domestically and internationally over his Hindu nationalist beliefs and his role during the 2002 Gujarat riots, cited as evidence of an exclusionary social agenda.[d]"""


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
         temp ={'doc_id' :i,'doc_length' :count}
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

text_sents =sent_tokenize(text)
text_sents_clean =[remove_string_special_characters(s) for s in text_sents ]
doc_info = get_doc(text_sents_clean)

freqDict_list=create_freq_dict(text_sents_clean)
TF_scores =computeTF(doc_info,freqDict_list)
IDF_scores = computeIDF(doc_info,freqDict_list)
TFIDF_scores = computeTFIDF(TF_scores,IDF_scores)

print(text_sents)

print(text_sents_clean)

print(doc_info)

print(freqDict_list)

print(TF_scores)

print(IDF_scores)

print(TFIDF_scores)