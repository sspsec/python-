import requests
import json
import os

# 初始化会话
session = requests.Session()

# 请求头和 cookies
headers = {
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Priority": "u=1, i",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/typerank?type_name=%E5%96%9C%E5%89%A7&amp;type=24&amp;interval_id=100:90&amp;action=",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Dest": "empty",
    "Pragma": "no-cache",
    "Sec-Fetch-Mode": "cors",
    "Cache-Control": "no-cache",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ee;q=0.6",
    "Sec-Ch-Ua-Mobile": "?0"
}
cookies = {
    "__utmz": "223695111.1731841511.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "_pk_ses.100001.4cf6": "1",
    "_pk_id.100001.4cf6": "6f512bb9bbc3cb80.1731841511.",
    "douban-fav-remind": "1",
    "__utmb": "223695111.0.10.1731982991",
    "ap_v": "0,6.0",
    "__utmc": "223695111",
    "bid": "VQEDHi0PTJ0",
    "__utma": "223695111.2111578994.1731841511.1731845769.1731982991.3"
}


# 爬取数据的函数
def fetch_movies(limit=20, max_movies=500):
    all_movies = []
    start = 0
    while len(all_movies) < max_movies:
        paramsGet = {
            "start": str(start),
            "limit": str(limit),
            "action": "",
            "type": "24",
            "interval_id": "100:90"
        }
        response = session.get("https://movie.douban.com/j/chart/top_list", params=paramsGet, headers=headers,
                               cookies=cookies)
        if response.status_code == 200:
            try:
                movies = response.json()
                if not movies:  # 如果没有更多数据，提前退出
                    break
                all_movies.extend(movies)
                start += limit  # 更新偏移量
            except Exception as e:
                print("解析数据失败:", e)
                break
        else:
            print(f"请求失败，状态码: {response.status_code}")
            break
    return all_movies[:max_movies]  # 截取最多 max_movies 条数据


# 主程序
def main():
    print("开始爬取电影数据...")
    movies = fetch_movies(limit=20, max_movies=500)

    if movies:
        # 创建文件夹保存图片
        os.makedirs("images", exist_ok=True)

        # 打开文件保存结果
        with open("movies.txt", "w", encoding="utf-8") as file:
            for movie in movies:
                title = movie.get("title", "未知电影")
                score = movie.get("rating", "暂无评分")
                actors = ", ".join(movie.get("actors", []))
                region = movie.get("regions", ["未知地区"])[0]
                image_url = movie.get("cover_url", "")

                # 写入到文本
                file.write(f"电影名: {title}\n")
                file.write(f"评分: {score}\n")
                file.write(f"演员: {actors}\n")
                file.write(f"地区: {region}\n")
                file.write(f"图片链接: {image_url}\n\n")

                # 下载图片
                if image_url:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        sanitized_title = title.replace("/", "_").replace("\\", "_")  # 防止非法文件名
                        with open(f"images/{sanitized_title}.jpg", "wb") as img_file:
                            img_file.write(image_response.content)

        print("数据保存完成！电影信息已写入 movies.txt，图片已保存到 images 文件夹。")
    else:
        print("未获取到电影数据，请检查请求设置。")


if __name__ == "__main__":
    main()
