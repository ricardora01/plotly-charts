import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_FILE = Path(__file__).with_name("data.json")


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data(filename: Path) -> dict:
    """Load and validate data from the JSON file."""

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

    if "dimensions" not in chart_data:
        raise ValueError(
            "The JSON file must contain a 'dimensions' property."
        )

    if not chart_data["data"]:
        raise ValueError(
            "The 'data' array cannot be empty."
        )

    if not chart_data["dimensions"]:
        raise ValueError(
            "The 'dimensions' array cannot be empty."
        )

    return chart_data


# --------------------------------------------------
# Validate dimensions
# --------------------------------------------------

def validate_dimensions(
    chart_data: dict,
    df: pd.DataFrame
) -> None:
    """Validate the dimensions defined in the JSON file."""

    for dimension in chart_data["dimensions"]:

        if "key" not in dimension:
            raise ValueError(
                "Every dimension must contain a 'key'."
            )

        key = dimension["key"]

        if key not in df.columns:
            raise ValueError(
                f"Dimension '{key}' was not found in the data."
            )

        if not pd.api.types.is_numeric_dtype(df[key]):
            raise ValueError(
                f"Dimension '{key}' must contain numeric values."
            )


# --------------------------------------------------
# Create Plotly dimensions
# --------------------------------------------------

def create_dimensions(
    chart_data: dict,
    df: pd.DataFrame
) -> list:
    """Create the dimensions required by Plotly."""

    dimensions = []

    for dimension in chart_data["dimensions"]:

        key = dimension["key"]

        label = dimension.get(
            "label",
            key
        )

        values = df[key]

        dimensions.append(
            {
                "label": label,
                "values": values
            }
        )

    return dimensions


# --------------------------------------------------
# Create chart
# --------------------------------------------------

def create_chart(chart_data: dict) -> None:
    """Create and display the parallel coordinates plot."""

    # Convert JSON data to DataFrame.
    df = pd.DataFrame(
        chart_data["data"]
    )

    # Validate dimensions.
    validate_dimensions(
        chart_data,
        df
    )

    # Build Plotly dimensions.
    dimensions = create_dimensions(
        chart_data,
        df
    )

    # --------------------------------------------------
    # Color configuration
    # --------------------------------------------------

    color_column = chart_data.get(
        "color_by",
        chart_data["dimensions"][-1]["key"]
    )

    if color_column not in df.columns:
        raise ValueError(
            f"Color variable '{color_column}' "
            "was not found in the data."
        )

    if not pd.api.types.is_numeric_dtype(
        df[color_column]
    ):
        raise ValueError(
            f"Color variable '{color_column}' "
            "must contain numeric values."
        )

    color_label = chart_data.get(
        "color_label",
        color_column
    )

    # --------------------------------------------------
    # Title configuration
    # --------------------------------------------------

    title = chart_data.get(
        "title",
        "Parallel Coordinates Plot"
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
    # Create figure
    # --------------------------------------------------

    fig = go.Figure(
        data=go.Parcoords(
            line={
                "color": df[color_column],
                "colorscale": "Viridis",
                "showscale": True,
                "colorbar": {
                    "title": color_label
                }
            },
            dimensions=dimensions
        )
    )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    fig.update_layout(
        title={
            "text": full_title,
            "x": 0.02,
            "xanchor": "left"
        },
        font={
            "family": "Arial",
            "size": 14
        },
        margin={
            "l": 80,
            "r": 120,
            "t": 120,
            "b": 60
        }
    )

    # Display chart.
    fig.show()


# --------------------------------------------------
# Main
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