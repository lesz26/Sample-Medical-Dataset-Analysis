The goal of this repository is to enhance the speed and computational power with
which the Healthcare Cost and Utilization Projects' National Inpatient Sample (NIS)
and National Ambulatory Surgical Sample (NASS) are analyzed. This codes provides the 
ability to quickly subset (subset.py) using the polars python package, create appropriate 
columns from ICD-10 codes (create_columns.py), and then generate tables 1, 2, and 3 for a 
manuscript (visual_tables.py, CI_Methods.py, log_reg.py). Most analyses should include additional
tables and graphs not coded in this repository. 
