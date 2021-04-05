#!/usr/bin/env python3
import pandas as pd
import numpy as np

df = pd.DataFrame()

df = df.append({'truth': 185.179993, 'day1': 197.22307753038834, 'day2':
                197.26118010160317, 'day3': 197.19846975345905, 'day4':
                197.1490578795196, 'day5': 197.37179265011116}, ignore_index=True)

df = df.append({'test': 185, 'day1': 197, 'day2':
                197, 'day3': 197, 'day4':
                197, 'day5': 197}, ignore_index=True)
