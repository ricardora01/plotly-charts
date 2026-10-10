import json
from pathlib import Path

import pandas as pd
import plotly.express as px


DATA_FILE = Path(__file__).with_name("data.json")


def load_data(filename: Path) -> dict:
    """Load and validate bubble chart data from a JSON file."""

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
            "The JSON data array cannot be empty."
        )

    required_fields = {
        "student",
        "hours",
        "score",
        "exercises"
    }

    for item in chart_data["data"]:

        if not required_fields.issubset(item):
            raise ValueError(
                "Each observation must contain "
                "'student', 'hours', 'score', and 'exercises'."
            )

        numeric_fields = {
            "hours",
            "score",
            "exercises"
        }

        for field in numeric_fields:
            if not isinstance(item[field], (int, float)):
                raise ValueError(
                    f"'{field}' must be numeric."
                )

        if item["exercises"] <= 0:
            raise ValueError(
                "'exercises' must be greater than zero."
            )

    return chart_data


def create_chart(chart_data: dict) -> None:
    """Create and display the bubble chart."""

    df = pd.DataFrame(chart_data["data"])

    fig = px.scatter(
        df,
        x="hours",
        y="score",
        size="exercises",
        hover_name="student",
        size_max=40,
        title=(
            f"{chart_data.get('title', 'Bubble Chart')}"
            f"<br><sup>{chart_data.get('subtitle', '')}</sup>"
        ),
        labels={
            "hours": chart_data.get(
                "x_label",
                "Study hours"
            ),
            "score": chart_data.get(
                "y_label",
                "Exam score"
            ),
            "exercises": chart_data.get(
                "size_label",
                "Completed exercises"
            ),
        },
    )

    # Improve bubble visibility.
    fig.update_traces(
        marker={
            "opacity": 0.7,
            "line": {
                "width": 1
            },
        },
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Study hours: %{x}<br>"
            "Exam score: %{y}<br>"
            "Completed exercises: %{marker.size}"
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
        title=chart_data.get(
            "x_label",
            "Study hours"
        ),
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        title_standoff=15,
    )

    # Y-axis.
    fig.update_yaxes(
        title=chart_data.get(
            "y_label",
            "Exam score"
        ),
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