import re

with open("data/raw_loans.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Remove unwanted characters
text = re.sub(r'\s+', ' ', text)
text = re.sub(r'[^A-Za-z0-9.,%()₹\- ]+', ' ', text)

# Remove duplicate sentences
sentences = list(dict.fromkeys(text.split(". ")))
clean_text = ". ".join(sentences)

with open("data/clean_loans.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("✅ Clean data prepared!")
