import pandas as pd


def process_misc_stats():
    # URL for scraping the miscellaneous stats
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/misc/Barcelona-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    # Read the HTML table
    df = pd.read_html(url, attrs={'id': table_id})[0]

    # Select columns up to 'Won%'
    columns_to_keep = df.columns.get_loc(('Aerial Duels', 'Won%')) + 1 
    df = df.iloc[:, :columns_to_keep] 

    # Remove the last row
    df = df.iloc[:-1] 

    # Reset the index for a clean dataframe
    df.reset_index(drop=True, inplace=True)

    return df



