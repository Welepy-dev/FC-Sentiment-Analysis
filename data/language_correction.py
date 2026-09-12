from langdetect import detect, LangDetectException
import pandas as pd

df = pd.read_parquet("./processed/reviews_clean.parquet")

def detect_language(text):
    try:
        return detect(str(text))
    except LangDetectException:
        return 'unknown'

df['language'] = df['review'].apply(detect_language)

df.to_parquet("./processed/reviews_clean_lang.parquet")

print(df['language'].value_counts())
