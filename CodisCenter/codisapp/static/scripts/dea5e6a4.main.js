var codisControllers = angular.module("codisControllers", ["ui.bootstrap", "ngResource", "highcharts-ng"]);
var dashboardip= document.getElementById("ip").value;
codisControllers.config(["$interpolateProvider",
function(a) {
    a.startSymbol("[["),
    a.endSymbol("]]")
}]),
codisControllers.config(["$httpProvider",
function(a) {
    a.defaults.useXDomain = !0,
    delete a.defaults.headers.common["X-Requested-With"]
}]),
codisControllers.factory("ServerGroupsFactory", ["$resource",
function(a) {
    return a("/api/server_groups/" + dashboardip + "/", {},
    {
        query: {
            method: "GET",
            isArray: !0
        },
        create: {
            method: "PUT"
        }
    })
}]),
codisControllers.factory("ProxyStatusFactory", ["$resource",
function(a) {
    return a("/api/proxy/" + dashboardip + "/", {},
    {
        query: {
            method: "GET",
            url: "/api/proxy/list/" + dashboardip + "/",
            isArray: !0
        },
        setStatus: {
            method: "POST"
        }
    })
}]),
codisControllers.factory("RedisStatusFactory", ["$resource",
function(a) {
    return a("/api/redis/" + dashboardip + "/", {},
    {
        stat: {
            method: "GET",
            url: "/api/redis/:addr/stat/" + dashboardip + "/"
        },
        slotInfoByGroupId: {
            method: "GET",
            url: "/api/redis/group/:group_id/:slot_id/slotinfo/" + dashboardip + "/"
        }
    })
}]),
codisControllers.factory("MigrateStatusFactory", ["$resource",
function(a) {
    return a("/api/migrate/status/" + dashboardip + "/", {},
    {
        tasks: {
            method: "GET",
            url: "/api/migrate/tasks/" + dashboardip + "/",
            isArray: !0
        },
        doMigrate: {
            method: "POST",
            url: "/api/migrate/" + dashboardip + "/"
        },
        doRebalance: {
            method: "POST",
            url: "/api/rebalance/" + dashboardip + "/"
        }
    })
}]),
codisControllers.factory("SlotFactory", ["$resource",
function(a) {
    return a("/api/slot/" + dashboardip + "/", {},
    {
        rangeSet: {
            method: "POST"
        }
    })
}]),
codisControllers.factory("ServerGroupFactory", ["$resource",
function(a) {
    return a("/api/server_group/:id/" + dashboardip + "/", {},
    {
        show: {
            method: "GET",
            isArray: !0
        },
        "delete": {
            method: "DELETE",
            params: {
                id: "@id"
            }
        },
        addServer: {
            method: "PUT",
            url: "/api/server_group/:id/addServer/" + dashboardip + "/",
            params: {
                id: "@group_id"
            }
        },
        deleteServer: {
            method: "PUT",
            url: "/api/server_group/:id/removeServer/" + dashboardip + "/",
            params: {
                id: "@group_id"
            }
        },
        promote: {
            method: "POST",
            url: "/api/server_group/:id/promote/" + dashboardip + "/",
            params: {
                id: "@group_id"
            }
        }
    })
}]),
codisControllers.controller("codisProxyCtl", ["$scope", "$http", "ProxyStatusFactory",
function(a, b, c) {
    a.proxies = c.query(),
    a.setStatus = function(b, d) {
        var e = "";
        e = "online" == d ? "Do you want to set " + b.id + " online?": "Do you want to mark " + b.id + " offline? the proxy process will exit after you marked it offline";
        var f = confirm(e);
        f && (b.state = d, c.setStatus(b,
        function() {
            a.proxies = c.query()
        },
        function(a) {
            b.state = "offline",
            alert(a.data)
        }))
    },
    a.refresh = function() {
        a.proxies = c.query()
    }
}]),
codisControllers.controller("codisOverviewCtl", ["$scope", "$http", "$timeout",
function(a, b, c) {
    Highcharts.setOptions({
        global: {
            useUTC: !1
        }
    });
    var d = function(b) {
        var c = a.chartOps.series[0].data;
        c.length > 20 && c.shift(),
        c.push({
            x: new Date,
            y: b
        }),
        a.chartOps.series[0].data = c
    };
    a.refresh = function() {
        b.get("/api/overview/" + dashboardip + "/").success(function(b) {
            var c = 0,
            e = 0,
            f = b.redis_infos;
            for (var g in f) {
                var h = f[g];
                for (var i in h) 0 == i.indexOf("db") && (c += parseInt(h[i].match(/keys=(\d+)/)[1])),
                "used_memory" == i && (e += parseInt(h[i]))
            }
            a.memUsed = (e / 1048576).toFixed(2),
            a.keys = c,
            a.product = b.product,
            void 0 !== b.ops && b.ops >= 0 ? a.ops = b.ops: a.ops = 0,
            d(a.ops)
        })
    },
    a.refresh(),
    a.chartOps = {
        chart: {
            useUTC: !1,
            type: "spline"
        },
        series: [{
            name: "OP/s",
            data: []
        }],
        title: {
            text: "OP/s"
        },
        xAxis: {
            type: "datetime",
            title: {
                text: "Time"
            }
        },
        yAxis: {
            title: {
                text: "value"
            }
        }
    },
    function e() {
        c(e, 1e3),
        a.refresh()
    } ()
}]),
codisControllers.controller("codisSlotCtl", ["$scope", "$http", "$modal", "SlotFactory",
function(a, b, c, d) {
    a.rangeSet = function() {
        var a = c.open({
            templateUrl: "slotRangeSetModal",
            controller: ["$scope", "$modalInstance",
            function(a, b) {
                a.task = {
                    from: "-1",
                    to: "-1",
                    new_group: "-1"
                },
                a.ok = function(a) {
                    b.close(a)
                },
                a.cancel = function() {
                    b.close(null)
                }
            }],
            size: "sm"
        });
        a.result.then(function(a) {
            a && (console.log(a), d.rangeSet(a,
            function() {
                alert("success")
            },
            function(a) {
                alert(a.data)
            }))
        })
    }
}]),
codisControllers.controller("codisMigrateCtl", ["$scope", "$http", "$modal", "MigrateStatusFactory", "$timeout",
function(a, b, c, d, e) {
    a.migrate_tasks = d.tasks(),
    a.migrate = function() {
        var b = c.open({
            templateUrl: "migrateModal",
            controller: ["$scope", "$modalInstance",
            function(a, b) {
                a.task = {
                    from: "-1",
                    to: "-1",
                    new_group: "-1",
                    delay: 0
                },
                a.ok = function(a) {
                    b.close(a)
                },
                a.cancel = function() {
                    b.close(null)
                }
            }],
            size: "sm"
        });
        b.result.then(function(b) {
            b && d.doMigrate(b,
            function() {
                a.refresh()
            },
            function(a) {
                alert(a.data)
            })
        })
    },
    a.rebalance = function() {
        d.doRebalance(function() {
            a.refresh()
        },
        function(a) {
            alert(a.data)
        })
    },
    a.refresh = function() {
        a.migrate_tasks = d.tasks()
    },
    function f() {
        e(f, 1e4),
        a.refresh()
    } ()
}]),
codisControllers.controller("redisCtl", ["$scope", "RedisStatusFactory",
function(a, b) {
    a.serverInfo = b.stat(a.server)
}]),
codisControllers.controller("slotInfoCtl", ["$scope", "RedisStatusFactory",
function(a, b) {
    a.slotInfo = b.slotInfoByGroupId({
        slot_id: a.slot.id,
        group_id: a.slot.state.migrate_status.from
    })
}]),
codisControllers.controller("codisServerGroupMainCtl", ["$scope", "$http", "$modal", "$log", "ServerGroupsFactory", "ServerGroupFactory",
function(a, b, c, d, e, f) {
    a.removeServer = function(b) {
        var c = confirm("are you sure to remove " + b.addr + " from group_" + b.group_id + "?");
        c && f.deleteServer(b,
        function(b) {
            a.server_groups = e.query()
        },
        function(a) {
            console.log(a.data),
            alert(a.data)
        })
    },
    a.promoteServer = function(b) {
        f.promote(b,
        function(b) {
            a.server_groups = e.query()
        },
        function(a) {
            alert(a.data)
        })
    },
    a.removeServerGroup = function(b) {
        var c = confirm("are you sure to remove group_" + b + " ?");
        c && f["delete"]({
            id: b
        },
        function() {
            a.server_groups = e.query()
        },
        function() {
            alert(failedData.data)
        })
    },
    a.addServer = function(b) {
        var d = c.open({
            templateUrl: "addServerToGroupModal",
            controller: ["$scope", "$modalInstance",
            function(a, c) {
                a.server = {
                    addr: "",
                    type: "slave",
                    group_id: b
                },
                a.ok = function(a) {
                    c.close(a)
                },
                a.cancel = function() {
                    c.close(null)
                }
            }],
            size: "sm"
        });
        d.result.then(function(b) {
            b && f.addServer(b,
            function(b) {
                a.server_groups = e.query()
            },
            function(a) {
                alert(a.data)
            })
        })
    },
    a.addServerGroup = function() {
        var b = c.open({
            templateUrl: "newServerGroupModal",
            controller: ["$scope", "$modalInstance",
            function(a, b) {
                a.ok = function(a) {
                    b.close(a)
                },
                a.cancel = function() {
                    b.close(null)
                }
            }],
            size: "sm"
        });
        b.result.then(function(b) {
            b && e.create(b,
            function(b) {
                a.server_groups = e.query()
            },
            function(a) {
                alert(a.data)
            })
        })
    },
    a.refresh = function() {
        a.server_groups = e.query()
    },
    a.server_groups = e.query()
}]);
