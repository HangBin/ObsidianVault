---
tags:
  - Prometheus
---

Prometheus 数据库，PromQL 语言

最新版本 3.0.1 / 2024-11-28

[prometheus cadvisor 容器相关指标](https://blog.csdn.net/qq_34556414/article/details/141866072)
- 容器监控的内存相关指标：
- 容器组内存用量promQL公式
- 容器组内存使用率（占 limit）% promQL公式


模板-docker服务监控
复制id 10619，导入
[配置grafana监控页面](https://blog.csdn.net/qq_32429805/article/details/137178322)

安装

    docker pull prom/prometheus
    docker run -d -p 9090:9090 --name prometheus prom/prometheus:latest
    #从容器中拷贝配置文件到本机目录下
    docker cp prometheus:/etc/prometheus/prometheus.yml /home/prometheus

修改prometheus.yml配置文件，添加监控的容器cAdvisor为目标容器，添加cadvisor地址。

    [root@docker myprom]# vim prometheus.yml
    scrape_configs:
      - job_name: "prometheus"
        static_configs:
          - targets: ["localhost:9090"]
      - job_name: cadvisor
        scrape_interval: 5s
        static_configs:
          - targets:
            - cadvisor:[192.168.10.200:8080]

    #加载配置重新启动容器
    docker run -d -p 9090:9090 --name prometheus \
        -v /home/monitor/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
        prom/prometheus:latest

prometheus访问地址：http://192.168.10.200:9090





docker方式安装
docker-compose.yaml文件如下

    services:
      prometheus:
        volumes:
          - prometheus_data:/prometheus
        command:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--web.console.libraries=/usr/share/prometheus/console_libraries'
          - '--web.console.templates=/usr/share/prometheus/consoles'
          #热加载配置
          - '--web.enable-lifecycle'
          #api配置
          #- '--web.enable-admin-api'
          #历史数据最大保留时间，默认15天
          - '--storage.tsdb.retention.time=30d'  
      cadvisor:
        image: gcr.io/cadvisor/cadvisor:latest
        container_name: cadvisor
        ports:
        - 8080:8080
        volumes:
        - /:/rootfs:ro
        - /var/run:/var/run:rw
        - /sys:/sys:ro
        - /var/lib/docker/:/var/lib/docker:ro
        depends_on:
        - redis

/var/lib/docker/:/var/lib/docker:ro docker的所有数据都挂载到了cadvisor下，所以cadvisor可以监控容器

prometheus数据目录映射

    volumes:
          - /etc/localtime:/etc/localtime:ro
          - ./prometheus/:/etc/prometheus/
          - prometheus_data:/prometheus

参考文档
[Prometheus+grafana环境搭建方法及流程两种方式(docker和源码包)(一)](https://blog.csdn.net/qq_32429805/article/details/137178322)


