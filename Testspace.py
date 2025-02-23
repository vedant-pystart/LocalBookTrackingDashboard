import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Input, Output
import datetime

app = Dash()

# Load and preprocess data
df = pd.read_excel("/Users/vedant/Documents/Python/Google Sheets Book Tracker/Book Log.xlsx")  
df = df.iloc[:, 0:17]  
df = df.dropna(how="all")  
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Book Link"] = df["Book"].apply(lambda book: f"[More Info](/book/{book.replace(' ', '_')})")
df["hello"] = "hello"


# Convert Start and End Dates to datetime format
df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
df["End Date"] = pd.to_datetime(df["End Date"], errors="coerce")

# Add separate year and month columns for Start Date and End Date
df["Start Year"] = df["Start Date"].dt.year
df["Start Month"] = df["Start Date"].dt.month_name()
df["End Year"] = df["End Date"].dt.year
df["End Month"] = df["End Date"].dt.month_name()


# Remove NaT values if any
df = df.dropna(subset=["Start Date", "End Date"])
year_options = [{"label": str(int(year)), "value": int(year)} for year in sorted(df["Start Year"].dropna().unique())]
month_options = [{"label": month, "value": month} for month in [
    "January", "February", "March", "April", "May", "June", "July", "August", 
    "September", "October", "November", "December"
]]

# Format Start and End Dates as strings in the format 'MMM DD, YYYY'
df["Start Date"] = df["Start Date"].dt.strftime('%b %d, %Y')  
df["End Date"] = df["End Date"].dt.strftime('%b %d, %Y')  

# App layout
app.layout = html.Div([

    html.Label("Select Year:", style={"fontWeight": "bold"}),
    dcc.Dropdown(
        id="year_dropdown",
        options=year_options,
        placeholder="Select a year",
        clearable=True,
        multi = True
    ),

    html.Label("Select Month(s):", style={"fontWeight": "bold"}),
    dcc.Dropdown(
        id="month_dropdown",
        options=month_options,
        multi=True,
        placeholder="Select Month(s)"
    ),


    dash_table.DataTable(
        data=df.assign(**{"Book Link": df["Book Link"].apply(lambda x: f"[More Info]({x})")}).to_dict("records"),
        columns=[
            {"name": "Status", "id": "Status"},
            {"name": "Book", "id": "Book"},
            {"name": "Author", "id": "Author"},
            {"name": "Rating", "id": "Rating"},
            {"name": "Recommended By", "id": "Recommended By"},
            {"name": "Start Date", "id": "Start Date"},
            {"name": "End Date", "id": "End Date"},
            {"name": "More Info", "id": "Book Link", "presentation": "markdown"},
        ],
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
])

@app.callback(
    Output("MainBookTable", "data"),
    [
        Input("year_dropdown", "value"),
        Input("month_dropdown", "value")
    ]
)
def update_table(selected_years, selected_months):
    # If years are selected, filter by the start year and end year
    if selected_years:
        filtered_df = df[df["Start Year"].isin(selected_years) | df["End Year"].isin(selected_years)]
    else:
        filtered_df = df
    
    # If months are selected, filter by start month and end month
    if selected_months:
        # Filter based on both the start and end month/year
        filtered_df = filtered_df[
            ((filtered_df["Start Year"].isin(selected_years)) & (filtered_df["Start Month"].isin(selected_months))) | 
            ((filtered_df["End Year"].isin(selected_years)) & (filtered_df["End Month"].isin(selected_months)))
        ]
        
    return filtered_df.assign(**{"Book Link": filtered_df["Book Link"].apply(lambda x: f"{x}")}).to_dict("records")

if __name__ == "__main__":
    app.run(debug=True)