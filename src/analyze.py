# analyze.py
# Orchestrates the full pipeline:
# 1) Read Input.xlsx (URL_ID, URL)
# 2) Scrape article text into Text/<URL_ID>.txt (if not already present)
# 3) Compute NLP metrics per article using metrics.py
# 4) Populate an output DataFrame matching "Output Data Structure.xlsx"
# 5) Save final results to Output.xlsx

import os
import pandas as pd

# Import the scraper and saver utilities from extract.py
from extract import fetch_and_clean_article, save_article_text
# Import all metric functions from metrics.py
import metrics as m

# Absolute paths (as per your setup)
INPUT_FILE = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Original\Input.xlsx"
OUTPUT_TEMPLATE = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Original\Output Data Structure.xlsx"
TEXT_DIR = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Text"
FINAL_OUTPUT = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Output.xlsx"

def main():
    # Load the list of URLs to process
    df_in = pd.read_excel(INPUT_FILE)
    results = []  # will collect one list per row to build a DataFrame

    # Iterate over each row (URL_ID, URL)
    for _, row in df_in.iterrows():
        url_id = row["URL_ID"]
        url = row["URL"]
        txt_path = os.path.join(TEXT_DIR, f"{url_id}.txt")

        # If the text file is missing or empty, scrape now
        if not os.path.exists(txt_path) or os.stat(txt_path).st_size == 0:
            print(f"[SCRAPING] {url_id}...")
            text = fetch_and_clean_article(url)
            save_article_text(url_id, text)

        # Read the text for analysis (even if scrape failed, this will be empty string)
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Tokenize words once and reuse for multiple metrics
        words_all = m.clean_and_tokenize(text)

        # Sentiment scores based on dictionaries
        pos = m.positive_score(words_all)
        neg = m.negative_score(words_all)
        pol = m.polarity_score(pos, neg)
        subj = m.subjectivity_score(pos, neg, len(words_all))

        # Readability and related metrics
        avg_sent_len = m.avg_sentence_length(text)            # words / sentences
        pct_complex = m.percentage_complex_words(words_all)   # complex / total words
        fog = m.fog_index(avg_sent_len, pct_complex)          # 0.4 * (ASL + %complex*100)
        complex_wc = m.count_complex_words(words_all)         # count of words with >2 syllables
        wc = m.word_count_excluding_stopwords(words_all)      # word count without stopwords

        # Other structural metrics
        syll_per_word = m.syllables_per_word(words_all)       # avg syllables per word
        pronouns = m.personal_pronouns(text)                  # I, we, my, ours, us
        avg_w_len = m.avg_word_length(words_all)              # average word length in characters

        # Append results in the same order as Output Data Structure.xlsx expects
        # Note: Both "AVG SENTENCE LENGTH" and "AVG NUMBER OF WORDS PER SENTENCE" are set to avg_sent_len
        results.append([
            url_id, url, pos, neg, pol, subj,
            avg_sent_len, pct_complex, fog, avg_sent_len, complex_wc, wc,
            syll_per_word, pronouns, avg_w_len
        ])

    # Load the template to capture exact column names and order
    df_template = pd.read_excel(OUTPUT_TEMPLATE)
    columns = list(df_template.columns)

    # Build output DataFrame with matching headers
    df_out = pd.DataFrame(results, columns=columns)

    # Round numeric columns (skip URL_ID and URL which are at positions 0 and 1)
    for col in df_out.columns[2:]:
        df_out[col] = df_out[col].apply(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

    # Save the final output Excel
    df_out.to_excel(FINAL_OUTPUT, index=False)
    print(f"[DONE] Saved Output to: {FINAL_OUTPUT}")

if __name__ == "__main__":
    main()
