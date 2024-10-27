import pandas as pd
import streamlit as st
import ast  # Import ast for safe evaluation

# Load your data from the project directory
data = pd.read_csv('simplelindygraft.csv')  # Make sure the CSV is in the same folder as app.py

# Replace NaN values in the 'citations per year' column with an empty list
data['citations per year'] = data['citations per year'].fillna('[]')

# Convert the 'citations per year' column from string representation to lists
data['citations per year'] = data['citations per year'].apply(ast.literal_eval)

def calculate_lindy_scores(data):
    scores = []
    for graft in data['graft'].unique():
        graft_data = data[data['graft'] == graft]

        # Flatten the citations lists and filter out any empty lists
        all_citations = [cite for sublist in graft_data['citations per year'] for cite in sublist if sublist]
        
        if all_citations:  # Check if the list is not empty
            citations_per_year = sum(all_citations) / len(all_citations)  # Average citations per year
            total_citations = sum(all_citations)  # Total citations
        else:
            citations_per_year = 0  # Default to 0 if no citations available
            total_citations = 0

        # Assuming 'age' is another column in your DataFrame; replace 'age' with the actual column name
        age = graft_data['age'].mean() if 'age' in graft_data else 0  # Default to 0 if no age data

        # Calculate a Lindy score (example calculation)
        lindy_score = citations_per_year * age  # You can modify this formula as needed
    
        # Append the results as a tuple (graft, age, total citations, citations per year, lindy score)
        scores.append((graft, age, total_citations, citations_per_year, lindy_score))

    return scores

# Get the scores
lindy_scores = calculate_lindy_scores(data)

# Create a DataFrame from the scores list
scores_df = pd.DataFrame(lindy_scores, columns=['Graft', 'Age', 'Total Citations', 'Citations per Year', 'Lindy Score'])

# Filter out rows where 'Citations per Year' is None or 0
scores_df = scores_df[scores_df['Citations per Year'] > 0]

# Display scores in Streamlit
st.write(scores_df)

