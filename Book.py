#!/usr/bin/env python
# coding: utf-8

# # Book Recommendation System

# # Table of Contents
# 
# 1. [Obtain](#1-Obtain-:-Web-Scraping-from-Google-Books)
# 2. [Scrub](#2-Scrub-:-Data-Cleaning)
# 3. [Explore](#3-Explore-:-Exploratory-Data-Analysis)

# # 1 Obtain : Web Scraping from Google Books

# In[1]:


import requests
import pandas as pd

# Book Genre Keywords
genre_list = ['invest', 'memoirs', 'art', 'entertainment', 'business', 'biography', 'children', 'comics', 'computers',               'technology', 'cooking', 'food', 'wine', 'education', 'fiction', 'literature', 'language', 'health',               'psychology', 'history', 'parenting', 'families', 'romance', 'science', 'travel', 'self-help', 'sports',               'young adult', 'science fiction', 'action', 'adventure', 'fantasy', 'mystery', 'horror', 'thriller',               'contemporary', 'literary', 'short story', 'crime', 'humor', 'guide', 'religion', 'mathematics', 'biology',               'physics', 'aerology', 'magic', 'dystopian', 'classic', 'tragedy', 'fairy tale', 'satire', 'biography',               'narrative', 'encyclopedia', 'politics', 'poetry', 'social science', 'detective', 'creative', 'spiritual',              'prose', 'autobiography', 'graphic', 'paranormal romance', 'home and garden', 'economics', 'finance',               'diary', 'leisure', 'suspense', 'drama', 'culture', 'short story', 'music', 'review', 'philosophy',               'fitness', 'dictionary', 'LGBTQ+', 'utopian', 'western', 'photography', 'DIY', 'how-to', 'motivational',               'craft', 'relationship', 'law', 'criminology', 'opera', 'film', 'wedding', 'dance', 'comedy', 'programming',              'automotive', 'manga', 'revolution', 'chick lit', 'architecture', 'alternate history', 'anthology',               'hobbies', 'culinary', 'realism', 'dark fantasy', 'mythology', 'body horror', 'gothic', 'paranormal',               'saga', 'epic', 'urban', 'heroic', 'noir', 'supernatural', 'police', 'medical', 'time travel',               'apocalypse', 'colonization', 'colony', 'biblical', 'military', 'steampunk', 'space', 'exploration',               'nature', 'plants', 'animals', 'alternate dimension', 'parallel world', 'conspiracy', 'forensic',               'espionage', 'eastern', 'women', 'POC', 'true crime', 'ghost', 'legend', 'pirate', 'parody', 'pop culture',               'self-insert', 'spy', 'superhero', 'survival', 'city', 'occult', 'zombie', 'feminist', 'mecha', 'academic',               'data-driven', 'environmental', 'fashion', 'trade', 'world', 'video games', 'global', 'gossip', 'monster',               'alien']

# Book Dict to store books based on genre
book_dict = {}

# Use loop to find books from each genre in genre list and put in dataframe
for genre in genre_list:
    # loop through index with increment by 40 (max fetch is 40 each time) until 2000
    for idx in range(0, 1000, 40):
        api_url = 'https://www.googleapis.com/books/v1/volumes?q='+genre+'+book&printType=books&langRestrict=en&startIndex='+str(idx)+'&maxResults=40'
        response = requests.get(api_url)
        # retrieve data only if the response is success
        if response.status_code == 200:
            data = response.json()
            # check if the book information is in the json file (may not have the info sometimes)
            # only put data into list if there is info
            if 'items' in data:
                # assign item list if the genre key is not in the book_dict, otherwise extend it
                if genre not in book_dict:
                    # book_dict[genre] = pd.DataFrame.from_dict(pd.json_normalize(data['items']), orient='columns')
                    book_dict[genre] = data['items']
                else:
                    # book_dict[genre] = book_dict[genre].append(pd.json_normalize(data['items']), ignore_index=True)
                    book_dict[genre].extend(data['items'])
        else:
            print("Request Error for", genre, ":", response.status_code)


# In[2]:


# check the books count for each genre
for book, ls in book_dict.items():
    print("Books count for", book,": ",len(ls))


# In[3]:


# cross-check if the list is correct and as expected
for book, ls in book_dict.items():
    if book == 'art':
        print(*ls, sep = "\n")


# In[4]:


# Put all books into a master list, then convert into dataframe
# create an empty list
book_list = []

# put all books in book_list
for ls in book_dict.values():
    book_list.extend(ls)

# convert book master list into dataframe
book_df = pd.DataFrame.from_dict(pd.json_normalize(book_list), orient='columns')
display(book_df)

# put in csv file
book_df.to_csv('books.csv')


# # 2 Scrub : Data Cleaning

# ## Data Understanding

# In[64]:


# read data from the saved CSV file
book_df = pd.read_csv('books.csv')


# In[65]:


# Check the rows and columns of the dataframe
print("Number of rows and columns: ", book_df.shape)


# In[66]:


# Display dataframe
display(book_df)


# In[67]:


# drop the Unnamed column
book_df.drop("Unnamed: 0", axis=1, inplace=True)


# In[68]:


# columns and its data types in dataframe
book_df.dtypes


# In[69]:


print(book_df.applymap(type))


# ## Data Cleaning

# ### Data Reduction

# In[70]:


# Attribute list to drop
to_drop = ['kind', 'volumeInfo.printType', 'volumeInfo.allowAnonLogging', 'volumeInfo.allowAnonLogging'            , 'volumeInfo.contentVersion', 'volumeInfo.panelizationSummary.containsEpubBubbles'            , 'volumeInfo.panelizationSummary.containsImageBubbles', 'volumeInfo.imageLinks.smallThumbnail'            , 'volumeInfo.imageLinks.thumbnail', 'volumeInfo.previewLink', 'volumeInfo.infoLink'            , 'volumeInfo.canonicalVolumeLink', 'saleInfo.buyLink', 'saleInfo.offers', 'accessInfo.country'            , 'accessInfo.epub.acsTokenLink', 'accessInfo.pdf.acsTokenLink', 'accessInfo.webReaderLink'            , 'accessInfo.quoteSharingAllowed', 'accessInfo.epub.downloadLink', 'accessInfo.pdf.downloadLink'            , 'volumeInfo.panelizationSummary.imageBubbleVersion', 'volumeInfo.comicsContent', 'volumeInfo.seriesInfo.kind'            , 'volumeInfo.seriesInfo.bookDisplayNumber', 'volumeInfo.seriesInfo.volumeSeries'            , 'volumeInfo.panelizationSummary.epubBubbleVersion', 'volumeInfo.seriesInfo.shortSeriesBookTitle']

# Drop unused columns
book_df.drop(to_drop, axis=1, inplace=True)
display(book_df.head())


# In[71]:


# check whether the id attribute is unique
print("Unique id count:", len(pd.unique(book_df['id'])))
print("Total row count:", len(book_df.index))


# In[72]:


# check those column with duplicates id
book_df[book_df.duplicated(['id'], keep=False)].sort_values("id")


# In[73]:


# Drop duplicate id and keep the first record
book_df.drop_duplicates(subset='id', keep="first", inplace = True)


# In[74]:


# cross-check whether the id attribute is unique
print("Unique id count:", len(pd.unique(book_df['id'])))
print("Total row count:", len(book_df.index))


# In[75]:


# Setting Id as index column
book_df.set_index("id", inplace = True)
display(book_df.head())


# In[76]:


# check how many NAs in each column
na_count = book_df.isna().sum()
print(na_count.sort_values())


# In[77]:


# drop records with empty title
book_df = book_df[book_df['volumeInfo.title'].notna()]
print("Book Title NA count:", book_df['volumeInfo.title'].isna().sum())
print("Total row count:", len(book_df.index))


# In[78]:


# filter language - only english selected
book_df = book_df[book_df['volumeInfo.language'] == "en"]
print("Total row count:", len(book_df.index))


# ### Data Imputation

# #### volumeInfo.title

# In[79]:


import html
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# decode the string
book_df['volumeInfo.title'] = book_df['volumeInfo.title'].apply(lambda x: html.unescape(x))

# replace " characters with empty string
book_df['volumeInfo.title'] = book_df['volumeInfo.title'].astype(str).str.replace('"', '')

display(book_df[['volumeInfo.title']])


# #### volumeInfo.subtitle

# In[80]:


import numpy as np

# contains string, integer and date in volumeInfo.subtitle column
sub_df = book_df[['volumeInfo.subtitle']].copy()

# convert integer and date to na and fill na
sub_df['subtitle_date'] = pd.to_datetime(sub_df['volumeInfo.subtitle'], errors='coerce')
sub_df['subtitle'] = np.where((~sub_df['subtitle_date'].isna()) | (sub_df['volumeInfo.subtitle'].isna()), "Missing", sub_df['volumeInfo.subtitle'])

# remove special characters except space from string
sub_df['subtitle'] = sub_df['subtitle'].str.replace('[^\w\s]', '')

# remove if only integer left
sub_df['subtitle_final'] = np.where(sub_df['subtitle'].str.isdigit(), "Missing", sub_df['subtitle'])

print("Subtitle NA count:", sub_df['subtitle_final'].isna().sum())

display(sub_df[['subtitle_final']])


# In[81]:


# replace the subtitle column in book_df by using the cleaned one
book_df['volumeInfo.subtitle'] = sub_df['subtitle_final']

print("Subtitle NA count:", book_df['volumeInfo.subtitle'].isna().sum())

display(book_df[['volumeInfo.subtitle']])


# #### volumeInfo.authors

# In[82]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Convert author list to string
book_df['volumeInfo.authors'].fillna("Missing", inplace = True)
book_df['volumeInfo.authors'] = book_df['volumeInfo.authors'].astype(str).str.replace('\[|\]|\'', '')

print("Authors NA count:", book_df['volumeInfo.authors'].isna().sum())

display(book_df[['volumeInfo.authors']])


# #### volumeInfo.publisher

# In[83]:


# decode string and remove some symbols in publisher
book_df['volumeInfo.publisher'].fillna("Missing", inplace = True)
book_df['volumeInfo.publisher'] = book_df['volumeInfo.publisher'].apply(lambda x: html.unescape(x))
book_df['volumeInfo.publisher'] = book_df['volumeInfo.publisher'].astype(str).str.replace('\[|\]|\:*"', '')

print("Publisher NA count:", book_df['volumeInfo.publisher'].isna().sum())

display(book_df[['volumeInfo.publisher']])


# #### volumeInfo.publishedDate

# In[84]:


date_df = book_df[['volumeInfo.publishedDate']].copy()

# remove special characters except space from string
date_df['volumeInfo.publishedDate'] = date_df['volumeInfo.publishedDate'].str.replace('[^\d$]', '')

# Get the published year
date_df['volumeInfo.publishedDate'] = date_df['volumeInfo.publishedDate'].str[:4]

# convert string to numeric
date_df['volumeInfo.publishedYear'] = pd.to_numeric(date_df['volumeInfo.publishedDate'], errors='coerce')

# convert to NaN if year < 1000
date_df['volumeInfo.publishedYear'] = np.where(date_df['volumeInfo.publishedYear'] < 1000, np.nan, date_df['volumeInfo.publishedYear'])

# fill na published year with median
date_df['volumeInfo.publishedYear'].fillna(date_df['volumeInfo.publishedYear'].median(), inplace = True)

# convert numeric to integer
date_df['volumeInfo.publishedYear'] = date_df['volumeInfo.publishedYear'].astype(int)

print("Published Year NA count:", date_df['volumeInfo.publishedYear'].isna().sum())

display(date_df)


# In[85]:


# drop published date column in book_df
book_df.drop(['volumeInfo.publishedDate'], axis=1, inplace = True)

# replace the published column in book_df by using the cleaned one
book_df['volumeInfo.publishedYear'] = date_df['volumeInfo.publishedYear']

print("Subtitle NA count:", book_df['volumeInfo.publishedYear'].isna().sum())

display(book_df[['volumeInfo.publishedYear']])


# #### volumeInfo.description

# #### volumeInfo.industryIdentifiers

# In[86]:


import ast
isbn_df = book_df[['volumeInfo.industryIdentifiers']].copy()
isbn_df = isbn_df.dropna()

# convert back from string to dictionary
isbn_df['volumeInfo.industryIdentifiers'] = isbn_df['volumeInfo.industryIdentifiers'].apply(ast.literal_eval)

# split ISBN in Industry Identifier
isbn_df = isbn_df.explode('volumeInfo.industryIdentifiers', ignore_index=False)
isbn_df = pd.json_normalize(isbn_df['volumeInfo.industryIdentifiers']).set_index(isbn_df.index)
display(isbn_df)


# In[87]:


# pivot isbn dataframe
isbn_df = isbn_df.drop_duplicates().reset_index()
isbn_df = isbn_df.pivot(index='id', columns='type', values = 'identifier')
isbn_df.fillna("Missing", inplace = True)
display(isbn_df)


# In[88]:


# cross-check the id count in book_df and isbn_df
print("Book unique id count:", len(book_df.index))
print("Book with isbn unique id count:", len(isbn_df.index))


# In[89]:


# Rename columns in df_cleaned_isbn
isbn_df.rename(columns = {'ISBN_10':'volumeInfo.industryIdentifiers.ISBN_10',                         'ISBN_13':'volumeInfo.industryIdentifiers.ISBN_13',                         'ISSN':'volumeInfo.industryIdentifiers.ISSN',                         'OTHER':'volumeInfo.industryIdentifiers.OTHER'}
                    , inplace = True)


# In[90]:


# Join isbn_df to book_df
book_df = book_df.join(isbn_df)

# fill na with missing
book_df['volumeInfo.industryIdentifiers.ISBN_10'] = book_df['volumeInfo.industryIdentifiers.ISBN_10'].fillna("Missing")
book_df['volumeInfo.industryIdentifiers.ISBN_13'] = book_df['volumeInfo.industryIdentifiers.ISBN_13'].fillna("Missing")
book_df['volumeInfo.industryIdentifiers.ISSN'] = book_df['volumeInfo.industryIdentifiers.ISSN'].fillna("Missing")
book_df['volumeInfo.industryIdentifiers.OTHER'] = book_df['volumeInfo.industryIdentifiers.OTHER'].fillna("Missing")

print("ISBN 10 NA count:", book_df['volumeInfo.industryIdentifiers.ISBN_10'].isna().sum())
print("ISBN 13 NA count:", book_df['volumeInfo.industryIdentifiers.ISBN_13'].isna().sum())
print("ISSN NA count:", book_df['volumeInfo.industryIdentifiers.ISSN'].isna().sum())
print("OTHER Identifier NA count:", book_df['volumeInfo.industryIdentifiers.OTHER'].isna().sum())

display(book_df[['volumeInfo.industryIdentifiers', 'volumeInfo.industryIdentifiers.ISBN_10',                  'volumeInfo.industryIdentifiers.ISBN_13', 'volumeInfo.industryIdentifiers.ISSN',                  'volumeInfo.industryIdentifiers.OTHER']])


# In[91]:


# Drop unused columns in book_df
book_df.drop(['volumeInfo.industryIdentifiers'], axis=1, inplace=True)


# #### volumeInfo.pageCount

# In[92]:


import numpy as np

# replace page count 0 to NaN
book_df['volumeInfo.pageCount'].replace(0, np.nan, inplace = True)

# fill na page count with mean
book_df['volumeInfo.pageCount'].fillna(book_df['volumeInfo.pageCount'].mean(), inplace = True)

# convert numeric to integer
book_df['volumeInfo.pageCount'] = book_df['volumeInfo.pageCount'].astype(int)

print("Page Count NA count:", book_df['volumeInfo.pageCount'].isna().sum())

display(book_df[['volumeInfo.pageCount']])


# #### volumeInfo.categories

# In[97]:


genre_df = book_df[['volumeInfo.categories']].copy()

# Fill na using forward fill
genre_df['volumeInfo.categories'].ffill(axis = 0, inplace = True)

# Convert genre list to string
genre_df['volumeInfo.categories'] = genre_df['volumeInfo.categories'].apply(eval).apply(','.join)

print("Genre NA count:", genre_df['volumeInfo.categories'].isna().sum())
display(genre_df[['volumeInfo.categories']])


# In[101]:


# replace the categories column in book_df by using the cleaned one
book_df['volumeInfo.categories'] = genre_df['volumeInfo.categories']

print("Categories NA count:", book_df['volumeInfo.categories'].isna().sum())

display(book_df[['volumeInfo.categories']])


# #### saleInfo.listPrice.amount & saleInfo.retailPrice.amount

# In[100]:


price_df = book_df[['saleInfo.retailPrice.amount', 'saleInfo.retailPrice.currencyCode',                    'saleInfo.listPrice.amount', 'saleInfo.listPrice.currencyCode']].copy()

# replace 0 with median price
price_df['saleInfo.retailPrice.amount'] = price_df['saleInfo.retailPrice.amount'].replace(0, price_df['saleInfo.retailPrice.amount'].median())
price_df['saleInfo.listPrice.amount'] = price_df['saleInfo.listPrice.amount'].replace(0, price_df['saleInfo.listPrice.amount'].median())

# fill na with 0
price_df['saleInfo.retailPrice.amount'].fillna(0, inplace = True)
price_df['saleInfo.listPrice.amount'].fillna(0, inplace = True)

# fill in empty currency code with MYR
price_df['saleInfo.retailPrice.currencyCode'].fillna("MYR", inplace = True)
price_df['saleInfo.listPrice.currencyCode'].fillna("MYR", inplace = True)

print("Retail Price NA count:", price_df['saleInfo.retailPrice.amount'].isna().sum())
print("List Price NA count:", price_df['saleInfo.listPrice.amount'].isna().sum())
print("Retail Price Currency Code NA count:", price_df['saleInfo.retailPrice.currencyCode'].isna().sum())
print("List Price Currency Code NA count:", price_df['saleInfo.listPrice.currencyCode'].isna().sum())

display(price_df[['saleInfo.retailPrice.currencyCode', 'saleInfo.retailPrice.amount', 'saleInfo.listPrice.currencyCode', 'saleInfo.listPrice.amount']])


# In[102]:


# replace the price columns in book_df by using the cleaned one
book_df['saleInfo.retailPrice.currencyCode'] = price_df['saleInfo.retailPrice.currencyCode']
book_df['saleInfo.retailPrice.amount'] = price_df['saleInfo.retailPrice.amount']
book_df['saleInfo.listPrice.currencyCode'] = price_df['saleInfo.listPrice.currencyCode']
book_df['saleInfo.listPrice.amount'] = price_df['saleInfo.listPrice.amount']

print("Retail Price Currency Code NA count:", book_df['saleInfo.retailPrice.currencyCode'].isna().sum())
print("Retail Price NA count:", book_df['saleInfo.retailPrice.amount'].isna().sum())
print("List Price Currency Code NA count:", book_df['saleInfo.listPrice.currencyCode'].isna().sum())
print("List Price NA count:", book_df['saleInfo.listPrice.amount'].isna().sum())

display(book_df[['saleInfo.retailPrice.currencyCode', 'saleInfo.retailPrice.amount',                  'saleInfo.listPrice.currencyCode', 'saleInfo.listPrice.amount']])


# #### searchInfo.textSnippet

# #### volumeInfo.averageRating & volumeInfo.ratingsCount

# In[103]:


# Fill in null average ratings and ratings count with 0
book_df['volumeInfo.averageRating'] = book_df['volumeInfo.averageRating'].fillna(0)
book_df['volumeInfo.ratingsCount'] = book_df['volumeInfo.ratingsCount'].fillna(0)

# convert rating count from double to int
book_df['volumeInfo.ratingsCount'] = book_df['volumeInfo.ratingsCount'].astype(int)

print("Average Rating NA count:", book_df['volumeInfo.averageRating'].isna().sum())
print("Rating Count NA count:", book_df['volumeInfo.ratingsCount'].isna().sum())

display(book_df[['volumeInfo.averageRating', 'volumeInfo.ratingsCount']])


# ### Final Cleaned Dataset

# In[104]:


# check how many NAs in each column in book_df_cleaned 
total_na_count = book_df.isna().sum()
print(total_na_count.sort_values())


# In[105]:


# fill na for columns (searchInfo.textSnippet, volumeInfo.description)
book_df.fillna("Missing", inplace = True)


# In[106]:


# check again how many NAs in each column in book_df_cleaned 
total_na_count = book_df.isna().sum()
print(total_na_count.sort_values())


# In[107]:


# put cleaned dataset in csv file
book_df.to_csv('books_clean.csv')


# ## 3 Explore : Exploratory Data Analysis

# In[ ]:




