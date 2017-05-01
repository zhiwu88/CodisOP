/**
 * Tools工具对象类,静态函数，可直接调用
 */
var Tools = {
    /**
     * 获取字符串的哈希值
     * @param {String} str
     * @param {Boolean} caseSensitive
     * @return {Number} hashCode
     */
    getHashCode:function(str,caseSensitive){
        if(!caseSensitive){
            str = str.toLowerCase();
        }
        // 1315423911=b'1001110011001111100011010100111'
        var hash  =   1315423911,i,ch;
        for (i = str.length - 1; i >= 0; i--) {
            ch = str.charCodeAt(i);
            hash ^= ((hash << 5) + ch + (hash >> 2));
        }
    
        return  (hash & 0x7FFFFFFF);
    },
    //可以用于重新生成分区数据。格式为：{"partition1":{"partition2":{"partition3":{}}}}
    rebuild_pars:function(r,d){
        var tp = {};
        $.each(d,function(idx,obj){
            var len = r.length;
            if (len == 1){
                if (obj[r[0]]){
                    if (!tp[obj[r[0]]]){
                        tp[obj[r[0]]] = {}
                    }
                }
            }
            else if (len == 2){
                if (obj[r[0]]){
                    if (!tp[obj[r[0]]]){
                        tp[obj[r[0]]] = {}
                    }
                }
                if (obj[r[1]]){
                    if (!tp[obj[r[0]]][obj[r[1]]]){
                        tp[obj[r[0]]][obj[r[1]]] = {}
                    }
                }
            }
            else if (len == 3){
                if (obj[r[0]]){
                    if (!tp[obj[r[0]]]){
                        tp[obj[r[0]]] = {}
                    }
                }
                if (obj[r[1]]){
                    if (!tp[obj[r[0]]][obj[r[1]]]){
                        tp[obj[r[0]]][obj[r[1]]] = {}
                    }
                }
                if (obj[r[2]]){
                    if (!tp[obj[r[0]]][obj[r[1]]][obj[r[2]]]){
                        tp[obj[r[0]]][obj[r[1]]][obj[r[2]]] = {}
                    }
                }
            }
        })
        return tp;
    },
    //递归生成html标签
    recurse:function(data){
        var html = '<ul>';
        $.each(data,function(k,v){
            html += '<li><span class="folder">'+k+'</span>';
            html += Tools.recurse(v);
            html += '</li>';
        })
        html += '</ul>';
        return html;
    },
    //调用页面提示，弹出框
    //id=notification的modal位于base.html模板
    set_notification:function(text, never_hide, timedelay){
        $('#notification h4').html(text);
        $('#notification').modal('show');
        
        if (!never_hide){
            var delay = timedelay?timedelay:1000;
            setTimeout(function(){
                $('#notification').modal('hide');    
            },delay)
        }
    }

}

/**
 * 这个方法不是很科学，不要停顿太长时间
 * @param numberMillis 停顿的毫秒数
 */
function sleep(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while (true) {
    now = new Date();
    if (now.getTime() > exitTime)
        return;
    }
}
