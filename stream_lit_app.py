# -*- coding: utf-8 -*-
import streamlit as st



#import library
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import random
import pickle
from sklearn.metrics.pairwise import cosine_similarity

#load data
cleaned_df = pd.read_csv("Books Subset.csv")

#build dashboard
add_sidebar=st.sidebar.selectbox('Navigation', ('Project Information','Book Data Facts','Book Recommendation Engine'))

st.title("What's Next, Shakespeare? :books: :apple:")

#condition
if add_sidebar == 'Project Information':
    st.subheader("Weekly Top Selling Books")
    st.image('book_image.png',use_column_width=True)

    #project background
    st.subheader('Project Background')
    st.markdown("<div style='text-align: justify;'>This project focuses on building a recommender system for books through content-based filtering algorithm and is named What's Next, Shakespeare?. This system serves the purpose of narrowing down the options available to users by predicting and making suggestions on books that they may be interested in. It will also benefit book sellers by boosting their book sales with the increase in public exposure, gaining more profits in return.</div>", unsafe_allow_html=True)
    st.write ('\n') 
       
    st.subheader('Project Objectives')
    st.write('1) Explore the best avenue of data collection which will result in a wide variety of books')
    st.write('2) Determine the key features of relevancy that will yield personalized recommendations to users') 
    st.write('3) Evaluate different algorithms and techniques to build the content-based filtering book recommendation system') 
    st.write('4) Successfully deploy an easily accessible webapp for the created model') 

if add_sidebar == 'Book Data Facts':
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader('Book Data Facts')

    st.subheader("Top 10 Categories of Books")
    st.write('Reviewing the categories gives a general overview of the popular genres. The top genres can be used as a measure of the kinds of books that sell well.')
    categories = cleaned_df['volumeInfo.categories'].value_counts()
    categories_df = categories.reset_index() 
    categories_df.columns = "Categories", "Amount"
    categories_df = categories_df.set_index("Categories")

    # categories_df.head(15)
    plt.figure(figsize=(15,15))
    ax = sns.barplot(x = categories_df.head(15)['Amount'], y = categories_df.head(15).index, palette='plasma')

    ax.set_xlabel("Amount")
    ax.set_title('Top 15 Categories of Books')
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    sns.set_theme(style='white')
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round(i.get_width())),fontsize = 15, color ='black')
    st.pyplot()
    st.write('Fiction is the most common category of books from the collected data, with 12,346 books. Juvenile fiction, which is in second place, only has 4,645 books. That is a huge difference of 7,701 books compared to the highest category. It can also be noted that juvenile fiction is also a type of fiction, albeit for a younger audience. In contrast, there are not much difference in the number of books for the remaining categories.')

    st.subheader("Top 15 Publishers")
    publisher_table = cleaned_df[cleaned_df['volumeInfo.publisher']!='Missing']
    publisher_table = publisher_table.replace(['HarperCollins', 'HarperCollins UK'],'Harper Collins')
    top_15_publisher = publisher_table.groupby('volumeInfo.publisher')['volumeInfo.title'].count().reset_index().sort_values('volumeInfo.title', ascending=False).head(15).set_index('volumeInfo.publisher')
    # top_15_publisher.head(15)
    plt.figure(figsize=(15,10))
    ax = sns.barplot(x = top_15_publisher['volumeInfo.title'], y = top_15_publisher.index, palette='plasma')

    ax.set_title("Top 15 publisher with most books")
    ax.set_xlabel("Total number of books")
    totals = []
    for i in ax.patches:
        totals.append(i.get_width())
    total = sum(totals)
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round(i.get_width())),fontsize = 15, color ='black')
    st.pyplot()
    st.write('Hachette UK published the most, with 1,322 different books based on our data. Subsequently, Harper Collins and Simon and Schuster ranked second and third with 1,142 and 1,128 books published respectively.')

    st.subheader("Top 15 Publishers based on Amount of Ratings")
    st.write('This section showcases the publishers that have a large number of ratings on their books. This could be used as a measure to demonstrate how popular the books by these publishers are as many consumers took the time to leave this feedback.')
    publisher_ratings_df = cleaned_df.copy()
    publisher_ratings_df = publisher_ratings_df[publisher_ratings_df['volumeInfo.publisher']!='Missing']
    publisher_ratings_df = publisher_ratings_df.replace(['HarperCollins', 'HarperCollins UK'],'Harper Collins')
    publisher_ratings_df = publisher_ratings_df[publisher_ratings_df['volumeInfo.ratingsCount']>0]
    publisher_ratings_df = publisher_ratings_df.groupby('volumeInfo.publisher', as_index = False).agg({"volumeInfo.ratingsCount": "sum", 'volumeInfo.averageRating': "mean"})
    publisher_ratings_df.sort_values(by=['volumeInfo.ratingsCount', 'volumeInfo.averageRating'], ascending = [False, False], inplace = True)
    # display(publisher_ratings_df[['volumeInfo.publisher', 'volumeInfo.ratingsCount', 'volumeInfo.averageRating']].head(15))
    plt.figure(figsize=(15,10))
    top_15_publisher_ratingCount = publisher_ratings_df[['volumeInfo.publisher', 'volumeInfo.ratingsCount', 'volumeInfo.averageRating']].head(15)
    ax = sns.barplot(x = top_15_publisher_ratingCount['volumeInfo.ratingsCount'], y = top_15_publisher_ratingCount['volumeInfo.publisher'], palette='plasma')
    ax.set_title("Top 15 publisher with most ratings")
    ax.set_xlabel("Total amount of Ratings")
    totals = []
    for i in ax.patches:
        totals.append(i.get_width())
    total = sum(totals)
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round(i.get_width())),fontsize = 15, color ='black')
    st.pyplot()
    st.write('Observation: Hachette UK is again at the top of the chart. It can be gathered that of the many books Hachette UK has released (1,322 books). Following that are Simon and Schuster and Harper Collins that were also in the top 4 of the previous list. In contrast, Routledge that has the most books published cannot be found in the current top 15 list.')

    st.subheader("Top Publishers based on both Top Ratings and Ratings Count")
    top_15_publisher_averageRating = publisher_ratings_df[['volumeInfo.publisher', 'volumeInfo.ratingsCount', 'volumeInfo.averageRating']].head(15)
    top_15_publisher_averageRating['volumeInfo.averageRating'] = top_15_publisher_averageRating['volumeInfo.averageRating'].round(decimals = 2)
    top_15_publisher_averageRating.sort_values(by='volumeInfo.averageRating', ascending = False, inplace = True)
    # display(top_15_publisher_averageRating)
    plt.figure(figsize=(10, 10))

    data = top_15_publisher_averageRating
    gr = sns.barplot(x="volumeInfo.averageRating", y="volumeInfo.publisher", data=data, palette="plasma")

    for i in gr.patches:
        gr.text(i.get_width() + .05, i.get_y() + 0.5, str(i.get_width()), fontsize = 12, color = 'k')
    st.pyplot()
    # st.write('')

    st.subheader("Top 15 Authors with most books")
    author_table=cleaned_df[cleaned_df['volumeInfo.authors']!='Missing']
    top_fifteen_authors = author_table.groupby('volumeInfo.authors')['volumeInfo.title'].count().reset_index().sort_values('volumeInfo.title', ascending=False).head(15).set_index('volumeInfo.authors')
    # top_fifteen_authors.head(15)
    plt.figure(figsize=(15,10))
    ax = sns.barplot(x = top_fifteen_authors['volumeInfo.title'], y = top_fifteen_authors.index, palette='plasma')

    ax.set_title("Top 15 authors with most books")
    ax.set_xlabel("Total number of books")
    totals = []
    for i in ax.patches:
        totals.append(i.get_width())
    total = sum(totals)
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round(i.get_width())),fontsize = 15, color ='black')
    st.pyplot()
    st.write("Based on our data, DK has the highest books written, which is 130, followed by Blake Pierce, Jupiter Kids and Betty Neels. 'Missing' category is removed prior to creating this chart to present accurate data.")

    st.subheader("Book Published Year")
    sns.histplot(cleaned_df
                ,x = 'volumeInfo.publishedYear'
                ,color = 'navy'
    #             ,alpha = 0
                ,bins = 50
    #             ,binwidth = 1
                ,kde = True
                )
    plt.xlabel('Published Year')
    plt.ylabel('No. of Books')
    plt.title('Histogram of Publication Year')
    st.pyplot()
    st.write('The publication year starts from 1547 up to 2022. From this plot it is observed that most of the publication year starts from the year 2000.')

    
    st.subheader("Book Accessibility")
    st.write("The ePub and PDF access increases consumer’s ability to obtain the books by giving them more avenues to read it.")
    pd.options.mode.chained_assignment = None 
    epub_pdf_df = cleaned_df[['accessInfo.epub.isAvailable','accessInfo.pdf.isAvailable']]
    epub_pdf_df.columns = "accessInfo.epub.isAvailable", "accessInfo.pdf.isAvailable"
    epub_pdf_df['Availability']=0

    def avail(epub_pdf_df):
        if (epub_pdf_df ['accessInfo.epub.isAvailable'] == True) & (epub_pdf_df ['accessInfo.pdf.isAvailable'] == True):
            return 'Both'
        elif (epub_pdf_df ['accessInfo.epub.isAvailable'] == True) & (epub_pdf_df ['accessInfo.pdf.isAvailable'] == False):
            return 'ePub only'
        elif (epub_pdf_df ['accessInfo.epub.isAvailable'] == False) & (epub_pdf_df ['accessInfo.pdf.isAvailable'] == True):
            return 'PDF only'
        elif (epub_pdf_df ['accessInfo.epub.isAvailable'] == False) & (epub_pdf_df ['accessInfo.pdf.isAvailable'] == False):
            return 'None'
        
    epub_pdf_df['Availability'] = epub_pdf_df.apply(avail, axis = 1)
    availability = epub_pdf_df['Availability'].value_counts()
    availability_df = availability.reset_index()
    availability_df.columns = "Type", "Amount"
    fig = plt.figure(figsize=[15,10])

    ax = sns.barplot(x='Type', y='Amount', data=availability_df, errwidth=0, palette = 'plasma')
    ax.set_title("Availability of ePub and PDF")
    ax.set_xlabel("Availability")
    ax.set_ylabel("Number of Books")
    sns.set_theme(style='white')
    for i in ax.containers:
        ax.bar_label(i,)
    st.pyplot()
    st.write("15,785 have neither of the formats available while a total of 12,392 have at least one option available. This means nearly 43% of books cannot be viewed as a ePub or PDF. This shows a lack of accessibility to those wanting a digital copy in these formats.")

    st.subheader("Books for Sale")
    sale_df = cleaned_df[['saleInfo.saleability']].copy()
    sale_df['saleInfo.saleability'] = np.where((cleaned_df['saleInfo.saleability'] =='FREE'), 'NOT FOR SALE', cleaned_df['saleInfo.saleability'])
    sale_df_v2 = sale_df.groupby(['saleInfo.saleability']).agg(No_of_books = ('saleInfo.saleability', 'count'))
    sale_df = cleaned_df[['saleInfo.saleability']].copy()
    sale_df['saleInfo.saleability'] = np.where((cleaned_df['saleInfo.saleability'] =='FREE'), 'NOT FOR SALE', cleaned_df['saleInfo.saleability'])
    sale_df_v2 = sale_df[['saleInfo.saleability']].value_counts()
    sale_df_v2 = sale_df_v2.reset_index()
    sale_df_v2.columns = "No_of_books",""

    colors = ['palevioletred', 'mediumpurple']
    explode = ( 0.03, 0.03)
    sale_df_v2.groupby(['No_of_books']).sum().plot(kind='pie', y='', autopct='%1.0f%%', colors=colors, explode=explode,
                                                startangle=30)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.title('Books Available for Sales', fontsize = 12)
    st.pyplot()
    st.write("Not all books are for sale in Google Books. Based on our data, 32% of books have a price tag that is available for sale online, while 68% are not for sale as partially some books are free of charge.")

    st.subheader("Books Price")
    pd.options.mode.chained_assignment = None 
    price_df = cleaned_df[['saleInfo.retailPrice.amount','saleInfo.saleability']].copy()
    price_df_forsale =price_df[price_df['saleInfo.saleability']=='FOR SALE']
    price_df_forsale_v2 = price_df_forsale[['saleInfo.retailPrice.amount']]
    price_df_forsale_v2.columns = ["saleInfo.retailPrice.amount"]
    price_df_forsale_v2['price_range']=0

    def avail(price_df_forsale_v2):
        if (price_df_forsale_v2 ['saleInfo.retailPrice.amount']<= 100) :
            return 'RM1-RM100'
        elif (price_df_forsale_v2 ['saleInfo.retailPrice.amount']<= 200):
            return 'RM101-RM200'
        elif (price_df_forsale_v2 ['saleInfo.retailPrice.amount']<= 300):
            return 'RM201-RM300'
        elif (price_df_forsale_v2 ['saleInfo.retailPrice.amount']<= 400):
            return 'RM301-RM400'
        elif (price_df_forsale_v2 ['saleInfo.retailPrice.amount']<= 500):
            return 'RM401-RM500'
        elif (price_df_forsale_v2 ['saleInfo.retailPrice.amount']> 500):
            return 'RM500 and above'
    price_df_forsale_v2['price_range'] = price_df_forsale_v2.apply(avail, axis = 1)
    # price_range = price_df_forsale_v2['price_range'].value_counts()
    price_df_forsale_v2 = price_df_forsale_v2.groupby(['price_range']).agg(No_of_books = ('price_range', 'count'))
    price_df_forsale_v2 = price_df_forsale_v2.reset_index()
    plt.figure(figsize=(10, 10))

    ax = sns.barplot(x='price_range', y='No_of_books', data=price_df_forsale_v2, errwidth=0, palette = 'plasma')
    ax.set_title("Price Range for Books for Sale")
    ax.set_xlabel("Price Range")
    ax.set_ylabel("No of Books")
    sns.set_theme(style='white')
    for i in ax.containers:
        ax.bar_label(i,)
    st.pyplot()
    st.write("80% of the books for sale price below RM100, followed by 11.2% that ranged from RM101 to RM200. This shows that the books are sold at an affordable price range that allows more readers to get access to their books of interest. From book price less than RM100, most of the books are within the price range of RM20 to RM45.")

    st.subheader("Books Costing Less Than RM 100")
    less_100_df = price_df_forsale[price_df_forsale[['saleInfo.retailPrice.amount']] <= 100]
    less_100_df = less_100_df.drop('saleInfo.saleability', inplace=False, axis=1)
    less_100_df = less_100_df.dropna().reset_index(drop=True)
    sns.histplot(data = less_100_df
                ,x = 'saleInfo.retailPrice.amount'
                ,color = 'navy'
    #             ,alpha = 0.7
                ,bins = 50
    #             ,binwidth = 1
                ,kde = True
                )
    plt.xlim(xmin=0, xmax = 100)
    sns.set_theme(style='white')
    sns.despine(top = False, right = False, bottom = False, left = False)
    plt.xlabel('Price')
    plt.ylabel('No. of Books')
    plt.title('Histogram of Books Costing Less than RM100')
    st.pyplot()

    st.subheader("Ebook Availability")
    ebook = cleaned_df['saleInfo.isEbook'].value_counts()
    ebook_1 = ebook.reset_index() 
    ebook_1.columns = "Ebook", ""

    colors = ['mediumpurple','palevioletred']
    explode = (0.03, 0.03)
    ebook_1.groupby(['Ebook']).sum().plot(kind='pie', y="", autopct='%1.0f%%', colors=colors, explode=explode,
                                                startangle=30)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.title('Ebook Availability', fontsize = 12)
    st.pyplot()
    st.write('It is observed that the Ebook availability is 67% false. This means that the books are not available as ebook.')

    st.subheader("Top 15 Most Rating Count Books")
    top_fifteen_books = cleaned_df.copy()
    top_fifteen_books.sort_values(by=['volumeInfo.ratingsCount', 'volumeInfo.averageRating'], ascending = [False, False], inplace = True)
    # display(top_fifteen_books[['volumeInfo.title', 'volumeInfo.ratingsCount', 'volumeInfo.averageRating']].head(15))
    plt.figure(figsize=(10, 10))

    data = top_fifteen_books.head(15)
    gr = sns.barplot(x="volumeInfo.ratingsCount", y="volumeInfo.title", data=data, palette="plasma")
    sns.set_theme(style='white')
    plt.xlabel('Ratings Count')
    plt.ylabel('Books')
    plt.title('Top 15 Books with Most Ratings Count')
    for i in gr.patches:
        gr.text(i.get_width() + .05, i.get_y() + 0.5, str(round(i.get_width())), fontsize = 10, color = 'k')
    st.pyplot()
    st.write("The graphs below showcased the top 15 books with the highest ratings count. From the graphs, it is noticed that 'Heaven is for Real' has the highest rating count among all the books, with the rating count at least 1x more than the other books. There are no significance difference in ratings count if compared between the rest of the books.")

    st.subheader("Top 15 Rated Books")
    plt.figure(figsize=(10, 10))

    data = top_fifteen_books.head(15).sort_values(by='volumeInfo.averageRating', ascending = False)
    gr = sns.barplot(x="volumeInfo.averageRating", y="volumeInfo.title", data=data, palette="plasma")
    sns.set_theme(style='white')
    plt.xlabel('Average Rating')
    plt.ylabel('Books')
    plt.title('Average Rating of the Top 15 Books with Most Ratings Count')
    for i in gr.patches:
        gr.text(i.get_width() + .05, i.get_y() + 0.5, str(i.get_width()), fontsize = 10, color = 'k')
    st.pyplot()
    st.write("Out of the top 15 highest ratings count books, it is observed that 'Unbroken' has the highest ratings, i.e. 4.5, followed by 'Heaven is for Real','The Giving Tree', 'The Giver' and 'A People History of the United States' that score 4.0. Noted that none of the books above attained 5.0 ratings. This is because the number of ratings is taken into consideration. Thus, books with 5.0 ratings but with only a few number of ratings will not be shown here.")

    st.subheader("Distribution of average_rating")
    cleaned_df['volumeInfo.averageRating'] = cleaned_df['volumeInfo.averageRating'].astype(float)
    averageRating_df = cleaned_df[cleaned_df['volumeInfo.averageRating'] > 0]

    fig, ax = plt.subplots(figsize=[15,10])

    sns.histplot(averageRating_df['volumeInfo.averageRating'],ax=ax,color = 'navy'
                ,alpha = 0.7
                ,bins = 20)
    ax.set_title('Average rating distribution for all books',fontsize=20)
    ax.set_xlabel('Average rating',fontsize=13)
    ax.set_ylabel('Ratings count',fontsize=13)
    st.pyplot()
    st.write('Overall, most books sit at ratings 3.0 and above, and a huge portion of the books are with rating 4.0.')

    st.subheader("Maturity_Rating")
    maturity_rate_df = cleaned_df[['volumeInfo.maturityRating']].value_counts()
    maturity_rate_df = maturity_rate_df.reset_index()
    maturity_rate_df.columns = "Maturity_Rating", ""
    maturity_rate_df = maturity_rate_df.groupby(['Maturity_Rating']).sum()
    colors = ['palevioletred','mediumpurple']
    explode = (0.03, 0.03)
    maturity_rate_df.plot(kind='pie', y='', autopct='%1.0f%%', colors=colors,explode=explode)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.title('Maturity Rating', fontsize = 15)
    st.write('Based on the pie chart below, most books are suitable for all ages.')
    st.pyplot()
    

if add_sidebar == 'Book Recommendation Engine':
    st.subheader('Start searching for your preferred books here!')
    st.write ('This engine will recommend the Top 10 books that are similar to your collective stated preferences.')
    st.write ('You may input between 1 to 5 choices, your ranking will not affect the results.')
    st.write ('\n')

    #Genre Selection

    # Create a dictionary of data
    # A total of 78,188 unique rows
    # st.write(len(options_df2))
    options_df = cleaned_df[['volumeInfo.title','volumeInfo.categories','volumeInfo.authors']].copy()
    options_df2=options_df.dropna()
    options_df2=options_df.dropna(axis=0)
    options_df2["volumeInfo.title"]= options_df2["volumeInfo.title"].apply(lambda x: x.strip().title())
    options_df2["volumeInfo.categories"]= options_df2["volumeInfo.categories"].apply(lambda x: x.strip().title())
    options_df2["volumeInfo.authors"] = options_df2["volumeInfo.authors"].apply(lambda x: x.strip().title())
    options_df2 = options_df2[options_df2["volumeInfo.title"] != 'Missing']
    options_df2 = options_df2[options_df2["volumeInfo.categories"] != 'Missing']
    options_df2 = options_df2[options_df2["volumeInfo.authors"] != 'Missing']



    # Create an empty DataFrame to store filtered data
    df_filtered = pd.DataFrame()

    # Initialize the author_select variable
    author_select = None

    # Get a list of 15 unique genre options from the original DataFrame
    options_df2.sort_values(by=['volumeInfo.categories'], ascending=True, inplace = True)
    genre_options = options_df2['volumeInfo.categories'].unique()
    # genre_options = np.random.choice(genre_full_options,15,replace=False)

    # Create a multi-select widget to select genres
    genre_select = st.multiselect("Which are your top 5 preferred genres?", genre_options, key="genre",max_selections=5)
    
    #Create a flag to track if the genre select has been changed
    genre_select_changed = False

    # If the user selects one or more genres:
    if genre_select:
        # Set the flag to indicate the genre select has been changed
        genre_select_changed = True
        
        # Filter the original DataFrame to only include rows with the selected genres
        options_df2.sort_values(by=['volumeInfo.authors'], ascending=True, inplace = True)
        df_filtered = options_df2[options_df2['volumeInfo.categories'].isin(genre_select)]
        
        # Get a list of unique author options from the filtered DataFrame
        author_options = df_filtered['volumeInfo.authors'].unique()
        
        # Create a multi-select widget to select authors
        author_select = st.multiselect("Which are your preferred author(s)?", author_options, key="author",max_selections=5)

    # If the user selects one or more authors, but the genre select has not been changed:
    if author_select and not genre_select_changed:
        # Filter the original DataFrame to only include rows with the selected authors
        df_filtered = options_df2[options_df2['volumeInfo.authors'].isin(author_select)]
        
        # Get a list of unique genre options from the filtered DataFrame
        genre_options = df_filtered['volumeInfo.categories'].unique()
        
        # Create a multi-select widget to select genres
        genre_select = st.multiselect("Which are your top 5 preferred genres?", genre_options, key="genre",max_selections=5)

    # If author_select option is not empty, display it
    if  author_select:

        # Use pickle to load the pre-trained model.
        with open(f'book_kmeans_model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Use pickle to load the tfidf vectorizer.
        with open(f'book_tfidf.pkl', 'rb') as f:
            tfidf_vectorizer = pickle.load(f)

        # Use pickle to load the SVD.
        with open(f'book_svd.pkl', 'rb') as f:
            svd_model = pickle.load(f)
        
        # read csv file with segments
        book_with_cluster_df = pd.read_csv("book segments.csv")

        # rename the first and second columns
        book_with_cluster_df.rename(columns={ book_with_cluster_df.columns[0]: "idx" }, inplace = True)
        book_with_cluster_df.rename(columns={ book_with_cluster_df.columns[1]: "title" }, inplace = True)

    
        
    # Function to recommend books
        def recommendBooks(genres, authors):
            # format user preference, trim and join in sentence, then put in a list
            user_pref = [i.strip() for i in genres] + [i.strip() for i in authors]
            user_pref_sen = " ".join([i.strip() for i in user_pref])
            user_pref_sen = [user_pref_sen]
            
            # vectorize the user input, fit into SVD
            tfidf_test_matrix = tfidf_vectorizer.transform(user_pref_sen)
            test_svd_data = svd_model.transform(tfidf_test_matrix)
            
            # predict the book cluster using pre-trained model
            cluster = model.predict(test_svd_data)[0]
            
            # filter the books in the same segments
            book_in_cluster_df = book_with_cluster_df[book_with_cluster_df['segment']==cluster]
            
            # reset the index (for merging later)
            book_in_cluster_df.reset_index(inplace=True)
            
            # a dataframe with index and book title
            indices_df = pd.DataFrame(book_in_cluster_df['title'])
            
            # vectorize the books with same segment
            tfidf_cluster_matrix = tfidf_vectorizer.transform(book_in_cluster_df['sentence_preprocessed'])
            
            # find the cosine similarity of user preference and the books within the same segment
            similarities = cosine_similarity(tfidf_cluster_matrix, tfidf_test_matrix)
            
            # convert similarities numpy array into dataframe
            similarities_df = pd.DataFrame(similarities, columns=['cos_sim'])
            
            # merge books with the cosine similarities df
            book_similarities_df = pd.concat([indices_df, similarities_df], axis=1)
            
            # drop any duplicate books (book with same title)
            book_similarities_df.drop_duplicates(subset = ['title'], keep = 'first', inplace = True)
            
            # get top 10 books with highest cosine similarity
            top10_book_similarities_df = book_similarities_df.sort_values('cos_sim',ascending = False).head(10)
            
            # save the books in a list
            top10_recommend_books = top10_book_similarities_df['title'].tolist()
            return top10_recommend_books

        user_genres = genre_select
        user_authors = author_select
        user_top10_recommended_books = recommendBooks(user_genres, user_authors)
        user_top10_recommended_books_df = pd.DataFrame(user_top10_recommended_books)
        user_top10_recommended_books_df.rename(columns={user_top10_recommended_books_df.columns[0]: "Book Title"}, inplace = True)
        # user_top10_recommended_books_df.sort_values("Book Title",ascending = True, inplace = True)
        st.write("Here are some recommendations for you.")
        st.write(user_top10_recommended_books_df)
