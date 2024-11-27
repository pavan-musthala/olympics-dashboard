import numpy as np
import pandas as pd
import seaborn as sns

def preprocess_data(df, df_region):
    # Merge with region data
    df = df.merge(df_region, on='NOC', how='left')
    
    # Convert Medal NaN to "No Medal"
    df['Medal'] = df['Medal'].fillna('No Medal')
    
    # Create medal columns
    medals = pd.get_dummies(df['Medal'])
    df = pd.concat([df, medals], axis=1)
    
    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Convert numeric columns
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
    
    return df

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')
    
    return years, countries

def fetch_medal_tally(df, year, country):
    """Fetch medal tally for specific year and/or country with team event handling"""
    # Remove duplicates for team events
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    
    # Filter for rows with medals
    medal_df = medal_df[medal_df['Medal'].notna()]
    
    # Apply filters
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    # Calculate medal counts
    medal_tally = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    # Sort results
    medal_tally = medal_tally.sort_values(
        ['Total', 'Gold', 'Silver', 'Bronze'],
        ascending=[False, False, False, False]
    ).reset_index()
    
    return medal_tally

def data_over_time(df, col):
    """
    Analyze how a column changes over time
    
    Parameters:
        df (pandas.DataFrame): Input DataFrame
        col (str): Column name to analyze
        
    Returns:
        pandas.DataFrame: Count of unique values over time
    """
    if col == 'Countries':
        col = 'region'  # Use 'region' instead of 'Countries'
    
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in DataFrame")
    
    result_df = df.drop_duplicates(['Year', col])[['Year', col]].groupby('Year').count().reset_index()
    result_df.rename(columns={col: 'Count'}, inplace=True)
    return result_df

def most_successful(df, sport):
    """Find most successful athletes in a sport"""
    temp_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x = temp_df['Name'].value_counts().reset_index().head(15)
    x = x.merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={
        'index': 'Name',
        'Name_x': 'Medals',
        'Sport': 'Sport(s)',
        'region': 'Country'
    }, inplace=True)
    return x

def yearwise_medal_tally(df, country):
    """Calculate year-wise medal counts for a country, handling team events correctly"""
    # Filter for the selected country first
    temp_df = df[df['region'] == country].copy()
    
    # Filter for actual medals and deduplicate using Event_ID
    temp_df = temp_df[temp_df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
    temp_df = temp_df.drop_duplicates(subset=['Event_ID', 'Medal'])
    
    # Group by year and count medals
    final_df = temp_df.groupby('Year').agg({
        'Medal': 'count'
    }).reset_index()
    
    final_df.rename(columns={'Medal': 'Medals'}, inplace=True)
    return final_df

def country_event_heatmap(df, country):
    """Create heatmap data for country's performance in different sports"""
    # Filter for the selected country first
    temp_df = df[df['region'] == country].copy()
    
    # Filter for actual medals and deduplicate using Event_ID
    temp_df = temp_df[temp_df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
    temp_df = temp_df.drop_duplicates(subset=['Event_ID', 'Medal'])
    
    # Create pivot table
    pt = temp_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count',
        fill_value=0
    )
    
    return pt

def get_sport_stats(df, sport):
    """Get comprehensive statistics for a sport"""
    temp_df = df[df['Sport'] == sport]
    
    stats = {
        'first_year': int(temp_df['Year'].min()),
        'events': temp_df['Event'].nunique(),
        'athletes': temp_df['Name'].nunique(),
        'nations': temp_df['region'].nunique(),
        'gender_ratio': temp_df['Sex'].value_counts().to_dict()
    }
    
    return stats

def men_vs_women(df):
    """Analyze gender distribution over time"""
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    
    final = men.merge(women, on='Year', how='left')
    final.fillna(0, inplace=True)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    
    # Calculate percentages
    final['Total'] = final['Male'] + final['Female']
    final['Male %'] = round((final['Male'] / final['Total'] * 100), 2)
    final['Female %'] = round((final['Female'] / final['Total'] * 100), 2)
    
    return final

def weight_v_height(df, sport):
    """Analyze physical attributes with proper handling of duplicates"""
    # Remove duplicates to get unique athletes
    athlete_df = df.drop_duplicates(subset=['Name', 'Games', 'Year'])
    
    if sport != 'Overall':
        athlete_df = athlete_df[athlete_df['Sport'] == sport]
    
    # Return only relevant columns with non-null values
    return athlete_df[['Weight', 'Height', 'Medal', 'Sex', 'Sport']].dropna()

def most_successful_countrywise(df, country):
    """Find most successful athletes for a country, handling team events correctly"""
    # Filter for the selected country first
    temp_df = df[df['region'] == country].copy()
    
    # Filter for actual medals and deduplicate using Event_ID
    temp_df = temp_df[temp_df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
    temp_df = temp_df.drop_duplicates(subset=['Event_ID', 'Medal'])
    
    # Count medals per athlete
    athlete_stats = temp_df.groupby('Name').agg({
        'Medal': 'count',
        'Sport': lambda x: ', '.join(sorted(set(x)))
    }).reset_index()
    
    athlete_stats.columns = ['Name', 'Medals', 'Sport']
    
    # Sort by medals and get top athletes
    return athlete_stats.sort_values('Medals', ascending=False).head(10)

def medal_tally(df):
    """Calculate overall medal tally with proper handling of team events"""
    # Remove duplicates for team events by considering unique combinations
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    
    # Filter for rows with medals
    medal_df = medal_df[medal_df['Medal'].notna()]
    
    # Group by region and medal type
    medal_tally = medal_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
    
    # Calculate total
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    # Sort by total medals, then gold, silver, bronze
    medal_tally = medal_tally.sort_values(
        ['Total', 'Gold', 'Silver', 'Bronze'],
        ascending=[False, False, False, False]
    ).reset_index()
    
    return medal_tally
