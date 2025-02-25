import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table, dcc, callback, Input, Output

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


df['month_year'] = df['End Date'].dt.strftime('%Y-%m')

# print(df["month_year"])

values_list = df.groupby(["month_year"]).size().reset_index(name="Book Count")

values_list.columns = ['Date', 'Books Read']

values_list["Date"] = pd.to_datetime(values_list["Date"])

# print(values_list)

fig = px.line(values_list, x='Date', y='Books Read', title='Books Read Per Month', markers=True)

# Update the layout with styling similar to your histogram example
fig.update_layout(
    title={
        'text': 'Books Read Per Month',  # Title text
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
        showticklabels=True,  # Show labels on the y-axis
        showgrid=False,  # Remove grid lines
        zeroline=False,  # Hide the zero line
        title="Books Read"  # Set y-axis title
    ),
    xaxis=dict(
        showgrid=True,  # Keep grid on the x-axis
        zeroline=True,  # Show the zero line
        linecolor="black"  # Change x-axis line color to black
    ),
    plot_bgcolor='white',  # Set the background color of the plot area
    paper_bgcolor='white',  # Set the background color of the entire figure
    hoverlabel=dict(
        bgcolor="rgba(255,255,255,0.7)",  # Slightly transparent background for hover
        font_size=14,  # Font size for hover label
        font_family="Arial, sans-serif",  # Font for hover label
        font_color="black"  # Hover label text color
    ),
    margin=dict(t=40, b=30, l=40, r=40),  # Adjust margins for compactness
    hovermode="closest",  # More responsive hover
    legend=dict(
        visible=False  # Hide the legend
    )
)

# Update the line thickness
fig.update_traces(line=dict(width=7, color = 'navy'), marker=dict(size=15, symbol = 'circle'))  # Line thickness and marker size

fig.update_traces(
    hovertemplate='%{x|%B %Y}<br>Books Read: %{y}<extra></extra>'  # Format x as Month Year and customize tooltip
)

app = Dash()

app.layout = html.Div([
    dcc.Graph(figure = fig)
])




if __name__ == "__main__":
    app.run(debug=True)

# from dash import Dash, html, dcc, Input, Output

# app = Dash(__name__)

# # Layout with hidden sort controls and a button to reveal them
# app.layout = html.Div([
#     html.Button("Show/Hide Sorting Options", id="toggle-button", n_clicks=0),
    
#     html.Div(id="sort-options", children=[
#         html.Label("Sort by:"),
#         dcc.Dropdown(
#             id="sort-dropdown",
#             options=[{"label": "Rating", "value": "Rating"},
#                      {"label": "Start Date", "value": "Start Date"}],
#             value="Rating"
#         ),
#         html.Button("Sort", id="sort-button"),
#     ], style={"display": "none"})  # Initially hidden
    
# ])

# # Callback to toggle the display of the sort options
# @app.callback(
#     Output("sort-options", "style"),
#     Input("toggle-button", "n_clicks")
# )
# def toggle_sort_options(n_clicks):
#     if n_clicks % 2 == 1:
#         return {"display": "block"}  # Show the sorting options
#     return {"display": "none"}  # Hide the sorting options


# if __name__ == '__main__':
#     app.run_server(debug=True)