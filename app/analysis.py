import spacy
from collections import Counter


def nlp_analysis (user_responses):
    """Returns the relevant topics for analysis usage
    
    takes in a list of user responses in string format and performs nlp analysis
    
    Returns:
    (dict) unordered dict of topics from mentee responses collection
  
    """

    nlp = spacy.load("en_core_web_sm")
   
    responses_list=[]
    for word in user_responses:
        for token in nlp(word):
            if not token.is_stop and not token.is_punct and token.pos_ in('ADJ','VERB','NOUN'):
                responses_list.append(token.lemma_.lower())
   
    return dict(Counter(responses_list))
