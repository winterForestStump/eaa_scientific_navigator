import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Configure Streamlit page
st.set_page_config(
    page_title="EAA Congress Topic Visual Navigator",
    layout="wide"
)

# Add title and description
st.title("EAA Scientific Program Topics Visual Navigator")

# Add the explanatory text
st.markdown("""
A Visual Navigator of the Scientific programmes' topics from the EAA Congress 2025 and 2026.
The link to the Congress in Prague - https://eaa-online.org/congress-2026/scientific-programme/. Topics semantically similar to each other are closer in the plot. 
Apparently, the tool can be improved if the conference provided also abstracts of the paper, so the embedding could be more precise 
and semantically rich. Also, using more advanced embedding model could improve the results. 
Small disclosure: the tool is a small pet project and may contain some significant flaws: not all topics or categories 
are extracted from the pdf, the embedding didn't work quite well, or there is a mix of authors etc.
""")

col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("Select Year")
with col2:
# Radio button for year selection
    selected_year = st.radio(
        "Choose year to visualize:",
        options=['2025', '2026'],
        horizontal=True,
        label_visibility="collapsed"
    )

# Load data for both years
@st.cache_data
def load_data(year):
    """Load embedding data for a specific year"""
    try:
        df = pd.read_csv(f'data/embeddings/embeddings_{year}.csv')
        return df
    except FileNotFoundError:
        st.error(f"Data file for {year} not found at 'data/embeddings/embeddings_{year}.csv'")
        return None

# Load data for both years simultaneously
data_2025 = load_data('2025')
data_2026 = load_data('2026')

# Check if data is available
if data_2025 is None or data_2026 is None:
    st.stop()

# Select the appropriate dataframe
plot_df = data_2025 if selected_year == '2025' else data_2026

# Create color scale
color_scale = alt.Scale(
    domain=plot_df['category'].unique().tolist(),
    scheme='tableau10'  # Altair's built-in color scheme
)

col1, col2 = st.columns([1, 3])
with col1:
    # Add category filter
    st.markdown("Filter by Category")

with col2:
    categories = ['All'] + sorted(plot_df['category'].unique().tolist())
    selected_categories = st.multiselect(
        "Select categories to display (leave empty for all):",
        options=categories[1:],  # Exclude 'All' from options
        default=[],
        label_visibility="collapsed"
    )

# Filter dataframe based on category selection
filtered_df = plot_df.copy()
if selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

# Create the scatter plot
scatter_plot = alt.Chart(filtered_df).mark_circle(
    size=100,
    stroke='black',
    strokeWidth=0.5
).encode(
    x=alt.X('x', title='UMAP 1', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
    y=alt.Y('y', title='UMAP 2', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
    color=alt.Color('category',
                    title='Category',
                    scale=color_scale,
                    legend=alt.Legend(titleFontSize=14, labelFontSize=12)),
    tooltip=['topic', 'year', 'authors', 'category']
).properties(
    title={
        'text': f'2D UMAP Projection of Research Paper Title Embeddings - {selected_year}',
        'fontSize': 16,
        'fontWeight': 'bold',
        'anchor': 'middle'
    },
    width=800,
    height=600
).interactive()  # Enable zooming and panning

# Display the chart
st.altair_chart(scatter_plot, use_container_width=True)

# Add statistics section
st.markdown("Statistics")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Total Papers Displayed", len(filtered_df))

with col4:
    st.metric("Categories Shown", len(filtered_df['category'].unique()) if not filtered_df.empty else 0)

# Add download button for filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name=f"eaa_{selected_year}_filtered_data.csv",
    mime="text/csv"
)

# Add footer
st.markdown("---")
st.markdown("Tip: Hover over any dot to see the topic title, authors, and category. Use zoom and pan to explore clusters")