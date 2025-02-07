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

df_filtered = df[["Status"] + df.columns[:2].tolist()]  


"""
==================================================
2. DASH APPLICATION FEATURES
==================================================
"""

app = Dash()

app.layout = html.Div([
    html.H1("Local Book Tracking Analytics Dashboard", style={"textAlign": "center", "fontFamily": "Arial, sans-serif"}),  
    html.Hr(),  

# Book Status Label and Dropdown
html.Div([
    html.Label("Book Status:", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "fontSize": "16px", "width": "150px"}),
    dcc.Dropdown(
        ["Complete", "Reading", "To Be Read"], 
        ["Complete"], 
        multi=True, 
        id="DropdownBookStatus", 
        style={"width": "75%", "fontFamily": "Arial, sans-serif"}
    )
], style={"width": "75%", "margin": "auto", "display": "flex", "alignItems": "center", "gap": "10px"}),

# Recommendation Label and Dropdown
html.Div([
    html.Label("Recommendation:", style={"fontSize": "16px", "fontFamily": "Arial, sans-serif", "fontWeight": "bold", "width": "150px"}),
    dcc.Dropdown(
        id="rec-dropdown",
        options=[
            {"label": "Yes", "value": "Yes"},
            {"label": "No", "value": "No"},
        ],
        value=["Yes"],  # Default to 'Yes'
        multi=True,  # Allow multiple selection
        style={"width": "75%", "fontFamily": "Arial, sans-serif"}
    ),
], style={"width": "75%", "margin": "auto", "display": "flex", "alignItems": "center", "gap": "10px"}),

html.Hr(),

        # Table
    dash_table.DataTable(
        data=df_filtered.to_dict("records"), 
        id="MainBookTable",
        style_table={"width": "80%", "margin": "auto"},  
        style_data={"fontFamily": "Arial, sans-serif", "fontSize": "14px", "fontWeight": "bold", "textAlign": "center"},
        style_header={"fontFamily": "Arial, sans-serif", "fontSize": "22px", "fontWeight": "bold", "backgroundColor": "#f4f4f4", "textAlign": "center", "padding": "10px"},
        style_data_conditional=[
            {"if": {"column_id": "Status", "filter_query": '{Status} = "Complete"'}, "color": "green", "fontWeight": "bold", "fontStyle": "italic"},
            {"if": {"column_id": "Status", "filter_query": '{Status} = "To Be Read"'}, "color": "#8B0000", "fontWeight": "bold", "fontStyle": "italic"},
            {"if": {"column_id": "Status", "filter_query": '{Status} = "Reading"'}, "color": "orange", "fontWeight": "bold", "fontStyle": "italic"}
        ]
    ),   
    html.Hr(),

    dcc.Graph(id="ratings_histogram"),
    html.Hr(),
  
    # Ratings Distribution Visualization


])

"""
==================================================
3. DASH CALLBACKS
==================================================
"""

@callback(
    Output("MainBookTable", "data"),  
    [Input("DropdownBookStatus", "value"), Input("rec-dropdown", "value") ] 
)
def update_table(status_values, rec_values):
    # If both "Yes" and "No" are selected, show both
    if not rec_values:  # If no values selected, show all
        df_filtered1 = df[df["Status"].isin(status_values)]
    else:
        # Filter based on selected recommendations (Yes and/or No)
        df_filtered1 = df[(df["Status"].isin(status_values)) & (df["Rec?"].isin(rec_values))]
    
    # Ensure we keep only the relevant columns for display
    df_filtered1 = df_filtered1[["Status", "Book", "Author", "Rating", "Recommended By"]]  # Selecting specific columns
    return df_filtered1.to_dict("records")

# Update visualization based on recommendation filter
@callback(
    Output("ratings_histogram", "figure"),
    Input("rec-dropdown", "value")
)
def update_vis(rec_values):
    if "All" in rec_values or not rec_values:  
        dfvis1 = df
    else:
        # Filter based on selected values for 'Rec?'
        dfvis1 = df[df["Rec?"].isin(rec_values)]

    # Categorize the ratings into buckets (you can adjust ranges as needed)
    rating_bins = pd.cut(dfvis1['Rating'], bins=[0, 5, 7, 10], labels=["Low", "Medium", "High"])

    # Add a new column for the rating categories
    dfvis1['Rating Category'] = rating_bins

    # Create histogram
    vis = px.histogram(
        dfvis1, 
        x="Rating",  # Show rating distribution
        nbins=20,  # Adjust number of bins as necessary
        color="Rating Category",  # Color based on the rating category
        color_discrete_map={"Low": "#8B0000", "Medium": "orange", "High": "green"},  # Set color map
        title="Ratings Distribution"
    )
    # Update layout for custom title styling, axis removal, and no legend
    vis.update_layout(
        title={
            'text': 'Ratings Distribution',  # Title text
            'font': {
                'family': 'Arial, sans-serif',  # Font type
                'size': 24,  # Font size
                'color': 'black',  # Font color
                'weight': 'bold'  # Font weight
            },
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center'  # Align the title to the center
        },
        yaxis=dict(
            showticklabels=False,  # Hides the labels (numbers) on the y-axis
            showgrid=False,  # Removes the grid lines
            zeroline=False,  # Hides the zero line
            title=""  # Remove y-axis title
        ),
        xaxis=dict(
            showgrid=True,  # Keeps the grid on the x-axis
            zeroline = True, 
            linecolor = "black"
        ),
        legend=dict(
            visible=False  # Hides the legend
        ), 
        plot_bgcolor='white',  # Sets the background color of the plot area (the actual graph area)
        paper_bgcolor='white',  # Sets the background color of the entire figure (including title, margins)
        hoverlabel=dict(
        bgcolor="rgba(255,255,255,0.7)",  # Slightly transparent background for hover
        font_size=14,  # Font size for hover label
        font_family="Arial, sans-serif",  # Font for hover label
        font_color="black"  # Hover label text color
    ),
    bargap=0.01,  # Reduce the gap between bars for a more packed look
    margin=dict(t=40, b=30, l=40, r=40),  # Reduce margins for compactness
    hovermode="closest"  # More responsive hover
    )

    

    return vis


if __name__ == "__main__":
    app.run(debug=True)