from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

books = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', on_bad_lines = 'skip')\
.sort_values(by = ['average_rating', '  num_pages'], ascending = False)[['title', 'authors', 'language_code', 'average_rating', '  num_pages']]

selection_auteur = [{'label' : auteur, 'value' : auteur} for auteur in sorted(books['authors'].unique())]
selection_langue = [{'label' : langue, 'value' : langue} for langue in sorted(books['language_code'].unique())]

# Layout
app.layout = dbc.Card([
    dbc.CardHeader('www.readersaddicts.com'),
    dbc.Row([
        dbc.Col(html.H1('Bienvenue sur le site Readers Addicts !'), width=12),
        html.Div([
            dbc.Tabs([
                dbc.Tab(label = 'Sélection des livres', children = [ 
                    html.P("Veuillez sélectionner un auteur, une langue et le nombre de pages souhaité :"),
                    html.Label('Sélectionnez un auteur :'),
                    dcc.Dropdown(
                        id = 'input-author',
                        options = selection_auteur,
                        value = 'Agatha Christie'
                    ),

                    html.Label('Sélectionnez une langue :'),
                    dcc.Dropdown(
                        id = 'input-language',
                        options = selection_langue,
                        value = 'eng'
                    ),

                    html.Label('Sélectionnez un nombre de pages:'),
                    dcc.Slider(
                        id = 'page-selection',
                        min = books['  num_pages'].min(),
                        max = books['  num_pages'].max(),
                        value = books['  num_pages'].max(),
                        step = 100,
                        marks={i: str(i) for i in range(0, books['  num_pages'].max() + 150, 150)},
                        tooltip = {'placement' : 'bottom', 'always_visible' : True}
                    ),
                    dcc.Graph(
                        id = 'nombre_page_graph',
                    )
                ]),
                dbc.Tab(label = 'Notes des meilleurs livres pour l\'auteur', children = [
                    dcc.Graph(
                        id = 'Top50_avg_rating_graph',
                    )
                ])
            ])
        ])
    ]),
    dbc.CardFooter('Merci pour votre visite et à bientôt !')
])

@app.callback(
    Output('nombre_page_graph', 'figure'),
    [Input('input-author', 'value'),
     Input('input-language', 'value'),
     Input('page-selection', 'value')]
)
def update_graph(selected_author, selected_language, selected_pages):
    filtered_books = books.copy()
    
    filtered_books = books[(books['authors'] == selected_author) & (books['language_code'] == selected_language) & (books['  num_pages'] <= selected_pages)]

    fig = px.bar(filtered_books.iloc[:50, :], x = '  num_pages', y = 'title', title = f'Nombre de pages par livres pour l\'auteur {selected_author} et dans la langue {selected_language}', height=800, width=1500)
    return fig

@app.callback(
    Output('Top50_avg_rating_graph', 'figure'),
    [Input('input-author', 'value'),
     Input('input-language', 'value'),
     Input('page-selection', 'value')]
)

def update_top50_graph(selected_author, selected_language, selected_pages):
    filtered_books = books.copy()

    filtered_books = books[(books['authors'] == selected_author) & (books['language_code'] == selected_language) & (books['  num_pages'] <= selected_pages)]

    filtered_books_sorted = filtered_books.sort_values(by = 'average_rating', ascending = False)
    top_50_df = filtered_books_sorted.head(50)
    
    fig = px.bar(top_50_df, x = 'average_rating', y = 'title', title = 'Note des livres', height = 800, width = 1500)
    return fig


if __name__ == '__main__':
    app.run_server()