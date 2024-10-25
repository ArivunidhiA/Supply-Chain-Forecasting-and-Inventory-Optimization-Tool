import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.preprocessing import MinMaxScaler

class DataProcessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load data from CSV file and perform initial cleaning."""
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def clean_sales_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean sales data by handling missing values and outliers."""
        # Handle missing values
        df['sales'] = df['sales'].fillna(df['sales'].mean())
        
        # Remove outliers using IQR method
        Q1 = df['sales'].quantile(0.25)
        Q3 = df['sales'].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df['sales'] < (Q1 - 1.5 * IQR)) | (df['sales'] > (Q3 + 1.5 * IQR)))]
        
        return df
    
    def prepare_time_series(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepare time series data for forecasting."""
        # Create time-based features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        
        # Scale numerical features
        numerical_cols = ['sales']
        df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
        
        # Split into features and target
        X = df[['year', 'month', 'day', 'day_of_week']]
        y = df['sales']
        
        return X, y
    
    def calculate_inventory_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate key inventory metrics."""
        metrics = {
            'average_inventory': df['inventory_level'].mean(),
            'stockout_rate': (df['inventory_level'] == 0).mean(),
            'turnover_rate': df['sales'].sum() / df['inventory_level'].mean(),
            'holding_cost': df['inventory_level'].mean() * 0.2  # Assuming 20% holding cost
        }
        return metrics

if __name__ == "__main__":
    # Example usage
    processor = DataProcessor()
    df = processor.load_data("data/raw/sales_history.csv")
    df = processor.clean_sales_data(df)
    X, y = processor.prepare_time_series(df)
    metrics = processor.calculate_inventory_metrics(df)
    print("Inventory Metrics:", metrics)
