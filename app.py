"""
Fingrid Open Data Viewer Application

This application retrieves electricity data from the Fingrid Open Data API
and displays it in a readable format with statistics and visualizations.
"""
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from services.api_client import FingridAPIClient
from services.data_processor import DataProcessor
from utils.error_handler import handle_error, validate_time_format


def display_menu():
    """Display main menu and return user choice."""
    print("\n" + "="*50)
    print("  Fingrid Open Data Viewer")
    print("="*50)
    print("1. View electricity data")
    print("2. Show available variables")
    print("3. Demo mode (with sample data)")
    print("4. Exit")
    print("="*50)
    return input("Select option (1-4): ").strip()


def display_variables():
    """Show available electricity variables."""
    variables = FingridAPIClient.get_common_variables()
    print("\nAvailable Electricity Variables:")
    print("-" * 50)
    for var_id, description in variables.items():
        print(f"  ID {var_id:3s} - {description}")
    print("-" * 50)


def get_time_input(prompt):
    """
    Get and validate time input from user.
    
    Returns:
        str: Validated time in ISO format.
    """
    while True:
        time_str = input(prompt).strip()
        if validate_time_format(time_str):
            # Format to ISO 8601
            if "T" not in time_str:
                time_str += "T00:00:00Z"
            elif not time_str.endswith("Z"):
                time_str += "Z"
            return time_str
        else:
            print("Invalid format. Please use: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ")


def get_variable_id():
    """
    Get and validate variable ID from user.
    
    Returns:
        str: Valid variable ID.
    """
    while True:
        var_id = input("Enter variable ID (e.g., 124 for Hydro, or 'list' to see all): ").strip()
        if var_id.lower() == "list":
            display_variables()
            continue
        if var_id:
            return var_id
        print("Variable ID cannot be empty.")


def display_results(df, stats, variable_id):
    """
    Display data results in table format with statistics.
    
    Args:
        df: DataFrame with electricity data.
        stats: Dictionary with statistics.
        variable_id: The variable ID being displayed.
    """
    if df.empty:
        print("No data available for the specified parameters.")
        return
    
    print(f"\n📊 Data for Variable {variable_id}:")
    print("-" * 50)
    
    # Display table
    from services.data_processor import DataProcessor
    table = DataProcessor.format_as_table(df, max_rows=20)
    print(table)
    
    # Display statistics
    if stats:
        print("\n📈 Statistics:")
        print("-" * 50)
        print(f"Count:     {stats.get('count', 'N/A')}")
        print(f"Average:   {stats.get('average', 0):.2f}")
        print(f"Maximum:   {stats.get('maximum', 0):.2f}")
        print(f"Minimum:   {stats.get('minimum', 0):.2f}")
        print(f"Median:    {stats.get('median', 0):.2f}")
        print(f"Std Dev:   {stats.get('std_dev', 0):.2f}")
        print("-" * 50)


def plot_data(df, variable_id):
    """
    Plot electricity data using matplotlib.
    
    Args:
        df: DataFrame with electricity data.
        variable_id: The variable ID being displayed.
    """
    if df.empty or "value" not in df.columns:
        print("Cannot plot: insufficient data.")
        return
    
    try:
        # Prepare data
        x_data = df["start_time"] if "start_time" in df.columns else range(len(df))
        y_data = df["value"]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x_data, y_data, marker="o", linestyle="-", linewidth=2, markersize=4)
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.set_title(f"Fingrid Variable {variable_id} - Electricity Data", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        if "start_time" in df.columns:
            fig.autofmt_xdate(rotation=45)
        
        plt.tight_layout()
        plt.show()
        print("✅ Chart displayed successfully.")
    
    except Exception as e:
        handle_error(Exception(f"Failed to create chart: {e}"))


def demo_mode():
    """Demonstrate application with sample data (no API needed)."""
    print("\n" + "="*50)
    print("  DEMO MODE - Sample Electricity Data")
    print("="*50)
    
    # Create mock data simulating hydro production
    import pandas as pd
    from datetime import datetime, timedelta
    import random
    
    try:
        # Generate sample data for hydro production (Variable 124)
        start = datetime(2024, 1, 15, 0, 0, 0)
        times = [start + timedelta(hours=i) for i in range(72)]
        
        # Simulate realistic hydro production values (MWh)
        base_value = 1200
        values = [base_value + random.uniform(-100, 150) for _ in times]
        
        mock_data = [
            {"start_time": t.isoformat() + "Z", "value": round(v, 2)}
            for t, v in zip(times, values)
        ]
        
        print("\n📊 Simulating: Hydro Power Production (Variable 124)")
        print("   Time Period: 2024-01-15 to 2024-01-18")
        
        # Process the mock data
        processor = DataProcessor()
        df = processor.to_dataframe(mock_data)
        stats = processor.calculate_stats(df)
        
        # Display results
        display_results(df, stats, "124")
        
        # Offer visualization
        visualize = input("\nGenerate chart? (y/n): ").strip().lower()
        if visualize == "y":
            plot_data(df, "124")
        
        print("\n✅ Demo completed successfully!")
        print("   This shows how the application processes and displays real data.")
    
    except Exception as e:
        handle_error(e)


def fetch_and_display_data():
    """Fetch data from API and display results."""
    try:
        # Get user inputs
        variable_id = get_variable_id()
        
        print("\nEnter time range for data retrieval:")
        start_time = get_time_input("Start time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ): ")
        end_time = get_time_input("End time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ): ")
        
        # Fetch data
        print("\n⏳ Fetching data from Fingrid API...")
        client = FingridAPIClient()
        raw_data = client.fetch_data(variable_id, start_time, end_time)
        
        # Process data
        processor = DataProcessor()
        df = processor.to_dataframe(raw_data)
        stats = processor.calculate_stats(df)
        
        # Display results
        display_results(df, stats, variable_id)
        
        # Ask about visualization
        if not df.empty:
            visualize = input("\nGenerate chart? (y/n): ").strip().lower()
            if visualize == "y":
                plot_data(df, variable_id)
    
    except Exception as e:
        handle_error(e)
        print("\n💡 Tip: Use Demo Mode (option 3) to see example output without an API key!")


def main():
    """Main application entry point."""
    print("🔌 Welcome to Fingrid Open Data Viewer!")
    print("App for retrieving and analyzing Finland's electricity data\n")
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            fetch_and_display_data()
        elif choice == "2":
            display_variables()
        elif choice == "3":
            demo_mode()
        elif choice == "4":
            print("\n👋 Thank you for using Fingrid Data Viewer. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-4.")


if __name__ == "__main__":
    main()
