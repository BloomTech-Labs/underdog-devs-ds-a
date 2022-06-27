import spacy
from collections import Counter


def nlp_analysis (user_responses):
    """Returns relevant topics
    
    takes responses performs nlp analysis
    
    Returns:
    unordered (dict)topics from mentee responses collection
  
    """

    nlp = spacy.load("en_core_web_sm")
   
    responses_list=[]
    for word in user_responses:
        for token in nlp(word):
            if token.pos_ in('ADJ','VERB','NOUN'):
                responses_list.append(token.lemma_.lower())
   
    return dict(Counter(responses_list))
