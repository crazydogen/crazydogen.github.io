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
    SELECT pvt.subject_id, pvt.hadm_id, pvt.icustay_id

    -- Easier names
    , min(case when VitalID = 1 then valuenum ELSE NULL END) AS heartrate_min
    , max(case when VitalID = 1 then valuenum ELSE NULL END) AS heartrate_max
    , avg(case when VitalID = 1 then valuenum ELSE NULL END) AS heartrate_mean
    , min(case when VitalID = 2 then valuenum ELSE NULL END) AS sysbp_min
    , max(case when VitalID = 2 then valuenum ELSE NULL END) AS sysbp_max
    , avg(case when VitalID = 2 then valuenum ELSE NULL END) AS sysbp_mean
    , min(case when VitalID = 3 then valuenum ELSE NULL END) AS diasbp_min
    , max(case when VitalID = 3 then valuenum ELSE NULL END) AS diasbp_max
    , avg(case when VitalID = 3 then valuenum ELSE NULL END) AS diasbp_mean
    , min(case when VitalID = 4 then valuenum ELSE NULL END) AS meanbp_min
    , max(case when VitalID = 4 then valuenum ELSE NULL END) AS meanbp_max
    , avg(case when VitalID = 4 then valuenum ELSE NULL END) AS meanbp_mean
    , min(case when VitalID = 5 then valuenum ELSE NULL END) AS resprate_min
    , max(case when VitalID = 5 then valuenum ELSE NULL END) AS resprate_max
    , avg(case when VitalID = 5 then valuenum ELSE NULL END) AS resprate_mean
    , min(case when VitalID = 6 then valuenum ELSE NULL END) AS tempc_min
    , max(case when VitalID = 6 then valuenum ELSE NULL END) AS tempc_max
    , avg(case when VitalID = 6 then valuenum ELSE NULL END) AS tempc_mean
    , min(case when VitalID = 7 then valuenum ELSE NULL END) AS spo2_min
    , max(case when VitalID = 7 then valuenum ELSE NULL END) AS spo2_max
    , avg(case when VitalID = 7 then valuenum ELSE NULL END) AS spo2_mean
    , min(case when VitalID = 8 then valuenum ELSE NULL END) AS glucose_min
    , max(case when VitalID = 8 then valuenum ELSE NULL END) AS glucose_max
    , avg(case when VitalID = 8 then valuenum ELSE NULL END) AS glucose_mean

    FROM  (
    select ie.subject_id, ie.hadm_id, ie.icustay_id
    , case
        when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then 1 -- HeartRate
        when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then 2 -- SysBP
        when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then 3 -- DiasBP
        when itemid in (456,52,6702,443,220052,220181,225312) and valuenum > 0 and valuenum < 300 then 4 -- MeanBP
        when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then 5 -- RespRate
        when itemid in (223761,678) and valuenum > 70 and valuenum < 120  then 6 -- TempF, converted to degC in valuenum call
        when itemid in (223762,676) and valuenum > 10 and valuenum < 50  then 6 -- TempC
        when itemid in (646,220277) and valuenum > 0 and valuenum <= 100 then 7 -- SpO2
        when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then 8 -- Glucose

        else null end as vitalid
        -- convert F to C
    , case when itemid in (223761,678) then (valuenum-32)/1.8 else valuenum end as valuenum

    from mimiciii.icustays ie
    left join mimiciii.chartevents ce
    on ie.icustay_id = ce.icustay_id
    -- and ce.charttime between ie.intime and DATETIME_ADD(ie.intime, INTERVAL '1' DAY)
    -- and DATETIME_DIFF(ce.charttime, ie.intime, SECOND) > 0
    -- and DATETIME_DIFF(ce.charttime, ie.intime, HOUR) <= 24
    -- exclude rows marked as error
    and (ce.error IS NULL or ce.error = 0)
    where ce.itemid in
    (
    -- HEART RATE
    211, --"Heart Rate"
    220045, --"Heart Rate"

    -- Systolic/diastolic

    51, --	Arterial BP [Systolic]
    442, --	Manual BP [Systolic]
    455, --	NBP [Systolic]
    6701, --	Arterial BP #2 [Systolic]
    220179, --	Non Invasive Blood Pressure systolic
    220050, --	Arterial Blood Pressure systolic

    8368, --	Arterial BP [Diastolic]
    8440, --	Manual BP [Diastolic]
    8441, --	NBP [Diastolic]
    8555, --	Arterial BP #2 [Diastolic]
    220180, --	Non Invasive Blood Pressure diastolic
    220051, --	Arterial Blood Pressure diastolic


    -- MEAN ARTERIAL PRESSURE
    456, --"NBP Mean"
    52, --"Arterial BP Mean"
    6702, --	Arterial BP Mean #2
    443, --	Manual BP Mean(calc)
    220052, --"Arterial Blood Pressure mean"
    220181, --"Non Invasive Blood Pressure mean"
    225312, --"ART BP mean"

    -- RESPIRATORY RATE
    618,--	Respiratory Rate
    615,--	Resp Rate (Total)
    220210,--	Respiratory Rate
    224690, --	Respiratory Rate (Total)


    -- SPO2, peripheral
    646, 220277,

    -- GLUCOSE, both lab and fingerstick
    807,--	Fingerstick Glucose
    811,--	Glucose (70-105)
    1529,--	Glucose
    3745,--	BloodGlucose
    3744,--	Blood Glucose
    225664,--	Glucose finger stick
    220621,--	Glucose (serum)
    226537,--	Glucose (whole blood)

    -- TEMPERATURE
    223762, -- "Temperature Celsius"
    676,	-- "Temperature C"
    223761, -- "Temperature Fahrenheit"
    678 --	"Temperature F"

    )
    ) pvt 
    group by pvt.subject_id, pvt.hadm_id, pvt.icustay_id
    order by pvt.subject_id, pvt.hadm_id, pvt.icustay_id;
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
