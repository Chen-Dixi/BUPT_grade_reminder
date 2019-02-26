#coding=utf-8

import time
import schedule
import threading
from collections import defaultdict

import config as cfg
from fetch_grade import make_grade_fetcher
from send_email import (make_email_sender,
                        convert_list_to_email_text)


class GradeReminder(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self._email_sender = make_email_sender(cfg) #在这个类里面加入一个邮件发送器
        self.__cached_classes = defaultdict(int)  # cache classes which are already known.

    def remind_grade(self):
        def remind_job():
            grade_fetcher = make_grade_fetcher(cfg)
            classes = grade_fetcher.fetch_grade()
            print(classes)
            remind_classes = []
            for class_ in classes:
                if class_[0] not in self.__cached_classes and \
                                    class_[1] != '成绩未录入':
                    self.__cached_classes[class_[0]] = 1
                    remind_classes.append(class_)
            # if exists classes which are not known yet.
            if len(remind_classes) != 0:

                text = convert_list_to_email_text(remind_classes)
                self._email_sender(text)

        assert len(cfg.strategy) == 1, 'wrong format for `strategy`, only support one key!'
        [[type_, number]] = cfg.strategy.items()
        if type_ == 'hours':
            schedule.every(number).hours.do(remind_job)
        elif type_ == 'minutes':
            schedule.every(number).minutes.do(remind_job)
        else:
            raise KeyError('wrong format for `strategy`, only support `hours` and `minutes`!')


def __start_schedule_deamon():
    def schedule_run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=schedule_run) #*target* is the callable object to be invoked by the run()
    t.start()
    t.join()


def main():
    grade_reminder = GradeReminder(cfg)
    grade_reminder.remind_grade()
    # start to run thread
    __start_schedule_deamon()


if __name__ == '__main__':
    main()

