import pandas as pd
import urllib.request
import re

nutrition_books = {
    "Book 1: Foods and Digestion": "https://www.gutenberg.org/cache/epub/61719/pg61719.txt",
    "Book 2: Science of Nutrition": "https://www.gutenberg.org/cache/epub/26209/pg26209.txt",
    "Book 3: Diet and Health": "https://www.gutenberg.org/cache/epub/15484/pg15484.txt",
    "Book 4: Modern Diet": "https://www.gutenberg.org/cache/epub/15237/pg15237.txt",
    "Book 5: Food Recipes": "https://www.gutenberg.org/cache/epub/17438/pg17438.txt"
}

combined_paragraphs = []
character_target_per_book = 60000

for name, url in nutrition_books.items():
    print(f"Fetching {name}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            raw_text = response.read().decode('utf-8', errors='ignore')
        
        # Skip Gutenberg legal header if present
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in raw_text:
            raw_text = raw_text.split("*** START OF THE PROJECT GUTENBERG EBOOK")[1]
            
        # Split on 2+ consecutive newlines regardless of \r or \n
        paragraphs = re.split(r'[\r\n]{2,}', raw_text)
        
        current_book_chars = 0
        for p in paragraphs:
            # Collapse embedded newlines and extra spaces into a single line
            clean_p = ' '.join(p.split())
            if len(clean_p) > 20:
                combined_paragraphs.append(clean_p)
                current_book_chars += len(clean_p)
                
            if current_book_chars >= character_target_per_book:
                break
                
    except Exception as e:
        print(f"Could not load {name}: {e}")

df_multi = pd.DataFrame(combined_paragraphs, columns=['text'])
df_multi.to_csv('../data/multi_nutrition_corpus.csv', index=False)

total_chars = df_multi['text'].str.len().sum()
print(f"\nSaved {len(df_multi)} paragraphs ({total_chars:,} characters) to multi_nutrition_corpus.csv")