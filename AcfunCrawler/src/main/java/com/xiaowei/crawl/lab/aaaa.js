(window.webpackJsonp = window.webpackJsonp || []).push([["common/widget/header/newHeader"], {
    "./common/widget/header/newHeader.es6": function (e, t, s) {
        "use strict";
        s.r(t);
        s("../node_modules/@ac/Ajs/dist/A.min.js");
        var i = s("../node_modules/jquery/dist/jquery.js"), a = s.n(i), r = s("./common/static/js/common.es6"),
            n = s("./common/widget/header/user.es6"), o = 0, l = 1, c = "", h = "", u = "";

        function d(e, t, s, i) {
            switch (e) {
                case 1:
                    return "/bangumi/aa" + t + "_" + i + "_" + i;
                case 2:
                    return "/v/ac" + t + (s > 0 ? "_" + (s + 1) : "");
                case 3:
                    return "/a/ac" + t + (s > 0 ? "_" + (s + 1) : "");
                default:
                    return "/"
            }
        }

        function f() {
            var e = {total: 0, items: []};
            try {
                a()("#guide-msg-list").find(".badget").each((function () {
                    parseInt(a()(this).text(), 10) > 0 && ("99+" === a()(this).text() ? e.total += parseInt("100", 10) : e.total += parseInt(a()(this).text(), 10))
                })), e.total = e.total > 99 ? "99+" : e.total
            } catch (e) {
                console.log("parseError.", e)
            }
            e.total ? a()(".guide-msg .icon-message").find(".badget").text(e.total) : a()(".guide-msg .icon-message").find(".badget").text(""), a()(".guide-item.guide-msg").find(".badget").each((function (e, t) {
                "" === t.innerText ? a()(t).css("display", "none") : a()(t).css("display", "inline-block")
            }))
        }

        function g(e) {
            if (e) {
                var t;
                try {
                    t = JSON.parse(localStorage.getItem("searchCache")) || []
                } catch (e) {
                    t = []
                }
                (t = t.filter((function (t) {
                    return t !== e
                }))).unshift(a.a.xssFilter(e)), t.splice(8), localStorage.setItem("searchCache", JSON.stringify(t))
            }
        }

        A.ready((function () {
            new A.Widget({
                el: "#header",
                events: {
                    "mouseover .download-app": "showDownloadPhoto",
                    "mouseout .download-app": "hideDownloadPhoto",
                    "click .search-btn": "actionSearch",
                    "focus #search-text": "onSearchInputFocus",
                    "blur #search-text": "onSearchInputBlur",
                    "click .search-result ul": "onULClick",
                    "click .search-history-body": "onHistoryWordClick",
                    "keyup #search-text": "onInputKeyUp",
                    "click .clear-history": "clearSearchHistory"
                },
                created: function () {
                    var e = this;
                    if (/\/v\/ac/gi.test(location.href) ? (a()(".channel-bread .channel-second").html(window.videoInfo.channel.parentName).attr("href", "/v/list" + window.videoInfo.channel.parentId + "/index.htm"), a()(".channel-bread .channel-third").html(window.videoInfo.channel.name).attr("href", "/v/list" + window.videoInfo.channel.id + "/index.htm")) : /\/livestreaming/gi.test(location.href) ? a()(".channel-bread").html("Live") : /\/bangumi\/aa/gi.test(location.href) ? a()(".channel-bread").html("<a href='/bangumilist' target='blank' class='channel-second'>番剧</a>") : a()(".channel-bread").hide(), this.$form = this.el.querySelector(".form"), this.$searchInput = this.el.querySelector("#search-text"), this.$searchResultContainer = this.el.querySelector(".search-result"), this.$searchHistoryOps = this.$searchResultContainer.querySelector(".search-history-tool"), this.$searchHistory = this.$searchResultContainer.querySelector(".search-history-body"), this.$sugPanel = this.$searchResultContainer.querySelector(".sug"), this.$sugList = this.$sugPanel.querySelector("ul"), this.$recPanel = this.$searchResultContainer.querySelector(".rec"), this.fillInSearchHistory(), this.searchMode = o, this.secChannelTimeout = null, n.userInfo.isLogin()) {
                        a()("#header-guide").find(".guide-user");
                        a.a.getScript(window.globalConfig.imsdkcdn, (function () {
                            e.watchIMMsgCountUpdate(), f()
                        })), this.loginBrowseHistory()
                    } else this.unLoginBrowseHistory();
                    var t, s, i, r = a()("#nav"), l = r.find(".nav-sub"), c = l.find(".nav-sub-con"),
                        h = a()(".channel-guide"), u = function (e) {
                            i = setTimeout((function () {
                                r.removeClass("hover").find("li").removeClass("hover"), l.find("ul").hide()
                            }), e >= 0 ? e : 150)
                        };
                    a()(".nav-parent .channel-list li").hover((function () {
                        var e = a()(this), n = a()(this).attr("data-category");
                        h.addClass("hover"), clearTimeout(s), clearTimeout(i), t = setTimeout((function () {
                            if (e.addClass("hover").siblings("li").removeClass("hover"), !c.find("ul[data-category=" + n + "]").length) return u(150), !1;
                            r.addClass("hover");
                            var t = l.find("ul"), s = l.find("[data-category=" + n + "]");
                            t.hide();
                            c.offset().left;
                            var i = a()("#nav .nav-parent").offset().left,
                                o = e.offset().left - s.outerWidth() / 2 + e.outerWidth() / 2;
                            o = o > i ? o : i, s.css({left: o}).show()
                        }), 150)
                    }), (function () {
                        clearTimeout(t), s = setTimeout((function () {
                            r.find("channel-list").removeClass("show"), h.removeClass("hover"), r.removeClass("hover").find("li").removeClass("hover"), l.find("li").removeClass("hover").find("ul").hide()
                        }), 0)
                    })), a()(".nav-sub").hover((function () {
                        r.find(".channel-list").addClass("show"), h.addClass("hover"), clearTimeout(s), clearTimeout(i)
                    }), (function () {
                        u(0), r.find(".channel-list").removeClass("show"), h.removeClass("hover")
                    }))
                },
                methods: {
                    fillInSearchHistory: function () {
                        var e = localStorage.getItem("searchCache");
                        if (e) {
                            var t, s = "";
                            try {
                                t = JSON.parse(e) || []
                            } catch (e) {
                                t = []
                            }
                            t.forEach((function (e) {
                                s += "<a href='/search?keyword=" + encodeURI(e) + "' target='_blank'>" + e + "</a>"
                            })), this.$searchHistory.innerHTML = s, this.el.querySelector(".search-history-box").style.display = "block", this.$searchHistoryOps.style.display = "block"
                        } else this.$searchHistoryOps.style.display = "none"
                    }, hideSearchResultPanel: function () {
                        this.$searchResultContainer.style.display = "none"
                    }, showSearchResultPanel: function () {
                        this.$searchResultContainer.style.display = "block"
                    }, switch2RecommendPanel: function () {
                        this.$recPanel.style.display = "block", this.$sugPanel.style.display = "none", this.searchMode = o;
                        var e = this.$sugList.querySelector("li.active");
                        e && (e.className = e.className.replace(/(\s+)?active/, ""))
                    }, switch2SuggestionPanel: function () {
                        this.$recPanel.style.display = "none", this.$sugPanel.style.display = "block", this.searchMode = l;
                        var e = this.$recPanel.querySelector("li.active");
                        e && (e.className = e.className.replace(/(\s+)?active/, ""))
                    }, actionSearch: function () {
                        var e = this.$searchInput.value.trim();
                        g(e);
                        var t = "/search?keyword=", s = this.$searchInput.getAttribute("data-url"),
                            i = this.$searchInput.getAttribute("placeholder");
                        e ? t += encodeURI(e) : s ? t = s : i && (t += encodeURI(i)), window.open(t), this.hideSearchResultPanel()
                    }, onInputKeyUp: function (e) {
                        var t, s = this.$searchInput.value;
                        if (38 !== e.which && 40 !== e.which) 13 !== e.which ? s ? (this.switch2SuggestionPanel(), this.fetchSuggestion()) : (this.fillInSearchHistory(), this.showSearchResultPanel(), this.switch2RecommendPanel()) : this.actionSearch(); else {
                            var i, a;
                            if (this.searchMode === l ? (i = this.$sugPanel.querySelector("li.active"), a = this.$sugList) : (i = this.$recPanel.querySelector("li.active"), a = this.$recPanel.querySelector("ul")), i) {
                                var n = a.querySelectorAll("li"), o = n.length, c = Object(r.findIndex)(n, i);
                                (t = 38 === e.keyCode ? c - 1 : c + 1) < 0 && (t = o - 1), t >= o && (t = 0), i.className = i.className.replace(/(\s+)?active/, ""), a.querySelector("li:nth-child(" + (t + 1) + ")").className += " active"
                            } else {
                                var h = 38 === e.keyCode ? "last-child" : "first-child";
                                a.querySelector("li:" + h).className += " active"
                            }
                            this.$searchInput.value = a.querySelector("li.active b").innerText
                        }
                    }, fetchSuggestion: function () {
                        var e = this, t = this.$searchInput.value, s = new RegExp(t, "i");
                        a.a.ajax({
                            type: "get",
                            url: "/rest/pc-direct/search/suggest?count=6&keyword=" + encodeURIComponent(t),
                            dataType: "jsonp"
                        }).done((function (i) {
                            var r = "";
                            if (0 === i.result && i.suggestKeywords && i.suggestKeywords.length) for (var n = Math.min(7, i.suggestKeywords.length), o = 0; o < n; o++) {
                                var l = i.suggestKeywords[o].replace(s, "<i class='light'>" + t + "</i>");
                                r += "<li><a href='/search?keyword=" + encodeURI(i.suggestKeywords[o]) + "' target='_blank'><b>" + l + "</b></a></li>"
                            }
                            if (!r) return e.$sugList.innerHTML = "", void e.hideSearchResultPanel();
                            e.$sugList.innerHTML = r, a()(e.$searchInput).is(":focus") && e.showSearchResultPanel()
                        })).fail((function () {
                            e.$sugList.innerHTML = "", e.hideSearchResultPanel()
                        }))
                    }, clearSearchHistory: function () {
                        localStorage.removeItem("searchCache"), this.el.querySelector(".search-history-box").style.display = "none", this.$searchHistory.innerHTML = "", this.$searchHistoryOps.style.display = "none"
                    }, onHistoryWordClick: function (e) {
                        if ("A" === e.target.tagName) {
                            var t = e.target.innerText;
                            this.$searchInput.value = t, g(t)
                        }
                    }, onULClick: function (e) {
                        var t = e.target;
                        "B" !== t.tagName && (t = t.querySelector("b")), g(t.innerText)
                    }, onSearchInputBlur: function () {
                        var e = this;
                        setTimeout((function () {
                            return e.hideSearchResultPanel()
                        }), 300)
                    }, onSearchInputFocus: function () {
                        this.searchMode === l ? this.switch2SuggestionPanel() : (this.fillInSearchHistory(), this.switch2RecommendPanel()), this.showSearchResultPanel()
                    }, showDownloadPhoto: function (e) {
                        var t = this.el.querySelector("div.app-download");
                        this.appTimer = setTimeout((function () {
                            t.style.display = "block", a()(e.target).offset().left + a()(t).outerWidth() > a()(window).width() ? a()(e.target).addClass("right") : a()(e.target).removeClass("right")
                        }), 100)
                    }, hideDownloadPhoto: function () {
                        clearTimeout(this.appTimer), this.el.querySelector("div.app-download").style.display = "none"
                    }, fillInHistroy: function (e, t) {
                        var s, i = (new Date).setHours(0, 0, 0, 0), a = i - 864e5;
                        e.forEach((function (e) {
                            if (!e.disable) {
                                t || (e.resourceType = "article" === e.type ? 3 : 2, e.platform = 10, e.resourceId = e.aid || e.bid, e.priority = e.part, e.playedSecondsShow = e.playedSecondsShow || "刚刚开始", e.browseTimeGroup = e.time < a ? 10 : e.time < i ? 2 : 1);
                                var s = 3 !== e.resourceType ? '<li><a href="[url]"  target="_blank" title="[title]"><i class="device [deviceType]"></i><span class="video-title item-title">[title]</span><span class="watch-progress">[watchedTime]</span></a></li>' : '<li><a href="[url]"  target="_blank" title="[title]"><i class="device [deviceType]"></i><span class="article-title item-title">[title]</span></a></li>',
                                    n = {
                                        url: d(e.resourceType, e.resourceId, e.priority, e.itemId),
                                        deviceType: Object(r.getPlatform)(e.platform),
                                        title: e.title,
                                        watchedTime: e.playedSecondsShow
                                    };
                                switch (e.browseTimeGroup) {
                                    case 1:
                                        0 == c.length && (c += '<h3 class="timeline">今天</h3>'), c += Object(r.parseTemp)(s, n);
                                        break;
                                    case 2:
                                        0 == h.length && (h += '<h3 class="timeline">昨天</h3>'), h += Object(r.parseTemp)(s, n);
                                        break;
                                    case 10:
                                        0 == u.length && (u += '<h3 class="timeline">更早</h3>'), u += Object(r.parseTemp)(s, n)
                                }
                            }
                        })), s = c + h + u, this.el.querySelector(".guide-history ul").innerHTML = s.length > 0 ? s : "尚未记录任何历史信息。"
                    }, loginBrowseHistory: function () {
                        var e = this;
                        a.a.ajax({
                            type: "post",
                            url: "/rest/pc-direct/browse/history/list",
                            data: {pageSize: 5, pageNo: 1, resourceTypes: "1,2,3"},
                            xhrFields: {withCredentials: !0}
                        }).done((function (t) {
                            0 === t.result && t.histories && e.fillInHistroy(t.histories, !0)
                        }))
                    }, unLoginBrowseHistory: function () {
                        var e = function (e) {
                            void 0 === e && (e = 10);
                            var t;
                            try {
                                t = JSON.parse(localStorage.getItem("cache"))
                            } catch (e) {
                                t = []
                            }
                            if (t && t.history && t.history.views) {
                                var s = t.history.views;
                                return Object(r.isArray)(s) && s.reverse().splice(0, e)
                            }
                            return []
                        }(5);
                        e && this.fillInHistroy(e, !1)
                    }, watchIMMsgCountUpdate: function () {
                        var e = "unreadCount_immsg";
                        localStorage.getItem(e) || localStorage.setItem(e, JSON.stringify({
                            name: "私信",
                            showCount: "",
                            realCount: 0,
                            href: "//message.acfun.cn/im",
                            type: "immsg"
                        })), window.ImSdk && (new window.ImSdk).on("unReadCountUpdate", (function (e) {
                            var t = "99+";
                            e <= 99 && (t = e <= 0 ? "" : e + ""), a()(".message").find(".badget").text(t), f()
                        }))
                    }
                }
            });
            a.a.getScript("//static.yximgs.com/udata/pkg/acfun-pwa/standalone.js").done((function () {
            })).fail((function (e, t, s) {
                console.log(s)
            }))
        }))
    }
}, [["./common/widget/header/newHeader.es6", "runtime", "@ac/Ajs", "jquery", "@ac/bigpipejs", "common/static/js/common", "common/widget/header/user"]]]);