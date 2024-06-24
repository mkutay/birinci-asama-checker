import urllib.parse
import urllib.request
import http.cookiejar
import ssl
import csolver

def scrape(sessionId, tc, url, file):
  headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    "DWRSESSIONID": sessionId,
  }

  cookie_jar = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
  urllib.request.install_opener(opener)

  request = urllib.request.Request("https://ebideb.tubitak.gov.tr/dogrula.jpg", headers=headers)
  response = urllib.request.urlopen(request)
  contents = response.read()

  with open(file, "wb") as f:
    f.write(contents)

  captcha = csolver.csolver(file)

  payload = {
    "hdnSinavBilgileriniGetir": 1,
    "TCKimlikNo": tc,
    "sinavYili": 2024,
    "olimpiyatDal.id": 7,
    "olimpiyatSinavTurleri.id": 1,
    "guvenlik": captcha
  }

  data = urllib.parse.urlencode(payload)
  binary_data = data.encode('UTF-8')

  request = urllib.request.Request(url, binary_data, headers)
  response = urllib.request.urlopen(request)
  contents = response.read()
  contents = contents.decode("utf-8")

  b1 = contents.find("açıklanmamıştır.")
  b2 = contents.find("Sayfayı Yazdır")

  if b1 == -1 and b2 == -1: # the captcha solver didn't work or something else
    return 0
  elif b1 == -1 and b2 != -1: # the results are out
    return 1
  else: # the results are not out
    return 2