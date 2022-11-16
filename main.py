import requests

from lxml import html

url = "https://www.cryptohopper.com/resources/candlestick-patterns/370-identical-three-crows"

payload = {}
headers = {
  'authority': 'www.cryptohopper.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
  'cache-control': 'max-age=0',
  'cookie': 'showed_cookie_consent_new=1; user_cookie_consent_new=functional%2Cmarketing%2Canalytical; _gid=GA1.2.607020890.1664895999; _gaexp=GAX1.2.jTiy3KqJScirm8gE9UFiWQ.19308.1; _hjFirstSeen=1; _hjSession_1464396=eyJpZCI6ImE0NGRjYWM0LTNkNzItNDQ4ZC1hNzFiLTA4MmU5MGRjYmViNCIsImNyZWF0ZWQiOjE2NjQ4OTU5OTk4NDAsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _hjSessionUser_1464396=eyJpZCI6ImM5NzgxNzAwLTliY2MtNWE3ZC04MmQxLTAxZDNiNTBmZDZkMSIsImNyZWF0ZWQiOjE2NjQ4OTU5OTk3NzMsImV4aXN0aW5nIjp0cnVlfQ==; cf_clearance=SHr3ND4ZMxewfnDCdKk0foYRt8NxV18lkOdmRohQrdY-1664896023-0-250; _fbp=fb.1.1664896025991.1364229455; _fw_crm_v=4b962ee2-2642-49cc-82f5-36eba896a34d; __adroll_fpc=fda59ddd549472a6151395506bb7fd3d-1664896027337; ded67d23668366c4e4ae034d74e7a929=hkhrniqh6e6q3487aecagnjpn8; joomla_user_state=logged_in; ch.sessionData=934jhUZWG+zgtHBo4RIfC7oemKr4nGmC1q0jcH5JN3skezojV6pa17VP766D+0TllLPwMGLBGmY3HzeQP9QDKA==; ajs_user_id=651892; ch.user==0nM5gTM1YjOiQWSyV2c1Jye; user_timezone_locale=vi; user_timezone=Asia/Saigon; ajs_anonymous_id=%226cb341a3-d132-4659-972b-8bbfd11cf3ec%22; dash_order_col=0; dash_order_type=asc; user_nightmode=0; _hjIncludedInSessionSample=0; _ga=GA1.2.848853741.1664895999; __ar_v4=H7DWHAT7XNBOTCXLIDJYZ4%3A20221003%3A2%7CP44GGYLGKZDU3J5A6CHKSN%3A20221003%3A3%7C6WADVVMC3ZFWRDPGAOMNIE%3A20221003%3A3%7CNAZA27GIJBGVXO6P4SG4P4%3A20221003%3A1; _ga_1PFDCLSF58=GS1.1.1664896025.1.1.1664896533.0.0.0',
  'referer': 'https://www.cryptohopper.com/academy',
  'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

tree = html.fromstring(response.content)
links = tree.xpath(
    '((//div[@data-id="main"]/div/div)[1]/div)[2]//img[@data-nimg="intrinsic"]/@src')
titles = tree.xpath('((//div[@data-id="main"]/div/div)[1]/div)[2]//a/div//p/text()')

titles = list(map(lambda x: x.replace(' ', '')
                             .replace('-', '')
                             .replace('/', ''), titles))

new_links = []

for link in links:
    if "/static/images/candlestick-patterns" in link:
        if link not in new_links:
            new_links.append('https://www.cryptohopper.com' + link)


list_svg = []
for link in new_links:
    print(link)
    res = requests.request('GET', link)
    list_svg.append(str(res.content))

list_svg = list(map(lambda x: x.replace('#5cc49d', '#14F195')
                    .replace('#e8897e', '#FF5C00')
                    .replace('#72b4c9', '#81D8B3')
                    .replace('#4eb0c6', '#81D8B3')
                    .replace("</svg>'", "</svg>")
                    .replace("b'", ""), list_svg))

for i in range(0, len(list_svg)):
    file_name = str(titles[i]) + '.svg'

    with open(f"candlestick-patterns1\\{file_name}", "w") as f:
        f.write(list_svg[i])
