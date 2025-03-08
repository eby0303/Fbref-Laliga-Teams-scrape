import pandas as pd

def process_possession_stats():
    # URL for scraping the possession stats
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/possession/Barcelona-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    # Step 1: Read the HTML table
    df = pd.read_html(url, attrs={'id': table_id})[0]

    # Step 2: Select columns up to 'PrgR'
    columns_to_keep = df.columns.get_loc(('Receiving', 'PrgR')) + 1  # Get the integer location of 'PrgR'
    df = df.iloc[:, :columns_to_keep]  # Slice the dataframe to keep columns up to 'PrgR'

    # Step 3: Remove the last row
    df = df.iloc[:-1]  # Remove the last row

    # Step 4: Reset the index for a clean dataframe
    df.reset_index(drop=True, inplace=True)

    return df


