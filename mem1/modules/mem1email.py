from gluon import *
from gluon.tools import Mail
import os
from gluon.contrib.appconfig import AppConfig
#from gluon.tools import Auth
# -*- coding: utf-8 -*-
# try something like
def join_email(mem_id, mem_first, address, folder, renew=False): 
    #mail = auth.settings.mailer
    myconf = AppConfig(reload=True)
    mail = Mail()
    mail.settings.server = myconf.get('smtp.server')
    mail.settings.sender = myconf.get('smtp.sender')
    mail.settings.login = myconf.get('smtp.login')
#     mail.settings.tls = myconf.get('smtp.tls') or False
#     mail.settings.ssl = myconf.get('smtp.ssl') or False
    
#     mail = Mail()
#     mail.settings.server = 'smtp.gmail.com:587'
#     mail.settings.sender = 'wpa4membership@gmail.com'
#     mail.settings.login = 'wpa4membership@gmail.com:mbrsstand2gether'
    
    join = "Thank you for joining Woodley Park Archers. "
    if(renew == True): join = "Thank you for renewing with Woodley Park Archers. "
    htmlmsg = u"""<html><p align="left" style="margin-bottom: 0in; line-height: 100%"><font face="Liberation Serif, serif"><font size="2" style="font-size: 11pt" color="black">"""
    htmlmsg += "Hi {},<br>".format(mem_first[0])
    if(len(mem_id) == 1):
        htmlmsg += join
        htmlmsg += "Your member number is {:06d}. ".format(mem_id[0])
    else:
        htmlmsg += join + "<br>"
        for i in range(len(mem_id)):
            htmlmsg += "{}'s member number is {:06d}. <br>".format(mem_first[i], mem_id[i])
    htmlmsg += "Please read the letter from our president below. <br>"
    htmlmsg += "Sam Amundson<br>"
    htmlmsg += "Membership Chair<br>"
    htmlmsg += "Woodley Park Archers<br><br>"
#         htmlmsg = self.textToHtml(text)
    htmlmsg += """<p align="left" style="margin-bottom: 0in; line-height: 100%"><font face="Liberation Serif, serif">
        <font size="2" style="font-size: 11pt"><a href="http://woodleyparkarchers.org/">WoodleyParkArchers.org</a></font></font></p>"""
    htmlmsg += """ <p align="left" style="margin-bottom: 0in; line-height: 100%"><font face="Liberation Serif, serif">
        <font size="2" style="font-size: 11pt"><a href="http://www.facebook.com/pages/Woodley-Park-Archers/131056656971079">Facebook: Woodley Park Archers</a></font></font></p>"""
    htmlmsg += """<img src="cid:photo" />"""
    with open(os.path.join(folder, 'static', 'emailbody.txt'), 'r') as f:
        for line in f:
            htmlmsg += u"""<p align="left" style="margin-bottom: 0in; line-height: 100%"><font face="Liberation Serif, serif"><font size="2" style="font-size: 11pt" color="black">{}</font></font></p>""".format(line.decode('utf-8'))
    htmlmsg += """</html>"""
    mail.send('sam.amundson@gmail.com', 'Woodley Park Archers Membership Confirmation', htmlmsg,
              attachments = mail.Attachment(os.path.join(folder, 'static', 'Header.png'), content_id='photo'),
             bcc=['sam_08123@yahoo.com'])
    return
