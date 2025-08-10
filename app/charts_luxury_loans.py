import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dash import Dash, dcc, html

# COnnect to Postgresql
engine = create_engine(
    "postgresql+psycopg2://user:password@postgres_db:5432/mydb"
)

# Load Data from postgresql
df = pd.read_sql("SELECT * FROM luxury_loan_portfolio", engine)
df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
df["funded_date"] = pd.to_datetime(df["funded_date"], errors="coerce")

theme_colors = {
    "bg": "#1f2c56",
    "card": "#243763",
    "text": "#f5f6fa",
    "accent": "#17a2b8"
}

# Average Interest Rate by Loan Purpose
avg_interest = df.groupby("purpose")["interest_rate_percent"].mean().reset_index()

fig1 = px.bar(
    avg_interest,
    x="interest_rate_percent",
    y="purpose",
    orientation="h",
    title="Average Interest Rate by Loan Purpose",
    labels={"interest_rate_percent": "Interest Rate (%)", "purpose": "Loan Purpose"},
    text=avg_interest["interest_rate_percent"].round(2).astype(str) + "%"
)
fig1.update_traces(
    textposition="outside",
    marker_color=theme_colors["accent"]
)
fig1.update_layout(
    plot_bgcolor=theme_colors["card"],
    paper_bgcolor=theme_colors["card"],
    font=dict(color=theme_colors["text"]),
    yaxis={'categoryorder': 'total ascending'}
)

# Donu Chart Total Funded Amount by Loan Purpose
funded_by_purpose = df.groupby("purpose")["funded_amount"].sum().reset_index()

fig2 = px.pie(
    funded_by_purpose,
    values="funded_amount",
    names="purpose",
    hole=0.45,
    title="Total Funded Amount by Loan Purpose",
    color_discrete_sequence=px.colors.sequential.Blues[::-1]
)
fig2.update_traces(
    textinfo="percent+label",
    pull=[0.05]*len(funded_by_purpose)
)
fig2.update_layout(
    plot_bgcolor=theme_colors["card"],
    paper_bgcolor=theme_colors["card"],
    font=dict(color=theme_colors["text"])
)

# Line Chart Total Funded Amount per Year
funded_per_year = df.groupby(df["funded_date"].dt.year)["funded_amount"].sum().reset_index()
funded_per_year.columns = ["year", "funded_amount"]

fig3 = px.line(
    funded_per_year,
    x="year",
    y="funded_amount",
    markers=True,
    title="Total Funded Amount per Year",
    labels={"funded_amount": "Total Funded Amount", "year": "Year"},
    text=funded_per_year["funded_amount"].apply(lambda x: f"{x:,.0f}"),
    color_discrete_sequence=[theme_colors["accent"]]
)
fig3.update_traces(textposition="top center")
fig3.update_layout(
    plot_bgcolor=theme_colors["card"],
    paper_bgcolor=theme_colors["card"],
    font=dict(color=theme_colors["text"])
)

# Dash App
app = Dash(__name__)
app.title = "Luxury Loan Dashboard"

app.layout = html.Div(
    style={"backgroundColor": theme_colors["bg"], "padding": "20px"},
    children=[
        html.H1(
            "Luxury Loan Portfolio Dashboard",
            style={"textAlign": "center", "color": theme_colors["text"]}
        ),

        html.Div([
            dcc.Graph(figure=fig1, config={"displayModeBar": False})
        ], style={"marginBottom": "30px"}),

        html.Div([
            dcc.Graph(figure=fig2, config={"displayModeBar": False})
        ], style={"marginBottom": "30px"}),

        html.Div([
            dcc.Graph(figure=fig3, config={"displayModeBar": False})
        ])
    ]
)

# Run Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)