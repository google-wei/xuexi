import os,click
@click.command()
@click.option('--c',default=1,prompt='--c Choose Openstack Manager [1]flavor manager [2]server manager [3]image manager',help='Choose number')
@click.option('--a',prompt='action name',help='input your choose number')

def openstackcloud(c,a):
    if c == 1:
        click.echo("openstack flavor %s" %a)
        cmd = "openstack flavor " + a
        os.system(cmd)
    if c == 2:
        click.echo("openstack server %s" %a)
        cmd = "openstack server " + a
        os.system(cmd)

    if c == 3:
        click.echo("openstack image %s" %a)
        cmd = "openstack image " + a
        os.system(cmd)

if __name__ == "__main__":
    openstackcloud()


#使用Python语言，基于Python click框架，对接云主机类型管理、云主机管理、镜像管理的程序，实现自定义的命令行管理工具，命令同openstack命令保持一致，并完成单元测试python代码编写，完成后提交实现代码文件。
######################## Respone  #################################3
python3 manager_openstack.py --c 1 --a list
openstack flavor list
+------+-------------+------+------+-----------+-------+-----------+
| ID   | Name        |  RAM | Disk | Ephemeral | VCPUs | Is Public |
+------+-------------+------+------+-----------+-------+-----------+
| 1    | m1.tiny     |  512 |   10 |         0 |     1 | True      |
| 2    | m1.small    | 1024 |   20 |         0 |     1 | True      |
| 3    | m1.medium   | 2048 |   40 |         0 |     2 | True      |
| 9999 | nova-flavor | 1024 |   10 |         0 |     2 | True      |
+------+-------------+------+------+-----------+-------+-----------+
