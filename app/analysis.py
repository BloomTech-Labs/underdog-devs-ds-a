import spacy
import pandas as pd
import numpy as np

def nlp_analysis (user_responses):
    """Returns the top n most relevant topics for analysis usage
    
    takes in a list of user responses in string format and performs nlp analysis
    
    Returns:
    the top n most relavant topics from the responses collection
  
    """

    nlp = spacy.load("en_core_web_sm")
    responses_tokenized = []

    for x in user_responses:
        responses_tokenized.append([token.lemma_.lower() for token in nlp(x) if not token.is_stop
                                    and not token.is_punct and (token.pos_ == 'ADJ'
                                                                or token.pos_ == 'VERB'
                                                                or token.pos_ == 'NOUN')])

    flat_list = list(np.concatenate(responses_tokenized).flat)

    data_frame = pd.DataFrame(data=pd.value_counts(flat_list), columns=['count'])
    data_frame['responses'] = data_frame.index
    data_frame.reset_index(drop=True,inplace=True)
    responses_dict = dict(zip(data_frame['responses'], data_frame['count']))

    return responses_dict
