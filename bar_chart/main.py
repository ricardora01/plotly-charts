import json
from pathlib import Path

import pandas as pd
import plotly.express as px


DATA_FILE = Path(__file__).with_name("data.json")


def load_data(filename: Path) -> dict:
    """Load and validate chart data from a JSON file."""

    if not filename.exists():
        raise FileNotFoundError(f"Data file not found: {filename}")

    with filename.open("r", encoding="utf-8") as file:
        chart_data = json.load(file)

    if "data" not in chart_data:
        raise ValueError("The JSON file must contain a 'data' property.")

    if not chart_data["data"]:
        raise ValueError("The JSON data array cannot be empty.")

    return chart_data


def create_chart(chart_data: dict) -> None:
    """Create and display the bar chart."""

    df = pd.DataFrame(chart_data["data"])

    required_columns = {"program", "students"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Each data item must contain 'program' and 'students'."
        )

    # Sort the data to make comparisons easier.
    df = df.sort_values("students", ascending=False)

    fig = px.bar(
        df,
        x="program",
        y="students",
        text="students",
        title=(
            f"{chart_data.get('title', 'Bar Chart')}"
            f"<br><sup>{chart_data.get('subtitle', '')}</sup>"
        ),
        labels={
            "program": chart_data.get("x_label", "Program"),
            "students": chart_data.get("y_label", "Students"),
        },
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Students: %{y:,}"
            "<extra></extra>"
        ),
    )

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
            "b": 100,
        },
        showlegend=False,
        hoverlabel={
            "font_size": 14,
        },
    )

    fig.update_xaxes(
        showgrid=False,
        tickangle=0,
        title_standoff=15,
    )

    fig.update_yaxes(
        rangemode="tozero",
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

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()