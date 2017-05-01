<h2>一、OPTools</h2>
<ol>
<li><h4>ScanMultiPrefixKey.py</h4></li>
<p>同时搜索多个前缀的key：</p>
<p>用于查询Codis集群是否存在某个前缀的key。</p>
<p>使用方法：</p>
<pre><code>修改代码中 groupsurl 变量和 key.startswith()
执行
$ python ScanMultiPrefixKey.py</code></pre>
<br/>

<li><h4>ScanMultiPrefixKey2f.py</h4></li>
<p>同时搜索多个前缀的key，并写入到 ScanMultiPrefixKey2f.txt 文件中：</p>
<p>用于查询Codis集群是否存在某个前缀的key，并输出到文本文件中。</p>
<p>使用方法：</p>
<pre><code>修改代码中 groupsurl 变量和 key.startswith()
执行
$ python ScanMultiPrefixKey.py</code></pre>
<br/>

<li><h4>crc32.py</h4></li>
<p>查询key名所在slot：</p>
<p>用于key名所在slot，然后可通过slot编号到Dashboard查询到Group_ID</p>
<p>使用方法：</p>
<pre><code>加入别名到.bashrc
alias crc32='python /home/work/crc32.py'
执行
$ crc32 keyname
slotNo=556</code></pre>
<br/>

<li><h4>codis_mem.sh</h4></li>
<p>一键修改Redis maxmemory：</p>
<p>用于修改Codis集群中所有Redis的maxmemory，数字单位是GB。</p>
<p>使用方法：</p>
<pre><code>加入别名到.bashrc
alias codismem='sh /home/work/CodisInstaller/tools/codis_mem.sh'
执行
$ codismem friend 15
</code></pre>
<br/>

<li><h4>ClusterManager.py</h4></li>
<p>提供 cml 命令和 cm 命令的脚本，用于管理现有的集群机器列表，读写 ClusterManager.db 数据库。</p>
<p>使用方法：</p>
<p>写入别名到环境变量.bashrc文件中，然后使用 cml和 cm 命令。</p>
<pre><code>alias cm='python /home/work/CodisInstaller/tools/ClusterManager/ClusterManager.py'
alias cml='python /home/work/CodisInstaller/tools/ClusterManager/ClusterManager.py list'
</code></pre>
<br/>

</ol>


<h2>二、CodisInstall</h2>
<ol>

<li><h4>createCodis_8x.py</h4></li>
<p>一键创建Codis集群（老版本）：</p>
<p>用于晓月机房2台机器，亦庄机房1台机器的环境下，机器数量2:1。<br/>
在晓月创建600x和700x端口的实例，在亦庄创建80xx端口的实例。</p>
<p>使用方法：</p>
<pre><code>python2.7 createCodis.py userfriend 10.x.x.1,10.x.x.2 100.y.y.32,100.y.y.33</code></pre>
<br/>

<li><h4>createCodis.py</h4></li>
<p>一键创建Codis集群：</p>
<p>用于晓月机房2台机器，亦庄机房2台机器的环境下，机器数量1:1。<br/>
在晓月和亦庄机房都是创建600x和700x端口的实例。</p>
<p>使用方法：</p>
<pre><code>python2.7 createCodis.py userfriend 10.x.x.1,10.x.x.2 100.y.y.32,100.y.y.33</code></pre>
<br/>

</ol>


<h2>三、OPTools_Danger</h2>
<ol>

<li><h4>startAll.sh</h4></li>
<p>启动多个集群的Redis/Dashboard/Proxy：</p>
<p>用于多个集群Redis/Dashboard/Proxy都停掉的情况下启动这些集群的进程。</p>
<p>使用方法：</p>
<pre><code>修改 productList 变量，
执行
$ ./startAll.sh
</code></pre>
<br/>

<li><h4>stopAll.sh</h4></li>
<p>停止多个集群的HA/Redis/Dashboard/Proxy：</p>
<p>用于需要停止多个集群所有HA/Redis/Dashboard/Proxy都停掉的情况下启动这些进程。</p>
<p>使用方法：</p>
<pre><code>修改 productList 变量，
执行
$ ./stopAll.sh
</code></pre>
<br/>

<li><h4>startha.sh</h4></li>
<p>启动多个集群的HA：</p>
<p>用于多个集群HA都停掉的情况下启动这些集群的HA进程。</p>
<p>使用方法：</p>
<pre><code>修改 productList 变量，
执行
$ ./startha.sh
</code></pre>
<br/>

</ol>


<h2>四、SwitchIDC</h2>
<ol>

<li><h4>qiejifang.py</h4></li>
<p>生成提主脚本的Python脚本：</p>
<p>可以单独使用生成提主脚本，也可以在Yz.sh上调用。</p>
<p>使用方法：</p>
<pre><code>执行
$ python qiejifang.py codisName dashboardIP
</code></pre>
<br/>

<li><h4>restartYzProxy.sh</h4></li>
<p>用于单独重启Codis集群Proxy：</p>
<p>可以单独用于重启集群Proxy，也可以在Yz.sh/Xy.sh上调用。</p>
<p>使用方法：</p>
<pre><code>执行
$ sh restartYzProxy.sh codisName
</code></pre>
<br/>

<li><h4>restartYzProxy.sh</h4></li>
<p>用于单独重启Codis集群Proxy：</p>
<p>可以单独用于重启集群Proxy，也可以在Yz.sh/Xy.sh上调用。</p>
<p>使用方法：</p>
<pre><code>执行
$ sh restartYzProxy.sh codisName
</code></pre>
<br/>

<li><h4>bgrewrite.sh</h4></li>
<p>用于直接对 晓月600x Redis操作BGREWRITEAOF做AOF重写，及备份。</p>
<p>使用方法：</p>
<pre><code>执行
$ sh bgrewrite.sh codisName
</code></pre>
<br/>

<li><h4>Yz.sh</h4></li>
<p>用于把Codis切换到亦庄：</p>
<p>调用qiejifang.py生成机房切换脚本，上传到第1台机器，并执行脚本修改亦庄为读写机房，提升亦庄600x Redis为主，重启Proxy。</p>
<p>使用方法：</p>
<pre><code>执行
$ sh Yz.sh codisName
</code></pre>
<br/>

<li><h4>Xy.sh</h4></li>
<p>用于把Codis切回到晓月：</p>
<p>执行之前生成切已上传的回切晓月脚本，修改晓月为读写机房，提升晓月600x Redis为主，重启Proxy。</p>
<p>使用方法：</p>
<pre><code>执行
$ sh Xy.sh codisName
</code></pre>
<br/>

</ol>


<h2>五、SwitchZK</h2>
<ol>

<li><h4>YZZK_Switch.py</h4></li>
<p>亦庄ZK提主脚本：</p>
<p>当晓月ZK超过2个节点故障时，需要切换为亦庄ZK。该脚本修改亦庄ZK配置，去掉peerType和observer配置，以及注释晓月ZK配置。</p>
<br/>
<p>使用方法：</p>
<pre><code>修改脚本内 yz_zk_list 列表为亦庄ZK主机地址。
执行，并按照提示操作输入 yes/no 进行确认操作。
$ python YZZK_Switch.py
</code></pre>
<br/>

<li><h4>Modify_Codis_ZK.py</h4></li>
<p>Codis集群Dashboard和Proxy的ZK配置修改脚本：</p>
<p>当晓月ZK超过2个节点故障时，需要切换为亦庄ZK。使用 YZZK_Switch.py 切换亦庄ZK后，可能需要将晓月的Codis集群中Dashboard和Proxy的ZK配置修改为亦庄ZK。该脚本用于修改Dashboard和Proxy的ZK配置。</p>
<br/>
<p>使用方法：</p>
<pre><code>修改为亦庄ZK时，修改脚本内 zklist_yz  列表为亦庄ZK主机地址。
修改回晓月ZK时，修改脚本内 zklist_xy  列表为晓月ZK主机地址。
修改同目录的 hostlist 文件，加入需要操作的Codis集群IP地址。
执行，并按照提示操作输入 yes/no 进行确认操作。
$ python Modify_Codis_ZK.py
</code></pre>
<br/>

</ol>


<h2>六、YumRepoInstall</h2>
<ol>

<li><h4>YUM_REPO_INSTALL.py</h4></li>
<p>安装YUM仓库脚本：</p>
<p>该脚本将 /etc/yum.repos.d/*.repo 备份，并根据机房选择下载 repo 仓库配置文件，然后执行 yum makecache 操作。</p>
<p>使用方法：</p>
<pre><code>修改同目录的 hostlist 文件，加入需要操作的服务器IP地址。
执行
$ python YUM_REPO_INSTALL.py
</code></pre>
<br/>


</ol>


<h2>七、RepairVulner</h2>
<ol>

<li><h4>Repair_Vulner.py</h4></li>
<p>系统漏洞检查与修复脚本：</p>
<p>按照提示检查Shellshock漏洞和Heartbleed漏洞，也可以根据提示选择漏洞修复操作。修复操作需要在YUM能用的前提下执行。</p>
<p>使用方法：</p>
<pre><code>修改同目录的 hostlist 文件，加入需要操作的服务器IP地址。
执行
$ python Repair_Vulner.py
</code></pre>
<br/>


</ol>


