#-*- coding:utf8 -*
import redis
import time

TIME_THRESHOLD_SECOND = 2592000  # 获取idletime时长超过TIME_THRESHOLD_SEC秒数键打印. 默认:30天
COUNT = 200  #scan每次返回的键个数,建议不要太大，避免O(n)的n过大出现慢查询. 默认:200个
YEILD_SECOND = 0.05 #每次scan后，sleep 0.05秒；本地测试如果不sleep，此工具会增加约2w的QPS. 避免对高负载的Redis实例产生影响。
            #默认:0.05秒，增长约3500个QPS,其中一个时间复杂度是O(COUNT). 如果实例负载高，key不多可以考虑sleep 0.1秒
def get_key_idletime():
    r = redis.Redis('127.0.0.1', '6000')
    cursor = '0'
    while cursor != 0:
        cursor, data = r.scan(cursor=cursor, count=COUNT)
        for key in data:
            key_idletime = r.object("idletime",key)
        if key_idletime > TIME_THRESHOLD_SECOND:
            print key , " ", key_idletime
        time.sleep(YEILD_SECOND)
get_key_idletime()
