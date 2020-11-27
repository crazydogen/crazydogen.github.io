---
layout: post
title: Getting started easily with the MIMIC-III DB
slug: mimiciiiQS
date: 2020-11-27 11:20
status: publish
author: CrazyDogen
categories: 
  - GettingStarted
tags: 
  - MIMIC-III
  - SQL
excerpt: Quick Start of MIMIC-III
---

### Working with the MIMIC-III database using Structured Query Language 

Before working with the MIMIC-III DB, you have to **be familiar with** basic SQL usage.

 - [Here is an offical tutorial from MIT-LCP](https://github.com/MIT-LCP/mimic-code/blob/master/tutorials/sql-intro.md)
 - [Runoob's cheatsheet](https://www.runoob.com/sql/sql-quickref.html)
 - [W3schools' SQL Tutorial](https://www.w3schools.com/sql/)

### Overview of the MIMIC-III data

 * [Offical Description](https://mimic.physionet.org/gettingstarted/overview/)

![Full Schema](https://mit-lcp.github.io/mimic-schema-spy/diagrams/summary/relationships.real.large.png)

### Bonus: Some query templates

 - Metadata for a particular table (admissions in this example) 

    ```
    \d+ MIMICIII.ADMISSIONS
    ```

 - Total patients
    ```
    SELECT COUNT(*)
    FROM patients;
    ```

 - subject_id hadm_id icustay_id(10 items) from icustays 

    ```
    SELECT subject_id, hadm_id, icustay_id 
    FROM icustays
    LIMIT 10
    ```

 - The numbers of male and female patients
    ```
    SELECT gender, COUNT(*)
    FROM patients
    GROUP BY gender;
    ```
 - Count the number of patients who died
    ```
    SELECT expire_flag, COUNT(*)
    FROM patients
    GROUP BY expire_flag;
    ```
 - Patient age and mortality
    ```
    WITH first_admission_time AS
    (
    SELECT
        p.subject_id, p.dob, p.gender
        , MIN (a.admittime) AS first_admittime
        , MIN( ROUND( (cast(admittime as date) - cast(dob as date)) / 365.242,2) )
            AS first_admit_age
    FROM patients p
    INNER JOIN admissions a
    ON p.subject_id = a.subject_id
    GROUP BY p.subject_id, p.dob, p.gender
    ORDER BY p.subject_id
    )
    SELECT
        subject_id, dob, gender
        , first_admittime, first_admit_age
        , CASE
            -- all ages > 89 in the database were replaced with 300
            WHEN first_admit_age > 89
                then '>89'
            WHEN first_admit_age >= 14
                THEN 'adult'
            WHEN first_admit_age <= 1
                THEN 'neonate'
            ELSE 'middle'
            END AS age_group
    FROM first_admission_time
    ORDER BY subject_id
    ```

 - How many of deaths occurred within the ICU
    ```
    SELECT ie.subject_id, ie.hadm_id, ie.icustay_id,
        ie.intime, ie.outtime, adm.deathtime,
        ROUND((cast(ie.intime as date) - cast(pat.dob as date))/365.242, 2) AS age,
        ROUND((cast(ie.intime as date) - cast(adm.admittime as date))/365.242, 2) AS preiculos,
        CASE
            WHEN ROUND((cast(ie.intime as date) - cast(pat.dob as date))/365.242, 2) <= 1
                THEN 'neonate'
            WHEN ROUND((cast(ie.intime as date) - cast(pat.dob as date))/365.242, 2) <= 14
                THEN 'middle'
            -- all ages > 89 in the database were replaced with 300
            WHEN ROUND((cast(ie.intime as date) - cast(pat.dob as date))/365.242, 2) > 100
                THEN '>89'
            ELSE 'adult'
            END AS ICUSTAY_AGE_GROUP,
        -- note that there is already a "hospital_expire_flag" field in the admissions table which you could use
        CASE
            WHEN adm.hospital_expire_flag = 1 then 'Y'           
        ELSE 'N'
        END AS hospital_expire_flag,
        -- note also that hospital_expire_flag is equivalent to "Is adm.deathtime not null?"
        CASE
            WHEN adm.deathtime BETWEEN ie.intime and ie.outtime
                THEN 'Y'
            -- sometimes there are typographical errors in the death date, so check before intime
            WHEN adm.deathtime <= ie.intime
                THEN 'Y'
            WHEN adm.dischtime <= ie.outtime
                AND adm.discharge_location = 'DEAD/EXPIRED'
                THEN 'Y'
            ELSE 'N'
            END AS ICUSTAY_EXPIRE_FLAG
    FROM icustays ie
    INNER JOIN patients pat
    ON ie.subject_id = pat.subject_id
    INNER JOIN admissions adm
    ON ie.hadm_id = adm.hadm_id;
    ```

 - Categorized Inquiry of Patient Vital Signs
    ```
    select
    ce.subject_id, ce.hadm_id, ce.icustay_id,
    case
        when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then 1 -- HeartRate 心率
        when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then 2 -- SysBP 
        when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then 3 -- DiasBP 
        when itemid in (456,52,6702,443,220052,220181,225312) and valuenum > 0 and valuenum < 300 then 4 -- MeanBP 
        when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then 5 -- RespRate 呼吸率
        when itemid in (223761,678) and valuenum > 70 and valuenum < 120  then 6 -- TempF, converted to degC in valuenum call 华氏度体温，将转为摄氏度
        when itemid in (223762,676) and valuenum > 10 and valuenum < 50  then 6 -- TempC 摄氏度体温
        when itemid in (646,220277) and valuenum > 0 and valuenum <= 100 then 7 -- SpO2 血氧饱和度
        when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then 8 -- Glucose 血糖
        else null end as vitalid
        -- convert F to C
    , case when itemid in (223761,678) then (valuenum-32)/1.8 else valuenum end as valuenum

    from mimiciii.chartevents ce
    where ce.itemid in
    (
    -- HEART RATE 心率
    211, --"Heart Rate"
    220045, --"Heart Rate"

    -- Systolic/diastolic 收缩压/舒张压
    51, --	Arterial BP [Systolic] 动脉压收缩压
    442, --	Manual BP [Systolic] 手动测量血压收缩压
    455, --	NBP [Systolic] 无创血压收缩压
    6701, --	Arterial BP #2 [Systolic] 动脉压 #2 收缩压
    220179, --	Non Invasive Blood Pressure systolic 无创血压收缩压
    220050, --	Arterial Blood Pressure systolic 动脉压收缩压

    8368, --	Arterial BP [Diastolic] 动脉压舒张压
    8440, --	Manual BP [Diastolic] 手动测量血压舒张压
    8441, --	NBP [Diastolic] 无创血压舒张压
    8555, --	Arterial BP #2 [Diastolic] 动脉压 #2 舒张压
    220180, --	Non Invasive Blood Pressure diastolic	 无创血压舒张压
    220051, --	Arterial Blood Pressure diastolic 动脉压舒张压

    -- MEAN ARTERIAL PRESSURE 平均压
    456, --"NBP Mean" 无创血压平均压
    52, --"Arterial BP Mean" 动脉压平均压
    6702, --	Arterial BP Mean #2  动脉压平均压 #2
    443, --	Manual BP Mean(calc) 手动测试血压平均压（计算）
    220052, --"Arterial Blood Pressure mean" 动脉压平均压
    220181, --"Non Invasive Blood Pressure mean" 无创血压平均压
    225312, --"ART BP mean" 动脉压平均压

    -- RESPIRATORY RATE 呼吸率
    618,--	Respiratory Rate 呼吸率
    615,--	Resp Rate (Total) 呼吸率（总）
    220210,--	Respiratory Rate 呼吸率
    224690, --	Respiratory Rate (Total) 呼吸率（总）

    -- SPO2, peripheral 血氧饱和度 体外测量
    646, 220277,

    -- GLUCOSE, both lab and fingerstick 血糖
    807,--	Fingerstick Glucose 指尖血糖
    811,--	Glucose (70-105) 血糖
    1529,--	Glucose 血糖
    3745,--	BloodGlucose 血糖
    3744,--	Blood Glucose 血糖
    225664,--	Glucose finger stick 指尖血糖
    220621,--	Glucose (serum) 血糖（血清）
    226537,--	Glucose (whole blood) 血糖（全血）

    -- TEMPERATURE 体温
    223762, -- "Temperature Celsius" 体温（摄氏度）
    676,	-- "Temperature C" 体温（摄氏度）
    223761, -- "Temperature Fahrenheit" 体温（华氏度）
    678 --	"Temperature F" 体温（华氏度）
    )
    limit 2000
    ```

    [Click me to get more templates](https://mimic.physionet.org/tutorials/intro-to-mimic-iii/)


### **Quick Reference**
 - [MIMIC-III Tables](https://mimic.physionet.org/mimictables/)
 - [MIMIC-III Data Details](https://mimic.physionet.org/mimicdata/)
 - [Querying MIMIC-III](https://mimic.physionet.org/tutorials/intro-to-mimic-iii/)
 - [MIMIC Offical Code Repository](https://github.com/MIT-LCP/mimic-code)
 - [DeepL](https://www.deepl.com/translator) - AI based Translator

    **SQL Tools**
 - [Psycopg](https://www.psycopg.org/docs/usage.html#basic-module-usage) is the most popular PostgreSQL adapter for the **Python** programming language.
 - [pgAdmin](https://www.pgadmin.org/) is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.
 - [Navicat](https://www.navicat.com/en/support/online-manual) is a series of **graphical** database management and development software produced by CyberTech Ltd. for MySQL, MariaDB, MongoDB, Oracle, SQLite, PostgreSQL and Microsoft SQL Server.
 - [Dbeaver](https://dbeaver.com/docs/wiki/) is a universal database management tool for everyone who needs to work with data in a professional way.
