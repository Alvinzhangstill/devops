云计算



nginx命令：



curl 命令：发起http网络请求，并且验证对方网站的信息。

curl -I：只取服务器相关信息；



1、修改nginx的首页：

查看nginx的安装文件，路径信息：

```sh
rpm -ql nginx
```



~~~
基础设施监控：
服务器温度，风扇转速  ipmitool命令，只能用在物理机
存储的监控（df,fdisk,iotop）
cpu监控（lscpu,uptime,top,htop,glances）
内存情况（free）
网络情况（iftop）


应用监控:
mysql  redis
nginx



~~~



监控：

~~~
硬件监控：
（1）通过远程控制卡：Dell的iDRAC，HP 的ILO和IBM 的 IMM等
（2）使用IPMI来完成物理设备的监控工作，通常必须要监控的就是温度、硬盘故障等
（3）路由器，交换机（端口，光衰，日志）打印机，Windows等
~~~

~~~
系统监控：
CPU，内存，硬盘使用率，硬盘IO，系统负载，进程数
~~~

~~~
服务监控：
Apache，nginx，php-fpm，mysql，memcache，redis，tomcat，JVM，TCP连接数
~~~

~~~
性能监控：
网站性能，服务器性能，数据库性能，存储性能
~~~

~~~
日志监控：
系统会产生系统日志，应用程序会有应用的访问日志，错误日志，服务有运行日志等，可以使用ELK来进行日志监控
~~~

~~~
安全监控：
（1）Nginx+lua编写了一个WAF通过kibana可以图形化的展示不同的攻击类型的统计
（2）用户登陆数，passwd文件变化，本地所有文件改动
~~~

~~~
网络监控：
端口，web（URL），DB，ping包，IDC带宽网络流量，网络流出速率，网络入流量，网络出流量，网络使用率，SMTP，POP3
~~~



多节点服务器：







查找文件：

~~~
[root@localhost tmp]# find / -name mysql
/etc/selinux/targeted/active/modules/100/mysql
/usr/bin/mysql
/usr/lib64/mysql
/usr/share/mysql

~~~



