# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
    id='site-dropdown',
    options=[{'label': 'All Sites', 'value': 'ALL'}] +  # Default “All Sites” option
            [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
    value='ALL',  # Default selection
    placeholder="Select a Launch Site here",
    searchable=True
)

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                               # Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Pie chart for total success launches by site
        fig = px.pie(
            spacex_df, 
            names='Launch Site',       # Each launch site as a slice
            values='class',            # Count of successes (class=1)
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        # Filter data for the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Pie chart for success vs failure at this site
        fig = px.pie(
            filtered_df,
            names='class',             # 0 = Failure, 1 = Success
            title=f'Success vs Failure for {entered_site}'
        )
        return fig


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
# Range Slider to select payload range
dcc.RangeSlider(
    id='payload-slider',
    min=0,                       # Slider starts at 0 Kg
    max=10000,                   # Slider ends at 10000 Kg
    step=1000,                   # Interval of 1000 Kg
    marks={i: str(i) for i in range(0, 10001, 1000)},  # Show marks every 1000 Kg
    value=[spacex_df['Payload Mass (kg)'].min(),       # Default min value
           spacex_df['Payload Mass (kg)'].max()]       # Default max value
)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
from dash.dependencies import Input, Output
import plotly.express as px

# Callback function to update scatter plot based on site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_plot(selected_site, payload_range):
    # Extract selected payload range
    low, high = payload_range
    
    # Filter data by payload range first
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                             (spacex_df['Payload Mass (kg)'] <= high)]
    
    # Further filter by launch site if a specific site is selected
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',                          # 0 = Failure, 1 = Success
        color='Booster Version Category',    # Color points by booster version
        title='Payload vs Success Scatter Plot',
        hover_data=['Launch Site', 'Payload Mass (kg)']
    )
    
    return fig

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
