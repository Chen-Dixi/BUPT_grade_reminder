#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup

from functools import partial

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,de;q=0.7,pt;q=0.6',
    'Connection': 'keep-alive',
}

class GradeScanner(object):
    def __init__(self,username,password,http_timeout):
        self._session  = requests.Session()
        self._get = partial(self._session.get, headers=HEADERS,timeout=http_timeout)
        self._post = partial(self._session.post, headers=HEADERS, timeout=http_timeout)
        self.username = username
        self.password = password

    def _login(self):
        login_url='http://auth.bupt.edu.cn/authserver/login'

        params = {
            "service":'http://yjxt.bupt.edu.cn/ULogin.aspx'
        }

        def prepare_login():
            response = self._get(login_url,params=params)
            response.encoding='utf-8'
            text = response.text
            soup = BeautifulSoup(text,'html.parser')
            items = soup.find_all('input',attrs={'type': 'hidden'})
            hidden_data = dict(map(lambda i: (i.get('name'), i.get('value')), items))
            return hidden_data
        hidden_data = prepare_login()
        auth_data = dict(
            username=self.username, password=self.password,
            **hidden_data
        )
        response = self._post(login_url, params=params, data=auth_data)

    def fetch_grade(self):
        leftmenu_url='http://yjxt.bupt.edu.cn/Gstudent/leftmenu.aspx?UID='+self.username

        def step1():
            self._login()
            response = self._get(leftmenu_url)
            response.encoding='utf-8'
            leftmenu_html = response.text
            soup = BeautifulSoup(leftmenu_html, 'html.parser')
            script = soup.find_all('script')[-1]
            # 从script中取地址
            pattern = re.compile(r"t:'课程成绩信息查询',url:'(.*?)', ", re.DOTALL)

            # 查成绩的url
            grade_url = 'http://yjxt.bupt.edu.cn/Gstudent/' + pattern.search(script.text).group(1)
            response = self._get(grade_url)
            response.encoding='utf-8'
            return response.text
        def convert_text_to_list(tr):
            tds = tr.find_all('td')
            tds = [tds[1],tds[6]]
            return list(map(lambda i: i.text.strip(), tds))

        grade_html = step1()
        soup = BeautifulSoup(grade_html,'html.parser')
        table = soup.find('table',id="contentParent_dgData")

        trs = table.find_all('tr')
        # title = convert_text_to_list(trs[0])
        classes = list(map(convert_text_to_list, trs[1:]))
        return classes

def make_grade_fetcher(cfg):
    return GradeScanner(cfg.username, cfg.password, cfg.http_timeout)


if __name__ == '__main__':
    test = GradeScanner('2018xxxxxx','xxxxxx',15)
    data = test.fetch_grade()
    print(data)
