---
tags:
  - InfluxDB
---

#### 常用的InfluxQL

    -- 查看所有的数据库
    show databases;
    -- 查看所有的measurement
    show measurements;
    -- 查询10条数据
    select * from measurement_name limit 10;

    -- 数据中的时间字段默认显示的是一个纳秒时间戳，改成可读格式
    -- 将时间格式转换为国际标准时间
    precision rfc3339;
    -- 或可以在连接数据库的时候，直接带该参数
    influx -precision rfc3339

    -- 查询最近50条cpu占用记录
    select * from cpu_usage_per_cpu order by time desc limit 50

用户管理

InfluxDB 默认管理员账号：admin，密码为空。我们可以新增用户和权限。命令如下：

    #显示用户
    show users
     
    #创建用户
    create user "username" with password 'password'
     
    #创建管理员权限用户
    create user "username" with password 'password' with all privileges
     
    #删除用户
    drop user "username"

#### 使用HTTP的API操作

    # 查询最近50条记录
    curl -G 'http://192.168.10.200:8086/query?pretty=true' --data-urlencode "db=cadvisor" --data-urlencode "q=SELECT \"value\" FROM \"cpu_usage_per_cpu\" order by time desc limit 50 "

    # 未验证过的语句
    curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE testdb"
    curl -i -XPOST http://192.168.10.200:8086/query --data-urlencode "q=select * from cpu_usage_per_cpu order by time desc limit 50"
    curl -i -XPOST 'http://192.168.10.200:8086/write?db=testdb' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'
    curl -i -XPOST http://192.168.10.200:8086/query --data-urlencode "q=CREATE DATABASE mydb"

InfluxDB下载安装

    wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.8.x86_64.rpm
    yum -y localinstall influxdb-1.7.8.x86_64.rpm
    cp /etc/influxdb/influxdb.conf /etc/influxdb/influxdb.conf.default
    systemctl enable --now influxdb

#### 数据保存策略（Retention Policies）

InfluxDB是没有提供直接删除数据记录的方法，但是提供数据保存策略，主要用于指定数据保留时间，超过指定时间，就删除这部分数据。（设置类似于定期清理的语句）

保留策略语法

    CREATE RETENTION POLICY <retention_policy_name> ON <database_name> DURATION <duration> REPLICATION <n> [SHARD DURATION <duration>] [DEFAULT]
    <retention_policy_name>：保留策略的名称（自定义）
    <database_name>：为哪个数据库创建保留策略
    <duration>：该保留策略对应的数据过期时间
    REPLICATION：副本因子 SHARD DURATION：分片组的默认时长

    -- 查看保留期
    SHOW RETENTION POLICIES ON mydb
    -- 修改保留期
    ALTER RETENTION POLICY "influx_retention" ON mydb DURATION 15d
    -- 删除保留期
    DROP RETENTION POLICY "influx_retention" ON mydb




