# Olympics Data Analysis Dashboard

An interactive web application built with Streamlit that provides comprehensive analysis of Olympics data throughout history.

## Features

- 📊 Overall Analysis: Explore general Olympics statistics and trends
- 🌍 Country Analysis: Analyze performance of different countries
- 🏃‍♂️ Athlete Analysis: Study athlete demographics and physical attributes
- ⚽ Sport Analysis: Investigate sport-specific patterns and trends

## Data Sources

The application uses two main datasets:
- `athlete_events.csv`: Historical data about Olympic athletes and events
- `noc_regions.csv`: Mapping of NOC (National Olympic Committee) codes to regions

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application locally:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Deployment

This application can be deployed on:
1. Streamlit Cloud (Recommended)
2. Heroku
3. Railway
4. Render

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Deploy your app by selecting the repository

## Requirements

- Python 3.7+
- Required packages are listed in `requirements.txt`
