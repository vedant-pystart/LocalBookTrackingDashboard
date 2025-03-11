from dash import Dash, html, dash_table, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


"""
==================================================
1. DATA PREPROCESSING
==================================================
"""

# Load and preprocess data
df = pd.read_excel("/Users/vedant/Documents/Python/Google Sheets Book Tracker/Book Log.xlsx")  
df = df.iloc[:, 0:18]  
df = df.dropna(how="all")  
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Book Link"] = df["Book"].apply(lambda book: f"/book/{book.replace(' ', '_')}")
df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
df["End Date"] = pd.to_datetime(df["End Date"], errors="coerce")
df["Start Year"] = df["Start Date"].dt.year
df["Start Month"] = df["Start Date"].dt.month_name()
df["End Year"] = df["End Date"].dt.year
df["End Month"] = df["End Date"].dt.month_name()

year_options = [{"label": str(int(year)), "value": int(year)} for year in sorted(df["Start Year"].dropna().unique())]
month_options = [{"label": month, "value": month} for month in [
    "January", "February", "March", "April", "May", "June", "July", "August", 
    "September", "October", "November", "December"
]]

unique_genres = sorted(set(df["Genre"].dropna().str.split(", ").explode()))

genre_options = [{"label": str(genre), "value": str(genre)} for genre in unique_genres]

# print(unique_genres)


df["Start Date"] = df["Start Date"].dt.strftime('%b %d, %Y')  
df["End Date"] = df["End Date"].dt.strftime('%b %d, %Y')  


"""
==================================================
2. Visualization Creation
==================================================
"""

print(df.head())

fig = px.scatter(df, x = 'Page Ct.', y = 'Rating', hover_name="Book", hover_data = ['Author'], color = 'Author')

fig.update_layout(showlegend=False)

fig.show()


treemap_data = df.groupby(['Genre', 'Author']).size().reset_index(name="Book Count")

# Create Treemap
fig1 = px.treemap(treemap_data, 
                 path=['Genre', 'Author'],  # Hierarchical path (Genre > Author)
                 values='Book Count',       # Value for size of the block
                 color='Book Count',        # Color based on the number of books
                 color_continuous_scale='RdYlGn',  # Color scale (adjust as needed)
                 title="Books by Genre and Author")

# Show the figure
fig1.show()

