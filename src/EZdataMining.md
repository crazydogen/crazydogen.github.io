---
layout: post
title: Easy data mining via python
slug: ezDM
date: 2021-04-22 17:01
status: publish
author: CrazyDogen
categories: 
  - Data Mining
tags: 
  - Python
  - Data Mining
excerpt: Easy data mining via python
---

# Easy data mining via python
*Note: This essay uses python for data mining.*

Agenda
 - Pandas
 - Pandas-Profiling
 - Statsmodels
 - Missingno
 - Wordcloud

***

## Pandas
[Pandas](http://pandas.pydata.org/pandas-docs/stable/reference/) is a Python library for exploring, processing, and model data.

Here we take a dataset named mimic-III as an example.

### Basic stats
```python
# First load df from a file
df.head()
df.shape
df[a column].mean()
df[a column].std()
df[a column].max()
df[a column].min()
df[a column].quantile()
df.describe() # brief description
df.isna().any() # check every columns whether it has missing values
df.isna().sum() # count NAN values 
```

#### *Additional tips*
- [Pandas dataframe methods](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html?highlight=dataframe#pandas.DataFrame)

- [Working with missing data](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html)

- [Pandas dataframe Operations](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html#operations)

- [Statistical functions](https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#statistical-functions)
### Charting a tabular dataset

*Supported charts*

```lua
DataFrame.plot([x, y], kind)

 - kind :

    - 'line': line plot (default)
    - 'bar': vertical bar plot
    - 'barh': horizontal bar plot
    - 'hist': histogram
    - 'box': boxplot
    - 'kde': Kernel Density Estimation plot
    - 'density': same as 'kde'
    - 'area': stacked area plot
    - 'pie': pie plot
    - 'scatter': scatter plot
    - 'hexbin': Hexagonal binning plot
```

[![show](https://cdn.kesci.com/upload/image/pz6v5kfnx9.jpg)](https://cdn.kesci.com/upload/image/pz6v5kfnx9.jpg)

***

```python
import pandas as pd
a = pd.read_csv("/path/mimic_demo/admissions.csv")
a.columns = map(str.lower, a.columns)
a.groupby(['marital_status']).count()['row_id'].plot(kind='pie')
```

![pie](https://cdn.kesci.com/rt_upload/8164ABCC4BD740B8B82E04D341CD2130/pz6v9lgwy6.png)
***

```python
a.groupby(['religion']).count()['row_id'].plot(kind = 'barh') 
```
![pie-bar](https://cdn.kesci.com/rt_upload/5CACB1E177EB41008A6539C7A5B0D5DC/pz6v9pk61e.png)
***

```python
p = pd.read_csv("/path/mimic_demo/patients.csv")
p.columns = map(str.lower, p.columns)
ap = pd.merge(a, p, on = 'subject_id' , how = 'inner')
ap.groupby(['religion','gender']).size().unstack().plot(kind="barh", stacked=True)
```
![brah-partients](https://cdn.kesci.com/rt_upload/437373AAB7694E74A9C04236EADFC3AE/pz6vabjbn.png)
***

```python
c = pd.read_csv("/path/mimic_demo/cptevents.csv")
c.columns = map(str.lower, c.columns)
ac = pd.merge(a, c, on = 'hadm_id' , how = 'inner')
ac.groupby(['discharge_location','sectionheader']).size().unstack().plot(kind="barh", stacked=True)
```
![barh-cptevents](https://cdn.kesci.com/rt_upload/BA4307CCFE364B778D53307BFF50F5AD/pz6vazdrjl.png)


## Pandas-profiling
[Pandas-Profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd) is a Python library for exploratory data analysis.


`A quick example`
```python
import pandas as pd
import pandas_profiling
a = pd.read_csv("/path/mimic_demo/admissions.csv")
a.columns = map(str.lower, a.columns)
# ignore the times when profiling since they are uninteresting
cols = [c for c in a.columns if not c.endswith('time')]
pandas_profiling.ProfileReport(a[cols], explorative=True)
```

``Save generated profile to a ".html". ``
```python
profile.to_file("/path/data_profile.html")
```


## Statsmodels
[Statsmodels](https://www.statsmodels.org/stable/index.html) is a Python module that provides classes and functions for the estimation of many different statistical models, as well as for conducting statistical tests, and statistical data exploration. 

### Basic stats
For simplicity, we use statsmodels' `describe` (*Note: ``Describe`` has been deprecated in favor of ``Description`` and it's simplified functional version, ``describe``. ``Describe`` will be removed after 0.13*) for quick stats. The selectable statistics include:

- “nobs” - Number of observations

- “missing” - Number of missing observations

- “mean” - Mean

- “std_err” - Standard Error of the mean assuming no correlation

- “ci” - Confidence interval with coverage (1 - alpha) using the normal or t. This option creates two entries in any tables: lower_ci and upper_ci.

- “std” - Standard Deviation

- “iqr” - Interquartile range

- “iqr_normal” - Interquartile range relative to a Normal

- “mad” - Mean absolute deviation

- “mad_normal” - Mean absolute deviation relative to a Normal

- “coef_var” - Coefficient of variation

- “range” - Range between the maximum and the minimum

- “max” - The maximum

- “min” - The minimum

- “skew” - The skewness defined as the standardized 3rd central moment

- “kurtosis” - The kurtosis defined as the standardized 4th central moment

- “jarque_bera” - The Jarque-Bera test statistic for normality based on the skewness and kurtosis. This option creates two entries, jarque_bera and jarque_beta_pval.

- “mode” - The mode of the data. This option creates two entries in all tables, mode and mode_freq which is the empirical frequency of the modal value.

- “median” - The median of the data.

- “percentiles” - The percentiles. Values included depend on the input value of percentiles.

- “distinct” - The number of distinct categories in a categorical.

- “top” - The mode common categories. Labeled top_n for n in 1, 2, …, ntop.

- “freq” - The frequency of the common categories. Labeled freq_n for n in 1, 2, …, ntop.


```python
import pandas as pd
import statsmodels.stats.descriptivestats as dst

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

a = pd.read_csv("/path/xx.csv") # load your file via pd.read_xx()
de = dst.describe(a)

# Save the description to excel (pandas also support other formats)
df.describe().to_excel("./pd_des.xlsx")
de.to_excel("./sm_des.xlsx")
```


## Missingno
[Missingno](https://github.com/ResidentMario/missingno) offers a visual summary of the completeness of a dataset. This example brings some intuitive thoughts about `ADMISSIONS` table:

 - Not every patient is admitted to the emergency department as there are many missing values in edregtime and edouttime.
 - `Language` data of patients is mendatory field, but it used to be not.

```python
import missingno as msno
a = pd.read_csv("/path/mimic_demo/admissions.csv")
msno.matrix(a)
```
![msno-show](https://cdn.kesci.com/rt_upload/F8F0800F2EEE484B8D2F6644E9FC75E5/pz6vdf5jgp.png)

Missingsno also supports bar charts, heatmaps and dendrograms, check it out at [github](https://github.com/ResidentMario/missingno).

## Wordcloud

[Wordcloud](https://github.com/amueller/word_cloud) visualizes a given text in a word-cloud format

This example illustrates that majority of patients suffered from sepsis.

```python
from wordcloud import WordCloud
text = str(a['diagnosis'].values) #Prepare an input text in string
wordcloud = WordCloud().generate(text) #Generate a word-cloud from the input text

# Plot the word-cloud 
import matplotlib.pyplot as plt
plt.figure(figsize = (10,10))
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.show()
```

![wordcloud](https://cdn.kesci.com/rt_upload/A509C511D92D448A9A23CBAE07F86754/pz6ve5zdjr.png)


## *Reference*
- [MIMIC 数据集数据可视化](https://www.heywhale.com/mw/project/5d9fe977037db3002d4159b4)
- [Data analysis and visualization tutorial at TMF summer school 2019](https://github.com/MIT-LCP/mimic-code/tree/master/tutorials/data_viz)
- [Statistics in Python](https://scipy-lectures.org/packages/statistics/index.html)
- [Bilogur, (2018). Missingno: a missing data visualization suite. Journal of Open Source Software, 3(22), 547.](https://doi.org/10.21105/joss.00547)
- [Allen B. Downey.  Think Stats, 2nd Edition.](https://greenteapress.com/wp/think-stats-2e/)
- [Scipy's statistical functions](https://docs.scipy.org/doc/scipy/reference/stats.html)