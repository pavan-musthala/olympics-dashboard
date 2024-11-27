import streamlit as st
import pandas as pd
import numpy as np
import preprocessor
import helper
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# Page config
st.set_page_config(
    page_title="Olympics Analysis",
    page_icon="🏅",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Overall dark theme */
    .stApp {
        background-color: #121212;  /* Very dark gray */
    }
    
    .main {
        padding: 0rem 0rem;
        color: #ffffff;
    }
    
    /* Chart container styling */
    .stPlotlyChart {
        background-color: #1e1e1e;  /* Dark gray */
        border-radius: 0.5rem;
        padding: 2rem;
        margin: 1rem 0;
        width: 100% !important;
        height: auto !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #404040;
    }
    
    /* Container styling */
    .element-container {
        width: 100% !important;
    }
    
    .js-plotly-plot, .plot-container {
        width: 100% !important;
        height: auto !important;
    }
    
    .main .block-container {
        max-width: 95% !important;
        padding: 2rem !important;
        background-color: #1e1e1e;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Text styling */
    .title-text {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #2d2d2d;  /* Slightly lighter dark */
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        text-align: center;
        border: 1px solid #404040;
    }
    
    .metric-card h3 {
        font-size: 1.2rem;
        color: #ffffff;
        margin-bottom: 0.8rem;
    }
    
    .metric-card h2 {
        font-size: 2rem;
        margin: 0;
        color: #ffffff;
    }
    
    /* Table styling */
    .dataframe {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        font-size: 1rem;
        border: 1px solid #404040;
        color: #ffffff;
    }
    
    .dataframe th {
        background-color: #404040;
        font-weight: 600;
        color: #ffffff;
        padding: 0.75rem !important;
    }
    
    .dataframe td {
        padding: 0.75rem !important;
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    /* Input styling */
    .stSelectbox, .stTextInput {
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        border: 1px solid #404040;
        padding: 0.5rem;
        color: #ffffff;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d2d2d;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #404040;
        border-radius: 0.3rem;
        margin-right: 0.5rem;
        padding: 0.5rem 1rem;
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #666666;
        color: #ffffff !important;
    }

    /* Fix text colors */
    .st-emotion-cache-1v0mbdj, .st-emotion-cache-16idsys p,
    .st-emotion-cache-16idsys, .st-emotion-cache-1v0mbdj p {
        color: #ffffff !important;
    }

    /* Dropdown text color fix */
    .st-emotion-cache-16idsys p, .st-emotion-cache-16idsys label, 
    .st-emotion-cache-16idsys span {
        color: #ffffff !important;
    }

    /* Selectbox options */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Default Plotly layout settings with dark theme
default_layout = dict(
    plot_bgcolor="#1e1e1e",  # Dark background
    paper_bgcolor="#1e1e1e",
    height=700,
    width=None,
    margin=dict(t=80, l=80, r=40, b=80),
    font=dict(
        size=16,
        color="#ffffff",  # White text
        family="Arial, sans-serif"
    ),
    title=dict(
        font=dict(size=24, color="#ffffff", family="Arial, sans-serif"),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=True,
    legend=dict(
        bgcolor="rgba(30, 30, 30, 0.9)",
        bordercolor="#404040",
        borderwidth=1,
        font=dict(size=14, family="Arial, sans-serif", color="#ffffff"),
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#404040',
        gridwidth=1,
        linecolor='#ffffff',
        linewidth=2,
        tickfont=dict(size=14, family="Arial, sans-serif", color="#ffffff"),
        title_font=dict(size=18, family="Arial, sans-serif", color="#ffffff"),
        tickangle=30
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#404040',
        gridwidth=1,
        linecolor='#ffffff',
        linewidth=2,
        tickfont=dict(size=14, family="Arial, sans-serif", color="#ffffff"),
        title_font=dict(size=18, family="Arial, sans-serif", color="#ffffff")
    )
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('athlete_events.csv')
    df_region = pd.read_csv('noc_regions.csv')
    df = preprocessor.preprocess(df, df_region)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/2560px-Olympic_rings_without_rims.svg.png", width=200)
    st.title("Olympics Analysis")
    user_menu = st.radio(
        "Select Analysis",
        ['🏅 Medal Tally', '📊 Overall Analysis', '🌍 Country Analysis', '🏃‍♂️ Athlete Analysis', '⚽ Sport Analysis']
    )

# Medal Tally
if user_menu == '🏅 Medal Tally':
    st.sidebar.header('Medal Tally')
    years, countries = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == 'Overall':
        st.markdown("### 🏅 Overall Medal Tally")
    elif selected_year != "Overall" and selected_country == 'Overall':
        st.markdown(f"### 🏅 Medal Tally in {str(selected_year)} Olympics")
    elif selected_year == "Overall" and selected_country != 'Overall':
        st.markdown(f"### 🏅 {selected_country}'s Overall Olympic Performance")
    else:
        st.markdown(f"### 🏅 {selected_country}'s Performance in {str(selected_year)} Olympics")

    # Add slider for number of countries to display
    if selected_country == 'Overall':
        num_countries = st.slider(
            "Number of Countries to Display",
            min_value=5,
            max_value=len(medal_tally),
            value=20,
            step=5,
            help="Adjust the slider to show more or fewer countries in the medal tally"
        )
        medal_tally = medal_tally.head(num_countries)

    # Format the medal tally table
    if not medal_tally.empty:
        # Create a styled dataframe
        styled_df = medal_tally.style.format({
            'Gold': '{:,.0f}',
            'Silver': '{:,.0f}',
            'Bronze': '{:,.0f}',
            'Total': '{:,.0f}'
        })
        
        # Display the table
        st.dataframe(styled_df, use_container_width=True)
        
        # Create medal visualization
        if selected_country == 'Overall':
            fig = px.bar(medal_tally, 
                        x='region' if 'region' in medal_tally.columns else 'NOC',
                        y=['Gold', 'Silver', 'Bronze'],
                        title='Medal Distribution by Country',
                        labels={'value': 'Number of Medals', 'variable': 'Medal Type'},
                        color_discrete_map={
                            'Gold': 'gold',
                            'Silver': 'silver',
                            'Bronze': '#cd7f32'
                        })
            
            fig.update_layout(
                barmode='group',
                xaxis_tickangle=-45,
                height=500,
                legend_title_text='Medal Type',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add pie chart for total medal distribution
            fig_pie = px.pie(medal_tally, 
                           values='Total', 
                           names='region' if 'region' in medal_tally.columns else 'NOC',
                           title='Share of Total Olympic Medals',
                           hole=0.3)
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No medal data available for the selected criteria.")

# Overall Analysis
elif user_menu == '📊 Overall Analysis':
    st.markdown("<h1 class='title-text'>Olympic Games Analysis</h1>", unsafe_allow_html=True)
    
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <h3>Editions</h3>
                <h2>%d</h2>
            </div>
        """ % editions, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <h3>Host Cities</h3>
                <h2>%d</h2>
            </div>
        """ % cities, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <h3>Sports</h3>
                <h2>%d</h2>
            </div>
        """ % sports, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <h3>Events</h3>
                <h2>%d</h2>
            </div>
        """ % events, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <h3>Athletes</h3>
                <h2>%d</h2>
            </div>
        """ % athletes, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <h3>Nations</h3>
                <h2>%d</h2>
            </div>
        """ % nations, unsafe_allow_html=True)

    st.markdown("### 📈 Participation Trends")
    
    tab1, tab2, tab3 = st.tabs(["Countries", "Events", "Athletes"])
    
    with tab1:
        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x='Year', y='Count',
                     title='Participating Nations Over Time',
                     labels={'Count': 'Number of Countries'})
        fig.update_layout(plot_bgcolor='white')
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
        
    with tab2:
        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x='Year', y='Count',
                     title='Olympic Events Over Time',
                     labels={'Count': 'Number of Events'})
        fig.update_layout(plot_bgcolor='white')
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
        
    with tab3:
        athletes_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athletes_over_time, x='Year', y='Count',
                     title='Athletes Participation Over Time',
                     labels={'Count': 'Number of Athletes'})
        fig.update_layout(plot_bgcolor='white')
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })

    st.markdown("### 🏆 Sports Analysis")
    
    # Create pivot table for heatmap
    pivot_data = df.pivot_table(
        index='Sport', 
        columns='Year', 
        values='Event', 
        aggfunc='count',
        fill_value=0
    )
    
    # Create heatmap with annotations
    fig = px.imshow(
        pivot_data,
        color_continuous_scale='Viridis',  # Using Viridis colorscale for better visibility in dark theme
        aspect='auto'  # Maintain aspect ratio
    )
    
    # Update layout for better visibility
    fig.update_layout(
        title=dict(
            text='Number of Events per Sport Over Time',
            font=dict(size=24)
        ),
        height=max(600, len(pivot_data.index) * 25),  # Dynamic height based on number of sports
        xaxis=dict(
            title='Year',
            tickangle=45,
            tickfont=dict(size=12),
            tickmode='array',
            ticktext=[str(int(year)) for year in pivot_data.columns],
            tickvals=list(range(len(pivot_data.columns)))
        ),
        yaxis=dict(
            title='Sport',
            tickfont=dict(size=12)
        ),
        coloraxis=dict(
            colorbar=dict(
                title='Number of Events',
                tickfont=dict(size=12),
                titlefont=dict(size=14)
            )
        )
    )
    
    # Add text annotations to show numbers in each cell
    for i in range(len(pivot_data.index)):
        for j in range(len(pivot_data.columns)):
            value = pivot_data.iloc[i, j]
            if value > 0:  # Only show non-zero values
                fig.add_annotation(
                    x=j,
                    y=i,
                    text=str(int(value)),
                    showarrow=False,
                    font=dict(
                        color='white',
                        size=10
                    )
                )
    
    fig.update_layout(default_layout)
    
    # Show the heatmap
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
    })

# Country Analysis
elif user_menu == '🌍 Country Analysis':
    st.markdown("<h1 class='title-text'>Country Analysis</h1>", unsafe_allow_html=True)
    
    # Country selection - ensure all values are strings before sorting
    countries = ['Overall'] + sorted([str(x) for x in df['region'].astype(str).unique() if pd.notna(x)])
    selected_country = st.selectbox('Select Country', countries)

    if selected_country == 'Overall':
        # Show overall statistics
        medal_tally = helper.medal_tally(df)
        
        # Display the medal tally table
        st.dataframe(medal_tally.style.format({
            'Gold': '{:,.0f}',
            'Silver': '{:,.0f}',
            'Bronze': '{:,.0f}',
            'Total': '{:,.0f}'
        }), use_container_width=True)
    else:
        # Country statistics
        country_df = df[df['region'] == selected_country].copy()
        
        # Count medals by type, handling team events by deduplicating on unique event identifiers
        medal_df = country_df.drop_duplicates(subset=['Year', 'Sport', 'Event', 'Medal'])
        
        gold_medals = len(medal_df[medal_df['Medal'] == 'Gold'])
        silver_medals = len(medal_df[medal_df['Medal'] == 'Silver'])
        bronze_medals = len(medal_df[medal_df['Medal'] == 'Bronze'])
        total_medals = gold_medals + silver_medals + bronze_medals
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class='metric-card gold'>
                    <h3>Gold Medals</h3>
                    <h2>{gold_medals}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='metric-card silver'>
                    <h3>Silver Medals</h3>
                    <h2>{silver_medals}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='metric-card bronze'>
                    <h3>Bronze Medals</h3>
                    <h2>{bronze_medals}</h2>
                </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Total Medals</h3>
                    <h2>{total_medals}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_athletes = country_df['Name'].nunique()
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Total Athletes</h3>
                    <h2>{total_athletes:,}</h2>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            years_participated = country_df['Year'].nunique()
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Olympics Participated</h3>
                    <h2>{years_participated}</h2>
                </div>
            """, unsafe_allow_html=True)

        # Medal timeline
        st.markdown("### 📈 Medal Timeline")
        medal_timeline = helper.yearwise_medal_tally(df, selected_country)
        
        if not medal_timeline.empty:
            fig = px.line(medal_timeline, x='Year', y='Medals',
                         title=f'Medal Timeline for {selected_country}',
                         labels={'Medals': 'Number of Medals'})
            
            # Update layout for better visibility
            fig.update_traces(
                line=dict(width=3),
                mode='lines+markers',
                marker=dict(size=8)
            )
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Number of Medals",
                showlegend=False,
                hovermode='x unified'
            )
            
            fig.update_layout(default_layout)
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
        else:
            st.info(f"No medal data available for {selected_country}")

        # Sports Performance
        st.markdown("### 🏆 Sports Performance")
        sports_data = helper.country_event_heatmap(df, selected_country)
        
        if not sports_data.empty:
            fig = px.imshow(
                sports_data,
                labels=dict(x="Year", y="Sport", color="Medals"),
                aspect="auto"
            )
            fig.update_layout(
                title=f'{selected_country}\'s Performance in Different Sports',
                plot_bgcolor='white'
            )
            fig.update_layout(default_layout)
            st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'scrollZoom': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
                })
        else:
            st.info(f"No sports performance data available for {selected_country}")

        # Top Athletes
        st.markdown("### 🥇 Top Athletes")
        top_athletes = helper.most_successful_countrywise(df, selected_country)
        
        if not top_athletes.empty:
            fig = px.bar(
                top_athletes.head(10),
                x='Name',
                y='Medals',
                text='Medals',
                hover_data=['Sport'],
                title=f'Top 10 Athletes from {selected_country}'
            )
            fig.update_layout(
                plot_bgcolor='white',
                xaxis_title="Athlete",
                yaxis_title="Number of Medals"
            )
            fig.update_layout(default_layout)
            st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'scrollZoom': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
                })
        else:
            st.info(f"No athlete data available for {selected_country}")

# Athlete Analysis
elif user_menu == '🏃‍♂️ Athlete Analysis':
    st.markdown("<h1 class='title-text'>Athlete Analysis</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Age Distribution", "📏 Physical Attributes"])
    
    with tab1:
        st.markdown("### Age Distribution Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            # Overall age distribution
            x1 = df['Age'].dropna()
            fig = px.histogram(
                x=x1,
                nbins=30,
                title='Overall Age Distribution',
                labels={'x': 'Age', 'y': 'Count'}
            )
            fig.update_layout(plot_bgcolor='white')
            fig.update_layout(default_layout)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
            
        with col2:
            # Medal winners age distribution
            medal_ages = {
                'Gold': df[df['Medal'] == 'Gold']['Age'].dropna(),
                'Silver': df[df['Medal'] == 'Silver']['Age'].dropna(),
                'Bronze': df[df['Medal'] == 'Bronze']['Age'].dropna()
            }
            
            fig = go.Figure()
            for medal, ages in medal_ages.items():
                fig.add_trace(go.Violin(
                    y=ages,
                    name=medal,
                    box_visible=True,
                    meanline_visible=True
                ))
            
            fig.update_layout(
                title='Age Distribution by Medal Type',
                yaxis_title='Age',
                plot_bgcolor='white'
            )
            fig.update_layout(default_layout)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
        
        # Age distribution by sport
        st.markdown("### Age Distribution by Sport")
        sports = ['Overall'] + sorted(df['Sport'].unique().tolist())
        selected_sport = st.selectbox('Select Sport', sports)
        
        if selected_sport == 'Overall':
            sport_df = df
        else:
            sport_df = df[df['Sport'] == selected_sport]
        
        fig = px.violin(
            sport_df,
            y='Age',
            x='Sex',
            color='Medal',
            box=True,
            title=f'Age Distribution for {selected_sport}',
            labels={'Age': 'Age (years)', 'Sex': 'Gender'}
        )
        fig.update_layout(plot_bgcolor='white')
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
    
    with tab2:
        st.markdown("### Physical Attributes Analysis")
        
        # Sport selection for physical attributes
        sports = ['Overall'] + sorted(df['Sport'].unique().tolist())
        selected_sport = st.selectbox('Select Sport for Physical Analysis', sports)
        
        if selected_sport == 'Overall':
            sport_df = df
        else:
            sport_df = df[df['Sport'] == selected_sport]
        
        # Height vs Weight scatter plot
        fig = px.scatter(
            sport_df,
            x='Weight',
            y='Height',
            color='Sex',
            symbol='Medal',
            title=f'Height vs Weight Distribution for {selected_sport}',
            labels={
                'Weight': 'Weight (kg)',
                'Height': 'Height (cm)',
                'Sex': 'Gender'
            }
        )
        fig.update_layout(plot_bgcolor='white')
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })
        
        # Gender participation
        st.markdown("### 👥 Gender Distribution Over Time")
        gender_data = helper.men_vs_women(df)
        
        fig = px.line(
            gender_data,
            x='Year',
            y=['Male', 'Female'],
            title='Gender Distribution in Olympics',
            labels={'value': 'Number of Athletes', 'variable': 'Gender'}
        )
        fig.update_layout(plot_bgcolor='white')
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
            })

# Sport Analysis
elif user_menu == '⚽ Sport Analysis':
    st.markdown("<h1 class='title-text'>Sport Analysis</h1>", unsafe_allow_html=True)
    
    # Sport selection
    sports = ['Overall'] + sorted(df['Sport'].unique().tolist())
    selected_sport = st.selectbox('Select Sport', sports)
    
    if selected_sport == 'Overall':
        # Show overall sports statistics
        total_sports = len(df['Sport'].unique())
        total_events = len(df['Event'].unique())
        total_athletes = len(df['Name'].unique())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Total Sports</h3>
                    <h2 style='color:#1f77b4'>{total_sports}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Total Events</h3>
                    <h2 style='color:#1f77b4'>{total_events:,}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Total Athletes</h3>
                    <h2 style='color:#1f77b4'>{total_athletes:,}</h2>
                </div>
            """, unsafe_allow_html=True)
            
        # Show sports distribution
        sports_dist = df.groupby('Sport')['Event'].nunique().sort_values(ascending=True)
        fig = px.bar(sports_dist, 
                    orientation='h',
                    title='Number of Events by Sport',
                    labels={'Sport': 'Sport', 'Event': 'Number of Events'})
        fig.update_layout(default_layout)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Get sport statistics
        sport_stats = helper.get_sport_stats(df, selected_sport)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>First Appearance</h3>
                    <h2 style='color:#1f77b4'>{sport_stats['first_year']}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Total Events</h3>
                    <h2 style='color:#1f77b4'>{sport_stats['events']}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>Athletes</h3>
                    <h2 style='color:#1f77b4'>{sport_stats['athletes']:,}</h2>
                </div>
            """, unsafe_allow_html=True)

        # Gender distribution in sport
        male_athletes = sport_stats['gender_ratio'].get('M', 0)
        female_athletes = sport_stats['gender_ratio'].get('F', 0)
        total_athletes = male_athletes + female_athletes
        
        if total_athletes > 0:
            male_percent = round((male_athletes / total_athletes * 100), 1)
            female_percent = round((female_athletes / total_athletes * 100), 1)
            
            st.markdown("### ⚖️ Gender Distribution")
            fig_gender = px.pie(values=[male_percent, female_percent],
                              names=['Male', 'Female'],
                              title=f'Gender Distribution in {selected_sport}')
            fig_gender.update_traces(textinfo='percent+label')
            fig_gender.update_layout(default_layout)
            st.plotly_chart(fig_gender, use_container_width=True, config={
                    'displayModeBar': True,
                    'scrollZoom': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
                })

else:
    st.error("Invalid menu selection")
