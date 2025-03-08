import pandas as pd

def process_passing_stats():
    # URL for scraping the passing stats
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/passing/Barcelona-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    # Read the HTML table
    df = pd.read_html(url, attrs={'id': table_id})[0]

    # Select columns up to 'PrgP'
    columns_to_keep = df.columns.get_loc(('Unnamed: 30_level_0', 'PrgP')) + 1 
    df = df.iloc[:, :columns_to_keep]  
    
    
    # Reset the index for a clean dataframe
    df.reset_index(drop=True, inplace=True)
    df = df.iloc[:-1]

    return df
