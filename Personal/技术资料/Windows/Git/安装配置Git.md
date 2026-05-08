---
tags:
  - windows
  - git
---

一、生成ssh key

```
ssh-keygen -t rsa -C "panbbin@cheercare.net" -b 4096
```

二、添加pub密钥到配置里

三、联通

```
ssh -v git@gitlab.cheercare.net
```

四、配置SSH Client程序

```
C:\Program Files\Git\usr\bin\ssh.exe
```

其他方式：

```
确认你的系统是否已安装git
sudo apt-get install git

进行git配置
git config --global user.name "panbin@cheercare.net" && git config --global user.email "panbin@cheercare.net"

创建验证用的公钥
ssh-keygen -C 'panbin@cheercare.net' -t rsa


ssh -T git@cheercare.net
ssh -T git@gitlab.com
```