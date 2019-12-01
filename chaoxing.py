import requests
import os,re
import execjs
import json
import img2pdf
import time
from pathlib import Path
from tqdm import tqdm
class Basic(object):
    def __init__(self,username:str,password:str):
        proxies = {'http': None, 'https': None}
        headers = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                   }
        self.proxies = proxies
        self.headers = headers
        self.username=username
        self.password=password
        self.s = requests.session()
        self.js = self.read('js.js', 'r')
        self.reload()
        if self.verify():
            print('Cookie失效，重新登录')
            self.login()
            self.write_json(self.s.cookies.get_dict(), 'cookies.json')
        else:
            print('登录成功')
        self.dirs='jpg/'
        self.check_dirs(self.dirs)
        self.pdf_dir='pdf/'
        self.check_dirs(self.pdf_dir)

    def check_dirs(self, dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    def reload(self):
        try:
            cookie_dict=self.read_json('cookies.json')
        except:
            cookie_dict={}
        requests.utils.add_dict_to_cookiejar(self.s.cookies, cookie_dict)
    def verify(self):
        url='http://i.mooc.chaoxing.com/'
        r=self.get(url,False)
        locations=r.headers['Location']
        if locations=='http://passport2.chaoxing.com/login?fid=&refer=http://i.mooc.chaoxing.com':
            return 1
        else:
            return 0
    def login(self):
        url='http://passport2.chaoxing.com/login'
        self.get(url)
        code_url='http://passport2.chaoxing.com/num/code'
        code=self.get_captcha(code_url)
        username=self.username
        psw=self.password
        e_psw=self.get_js(psw)
        data={
            'refer_0x001': 'http://i.mooc.chaoxing.com',
                'pid': '-1',
        'pidName':'',
        'fid': '-1',
        'fidName':'',
        'allowJoin': '0',
        'isCheckNumCode': '1',
        'f': '0',
        'productid':'',
        't': 'true',
        'uname': username,
        'password': e_psw,
                  'numcode': code,
        'verCode':''
        }
        login_url='http://passport2.chaoxing.com/login?refer=http%3A%2F%2Fi.mooc.chaoxing.com'
        self.post(login_url,data)
        if self.verify():
            print('登录失败')
            self.login()
    def get_js(self, *args):
        js = execjs.compile(self.js)
        a = js.call('main',args)
        return a
    def get_captcha(self,url):
        self.download(url, 'captha.png')
        os.startfile('captha.png')
        return input('请输入验证码：\n')
    def get(self, url,allow_redirects=True):
        return self.s.get(url=url, headers=self.headers, proxies=self.proxies,allow_redirects=allow_redirects)

    def post(self, url, data):
        return self.s.post(url=url, data=data, headers=self.headers, proxies=self.proxies)

    def download(self, url, path='download'):
        r = self.get(url)
        if r.headers['Content-Type'] != 'image/png':
            time.sleep(1)
            self.download(url, path)
            return 0
        with open(path, 'wb') as f:
            f.write(r.content)
    def read(self, path, mode):
        with open(path, mode) as f:
            data = f.read()
        return data
    def write_json(self,data,path):
        with open(path,'w') as f:
            json.dump(data,f)
        return 0
    def read_json(self,path):
        with open(path,'r') as f:
            data=json.load(f)
        return data
    def book(self,url):
        url=url.replace('detail','read')
        r=self.get(url)
        pattern='<a title="(.*?)"'
        file_name=re.findall(pattern,r.text)[0]
        pattern="goSimple1\('(.*?)'\);"
        redirect_url=re.findall(pattern,r.text)[0]
        r=self.get(redirect_url)
        pattern='_epage = (.*?);'
        pages=re.findall(pattern,r.text)[0]
        print(f'{file_name},共有{pages}页')
        pattern='var str = "(.*?)";'
        sub_url=re.findall(pattern,r.text)[0]
        data=[]
        for i in tqdm(range(int(pages))):
            down_url = 'http://readsvr.chaoxing.com{}{:0>6d}?zoom=0'.format(sub_url, i+1)
            name=self.dirs+str(i+1)+'.png'
            self.download(down_url,name)
            data.append(name)
        self.create_pdf(self.pdf_dir+file_name+'.pdf',data)
        print('成功')
    def create_pdf(self,pdf_name:str,data:list):
        with open(pdf_name,'wb') as f:
            # p=Path(self.dirs)
            # data=[str(i) for i in p.iterdir() if i.suffix == ".png"]
            try:
                f.write(img2pdf.convert(data))
                for i in tqdm(data):
                    Path(i).unlink()
            except Exception as e:
                print(e)
                print('jpg/ 目录为空')



if __name__ == '__main__':
    username='xxxx'
    password='xxxxxx'
    b = Basic(username,password)
    url='http://book.chaoxing.com/ebook/detail_8119069820667abc9c104ed611ea97ec98c38a1c8.html'
    b.book(url)
