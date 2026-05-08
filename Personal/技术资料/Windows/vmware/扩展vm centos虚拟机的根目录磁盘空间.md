---
tags:
  - vmware
  - windows
  - 虚拟机
  - 磁盘空间
---


## [](#1-关闭-centos)1、关闭 centos

执行 init 0

## [](#2-vmware-扩展该虚拟机的磁盘空间)2、vmware 扩展该虚拟机的磁盘空间

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701125155683-219313374.png?ynotemdtimestamp=1778125574642)

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701125254534-1100233640.png?ynotemdtimestamp=1778125574642)

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701125404488-1484465175.png?ynotemdtimestamp=1778125574642)

## [](#3-重启虚拟机查看系统分区情况)3、重启虚拟机，查看系统分区情况

指令：df -h

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701125607980-1146597393.png?ynotemdtimestamp=1778125574642)

## [](#4-创建新的分区)4、创建新的分区

查看分区 fdisk -l

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130037781-194683237.png?ynotemdtimestamp=1778125574642)

分区 fdisk /dev/sda

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130146028-2116062036.png?ynotemdtimestamp=1778125574642)

输入 m 获取帮助

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130247126-1328192297.png?ynotemdtimestamp=1778125574642)

输入 n 添加分区

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130318806-938481959.png?ynotemdtimestamp=1778125574642)

输入 p

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130349419-87972837.png?ynotemdtimestamp=1778125574642)

输入 3

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130414294-2032466443.png?ynotemdtimestamp=1778125574642)

一路回车, 最后输入 w 保存本次操作结果

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130559397-1636439399.png?ynotemdtimestamp=1778125574642)

再次查看 磁盘情况 fdisk -l, 多了一个 /dev/sda3

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701130731775-1852718925.png?ynotemdtimestamp=1778125574642)

新建分区/dev/sda3，发现不是LVM的。所以，接下来使用fdisk将其改成LVM的:

fdisk /dev/sda, 然后输入m查看帮助，然后输入 t

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701131059912-1931433160.png?ynotemdtimestamp=1778125574642)

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701131255408-1276278352.png?ynotemdtimestamp=1778125574642)

再次查看 fdisk -l

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701131401028-1900199637.png?ynotemdtimestamp=1778125574642)

## [](#5-重启系统-reboot-新区格式化)5、重启系统 reboot, 新区格式化

将新分区格式化为ext3：mkfs -t ext3 /dev/sda3

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701131934078-1157904248.png?ynotemdtimestamp=1778125574642)

## [](#6-扩展根分区)6、扩展根分区

lvs 查看

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701132033130-1436877423.png?ynotemdtimestamp=1778125574642)

pvcreate /dev/sda3

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701132141523-427547278.png?ynotemdtimestamp=1778125574642)

vgextend centos /dev/sda3

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701132238414-859721476.png?ynotemdtimestamp=1778125574642)

vgdisplay （原先虚拟机划分了20G，这次扩展为最大50G，所以还有 <30G 可用）

主要查看Free PE / Size 7679/ <30 GB，说明我们最多可以有<30G的扩充空间

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701132353131-1361853098.png?ynotemdtimestamp=1778125574642)

扩大根目录所在的逻辑卷: lvextend -L +29G /dev/centos/root /dev/sda3

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701132915577-1534085620.png?ynotemdtimestamp=1778125574642)

扩大/文件系统: xfs_growfs /dev/mapper/centos-root

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701133229425-2143323070.png?ynotemdtimestamp=1778125574642)

再次查看 df -h

![img](https://img2020.cnblogs.com/blog/1615446/202007/1615446-20200701133322398-1031837469.png?ynotemdtimestamp=1778125574642)