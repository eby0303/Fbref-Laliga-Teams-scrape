import pandas as pd

def process_passtypes_stats():
    # URL for scraping the passing types stats
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/passing_types/Barcelona-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    # Step 1: Read the HTML table
    df = pd.read_html(url, attrs={'id': table_id})[0]

    # Step 2: Select columns up to 'Blocks'
    columns_to_keep = df.columns.get_loc(('Outcomes', 'Blocks')) + 1  # Get the integer location of 'Blocks'
    df = df.iloc[:, :columns_to_keep]  # Slice the dataframe to keep columns up to 'Blocks'

    # Step 3: Reset the index for a clean dataframe
    df.reset_index(drop=True, inplace=True)
    df = df.iloc[:-1]

    return df
