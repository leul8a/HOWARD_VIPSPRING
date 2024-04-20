import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import nltk
from datetime import datetime
import csv

from nltk.corpus import stopwords

# Load the list of stopwords
stopwords_set = set(stopwords.words('english'))

# Function to clean and split text into words
def get_clean_words(text):
    return (x.rstrip(punctuation).title() for x in text.split() if x.rstrip(punctuation).lower() not in stopwords_set)

# Function to count words in text
def count_words(text):
    return Counter(get_clean_words(text))

# Function to get unique text from the HTML
def get_unique_text(soup):
    texts = set(soup.stripped_strings)  # Use a set to avoid duplicates
    return ' '.join(texts)

# Functions for saving the current and max word counts
def save_word_counts(word_counts, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for word, count in sorted(word_counts.items()):
            writer.writerow([word, count])

def read_max_counts(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            return {rows[0]: int(rows[1]) for rows in reader}
    except FileNotFoundError:
        return {}

def update_max_counts(current_counts, max_counts):
    for word, count in current_counts.items():
        max_counts[word] = max(max_counts.get(word, 0), count)
    return max_counts

def save_max_counts(max_counts, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for word, count in sorted(max_counts.items()):
            writer.writerow([word, count])

# Function for saving the deltas
def save_word_deltas(current_counts, previous_counts, filename):
    deltas = {word: current_counts.get(word, 0) - previous_counts.get(word, 0)
              for word in set(current_counts) | set(previous_counts)}
    with open(filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for word, delta in sorted(deltas.items()):
            writer.writerow([word, delta])
def save_word_counts_with_timestamp(word_counts):
    timestamp = datetime.now().strftime("%Y-%m-%d")  # Generate timestamp
    filename = f"word_counts_{timestamp}.txt"  # Dynamic filename with timestamp
    with open(filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for word, count in sorted(word_counts.items()):
            writer.writerow([word, count])

# Get the url content
r = requests.get("https://www.bbc.com")  # Update with your URL
soup = BeautifulSoup(r.content, "html.parser")

# Get unique text from the HTML content
unique_text = get_unique_text(soup)

# Count words in the unique text
current_counts = count_words(unique_text)

# Read the previous word counts for delta calculation
previous_counts = read_max_counts("word_counts.txt")

# Save the current word counts
save_word_counts(current_counts, "word_counts.txt")

# Calculate and save word deltas based on the previous counts
save_word_deltas(current_counts, previous_counts, "word_deltas.txt")

# Read the previous max counts and update them
max_counts = read_max_counts("max_word_counts.txt")
updated_max_counts = update_max_counts(current_counts, max_counts)

# Save the updated max counts
save_max_counts(updated_max_counts, "max_word_counts.txt")
save_word_counts_with_timestamp(current_counts)


print("Script completed, word counts and deltas have been saved.")