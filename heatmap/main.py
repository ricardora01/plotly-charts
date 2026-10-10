import json
from pathlib import Path

import plotly.express as px


DATA_FILE = Path(__file__).with_name("data.json")


def load_data(filename: Path) -> dict:
    """Load and validate heatmap data from a JSON file."""

    if not filename.exists():
        raise FileNotFoundError(
            f"Data file not found: {filename}"
        )

    with filename.open("r", encoding="utf-8") as file:
        chart_data = json.load(file)

    required_fields = {
        "x_values",
        "y_values",
        "values"
    }

    if not required_fields.issubset(chart_data):
        raise ValueError(
            "The JSON file must contain "
            "'x_values', 'y_values', and 'values'."
        )

    x_values = chart_data["x_values"]
    y_values = chart_data["y_values"]
    values = chart_data["values"]

    if not x_values or not y_values or not values:
        raise ValueError(
            "The heatmap data cannot be empty."
        )

    # Number of rows must match y-axis categories.
    if len(values) != len(y_values):
        raise ValueError(
            "The number of rows in 'values' must match "
            "the number of items in 'y_values'."
        )

    # Every row must match the number of x-axis categories.
    for row in values:

        if len(row) != len(x_values):
            raise ValueError(
                "Each row in 'values' must contain the same "
                "number of elements as 'x_values'."
            )

        if not all(
            isinstance(value, (int, float))
            for value in row
        ):
            raise ValueError(
                "All heatmap values must be numeric."
            )

    return chart_data


def create_chart(chart_data: dict) -> None:
    """Create and display the heatmap."""

    fig = px.imshow(
        chart_data["values"],
        x=chart_data["x_values"],
        y=chart_data["y_values"],
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title=(
            f"{chart_data.get('title', 'Heatmap')}"
            f"<br><sup>{chart_data.get('subtitle', '')}</sup>"
        ),
        labels={
            "x": chart_data.get(
                "x_label",
                "X"
            ),
            "y": chart_data.get(
                "y_label",
                "Y"
            ),
            "color": "Score"
        },
    )

    # Improve hover information.
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "%{x}<br>"
            "Average score: %{z}"
            "<extra></extra>"
        )
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
            "l": 140,
            "r": 70,
            "t": 100,
            "b": 80,
        },
        hoverlabel={
            "font_size": 14,
        },
        coloraxis_colorbar={
            "title": "Score"
        },
    )

    # X-axis.
    fig.update_xaxes(
        title=chart_data.get(
            "x_label",
            "Semester"
        ),
        side="bottom",
        title_standoff=15,
    )

    # Y-axis.
    fig.update_yaxes(
        title=chart_data.get(
            "y_label",
            "Subject"
        ),
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