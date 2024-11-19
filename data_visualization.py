import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

# Read the CSV file
df = pd.read_csv('./LDA_topics_modelled_emails.csv')

# Convert sent_time to datetime explicitly
def parse_email_time(time_str):
    try:
        time_str = time_str.replace('(PDT)', '').strip()
        return pd.to_datetime(time_str, format='%a, %d %b %Y %H:%M:%S %z')
    except Exception as e:
        return pd.NaT

# Convert sent_time to datetime
df['parsed_time'] = pd.to_datetime(df['sent_time'].apply(parse_email_time))

# Create time features
df['hour'] = df['parsed_time'].dt.hour
df['day_of_week'] = df['parsed_time'].dt.dayofweek
df['is_business_hours'] = ((df['parsed_time'].dt.hour >= 9) & 
                          (df['parsed_time'].dt.hour < 17) & 
                          (df['parsed_time'].dt.dayofweek < 5)).astype(int)

# Select all numeric columns for correlation
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Calculate correlations with all numeric features
correlation_matrix = df[numeric_cols].corr()

# Create heatmap
plt.figure(figsize=(20, 16))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
            linewidths=0.5, fmt='.2f', center=0)
plt.title('Correlation Heatmap of All Numeric Features')
plt.tight_layout()
plt.show()

# Print top correlations for each time-related feature
time_features = ['hour', 'day_of_week', 'is_business_hours']

for feature in time_features:
    print(f"\nTop 5 correlations for {feature}:")
    correlations = correlation_matrix[feature].sort_values(key=abs, ascending=False)
    print(correlations.drop(feature).head())

# Print time-based statistics
print("\nEmail Statistics by Business Hours:")
print(df.groupby('is_business_hours').agg({
    'email_length': 'mean',
    'num_receivers': 'mean',
    'is_forwarded': 'mean'
}).round(2))

print("\nMost Common Email Hours:")
print(df['hour'].value_counts().head())

print("\nMost Active Days:")
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = df['day_of_week'].value_counts().sort_index()
day_counts.index = days
print(day_counts)