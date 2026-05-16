---
tags:
  - Cadvisor
  - InfluxDB
  - Grafan
---
### 一、概述

Docker作为目前十分出色的容器管理技术，得到大量企业的青睐，在生产环境中使用Docker容器部署服务及应用的场景越来越多。所以面对日益庞大的docker服务群应用，如何具有针对性的，有效的监控也变成了企业运维人员工作需求。

容器信息采集及监控的方案有很多，有docker自身的docker stats命令、Scout、Data Dog、Prometheus等，本次分享两款比较经典的容器开源监控组合方案Cadvisor +InfluxDB+Grafana

#### 1. Cadvisor 

Cadvisor 是Google用来监测单节点资源信息的监控工具。 Cadvisor 提供了基础查询界面和http接口，方便其他组件如Grafana 、Prometheus等进行数据抓取。Cadvisor 可以对Docker主机上的资源及容器进行实时监控和性能数据采集，包括CPU使用情况、内存使用情况、网络吞吐量及文件系统使用情况等。Cadvisor 使用Go语言开发，利用Linux的Cgroups获取容器的资源使用信息。

#### 2. 什么是InfluxDB

InfluxDB（时序数据库），常用的一种使用场景：监控数据统计。每毫秒记录一下电脑内存的使用情况，然后就可以根据统计的数据，利用图形化界面（InfluxDB V1一般配合Grafana）制作内存使用情况的折线图；可以理解为按时间记录一些数据（常用的监控数据、埋点统计数据等），然后制作图表做统计。

InfluxDB自带的各种特殊函数如求标准差，随机取样数据，统计数据变化比等，使数据统计和实时分析变得十分方便，适合用于包括DevOps监控，应用程序指标，物联网传感器数据和实时分析的后端存储。类似的数据库有Elasticsearch、Graphite等。

influxdb是一个分布式的时序数据库，它使用Go语言编写的一个开源分布式时序、事件和指标数据库，无需外部依赖。类似的数据库有Elasticsearch、Graphite等。

对常见关系型数据库（Mysql）基础概念的对比

| 概念 | Mysql | InfluxDB |
| --- | --- | --- |
| 数据库 | Database | Database |
| 表 | Table | Measurement |
| 列 | Column | Tag(带索引的，非必须)、field(不带索引)、timestemp(唯一主键) |

#### 3. Grafana

Grafana是一个可视化面板（Dashboard）工具，有着非常漂亮的图表和布局等展示功能，功能齐全的度量仪表盘和图形编辑器，支持Graphite、zabbix、InfluxDB、Prometheus和OpenTSDB等组件作为数据源。

Grafana作为一个开源的数据可视化工具，其最核心的功能是将各种数据通过图表的形式展现出来，以便于进行数据监控和统计分析。它支持多种数据源，如MySQL、Elasticsearch、InfluxDB等，这使得Grafana能够适用于多种不同的监控场景。除此之外，Grafana还具备告警功能，当系统出现问题时能够及时通知用户。


### 二、Cadvisor+InfluxDB+Grafan监控组件架构

监控组件架构图：

组件架构图：
![image](https://i-blog.csdnimg.cn/blog_migrate/1086cd0008aa0b62d5889a1bd9871d04.png)

提示：InfluxDB用于数据存储，Cadvisor 用户数据采集，Grafana用于数据展示。

### 三、Cadvisor+InfluxDB+Grafan安装部署

#### 1. 下载组件镜像

    docker pull tutum/influxdb
    docker pull google/cadvisor
    docker pull grafana/grafana

#### 2. 创建自定义网络
为了把后期创建的Cadvisor+InfluxDB+Grafana这三个容器都加入自己定义的网络便于理解和管理，所以才新建一个自定义网络。

    docker network create monitor
    docker network ls

#### 3. 创建influxdb容器

    docker run -d --net monitor -p 8083:8083 -p 8086:8086 --name influxdb tutum/influxdb
    docker run -d --net monitor -p 8083:8083 -p 8086:8086 --name influxdb -v /home/monitor/influxdb/data:/data tutum/influxdb
    # 8083端口为infuxdb后台控制端口
    # 8086端口是infuxdb的数据端口

访问influxdb控制台http://192.168.10.200:8083,数据准备

    # 创建数据库和数据库用户。
    CREATE USER "root" WITH PASSWORD '123456' WITH ALL PRIVILEGES

    # 创建Cadvisor 数据库cadvisor、用户root，用户和数据库大家可以自行随意定义，用于后期grafana的配置：
    CREATE DATABASE "cadvisor"

#### 4. 创建Cadvisor 容器

    docker run -d -p 8080:8080 --net monitor \
        --volume=/:/rootfs:ro \
    	--volume=/var/run:/var/run:rw \
    	--volume=/sys:/sys:ro \
    	--volume=/var/lib/docker/:/var/lib/docker:ro \
        --name=cadvisor google/cadvisor \
    	-storage_driver=influxdb -storage_driver_db=cadvisor -storage_driver_host=influxdb:8086
    # --mout：把宿主机的相文目录绑定到容器中，这些目录都是Cadvisor 需要采集的目录文件和监控内容；
    # storage_driver：需要指定Cadvisor 的存储驱动、数据库主机、数据库名；

通过http://192.168.10.200:8080端口访问测试一下，第一次访问这个页面有点慢

#### 5. 创建granafa容器

    docker run -d --name grafana --net monitor -p 3000:3000 \
        -v /home/monitor/grafana:/var/lib/grafana grafana/grafana

访问granfana，通过http://192.168.10.200:3000端口的方式访问,默认账户密码（admin/admin），首次登陆需要更新密码。

添加数据源Add data source，如下：

    influxdb数据源
    url:http://influxdb:8086
    Auth:root 123456
    database:cadvisor


测试：
  nginx容器
    docker run -itd  --name nginx -p 8000:80 nginx
  nginx界面: http://192.168.10.200:8000/
  Cadvisor界面：http://192.168.10.200:8080
  influxdb库：http://192.168.10.200:8083/#
  界面：http://192.168.10.200:3000/connections/datasources

