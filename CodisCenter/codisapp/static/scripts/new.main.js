var codisControllers = angular.module("codisControllers", ["ui.bootstrap", "ngResource", "highcharts-ng"]);
var dashboardip= document.getElementById("ip").value;
codisControllers.config(["$interpolateProvider", function (a) {
    a.startSymbol("[["), a.endSymbol("]]")
}]), codisControllers.config(["$httpProvider", function (a) {
    a.defaults.useXDomain = !0, delete a.defaults.headers.common["X-Requested-With"]
}]), codisControllers.factory("ServerGroupsFactory", ["$resource", function (a) {
    return a("/api/server_groups/" + dashboardip + "/", {}, {query: {method: "GET", isArray: !0}, create: {method: "PUT"}})
}]), codisControllers.factory("ProxyStatusFactory", ["$resource", function (a) {
    return a("/api/proxy/" + dashboardip + "/", {}, {
        query: {method: "GET", url: "/api/proxy/list/" + dashboardip + "/", isArray: !0},
        setStatus: {method: "POST"}
    })
}]), codisControllers.factory("RedisStatusFactory", ["$resource", function (a) {
    return a("/api/redis/" + dashboardip + "/", {}, {
        stat: {method: "GET", url: "/api/redis/:addr/stat/" + dashboardip + "/"},
        slotInfoByGroupId: {method: "GET", url: "/api/redis/group/:group_id/:slot_id/slotinfo/" + dashboardip + "/"}
    })
}]), codisControllers.factory("MigrateStatusFactory", ["$resource", function (a) {
    return a("/api/migrate/status/" + dashboardip + "/", {}, {
        tasks: {method: "GET", url: "/api/migrate/tasks/" + dashboardip + "/", isArray: !0},
        doMigrate: {method: "POST", url: "/api/migrate/" + dashboardip + "/"},
        doRebalance: {method: "POST", url: "/api/rebalance/" + dashboardip + "/"}
    })
}]), codisControllers.factory("SlotFactory", ["$resource", function (a) {
    return a("/api/slot/" + dashboardip + "/", {}, {rangeSet: {method: "POST"}})
}]), codisControllers.factory("ServerGroupFactory", ["$resource", function (a) {
    return a("/api/server_group/:id/" + dashboardip + "/", {}, {
        show: {method: "GET", isArray: !0},
        "delete": {method: "DELETE", params: {id: "@id"}},
        addServer: {method: "PUT", url: "/api/server_group/:id/addServer/" + dashboardip + "/", params: {id: "@group_id"}},
        deleteServer: {method: "PUT", url: "/api/server_group/:id/removeServer/" + dashboardip + "/", params: {id: "@group_id"}},
        promote: {method: "POST", url: "/api/server_group/:id/promote/" + dashboardip + "/", params: {id: "@group_id"}}
    })
}]), codisControllers.controller("codisProxyCtl", ["$scope", "$http", "ProxyStatusFactory", "$timeout", function (a, b, c, d) {
    a.proxies = c.query(), a.setStatus = function (b, d) {
        var e = "";
        e = "online" == d ? "Do you want to set " + b.id + " online?" : "Do you want to mark " + b.id + " offline? the proxy process will exit after you marked it offline";
        var f = confirm(e);
        f && (b.state = d, c.setStatus(b, function () {
            a.proxies = c.query()
        }, function (a) {
            b.state = "offline", alert(a.data)
        }))
    }, a.refresh = function () {
        a.proxies = c.query()
    }, a.refresh(), function e() {
        d(e, 1e4), a.refresh()
    }()
}]), codisControllers.controller("codisOverviewCtl", ["$scope", "$http", "$timeout", function (a, b, c) {
    Highcharts.setOptions({global: {useUTC: !1}});
    var d = function (b) {
        var c = a.chartOps.series[0].data;
        c.length > 20 && c.shift(), c.push({x: new Date, y: b}), a.chartOps.series[0].data = c
    };
    a.refresh = function () {
        b.get("/api/overview/" + dashboardip + "/").success(function (b) {
            var c = 0, e = 0, rss = 0, f = b.redis_infos;
            for (var g in f) {
                var h = f[g];
                for (var i in h) {
                    0 == i.indexOf("db") && (c += parseInt(h[i].match(/keys=(\d+)/)[1]));
                    "used_memory" == i && (e += parseInt(h[i]));
                    "used_memory_rss" == i && (rss += parseInt(h[i]));
                }
            }
            a.memUsed = (e / 1048576).toFixed(2);
            a.rss = (rss / 1048576).toFixed(2);
            a.keys = c;
            a.product = b.product;
            void 0 !== b.opsps && b.opsps >= 0 ? a.opsps = b.opsps : a.opsps = 0;
            d(a.opsps);
            a.maxmemory = b.maxmemory;
            a.role = b.role;
            a.zk = b.zk;
            a.backend_ping_period = b.backend_ping_period;
            a.session_max_timeout = b.session_max_timeout;
            a.session_max_bufsize = (parseInt(b.session_max_bufsize) / 1024).toFixed(2) + "KB";
            a.session_max_pipeline = b.session_max_pipeline;
            a.zk_session_timeout = b.zk_session_timeout;
            a.dashboard = b.dashboard;
            a.idc = b.idc;
            a.dashboardSize = b.dashboardSize;
            a.action_count = b.action_count;
            a.slotnum = b.slotnum;

            a.bigreqsize = b.bigreqsize;
            a.recordtype = b.recordtype;
            a.enablesafepromotion = b.enablesafepromotion;
            a.safepromotionmaxblockingms = b.safepromotionmaxblockingms;
            a.prefixwhitelist = b.prefixwhitelist;
            a.ipwhitelist = b.ipwhitelist;
            a.activitymigr = b.activitymigr;
        })
    }, a.refresh(), a.chartOps = {
        chart: {useUTC: !1, type: "spline"},
        series: [{name: "OP/s", data: []}],
        title: {text: "OP/s"},
        xAxis: {type: "datetime", title: {text: "Time"}},
        yAxis: {title: {text: "value"}}
    }, function e() {
        c(e, 1e3), a.refresh()
    }()
}]), codisControllers.controller("codisHaCtl", ["$scope", "$http", "$timeout", function (a, b, c) {
    a.refresh = function () {
        b.get("/api/hastatus/" + dashboardip + "/").success(function (b) {
            a.globalMaxParallelRepl = b.globalMaxParallelRepl;
            a.localMaxParallelRepl = b.localMaxParallelRepl;
            a.globalCurrParallelRepl = b.globalCurrParallelRepl;
            a.localCurrParallelRepl = b.localCurrParallelRepl;
            a.gRepl = b.gRepl;
            a.lRepl = b.lRepl;
            a.product = b.product;
            a.haStatus = b.haStatus;
        })
    }, a.refresh(), function e() {
        c(e, 1e3), a.refresh()
    }()
}]), codisControllers.controller("codisSlotCtl", ["$scope", "$http", "$modal", "SlotFactory", function (a, b, c, d) {
    a.rangeSet = function () {
        var a = c.open({
            templateUrl: "slotRangeSetModal", controller: ["$scope", "$modalInstance", function (a, b) {
                a.task = {from: "-1", to: "-1", new_group: "-1"}, a.ok = function (a) {
                    b.close(a)
                }, a.cancel = function () {
                    b.close(null)
                }
            }], size: "sm"
        });
        a.result.then(function (a) {
            a && (console.log(a), d.rangeSet(a, function () {
                alert("success")
            }, function (a) {
                alert(a.data)
            }))
        })
    }
}]), codisControllers.controller("codisMigrateCtl", ["$scope", "$http", "$modal", "MigrateStatusFactory", "$timeout", function (a, b, c, d, e) {
    a.migrate_tasks = d.tasks(), a.migrate = function () {
        var b = c.open({
            templateUrl: "migrateModal", controller: ["$scope", "$modalInstance", function (a, b) {
                a.task = {from: "-1", to: "-1", new_group: "-1", delay: 0}, a.ok = function (a) {
                    b.close(a)
                }, a.cancel = function () {
                    b.close(null)
                }
            }], size: "sm"
        });
        b.result.then(function (b) {
            b && d.doMigrate(b, function () {
                a.refresh()
            }, function (a) {
                alert(a.data)
            })
        })
    }, a.rebalance = function () {
        d.doRebalance(function () {
            a.refresh()
        }, function (a) {
            alert(a.data)
        })
    }, a.refresh = function () {
        a.migrate_tasks = d.tasks()
    }, function f() {
        e(f, 1e4), a.refresh()
    }()
}]), codisControllers.controller("redisCtl", ["$scope", "RedisStatusFactory", function (a, b) {
    a.slaves = {};
    var t = b.stat(a.server);
    t.$promise.then(function (data) {
        a.serverInfo = data;
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                if (/^slave(\d+)$/.test(key)) {
                    a.slaves[key] = data[key];
                }
            }
        }
    });
}]), codisControllers.controller("slotInfoCtl", ["$scope", "RedisStatusFactory", function (a, b) {
    a.slotInfo = b.slotInfoByGroupId({slot_id: a.slot.id, group_id: a.slot.state.migrate_status.from})
}]), codisControllers.controller("codisServerGroupMainCtl", ["$scope", "$http", "$modal", "$log", "ServerGroupsFactory", "ServerGroupFactory", "$timeout", function (a, b, c, d, e, f, g) {
    a.removeServer = function (b) {
        var c = confirm("are you sure to remove " + b.addr + " from group_" + b.group_id + "?");
        c && f.deleteServer(b, function (b) {
            a.server_groups = e.query()
        }, function (a) {
            console.log(a.data), alert(a.data)
        })
    }, a.promoteServer = function (b) {
        f.promote(b, function (b) {
            a.server_groups = e.query()
        }, function (a) {
            alert(a.data)
        })
    }, a.removeServerGroup = function (b) {
        var c = confirm("are you sure to remove group_" + b + " ?");
        c && f["delete"]({id: b}, function () {
            a.server_groups = e.query()
        }, function () {
            alert(failedData.data)
        })
    }, a.addServer = function (b) {
        var d = c.open({
            templateUrl: "addServerToGroupModal", controller: ["$scope", "$modalInstance", function (a, c) {
                a.server = {addr: "", type: "slave", group_id: b}, a.ok = function (a) {
                    c.close(a)
                }, a.cancel = function () {
                    c.close(null)
                }
            }], size: "sm"
        });
        d.result.then(function (b) {
            b && f.addServer(b, function (b) {
                a.server_groups = e.query()
            }, function (a) {
                alert(a.data)
            })
        })
    }, a.addServerGroup = function () {
        var b = c.open({
            templateUrl: "newServerGroupModal", controller: ["$scope", "$modalInstance", function (a, b) {
                a.ok = function (a) {
                    b.close(a)
                }, a.cancel = function () {
                    b.close(null)
                }
            }], size: "sm"
        });
        b.result.then(function (b) {
            b && e.create(b, function (b) {
                a.server_groups = e.query()
            }, function (a) {
                alert(a.data)
            })
        })
    }, a.refresh = function () {
        a.server_groups = e.query()
    }, a.refresh();
    // , function h() {
    //     g(h, 1000*60*10), a.refresh()
    // }()
}]);
