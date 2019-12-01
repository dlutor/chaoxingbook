from chaoxing import Basic

username = 'xxxx'
password = 'xxxxxx'
b = Basic(username, password)
url = 'http://book.chaoxing.com/ebook/detail_8119069820667abc9c104ed611ea97ec98c38a1c8.html'
b.book(url)