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


import pandas as pd

def read_article_dataset(file_path, articleID):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Print the column names
    print("Column names:", df.columns.tolist())

    # Filter the rows where the 'uniqueID' column contains the specified string
    filtered_df = df[df['articleID'].str.contains(articleID, na=False)]

    # Display the filtered rows
    print(filtered_df)

    # Write the filtered DataFrame to a new CSV file
    filtered_df.to_csv('read_wine_dataset_comments.csv', index=False)

if __name__ == "__main__":
    # Define the path to the CSV file
    file_path = './dataset/nyt-comments-2020.csv'
    articleID = '4fd9aff5b1ba'

    # Call the function to print the column names and write the filtered DataFrame to a new CSV file
    read_article_dataset(file_path, articleID)