
# 在线安装(所有节点)
ubuntu
```shell
apt update
apt install -y nfs-kernel-server
apt install -y nfs-common
```
centos
```shell
yum install -y nfs-utils rpcbind

```
# 离线安装

### ubuntu使用deb包方式安装(所有节点)

查看自己版本的包https://mirrors.tuna.tsinghua.edu.cn/ubuntu/pool/main/n/nfs-utils/
下载nfs-common、nfs-kernel-server

```shell
dpkg -i nfs-common

dpkg -i nfs-kernel-server
```

### centos使用rpm包方式安装(所有节点)

```shell
wget https://docker-76009.sz.gfp.tencent-cloud.com/github/cube-studio/deploy/nfs/nfsrpm.tar.gz
tar -zxvf nfsrpm.tar.gz
cd nfs
rpm -ivh *.rpm --force --nodeps
```

# nfs server配置

```shell

# 修改配置文件，增加下面这一行数据，指定的ip地址为客户端的地址
# /data/nfs/ 代表nfs server本地存储目录
mkdir -p /data/nfs
echo "/data/nfs/ *(rw,no_root_squash,async)" >> /etc/exports

# 加载配置文件
exportfs -arv
systemctl enable rpcbind.service 
systemctl enable nfs-server.service
systemctl start rpcbind.service
systemctl start nfs-server.service

#验证
[root@nfs ~]# showmount -e localhost
Export list for localhost:
/data/nfs   *
```

server端可以软链到/data/k8s目录
```bash
mkdir -p /data/nfs/k8s
ln -s /data/nfs/k8s /data/
```

### nfs client配置

```shell
export server=10.101.135.101

#查看nfs server 信息

showmount -e $server

结果
Export list for xx.xx.xx.xx:
/data/nfs      *
 
# 系统层面添加挂载添加一行，重启自动添加
mkdir -p /data/nfs
echo "${server}:/data/nfs  /data/nfs   nfs   defaults  0  0" >> /etc/fstab

mount -a 

# 或者使用命令行,如果是一台机器记得不要是同一个地址
mount -t nfs $server:/data/nfs /data/nfs

#验证
df -h |grep nfs

# 软链到cube studio的目录
mkdir -p /data/nfs/k8s
ln -s /data/nfs/k8s /data/

#输出 表示挂载成功
[root@node02 ~]# df -h /data/nfs/
Filesystem                Size  Used Avail Use% Mounted on
172.16.101.13:/data/nfs  3.5T  626M  3.5T   1% /data/nfs

```

