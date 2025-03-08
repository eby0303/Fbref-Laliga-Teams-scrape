import pandas as pd

def process_stats():

    # Hardcoded URL and table ID
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga'
    table_id = 'matchlogs_for'

    # Read the HTML table
    df = pd.read_html(url, attrs={'id': table_id})[0]

    # Select columns up to 'Poss'
    key_column = "Poss"
    columns_to_keep = df.columns[:df.columns.get_loc(key_column) + 1]
    df = df[columns_to_keep]

    # Drop rows with missing values
    df = df.dropna(subset=["Result"])

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    return df


