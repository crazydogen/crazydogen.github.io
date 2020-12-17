---
layout: post
title: Getting started easily with the time series analysis(TSA)
slug: GetStartedTSA
date: 2020-12-16 10:20
status: publish
author: CrazyDogen
categories: 
  - GettingStarted
tags: 
  - TimeSeries
  - Python
excerpt: Quick Start of TSA
---


### State of the art algorithms in 2020
![Critical difference diagram for classifiers](http://www.timeseriesclassification.com/images/megaCD.jpg)

Solid bars indicate cliques, within which there is no significant difference in rank. Tests are performed with the sign rank test using the Holm correction. **Top clique of four classifiers** represent the state of the art in Spring 2020.

[Click here](http://www.timeseriesclassification.com/results.php) (based on UEA & UCR project) to get more details.
### Datasets
 - [UEA & UCR Time Series Classification Repository](http://www.timeseriesclassification.com/dataset.php) is an ongoing project to develop a comprehensive repository for research into time series classification. 
 - [Peter H Charlton's Project (clinical signals)](http://peterhcharlton.github.io) composes of four clinical time series (Respiratory rate, pulse wave, etc.) now. Besides, he also provided some useful toolboxes for time series mentioned above.
### Python's libs
 - The objective of the  [pyts](https://pyts.readthedocs.io/en/stable/introduction.html#id2) Python package is to make time series classification easily accessible by providing preprocessing and utility tools, and implementations ([Comparisons of performance](https://pyts.readthedocs.io/en/stable/reproducibility.html)) of several algorithms for time series classification.
 - [tslearn ](https://tslearn.readthedocs.io/en/stable/user_guide/userguide.html) (sklearn flavour) is a Python package that provides machine learning tools for the analysis of time series. This package builds on (and hence depends on) scikit-learn, numpy and scipy libraries.

