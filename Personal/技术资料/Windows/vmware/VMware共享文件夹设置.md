---
tags:
  - vmware
  - windows
  - 虚拟机
  - 共享文件夹
---

通过VMware共享文件夹功能实现Windows 10与Ubuntu虚拟机中的Obsidian知识库同步。

### 一、准备阶段
1. **确认环境**
    - VMware版本：确保使用VMware Workstation/Player（支持共享文件夹功能）。
    - 网络模式：虚拟机网络设置为**NAT**或**桥接模式**（确保网络连通性）。
    - 文件权限：Ubuntu用户需有共享文件夹的读写权限。

2. **安装依赖工具**
    - 在Ubuntu中安装VMware Tools（或open-vm-tools）：
        ```bash
        sudo apt update
        sudo apt install open-vm-tools-desktop -y  # 桌面版推荐
        # 或通过VMware菜单安装：虚拟机 → 安装VMware Tools
        ```
### 二、配置共享文件夹（两种方案任选其一）

#### **方案A：VMware原生共享文件夹（推荐）**

1. **设置共享文件夹**
    - 在VMware中右键虚拟机 → **设置** → **选项** → **共享文件夹**。
    - 启用共享文件夹，添加Windows路径（如E:\ObsidianVault`），勾选**启用此共享**和**只读模式（可选）**。

2. **挂载到Ubuntu**
    - 启动Ubuntu，创建挂载点：
        ```bash
        sudo mkdir /mnt/obsidian_share
        ```
    - 挂载共享文件夹（永久生效需编辑`/etc/fstab`）：
        ```bash
        sudo mount -t vmhgfs -o allow_other,uid=1000,gid=1000 .host:/ObsidianVault /mnt/obsidian_share
        ```
     - uid/gid`替换为你的Ubuntu用户ID（通过`id -u`和`id -g`查看）。

3. **自动挂载（可选）**
    - 编辑`/etc/fstab`，添加以下行：
        ```bash
        .host:/ObsidianVault /mnt/obsidian_share vmhgfs defaults,allow_other,uid=1000,gid=1000 0 0
        ```

### 三、测试验证

1. 确认共享文件夹是否已自动挂载
运行以下命令，检查 `/mnt/hgfs/` 下是否存在 `ObsidianVault` 文件夹：

```bash
ls /mnt/hgfs/
```
如果能看到 `ObsidianVault`，说明 VMware Tools 已自动挂载共享文件夹，无需额外操作。

2. 检查挂载权限

即使共享文件夹已挂载，仍需确保 Ubuntu 用户有读写权限：

```bash
ls -ld /mnt/hgfs/ObsidianVault
```
- 如果权限不足（如显示 `drwxr-xr-x 1 root root`），需修改权限：
    
    ```bash
    sudo chown -R $USER:$USER /mnt/hgfs/ObsidianVault  # 将 $USER 替换为你的用户名
    sudo chmod -R 755 /mnt/hgfs/ObsidianVault          # 可选：调整权限为读写执行
    ```

3. 测试读写功能

在 Ubuntu 中创建/修改文件，验证是否同步到 Windows：

```bash
echo "Test sync" > /mnt/hgfs/ObsidianVault/test.txt
```
然后在 Windows 的共享文件夹中检查是否出现 `test.txt`。

### **四、推荐优化：创建符号链接（可选）**

如果希望直接在用户目录下访问共享文件夹，可以创建符号链接：

1️⃣ **删除旧符号链接**

```bash
bash# 先确认旧符号链接的准确路径（大小写敏感！）
ls -l ~/ObsidianVault

# 执行删除（符号链接直接当文件删除，不会影响源目录）
rm -f ~/ObsidianVault  # 强制删除，忽略不存在警告
```

2️⃣ **创建小写符号链接**
```bash
# 创建指向原共享文件夹的小写符号链接
ln -s /mnt/hgfs/ObsidianVault /home/obsidian_vault  # 注意源路径大小写保持原样！

# 验证符号链接是否正确
ls -l /home/obsidian_vault  # 应显示指向 /mnt/hgfs/ObsidianVault
```
之后可直接通过 `~/ObsidianVault` 访问知识库。
