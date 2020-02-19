# -*-coding: utf-8 -*-

from Linephu.linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, timeit
import random
from youtube_dl import YoutubeDL
#==============================================================================#
botStart = time.time()

cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))

#ki = LINE()
#ki.log("Auth Token : " + str(ki.authToken))

#k1 = LINE()
#k1.log("Auth Token : " + str(k1.authToken))

#k2 = LINE()
#k2.log("Auth Token : " + str(k2.authToken))

clMID = cl.profile.mid

#AMID = ki.profile.mid
#BMID = k1.profile.mid
#CMID = k2.profile.mid

#KAC = [cl,ki,k1,k2]
#Bots = [clMID,AMID,BMID,CMID]

clProfile = cl.getProfile()
#kiProfile = ki.getProfile()
#k1Profile = k1.getProfile()
#k2Profile = k2.getProfile()
lineSettings = cl.getSettings()
#kiSettings = ki.getSettings()
#k1Settings = k1.getSettings()
#k2Settings = k2.getSettings()

oepoll = OEPoll(cl)
#oepoll1 = OEPoll(ki)
#oepoll2 = OEPoll(k1)
#oepoll3 = OEPoll(k2)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
banOpen = codecs.open("ban.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)
ban = json.load(banOpen)

msg_dict = {}
bl = [""]

#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = ban
        f = codecs.open('ban.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = cl.genOBSParams({'oid': clMID, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4', 'name': 'Hello_World.mp4'})
        data = {'params': obs_params}
        r_vp = cl.server.postContent('{}/talk/vp/upload.nhn'.format(str(cl.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        cl.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile %s"%str(e))
def helpmessage():
    helpMessage = """╔══════════════
╠♥ ☾✟ 單體半垢 ✟☽ ♥
║
╠══✪〘 Help Message 〙✪═══
║
╠✪〘 Help 〙✪══════════
╠➥ Help 查看指令
║
╠✪〘 Status 〙✪════════
╠➥ Save 儲存設定
╠➥ rt 運作時間
╠➥ Sp 速度
╠➥ supersp 極限速度
╠➥ Set 設定
╠➥ About關於本帳
║
╠✪〘 Settings 〙✪═══════
╠➥ AutoAdd On/Off 自動加入
╠➥ AutoJoin On/Off 自動進群
╠➥ AutoLeave On/Off 離開副本
╠➥ AutoRead On/Off 自動已讀
╠➥ Share On/Off 公開/私人
╠➥ ReRead On/Off 查詢收回
╠➥ Pro On/Off 所有保護(失效)
╠➥ Protect On/Off 踢人保護(失效)
╠➥ QrProtect On/Off 網址保護(失效)
╠➥ Invprotect On/Off 邀請保護(失效)
╠➥ Getmid On/Off 取得mid
╠➥ Detect On/Off 標註偵測
╠➥ Timeline On/Off 文章網址預覽
║
╠✪〘 Self 〙✪═════════
╠➥ Me 我的連結
╠➥ MyMid 我的mid
╠➥ MyName 我的名字
╠➥ MyBio 個簽
╠➥ MyPicture 我的頭貼
╠➥ MyCover 我的封面
╠➥ Contact @ 標註取得連結
╠➥ Mid @ 標註查mid
╠➥ Name @ 查看名字
║
╠✪〘 Blacklist 〙✪═══════
╠➥ Ban @ 加入黑單
╠➥ Unban @ 取消黑單
╠➥ Banlist 查看黑單
╠➥ CleanBan 清空黑單
╠➥ Nkban 踢除黑單
║
╠✪〘 Group 〙✪════════
╠➥ GroupCreator創群者
╠➥ GroupId 群組ID
╠➥ GroupName 群組名稱
╠➥ GroupPicture 群組圖片
╠➥ GroupLink 群組網址
╠➥ Link「On/Off」網址開啟/關閉
╠➥ GroupList所有群組列表
╠➥ GroupMemberList 成員名單
╠➥ GroupInfo 群組資料
╠➥ Gn (文字) 更改群名
╠➥ Inv (mid) 透過mid邀請
╠➥ Inv @ 標註多邀
╠➥ gmlmidsp 成員mid碼(乾淨版)
╠➥ gmlmidspsp 成員mid碼(後台乾淨版)
╠➥ gmlmid 成員名單兼mid碼
║
╠✪〘 Special 〙✪═══════
╠➥ Mimic「On/Off」模仿說話
╠➥ MimicList 模仿名單
╠➥ MimicAdd @ 新增模仿名單
╠➥ MimicDel @ 模仿名單刪除
╠➥ Tagall 標註全體
╠➥ Setread 已讀點設置
╠➥ Cancelread 取消偵測
╠➥ Checkread 已讀偵測
║
╠✪〘 Admin 〙✪═════════
╠➥ Adminadd @ 新增權限
╠➥ Admindel @ 刪除權限
╠➥ Adminlist 查看權限表
║═〘 版權 by YT 傳說沅哥〙
╚═〘 版權 by 沅哥公開半垢〙"""
    return helpMessage
def help1message():
    help1Message = """╔════════════
╠〘 help1機器狀態指令表 〙══════
╠
╠➥ Save 儲存設定
╠➥ rt 運作時間
╠➥ Sp 速度
╠➥ supersp 極限速度
╠➥ Set 設定
╠➥ About關於本帳
╚═〘 版權 by 沅哥公開半垢〙"""
    return help1Message
def help2message():
    help2Message = """╔════════════
╠〘 help2機器設定指令表 〙══════
╠
╠  AutoAdd On/Off 自動加入
╠  AutoJoin On/Off 自動進群
╠  AutoLeave On/Off 離開副本
╠  AutoRead On/Off 自動已讀
╠  Share On/Off 公開/私人
╠  ReRead On/Off 查詢收回
╠  Getmid On/Off 取得mid
╠  Detect On/Off 標註偵測
╠  Timeline On/Off 文章網址預覽
╠  Pro On/Off 所有保護
╠  Protect On/Off 踢人保護
╠  QrProtect On/Off 網址保護
╠  Invprotect On/Off 邀請保護
╚═〘 版權 by 沅哥公開半垢〙"""
    return help2Message
def help3message():
    help3Message = """╔════════════
╠〘 help3機器常用指令表 〙══════
╠
╠ Tagall 標註全體
╠ Setread 已讀點設置
╠ Cancelread 取消偵測
╠ Checkread 已讀偵測
╠ gm 管理員清單
╠ gmlmid 成員名單兼mid碼
╚═〘 版權 by 沅哥公開半垢〙"""
    return help3Message
def help4message():
    help4Message = """╔════════════
╠〘 help4機器黑名單指令表 〙══════
╠
╠ Ban @ 加入黑單
╠ Unban @ 取消黑單
╠ Banlist 查看黑單
╠ CleanBan 清空黑單
╠ Nkban 踢除黑單
╚═〘 版權 by 沅哥公開半垢〙"""
    return help4Message
def help5message():
    help5Message = """╔════════════
╠〘 help5機器群組指令表 〙══════
╠
╠ GroupCreator創群者
╠ GroupId 群組ID
╠ GroupName 群組名稱
╠ GroupPicture 群組圖片
╠ GroupLink 群組網址
╠ Link「On/Off」網址開啟/關閉
╠ GroupMemberList 成員名單
╠ GroupInfo 群組資料
╠ Gn (文字) 更改群名
╠ Inv (mid) 透過mid邀請
╠ Inv @ 標註多邀
╠ gmlmidsp 成員mid碼(乾淨版)
╠ gmlmidspsp 成員mid碼(後台乾淨版)
╠ gmlmid 成員名單兼mid碼
╚═〘 版權 by 沅哥公開半垢〙"""
    return help5Message
def help6message():
    help6Message = """╔════════════
╠〘 help6機器特殊指令表 〙══════
╠
╠ Mimic「On/Off」模仿說話
╠ MimicList 模仿名單
╠ MimicAdd @ 新增模仿名單
╠ MimicDel @ 模仿名單刪除
╚═〘 版權 by 沅哥公開半垢〙"""
    return help6Message
def help7message():
    help7Message = """╔════════════
╠〘 help7機器權限指令表 〙══════
╠
╠ Adminadd @ 新增權限
╠ Admindel @ 刪除權限
╠ Adminlist 查看權限表
╚═〘 版權 by 沅哥公開半垢〙"""
    return help7Message
def help8message():
    help8Message = """╔════════════
╠〘 help8自訂指令表 〙══════
╠   
╠➥ 三十六計(還在開發)
╠
╠➥ 猜拳(簡略:「猜」)(還在開發)
╠
╠➥ 解答之書(簡略:「解」) (取自胡子的靈感)
╠
╠➥ 備份群組名單 指令 gmlback
╠
╚═〘 版權 by 沅哥公開半垢〙"""
    return help8Message
def help9message():
    help9Message = """╔════════════
╠〘 指令總表 〙══════
╠   (皆須權限才可使用)
╠➥ help0機器綜合指令表
╠➥ help1機器狀態指令表
╠➥ help2機器設定指令表
╠➥ help3機器常用指令表(推)
╠➥ help4機器黑名單指令表
╠➥ help5機器群組指令表
╠➥ help6機器特殊指令表
╠➥ help7機器權限指令表
╠➥ help8自訂指令表(所有人皆可使用)
╠
╚═〘 版權 by 沅哥公開半垢〙"""
    return help9Message
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

admin =[clMID,"u3bd2c4b1f43c0313fb79d405ec1ec90d","u079e75ac47a1eb702b4ff3cdb7ee9e21"]
owners = ["u3bd2c4b1f43c0313fb79d405ec1ec90d,u079e75ac47a1eb702b4ff3cdb7ee9e21"]
#if clMID not in owners:
#    python = sys.executable
#    os.execl(python, python, *sys.argv)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
#        if op.type == 5:
#            print ("[ 5 ] NOTIFIED ADD CONTACT")
#            if settings["autoAdd"] == True:
#                cl.findAndAddContactsByMid(op.param1)
#                cl.sendMessage(op.param1, "感謝加我好友喔".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            if settings["qrprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            if clMID in op.param3:
                group = cl.getGroup(op.param1)
                if settings["autoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
            elif settings["invprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
            else:
                group = cl.getGroup(op.param1)
                gInviMids = []
                for z in group.invitee:
                    if z.mid in ban["blacklist"]:
                        gInviMids.append(z.mid)
                if gInviMids == []:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, gInviMids)
                    cl.sendMessage(op.param1,"被邀請者黑單中...")
        if op.type == 17:
            if op.param2 in admin or op.param2 in ban["bots"]:
                return
            ginfo = str(cl.getGroup(op.param1).name)
            try:
                strt = int(3)
                akh = int(3)
                akh = akh + 8
                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(op.param2)+"},"""
                aa = (aa[:int(len(aa)-1)])
                cl.sendMessage(op.param1, "歡迎 @wanping 加入"+ginfo , contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
            except Exception as e:
                print(str(e))
        if op.type == 19:
            msg = op.message
            chiya = []
            chiya.append(op.param2)
            chiya.append(op.param3)
            cmem = cl.getContacts(chiya)
            zx = ""
            zxc = ""
            zx2 = []
            if op.param2 not in admin:
                if op.param2 in ban["bots"]:
                    pass
                elif settings["protect"] == True:
                    ban["blacklist"][op.param2] = True
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.inviteIntoGroup(op.param1,[op.param3])
                    try:
                          cl.sendMessage(op.param1, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                    except:
                          cl.sendMessage(op.param1,"Notified kick out from group")
                else:
                    cl.sendMessage(op.param1,"")
            else:
                cl.sendMessage(op.param1,"")

        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25 or op.type == 26:
            K0 = admin
            msg = op.message
            if settings["share"] == True:
                K0 = msg._from
            else:
                K0 = admin
#        if op.type == 25 :
#            if msg.toType ==2:
#                g = cl.getGroup(op.message.to)
#                print ("sended:".format(str(g.name)) + str(msg.text))
#            else:
#                print ("sended:" + str(msg.text))
#        if op.type == 26:
#            msg =op.message
#            pop = cl.getContact(msg._from)          
#            print (str(time.strftime("%Y/%m/%d  %H:%M:%S"))+":"+"Mid碼["+pop.mid+"]"+pop.displayName + ":" + str(msg.text))
#            f = open('welcomein/autorecoder.txt','a+')
#            f.write('\n')
#            f.write(str(time.strftime("%Y/%m/%d  %H:%M:%S"))+":"+"Mid碼["+pop.mid+"]"+pop.displayName + ":" + str(msg.text))
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
#==============================================================================#
            if msg.text.lower().startswith('織田信長 '):
                    x = text.split(' ',1)
                    f = open("ksk/odklm/"+str(x[1])+".txt","r")
                    cl.sendMessage(to, str(f.read()))
            if text.lower() == "gm":
                    if admin == []:
                        cl.sendMessage(to,"無擁有權限者!")
                    else:
                        mc = "╔══[ 管理員清單 ]"
                        for mi_d in admin:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
            if sender in owners: #唯有擁有者可使用重啟指令
                if text.lower() == 'restart':
                    cl.sendMessage(to, "準備重新啟動，機器正在登出中")
                    time.sleep(5)
                    cl.sendMessage(to, "登出成功，正在自動重新進行重新登入")
                    restartBot()
                elif msg.text.lower().startswith("cvp"):
                    sep = text.split(" ")
                    link = text.replace(sep[0] + " ","")
                    contact = cl.getContact(sender)
                    cl.sendMessage(to, "狀態: 下載中...")
                    print("正在下載中...需耗時數分鐘")
                    pic = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
                    os.system('youtube-dl --format mp4 --output BotVideo.mp4 {}'.format(link))
                    pict = cl.downloadFileURL(pic)
                    vids = "BotVideo.mp4"
                    changeVideoAndPictureProfile(pict, vids)
                    cl.sendMessage(to, "成功替換頭像影片")
                    print("成功替換頭像影片 刪除影片完畢")
                    os.remove("BotVideo.mp4")         
                elif msg.text.lower().startswith("cp"):
                    contact = cl.getContact(sender)
                    cl.sendMessage(to, "狀態: 更換中...")
                    print("需耗時數分鐘")
                    pic = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
                    pict = cl.downloadFileURL(pic)
                    vids = "Video.mp4"
                    changeVideoAndPictureProfile(pict, vids)
                    cl.sendMessage(to, "成功替換頭像影片")
                    print("成功替換頭像影片 刪除影片完畢")
                    os.remove("Video.mp4")  
            if sender in K0 or sender in owners:
#==============================================================================#
                if text.lower() == 'sp':
                        start = time.time()
                        cl.sendMessage(to, "嘗試解除封印中，請稍後")
                        elapsed_time = time.time() - start
                        cl.sendMessage(to,"一般解除封印所需時間"+format(str(elapsed_time)) + "秒")                
                elif text.lower() == 'help0':
                        helpMessage = helpmessage()
                        cl.sendMessage(to, str(helpMessage))
                elif text.lower() == 'help1':
                        help1Message = help1message()
                        cl.sendMessage(to, str(help1Message))
                elif text.lower() == 'help2':
                        help2Message = help2message()
                        cl.sendMessage(to, str(help2Message))
                elif text.lower() == 'help3':
                        help3Message = help3message()
                        cl.sendMessage(to, str(help3Message))
                elif text.lower() == 'help4':
                        help4Message = help4message()
                        cl.sendMessage(to, str(help4Message))
                elif text.lower() == 'help5':
                        help5Message = help5message()
                        cl.sendMessage(to, str(help5Message))
                elif text.lower() == 'help6':
                        help6Message = help6message()
                        cl.sendMessage(to, str(help6Message))
                elif text.lower() == 'help7':
                        help7Message = help7message()
                        cl.sendMessage(to, str(help7Message))
                elif text.lower() == 'help8':
                        help8Message = help8message()
                        cl.sendMessage(to, str(help8Message))
                elif text.lower() == 'help':
                        help9Message = help9message()
                        cl.sendMessage(to, str(help9Message))
                elif text.lower() == '解答之書':
                        cl.sendImage(to,"ans/"+random.randrange(1,401,1)+".jpg")
                elif text.lower() == '解':
                        cl.sendImage(to,"ans/"+str(random.randrange(1,401,1))+".jpg")
    #=============================猜拳系統==========================================#
                elif text.lower() == '石頭':
                        pea = random.randrange(1,6,1)
                        if pea == 1:
                            cl.sendMessage(to,"你出石頭，我出剪刀，你贏了喔喔!!")
                        if pea == 2:
                            cl.sendMessage(to,"你出石頭，我出石頭，平手喔喔!!")
                        if pea == 3:
                            cl.sendMessage(to,"你出石頭，我出布，你輸了喔喔!!")
                        if pea == 4:
                            cl.sendMessage(to,"你出石頭，我出剪刀，你贏了喔喔!!")
                        if pea == 5:
                            cl.sendMessage(to,"你出石頭，我出石頭，平手喔喔!!")
                        if pea == 6:
                            cl.sendMessage(to,"你出石頭，我出布，你輸了喔喔!!")
                elif text.lower() == '剪刀':
                        pea = random.randrange(1,6,1)
                        if pea == 1:
                            cl.sendMessage(to,"你出剪刀，我出剪刀，平手喔喔!!")
                        if pea == 2:
                            cl.sendMessage(to,"你出剪刀，我出石頭，你輸了喔喔!!")
                        if pea == 3:
                            cl.sendMessage(to,"你出剪刀，我出布，你贏了喔喔!!")
                        if pea == 4:
                            cl.sendMessage(to,"你出剪刀，我出剪刀，平手喔喔!!")
                        if pea == 5:
                            cl.sendMessage(to,"你出剪刀，我出石頭，你輸了喔喔!!")
                        if pea == 6:
                            cl.sendMessage(to,"你出剪刀，我出布，你贏了喔喔!!")
                elif text.lower() == '布':
                        pea = random.randrange(1,6,1)
                        if pea == 1:
                            cl.sendMessage(to,"你出布，我出剪刀，你輸了喔喔!!")
                        if pea == 2:
                            cl.sendMessage(to,"你出布，我出石頭，你贏了喔喔!!")
                        if pea == 3:
                            cl.sendMessage(to,"你出布，我出布，平手喔喔!!")
                        if pea == 4:
                            cl.sendMessage(to,"你出布，我出剪刀，你輸了喔喔!!")
                        if pea == 5:
                            cl.sendMessage(to,"你出布，我出石頭，你贏了喔喔!!")
                        if pea == 6:
                            cl.sendMessage(to,"你出布，我出布，平手喔喔!!")
                elif text.lower() == 'supersp':
                    start = time.time()
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")
                    cl.sendMessage(to, "極限解除封印所需時間")
                elif msg.text.lower().startswith('xiao!'): #笑笑活動寫入
                    x = text.split('!',1)
                    f = open('welcomein/xiao.txt','w')
                    f.write(str(x[1]))
                elif msg.text.lower().startswith('xiu!'): #修分靈活動寫入
                    x = text.split('!',1)
                    f = open('welcomein/xiu.txt','w')
                    f.write(str(x[1]))
                elif msg.text.lower().startswith('lin!'): #凌白活動寫入
                    x = text.split('!',1)
                    f = open('welcomein/lin.txt','w')
                    f.write(str(x[1]))
                elif text.lower() == 'save':
                    backupData()
                    cl.sendMessage(to,"儲存設定成功!")
                elif text.lower() == 'rt':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "解除封印累計時間 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner ="u3bd2c4b1f43c0313fb79d405ec1ec90d"
                        owner2 = "u079e75ac47a1eb702b4ff3cdb7ee9e21"
                        creator = cl.getContact(owner)
                        creator2 = cl.getContact(owner2)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於使用者 ]"
                        ret_ += "\n╠ 使用者名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組數 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友數 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 已封鎖 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於本bot ]"
                        ret_ += "\n╠ 版本 : 第一代防翻"
                        ret_ += "\n╠ 檔案者 : {}".format(creator.displayName)
                        ret_ += "\n╠ 權限者 : {}".format(creator2.displayName)
                        ret_ += "\n╚══[ 感謝您的使用 ]"
                        cl.sendMessage(to, str(ret_))
                        cl.sendContact(to,"u079e75ac47a1eb702b4ff3cdb7ee9e21")
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 狀態 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ 自動加友 ✅"
                        else: ret_ += "\n╠ 自動加友 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ 自動進群 ✅"
                        else: ret_ += "\n╠ 自動進群 ❌"
#                        if settings["autoLeave"] == True: ret_ += "\n╠ Auto Leave ✅"
#                        else: ret_ += "\n╠ Auto Leave ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ 自動已讀 ✅"
                        else: ret_ += "\n╠ 自動已讀 ❌"
                        if settings["protect"] ==True: ret_+="\n╠ Protect ✅"
                        else: ret_ += "\n╠ Protect ❌"
                        if settings["qrprotect"] ==True: ret_+="\n╠ QrProtect ✅"
                        else: ret_ += "\n╠ QrProtect ❌"
                        if settings["invprotect"] ==True: ret_+="\n╠ InviteProtect ✅"
                        else: ret_ += "\n╠ InviteProtect ❌"
                        if settings["detectMention"] ==True: ret_+="\n╠ DetectMention ✅"
                        else: ret_ += "\n╠ DetectMention ❌"
                        if settings["reread"] ==True: ret_+="\n╠ 復讀功能 ✅"
                        else: ret_ += "\n╠ 復讀功能 ❌"
                        if settings["share"] ==True: ret_+="\n╠ 公開權限 ✅"
                        else: ret_ += "\n╠ 公開權限 ❌"
                        if settings["tagtag"] ==True: ret_+="\n╠ 全標功能 ✅"
                        else: ret_ += "\n╠ 全標功能 ❌"
                        ret_ += "\n╚══[ 以上結束 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加友啟動")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加友取消")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動進群啟動")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動進群取消")
#                elif text.lower() == 'autoleave on':
#                    settings["autoLeave"] = True
#                    cl.sendMessage(to, "Auto Leave on success")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "Auto Leave off success")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "自動已讀啟動")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "自動已讀關閉")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to,"復讀啟動")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to,"復讀關閉")
                elif text.lower() == 'protect on':
                    settings["protect"] = True
                    cl.sendMessage(to, "踢人保護開啟")
                elif text.lower() == 'protect off':
                    settings["protect"] = False
                    cl.sendMessage(to, "踢人保護關閉")
                elif text.lower() == 'share on':
                    settings["share"] = True
                    cl.sendMessage(to, "已開啟分享權限")
                elif text.lower() == 'share off':
                    settings["share"] = False
                    cl.sendMessage(to, "已關閉分享權限")
                elif text.lower() == 'detect on':
                    settings["detectMention"] = True
                    cl.sendMessage(to, "已開啟標註偵測")
                elif text.lower() == 'detect off':
                    settings["detectMention"] = False
                    cl.sendMessage(to, "已關閉標註偵測")
                elif text.lower() == 'qrprotect on':
                    settings["qrprotect"] = True
                    cl.sendMessage(to, "網址保護開啟")
                elif text.lower() == 'qrprotect off':
                    settings["qrprotect"] = False
                    cl.sendMessage(to, "網址保護關閉")
                elif text.lower() == 'invprotect on':
                    settings["invprotect"] = True
                    cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'invprotect off':
                    settings["invprotect"] = False
                    cl.sendMessage(to, "邀請保護關閉")
                elif text.lower() == 'getmid on':
                    settings["getmid"] = True
                    cl.sendMessage(to, "mid獲取開啟")
                elif text.lower() == 'getmid off':
                    settings["getmid"] = False
                    cl.sendMessage(to, "mid獲取關閉")
                elif text.lower() == 'timeline on':
                    settings["timeline"] = True
                    cl.sendMessage(to, "文章預覽開啟")
                elif text.lower() == 'timeline off':
                    settings["timeline"] = False
                    cl.sendMessage(to, "文章預覽關閉")
                elif text.lower() == 'tagtag on':
                    settings["tagtag"] = True
                    cl.sendMessage(to, "全標功能開啟")
                elif text.lower() == 'tagtag off':
                    settings["tagtag"] = False
                    cl.sendMessage(to, "全標功能關閉")
                elif text.lower() == 'pro on':
                    settings["protect"] = True
                    settings["qrprotect"] = True
                    settings["invprotect"] = True
                    cl.sendMessage(to, "踢人網址邀請保護開啟")
                elif text.lower() == 'pro off':
                    settings["protect"] = False
                    settings["qrprotect"] = False
                    settings["invprotect"] = False
                    cl.sendMessage(to, "踢人網址邀請保護關閉")
#==============================================================================#
                elif msg.text.lower().startswith("adminadd "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.append(str(inkey))
                    cl.sendMessage(to, "已獲得權限！")
                elif msg.text.lower().startswith("admindel "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.remove(str(inkey))
                    cl.sendMessage(to, "已取消權限！")
                elif text.lower() == 'adminlist':
                    if admin == []:
                        cl.sendMessage(to,"無擁有權限者!")
                    else:
                        mc = "╔══[ Admin List ]"
                        for mi_d in admin:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif msg.text.lower().startswith("invite "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    G = cl.getGroup
                    cl.inviteIntoGroup(to,targets)
                elif ("Say " in msg.text):
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        cl.sendMessage(to,x[1])
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        sendMessageWithMention(to, inkey)
                elif msg.text.lower().startswith("botsadd "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].append(str(inkey))
                    cl.sendMessage(to, "已加入分機！")
                elif msg.text.lower().startswith("botsdel "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].remove(str(inkey))
                    cl.sendMessage(to, "已取消分機！")
                elif text.lower() == 'botslist':
                    if ban["bots"] == []:
                        cl.sendMessage(to,"無分機!")
                    else:
                        mc = "╔══[ Inviter List ]"
                        for mi_d in ban["bots"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'join':
                    if msg.toType == 2:
                        G = cl.getGroup
                        cl.inviteIntoGroup(to,ban["bots"])
                elif msg.text.lower().startswith("ii "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.createGroup("fuck",[inkey])
                    cl.leaveGroup(op.param1)
#==============================================================================#
                elif text.lower() == 'me':
                    if msg.toType == 2 or msg.toType == 1:
                        sendMessageWithMention(to, sender)
                        cl.sendContact(to, sender)
                    else:
                        cl.sendContact(to,sender)
                elif text.lower() == 'mymid':
                    cl.sendMessage(msg.to,"[MID]\n" +  sender)
                elif text.lower() == 'myname':
                    me = cl.getContact(sender)
                    cl.sendMessage(msg.to,"[Name]\n" + me.displayName)
                elif text.lower() == 'mybio':
                    me = cl.getContact(sender)
                    cl.sendMessage(msg.to,"[StatusMessage]\n" + me.statusMessage)
                elif text.lower() == 'mypicture':
                    me = cl.getContact(sender)
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideoprofile':
                    me = cl.getContact(sender)
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = cl.getContact(sender)
                    cover = cl.getProfileCoverURL(sender)
                    cl.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("name "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 名字 ]\n" + contact.displayName)
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 個簽 ]\n" + contact.statusMessage)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))
                
#==============================================================================#
                elif msg.text.lower().startswith("mimicadd "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["mimic"]["target"][target] = True
                            cl.sendMessage(msg.to,"已加入模仿名單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"添加失敗 !")
                            break
                elif msg.text.lower().startswith("mimicdel "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["模仿名單"]["target"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'mimiclist':
                    if ban["mimic"]["target"] == {}:
                        cl.sendMessage(msg.to,"未設定模仿目標")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in ban["mimic"]["target"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif "mimic" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if ban["mimic"]["status"] == False:
                            ban["mimic"]["status"] = True
                            cl.sendMessage(msg.to,"Reply Message on")
                    elif mic == "off":
                        if ban["mimic"]["status"] == True:
                            ban["mimic"]["status"] = False
                            cl.sendMessage(msg.to,"Reply Message off")
#==============================================================================#
                elif text.lower() == 'groupcreator':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'groupid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[ID Group : ]\n" + gid.id)
                elif text.lower() == 'grouppicture':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupname':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[群組名稱 : ]\n" + gid.name)
                elif text.lower() == 'grouplink':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ Group Ticket ]\nhttps://cl.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "Grouplink未開啟 {}openlink".format(str(settings["keyCommand"])))
                elif text.lower() == 'link on':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "群組網址已開")
                        else:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            cl.sendMessage(to, "開啟成功")
                elif text.lower() == 'link off':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "群組網址已關")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to, "關閉成功")
                elif text.lower() == 'groupinfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ Group Info ]"
                    ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組 Id : {}".format(group.id)
                    ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請中 : {}".format(gPending)
                    ret_ += "\n╠ 網址狀態 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ Finish ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupmemberlist':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員名單 ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'gmlmid':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員與mid碼名單 ]"
                        na = 0 + 1
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(na), str(mem.displayName))
                            na +=1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.mid))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'gmlmidspsp':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員與mid碼名單(省略標頭) ]"
                        na = 0 + 1
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.displayName))
                            na +=1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.mid))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
#                        cl.sendMessage(to, str(ret_))
                        print(to, str(ret_))
                elif text.lower() == 'gmlback': #備份群組名單儲存檔案
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        try:
                            gCreator = group.creator.displayName
                        except:
                            gCreator = "不明"
                        if group.invitee is None:
                            gPending = "0"
                        else:
                            gPending = str(len(group.invitee))
                        if group.preventedJoinByTicket == True:
                            gQr = "關閉"
                            gTicket = "無"
                        else:
                            gQr = "開啟"
                            gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                        path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                        ret_ = "╔══[ 群組資訊 ]"
                        ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
                        ret_ += "\n╠ 群組 Id : {}".format(group.id)
                        ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
                        ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
                        ret_ += "\n╠ 邀請中 : {}".format(gPending)
                        ret_ += "\n╠ 網址狀態 : {}".format(gQr)
                        ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                        ret_ += "\n╚══[ 群組資訊截止 ]"
                        ret_ += "\n╔══[ 群組名單與mid碼 ]"
                        na = 0 + 1
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.displayName))
                            na +=1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.mid))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
#                        cl.sendMessage(to, str(ret_))
#                        print(to, str(ret_))
                        thethetime = time.strftime('%Y%m%d %H%M%S',time.localtime(time.time()))
                        thethetime += "{}".format(str(group.name))
                        f = open('welcomein/group/' +thethetime +'.txt', 'w')
                        f.write(str(ret_))
                elif text.lower() == 'gmlbacks': #完全備份所有群組名單儲存檔案
                    groups = cl.groups
                    ret_ = "╔══[ 總群組備份 ]"
                    for gid in groups:
                        group = cl.getGroup(gid)
                        try:
                            gCreator = group.creator.displayName
                        except:
                            gCreator = "不明"
                        if group.invitee is None:
                            gPending = "0"
                        else:
                            gPending = str(len(group.invitee))
                        if group.preventedJoinByTicket == True:
                            gQr = "關閉"
                            gTicket = "無"
                        else:
                            gQr = "開啟"
                            gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                        path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                        ret_ += "╔══[ 群組資訊 ]"
                        ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
                        ret_ += "\n╠ 群組 Id : {}".format(group.id)
                        ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
                        ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
                        ret_ += "\n╠ 邀請中 : {}".format(gPending)
                        ret_ += "\n╠ 網址狀態 : {}".format(gQr)
                        ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                        ret_ += "\n╚══[ 群組資訊截止 ]"
                        ret_ += "\n╔══[ 群組名單與mid碼 ]"
                        na = 0 + 1
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.displayName))
                            na +=1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.mid))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
                        ret_ += "\n"
                    thethetime = time.strftime('%Y%m%d %H%M%S',time.localtime(time.time()))
                    f = open('allgroup/'+thethetime +'.txt', 'w')
                    f.write(str(ret_))
                elif text.lower() == 'gmlmidsp':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員與mid碼名單(省略標頭) ]"
                        na = 0 + 1
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.displayName))
                            na +=1
                        for mem in group.members:
                            ret_ += "\n{}".format(str(mem.mid))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
#                elif text.lower() == 'grouplist':
#                        groups = cl.groups
#                        ret_ = "╔══[ Group List ]"
#                        no = 0 + 1
#                        for gid in groups:
#                            group = cl.getGroup(gid)
#                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
#                            no += 1
#                        ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
#                        cl.sendMessage(to, str(ret_))
 #               elif msg.text.lower().startswith("nk "):
 #                   targets = []
 #                   key = eval(msg.contentMetadata["MENTION"])
 #                   key["MENTIONEES"][0]["M"]
 #                   for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        try:
#                            cl.sendMessage(to,"Fuck you")
#                            cl.kickoutFromGroup(msg.to,[target])
#                        except:
#                            cl.sendMessage(to,"Error")
#                
#                elif "Zk" in msg.text:
 #                   gs = cl.getGroup(to)
 #                   targets = []
 #                   for g in gs.members:
 #                       if g.displayName in "":
 #                           targets.append(g.mid)
 #                   if targets == []:
 #                       pass
 #                   else:
 #                       for target in targets:
 #                           if target in admin:
 #                               pass
 #                           else:
 #                               try:
 #                                   cl.kickoutFromGroup(to,[target])
 #                               except:
 #                                   pass
#
 #               elif msg.text.lower().startswith("ri "):
#                    targets = []
 #                   key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
#                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        try:
#                            cl.sendMessage(to,"來回機票一張ww")
#                            cl.kickoutFromGroup(msg.to,[target])
#                            cl.inviteIntoGroup(to,[target])
#                        except:
#                            cl.sendMessage(to,"Error")
#                elif text.lower() == 'byeall':
 #                   if msg.toType == 2:
 #                       print ("[ 19 ] KICK ALL MEMBER")
#                        _name = msg.text.replace("Byeall","")
#                        gs = cl.getGroup(msg.to)
#                        cl.sendMessage(msg.to,"Sorry guys")
#                        targets = []
#                        for g in gs.members:
#                            if _name in g.displayName:
#                                targets.append(g.mid)
#                        if targets == []:
 #                           cl.sendMessage(msg.to,"Not Found")
 #                       else:
 #                           for target in targets:
 #                               try:
 #                                   cl.kickoutFromGroup(msg.to,[target])
 #                                   print (msg.to,[g.mid])
 #                               except:
#                                    cl.sendMessage(msg.to,"")
#                elif ("Gn " in msg.text):
#                    if msg.toType == 2:
#                        X = cl.getGroup(msg.to)
#                        X.name = msg.text.replace("Gn ","")
#                        cl.updateGroup(X)
#                    else:
#                        cl.sendMessage(msg.to,"It can't be used besides the group.")
#                elif text.lower() == 'cancel':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        gMembMids = [contact.mid for contact in group.invitee]
#                    for _mid in gMembMids:
#                        cl.cancelGroupInvitation(msg.to,[_mid])
#                    cl.sendMessage(msg.to,"已取消所有邀請!")
                elif ("Inv " in msg.text):
                    if msg.toType == 2:
                        midd = msg.text.replace("Inv ","")
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(to,[midd])
                elif ("Invr " in msg.text):
                    if msg.toType == 2:
                        midd = msg.text.replace("Invr ","")
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoRoom(to,[midd])
#==============================================================================#
                elif text.lower() == 'tagall':
                    if settings["tagtag"] == True:
                        group = cl.getGroup(msg.to)
                        nama = [contact.mid for contact in group.members]
                        k = len(nama)//20
                        for a in range(k+1):
                            txt = u''
                            s=0
                            b=[]
                            for i in group.members[a*20 : (a+1)*20]:
                                b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                                s += 7
                                txt += u'@Alin \n'
                            cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                    else:
                        cl.sendMessage(to,"zone已關閉全體標記功能,謹慎評估後可私訊zone請求開啟!!")
                elif text.lower() == 'zt':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            sendMessageWithMention(to,target)
                elif text.lower() == 'zm':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for mi_d in targets:
                           cl.sendContect(to,mi_d)
                elif text.lower() == 'setread':
                    cl.sendMessage(msg.to, "已讀點設置成功")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                elif text.lower() == "cancelread":
                    cl.sendMessage(to, "已讀點已刪除")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif msg.text in ["checkread","Checkread"]:
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "[已讀順序]%s\n\n[已讀的人]:\n%s\n查詢時間:[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "請輸入setread")

#==============================================================================#
                elif msg.text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["blacklist"][target] = True
                            cl.sendMessage(msg.to,"已加入黑單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"添加失敗 !")
                            break
                elif "Ban:" in msg.text:
                    mmtxt = text.replace("Ban:","")
                    try:
                        ban["blacklist"][mmtext] = True
                        cl.sendMessage(msg.to,"已加入黑單!")
                    except:
                        cl.sendMessage(msg.to,"添加失敗 !")
                elif msg.text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["blacklist"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'banlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'nkban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"Blacklist kicked out")
                elif text.lower() == 'cleanban':
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                elif text.lower() == 'banmidlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n╠ "+mi_d
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")


#==============================================================================#
#                elif "Fbc:" in msg.text:
#                    bctxt = text.replace("Fbc:","")
#                    t = cl.getAllContactIds()
#                    for manusia in t:
#                        cl.sendMessage(manusia,(bctxt))
#                elif "Gbc:" in msg.text:
#                    bctxt = text.replace("Gbc:","")
#                    n = cl.getGroupIdsJoined()
#                    for manusia in n:
#                        cl.sendMessage(manusia,(bctxt))
                elif "Copy " in msg.text:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            contact = cl.getContact(target)
                            X = contact.displayName
                            profile = cl.getProfile()
                            profile.displayName = X
                            cl.updateProfile(profile)
                            cl.sendMessage(to, "Success...")
                            Y = contact.statusMessage
                            lol = cl.getProfile()
                            lol.statusMessage = Y
                            cl.updateProfile(lol)
                            path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                            P = contact.pictureStatus
                            cl.updateProfilePicture(P)
                        except Exception as e:
                            cl.sendMessage(to, "Failed!")
 #           if text.lower() == 'cc9487':
 #               if sender in ['ua10c2ad470b4b6e972954e1140ad1891']:
 #                   python = sys.executable
 #                   os.execl(python, python, *sys.argv)
 #               else:
 #                   pass
#==============================================================================#
            if msg.contentType == 13:
                if settings["getmid"] == True:
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
                    else:
                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    msg.contentType = 0
                    msg.text = "文章網址：\n" + msg.contentMetadata["postEndUrl"]
                  #  detail = cl.downloadFileURL(to,msg,msg.contentMetadata["postEndUrl"])
                    cl.sendMessage(msg.to,msg.text)
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in ban["mimic"]["target"] and ban["mimic"]["status"] == True and ban["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        cl.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    sendMessageWithMention(to, contact.mid)
                                    cl.sendMessage(to, "本帳歸沅哥管理,如有需要找他可找管理員名單使用「about」指令,屆時會出現最終修改者(非原作者)友資,謝謝!!")
                                break
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                    elif msg.contentType == 7:
                        stk_id = msg.contentMetadata['STKID']
                        msg_dict[msg.id] = {"text":"貼圖id:"+str(stk_id),"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)

#==============================================================================#
        if op.type == 65:
            print ("[ 65 ] REREAD")
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            timeNow = datetime.now()
                            timE = datetime.strftime(timeNow,"(%y-%m-%d %H:%M:%S)")
                            try:
                                strt = int(3)
                                akh = int(3)
                                akh = akh + 8
                                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(msg_dict[msg_id]["from"])+"},"""
                                aa = (aa[:int(len(aa)-1)])
                                cl.sendMessage(at, "收回訊息者 @wanping ", contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                            except Exception as e:
                                print(str(e))
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            cl.sendMessage(at,"/n發送時間/n"+strftime("%y-%m-%d %H:%M:%S")+"/n收回時間/n"+timE)                           
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
