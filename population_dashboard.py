import streamlit as st
import pandas as pd
from map_data import country_coordinates

# Add CSS styling
def inject_custom_css():

    with open('assests/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    inject_custom_css()

main()


population_data = st.file_uploader("Upload CSV file", type="csv")

if population_data is not None:
    st.markdown('<h1 class="title">Population Dashboard from the Year (2015 to 2020)</h1>', unsafe_allow_html=True)

    df = pd.read_csv(population_data)

    countries = df['Country'].unique()
    selected_country = st.sidebar.selectbox('Select Country', countries)
    compare_metric = st.sidebar.selectbox('Metrics', ['Population', 'Line graph', 'Yearly Percentage Change'])

    country_data = df[df['Country'] == selected_country]

    st.markdown("## Population Data")
    st.write(country_data)

    # st.markdown('<div class="section-header">Population Growth</div>', unsafe_allow_html=True)

    if compare_metric == 'Population':
        st.markdown("### Population growth in BarGraph")
        st.bar_chart(country_data[['Year', 'Population']].set_index('Year'))

        population_change = country_data['Population'].diff()
        st.markdown("### Population Change Over Time")
        st.line_chart(population_change)

    elif compare_metric == 'Line graph':
        st.markdown("### Population growth in Linegraph")
        st.line_chart(country_data[['Year', 'Population']].set_index('Year'))

    elif compare_metric == 'Yearly Percentage Change':
        st.markdown("### Yearly Percentage Change")
        st.line_chart(country_data[['Year', 'Yearly Percentage Change']].set_index('Year'))

    st.markdown('<div class="section-header">Population Distribution Map</div>', unsafe_allow_html=True)

    selected_country_coords = country_coordinates.get(selected_country)

    if selected_country_coords:
        selected_country_df = pd.DataFrame({
            'latitude': [selected_country_coords['latitude']],
            'longitude': [selected_country_coords['longitude']]
        })
        st.map(selected_country_df, zoom=4)

    else:
        st.warning("Selected country not found in the database.")
