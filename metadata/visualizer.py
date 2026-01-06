import plotly.express as px
from pathlib import Path


def visualize(df):
    """
    Auto-detect chart type:
    - 1 numeric + time → line chart
    - 2 dimensions → heatmap
    """

    # Normalize column names
    cols = list(df.columns)

    # -------------------------------
    # HEATMAP LOGIC (2 dimensions)
    # -------------------------------
    if len(cols) >= 3:
        dim_x = cols[0]
        dim_y = cols[1]
        value_col = cols[2]

        fig = px.density_heatmap(
            df,
            x=dim_x,
            y=dim_y,
            z=value_col,
            color_continuous_scale="Viridis",
            title=f"{value_col} by {dim_y} and {dim_x}"
        )

        output_path = Path(__file__).parent / "heatmap.html"
        fig.write_html(output_path)

        print(f"🔥 Heatmap saved to: {output_path}")
        return

    # -------------------------------
    # LINE CHART (fallback)
    # -------------------------------
    fig = px.line(
        df,
        x=cols[0],
        y=cols[-1],
        markers=True,
        title="Trend"
    )

    output_path = Path(__file__).parent / "line_chart.html"
    fig.write_html(output_path)

    print(f"📈 Line chart saved to: {output_path}")



if __name__ == "__main__":
    print("📊 Running query and generating chart...")
    df = run_query()
    visualize(df)
