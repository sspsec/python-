import os
import time

import requests
from bs4 import BeautifulSoup

# 创建 image 文件夹
os.makedirs("image", exist_ok=True)

# 初始化请求
session = requests.Session()
headers = {
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Priority": "u=0, i",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.xingfujie.cn/",
    "Connection": "keep-alive",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Dest": "document",
    "Pragma": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "navigate",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-User": "?1",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ee;q=0.6",
    "Sec-Ch-Ua-Mobile": "?0"
}
cookies = {
    "acw_tc": "0a47318e17320118291342143e0044f8fcc8de774f60d82011eac27d1f66d0",
    "login_captcha_image": "%3Cimg+id%3D%22captcha%22+src%3D%22%2Fimages%2Fcaptcha%2F1732011887286.png%22+width%3D%2280%22+height%3D%2230%22+style%3D%22border%3A0%3B%22+%2F%3E",
    "login_captcha_hash": "4f72bb1e37f196eb2f08efd8a4a2af0a",
    "login_captcha_word": "0457af71d950881267207a988e258c23",
    "login_captcha_time": "1732011887286"
}

# 爬取4页内容
base_url = "http://www.xingfujie.cn/web/all,{},0.html"
products = []

for page in range(1, 6):
    url = base_url.format(page)
    response = session.get(url, headers=headers, cookies=cookies, verify=False)
    # print(response.text)
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    for li in soup.find_all('li'):
        product = {}

        # 获取名称
        name = li.find('div', class_='dt')
        product['name'] = name.text.strip() if name else None

        # 获取价格
        price = li.find('div', class_='pp')
        if price:
            price_text = price.text.strip()
            product['price'] = price_text.split('¥')[1].split()[0] if '¥' in price_text else None

        # 获取地址
        market = price.find('span', class_='market') if price else None
        product['address'] = market.text.strip() if market else None

        # 获取图片地址
        img = li.find('img', class_='scrollLoading')
        product['image_url'] = img['data-url'] if img else None

        # 添加到产品列表
        if product['name']:
            products.append(product)

# 保存到文件和下载图片
with open("products.txt", "a+", encoding="utf-8") as file:
    for product in products:
        file.write(f"名称: {product['name']}\n")
        file.write(f"价格: {product['price']}\n")
        file.write(f"地址: {product['address']}\n")
        file.write(f"图片地址: {product['image_url']}\n")
        file.write("-" * 40 + "\n")

        # 下载图片
        if product['image_url']:
            try:
                time.sleep(2)  #
                response = requests.get(product['image_url'], stream=True, headers=headers, cookies=cookies,)
                response.raise_for_status()
                image_name = product['name'].replace('&', '_').replace('/', '_') + ".jpg"
                image_path = os.path.join("image", image_name)
                with open(image_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f"图片下载成功: {image_path}")
            except Exception as e:
                print(f"图片下载失败: {product['image_url']}, 错误: {e}")

print("所有任务完成！")
