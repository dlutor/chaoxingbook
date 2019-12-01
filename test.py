from chaoxing import Basic

username = 'xxxx'
password = 'xxxxxx'
b = Basic(username, password)
url = 'http://book.chaoxing.com/ebook/detail_8144456069d6dca7b25f25aee4574f571490e5ff7.html'
b.book(url)