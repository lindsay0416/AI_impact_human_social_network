# Clustering: https://scikit-learn.org/stable/modules/clustering.html#clustering
# Use LLM to extract the aspect and opinion.
# Use prompt engineering to improve the accuracy of LLM's output.

# Aspects: Extract from the original topcis.
# Opinion: Extract from the original comments and simulation results
# Cluster the opinion in the original comments and simulation results
# Profile analysis: 
# 1. Profiles of positive opinion for each topic, 
# 2. Profiles of negative opinion for each topicn, 
# 3. profile each cluster

# https://huggingface.co/siebert/sentiment-roberta-large-english

import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('./dataset/nyt-articles-2020.csv')

# Filter the rows where the 'uniqueID' column contains the string "1db9abc2756a"
filtered_df = df[df['uniqueID'].str.contains("1db9abc2756a", na=False)]

# Display the filtered rows
print(filtered_df)

def main():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('./dataset/nyt-articles-2020.csv') 
    # https://www.nytimes.com/2020/02/05/us/politics/trump-acquitted-impeachment.html#:~:text=WASHINGTON%20%E2%80%94%20After%20five%20months%20of,acrimonious%20impeachment%20trial%20to%20its

    # Filter the rows where the 'uniqueID' column contains the string "1db9abc2756a"
    filtered_df = df[df['uniqueID'].str.contains("1db9abc2756a", na=False)]

    # Print the whole content in the 'headline' column of the filtered rows
    for headline in filtered_df['headline']:
        print(headline)

    # Save the filtered rows to a new CSV file
    filtered_df.to_csv('filtered_nyt_articles.csv', index=False)





if __name__ == '__main__':
    main()
