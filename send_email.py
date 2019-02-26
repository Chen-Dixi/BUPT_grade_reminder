#coding=utf-8

import smtplib
from email.mime.text import MIMEText

from functools import partial


def convert_list_to_email_text(list_):
    text = []
    text.append('您的新成绩如下：<br>')
    for item in list_:
        text.append('课程: {0} <br>'.format(item[0]) + \
                    '成绩: {0} <br>'.format(item[1]))
    return ''.join(text)



def send_email(text=None, mail_sender=None,
                          mail_password=None,
                          mail_host=None,
                          mail_receiver_list=None):
    msg = MIMEText(text, _subtype="html", _charset="utf-8")
    msg["Subject"] = "成绩提醒"
    msg["From"] = "<" + mail_sender + ">"
    msg["To"] = ",".join(mail_receiver_list)

    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(mail_sender, mail_password)
        server.sendmail(mail_sender, mail_receiver_list, msg.as_string())
        server.close()
    except Exception as e:
        print('send mail failed with error: %s' % str(e))
        return False
    return True


def make_email_sender(cfg):
    return partial(send_email, mail_sender=cfg.mail_sender,
                               mail_password=cfg.mail_password,
                               mail_host=cfg.mail_host,
                               mail_receiver_list=cfg.mail_receiver_list)


if __name__ == '__main__':
    import config as cfg
    email_sender = make_email_sender(cfg)
    list_ = [['政治', 'xx']]
    email_sender(convert_list_to_email_text(list_))
