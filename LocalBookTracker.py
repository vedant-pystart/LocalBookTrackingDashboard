from dash import Dash, html, dash_table, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

"""
==================================================
1. DATA PREPROCESSING
==================================================
"""

# Load and preprocess data
df = pd.read_excel("Google Sheets Book Tracker/Book Log.xlsx")  
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

    # Status Dropdown
    dcc.Dropdown(["Complete", "Reading", "To Be Read"], ["Complete"], multi=True, id="DropdownBookStatus", 
                 style={"width": "75%", "margin": "auto", "fontFamily": "Arial, sans-serif"}),  

    # Recommended Dropdown
    # html.H2("Filter by Recommendation", style={"textAlign": "center", "fontFamily": "Arial, sans-serif"}),
    dcc.Dropdown(
        id="rec-dropdown",
        options=[
            {"label": "Yes", "value": "Yes"},
            {"label": "No", "value": "No"}, 
            {"label": "All", "value": "All"}
        ],
        value="Yes",
        style={"width": "75%", "margin": "auto", "fontFamily": "Arial, sans-serif"}
    ),

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


    html.H2("Ratings Distribution", style={"textAlign": "center", "fontFamily": "Arial, sans-serif"}),
    dcc.Graph(id="ratings_histogram"),
    html.Hr(),


    

  
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
    Input("DropdownBookStatus", "value") 
)
def update_table(status_values):
    df_filtered1 = df_filtered[df_filtered["Status"].isin(status_values)]  
    return df_filtered1.to_dict("records")

# Update visualization based on recommendation filter
@callback(
    Output("ratings_histogram", "figure"),
    Input("rec-dropdown", "value")
)
def update_vis(rec_value):
    if rec_value == "All":
        df_filtered_by_rec = df
    else: 
        df_filtered_by_rec = df[df["Rec?"] == rec_value]

    if df_filtered_by_rec.empty:
        return {
            'data': [],
            'layout': {'title': f'No Data Available for Rec? = {rec_value}'}
        }

    # Create histogram
    vis = px.histogram(
        df_filtered_by_rec, 
        x="Rating", 
        nbins=25,
        title=f"Ratings Distribution: {rec_value}",
        labels={"Rating": "Ratings"}
    )
    return vis

if __name__ == "__main__":
    app.run(debug=True)