import os
import re
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}


def img_download(content, x=int):
    img_paths = re.findall(r'<li><figure.*?>.*?<a class="preview" href="(.*?)" .*?></a>.*?</figure></li>', content,
                           flags=re.S)
    dirname = 'wallhaven'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    download_url = 'https://w.wallhaven.cc/full/'
    for img_url in img_paths:
        data = []
        download_img_url = download_url + img_url[-6:-4] + '/wallhaven-' + img_url[-6:] + '.jpg'
        file_name = dirname + '/' + download_img_url[-10:]
        start_time = time.time()
        request = requests.get(url=download_img_url, headers=headers, stream=True)

        if request.status_code == 200:
            try:
                with open(file_name, 'wb') as f:
                    f.write(request.content)
                data.append(img_url)
                print("%s download sucess!" % file_name)
            except Exception as e:
                print(e)
        else:
            download_img_url = download_url + img_url[-6:-4] + '/wallhaven-' + img_url[-6:] + '.png'
            file_name = dirname + '/' + download_img_url[-10:]
            request = requests.get(url=download_img_url, headers=headers, stream=True)
            if request.status_code == 200:
                try:
                    with open(file_name, 'wb') as f:
                        f.write(request.content)
                    data.append(img_url)
                    print("%s download sucess!" % file_name)
                except Exception as e:
                    print(e)
        download_time = time.time() - start_time
        download_times.append(download_time)
        data.append(download_time)
        download_data.append(data)

        x += 1
    return x


def request_content(url, headers, page):
    page_url = url + str(page)
    request = requests.get(url=page_url, headers=headers)
    return request.text


def show(x, download_times):
    plt.plot(range(0, x), download_times)
    plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']
    plt.xlabel('下载次数')
    plt.ylabel('下载时间 (秒)')
    plt.title('下载时间折线图')
    plt.show()


def save_to_excel(data_list, file_name):
    df = pd.DataFrame(data_list)
    df.to_excel(file_name, index=False)
    print(f"数据已保存到 {file_name}")


def main():
    x = 0
    page_start = int(input("start page:"))
    page_end = int(input("end page:"))
    url = 'https://wallhaven.cc/toplist?page='
    for page in range(page_start, page_end + 1):
        content = request_content(url, headers, page)
        # print(content)
        x = img_download(content, x)
        time.sleep(0.5)

    show(x, download_times)
    save_to_excel(download_data, 'result.xlsx')


if __name__ == "__main__":
    download_times = []
    download_data = [['下载链接', '下载时间']]
    main()
