# chaoxingbook
超星电子书下载

实现超星阅读电子书下载为PDF

## 用法

安装[Node](https://nodejs.org/en/)

安装依赖
```shell
pip install -r requirements.txt
```

```python
from chaoxing import Basic

username = 'xxxx'   #用户名
password = 'xxxxxx' #密码
b = Basic(username, password)
url = ''            #图书详情页URL
b.book(url)
```

需要登录才能下载全部页，PDF为图片，在`pdf/`目录下
