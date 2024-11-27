import pandas as pd
import numpy as np

def preprocess(df, df_region):
    """
    Preprocess the Olympic data for analysis
    
    Parameters:
    df: DataFrame with athlete events data
    df_region: DataFrame with NOC region mappings
    
    Returns:
    Preprocessed DataFrame
    """
    # Keep only Summer Olympics
    df = df[df['Season'] == 'Summer']
    
    # Convert region names to string before merge
    df_region['region'] = df_region['region'].astype(str)
    
    # Merge with region data
    df = df.merge(df_region, on='NOC', how='left')
    
    # Handle region names and convert to string
    df['region'] = df['region'].fillna('Unknown')
    df['region'] = df['region'].astype(str)
    
    # Create unique Games column for identifying unique Olympic events
    df['Games'] = df['Year'].astype(str) + ' ' + df['City']
    
    # Create Event ID for unique event identification
    df['Event_ID'] = df['Year'].astype(str) + '_' + df['Sport'] + '_' + df['Event']
    
    # Handle team events - keep only one entry per team per event
    df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Event', 'Medal'])
    
    # Create binary medal columns
    df['Gold'] = (df['Medal'] == 'Gold').astype(int)
    df['Silver'] = (df['Medal'] == 'Silver').astype(int)
    df['Bronze'] = (df['Medal'] == 'Bronze').astype(int)
    
    # Convert numeric columns
    df['Year'] = df['Year'].astype(int)
    
    # Handle missing values
    df['Age'] = df['Age'].fillna(0).astype(int)
    df['Height'] = df['Height'].fillna(0).astype(int)
    df['Weight'] = df['Weight'].fillna(0).astype(int)
    
    # Convert other string columns to proper string type
    string_columns = ['Name', 'Sex', 'Team', 'NOC', 'Games', 'City', 'Sport', 'Event']
    for col in string_columns:
        df[col] = df[col].astype(str)
    
    # Sort values by Year for better visualization
    df = df.sort_values('Year')
    
    return df