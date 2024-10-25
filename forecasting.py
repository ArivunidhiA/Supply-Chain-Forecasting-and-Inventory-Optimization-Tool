import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging

class DemandForecaster:
    def __init__(self):
        self.model = None
        self.mae = None
        self.rmse = None
        logging.basicConfig(level=logging.INFO)
        
    def train_exponential_smoothing(self, data: pd.Series, 
                                  seasonal_periods: int = 12) -> None:
        """
        Train Holt-Winters exponential smoothing model.
        
        Args:
            data: Time series data
            seasonal_periods: Number of periods in a season (default: 12 for monthly)
        """
        try:
            self.model = ExponentialSmoothing(
                data,
                seasonal_periods=seasonal_periods,
                trend='add',
                seasonal='add'
            ).fit()
            logging.info("Model training completed successfully")
        except Exception as e:
            logging.error(f"Error during model training: {str(e)}")
            raise
            
    def make_forecast(self, steps: int) -> pd.Series:
        """
        Generate forecast for specified number of steps.
        
        Args:
            steps: Number of periods to forecast
            
        Returns:
            Forecast values as pandas Series
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        forecast = self.model.forecast(steps)
        return forecast
    
    def evaluate_forecast(self, actual: pd.Series, predicted: pd.Series) -> Dict[str, float]:
        """
        Calculate forecast accuracy metrics.
        
        Args:
            actual: Actual values
            predicted: Predicted values
            
        Returns:
            Dictionary containing MAE and RMSE metrics
        """
        self.mae = mean_absolute_error(actual, predicted)
        self.rmse = np.sqrt(mean_squared_error(actual, predicted))
        
        metrics = {
            'MAE': self.mae,
            'RMSE': self.rmse
        }
        
        logging.info(f"Forecast evaluation metrics: {metrics}")
        return metrics
    
    def get_confidence_intervals(self, forecast: pd.Series, 
                               confidence_level: float = 0.95) -> pd.DataFrame:
        """
        Calculate confidence intervals for the forecast.
        
        Args:
            forecast: Forecasted values
            confidence_level: Confidence level (default: 0.95)
            
        Returns:
            DataFrame with lower and upper confidence bounds
        """
        if self.rmse is None:
            raise ValueError("Model must be evaluated before calculating confidence intervals")
            
        z_score = 1.96  # For 95% confidence level
        margin_of_error = z_score * self.rmse
        
        ci_df = pd.DataFrame({
            'forecast': forecast,
            'lower_bound': forecast - margin_of_error,
            'upper_bound': forecast + margin_of_error
        })
        
        return ci_df

if __name__ == "__main__":
    # Example usage
    # Load sample data
    data = pd.read_csv("data/raw/sales_history.csv")
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')['sales']
    
    # Split data
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]
    
    # Create and train forecaster
    forecaster = DemandForecaster()
    forecaster.train_exponential_smoothing(train_data)
    
    # Make predictions
    forecast = forecaster.make_forecast(len(test_data))
    
    # Evaluate
    metrics = forecaster.evaluate_forecast(test_data, forecast)
    print("Forecast Metrics:", metrics)
    
    # Get confidence intervals
    ci_df = forecaster.get_confidence_intervals(forecast)
    print("\nForecast with Confidence Intervals:")
    print(ci_df.head())
