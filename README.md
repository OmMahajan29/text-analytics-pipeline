Project overview
An end-to-end article text analysis pipeline that reads URLs from an Excel file, scrapes only title/body content, computes sentiment and readability metrics, and exports a template-aligned Excel report. The workflow is split into extraction, metrics, and orchestration for clarity and maintainability.

How the solution is approached

Clear separation of responsibilities

extract.py: Fetch pages, strip boilerplate (scripts, nav, header, footer, aside), and keep only article title and paragraph text; save one .txt per URL_ID in Text/.

metrics.py: Computes metrics:

Sentiment: Positive Score, Negative Score, Polarity, Subjectivity.

Readability: Average Sentence Length, Percentage of Complex Words, Fog Index.

Structure/Counts: Complex Word Count, Word Count (stopwords removed), Syllables per Word, Personal Pronouns, Average Word Length.

analyze.py: Orchestrates the run—reads Input.xlsx, triggers scraping if needed, computes metrics, matches Output Data Structure.xlsx columns, writes Output.xlsx.

Content extraction strategy

Use realistic HTTP headers (User-Agent, Accept, Accept-Language, Referer) to reduce 403/406 blocks.

Prefer known article containers (e.g., div.td-post-content). If missing, fall back to all paragraph tags.

Remove header, footer, nav, aside, script, and style nodes to keep only article content.

Text cleaning and tokenization

Tokenize sentences and words; keep alphabetic tokens.

Lowercase for dictionary matching.

Remove stopwords only for Word Count; sentiment uses the full alphabetic token set.

Metric definitions

Positive/Negative Score: Matches tokens against provided dictionaries.

Polarity: (Positive − Negative) / ((Positive + Negative) + 0.000001).

Subjectivity: (Positive + Negative) / (Total words + 0.000001).

Complex Word: > 2 syllables.

Average Sentence Length: Total words / Total sentences.

Percentage Complex Words: Complex / Total words.

Fog Index: 0.4 × (Average Sentence Length + Percentage Complex Words × 100).

Word Count: Tokens excluding provided stopwords (Original/StopWords).

Syllables per Word: Vowel-group heuristic with “-es/-ed” adjustment when count > 1.

Personal Pronouns: Count of “I, we, my, ours, us” with word boundaries (case-insensitive).

Average Word Length: Total characters / number of words.

Note: “AVG NUMBER OF WORDS PER SENTENCE” equals “AVG SENTENCE LENGTH” to satisfy the template.

Output conformance

Uses the exact column names and order from Original/Output Data Structure.xlsx.

Rounds numeric metrics to two decimals.

Saves the final report as Output.xlsx in the project root.

How to run
Prerequisites

Windows with Python 3.12 recommended.

Folder layout:

Original/

Input.xlsx

Output Data Structure.xlsx

MasterDictionary/positive-words.txt

MasterDictionary/negative-words.txt

StopWords/ (multiple .txt lists)

src/

analyze.py

extract.py

metrics.py

Text/ (auto-created if missing)

Setup

Create and activate a virtual environment:

py -3.12 -m venv venv

venv\Scripts\activate

Install dependencies:

python -m pip install --upgrade pip

pip install requests beautifulsoup4 lxml pandas numpy nltk regex openpyxl

python -m nltk.downloader punkt

Run

cd src

python analyze.py

What happens on run

For each row in Original/Input.xlsx, the script checks Text/<URL_ID>.txt.

If missing/empty, it scrapes the page and saves cleaned article text.

Computes all metrics and writes Output.xlsx at the project root.

Re-running

Delete any Text/<URL_ID>.txt to force re-scrape for that URL on the next run.

If metric logic changes, rerun python analyze.py to regenerate Output.xlsx from existing text files.
