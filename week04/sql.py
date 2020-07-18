# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

'''
作业要求：请将以下的 SQL 语句翻译成 pandas 语句：
1. SELECT * FROM data;
2. SELECT * FROM data LIMIT 10;
3. SELECT id FROM data;  //id 是 data 表的特定一列
4. SELECT COUNT(id) FROM data;
5. SELECT * FROM data WHERE id<1000 AND age>30;
6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
8. SELECT * FROM table1 UNION SELECT * FROM table2;
9. DELETE FROM table1 WHERE id=10;
10. ALTER TABLE table1 DROP COLUMN column_name;
'''

data1 = pd.DataFrame({'id': range(20), 'order_id': np.random.randint(1000, 1020, 20), 'age': np.random.randint(0, 100, 20)})
data2 = pd.DataFrame({'id': range(20), 'price': np.random.randint(1000, 1010, 20), 'column_name': range(20)})

# 1. SELECT * FROM data;
print(data1)

# 2. SELECT * FROM data LIMIT 10;
print(data1[0:10])

# 3. SELECT id FROM data;
print(data1['id'])

# 4. SELECT COUNT(id) FROM data;
print(data1['id'].count())

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
print(data1[(data1['id'] < 1000) & (data1['age'] > 30)])

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
data1.groupby('age').agg({'order_id': 'value_counts'})

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
print(pd.merge(data1, data2, on='id'))

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
print(pd.concat([data1, data2], axis=1, join='inner'))

# 9. DELETE FROM table1 WHERE id=10;
print(data1[data1['id'] != 10])

# 10. ALTER TABLE table1 DROP COLUMN column_name;
print(data2.drop('column_name',axis = 1))