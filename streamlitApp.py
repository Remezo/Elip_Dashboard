import os
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sqlalchemy import create_engine
from io import BytesIO


def get_db_connection_string():
    user = os.environ.get("POSTGRES_USER", "ascentris")
    password = os.environ.get("POSTGRES_PASSWORD", "Ascentris2023")
    host = os.environ.get("POSTGRES_HOST", "postgres")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "ascentris_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


@st.cache_data(ttl=24 * 60 * 60)
def retrieveData():
    base_dir = os.environ.get("APP_BASE_DIR", os.path.dirname(os.path.abspath(__file__)))
    df3 = pd.read_csv(os.path.join(base_dir, "input", "DataSummary.csv"))

    db_connection_str = get_db_connection_string()
    db_connection = create_engine(db_connection_str, pool_pre_ping=True)

    processed_data_frames = {}
    fred_data_frames = {}

    processed_data_frames["Daily"] = pd.read_sql('SELECT * FROM "Daily"', con=db_connection)
    processed_data_frames["Monthly"] = pd.read_sql('SELECT * FROM "Monthly"', con=db_connection)
    processed_data_frames["Quarterly"] = pd.read_sql('SELECT * FROM "Quarterly"', con=db_connection)

    fred_data_frames["Daily"] = (
        pd.read_sql('SELECT * FROM "raw_Daily"', con=db_connection)
        .dropna(thresh=4)
        .replace(".", 0)
    )
    # Drop 'Unnamed: 0' only if it exists
    if "Unnamed: 0" in fred_data_frames["Daily"].columns:
        fred_data_frames["Daily"] = fred_data_frames["Daily"].drop("Unnamed: 0", axis=1)

    fred_data_frames["Monthly"] = (
        pd.read_sql('SELECT * FROM "raw_Monthly"', con=db_connection)
        .dropna(thresh=15)
        .replace(".", 0)
    )
    if "Unnamed: 0" in fred_data_frames["Monthly"].columns:
        fred_data_frames["Monthly"] = fred_data_frames["Monthly"].drop("Unnamed: 0", axis=1)

    fred_data_frames["Quarterly"] = (
        pd.read_sql('SELECT * FROM "raw_Quarterly"', con=db_connection)
        .dropna(thresh=16)
        .replace(".", 0)
    )
    if "Unnamed: 0" in fred_data_frames["Quarterly"].columns:
        fred_data_frames["Quarterly"] = fred_data_frames["Quarterly"].drop("Unnamed: 0", axis=1)

    CPI = pd.read_sql('SELECT * FROM "CPIWeightedChange"', con=db_connection)

    db_connection.dispose()
    return processed_data_frames, fred_data_frames, df3, CPI


def main():
    pages = [
        "CPI",
        "Signs of Excess",
        "Operating Fundamentals",
        "Yield Spreads",
        "Global Growth",
        "Download Data",
    ]

    processed_data_frames, fred_data_frames, df3, CPI = retrieveData()

    selected_page = st.sidebar.radio("Select a page", pages)

    if selected_page == "CPI":
        render_cpi_page(CPI, processed_data_frames)
    elif selected_page == "Signs of Excess":
        render_signs_of_excess_page(df3, processed_data_frames, fred_data_frames)
    elif selected_page == "Operating Fundamentals":
        render_operating_fundamentals_page(df3, processed_data_frames, fred_data_frames)
    elif selected_page == "Yield Spreads":
        render_yield_spreads_page(df3, processed_data_frames, fred_data_frames)
    elif selected_page == "Global Growth":
        render_global_growth_page(df3, processed_data_frames, fred_data_frames)
    elif selected_page == "Download Data":
        render_download_page(CPI, processed_data_frames)


@st.cache_data
def plot_graphs(filtered_df, processed_data_frames, fred_data_frames):
    for index, row in filtered_df.iterrows():
        data = row["Data"]
        frequency = row["Frequency"]
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        if frequency == "Daily" or frequency == "Monthly":
            fig.add_trace(
                go.Bar(
                    x=processed_data_frames["Monthly"]["Dates"],
                    y=processed_data_frames["Monthly"]["USREC"]
                    * processed_data_frames[frequency][data].max(),
                    name="US Recession",
                    marker=dict(color="rgba(250, 0, 0, 0.7)"),
                ),
                secondary_y=True,
            )
        elif frequency == "Quarterly":
            fig.add_trace(
                go.Bar(
                    x=processed_data_frames["Quarterly"]["Dates"],
                    y=processed_data_frames["Quarterly"]["USREC"]
                    * processed_data_frames[frequency][data].max(),
                    name="US Recession",
                    marker=dict(color="rgba(250, 0, 0, 0.7)"),
                ),
                secondary_y=True,
            )

        fig.add_trace(
            go.Scatter(
                x=fred_data_frames[frequency]["Dates"],
                y=fred_data_frames[frequency][data],
                name=f"{data}",
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=processed_data_frames[frequency]["Dates"],
                y=processed_data_frames[frequency][data],
                name=f"{row['Processing']}",
            ),
            secondary_y=True,
        )

        fig.update_layout(title_text=f"{row['Name']}")
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text=f"{row['Data']}", secondary_y=False)
        fig.update_yaxes(title_text=frequency, secondary_y=True)
        st.plotly_chart(fig)


def render_cpi_page(df, processed_data_frames):
    st.title("CPI Page")
    categories = df.columns[2:-1]

    bar_trace_data = []
    for i, category in enumerate(categories):
        bar_trace_data.append(go.Bar(x=df["Unnamed: 0"], y=df[category], name=category))

    line_trace = go.Scatter(
        x=df["Unnamed: 0"],
        y=df["All items"],
        name="All items",
        mode="lines+markers",
        line=dict(color="red"),
    )
    trace_data = bar_trace_data + [line_trace]
    layout = go.Layout(
        barmode="stack",
        title="CPI Components",
        xaxis=dict(title="Years"),
        yaxis=dict(title="Weighted CPI"),
    )
    fig = go.Figure(data=trace_data, layout=layout)

    for i, category in enumerate(categories):
        fig.add_trace(
            go.Scatter(x=[None], y=[None], mode="markers", showlegend=False, name=category)
        )
    st.plotly_chart(fig, height=800, width=800)


def render_signs_of_excess_page(df3, processed_data_frames, fred_data_frames):
    st.title("Signs of Excess Page")
    filtered_df = df3[df3["Sector"] == "Signs of Excess"]
    plot_graphs(filtered_df, processed_data_frames, fred_data_frames)


def render_operating_fundamentals_page(df3, processed_data_frames, fred_data_frames):
    st.title("Operating Fundamentals Page")
    filtered_df = df3[df3["Sector"] == "Operating Fundamentals"]
    plot_graphs(filtered_df, processed_data_frames, fred_data_frames)


def render_yield_spreads_page(df3, processed_data_frames, fred_data_frames):
    st.title("Yield Spreads Page")
    filtered_df = df3[df3["Sector"] == "Yield Spreads"]
    plot_graphs(filtered_df, processed_data_frames, fred_data_frames)


def render_global_growth_page(df3, processed_data_frames, fred_data_frames):
    st.title("Global Growth Page")
    filtered_df = df3[df3["Sector"] == "Global Growth"]
    plot_graphs(filtered_df, processed_data_frames, fred_data_frames)


def render_download_page(df, processed_data_frames):
    st.title("Download Page")
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="CPI_weighted")
        processed_data_frames["Daily"].to_excel(writer, index=False, sheet_name="Daily")
        processed_data_frames["Monthly"].to_excel(writer, index=False, sheet_name="Monthly")
        processed_data_frames["Quarterly"].to_excel(writer, index=False, sheet_name="Quarterly")

    excel_data.seek(0)
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="scraped_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    main()
    st.sidebar.markdown("# Project Description")
    st.sidebar.markdown("This is a Streamlit dashboard for analyzing financial data.")
