import os
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize
import pyLDAvis.gensim_models
import nltk
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set NLTK data path (only needed if nltk data is not in the default location)
nltk.data.path.append('/Users/vidhishakamat/nltk_data')

# Download NLTK data (only once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the dataset
DATA_PATH = "./data/crawled/emails.csv"  # Adjust the path if necessary
emails_df = pd.read_csv(DATA_PATH)
emails_df = emails_df.head(100)  # Limiting to first 100 rows for quick testing

# Combine NLTK and additional stopwords
stop_words = set(stopwords.words('english'))

# Function to clean and preprocess email text
def preprocess_email(email):
    if not isinstance(email, str):  # Check if the input is a string
        return ''
    
    # Remove headers like 'To', 'From', and 'Subject'
    email = re.sub(r'(To|From|Subject):.*', '', email, flags=re.MULTILINE)
    
    # Remove special characters, numbers, and extra spaces
    email = re.sub(r'[^a-zA-Z\s]', '', email)
    
    # Convert text to lowercase and tokenize
    email = email.lower()
    words = word_tokenize(email)
    
    # Remove stopwords
    words = [word for word in words if word not in stop_words]
    
    return ' '.join(words)

# Test the preprocessing function with a sample email
test_email = "This is a test email. Check if the tokenization works."
processed_content = preprocess_email(test_email)
print("Processed Email Content:", processed_content)

# Apply preprocessing to the email content in the dataframe
emails_df['ProcessedContent'] = emails_df['EmailContent'].apply(preprocess_email)

# Remove rows with empty processed content
emails_df = emails_df[emails_df['ProcessedContent'].map(len) > 0]

# Create dictionary and corpus
dictionary = corpora.Dictionary(emails_df['ProcessedContent'].apply(lambda x: x.split()))
corpus = [dictionary.doc2bow(text.split()) for text in emails_df['ProcessedContent']]

# Train the LDA model
NUM_TOPICS = 2  # You can experiment with the number of topics
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=NUM_TOPICS, passes=15, random_state=42)

# Display topics
print("Generated Topics:")
for idx, topic in lda_model.print_topics(num_words=10):
    print(f"Topic {idx}: {topic}")

# Visualize the topics using pyLDAvis
# Define the path to the local CSS file
local_css_path = 'file:///' + os.path.abspath('static/css/ldavis.v1.0.0.css')

# Prepare the LDA visualization
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

# Show the visualization in a browser
pyLDAvis.display(vis)

# Save visualization to HTML
VISUALIZATION_PATH = "./lda_visualization.html"
pyLDAvis.save_html(vis, VISUALIZATION_PATH)
print(f"LDA visualization saved to {VISUALIZATION_PATH}")

# Evaluate the model with coherence score
from gensim.models.coherencemodel import CoherenceModel

coherence_model_lda = CoherenceModel(model=lda_model, texts=emails_df['ProcessedContent'].apply(lambda x: x.split()), dictionary=dictionary, coherence='c_v')
coherence_score = coherence_model_lda.get_coherence()
print(f"Coherence Score: {coherence_score}")
