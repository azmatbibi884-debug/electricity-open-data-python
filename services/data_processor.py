"""
Data processing service for Fingrid electricity data.
"""
import pandas as pd
from tabulate import tabulate
from utils.error_handler import DataProcessingError


class DataProcessor:
    """Process and analyze electricity data from Fingrid API."""
    
    @staticmethod
    def to_dataframe(data):
        """
        Convert raw API response to pandas DataFrame.
        
        Args:
            data (list): Raw data from API.
            
        Returns:
            pd.DataFrame: Processed dataframe.
        """
        try:
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            if "start_time" in df.columns:
                df["start_time"] = pd.to_datetime(df["start_time"])
            return df
        except Exception as e:
            raise DataProcessingError(f"Failed to convert data to dataframe: {e}")

    @staticmethod
    def calculate_stats(df):
        """
        Calculate statistics for the data.
        
        Args:
            df (pd.DataFrame): The data frame.
            
        Returns:
            dict: Statistics including mean, max, min, median, and count.
        """
        try:
            if df.empty or "value" not in df.columns:
                return {}
            return {
                "average": df["value"].mean(),
                "maximum": df["value"].max(),
                "minimum": df["value"].min(),
                "median": df["value"].median(),
                "std_dev": df["value"].std(),
                "count": len(df),
            }
        except Exception as e:
            raise DataProcessingError(f"Failed to calculate statistics: {e}")
    
    @staticmethod
    def format_as_table(df, max_rows=20):
        """
        Format data as a readable table for console display.
        
        Args:
            df (pd.DataFrame): The data frame.
            max_rows (int): Maximum rows to display.
            
        Returns:
            str: Formatted table string.
        """
        try:
            if df.empty:
                return "No data available."
            
            # Select relevant columns and limit rows
            display_cols = ["start_time", "value"] if "start_time" in df.columns else ["value"]
            display_df = df[display_cols].head(max_rows).copy()
            
            # Format timestamp column if present
            if "start_time" in display_df.columns:
                display_df["start_time"] = display_df["start_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
            
            # Round numeric columns to 2 decimal places
            for col in display_df.select_dtypes(include=['float64', 'float32']).columns:
                display_df[col] = display_df[col].round(2)
            
            table = tabulate(display_df, headers="keys", tablefmt="grid", showindex=False)
            
            if len(df) > max_rows:
                table += f"\n... (showing {max_rows} of {len(df)} rows)"
            
            return table
        except Exception as e:
            raise DataProcessingError(f"Failed to format table: {e}")
