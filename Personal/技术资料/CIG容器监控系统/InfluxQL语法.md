---
tags:
  - InfluxDB
---

基本的InfluxQL查询语法如下：

    SELECT <字段> FROM <测量> WHERE <条件> GROUP BY <字段> ORDER BY <时间>

例如：

    #这将返回每日平均温度
    SELECT MEAN(temperature) FROM weather WHERE location = 'beijing' GROUP BY time(1d)

influxdb内置函数

    count() 查询非空值的数量
    distinct() 查询唯一值
    top(value,3) 查询最大的N个值
    bottom(value,3) 查询最小的N个值

INTEGRAL()
返回field value曲线下的面积，即关于field value的积分。

    INTEGRAL(/regular_expression/)
    返回满足正则表达式的每个field key关联的值之下的面积。
    
    #该查询返回h2o_feet中的字段water_level的曲线下的面积（以秒为单位）。
    SELECT INTEGRAL("water_level") FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'
    
    #该查询返回h2o_feet中的字段water_level的曲线下的面积（以分钟为单位）。
    SELECT INTEGRAL("water_level",1m) FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'

mean()
返回field value的平均值。

    mean(field_key)
    返回field key对应的field value的平均值。
    
    mean(/regular_expression/)
    返回与正则表达式匹配的每个field key对应的field value的平均值。

    #该查询返回measurement h2o_feet中field key water_level对应的field value的平均值。
    SELECT mean("water_level") FROM "h2o_feet"
    
    #返回h2o_feet中water_level对应的平均值，时间范围在2015-08-17T23:48:00Z和2015-08-18T00:30:00Z之间，并将查询结果按12分钟的时间间隔和每个tag进行分组，同时，该查询用9.01填充没有数据的时间间隔，并将返回的数据point个数和series个数分别限制为7和1。
    SELECT MEAN("water_level") FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:54:00Z' GROUP BY time(12m),* fill(9.01) LIMIT 7 SLIMIT 1

sum()
返回field value的总和。

    SUM(field_key)
    返回field key对应的field value的总和。
    
    SUM(/regular_expression/)
    返回与正则表达式匹配的每个field key对应的field value的总和。
    
    