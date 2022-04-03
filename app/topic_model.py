from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# will be ignoring terms with a document frequency greater than .8
tfidf_vect = TfidfVectorizer(max_df=.8, min_df=2, stop_words='english')

def cleaner(text: str):
  '''
  Return only the lowercased letters, single spaces and numeric characters of the text,
  cleaned of punctuation and unnecessary spaces
  '''
  
  text = text.replace('\n', ' ')
  text = re.sub('[^a-z A-Z0-9]', '', text)
  text = re.sub('[ ]{2, }', ' ', text)

  return text.lower().strip()
  

def topicizer(texts: list):
  '''
  Accepts a list of documents, cleans and transforms each document into a dimensional vector,
  then uses non-negative matrix factorization along with inverse document frequency
  to return a list of topics.
  '''
  
  texts = [cleaner(x) for x in texts]
  
  idfm = tfidf_vect.fit_transform(texts)
  
  # n_components is set so that six topics will be produced
  nmf = NMF(n_components=6, random_state=42)
  
  nmf.fit(idfm)
  
  nmf_topics = []

  for topic in nmf.components_:

    component_words = []
    
    # take the 10 most contributory words for the topic (essentially describes the topic)
    s = topic.argsort()[-10:]

    for x in s:

      component_words += [tfidf_vect.get_feature_names()[x]]

    nmf_topics += [component_words]
    
  return '\n\n'.join(' '.join(c) for c in nmf_topics)
  
  
  
  


