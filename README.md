# BUPT_grade_reminder
北京邮电大学研究生期末成绩提醒，通过邮件发送成绩推送通知

![image](https://github.com/Chen-Dixi/BUPT_grade_reminder/blob/master/IMG_3994766EC11E-1.jpeg)

#### 程序是从上海科技大学的朋友那里改的，修改了一下抓取方式抓北邮的研究生成绩
上海科技大学成绩提醒仓库：
https://github.com/beaulian/grade-reminder

#### 安装依赖包
```bash
pip install requests bs4 schedule 
```
#### 设置参数
参数设置在`config.py`文件里，各个参数都有注释

#### 运行脚本
```bash
python remind_grade.py &
```

#### 注意
方便大家成绩，但是乱改程序，对研究生系统进行洪水攻击等行为均和本人无关，一切后果自负！
