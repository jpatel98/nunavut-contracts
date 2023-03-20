# Govt of Nunavut, Dept of Family Services Contracts
Analysis of contracts worth over $5,000 awarded by the Govt of Nunavut. The data last was scraped on March 18, 11:05pm EDT (see scraper.py for the code).

## Importing libraries


```python
# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
```

## Importing the csv file and exploring the data
Import the csv file from the data directory and look for any duplicates, summary stats and inspect random rows.


```python
# Importing the csv file
df = pd.read_csv('./data/data.csv')
print(f"Number of rows and columns in the dataset: {df.shape}")
```

    Number of rows and columns in the dataset: (1847, 8)



```python
# displays summary statistics for numerical columns
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Project Name</th>
      <th>Contract Type</th>
      <th>Contract Method</th>
      <th>Community</th>
      <th>Originating Department</th>
      <th>Awarded To</th>
      <th>Award Date</th>
      <th>Award Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1838</td>
      <td>1838</td>
      <td>1838</td>
      <td>1838</td>
      <td>1838</td>
      <td>1838</td>
      <td>1838</td>
      <td>1838</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>342</td>
      <td>7</td>
      <td>6</td>
      <td>32</td>
      <td>1</td>
      <td>335</td>
      <td>559</td>
      <td>1574</td>
    </tr>
    <tr>
      <th>top</th>
      <td>Residential Care</td>
      <td>Service Contract</td>
      <td>Public Request for Proposals</td>
      <td>Iqaluit</td>
      <td>Family Services</td>
      <td>Bairn Croft Residential Services Inc.</td>
      <td>01 April 2014</td>
      <td>$23,500.00</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>1054</td>
      <td>1006</td>
      <td>923</td>
      <td>455</td>
      <td>1838</td>
      <td>126</td>
      <td>194</td>
      <td>14</td>
    </tr>
  </tbody>
</table>
</div>



## Data Clean Up
There are 1847 rows in the dataframe. However, the describe() function shows there are only 1838 non-empty values. That means there are 9 empty rows. <br> <br>
*Note: Indexes in programming generally start with 0 and jupyter notebook ignores the first row as it's all column names. So the row numbers are offset by 2 ie. if you see row number 296 as empty, it will show as row 298 on any csv file viewer like excel / google sheets.*


```python
# check for empty rows in the DataFrame
empty_rows = df[df.isnull().all(axis=1)]

# print the empty rows and row numbers
print(empty_rows)
```

         Project Name Contract Type Contract Method Community  \
    296           NaN           NaN             NaN       NaN   
    297           NaN           NaN             NaN       NaN   
    328           NaN           NaN             NaN       NaN   
    448           NaN           NaN             NaN       NaN   
    449           NaN           NaN             NaN       NaN   
    588           NaN           NaN             NaN       NaN   
    726           NaN           NaN             NaN       NaN   
    756           NaN           NaN             NaN       NaN   
    1310          NaN           NaN             NaN       NaN   
    
         Originating Department Awarded To Award Date Award Value  
    296                     NaN        NaN        NaN         NaN  
    297                     NaN        NaN        NaN         NaN  
    328                     NaN        NaN        NaN         NaN  
    448                     NaN        NaN        NaN         NaN  
    449                     NaN        NaN        NaN         NaN  
    588                     NaN        NaN        NaN         NaN  
    726                     NaN        NaN        NaN         NaN  
    756                     NaN        NaN        NaN         NaN  
    1310                    NaN        NaN        NaN         NaN  



```python
# drop rows that have ALL missing or null values
df = df.dropna(how='all')

# Confirming the null rows have been dropped
print(f"Number of rows and columns in the clean dataset: {df.shape}")
```

    Number of rows and columns in the clean dataset: (1838, 8)



```python
# Print a sample of 10 rows
df.sample(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Project Name</th>
      <th>Contract Type</th>
      <th>Contract Method</th>
      <th>Community</th>
      <th>Originating Department</th>
      <th>Awarded To</th>
      <th>Award Date</th>
      <th>Award Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1752</th>
      <td>Residential Care</td>
      <td>Consulting</td>
      <td>Public Request for Proposals</td>
      <td>Rankin Inlet</td>
      <td>Family Services</td>
      <td>Bairn Croft Residential Services Inc.</td>
      <td>29 March 2019</td>
      <td>$483,496.64</td>
    </tr>
    <tr>
      <th>203</th>
      <td>Review Child Abuse Response Protocols</td>
      <td>Consulting</td>
      <td>Public Request for Proposals</td>
      <td>Nunavut Territory</td>
      <td>Family Services</td>
      <td>Michael Rudolph Consulting</td>
      <td>17 January 2019</td>
      <td>$14,000.00</td>
    </tr>
    <tr>
      <th>1284</th>
      <td>Group Home Windows and Doors Upgrades</td>
      <td>Minor Construction or Services</td>
      <td>Public Tender</td>
      <td>Cambridge Bay</td>
      <td>Family Services</td>
      <td>Matador Products</td>
      <td>15 September 2016</td>
      <td>$173,830.00</td>
    </tr>
    <tr>
      <th>243</th>
      <td>SMC Charter</td>
      <td>Air Charters</td>
      <td>Invitational Tender</td>
      <td>Iqaluit</td>
      <td>Family Services</td>
      <td>Air Nunavut</td>
      <td>27 September 2013</td>
      <td>$15,998.00</td>
    </tr>
    <tr>
      <th>870</th>
      <td>Residential Care</td>
      <td>Service Contract</td>
      <td>Public Request for Proposals</td>
      <td>Gjoa Haven</td>
      <td>Family Services</td>
      <td>Sinclair Children's Residence Inc.</td>
      <td>01 April 2015</td>
      <td>$97,150.00</td>
    </tr>
    <tr>
      <th>1673</th>
      <td>Residential Care</td>
      <td>Consulting</td>
      <td>Public Request for Proposals</td>
      <td>Qikiqtaaluk Region</td>
      <td>Family Services</td>
      <td>Partners in Parenting Inc.</td>
      <td>01 April 2017</td>
      <td>$328,260.00</td>
    </tr>
    <tr>
      <th>403</th>
      <td>Residential Care</td>
      <td>Consulting</td>
      <td>Public Request for Proposals</td>
      <td>Iqaluit</td>
      <td>Family Services</td>
      <td>Stepping Stones Foster Care Inc.</td>
      <td>01 April 2017</td>
      <td>$28,811.86</td>
    </tr>
    <tr>
      <th>50</th>
      <td>Residential Care</td>
      <td>Consulting</td>
      <td>Public Request for Proposals</td>
      <td>Iqaluit</td>
      <td>Family Services</td>
      <td>Stirpe, Stones &amp; Associates</td>
      <td>16 January 2016</td>
      <td>$6,638.75</td>
    </tr>
    <tr>
      <th>452</th>
      <td>Ford Explorer</td>
      <td>Purchase Order</td>
      <td>Public Request for Proposals</td>
      <td>Arctic Bay</td>
      <td>Family Services</td>
      <td>Ikpiaryuk Services Ltd.</td>
      <td>22 March 2017</td>
      <td>$36,664.00</td>
    </tr>
    <tr>
      <th>1628</th>
      <td>Residential Care</td>
      <td>Service Contract</td>
      <td>Sole Source</td>
      <td>Rankin Inlet</td>
      <td>Family Services</td>
      <td>Bairn Croft Residential Services Inc.</td>
      <td>01 April 2020</td>
      <td>$285,348.60</td>
    </tr>
  </tbody>
</table>
</div>



## Analysis
The data is now clean, let's try and answer the following questions: <br>
- What is the distribution of contract types?
- Which communities have the highest average awarded value?
- What contractors were awarded the most number of contracts?
- What were the most repeating projects?
- What contractors were received the most amount of money?
- What is the distribution of contract methods?
- What is the distribution of awarded dates?

### Distribution of contract types


```python
# count the occurrences of each contract type
contract_counts = df['Contract Type'].value_counts()

print(contract_counts)
```

    Service Contract                  1006
    Consulting                         630
    Purchase Order                     180
    Air Charters                        10
    Minor Construction or Services       7
    Major Construction                   4
    Architectural/Engineering            1
    Name: Contract Type, dtype: int64


### Communities with highest average awarded value


```python
# Converting the "Award Value" column from object to string.
df['Award Value'] = df['Award Value'].astype(str)

# remove dollar signs and commas from the Award Value column
df['Award Value'] = df['Award Value'].str.replace('$', '', regex=True).str.replace(',', '', regex=True).astype(float)

# group the data by community and calculate the mean awarded value for each community
awarded_mean = df.groupby('Community')['Award Value'].mean()

# sort the results by the mean awarded value in descending order
awarded_mean_sorted = awarded_mean.sort_values(ascending=False).round(2)

# print the top 10 communities by average awarded value
print(awarded_mean_sorted.head(10))
```

    Community
    Kivalliq Region       941427.28
    Chesterfield Inlet    908381.37
    Kitikmeot Region      525957.47
    Qikiqtaaluk Region    307634.51
    Rankin Inlet          252845.33
    Baker Lake            230600.14
    Kugaaruk              207250.48
    Gjoa Haven            197513.34
    Arviat                171800.69
    Sanikiluaq            158495.99
    Name: Award Value, dtype: float64


### Contractors with most number of contracts


```python
# group the data by Awarded To, count the number of contracts awarded to each company, 
# and sort the results in descending order
awarded_count = df.groupby('Awarded To')['Awarded To'].count().sort_values(ascending=False)

# print the top 5 companies awarded the most contracts
top_5_awarded_count = awarded_count.head(5)

print('The top 5 companies awarded the most contracts:\n')
for company, count in top_5_awarded_count.items():
    print(f'{company} - {count} contracts')
```

    The top 5 companies awarded the most contracts:
    
    Bairn Croft Residential Services Inc. - 126 contracts
    Sinclair Children's Residence Inc. - 107 contracts
    I Have a Chance Support Services Ltd. - 103 contracts
    Northern Networks Ltd. - 77 contracts
    Partners in Parenting Inc. - 69 contracts


### Projects with the most awarded contracts


```python
# count the occurrences of each project name
project_counts = df['Project Name'].value_counts()

# sort the results in descending order
project_counts_sorted = project_counts.sort_values(ascending=False)

# print the top 10 project names with the highest frequency
print(project_counts_sorted.head(5))
```

    Residential Care                          1054
    Specialized Residential Care               174
    Office Supplies                             50
    Specialized Residential Care Treatment      43
    Relocation                                  19
    Name: Project Name, dtype: int64


### Contractors with the highest total awarded value across all contracts


```python
top_5_companies = df.groupby('Awarded To')['Award Value'].sum().nlargest(5).round(2)
print(top_5_companies)
```

    Awarded To
    Bairn Croft Residential Services Inc.    32124635.05
    I Have a Chance Support Services Ltd.    20784713.76
    March of Dimes Canada                    19420243.44
    Protegra Inc.                            13217471.30
    Pimakslirvik Corporation                 13137910.04
    Name: Award Value, dtype: float64


### Distribution of contract methods


```python
# create a bar chart of the distribution of contract methods
contract_methods = df['Contract Method'].value_counts()

fig, ax = plt.subplots()
ax.bar(contract_methods.index, contract_methods.values)

# set the x-axis label to vertical orientation
plt.xticks(rotation='vertical')

# add text labels to the bars
for i, v in enumerate(contract_methods.values):
    ax.text(i, v, str(v), ha='center', fontweight='bold')
    
ax.set(title='Distribution of Contract Methods', xlabel='Contract Method', ylabel='Number of Contracts')

plt.show()
```


    
![png](README_files/README_22_0.png)
    


### Distribution of awarded dates


```python
# create a pivot table to count the number of contracts awarded on each day
date_counts = df.groupby('Award Date')['Awarded To'].count()

# reshape the data to create a pivot table
date_counts = date_counts.reset_index(name='count')
date_counts['year'] = pd.DatetimeIndex(date_counts['Award Date']).year
date_counts['month'] = pd.DatetimeIndex(date_counts['Award Date']).month_name()

pivot_table = pd.pivot_table(date_counts, index='month', columns='year', values='count', aggfunc='sum')

# create a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='g')
plt.title('Distribution of Awarded Dates')
plt.xlabel('Year')
plt.ylabel('Month')
plt.show()
```


    
![png](README_files/README_24_0.png)
    

