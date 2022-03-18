# coding: utf-8
import time
import json
import hashlib
import base64
import urllib.parse
import fgourl as url
import mytime


class user:
    def __init__(self, userId, authKey, secretKey):
        self.name = ''
        self.userId = (int)(userId)
        self.authKey = authKey
        self.secretKey = secretKey
        self.session = url.NewSession()
        self.freeDraw = False

    def getAuthCode(self, par):
        par = {k: par[k] for k in sorted(par)}
        par = urllib.parse.urlencode(par, safe='+=:/ ')
        text = par + ':' + self.secretKey
        dig = hashlib.sha1(text.encode('utf-8')).digest()
        return base64.b64encode(dig)

    def userLogin(self):
        self.gameData()
        time.sleep(6)
        self.topLogin()
        time.sleep(3)
        self.topHome()

    def topLogin(self):
        lastAccessTime = mytime.GetTimeStamp()
        userState = (
            -lastAccessTime >> 2) ^ self.userId & url.dataServerFolderCrc
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': lastAccessTime,
            'verCode': url.verCode,
            'userState': userState,
            'assetbundleFolder': url.assetbundleFolder,
            'dataVer': url.dataVer,
            'isTerminalLogin': '1'
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)

        data = url.PostReq(
            self.session,
            "%s/login/top?_userId=%s" % (url.gameServerAddr, self.userId), req)
        self.message = data['cache']['replaced']['userGame'][0]['message']
        self.name = hashlib.md5(data['cache']['replaced']['userGame'][0]
                                ['name'].encode('utf-8')).hexdigest()
        self.stone = data['cache']['replaced']['userGame'][0]['stone']
        self.lv = data['cache']['replaced']['userGame'][0]['lv']
        self.exp = data['cache']['replaced']['userGame'][0]['exp']
        self.ticket = 0

        # 呼符
        for item in data['cache']['replaced']['userItem']:
            if (item['itemId'] == 4001):
                self.ticket = item['num']
                break

        # 登入天數
        res = "[%s]\n`登入天數: %s天 / %s天\n" % (
            self.name,
            data['cache']['updated']['userLogin'][0]['seqLoginCount'],
            data['cache']['updated']['userLogin'][0]['totalLoginCount'])

        # 角色訊息
        res += "等級: %s\n石頭: %s\n呼符: %s\n" % (self.lv, self.stone, self.ticket)

        # 現有體力
        #actMax = data['cache']['replaced']['userGame'][0]['actMax']
        #actRecoverAt = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        #res += "現存體力: %s\n" % (actMax - (actRecoverAt - mytime.GetTimeStamp()) / 300)

        # 友情點
        res += "友情點: +%s / %s`\n" % (
            data['response'][0]['success']['addFriendPoint'],
            data['cache']['replaced']['tblUserGame'][0]['friendPoint'])

        # 登入獎勵
        if 'seqLoginBonus' in data['response'][0]['success']:
            res += '*%s*\n`' % data['response'][0]['success']['seqLoginBonus'][
                0]['message']
            for i in data['response'][0]['success']['seqLoginBonus'][0][
                    'items']:
                res += "%s X %s\n" % (i['name'], i['num'])
            if 'campaignbonus' in data['response'][0]['success']:
                for cp in data['response'][0]['success']['campaignbonus']:
                    res += '`*%s*\n*%s*\n%s\n`' % (
                        cp['name'],
                        cp['detail'],
                        cp['script']['banners'][0]['bannerUrl']
                    )
                    for i in cp['items']:
                        res += "%s X %s\n" % (i['name'], i['num'])
            res += '`'
        
        # 間隔12小時才友抽
        # for i in data['cache']['replaced']['userGacha']:
            # if i['gachaId']==1 and lastAccessTime - i['freeDrawAt'] > 43200 and data['cache']['replaced']['tblUserGame'][0]['friendPoint'] > 2000 :
                # self.freeDraw = True
                # break
        # 檢查UTC+9不同天才友抽
        for i in data['cache']['replaced']['userGacha']:
            if i['gachaId'] == 1 and mytime.IsDaySame(i['freeDrawAt']) == False and data['cache']['replaced']['tblUserGame'][0]['friendPoint'] > 2000:
                self.freeDraw = True
                break
        svtCount = 0
        ceCount = 0
        for svt in data['cache']['updated']['userSvt']:
            if str(svt['svtId']).startswith( '93' ) or str(svt['svtId']).startswith( '94' ) or str(svt['svtId']).startswith( '98' ) :
                ceCount += 1
            else:
                svtCount += 1
        res += "`從者/禮裝數: %s / %s`\n" % (
            svtCount,
            ceCount)
        if ceCount>=data['cache']['replaced']['userGame'][0]['svtEquipKeep']+100 or svtCount>=data['cache']['replaced']['userGame'][0]['svtKeep']+100 :
            self.freeDraw = False

        return res + '_%s_\n--------\n' % mytime.TimeStampToString(
            data['cache']['serverTime'])

    def topHome(self):
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': mytime.GetTimeStamp(),
            'verCode': url.verCode,
            'dataVer': url.dataVer
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)
        url.PostReq(
            self.session,
            "%s/home/top?_userId=%s" % (url.gameServerAddr, self.userId), req)

    def friendGacha(self):
        mstGachaSub = url.GetJsonFromUrl(url.MstDataUrl+"mstGachaSub.json")
        gachaSubIdNow = 1
        for gs in mstGachaSub :
            if gs['gachaId'] == 1 and gs['openedAt'] < mytime.GetTimeStamp() and gs['closedAt'] > mytime.GetTimeStamp() and gs['commonReleaseId'] == 0 :
                gachaSubIdNow = gs[id]
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': mytime.GetTimeStamp(),
            'verCode': url.verCode,
            'dataVer': url.dataVer,
            'storyAdjustIds': [],
            'gachaId': 1,
            'num': 10,
            'ticketItemId': 0,
            'shopIdIndex': 1,
            'gachaSubId': gachaSubIdNow
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)
        data = url.PostReq(
            self.session,
            "%s/gacha/draw?_userId=%s" % (url.gameServerAddr, self.userId), req)
        if data['response'][0]['resCode'] == '00':
            res = '`友情點數召喚累計%s次\n\n`' % (
                data['cache']['updated']['userGacha'][0]['num']
            )
        return res

    def gameData(self):
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': mytime.GetTimeStamp(),
            'verCode': url.verCode,
            'dataVer': url.dataVer
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)
        data = url.PostReq(
            self.session,
            "%s/gamedata/top?_userId=%s" % (url.gameServerAddr, self.userId),
            req)
        if 'action' in data['response'][0]['fail'] and data['response'][0][
                'fail']['action'] == "app_version_up":
            url.UpdateAppVer(data['response'][0]['fail']['detail'].replace(
                "\r\n", ""))
            self.gameData()
            return
        if data['response'][0]['success']['dateVer'] != url.dateVer or data[
                'response'][0]['success']['dataVer'] != url.dataVer:
            s = "*Need Update*\n"
            s += "appVer: %s\n" % (url.appVer)
            s += "dateVer: %s Server: %s\n" % (
                url.dateVer, data['response'][0]['success']['dateVer'])
            s += "dataVer: %s Server: %s" % (
                url.dataVer, data['response'][0]['success']['dataVer'])
            url.SendMessageToAdmin(s)
            val = url.UpdateBundleFolder(
                data['response'][0]['success']['assetbundle'])
            if val == 1:
                url.dataVer = data['response'][0]['success']['dataVer']
                url.dateVer = data['response'][0]['success']['dateVer']
                dict = {}
                dict['global'] = {
                    "appVer": url.appVer,
                    "assetbundleFolder": url.assetbundleFolder,
                    "dataServerFolderCrc": url.dataServerFolderCrc,
                    "dataVer": url.dataVer,
                    "dateVer": url.dateVer
                }
                url.WriteConf(json.dumps(dict))
            else:
                url.SendMessageToAdmin('update failed')
