import json

def markdown_cell(source):
    if isinstance(source, str):
        source = [line + '\n' if not line.endswith('\n') else line for line in source.split('\n')]
    return {
        'cell_type': 'markdown',
        'metadata': {},
        'source': source
    }

def code_cell(source):
    if isinstance(source, str):
        source = [line + '\n' if not line.endswith('\n') else line for line in source.split('\n')]
    return {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': source
    }

cells = []

# Title & Install
cells.append(markdown_cell('# Exploratory Data Analysis (EDA) on FNC-1 Dataset'))
cells.append(code_cell('!pip install pandas matplotlib seaborn transformers wordcloud nltk'))

# Imports
cells.append(code_cell('''\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from wordcloud import WordCloud
from transformers import RobertaTokenizer, XLNetTokenizer
from collections import Counter
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid')\
'''))

# Dataset Overview
cells.append(markdown_cell('## Dataset Overview'))
cells.append(code_cell('''\
# Load the dataset
df = pd.read_csv('./data/train/train.csv')

print("Shape of dataset:", df.shape)
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])
print("\\nData Types:\\n", df.dtypes)
print("\\nFeature Names:", list(df.columns))

# Display sample data
display(df.head())\
'''))

cells.append(code_cell('''\
# Visualisasi: Missing value heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
plt.title('Missing Value Heatmap')
plt.show()\
'''))
cells.append(markdown_cell('**Insight Singkat:**\n(Isi dengan hasil pengamatan Anda dari overview data, seperti fitur dominan yang berupa string dan seberapa banyak data yang kita miliki).'))

# Analisis Data Null
cells.append(markdown_cell('## Analisis Data Null'))
cells.append(code_cell('''\
# Missing value per kolom dan persentase
null_counts = df.isnull().sum()
null_percentages = 100 * null_counts / len(df)
null_df = pd.DataFrame({'Missing Values': null_counts, 'Percentage (%)': null_percentages})
display(null_df)

# Visualisasi: Barplot jumlah & persentase missing value
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

sns.barplot(x=null_df.index, y=null_df['Missing Values'], ax=axes[0], palette='Reds')
axes[0].set_title('Jumlah Missing Value per Kolom')
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(x=null_df.index, y=null_df['Percentage (%)'], ax=axes[1], palette='Reds')
axes[1].set_title('Persentase Missing Value per Kolom')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()\
'''))
cells.append(markdown_cell('**Insight Singkat:**\n(Tuliskan apakah ada kolom yang kehilangan banyak data atau apakah dataset cukup bersih dari nilai null).'))

# Analisis Data Duplikat
cells.append(markdown_cell('## Analisis Data Duplikat'))
cells.append(code_cell('''\
# Periksa duplikat
dup_row = df.duplicated().sum()
dup_headline = df['Headline'].duplicated().sum() if 'Headline' in df.columns else 0
dup_body = df['articleBody'].duplicated().sum() if 'articleBody' in df.columns else 0

# Duplicate pair (Headline + Body)
if 'Headline' in df.columns and 'articleBody' in df.columns:
    dup_pair = df.duplicated(subset=['Headline', 'articleBody']).sum()
else:
    dup_pair = 0

dup_stats = {
    'Duplicate Rows': dup_row,
    'Duplicate Headlines': dup_headline,
    'Duplicate Article Bodies': dup_body,
    'Duplicate Pairs': dup_pair
}

# Visualisasi Barplot
plt.figure(figsize=(10, 5))
sns.barplot(x=list(dup_stats.keys()), y=list(dup_stats.values()), palette='Oranges')
plt.title('Jumlah Duplikat Berdasarkan Kategori')
plt.ylabel('Jumlah Duplikat')
plt.show()

# Menampilkan contoh data duplikat jika ada
if dup_row > 0:
    print("\\nContoh Exact Duplicate Row:")
    display(df[df.duplicated(keep=False)].head(2))

if dup_headline > 0:
    print("\\nContoh Duplicate Headline (beda body/stance):")
    display(df[df.duplicated(subset=['Headline'], keep=False)].sort_values('Headline').head(2))

if dup_body > 0:
    print("\\nContoh Duplicate Article Body (beda headline/stance):")
    display(df[df.duplicated(subset=['articleBody'], keep=False)].sort_values('articleBody').head(2))\
'''))
cells.append(markdown_cell('**Insight Singkat:**\n(Analisis apakah duplikasi yang terjadi adalah wajar, misalnya karena satu berita dikaitkan dengan banyak headline yang berbeda).'))

# Analisis Distribusi Label
cells.append(markdown_cell('## Analisis Distribusi Label'))
cells.append(code_cell('''\
if 'Stance' in df.columns:
    stance_counts = df['Stance'].value_counts()
    stance_percentages = 100 * stance_counts / len(df)
    
    dist_df = pd.DataFrame({'Count': stance_counts, 'Percentage (%)': stance_percentages})
    display(dist_df)
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    
    # 1. Countplot
    sns.countplot(data=df, x='Stance', order=stance_counts.index, ax=axes[0], palette='viridis')
    axes[0].set_title('Countplot Label Stance')
    
    # 2. Pie chart
    axes[1].pie(stance_counts, labels=stance_counts.index, autopct='%1.1f%%', colors=sns.color_palette('viridis', len(stance_counts)))
    axes[1].set_title('Pie Chart Distribusi Stance')
    
    # 3. Bar chart persentase
    sns.barplot(x=dist_df.index, y=dist_df['Percentage (%)'], ax=axes[2], palette='viridis')
    axes[2].set_title('Bar Chart Persentase Stance')
    
    plt.tight_layout()
    plt.show()
    
    # Hitung imbalance ratio (Majority class / Minority class)
    imbalance_ratio = stance_counts.max() / stance_counts.min()
    print(f"Imbalance Ratio (Max/Min): {imbalance_ratio:.2f}")\
'''))
cells.append(markdown_cell('**Insight Singkat mengenai tingkat class imbalance:**\n(Catat apakah data sangat didominasi oleh kelas unrelated dan seberapa parah ketidakseimbangannya).'))


# Analisis Headline
cells.append(markdown_cell('## Analisis Headline'))
cells.append(code_cell('''\
if 'Headline' in df.columns:
    # Mengisi NaN dengan string kosong jika ada
    df['Headline'] = df['Headline'].fillna('')
    
    df['Headline_Char_Len'] = df['Headline'].apply(len)
    df['Headline_Word_Count'] = df['Headline'].apply(lambda x: len(x.split()))
    
    print("Statistik Panjang Headline:")
    display(df[['Headline_Char_Len', 'Headline_Word_Count']].describe().T[['mean', '50%', 'min', 'max', 'std']].rename(columns={'50%':'median'}))
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.histplot(df['Headline_Char_Len'], bins=50, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('Histogram Panjang Karakter Headline')
    
    sns.histplot(df['Headline_Word_Count'], bins=50, kde=True, ax=axes[1], color='green')
    axes[1].set_title('Histogram Jumlah Kata Headline')
    
    sns.boxplot(x=df['Headline_Char_Len'], ax=axes[2], color='orange')
    axes[2].set_title('Boxplot Panjang Karakter Headline')
    
    plt.tight_layout()
    plt.show()\
'''))
cells.append(markdown_cell('**Insight Singkat:**\n(Analisis variasi panjang headline dan apakah ada headline yang tidak masuk akal panjang atau pendeknya).'))


# Analisis Article Body
cells.append(markdown_cell('## Analisis Article Body'))
cells.append(code_cell('''\
if 'articleBody' in df.columns:
    df['articleBody'] = df['articleBody'].fillna('')
    
    df['Body_Char_Len'] = df['articleBody'].apply(len)
    df['Body_Word_Count'] = df['articleBody'].apply(lambda x: len(x.split()))
    
    print("Statistik Panjang Article Body:")
    display(df[['Body_Char_Len', 'Body_Word_Count']].describe().T[['mean', '50%', 'min', 'max', 'std']].rename(columns={'50%':'median'}))
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Histogram
    sns.histplot(df['Body_Word_Count'], bins=50, ax=axes[0,0], color='purple')
    axes[0,0].set_title('Histogram Jumlah Kata Article Body')
    
    # 2. KDE
    sns.kdeplot(df['Body_Word_Count'], fill=True, ax=axes[0,1], color='magenta')
    axes[0,1].set_title('KDE Distribution Jumlah Kata')
    
    # 3. Boxplot
    sns.boxplot(x=df['Body_Word_Count'], ax=axes[1,0], color='cyan')
    axes[1,0].set_title('Boxplot Jumlah Kata')
    
    # 4. Violin
    sns.violinplot(x=df['Body_Word_Count'], ax=axes[1,1], color='teal')
    axes[1,1].set_title('Violin Plot Jumlah Kata')
    
    plt.tight_layout()
    plt.show()
    
    # Highlight outlier article
    print("Contoh Outlier (Top 3 artikel terpanjang berdasarkan kata):")
    display(df.sort_values('Body_Word_Count', ascending=False)[['articleBody', 'Body_Word_Count']].head(3))\
'''))
cells.append(markdown_cell('**Insight Singkat:**\n(Sebutkan temuan dari bentuk sebaran artikel body, seperti ekor distribusi yang panjang menandakan adanya outlier sangat panjang).'))


# Token Distribution Analysis
cells.append(markdown_cell('## Token Distribution Analysis'))
cells.append(code_cell('''\
# Meng-load tokenizers
roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
xlnet_tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')

def count_tokens(text, tokenizer):
    # Menggunakan metode yang cepat untuk menghitung token length (tanpa padding/truncation)
    return len(tokenizer.tokenize(text))

sample_df = df

if 'Headline' in sample_df.columns and 'articleBody' in sample_df.columns:
    sample_df['Combined_Text'] = sample_df['Headline'] + " " + sample_df['articleBody']
    
    # RoBERTa
    sample_df['RoBERTa_Headline'] = sample_df['Headline'].apply(lambda x: count_tokens(str(x), roberta_tokenizer))
    sample_df['RoBERTa_Body'] = sample_df['articleBody'].apply(lambda x: count_tokens(str(x), roberta_tokenizer))
    sample_df['RoBERTa_Combined'] = sample_df['Combined_Text'].apply(lambda x: count_tokens(str(x), roberta_tokenizer))
    
    # XLNet
    sample_df['XLNet_Combined'] = sample_df['Combined_Text'].apply(lambda x: count_tokens(str(x), xlnet_tokenizer))
    
    # Buat fungsi ringkasan
    def token_summary(series):
        return {
            'Mean': series.mean(),
            'Median': series.median(),
            'P90': np.percentile(series, 90),
            'P95': np.percentile(series, 95),
            'P99': np.percentile(series, 99),
            'Max': series.max(),
            '> 512': (series > 512).mean() * 100,
            '> 1024': (series > 1024).mean() * 100,
            '> 2048': (series > 2048).mean() * 100,
            '> 4096': (series > 4096).mean() * 100
        }
    
    summary_df = pd.DataFrame({
        'RoBERTa Headline': token_summary(sample_df['RoBERTa_Headline']),
        'RoBERTa Body': token_summary(sample_df['RoBERTa_Body']),
        'RoBERTa Combined': token_summary(sample_df['RoBERTa_Combined']),
        'XLNet Combined': token_summary(sample_df['XLNet_Combined'])
    }).T
    
    display(summary_df)
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.histplot(sample_df['RoBERTa_Combined'], bins=50, ax=axes[0], color='blue', alpha=0.6, label='RoBERTa')
    sns.histplot(sample_df['XLNet_Combined'], bins=50, ax=axes[0], color='red', alpha=0.4, label='XLNet')
    axes[0].set_title('Histogram Token Length (Combined Text)')
    axes[0].legend()
    
    sns.kdeplot(sample_df['RoBERTa_Combined'], fill=True, ax=axes[1], color='blue', label='RoBERTa')
    sns.kdeplot(sample_df['XLNet_Combined'], fill=True, ax=axes[1], color='red', label='XLNet')
    axes[1].set_title('KDE Token Length')
    axes[1].legend()
    
    sns.boxplot(data=sample_df[['RoBERTa_Combined', 'XLNet_Combined']], ax=axes[2])
    axes[2].set_title('Boxplot Token Length')
    
    plt.tight_layout()
    plt.show()
'''))


# Token Distribution per Label
cells.append(markdown_cell('## Token Distribution per Label'))
cells.append(code_cell('''\
if 'Stance' in sample_df.columns:
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    sns.boxplot(x='Stance', y='RoBERTa_Combined', data=sample_df, ax=axes[0], palette='Set2')
    axes[0].set_title('Boxplot Token Length per Stance')
    
    sns.violinplot(x='Stance', y='RoBERTa_Combined', data=sample_df, ax=axes[1], palette='Set2')
    axes[1].set_title('Violin Plot Token Length per Stance')
    
    sns.histplot(data=sample_df, x='RoBERTa_Combined', hue='Stance', element='step', common_norm=False, ax=axes[2], palette='Set2', bins=50)
    axes[2].set_title('Histogram Token Length per Stance')
    
    plt.tight_layout()
    plt.show()\
'''))


# Word Frequency Analysis
cells.append(markdown_cell('## Word Frequency Analysis'))
cells.append(code_cell('''\
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Lowercase & remove punctuation
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove stopwords
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return words

if 'Headline' in df.columns and 'articleBody' in df.columns:
    print("Memproses teks untuk word frequency...")
    freq_df = df
    
    all_headlines_words = []
    freq_df['Headline'].apply(lambda x: all_headlines_words.extend(preprocess_text(x)))
    
    all_body_words = []
    freq_df['articleBody'].apply(lambda x: all_body_words.extend(preprocess_text(x)))
    
    head_counter = Counter(all_headlines_words).most_common(30)
    body_counter = Counter(all_body_words).most_common(30)
    
    head_df = pd.DataFrame(head_counter, columns=['Word', 'Count'])
    body_df = pd.DataFrame(body_counter, columns=['Word', 'Count'])
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    sns.barplot(data=head_df, y='Word', x='Count', ax=axes[0], palette='Blues_r')
    axes[0].set_title('Top 30 Kata di Headline')
    
    sns.barplot(data=body_df, y='Word', x='Count', ax=axes[1], palette='Greens_r')
    axes[1].set_title('Top 30 Kata di Article Body')
    
    plt.tight_layout()
    plt.show()\
'''))


# Wordcloud Analysis
cells.append(markdown_cell('## WordCloud Analysis'))
cells.append(code_cell('''\
def generate_wordcloud(words_list, title):
    text = ' '.join(words_list)
    if not text.strip(): return
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.show()

if 'Headline' in df.columns and 'articleBody' in df.columns:
    print("Wordcloud untuk Seluruh Teks:")
    generate_wordcloud(all_headlines_words, 'WordCloud - Seluruh Headline')
    generate_wordcloud(all_body_words, 'WordCloud - Seluruh Article Body')
    
    # Wordcloud per label
    if 'Stance' in df.columns:
        stances = df['Stance'].unique()
        for s in stances:
            subset = df[df['Stance'] == s]
            words = []
            subset['Headline'].apply(lambda x: words.extend(preprocess_text(x)))
            generate_wordcloud(words, f'WordCloud Headline - Label: {s}')\
'''))


# Text Quality Analysis
cells.append(markdown_cell('## Text Quality Analysis'))
cells.append(code_cell('''\
quality_stats = {'URL': 0, 'HTML': 0, 'Email': 0, 'UnicodeAneh': 0, 'MultipleWhitespace': 0}

url_pattern = re.compile(r'https?://\S+|www\.\S+')
html_pattern = re.compile(r'<.*?>')
email_pattern = re.compile(r'\S+@\S+')
unicode_pattern = re.compile(r'[^\x00-\x7F]+')
whitespace_pattern = re.compile(r'\s{2,}')

def check_quality(text):
    text = str(text)
    has_url = bool(url_pattern.search(text))
    has_html = bool(html_pattern.search(text))
    has_email = bool(email_pattern.search(text))
    has_unicode = bool(unicode_pattern.search(text))
    has_multiple_ws = bool(whitespace_pattern.search(text))
    
    return pd.Series([has_url, has_html, has_email, has_unicode, has_multiple_ws])

if 'articleBody' in df.columns:
    qual_df = df['articleBody'].apply(check_quality)
    qual_df.columns = ['URL', 'HTML', 'Email', 'UnicodeAneh', 'MultipleWhitespace']
    
    qual_sums = qual_df.sum()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=qual_sums.index, y=qual_sums.values, palette='Reds_r')
    plt.title('Kemunculan Isu Kualitas Teks di Article Body')
    plt.ylabel('Jumlah Baris')
    plt.show()
    
    print("Contoh Artikel mengandung URL:")
    if qual_sums['URL'] > 0:
        display(df[qual_df['URL']]['articleBody'].head(1).values[0][:500])
'''))
cells.append(markdown_cell('**Insight Singkat:**\n(Review apakah teks membutuhkan pembersihan ekstra dari HTML, URL, atau karakter non-ASCII).'))

# Model Selection Insight
cells.append(markdown_cell('## Model Selection Insight'))
cells.append(markdown_cell('''\
Berdasarkan hasil "Token Distribution Analysis" di atas, kita dapat merangkum metrik berikut:

| Metric | Value |
|----------|----------|
| Avg Token | *[Lihat tabel ringkasan Token Analysis]* |
| Median Token | *[Lihat tabel ringkasan]* |
| P95 Token | *[Lihat tabel ringkasan]* |
| P99 Token | *[Lihat tabel ringkasan]* |
| Max Token | *[Lihat tabel ringkasan]* |
| % > 512 | *[Lihat tabel ringkasan]* |
| % > 1024 | *[Lihat tabel ringkasan]* |
| % > 2048 | *[Lihat tabel ringkasan]* |

### Rekomendasi:
1. **Apakah RoBERTa layak digunakan?**
   - RoBERTa memiliki batas maksimum 512 token. Jika *persentase data > 512 token* tergolong besar (misalnya di atas 10-15%), memotong (truncate) teks bisa menghilangkan informasi penting dari akhir artikel. Jika persentase di atas 512 sangat kecil, RoBERTa sangat direkomendasikan.

2. **Apakah XLNet layak digunakan?**
   - XLNet pada teorinya tidak dibatasi panjang urutan teks layaknya model BERT-based tradisional. Namun, komputasinya akan meledak secara kuadratik dan bisa membutuhkan memori (VRAM) yang luar biasa besar untuk artikel dengan ribuan kata. XLNet layak jika rentang token rata-rata masih dalam batas toleransi VRAM (misal <= 1024).

3. **Apakah Longformer diperlukan?**
   - Longformer (atau BigBird) sangat direkomendasikan jika `P95 Token` atau `% > 512` dan `% > 1024` bernilai sangat signifikan, karena arsitekturnya didesain khusus memproses teks panjang hingga 4096 token dengan *sparse attention*.

4. **Tantangan Terbesar: Token Length vs Class Imbalance**
   - Kombinasi panjang token ekstrim dan *class imbalance* (dengan dominasi `unrelated`) akan mengakibatkan model cepat _overfit_ menebak mayoritas kelas. Oleh karena itu, strategi *undersampling*/*oversampling* atau kalkulasi *class weights* di *Loss Function* wajib digunakan apa pun jenis arsitektur model transformer yang dipilih.
'''))

# Construct JSON
notebook = {
    'cells': cells,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {'name': 'ipython', 'version': 3},
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.8.0'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

with open('eda_train.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)
print('eda_train.ipynb created successfully.')
