---
tags:
  - windows
  - notepad
---

> notepad怎么批量删除每行从左边开始数的第一个\前面的内容

```
notepad++，正则模式
^[^\\]+替换成空
```

删除@后面文本

```
192.168.1.9
192.168.1.1@武昌区南湖街道南国SOHO520
192.168.1.6@洪山区南湖街道南国SOHO520
192.168.1.3@江夏区南湖街道南国SOHO520

操作：
正则表达式，然后查找目标@.*
直接点全部替换
```

提取推送日志

```
行 46451: 2023-03-07 10:57:15,549 [523] DEBUG Himall.Core.Log.Debug [(null)] - Rabbit推送-master.de-{"methodName":"member.integral.change","content":{"SerialNo":"HM_13390638","MemberId":"HM_6456300","ChangeValue":139.0,"Description":"消费获得:2023030710571081109","DocType":3,"UnitId":"ER_3852","DocNo":""},"uuid":"27253396912046080","requestMessage":"member.integral.change"}
行 46282: 2023-03-07 10:56:35,444 [523] DEBUG Himall.Core.Log.Debug [(null)] - Rabbit推送-master.de-{"methodName":"member.integral.change","content":{"SerialNo":"HM_13390637","MemberId":"ER_3307219","ChangeValue":58.0,"Description":"消费获得:2023030710563217198","DocType":3,"UnitId":"ER_2471","DocNo":""},"uuid":"27253394305613824","requestMessage":"member.integral.change"}

操作：
替换：Rabbit推送 为 &Rabbit推送
正则默认替换^[^\\]+成空
Rabbit推送-master.de-{"methodName":"member.integral.change","content":{"SerialNo":"HM_13390638","MemberId":"HM_6456300","ChangeValue":139.0,"Description":"消费获得:2023030710571081109","DocType":3,"UnitId":"ER_3852","DocNo":""},"uuid":"27253396912046080","requestMessage":"member.integral.change"}
Rabbit推送-master.de-{"methodName":"member.integral.change","content":{"SerialNo":"HM_13390637","MemberId":"ER_3307219","ChangeValue":58.0,"Description":"消费获得:2023030710563217198","DocType":3,"UnitId":"ER_2471","DocNo":""},"uuid":"27253394305613824","requestMessage":"member.integral.change"}
```