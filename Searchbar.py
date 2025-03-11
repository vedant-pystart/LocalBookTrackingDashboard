import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

# Sample data
data = {
    'Column1': ['apple', 'banana', 'cherry', 'date', 'elderberry'],
    'Column2': ['fruit', 'fruit', 'fruit', 'fruit', 'fruit'],
    'Column3': ['red', 'yellow', 'red', 'brown', 'purple']
}
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Wildcard Search Example"),
    dcc.Input(id='search-bar', type='text', placeholder='Search...', debounce=True),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'}
    )
])

# Callback to update table based on search query
@app.callback(
    Output('table', 'data'),
    [Input('search-bar', 'value')]
)
def filter_table(search_value):
    if not search_value:
        return df.to_dict('records')
    
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_value, case=False, na=False).any(), axis=1)]
    
    return filtered_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)