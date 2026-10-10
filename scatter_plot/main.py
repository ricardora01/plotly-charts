import json
from pathlib import Path

import pandas as pd
import plotly.express as px


DATA_FILE = Path(__file__).with_name("data.json")


def load_data(filename: Path) -> dict:
    """Load and validate scatter plot data from a JSON file."""

    if not filename.exists():
        raise FileNotFoundError(f"Data file not found: {filename}")

    with filename.open("r", encoding="utf-8") as file:
        chart_data = json.load(file)

    if "data" not in chart_data:
        raise ValueError(
            "The JSON file must contain a 'data' property."
        )

    if not chart_data["data"]:
        raise ValueError(
            "The JSON data array cannot be empty."
        )

    for item in chart_data["data"]:

        required_fields = {"student", "hours", "score"}

        if not required_fields.issubset(item):
            raise ValueError(
                "Each observation must contain "
                "'student', 'hours', and 'score'."
            )

        if not isinstance(item["hours"], (int, float)):
            raise ValueError("'hours' must be numeric.")

        if not isinstance(item["score"], (int, float)):
            raise ValueError("'score' must be numeric.")

    return chart_data


def create_chart(chart_data: dict) -> None:
    """Create and display the scatter plot."""

    df = pd.DataFrame(chart_data["data"])

    fig = px.scatter(
        df,
        x="hours",
        y="score",
        hover_name="student",
        title=(
            f"{chart_data.get('title', 'Scatter Plot')}"
            f"<br><sup>{chart_data.get('subtitle', '')}</sup>"
        ),
        labels={
            "hours": chart_data.get("x_label", "X"),
            "score": chart_data.get("y_label", "Y"),
        },
    )

    # Improve point visibility.
    fig.update_traces(
        marker={
            "size": 11,
            "opacity": 0.8,
            "line": {
                "width": 1
            },
        },
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Study hours: %{x}<br>"
            "Exam score: %{y}"
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
        hoverlabel={
            "font_size": 14,
        },
    )

    # X-axis.
    fig.update_xaxes(
        title=chart_data.get("x_label", "X"),
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        title_standoff=15,
    )

    # Y-axis.
    fig.update_yaxes(
        title=chart_data.get("y_label", "Y"),
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        title_standoff=15,
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