import requests

from lxml import html

url = "https://www.cryptohopper.com/resources/technical-indicators/287-absolute-price-oscillator-apo"

payload = {}
headers = {
  'authority': 'www.cryptohopper.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
  'cache-control': 'max-age=0',
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
    if "/static/images/technical-indicators" in link:
        if link not in new_links:
            new_links.append('https://www.cryptohopper.com' + link)

list_svg = []
for link in new_links:
    print(link)
    res = requests.request('GET', link)
    list_svg.append(str(res.content))

list_svg = list(map(lambda x: x.replace('#39b54a', '#14F195')
                    .replace('red', '#FF5C00')
                    .replace('#edb5b0', '#FF5C00')
                    .replace('#8fd8c4', '#14F195')
                    .replace('#ec4945', '#FF5C00')
                    .replace('#49a799', '#14F195')
                    .replace('#ec787d', '#FF5C00')
                    .replace('#b2d98f', '#14F195')
                    .replace('#5cc49d', '#14F195')
                    .replace('#49a69a', '#14F195')
                    .replace('#f1bbc1', '#FF5C00')
                    .replace('#2a2a67', '#81D8B3')
                    .replace('#51b1c6', '#022013')
                    .replace('#303063', '#81D8B3')
                    .replace('#662d91', '#9f83b5')
                    .replace('#d7d7e7', '#ececf1')
                    .replace('#4eb0c6', '#022013')
                    .replace('#cfe6bd', '#81D8B3')
                    .replace('#4eafc7', '#81D8B3')
                    .replace('#2a2a68', '#022013')
                    .replace('#ed1e79', '#FF5C00')
                    .replace('#2a2a65', '#022013')
                    .replace('#82cfde', '#81D8B3')
                    .replace('#efacb2', '#ffa877')
                    .replace('#9f83b5', '#FF5C00')
                    .replace('#4eafc5', '#FF5C00')
                    .replace('#4eb0c5', '#022013')
                    .replace('#2a2b68', '#000905')
                    .replace('<path style="opacity:.58;fill:#022013"', '<path style="opacity:.1;fill:#022013"')
                    .replace("</svg>'", "</svg>")
                    .replace("b'", ""), list_svg))

for i in range(0, len(list_svg)):
    file_name = str(titles[i]) + '.svg'

    with open(f"mau\\{file_name}", "w") as f:
        f.write(list_svg[i])
