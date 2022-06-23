import spacy
from collections import Counter


def nlp_analysis (user_responses):
    """Returns the relevant topics for analysis usage
    
    takes in a list of user responses in string format and performs nlp analysis
    
    Returns:
    (dict) unordered dict of topics from mentee responses collection
  
    """

    nlp = spacy.load("en_core_web_sm")
   
    list_responses=[token.lemma_.lower() for x in user_responses for token in nlp(x) if not token.is_stop
                                    and not token.is_punct and (token.pos_ == 'ADJ'
                                                                or token.pos_ == 'VERB'
                                                                or token.pos_ == 'NOUN')]
   
    return dict(Counter(list_responses))
