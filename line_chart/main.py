import json
from pathlib import Path

import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_FILE = Path(__file__).with_name("data.json")


# --------------------------------------------------
# Load and validate data
# --------------------------------------------------

def load_data(filename: Path) -> dict:
    """Load and validate line chart data from a JSON file."""

    if not filename.exists():
        raise FileNotFoundError(
            f"Data file not found: {filename}"
        )

    with filename.open("r", encoding="utf-8") as file:
        chart_data = json.load(file)

    if "data" not in chart_data:
        raise ValueError(
            "The JSON file must contain a 'data' property."
        )

    if not chart_data["data"]:
        raise ValueError(
            "The 'data' array cannot be empty."
        )

    required_fields = {
        "month",
        "visits"
    }

    for item in chart_data["data"]:

        if not required_fields.issubset(item):
            raise ValueError(
                "Each observation must contain "
                "'month' and 'visits'."
            )

        if not isinstance(item["visits"], (int, float)):
            raise ValueError(
                "'visits' must contain numeric values."
            )

    return chart_data


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

def prepare_data(chart_data: dict) -> pd.DataFrame:
    """Convert JSON data to a DataFrame and prepare dates."""

    df = pd.DataFrame(
        chart_data["data"]
    )

    # Convert month strings into real dates.
    df["month"] = pd.to_datetime(
        df["month"],
        format="%Y-%m"
    )

    # A line chart represents an ordered sequence,
    # so ensure that the observations are chronological.
    df = df.sort_values(
        "month"
    )

    return df


# --------------------------------------------------
# Create chart
# --------------------------------------------------

def create_chart(chart_data: dict) -> None:
    """Create and display the line chart."""

    df = prepare_data(
        chart_data
    )

    # Get title information.
    title = chart_data.get(
        "title",
        "Line Chart"
    )

    subtitle = chart_data.get(
        "subtitle",
        ""
    )

    if subtitle:
        full_title = (
            f"{title}"
            f"<br><sup>{subtitle}</sup>"
        )
    else:
        full_title = title

    # --------------------------------------------------
    # Create Plotly figure
    # --------------------------------------------------

    fig = px.line(
        df,
        x="month",
        y="visits",
        markers=True,
        title=full_title,
        labels={
            "month": chart_data.get(
                "x_label",
                "Month"
            ),
            "visits": chart_data.get(
                "y_label",
                "Visits"
            )
        }
    )

    # --------------------------------------------------
    # Improve line appearance and interaction
    # --------------------------------------------------

    fig.update_traces(
        line={
            "width": 3
        },
        marker={
            "size": 8
        },
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Visits: %{y:,}"
            "<extra></extra>"
        )
    )

    # --------------------------------------------------
    # General layout
    # --------------------------------------------------

    fig.update_layout(
        template="plotly_white",

        title={
            "x": 0.02,
            "xanchor": "left"
        },

        font={
            "family": "Arial",
            "size": 14
        },

        margin={
            "l": 80,
            "r": 40,
            "t": 100,
            "b": 80
        },

        showlegend=False,

        hovermode="x unified",

        hoverlabel={
            "font_size": 14
        }
    )

    # --------------------------------------------------
    # X-axis
    # --------------------------------------------------

    fig.update_xaxes(
        title=chart_data.get(
            "x_label",
            "Month"
        ),

        tickformat="%b",

        dtick="M1",

        showgrid=False,

        title_standoff=15
    )

    # --------------------------------------------------
    # Y-axis
    # --------------------------------------------------

    fig.update_yaxes(
        title=chart_data.get(
            "y_label",
            "Visits"
        ),

        tickformat=",",

        showgrid=True,

        gridwidth=1,

        zeroline=False,

        title_standoff=15
    )

    # Display chart.
    fig.show()


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main() -> None:
    """Main program entry point."""

    try:

        chart_data = load_data(
            DATA_FILE
        )

        create_chart(
            chart_data
        )

    except FileNotFoundError as error:
        print(
            f"File error: {error}"
        )

    except json.JSONDecodeError as error:
        print(
            f"JSON error: {error}"
        )

    except ValueError as error:
        print(
            f"Data error: {error}"
        )

    except Exception as error:
        print(
            f"Unexpected error: {error}"
        )


if __name__ == "__main__":
    main()