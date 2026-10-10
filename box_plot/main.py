import json
from pathlib import Path

import pandas as pd
import plotly.express as px


DATA_FILE = Path(__file__).with_name("data.json")


def load_data(filename: Path) -> dict:
    """Load and validate box plot data from a JSON file."""

    if not filename.exists():
        raise FileNotFoundError(f"Data file not found: {filename}")

    with filename.open("r", encoding="utf-8") as file:
        chart_data = json.load(file)

    if "data" not in chart_data:
        raise ValueError("The JSON file must contain a 'data' property.")

    if not chart_data["data"]:
        raise ValueError("The JSON data array cannot be empty.")

    for item in chart_data["data"]:

        if "group" not in item or "scores" not in item:
            raise ValueError(
                "Each item must contain 'group' and 'scores'."
            )

        if not item["scores"]:
            raise ValueError(
                f"The group '{item['group']}' has no scores."
            )

        if not all(
            isinstance(value, (int, float))
            for value in item["scores"]
        ):
            raise ValueError(
                f"All scores in '{item['group']}' must be numeric."
            )

    return chart_data


def prepare_dataframe(chart_data: dict) -> pd.DataFrame:
    """
    Convert the grouped JSON structure into a format
    suitable for Plotly.
    """

    rows = []

    for item in chart_data["data"]:

        for score in item["scores"]:

            rows.append({
                "group": item["group"],
                "score": score
            })

    return pd.DataFrame(rows)


def create_chart(chart_data: dict) -> None:
    """Create and display the box plot."""

    df = prepare_dataframe(chart_data)

    fig = px.box(
        df,
        x="group",
        y="score",
        points="outliers",
        title=(
            f"{chart_data.get('title', 'Box Plot')}"
            f"<br><sup>{chart_data.get('subtitle', '')}</sup>"
        ),
        labels={
            "group": chart_data.get("x_label", "Group"),
            "score": chart_data.get("y_label", "Value"),
        },
    )

    # Improve the box plot appearance.
    fig.update_traces(
        boxmean=True,
        line_width=2,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Score: %{y}"
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
        title=chart_data.get("x_label", "Group"),
        showgrid=False,
        title_standoff=15,
    )

    # Y-axis.
    fig.update_yaxes(
        title=chart_data.get("y_label", "Value"),
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