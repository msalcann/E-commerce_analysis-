import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
import numpy as np

# 1. Load Data
df = pd.read_csv('ecommerce_analysis_dataset.csv')

# 2. Show missing values
print("Missing values before filling:")
print(df.isnull().sum())
print("\nMissing value ratios (%):")
print(df.isnull().sum() / len(df) * 100)

# 3. Fill missing values with logical replacements
# Age Group: fill with mode (most frequent)
df['Age Group'] = df['Age Group'].fillna(df['Age Group'].mode()[0])

# Delivery Time: fill with mean (rounded)
df['Delivery Time'] = df['Delivery Time'].fillna(round(df['Delivery Time'].mean()))

# Discount Rate: fill with mean
df['Discount Rate'] = df['Discount Rate'].fillna(df['Discount Rate'].mean())

# City: fill with mode
df['City'] = df['City'].fillna(df['City'].mode()[0])

print("\nMissing values after filling:")
print(df.isnull().sum())

# 4. Data Preparation
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Delivery Date'] = pd.to_datetime(df['Delivery Date'])

# Calculate daily order counts
daily_orders = df.groupby('Order Date').size().reset_index(name='Order Count')

# 5. Hypothesis Tests and Visualizations

# HYPOTHESIS 1: Effect of Discount Rate on Order Volume
plt.figure(figsize=(10, 6))
sns.boxplot(x='Discount Rate', y='Order Count',
            data=df.groupby(['Order Date', 'Discount Rate']).size().reset_index(name='Order Count'))
plt.title('Order Count by Discount Rate')
plt.xlabel('Discount Rate (%)')
plt.ylabel('Order Count')
plt.show()

# T-test: Discounted vs Non-discounted days
discounted = df[df['Discount Rate'] > 0].groupby('Order Date').size()
non_discounted = df[df['Discount Rate'] == 0].groupby('Order Date').size()
t_stat, p_value = stats.ttest_ind(discounted, non_discounted)
print("\nHypothesis 1 - Discount Effect T-Test:")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# HYPOTHESIS 2: Effect of Weather on Order Volume
plt.figure(figsize=(10, 6))
sns.boxplot(x='Weather', y='Order Count',
            data=df.groupby(['Order Date', 'Weather']).size().reset_index(name='Order Count'))
plt.title('Order Count by Weather')
plt.xlabel('Weather')
plt.ylabel('Order Count')
plt.show()

# T-test: Sunny vs Rainy days
sunny = df[df['Weather'] == 'Sunny'].groupby('Order Date').size()
rainy = df[df['Weather'] == 'Rainy'].groupby('Order Date').size()
t_stat, p_value = stats.ttest_ind(sunny, rainy)
print("\nHypothesis 2 - Weather Effect T-Test:")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# HYPOTHESIS 3: Effect of Delivery Time on Return Status
plt.figure(figsize=(10, 6))
sns.boxplot(x='Delivery Time', y='Return Status', data=df)
plt.title('Return Status by Delivery Time')
plt.xlabel('Delivery Time (days)')
plt.ylabel('Return Status (0: No Return, 1: Returned)')
plt.show()

# Correlation: Delivery Time and Return Status
correlation, p_value = stats.pointbiserialr(df['Delivery Time'], df['Return Status'])
print("\nHypothesis 3 - Delivery Time and Return Status Correlation:")
print(f"Correlation: {correlation:.4f}")
print(f"p-value: {p_value:.4f}")

# HYPOTHESIS 4: New vs Returning Customers and Return Status
plt.figure(figsize=(10, 6))
sns.barplot(x='Customer Type', y='Return Status', data=df)
plt.title('Return Rate by Customer Type')
plt.xlabel('Customer Type')
plt.ylabel('Return Rate')
plt.show()

# Chi-square test
contingency_table = pd.crosstab(df['Customer Type'], df['Return Status'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print("\nHypothesis 4 - Customer Type and Return Status (Chi-square Test):")
print(f"Chi-square value: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")

# 6. Additional Visualizations

# Correlation Matrix
numeric_cols = ['Delivery Time', 'Discount Rate', 'Return Status']
correlation_matrix = df[numeric_cols].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

# Time Series: Daily Order Count
plt.figure(figsize=(12, 6))
daily_orders.plot(x='Order Date', y='Order Count', kind='line')
plt.title('Daily Order Count Trend')
plt.xlabel('Date')
plt.ylabel('Order Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Orders by City
plt.figure(figsize=(10, 6))
df['City'].value_counts().plot(kind='bar')
plt.title('Order Count by City')
plt.xlabel('City')
plt.ylabel('Order Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Orders by Product Category
plt.figure(figsize=(10, 6))
df['Product Category'].value_counts().plot(kind='bar')
plt.title('Order Count by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Order Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Orders by Age Group
plt.figure(figsize=(10, 6))
df['Age Group'].value_counts().plot(kind='bar')
plt.title('Order Count by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Order Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Summary Statistics
print("\nSummary Statistics:")
print("\nDelivery Time Statistics:")
print(df['Delivery Time'].describe())
print("\nReturn Rate:", df['Return Status'].mean())
print("\nAverage Discount Rate:", df['Discount Rate'].mean())

print("\nCategorical Variable Distributions:")
print("\nCustomer Type Distribution:")
print(df['Customer Type'].value_counts(normalize=True))
print("\nWeather Distribution:")
print(df['Weather'].value_counts(normalize=True))
print("\nProduct Category Distribution:")
print(df['Product Category'].value_counts(normalize=True))
