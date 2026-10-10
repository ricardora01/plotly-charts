import json
from pathlib import Path

import pandas as pd
import plotly.express as px


DATA_FILE = Path(__file__).with_name("data.json")


def load_data(filename: Path) -> dict:
    """Load and validate histogram data from a JSON file."""

    if not filename.exists():
        raise FileNotFoundError(f"Data file not found: {filename}")

    with filename.open("r", encoding="utf-8") as file:
        chart_data = json.load(file)

    if "data" not in chart_data:
        raise ValueError("The JSON file must contain a 'data' property.")

    if not chart_data["data"]:
        raise ValueError("The JSON data array cannot be empty.")

    if not all(
        isinstance(value, (int, float))
        for value in chart_data["data"]
    ):
        raise ValueError("All values in 'data' must be numeric.")

    return chart_data


def create_chart(chart_data: dict) -> None:
    """Create and display the histogram."""

    df = pd.DataFrame({
        "score": chart_data["data"]
    })

    number_of_bins = chart_data.get("bins", 10)

    fig = px.histogram(
        df,
        x="score",
        nbins=number_of_bins,
        title=(
            f"{chart_data.get('title', 'Histogram')}"
            f"<br><sup>{chart_data.get('subtitle', '')}</sup>"
        ),
        labels={
            "score": chart_data.get("x_label", "Value"),
            "count": chart_data.get("y_label", "Frequency"),
        },
    )

    # Improve bar appearance.
    fig.update_traces(
        marker_line_width=1,
        opacity=0.85,
        hovertemplate=(
            "<b>Range:</b> %{x}<br>"
            "<b>Students:</b> %{y}"
            "<extra></extra>"
        ),
    )

    # General layout.
    fig.update_layout(
        template="plotly_white",
        title={
            "x": 0.02,
            "xanchor": "left",
        },
        font={
            "family": "Arial",
            "size": 14,
        },
        margin={
            "l": 70,
            "r": 40,
            "t": 100,
            "b": 70,
        },
        showlegend=False,
        bargap=0.05,
        hoverlabel={
            "font_size": 14,
        },
    )

    # X-axis configuration.
    fig.update_xaxes(
        title=chart_data.get("x_label", "Value"),
        showgrid=False,
        title_standoff=15,
    )

    # Y-axis configuration.
    fig.update_yaxes(
        title=chart_data.get("y_label", "Frequency"),
        rangemode="tozero",
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        title_standoff=15,
        dtick=1,
    )

    fig.show()


def main() -> None:
    try:
        chart_data = load_data(DATA_FILE)
        create_chart(chart_data)

    except (
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError
    ) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()