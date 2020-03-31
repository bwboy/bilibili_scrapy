return Number(this.input.quality)
},
enumerable:!0, configurable
:
!0
}),
Object.defineProperty(e.prototype, "type", {
    get: function () {
        return Number(this.input.type)
    }, enumerable: !0, configurable: !0
}), Object.defineProperty(e.prototype, "upPreview", {
    get: function () {
        return Boolean(this.input.upPreview)
    }, enumerable: !0, configurable: !0
}), e
}
(), k = function () {
    function e() {
        try {
            var e = (t = "bilibili_player_settings", window.localStorage && localStorage.getItem ? localStorage.getItem(t) : P(t));
            this.data = null == e ? {} : Object(JSON.parse(e))
        } catch (e) {
            this.data = {}
        }
        var t
    }

    return Object.defineProperty(e.prototype, "volume", {
        get: function () {
            try {
                return +this.data.video_status.volume || .66
            } catch (e) {
                return .66
            }
        }, enumerable: !0, configurable: !0
    }), Object.defineProperty(e.prototype, "quality", {
        get: function () {
            try {
                return O.normalize(this.data.setting_config.defquality) || 0
            } catch (e) {
                return 0
            }
        }, enumerable: !0, configurable: !0
    }), e
}(), x = function () {
    function e(e) {
        this.player = e;
        var t = p.a.CancelToken;
        this.cancelTokenSource = t.source()
    }

    return e.prototype.r = function (e, t, n) {
        var r, i = {params: e, resolve: t, reject: n}, a = this.player.ccl.__playinfo__;
        a && "object" == typeof a && (delete this.player.ccl.__playinfo__, a.videoFrame && a.data && (a.data.videoFrame = a.videoFrame), a.session && (this.player.session = a.session, e.session = a.session), "object" == typeof a.data && (a = a.data), !this.player.state.allowFlv && a.format && -1 === a.format.indexOf("mp4") || (r = this.parse(a, {
            params: i.params,
            resolve: i.resolve,
            reject: N
        }))), r ? this.urlChecker(r, (function (e) {
            return i.resolve(e)
        })) : this.handlePlayurlRequest(e, i, 3)
    }, e.prototype.handlePlayurlRequest = function (e, t, n, r) {
        var i = this,
            a = e.pugv ? "api.bilibili.com/pugv/player/web/playurl" : e.inner ? "manager.bilibili.co/v2/playurl" : e.upPreview ? "member.bilibili.com/x/web/archive/video/playurl" : e.seasonType >= 1 ? "api.bilibili.com/pgc/player/web/playurl" : "api.bilibili.com/x/player/playurl",
            o = r ? "http://" + a : "//" + a, s = {cid: e.cid, qn: e.quality, type: e.type, otype: "json"};
        e.bvid ? s.bvid = e.bvid : s.avid = e.aid, e.episodeId && (s.ep_id = e.episodeId), e.seasonType >= 1 && (s.fourk = 1), "number" != typeof e.fnver || e.inner || (s.fnver = e.fnver, s.fnval = e.fnval, s.session = e.session);
        var u = Date.now();
        p()({
            method: "get",
            url: o,
            responseType: "json",
            params: s,
            withCredentials: !0,
            cancelToken: this.cancelTokenSource.token
        }).then((function (e) {
            i.player.reportQueues.push({type: "api_playurl_done_time", value: Date.now() - u, timestamp: Date.now()});
            var n = i.parse(e.data, t, o);
            void 0 !== n && i.urlChecker(n, (function (e) {
                return t.resolve(e)
            }))
        })).catch((function (a) {
            if (i.player.reportQueues.push({
                type: "api_playurl_fail_time",
                value: Date.now() - u,
                timestamp: Date.now()
            }), /^https:/.test(o) || /^\/\//.test(o)) return n ? i.handlePlayurlRequest(e, t, --n, r) : i.handlePlayurlRequest(e, t, n, !0);
            t.reject(0, a.response && a.response.status && a.response.status.toString() || "", o)
        }))
    }, e.prototype.urlChecker = function (e, t) {
        var n = e.mediaDataSource && e.mediaDataSource.segments && e.mediaDataSource.segments[0] && e.mediaDataSource.segments[0].url;
        e.videoFrame && e.mediaDataSource && (e.mediaDataSource.preloadAVData = e.videoFrame, e.quality === Number(e.videoFrame.qn) && e.videoFrame.type === e.mediaDataSource.type && "flv" === e.videoFrame.type && e.videoFrame.video && (e.mediaDataSource.prebuffer = function (e) {
            try {
                for (var t = window.atob(e), n = new Uint8Array(t.length), r = 0; r < t.length; r++) n[r] = t.charCodeAt(r);
                return n.buffer
            } catch (e) {
                return
            }
        }(e.videoFrame.video))), "dash" === e.mediaDataSource.type ? t(e) : "mp4" === e.mediaDataSource.type && e.mediaDataSource.url && e.mediaDataSource.url.match(/:\/\/ws\.acgvideo\.com\//) ? p()({
            method: "get",
            url: e.mediaDataSource.url + "&get_url=1",
            responseType: "text",
            cancelToken: this.cancelTokenSource.token
        }).then((function (n) {
            e.mediaDataSource.url = n.data, t(e)
        })).catch((function () {
            t(e)
        })) : (I.safari.alike || I.trident.alike || I.edge.alike) && "flv" === e.mediaDataSource.type && n && n.match(/:\/\/ws\.acgvideo\.com\//) ? p()({
            method: "get",
            url: n + "&get_url=1",
            responseType: "text",
            cancelToken: this.cancelTokenSource.token
        }).then((function (n) {
            var r = /\/\/(.*)?\/ws\.acgvideo\.com/.exec(n.data);
            if (r) {
                var i = r[1];
                if (e.mediaDataSource.segments) for (var a = 0; a < e.mediaDataSource.segments.length; a++) {
                    var o = e.mediaDataSource.segments[a]
