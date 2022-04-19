from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# max_df allows us to ignore terms with a document frequency greater than .8
tfidf_vect = TfidfVectorizer(max_df=.8, stop_words='english')

def cleaner(text):
    """
    Removes extra spaces, symbols, and punctuation from string.
    
    Parameters: text - string
    Returns: a lowercased version of the string
    """


    text = text.replace('\n', ' ')
    text = re.sub('[^a-z A-Z0-9]', '', text)
    text = re.sub('[ ]{2, }', ' ', text)

    return text.lower().strip()


def topicizer(texts, num_topics = 5, len_topic_repr = 5):
    """
    Accepts a list of documents, cleans and transforms each document into a
    dimensional vector, then uses non-negative matrix factorization along with
    inverse document frequency, and singular value decomposition dimensionality
    reduction, to return a list of topics.
    Parameters:
    
      texts      - List of length two or greater. Each element in the list
                   is a sequence of at least three space separated words, for
                   a total of at least 10 unique words within the list.
      num_topics - Positive integer. The number of topics to present the entire
                   text. Will repeat topics if a large number is specified
                   but there is not enough data.
                  
      len_topic_repr - Positive integer. The number of words that will be used
                       to represent each topic.
    Returns: A list of topic representations, each is a list
             of the most influential words for the topic.
    """


    if len(texts) >= 2:
        texts = [cleaner(x) for x in texts]
        idfm = tfidf_vect.fit_transform(texts)
        nmf = NMF(n_components=num_topics, random_state=42)
        nmf.fit(idfm)
        nmf_topics = []
        for topic in nmf.components_:
            s = topic.argsort()[-len_topic_repr:]
            component_words = [tfidf_vect.get_feature_names_out()[i] for i in s]
            nmf_topics += [component_words]
        
        return '\n\n'.join(' '.join(c) for c in nmf_topics)

    return 'Not enough text to analyze'
