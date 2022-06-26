from urllib.request import urlopen





def search_maximo():
    sn = '192.168.10.'

    for n in range(21, 255):
        ip = sn + str(n)

        try:
            html = urlopen("http://%s/maximo" % ip).read()
        except:
            html = ''


        if str(html).find('maximo') > -1:
            print(ip, 'FOUND!')
        else:
            print(ip, '---')


if __name__ == '__main__':
    search_maximo()