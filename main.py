import os
import time
import mytime
import fgourl as url
from user import user

userIds = os.environ['userIds'].split(",")
authKeys = os.environ['authKeys'].split(",")
secretKeys = os.environ['secretKeys'].split(",")

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

url.verCode = os.environ['verCode']
url.WebhookUrl = os.environ['WebhookUrl']
url.TelegramBotToken = os.environ['TGBotToken']
url.TelegramAdminId = os.environ['TGAdminId']
url.GithubToken = os.environ['GithubToken']
url.GithubName = os.environ['GithubName']
url.MstDataUrl = os.environ['MstDataUrl']
UA = os.environ['UserAgent']
if UA != 'nullvalue':
    url.UserAgent = UA


def main():
    url.SendMessageToAdmin("鐺鐺鐺( \`д´) *%s點* 了" % mytime.GetNowTimeHour())
    if userNums == authKeyNums and userNums == secretKeyNums:
        url.ReadConf()
        print("待簽到: %d 個" % userNums)
        res = '【登入訊息】\n'
        for i in range(userNums):
            instance = user(userIds[i], authKeys[i], secretKeys[i])
            instance.gameData()
            time.sleep(5)
            res2 = instance.topLogin()
            time.sleep(2)
            instance.topHome()
            if(instance.freeDraw):
                time.sleep(2)
                res2 += instance.friendGacha()
            res += res2
            url.SendMessageToAdmin(res2)
        url.UploadFileToRepo(mytime.GetNowTimeFileName(), res,
                             mytime.GetNowTimeFileName())
    else:
        print("帳號密碼數量不匹配")


if __name__ == '__main__':
    main()
