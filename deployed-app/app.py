import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import pymongo
from pymongo import MongoClient
from urllib import parse

# import sys
# sys.path.append('../')
# import extractToMongo

#HOW TO DEPLOY TO HEROKU
#in terminal:
#git add .
#git commit -m 'git message'
#git push heroku master

#HOW TO RUN LOCALLY
#py app.py


import warnings
from flask import Flask
import numpy as np

warnings.filterwarnings("ignore", message="numpy.dtype size changed")


app = dash.Dash(__name__)
server = app.server
app.css.append_css(
    {
        "external_url": (
            "https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75"
            "/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css"
        )
    }
)


#--------------------------------------------------------------------------------------------------------------------

#RETRIEVE ALL DATAFRAMES FROM MONGODB USING MONGOHQ
# MONGO_URL = os.environ.get('MONGOHQ_URL') 

# if MONGO_URL:
#     conn = MongoClient(MONGO_URL)
#     db = conn.app105426028
# else:
#     conn = MongoClient('localhost', 27017)  
#     db = conn['app105426028']


client = MongoClient('mongodb://erra:qwerty123@ds121312.mlab.com:21312/pdsca2victoria')
db = client.pdsca2victoria

collection1 = db.Compensation
collection2 = db.RateSalary
collection3 = db.Jobs
collection32 = db.Jobs2
collection4 = db.IT


df_RateSalary = pd.DataFrame(list(collection2.find()))

df = pd.DataFrame(list(collection1.find()))
df = df[df.level_2.str.contains("Utilities") == False]
df_Compensation = df[df.level_2.str.contains("Other Goods Industries") == False]

df_Jobs = pd.DataFrame(list(collection3.find()))
df_Jobs = df_Jobs[df_Jobs.quarter.str.contains("2018") == False]

df_Jobs2 = pd.DataFrame(list(collection32.find()))

df_IT = pd.DataFrame(list(collection4.find()))

#--------------------------------------------------------------------------------------------------------------------
# Dropdown Menu Values for Scatter
sortEmploymentRate = {
    "Overall Employment Rate": "employment_rate_overall",
    "Permanent Employment Rate": "employment_rate_permanent",
}
# Dropdown Menu Values for Bar
sortOccupations = {
    "Average Wages ($)": "avg_wage",
    "Number of People": "num_ppl",
}

sortSalary = {
    "Basic Mean Monthly Salary": "basic_monthly_mean",
    "Basic Median Monthly Salary": "basic_monthly_median",
    "Gross Mean Monthly Salary": "gross_monthly_mean",
    "Gross Median Monthly Salary": "gross_monthly_median",
    "Gross 25th Percentile Monthly Salary": "gross_mthly_25_percentile",
    "Gross 75th Percentile Monthly Salary": "gross_mthly_75_percentile",
}
# Map industry to colours
colorsIdx = {
    "Business": "rgb(90,151,194)",
    "Engineering": "rgb(246,157,78)",
    "Humanities & Social Sciences": "rgb(99,180,99)",
    "Sciences": "rgb(218,95,96)",
    "Education": "rgb(172,140,200)",
    "Computing & Information Technology": "rgb(84,201,213)",
    "Medicine": "rgb(227,151,204)",
    "Design": "rgb(157,157,157)",
    "Law": "rgb(199,200,92)",
    "Others": "rgb(166,128,121)",
    "Accountancy": "rgb(218,124,48)",
    "Economics": "rgb(57,106,177)",
}
colorsIdx2 = {
    "manufacturing": "rgb(90,151,194)",
    "construction": "rgb(246,157,78)",
    "services": "rgb(218,95,96)",
    "others": "rgb(84,201,213)",
}

cols = df_RateSalary["school"].map(colorsIdx)



# Text Style
text_style = dict(
    color="#FFFFFF", fontFamily="sans-serif", fontWeight=300, horizontalAlign="middle"
)

#--------------------------------------------------------------------------------------------------------------------

# PLOT LINECHART 
def display_linechart(df):
        return dcc.Graph(
        id='line-compensation',
        animate=True,
        figure={
            'data': [
                
                    go.Scatter(
                        y=list(df[df['level_2'] == i]['value']),
                        x=list(df[df['level_2'] == i]['year']),
                        text=list(df[df['level_2'] == i]['value']),
                        mode='lines',
                        name=i
                        
                ) for i in df.level_2.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Year'},
                yaxis={'title': 'Annual Salary($)'},
                margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
                legend=dict(
                x=1,
                y=1,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="#000"),
                bgcolor="#FAFAFA",
                bordercolor="#FFFFFF",
                borderwidth=2,
                
            ),
                hovermode='closest'
            )
        }
    )


#--------------------------------------------------------------------------------------------------------------------
# LAYOUT OF APP----------------------------------------------------------
app.layout = html.Div(
    [
        # INTRODUCTION----------------------------------------------------------
        html.Div(
            [
                 html.Div(
                    [
                        html.H1(style={'color':'white'},
                            children="Choose Your Future Industry"
                        ),
                        html.P("Having trouble figuring out what course in University to take after graduating from your diploma in Information Technology?"),
                        html.P("Thinking of switching to a different industry field, and unsure whether you should continue on in IT?"),
                        html.P("Choose Your Future Industry is a project dedicated to helping you figure out what you wanna do in the future!"),
                        
                    ],
                            style={
                                "maxWidth": "70%",
                            "text-align": "center",
                            "horizontal-align": "middle",
                            "padding-bottom": "120px",
                            "padding-top": "120px",
                            "padding-left": "550px",
                            "padding-right": "550px",
                            "borderTop": "thin white solid"
                            },
                ),

            ],
            style={
                # https://png.pngtree.com/thumb_back/fw800/back_pic/05/06/81/77597064f5b9eb0.jpg
                # https://images.fatguymedia.com/wp-content/uploads/2013/06/background-JOBS.jpg
                # http://backgrounds-desktop.com/uploads/posts/2017-08/1_life_choices.jpg
                "background-image": "url(http://i.imgur.com/mb1nAsU.gif)",
                "color": "#FFFFFF"
            },
        ),

        #GREY TITLE EMPLOYMENT RATE VS MONTHLY SALARY----------------------------------------------------------
        
        html.Div(
            [
                html.Div([
                html.Div(
                    [
                        html.H1(
                            children="Employment Rate & Mean Monthly Salary"
                        ),
                        html.Div([
                        html.P("Click dropdown to select Salary and Employment Rate:"),
                        ], style={"margin": "10px 5px"})
                    ],
                            style={
                                "margin-top":"10px"
                            },
                ),
                # DROPDOWN SCATTERPLOT----------------------------------------------------------
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="xaxis-column",
                                    options=[
                                        {"label": label, "value": value}
                                        for label, value in sortSalary.items()
                                    ],
                                    value="gross_monthly_mean",
                                )
                            ],
                            style={
                                "width": "38%",
                                "float": "left",
                                "display": "inline-block",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="yaxis-column",
                                    options=[
                                        {"label": label, "value": value}
                                        for label, value in sortEmploymentRate.items()
                                    ],
                                    value="employment_rate_overall",
                                )
                            ],
                            style={"width": "38%", "display": "inline-block"},
                        ),
                    ]
                ),
                ],  
                    style={
                        "padding": "10px 0px",
                        "width": "90%",
                        "float": "right",
                    },
                ), 
            ],
            style={
                "width": "100%",
                "float": "right",
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "25px 30px",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),
        html.Br(),
        # PLOT SCATTERPLOT----------------------------------------------------------
        html.Div(
            [
                # html.P("Scatterplot of Mean Monthly Salary against Employment Rate"),
                # Plot Scatter
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="graph-with-slider", animate=True)],
                            style={
                                "width": "80%",
                                "display": "inline-block",
                                "float": "left",
                            },
                        ),
                        # DESC SCATTERPLOT----------------------------------------------------------
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
    ***
    ## Job Stability?
    Does your Salary have anything to do with the Employment Rate? 
    
    In other words, will your salary change with the fluctuations in demand for your industry?
    
    Let's find out.

    [Dataset](https://data.gov.sg/dataset/graduate-employment-survey-ntu-nus-sit-smu-sutd)
    """.replace(
                                        "  ", ""
                                    ),
                                    className="container",
                                    containerProps={
                                        "style": {
                                            "maxWidth": "70%",
                                            "vertical-align": "middle",
                                            "horizontal-align": "middle",
                                            # "horizontal-align": "middle",
                                            # "padding-bottom": "120px",
                                            "padding-top": "10%",
                                            "padding-left": "2%",
                                            "padding-right": "2%",
                                        }
                                    },
                                )
                            ],
                            style={
                                "display": "inline-block",
                                "float": "right",
                                "width": "10%",
                                "padding-left": "5%",
                                "padding-right": "5%",
                            },
                        ),
                    ]
                )
            ],
            style={
                "borderBottom": "thin lightgrey solid",
                "margin-bottom": "20px",
                "padding-bottom": "50px",
                "padding-top":"10px",
                "padding-left": "5px",
                "padding-right": "5px",
                "width": "90%",
                "float": "right",
                "display": "inline-block",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),  # END SCATTER
        # SLIDER YEAR FOR SCATTER & BOXPLOT----------------------------------------------------------
        html.Div(
            [
                dcc.Slider(
                    id="year-slider",
                    min=df_RateSalary["year"].min(),
                    max=df_RateSalary["year"].max(),
                    value=df_RateSalary["year"].median(),
                    step=None,
                    vertical=True,
                    marks={
                        str(year): str(year) for year in df_RateSalary["year"].unique()
                    },
                )
            ],
            style={
                "display": "inline-block",
                "float": "left",
                "height": "650px",
                "margin-top": "10%",
                "margin-left": "5%",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),
        # PLOT BOXPLOT----------------------------------------------------------
        html.Div(
            [
                # html.P("Boxplot of Monthly Salaries for each Industry"),
                html.Div(
                    [dcc.Graph(id="boxplot-spread-of-wages")],
                    style={
                        "width": "65%",
                        "margin-bottom": "50px",
                        "padding": "80px 0px",
                        "display": "inline-block",
                        "color":"#444", "font-family":"sans-serif", "font-weight":"300", 
                        "horizontal-align":"middle"
                    },
                ),
                # DESC BOXPLOT----------------------------------------------------------
                html.Div(
                    [
                        dcc.Markdown(
                            """
    ***
    ## What's Your Projected Salary Range?
    Find out the range of monthly wages for jobs in each industry, from the lowest to the most common, and the upper quartile.
    
    Compare the industries, and consider how much you'll be aiming to earn.
    

    [Dataset](https://data.gov.sg/dataset/graduate-employment-survey-ntu-nus-sit-smu-sutd)
    """.replace(
                                "  ", ""
                            ),
                            className="container",
                            containerProps={
                                "style": {
                                    "maxWidth": "90%",
                                    "horizontal-align": "middle",
                                    # "horizontal-align": "middle",
                                    # "padding-bottom": "120px",
                                    "padding-top": "0px",
                                    "padding-left": "2%",
                                    "padding-right": "2%",
                                    "padding-bottom":"10px"
                                }
                            },
                        )
                    ],
                    style={
                        "display": "inline-block",
                        "float": "left",
                        "width": "15%",
                        "padding-left": "5%",
                        "padding-right": "3%",
                    },
                ),
            ],
            style={
                "margin-bottom": "0px",
                "vertical-align":"middle",
                "padding": "10px 0px",
                "width": "90%",
                "float": "right",
                "display": "inline-block",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),
        
        #GREY TITLE SALARY GROWTH----------------------------------------------------------
        html.Div(
            [
                html.Div([
                html.Div(
                    [
                        html.H1(
                            children="Salary Growth Projections"
                        ),
                        html.P("Annual Compensation By Industry from 1980 to 2016"),
                        
                    ],
                            style={
                                "margin-top":"10px"
                            },
                ),
               
                ],  
                    style={
                        "padding": "10px 0px",
                        "width": "90%",
                        "float": "right",
                    },
                ), 
            ],
            style={
                "width": "100%",
                "float": "right",
                "borderTop": "thin lightgrey solid",
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "25px 30px",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),

        html.Div([
                html.Div(
                    [
                          # DESC LINECHART----------------------------------------------------------
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
    ***
    ## Will Your Salary Grow?
    View how annual compensations for jobs vary by industry;
    
    and how each industry's employee compensation has grown, and is expected to grow with time.
    

    [Dataset](https://data.gov.sg/dataset/compensation-of-employees-by-industry-at-current-prices-annual?resource_id=442c08cb-4765-4082-ab31-2302bc3ba2aa)
    """.replace(
                                        "  ", ""
                                    ),
                                    className="container",
                                    containerProps={
                                        "style": {
                                            "maxWidth": "80%",
                                            "vertical-align": "middle",
                                            "horizontal-align": "middle",
                                            # "horizontal-align": "middle",
                                            # "padding-bottom": "120px",
                                            "padding-top": "15%",
                                            "padding-bottom": "8%",
                                            "padding-left": "2%",
                                            "padding-right": "2%",
                                        }
                                    },
                                )
                            ],
                            style={
                                "display": "inline-block",
                                "float": "right",
                                "width": "10%",
                                "padding-bottom": "30px",
                                "padding-left": "5%",
                                "padding-right": "5%",
                                "color":"#444", "font-family":"sans-serif", "font-weight":"300", 
                                "horizontal-align":"middle"
                            },
                        ),
            # PLOT LINECHART----------------------------------------------------------
                        html.Div(
                            [display_linechart(df_Compensation)],
                            style={
                                "margin-top":"50px",
                                "margin-bottom":"50px",
                                "width": "70%",
                                "display": "inline-block",
                                "float": "right",
                                "padding": "20px 0px"
                                
                            },
                        ),
           
        ])
        ], style=text_style),

        
        #GREY TITLE JOB VACANCIES----------------------------------------------------------
        html.Div(
            [
                html.Div([
                html.Div(
                    [
                        html.H1(
                            children="Job Vacancies"
                        ),
                        html.P("Distribution of Job Vacancies By Industry from the year 1990 to 2018. Hover over histogram bars to view more on the job vacancies in the form of a line chart."),
                        
                    ],
                            style={
                                "margin-top":"10px",
                                "margin-bottom":"20px"
                            },
                ),
               
                # SLIDER YEAR HISTOGRAM----------------------------------------------------------(hidden)
        html.Div(
            [
                dcc.Slider(
                    id="year-slider2",
                    min=df_Jobs["quarter"].min(),
                    max=df_Jobs["quarter"].max(),
                    value=df_Jobs["quarter"].max(),
                    step=None,
                    marks={
                        str(year): str(year) for year in df_Jobs["quarter"].unique()
                    },
                )
            ],
            style={
                "margin-top":"2%",
                "width": "80%",
                "margin-top": "0%",
                "margin-left": "5%",
                "display":"none"
            },
        ),
                ],  
                    style={
                        "padding": "10px 0px",
                        "width": "90%",
                        "float": "right",
                    },
                ), 
            ],
            style={
                "width": "100%",
                "float": "right",
                "borderTop": "thin lightgrey solid",
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "25px 30px",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),



      # DESC HISTOGRAM & LINECHART ----------------------------------------------------------
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
    ***
    ## How has your industry's job vacancies changed?
    Is there a little bit of variability in your industry's job vacancies throughout the years, or a lot?
    

    What's the range of job vacancies available? Find out the spread of data here.


    [Dataset](https://data.gov.sg/dataset/job-vacancy-by-industry-and-occupational-group-quarterly?view_id=fb49ef65-e863-435f-afe7-621393328e57&resource_id=f8134bbb-c36f-4422-83a1-677b0e17e592)
    """.replace(
                                        "  ", ""
                                    ),
                                    className="container",
                                    containerProps={
                                        "style": {
                                            "maxWidth": "80%",
                                            "vertical-align": "middle",
                                            "horizontal-align": "middle",
                                            # "horizontal-align": "middle",
                                            # "padding-bottom": "120px",
                                            "padding-top": "15%",
                                            "padding-bottom": "8%",
                                            "padding-left": "2%",
                                            "padding-right": "2%",
                                        }
                                    },
                                )
                            ],
                            style={
                                "display": "inline-block",
                                "float": "left",
                                "width": "10%",
                                "padding-bottom": "30px",
                                "padding-left": "7%",
                                "padding-right": "3%",
                                "color":"#444", "font-family":"sans-serif", "font-weight":"300", 
                                "horizontal-align":"middle"
                            },
                        ),


                         # PLOT HISTOGRAM----------------------------------------------------------
                         html.Div([
                    html.Div(
                    [dcc.Graph(id="histogram-job-vacancies", 
                    hoverData={'points': [{'customdata': 'services'}]
                    }
                    )],
                    style={
                        "width": "100%",
                        "padding": "20px 0px",
                        "horizontal-align":"middle"
                    },
                ),
                # PLOT LINECHART----------------------------------------------------------
                 html.Div([
           html.Div([                 
        dcc.Graph(id='line-jobs',
        animate=False,
        )
        ])
    
        ], style={ 'width': '100%'},
        )
    

    ], style={'display': 'inline-block', 
                         "float": "left", 
                        "margin-bottom": "50px",
                        "margin-left":"5%",
                        'width': '70%'}),


        #GREY TITLE IT CHOICES----------------------------------------------------------
        html.Div(
            [
                html.Div([
                html.Div(
                    [
                        html.H1(
                            children="Employment In The Information Technology Industry"
                        ),
                        html.P("Say you decide to continue your studies in Information Technology, what jobs and salaries does it have to offer you, and what are the highest paying ones? The closest comparable data for the Information Technology Course is from the Computer and Information Sciences and Support Services Course in 2016. "),
                         html.Div([
                             html.P("Sort Occupations by:"),
                         ], style={ "margin":"10px 0px"})
                        
                    ],
                            style={
                                "margin-top":"10px"
                            },
                ),
                  html.Div(
                            [
                                dcc.Dropdown(
                                    id="occupation-column",
                                    options=[
                                        {"label": label, "value": value}
                                        for label, value in sortOccupations.items()
                                    ],
                                    value="avg_wage",
                                )
                            ],
                            style={
                                'padding-top':'5px',
                                "width": "38%",
                                "float": "left"
                            },
                        ),
                ],  
                    style={
                        "padding": "10px 0px",
                        "width": "90%",
                        "float": "right",
                    },
                ), 
            ],
            style={
                "width": "100%",
                "float": "right",
                "borderTop": "thin lightgrey solid",
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "25px 30px",
                "color":"#444", "font-family":"sans-serif", "font-weight":"300", "horizontal-align":"middle"
            },
        ),

    #PLOT BAR CHART----------------------------------------------------------

        html.Div([
         html.Div([
           html.Div([                 
        dcc.Graph(id='barchart-it-top'
        )
        ])
    
        ], style={ 'width': '40%',
        'margin-left':"8%",
        'margin-top':"60px",
        'margin-bottom':"60px",
        'padding':'20px 10px',
                "float": "left", 
                "display":"inline-block"},
        ),
        html.Div([
           html.Div([                 
        dcc.Graph(id='barchart-it-bottom'
        )
        ])
    
        ], style={ 'width': '40%',
        'margin-right':"8%",
        'margin-top':"60px",
        'margin-bottom':"60px",
        'padding':'20px 10px',
                "float": "right", 
                "display":"inline-block"},
        )
    ], style={ 'width': '100%'}),
    html.Div([
         html.Div(
                            [
                                dcc.Markdown(
                                    """
    [Dataset](https://datausa.io/profile/cip/110103/#locationshttps://datausa.io/profile/cip/110103/#locations)
    """.replace(
                                        "  ", ""
                                    ),
                                    className="container",
                                    containerProps={
                                        "style": {
                                            "maxWidth": "80%",
                                            "horizontal-align": "right"
                                        }
                                    },
                                )
                            ],
                            style={
                                "float": "right",
                                "width": "100%",
                                "padding-bottom": "30px",
                                "color":"#444", 
                                "font-family":"sans-serif", 
                                "font-weight":"300", 
                                "horizontal-align":"right"
                            },
                        ),
    ])

    ],  # END APP LAYOUT----------------------------------------------------------
    style = text_style
)


#--------------------------------------------------------------------------------------------------------------------


# SCATTER CALLBACK
@app.callback(
    dash.dependencies.Output("graph-with-slider", "figure"),
    [dash.dependencies.Input("xaxis-column", "value"),
        dash.dependencies.Input("yaxis-column", "value"),
        dash.dependencies.Input("year-slider", "value"),
    ],
)
def update_figure(selected_xaxis, selected_yaxis, selected_year):
    filtered_df = df_RateSalary[df_RateSalary.year == selected_year]
    traces = []
    for i in filtered_df.school.unique():
        df_by_school = filtered_df[filtered_df["school"] == i]
        traces.append(
            go.Scatter(
                x=df_by_school[selected_yaxis],
                y=df_by_school[selected_xaxis],
                text=df_by_school["degree"],
                mode="markers",
                opacity=0.999,
                marker=dict(size=10, line={"width": 0.5, "color": "white"}),
                name=i,
            )
        )

    return {
        "data": traces,
        "layout": go.Layout(
            xaxis={"type": "log", "title": "Employment Rate (%)"},
            yaxis={"title": "Monthly Salary ($)"},
            margin={"l": 80, "b": 50, "t": 40, "r": 80},
            legend=dict(
                x=1,
                y=1,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="#000"),
                bgcolor="#FAFAFA",
                bordercolor="#FFFFFF",
                borderwidth=2,
            ),
            hovermode="closest",
        ),
    }


#--------------------------------------------------------------------------------------------------------------------

# BOXPLOT CALLBACK
@app.callback(
    dash.dependencies.Output("boxplot-spread-of-wages", "figure"),
    [dash.dependencies.Input("year-slider", "value")],
)
def update_box(selected_year):
    filtered_df = df_RateSalary[df_RateSalary.year == selected_year]
    traces = []
    for i in filtered_df.school.unique():
        df_by_school = filtered_df[filtered_df["school"] == i]
        all_pay = []
        all_pay.extend(list(df_by_school["basic_monthly_mean"].values))
        all_pay.extend(list(df_by_school["basic_monthly_median"].values))
        all_pay.extend(list(df_by_school["gross_monthly_mean"].values))
        all_pay.extend(list(df_by_school["gross_monthly_median"].values))
        all_pay.extend(list(df_by_school["gross_mthly_25_percentile"].values))
        all_pay.extend(list(df_by_school["gross_mthly_75_percentile"].values))

        traces.append(
            {
                "y": all_pay,
                "name": i,
                "type": "box"
            }
        )

    return {
        "data": traces,
        "layout": go.Layout(
            # title= "Box Plot",
            margin={"l": 80, "b": 130, "t": 40, "r": 80},
            yaxis={"title": "Monthly Salary ($)"},
            hovermode="closest", 
            legend=dict(
                x=1,
                y=1,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="#000"),
                bgcolor="#FAFAFA",
                bordercolor="#FFFFFF",
                borderwidth=2,
            ),
        ),
    }

#--------------------------------------------------------------------------------------------------------------------


# HISTOGRAM CALLBACK
@app.callback(
    dash.dependencies.Output("histogram-job-vacancies", "figure"),
    [dash.dependencies.Input("year-slider2", "value")],
)
def update_histogram(selected_year):
    filtered_df = df_Jobs
    traces = []
    for i in filtered_df.industry1.unique():
        df_by_occupation = filtered_df[filtered_df["industry1"] == i]
        traces.append(
                    go.Histogram(
                    x = np.array(df_by_occupation["job_vacancy"]),
                    name = i,
                    xbins=dict(
                        start=0,
                        end=9000,
                        size=500
                    ),
                    marker = dict(
            	    color = (colorsIdx2[i])
                    ),
                     opacity=0.85,
                    customdata=df_by_occupation['industry1']
                )
            
        )

    return {
        "data": traces,
        "layout": go.Layout(
            margin={"l": 80, "b": 130, "t": 40, "r": 80},
            xaxis=dict(
        title='Job Vacancies'
    ),
            yaxis={"title": "Frequency"},
            hovermode="closest", 
            legend=dict(
                x=1,
                y=1,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="#000"),
                bgcolor="#FAFAFA",
                bordercolor="#FFFFFF",
                borderwidth=2,
            ),
            
            bargap=0.2,
            bargroupgap=0.1
        ),
    }

#--------------------------------------------------------------------------------------------------------------------

# LINE CALLBACK
@app.callback(
    dash.dependencies.Output("line-jobs", "figure"),
    [
        dash.dependencies.Input("histogram-job-vacancies", "hoverData")
    ],
)
def update_figure(hoverData):
    industry = hoverData['points'][0]['customdata']
    traces = []
    df_by_industry = df_Jobs2[df_Jobs2["industry1"] == industry]
    df_by_industry = df_by_industry.groupby('quarter', as_index=False)['job_vacancy'].mean()

    traces.append(
            go.Scatter(
                y=list(df_by_industry['job_vacancy']),
                x= list(df_by_industry['quarter']),
                mode="lines",
                opacity=0.999,
                line = dict(
            	    color = (colorsIdx2[industry])
                ),
                marker=dict(size=10, line={"width": 0.5, "color": "white"}),
                name=industry,
            )
        )

    return {
        "data": traces,
        "layout": go.Layout(
            yaxis={"title": "Job Vacancies"},
            xaxis=dict(
                title = "Year Quarter",
                autorange = True
            ),
            margin={"l": 80, "b": 150, "t": 40, "r": 80},
            legend=dict(
                x=1,
                y=1,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="#000"),
                bgcolor="#FAFAFA",
                bordercolor="#FFFFFF",
                borderwidth=2,
            ),
            hovermode="closest",
        ),
    }


#--------------------------------------------------------------------------------------------------------------------
    


# BARCHART TOP CALLBACK
@app.callback(
    dash.dependencies.Output("barchart-it-top", "figure"),
    [dash.dependencies.Input("occupation-column", "value")],
)
def update_barchart(value):

    if value == "avg_wage":
        label = 'Highest Wages ($)'
    elif value == "num_ppl":
        label= 'Most Common (Pax)'

    filtered_df = (df_IT.sort_values(value, ascending=False)).head(25)
    x_job_labels = list(filtered_df['soc_name'])
    y_job_values = list(filtered_df[value])
    traces = []
    col = []
    a = 1.0
    for i in np.arange(0,25):
        col.append('rgba(50, 171, 96, ' + str(a) + ')')
        a -= 0.02

    traces.append({
                    'y' : x_job_labels,
                    'x' : y_job_values,
                    'orientation':'h',
                    "type" : "bar",
                    'marker': dict(
                        color= col,
                        line=dict(
                        color='rgba(50, 171, 96, 1.0)',
                        width = 1),
    ),
     
           } 
        )
    return {
        "data": traces,
        "layout": go.Layout(
             margin={"l": 50, "b": 80, "t": 40, "r": 390},
            xaxis=dict(
                title=label,
                titlefont=dict(
                    size=24
                )
            ),
            yaxis=dict(
                autorange='reversed',
                side='right'
            ),
            hovermode="closest", 
            
        ),
    }




#--------------------------------------------------------------------------------------------------------------------


# BARCHART BOTTOM CALLBACK
@app.callback(
    dash.dependencies.Output("barchart-it-bottom", "figure"),
    [dash.dependencies.Input("occupation-column", "value")],
)
def update_barchart(value):

    if value == "avg_wage":
        label = 'Lowest Wages ($)'
    elif value == "num_ppl":
        label= 'Least Common (Pax)'

    filtered_df = (df_IT.sort_values(value, ascending=False)).tail(20)
    x_job_labels = list(filtered_df['soc_name'])
    y_job_values = list(filtered_df[value])
    traces = []
    col = []
    a = 0.95
    for i in np.arange(0,25):
        col.append('rgba(222,45,38, ' + str(a) + ')')
        a -= 0.02

    traces.append({
                    'y' : x_job_labels,
                    'x' : y_job_values,
                    'orientation':'h',
                    "type" : "bar",
                    'marker': dict(
                        color= col,
                        line=dict(
                        color='rgba(222,45,38, 0.9)',
                        width = 1),
    ),
     
           } 
        )
    return {
        "data": traces,
        "layout": go.Layout(
             margin={"l": 50, "b": 80, "t": 40, "r": 390},
            xaxis=dict(
                title=label,
                titlefont=dict(
                    size=24
                )
            ),
            yaxis=dict(
                autorange='reversed',
                side='right'
            ),
            hovermode="closest", 
            
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True)
