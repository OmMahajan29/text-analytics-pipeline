Project overview

This project automates:
●	Extraction of article title and body text from each URL in Original/Input.xlsx.
●	Text cleaning and NLP metric computation as per Text-Analysis.docx.
●	Writing the results to an Excel file that matches Original/Output Data Structure.xlsx, saved as Output.xlsx.

A) How the solution is approached

1.	Clear separation of responsibilities
●	extract.py: Fetches each web page, removes non-content elements (scripts, nav, header, footer, aside), and extracts only the article title and paragraph text. It saves one .txt file per URL_ID in the Text/ folder.
●	metrics.py: Computes all required metrics from Text-Analysis.docx:
●	Sentiment: Positive Score, Negative Score, Polarity Score, Subjectivity Score.
●	Readability: Average Sentence Length, Percentage of Complex Words, Fog Index.
●	Structure/Counts: Complex Word Count, Word Count (excluding provided stopwords), Syllables per Word, Personal Pronouns, Average Word Length.
●	analyze.py: Orchestrates the pipeline—reads Input.xlsx, triggers extraction if needed, computes metrics, aligns results to the Output Data Structure.xlsx template, and writes Output.xlsx.

2.	Content extraction strategy
●	Mimic a real browser by setting realistic HTTP headers (User-Agent, Accept, Accept-Language, Referer), reducing blocks (e.g., 406/403).
●	Prefer known article containers on insights.blackcoffer.com (e.g., div.td-post-content). If not found, fall back to joining all paragraph tags.
●	Remove header, footer, nav, aside, script, and style nodes to comply with the requirement: include only article title and main article text.

3.	Text cleaning and tokenization
●	Tokenize sentences and words; retain only alphabetic tokens for metrics.
●	Lowercase tokens for dictionary matching.
●	Stopwords are only removed for the Word Count metric; for sentiment metrics, the full token set (alphabetic) is used.

4.	Metric definitions (aligned to Text-Analysis.docx)
●	Positive Score: Count of tokens present in positive-words.txt.
●	Negative Score: Count of tokens present in negative-words.txt.
●	Polarity Score: (Positive − Negative) / ((Positive + Negative) + 0.000001).
●	Subjectivity Score: (Positive + Negative) / (Total words + 0.000001).
●	Complex Word: A word with more than 2 syllables.
●	Average Sentence Length: Total words / Total sentences.
●	Percentage of Complex Words: Complex Word Count / Total words.
●	Fog Index: 0.4 × (Average Sentence Length + Percentage of Complex Words × 100).
●	Word Count: Count of words excluding all provided stopwords (from Original/StopWords).
●	Syllables per Word: Average syllables across words; syllable count approximated via vowel-group counting with an adjustment for words ending in “es” or “ed” when count>1.
●	Personal Pronouns: Count of “I”, “we”, “my”, “ours”, “us” (case-insensitive), excluding “US” via word boundaries.
●	Average Word Length: Total characters across words / number of words.
●	The column “AVG NUMBER OF WORDS PER SENTENCE” is set equal to “AVG SENTENCE LENGTH” per the typical template.

5.	Output conformance
●	The output DataFrame strictly uses the column names and order from Original/Output Data Structure.xlsx.
●	Floating metrics are rounded to 2 decimals to avoid format mismatches.
●	Output is saved to Output.xlsx in the project root.

B) How to run the project
Prerequisites
●	Windows with Python 3.12 installed (recommended).
●	The following folders/files present (as per your setup):
●	Original/
●	Input.xlsx
●	Output Data Structure.xlsx
●	MasterDictionary/positive-words.txt
●	MasterDictionary/negative-words.txt
●	StopWords/ (contains multiple stopword .txt files)
●	src/
●	analyze.py
●	extract.py
●	metrics.py
●	Text/ (will be created if missing)

1.	Create and activate a virtual environment (recommended)
●	Open a terminal in the project root (e.g., C:\Users\91897\OneDrive\Desktop\BlackCoffer Assignment).
●	py -3.12 -m venv venv
●	venv\Scripts\activate

2.	Install dependencies into the venv
●	python -m pip install --upgrade pip
●	pip install requests beautifulsoup4 lxml pandas numpy nltk regex openpyxl
●	python -m nltk.downloader punkt

3.	Run the pipeline
●	cd src
●	python analyze.py
What happens:
●	For each row in Original\Input.xlsx, the script checks Text<URL_ID>.txt.
●	If missing or empty, it scrapes the page and saves the cleaned article text.
●	It computes all metrics and writes the final results to Output.xlsx in the project root.

4.	Re-running
●	If you delete any .txt from Text/, the script will scrape that URL again on the next run.
●	If you update metric logic, just rerun python analyze.py; it will read the existing .txt files and regenerate Output.xlsx.

































C) Dependencies required
Python version
●	Python 3.12 (Windows). If you switch Python versions later, recreate the venv; old venvs tie to the original interpreter path.
Python packages
●	requests: HTTP requests for scraping
●	beautifulsoup4: HTML parsing
●	lxml: Faster, robust parser for BeautifulSoup
●	pandas: Reading/writing Excel and tabular processing
●	numpy: Numeric helpers (pandas dependency)
●	nltk: Tokenization (sentences/words)
●	regex: Advanced regular expressions (used by some environments; Python’s re is used for pronouns here)
●	openpyxl: Excel read/write engine used by pandas
Install command
●	pip install requests beautifulsoup4 lxml pandas numpy nltk regex openpyxl
NLTK data
●	punkt (sentence and word tokenizers)
●	Install via: python -m nltk.downloader punkt
Project structure (recommended)
●	BlackCoffer Assignment/
●	venv/
●	src/
●	analyze.py
●	extract.py
●	metrics.py
●	Original/
●	Input.xlsx
●	Output Data Structure.xlsx
●	MasterDictionary/
●	positive-words.txt
●	negative-words.txt
●	StopWords/
●	StopWords_Auditor.txt, StopWords_Generic.txt, etc.
●	Text/ # generated article text files
●	Output.xlsx # generated final report

