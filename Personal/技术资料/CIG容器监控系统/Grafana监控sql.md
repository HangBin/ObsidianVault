---
tags:
  - Grafana
---
计算的是内存使用百分比（以MB为单位）的平均值(以2G内存为准)

    SELECT (mean("value") / (1024.0 * 1024.0)) / 2048.0 * 100 AS "memory_usage_percent"
    FROM "memory_usage"
    WHERE time > now() - 1h
    GROUP BY time(1m)

cadvisor指标数据


ngnix监控数据输出
```http://192.168.10.200:8080/api/v1.0/containers/docker/e53f3665012732f2ecabe2ad228818bb6257395e88004516faf832185eb3a2eb```

> cpu、memory容量
> stats监控数据

    {
        "id": "e53f3665012732f2ecabe2ad228818bb6257395e88004516faf832185eb3a2eb",
        "name": "/docker/e53f3665012732f2ecabe2ad228818bb6257395e88004516faf832185eb3a2eb",
        "aliases": [
            "nginx",
            "e53f3665012732f2ecabe2ad228818bb6257395e88004516faf832185eb3a2eb"
        ],
        "spec": {
            "has_cpu": true,
            "cpu": {
                "limit": 1024,
                "max_limit": 0,
                "mask": "0",
                "period": 100000
            },
            "has_memory": true,
            "memory": {
                "limit": 9223372036854771712,
                "reservation": 9223372036854771712,
                "swap_limit": 9223372036854771712
            },
            "has_network": true,
            "has_filesystem": true,
            "has_diskio": true,
            "has_custom_metrics": false,
            "image": "goharbor/nginx-photon:v2.12.0"
        },
        "stats": [
            {
                "timestamp": "2024-11-28T17:18:09.195812211Z",
                "cpu": {
                    "usage": {
                        "total": 25483654041,
                        "per_cpu_usage": [
                            25483654041
                        ],
                        "user": 18070000000,
                        "system": 7600000000
                    }
                },
                "memory": {
                    "usage": 6365184,
                    "max_usage": 17309696,
                    "cache": 6021120,
                    "rss": 344064,
                    "swap": 2846720,
                    "mapped_file": 499712,
                    "working_set": 3325952,
                    "failcnt": 0,
                    "container_data": {
                        "pgfault": 2321838,
                        "pgmajfault": 1209
                    },
                    "hierarchical_data": {
                        "pgfault": 2321838,
                        "pgmajfault": 1209
                    }
                }
            }
        ]

http://192.168.10.200:8080/api/v1.1/subcontainers/docker/e53f3665012732f2ecabe2ad228818bb6257395e88004516faf832185eb3a2eb

    [
        {
            "name": "/system.slice/sshd.service",
            "spec": {
                "creation_time": "2024-11-28T09:32:25.174000415Z",
                "has_cpu": true,
                "cpu": {
                    "limit": 1024,
                    "max_limit": 0,
                    "period": 100000
                },
                "has_memory": true,
                "memory": {
                    "limit": 9223372036854771712,
                    "reservation": 9223372036854771712,
                    "swap_limit": 9223372036854771712
                }
            },
            "stats": [
                {
                    "timestamp": "2024-11-28T17:07:41.066683347Z",
                    "cpu": {
                        "usage": {
                            "total": 700658536,
                            "per_cpu_usage": [
                                700658536
                            ],
                            "user": 70000000,
                            "system": 640000000
                        },
                        "cfs": {
                            "periods": 0,
                            "throttled_periods": 0,
                            "throttled_time": 0
                        },
                        "schedstat": {
                            "run_time": 0,
                            "runqueue_time": 0,
                            "run_periods": 0
                        },
                        "load_average": 0
                    },
                    "memory": {
                        "usage": 495616,
                        "max_usage": 15622144,
                        "cache": 20480,
                        "rss": 475136,
                        "swap": 4673536,
                        "mapped_file": 20480,
                        "working_set": 487424,
                        "failcnt": 0,
                        "container_data": {
                            "pgfault": 11628,
                            "pgmajfault": 130
                        },
                        "hierarchical_data": {
                            "pgfault": 11628,
                            "pgmajfault": 130
                        }
                    }
                }
            ]
        }
    ]

