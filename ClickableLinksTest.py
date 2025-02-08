from dash import Dash, html, dash_table, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load and preprocess data
df = pd.read_excel("/Users/vedant/Documents/Python/Google Sheets Book Tracker/Book Log.xlsx")  
df = df.iloc[:, 0:18]  
df = df.dropna(how="all")  
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df["Book Link"] = df["Book"].apply(lambda book: f"/book/{book.replace(' ', '_')}")

# Create the app
app = Dash()

# Define layout with both the table and the location for different pages
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Tracks URL changes
    html.Div(id="page-content"),  # Placeholder for different pages (content changes here)
])

# Callback to display the correct page based on the URL
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname.startswith("/book/"):
        book_name = pathname.split("/book/")[1].replace("_", " ")
        book_data = df[df["Book"] == book_name]

        if book_data.empty:
            return html.H1("Book Not Found")

        book_info = book_data.iloc[0]
        
        return html.Div([
            html.H1(book_info["Book"], style={"textAlign": "center"}),
            html.Hr(),
            html.H3(f"Author: {book_info['Author']}"),
            html.H3(f"Status: {book_info['Status']}"),
            html.H3(f"Recommendation: {book_info['Rec?']}"),
            html.H3(f"Recommended By: {book_info['Recommended By']}"),
            html.H3(f"Start Date: {book_info['Start Date']}"),
            html.H3(f"End Date: {book_info['End Date']}"),
            html.P(f"Summary: {book_info['Summary']}"),
            html.P(f"Core Themes: {book_info['Core Themes']}"),
            html.P(f"Review: {book_info['Review']}"),
            html.P(f"What I Gained from Reading: {book_info['What I gained from reading']}"),
            html.P(f"Story Behind Finding the Book: {book_info['Story behind finding the book']}"),
            html.H3(f"Genre: {book_info['Genre']}"),
            html.H3(f"Personal Collection: {book_info['Personal Collection?']}"),
            html.H3(f"Series/Standalone: {book_info['Series/Standalone?']}"),
            html.H3(f"Page Count: {book_info['Page Ct.']}"),
            html.A("Back to Home", href="/"),
        ])

    else:
        return html.Div([
            html.H1("Local Book Tracking Analytics Dashboard", style={"textAlign": "center"}),
            dash_table.DataTable(
                data=df.assign(**{"Book Link": df["Book Link"].apply(lambda x: f"[More Info]({x})")}).to_dict("records"),
                columns=[
                    {"name": "Book", "id": "Book"},
                    {"name": "Status", "id": "Status"},
                    {"name": "Rating", "id": "Rating"},
                    {"name": "More Info", "id": "Book Link", "presentation": "markdown"},
                ],
                id="MainBookTable",
            ),
        ])

if __name__ == "__main__":
    app.run(debug=True)