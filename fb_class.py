from sleeper_wrapper import Stats, Players
import pandas as pd

class StatsDF:
    """
    Class to manage player stats for a specific season.
    """
    def __init__(self, season_type: str = None, season_year: int = None):
        self.season_type = season_type
        self.season_year = season_year
        self.stats = Stats()
        self.players = Players()
        self.players_df = None  # This will store the DataFrame with players
        self.stats_df = None  # This will store the DataFrame with stats
        self.all_stats = None  # This will store the merged DataFrame

        self.selected_columns = [
            'search_full_name','player_id', 'team', 'fantasy_positions', 'years_exp',
            'active','age','height','weight','depth_chart_order'
        ]

        if season_year is not None and season_type is not None:
            self.refresh_stats()

    def refresh_stats(self):
        """
        Get stats for the specified season type and year
        and assign the DataFrame with players.
        """
        self.stats_df = self.stats.get_all_stats(self.season_type, self.season_year)
        self.stats_df = self.stats_df.T
        self.players_df = self.get_players_df()
        self.all_stats = self.merge_players_df()
        self.all_stats = self.make_column_first('search_full_name')

    def get_players_df(self) -> pd.DataFrame:
        """
        Retrieve all players and filter selected columns.
        """
        all_players = self.players.get_all_players()
        players_df = pd.DataFrame(all_players)
        players_df = players_df.T
        return players_df[self.selected_columns]

    def merge_players_df(self) -> pd.DataFrame:
        """
        Merge player stats and details.
        """
        return pd.merge(self.stats_df, self.players_df, how='outer', on='player_id')

    def get_stats_df(self) -> pd.DataFrame:
        """
        Return the DataFrame with stats.
        """
        return self.stats_df

    def display_stats_df(self) -> None:
        """
        Display the first few rows of the DataFrame.
        """
        print(self.all_stats.head())

    def make_column_first(self, col_name: str) -> pd.DataFrame:
        """
        Move specified column to the first position and sort the DataFrame by column.
        """
        col_to_move = self.all_stats.pop(col_name)
        self.all_stats.insert(0, col_name, col_to_move)
        return self.all_stats.sort_values(by=col_name, axis=0)
