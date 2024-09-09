import requests
from lxml import etree
import time
import csv

# 打开CSV文件
with open('questions_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 写入CSV表头
    writer.writerow(['Question', 'Title', 'Date', 'Timestamp'])

    # 遍历页码范围
    for p in range(1,11):
        url = f'https://www.kanxue.com/question-list-0-{p}.htm'

        headers = {
            "Referer": "https://bbs.kanxue.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        }

        response = requests.get(url, headers=headers)

        # 如果请求失败，则跳过该页
        if response.status_code != 200:
            print(f"请求失败，跳过第 {p} 页。")
            continue

        html = etree.HTML(response.text)
        divs = html.xpath("//div[@class='col left_card bg-white']/div")

        # 逐个解析页面中的每个问题
        for div in divs:
            question = "".join(div.xpath("./div[3]/div[1]/div[1]/a/text()")).strip()

            #处理异常数据
            if question == "":
                continue

            title = "".join(div.xpath("./div[3]/div[2]/div[1]/a//text()")).strip()
            data = div.xpath("./div[3]/div[2]/div[2]/span[last()]/text()")[0]
            timestamp = int(time.time() * 1000)  # 获取当前时间的时间戳（毫秒）

            # 将解析的数据写入CSV文件
            writer.writerow([question, title, data, timestamp])

        # 每次抓取完一页，输出进度提示
        print(f"第 {p} 页数据已成功写入 questions_data.csv 文件。")

print("所有页的数据已成功写入 CSV 文件。")
