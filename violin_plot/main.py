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
    """Load and validate violin plot data."""

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

    for item in chart_data["data"]:

        if "group" not in item:
            raise ValueError(
                "Each item must contain a 'group' property."
            )

        if "scores" not in item:
            raise ValueError(
                "Each item must contain a 'scores' property."
            )

        if not item["scores"]:
            raise ValueError(
                f"Group '{item['group']}' has no scores."
            )

        if not all(
            isinstance(value, (int, float))
            for value in item["scores"]
        ):
            raise ValueError(
                f"All scores in '{item['group']}' "
                "must be numeric."
            )

    return chart_data


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

def prepare_data(chart_data: dict) -> pd.DataFrame:
    """
    Convert the grouped JSON structure into
    a tabular DataFrame.
    """

    rows = []

    for item in chart_data["data"]:

        group = item["group"]

        for score in item["scores"]:

            rows.append(
                {
                    "group": group,
                    "score": score
                }
            )

    return pd.DataFrame(rows)


# --------------------------------------------------
# Create chart
# --------------------------------------------------

def create_chart(chart_data: dict) -> None:
    """Create and display the violin plot."""

    df = prepare_data(
        chart_data
    )

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    title = chart_data.get(
        "title",
        "Violin Plot"
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

    x_label = chart_data.get(
        "x_label",
        "Group"
    )

    y_label = chart_data.get(
        "y_label",
        "Value"
    )

    # --------------------------------------------------
    # Create violin plot
    # --------------------------------------------------

    fig = px.violin(
        df,
        x="group",
        y="score",

        # Show a box plot inside each violin.
        box=True,

        # Show individual observations.
        points="all",

        title=full_title,

        labels={
            "group": x_label,
            "score": y_label
        }
    )

    # --------------------------------------------------
    # Improve appearance
    # --------------------------------------------------

    fig.update_traces(
        meanline_visible=True,

        points="all",

        jitter=0.15,

        marker={
            "size": 5,
            "opacity": 0.55
        },

        line={
            "width": 2
        },

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Score: %{y}"
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

        hoverlabel={
            "font_size": 14
        }
    )

    # --------------------------------------------------
    # X-axis
    # --------------------------------------------------

    fig.update_xaxes(
        title=x_label,

        showgrid=False,

        title_standoff=15
    )

    # --------------------------------------------------
    # Y-axis
    # --------------------------------------------------

    fig.update_yaxes(
        title=y_label,

        showgrid=True,

        gridwidth=1,

        zeroline=False,

        title_standoff=15
    )

    # --------------------------------------------------
    # Display chart
    # --------------------------------------------------

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