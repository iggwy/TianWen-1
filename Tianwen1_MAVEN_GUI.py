import time

import matplotlib
from tqdm import tqdm
import csv
import tkinter as tk
from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import os
import pds4_tools



HZ_USTC_ = "TIANWEN1_Data/MOMAG/1Hz_USTC/"
current_path = os.path.abspath(__file__)
# Get the path to the folder where the current script file resides
MARs_data_folder = os.path.dirname(current_path)



def download_TW1_data(instru='M0MAG', accur='32Hz', Time_range=None):
    """
    下载指定 Hz MOMAG 数据文件。
    如果本地 TXT 文件 TW1_MOMAG_filename&id.txt 不存在，则从 GitHub 下载。
    然后解析文件名并下载数据。
    """
    if instru=='MOMAG':
      TXT_FILE = "TW1_MOMAG_filename&id.txt"
      SAVE_DIR = f"TIANWEN1_Data/MOMAG/{accur}/"
      GITHUB_URL = "https://raw.githubusercontent.com/iggwy/Python_YangWang/main/Mars/TianWen-1/TW1_MOMAG_filename&id.txt"
    if instru=='MINPA':
      TXT_FILE = "TW1_MINPA_filename&id.txt"
    # 2C 下载链接模板
    BASE_URL_2C = (
        "https://moon.bao.ac.cn/web/zhmanager/kxsj"
        "?p_p_id=scientificdata_WAR_ScientificDataportlet"
        "&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view"
        "&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1"
        "&p_p_col_count=1&p_p_resource_id=download&id={id_2c}&flagCol=SP&name={name_2c}"
    )

    # 2CL 下载链接模板
    BASE_URL_2CL = (
        "https://moon.bao.ac.cn/web/zhmanager/kxsj"
        "?p_p_id=scientificdata_WAR_ScientificDataportlet"
        "&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view"
        "&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_col_id=column-1"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_lifecycle=2"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bname={name_2c}"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_state=normal"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_col_count=1"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_resource_id=download"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bid={id_2c}"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3BflagCol=SPL"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_mode=view"
        "&_scientificdata_WAR_ScientificDataportlet_amp%3Bp_p_cacheability=cacheLevelPage"
        "&p_p_resource_id=download&id={id_2cl}&flagCol=SPL&name={name_2cl}"
    )

    # HTTP headers with cookie for authentication
    HEADERS = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB-oxendict;q=0.7,en-GB;q=0.6,en-US;q=0.5",
        "connection": "keep-alive",
        "content-length": "30",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "host": "moon.bao.ac.cn",
        "origin": "https://moon.bao.ac.cn",
        "referer": "https://moon.bao.ac.cn/web/zhmanager/kxsj?missionName=HX1&zhName=MOMAG&grade=2C",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }

    def login_and_get_cookies(username, password):
        import os
        import time
        import requests
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        if instru=='MAMOG':
            COOKIE_FILE = "cookies_MAG.txt"  # cookies文件，如果不存在或cookies内容失效将会通过登录自动下载
            TEST_URL = "https://moon.bao.ac.cn/web/zhmanager/kxsj?missionName=HX1&zhName=MOMAG&grade=2C"
            # HTTP headers with cookie for authentication
            HEADERS = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB-oxendict;q=0.7,en-GB;q=0.6,en-US;q=0.5",
                "connection": "keep-alive",
                "content-length": "30",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "host": "moon.bao.ac.cn",
                "origin": "https://moon.bao.ac.cn",
                "referer": "https://moon.bao.ac.cn/web/zhmanager/kxsj?missionName=HX1&zhName=MOMAG&grade=2C",
                "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
                "x-requested-with": "XMLHttpRequest",
            }

        # === 保存 cookies 为 TXT 文件 ===
        def save_cookies(cookie_dict):
            with open(COOKIE_FILE, "w", encoding="utf-8") as f:
                for key, value in cookie_dict.items():
                    f.write(f"{key}={value}\n")

        # === 读取 cookies 从 TXT 文件 ===
        def load_cookies():
            if not os.path.exists(COOKIE_FILE):
                return None

            cookie_dict = {}
            with open(COOKIE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        cookie_dict[key] = value

            return cookie_dict

        # === 检查是否已登录 ===
        def is_logged_in(cookies):
            try:
                response = requests.get(TEST_URL, cookies=cookies, headers=HEADERS)
                return 'id="logoutBtn"' in response.text
            except Exception as e:
                print("测试登录状态失败：", e)
                return False

        # === 登录并获取 cookies ===
        def login_and_get_cookies(username, password):
            driver = webdriver.Edge()
            driver.get(TEST_URL)

            wait = WebDriverWait(driver, 5)

            login_trigger = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "登录")))
            login_trigger.click()

            username_input = wait.until(EC.element_to_be_clickable((By.ID, "_58_login")))
            username_input.clear()
            username_input.send_keys(username)

            password_input = wait.until(EC.element_to_be_clickable((By.ID, "_58_password")))
            password_input.clear()
            password_input.send_keys(password)

            captcha_text = wait.until(EC.visibility_of_element_located((By.ID, "checkCode"))).text
            print(f"验证码识别为：{captcha_text}")
            captcha_input = wait.until(EC.element_to_be_clickable((By.ID, "inputCode")))
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)

            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))
            submit_button.click()

            time.sleep(5)

            cookies = driver.get_cookies()
            cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}

            cookie_dict["ce5web_authcode"] = "5308"

            driver.quit()

            print("登录成功，Cookies 已获取：")
            for k, v in cookie_dict.items():
                print(f"{k}: {v}")

            save_cookies(cookie_dict)
            return cookie_dict

        # === 统一接口：如果无效就重新登录 ===
        def get_cookies(username, password):
            cookie_dict = load_cookies()
            if cookie_dict and is_logged_in(cookie_dict):
                print("已有有效的登录 cookie，无需重新登录")
                return cookie_dict

            print("cookie 无效，正在重新登录...")
            return login_and_get_cookies(username, password)

        # === 使用 cookie 访问 URL 示例 ===
        def access_url_with_cookies(url, cookie_file):
            cookies = {}
            with open(cookie_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        cookies[key] = value

            response = requests.get(url, cookies=cookies)

            if response.status_code == 200:
                print("成功访问页面")
                print(response.text[:200])  # 打印部分返回内容
            else:
                print(f"访问失败，状态码: {response.status_code}")

        # ==== 主程序调用 ====
        if __name__ == "__main__":
            username = "yangwangdsel2025"
            password = "Wang1234."

            cookies = get_cookies(username, password)
            return cookies
            print("\n最终获取的 cookies：")
            for k, v in cookies.items():
                print(f"{k}: {v}")

            # 尝试访问页面
            access_url_with_cookies(TEST_URL, COOKIE_FILE)

    def ensure_txt_exists():
        """检查 TXT 文件是否存在，不存在则从 GitHub 下载"""
        if not os.path.exists(TXT_FILE):
            print(f"{TXT_FILE} not found. Downloading from GitHub...")
            try:
                response = requests.get(GITHUB_URL, stream=True)
                response.raise_for_status()
                with open(TXT_FILE, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded {TXT_FILE} successfully.")
            except requests.RequestException as e:
                print(f"Failed to download TXT file: {e}")
                return False
        return True
    if not ensure_txt_exists():
        return
    # 确保保存目录存在
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 读取 TXT 文件
    filenames_and_ids = []
    with open(TXT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                filenames_and_ids.append((parts[0], parts[1]))

    # 过滤指定 Hz 数据
    filtered_files = [(filename, file_id) for filename, file_id in filenames_and_ids if accur in filename]

    # 按时间范围筛选数据
    if Time_range:
        start_time = datetime.strptime(Time_range[0], "%Y-%m-%dT%H:%M:%S.%f")
        end_time = datetime.strptime(Time_range[1], "%Y-%m-%dT%H:%M:%S.%f")

        def extract_time_from_filename(filename):
            """从文件名提取开始和结束时间"""
            parts = filename.split('_')
            start_str, end_str = parts[5], parts[6]
            start_datetime = datetime.strptime(start_str, "%Y%m%d%H%M%S")
            end_datetime = datetime.strptime(end_str, "%Y%m%d%H%M%S")
            return start_datetime, end_datetime

        def is_within_time_range(filename):
            """检查文件时间范围是否与指定范围有交集"""
            file_start, file_end = extract_time_from_filename(filename)
            return not (file_end < start_time or file_start > end_time)

        filtered_files = [(filename, file_id) for filename, file_id in filtered_files if is_within_time_range(filename)]

    # 下载文件
    start_index = 3792  # Python 是 0-based 索引，所以 3792 表示第 3793 个文件
    for filename, file_id in tqdm(filtered_files[start_index:], desc=f"Downloading {accur} Files"):
        # 处理文件...
        start_index =  start_index +1
        print(start_index)
        # 你的下载逻辑...
        download_url_2C = BASE_URL_2C.format(id_2c=file_id, name_2c=filename)
        download_url_2CL = BASE_URL_2CL.format(id_2c=file_id, name_2c=filename,id_2cl=file_id+'0', name_2cl=filename+'L')
        file_path_2C = os.path.join(SAVE_DIR, filename)
        file_path_2CL = os.path.join(SAVE_DIR, filename+'L')
        COOKIES = login_and_get_cookies('yangwangdsel2025', 'Wang1234.')
        # 跳过已存在的文件
        if os.path.exists(file_path_2C):
            print(f"File already exists: {filename}")
            continue
            # 跳过已存在的文件
        if os.path.exists(file_path_2CL):
                print(f"File already exists: {filename+'L'}")
                continue

        # 下载文件
        try:
            response = requests.get(download_url_2C, headers=HEADERS, cookies=COOKIES, stream=True)
            response.raise_for_status()
            with open(file_path_2C, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
            response = requests.get(download_url_2CL, headers=HEADERS, cookies=COOKIES, stream=True)
            response.raise_for_status()
            with open(file_path_2CL, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {filename+'L'}")
        except requests.RequestException as e:
            print(f"Failed to download {filename+'L'}: {e}")
# 调用函数
#download_TW1_data(instru='MAMOG', accur='32Hz', Time_range=["2020-08-30T00:00:00.000", "2024-09-01T00:00:00.000"])
def doy_to_date(year, day_of_year):
    # How many days of the year are converted to dates
    # The first day of the specified year
    start_of_year = datetime(year, 1, 1)
    # Calculate the target date by increasing the number of days
    target_date = start_of_year + timedelta(days=int(day_of_year) - 1)
    # Format the date as YYYY-MM-DD
    return target_date.strftime('%Y-%m-%d')





import os
import requests
from datetime import datetime, timedelta

def download_maven_data( time_range,instru, accur="1sec"):
    start_date_str, end_date_str = time_range
    if instru=='MAG':
      base_url = "https://search-pdsppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/maven.mag.calibrated/data/pc"
      save_folder= f"MAVEN_Data/MAG/{accur}"
    if instru=='KP':
      base_url="https://search-pdsppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/maven.insitu.calibrated/data"
      save_folder = f"MAVEN_Data/KP"
    # 创建保存目录
    os.makedirs(save_folder, exist_ok=True)

    def download_file_if_exists(url):
        try:
            response = requests.get(url, timeout=20)
            content = response.content
            text_head = content[:200].decode("utf-8", errors="ignore")

            # 检查错误页面内容
            if ("Directory or file does not exist" in text_head or
                "error on line" in text_head or
                "<html" in text_head.lower()):
                return None
            return content

        except Exception as e:
            print(f"❌ 请求失败：{url}，原因：{e}")
            return None

    start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%f")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S.%f")

    date = start_date
    while date <= end_date:
        year = date.strftime("%Y")
        month = date.strftime("%m")
        doy = date.strftime("%j")
        yyyymmdd = date.strftime("%Y%m%d")
        if instru=='MAG':
            prefix = f"mvn_mag_l2_{year}{doy}pc1s_{yyyymmdd}_v01_r01"
            sts_url = f"{base_url}/{accur}/{year}/{month}/{prefix}.sts"
            xml_url = f"{base_url}/{accur}/{year}/{month}/{prefix}.xml"
            sts_path = os.path.join(save_folder, f"{prefix}.sts")
            xml_path = os.path.join(save_folder, f"{prefix}.xml")
        if instru=='KP':
            prefix = f"mvn_kp_insitu_{yyyymmdd}_v22_r01"
            sts_url = f"{base_url}/{year}/{month}/{prefix}.tab"
            xml_url = f"{base_url}/{year}/{month}/{prefix}.xml"
            sts_path = os.path.join(save_folder, f"{prefix}.tab")
            xml_path = os.path.join(save_folder, f"{prefix}.xml")
        # 下载 .sts 文件
        if not os.path.exists(sts_path):
            print(f"\n⬇️ 尝试下载：{prefix}.sts/tab")
            sts_content = download_file_if_exists(sts_url)
            if sts_content:
                with open(sts_path, "wb") as f:
                    f.write(sts_content)
                print(f"✅ 下载成功：{prefix}.sts/tab")

                # 下载对应的 .xml 文件
                print(f"↪️ 尝试下载配套 XML...")
                xml_content = download_file_if_exists(xml_url)
                if xml_content:
                    with open(xml_path, "wb") as f:
                        f.write(xml_content)
                    print(f"✅ 下载成功：{prefix}.xml")
                else:
                    print(f"❌ XML 不存在，跳过：{prefix}.xml")
            else:
                print(f"❌ .sts 不存在，跳过该日全部")
                return None
        else:
            print(f"⏩ 已存在：{prefix}.sts，跳过")

        date += timedelta(days=1)

#def plot_

def webbugs_filenames(instru='MINPA'):

    #爬取网页上的文件名和对应的ID，筛选包含 'HX1-Or_GRAS_MOMAG-DB-1Hz' 或 'HX1-Or_GRAS_MOMAG-DB-32Hz' 的文件，
    #并保存到 file_list.txt。

    if instru == 'MOMAG':
        grade="2C"
        txt_filename = "TW1_MOMAG_filename&id.txt"
    if instru == 'MINPA':
        grade = "2B"
        txt_filename = "TW1_MINPA_filename&id.txt"
    BASE_URL = "https://moon.bao.ac.cn/web/zhmanager/kxsj"  # 可替换
    PARAMS = {
        "p_p_id": "scientificdata_WAR_ScientificDataportlet",
        "p_p_lifecycle": "2",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "p_p_cacheability": "cacheLevelPage",
        "p_p_col_id": "column-1",
        "p_p_col_count": "1",
        "p_p_resource_id": "searchList",
        "missionName": "HX1",
        "grade": grade,
        "zhName": instru,
        "beginDate": "",
        "endDate": "",
        "timeFlag": "0",
        "pageSize": "5",  # 每页记录数，可调整
        "name": "",
        "startQs": "",
        "endQs": "",
        "longitudeBegin": "",
        "longitudeEnd": "",
        "latitudeBegin": "",
        "latitudeEnd": "",
    }

    def extract_filenames_and_ids(json_data):
        """从 JSON 数据中提取符合条件的文件名和对应的 ID"""
        filenames_and_ids = []
        for entry in json_data.get("data", []):
            filename = entry.get("dmName", "")
            file_id = entry.get("dmProductId", "")  # 假设文件ID是dmID字段
            if instru == 'MOMAG':
              if "HX1-Or_GRAS_MOMAG-DB-1Hz" in filename or "HX1-Or_GRAS_MOMAG-DB-32Hz" in filename:
                 filenames_and_ids.append((filename, file_id))
            if instru == 'MINPA':
              if "HX1-Or_GRAS_MINPA-MOD" in filename:
                 filenames_and_ids.append((filename, file_id))
        return filenames_and_ids


    with open(txt_filename, "w", encoding="utf-8") as txtfile:
        total_files = 0
        for page in range(1, 3130):  # 这里只爬取前 5 页，修改为你需要的页数
            print(f"\n正在爬取第 {page} 页...")
            PARAMS["pageNow"] = str(page)

            while True:  # 无限循环，直到请求成功
                try:
                    response = requests.get(BASE_URL, params=PARAMS, timeout=30)
                    response.raise_for_status()  # 如果请求失败，将抛出异常
                    json_data = response.json()
                    filenames_and_ids = extract_filenames_and_ids(json_data)

                    if filenames_and_ids:
                        print(f"第 {page} 页获取到 {len(filenames_and_ids)} 个文件:")
                        for fname, file_id in filenames_and_ids:
                            print(f"  - filename: {fname}, ID: {file_id}")
                            # 保存到txt文件
                            txtfile.write(f"{fname}\t{file_id}\n")
                            # 显式刷新缓冲区
                            txtfile.flush()
                        total_files += len(filenames_and_ids)
                    else:
                        print(f"第 {page} 页没有符合条件的文件")
                    break  # 如果成功获取数据，退出重试循环

                except requests.exceptions.RequestException as e:
                    print(f"第 {page} 页请求失败: {e}，正在重新请求...")  # 输出请求失败信息
                    time.sleep(2)  # 等待一段时间后重试

            time.sleep(1)  # 避免请求过快被封禁
            print(f"\n总共爬取到 {total_files} 个文件名和 ID，已保存在 {txt_filename} 中")
def download_TW1MOMAG_USTC(Time_range, save_dir,accur):
    """
    下载天问一号 MOMAG 1Hz 数据（USTC）。
    :param Time_range: 起止时间（格式如 ["2020-08-30T00:00:00.000", "2024-09-01T00:00:00.000"]）
    :param save_dir: 数据保存路径
    """
    os.makedirs(save_dir, exist_ok=True)

    start = datetime.strptime(Time_range[0], "%Y-%m-%dT%H:%M:%S.%f")
    end = datetime.strptime(Time_range[1], "%Y-%m-%dT%H:%M:%S.%f")
    delta = timedelta(days=1)

    base_url = f"https://space.ustc.edu.cn/dreams/tw1_momag/fetch.php?datafile=TW1_MOMAG_MSO_{accur}" + "_{}_2C_v03.dat"
    current = start
    while current <= end:
        ymd_str = current.strftime("%Y%m%d")
        filename = f"TW1_MOMAG_MSO_{accur}_{ymd_str}_2C_v03.dat"
        url = base_url.format(ymd_str)
        local_path = os.path.join(save_dir, filename)

        if os.path.exists(local_path):
            print(f"已存在，跳过：{filename}")
        else:
            try:
                response = requests.get(url, timeout=30)
                content_text = response.text.strip()
                # 检查是否为网页错误提示
                if "Sorry, the data you request does not exist!" in content_text:
                    print(f"⚠️ 无数据（网页返回提示）：{filename}")
                elif response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ 成功下载：{filename}")
                else:
                    print(f"⚠️ 非 200 状态码，跳过：{filename}")
            except Exception as e:
                print(f"❌ 下载失败 {filename}: {e}")
        current += delta
def Read_TW1_data(instru,Time_range,accur='01Hz'):
    if instru=='MOMAG':
        """
        读取天问一号 MOMAG 数据（USTC）为结构化 np.array。
        :param Time_range: 起止时间（格式如 ["2021-11-16T11:00:33.200", "2024-03-31T11:00:03.400"]）
        :param accur: 数据精度，默认 '01Hz'，可设为 '32Hz'
        :return: MAG，结构化 NumPy 数组，可通过 MAG['UTC'], MAG['Bx'] 等访问
        """
        folder = f"TIANWEN1_Data/MOMAG/{accur}_USTC"
        os.makedirs(folder, exist_ok=True)

        # 转换时间范围
        start_time = datetime.strptime(Time_range[0], "%Y-%m-%dT%H:%M:%S.%f")
        end_time = datetime.strptime(Time_range[1], "%Y-%m-%dT%H:%M:%S.%f")
        dates = [(start_time + timedelta(days=i)).strftime("%Y%m%d")
                 for i in range((end_time.date() - start_time.date()).days + 1)]

        all_data = []

        for date_str in dates:
            fname = f"TW1_MOMAG_MSO_{accur}_{date_str}_2C_v03.dat"
            fpath = os.path.join(folder, fname)

            # 若文件不存在，尝试下载
            if not os.path.exists(fpath):
                download_TW1MOMAG_USTC(
                    [f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}T00:00:00.000",
                     f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}T00:00:00.000"],
                    folder,accur
                )
            if not os.path.exists(fpath):
                print(f"❌ 无数据：{fname}")
                continue

            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # 跳过注释行
            data_lines = [line for line in lines if not line.startswith("#")]
            if not data_lines:
                continue

            for line in data_lines:
                parts = line.split()
                if len(parts) < 12:
                    continue
                all_data.append((
                    parts[0],  # UTC
                    float(parts[2]), float(parts[3]), float(parts[4]),  # Bx, By, Bz
                    float(parts[5]), float(parts[6]), float(parts[7]),  # X, Y, Z
                    float(parts[8]), float(parts[9]), float(parts[10]),  # Roll, Pitch, Yaw
                    parts[11]  # Quality flag
                ))

        # 定义结构化 dtype
        dtype = [
            ('UTC', 'U30'),
            ('Bx', 'f4'), ('By', 'f4'), ('Bz', 'f4'),
            ('X', 'f4'), ('Y', 'f4'), ('Z', 'f4'),
            ('Roll', 'f4'), ('Pitch', 'f4'), ('Yaw', 'f4'),
            ('Flag', 'U2')
        ]
        MAG = np.array(all_data, dtype=dtype)

        # 可选：筛选时间段内数据
        def parse_utc(utc):
            return datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S.%fZ")

        if len(MAG) > 0:
            mask = [(start_time <= parse_utc(utc) <= end_time) for utc in MAG['UTC']]
            MAG = MAG[mask]

        return MAG
    #if instru=='kp':
def Read_MAVEN_data(instru,time_range, time_resolution='1s'):
    if instru=='MAG':
        """
            Parameters:
                time_range: list of str, ["start_time", "end_time"] 格式 "%Y-%m-%dT%H:%M:%S.%f"
                time_resolution: str, 比如 '1s'、'4s'

            Returns:
                dict: 包含时间、磁场、位置数据的字典
            """

        # 1. 解析时间范围
        start_time, end_time = time_range
        start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")
        end_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f")

        # 2. 生成文件夹路径
        base_folder = os.path.join(os.getcwd(), "MAVEN_Data", "MAG", time_resolution + 'ec')

        # 3. 匹配文件名中不同精度的代码
        resolution_code = {
            '1s': 'pc1s',
            '4s': 'pc4s'
        }.get(time_resolution, 'pc1s')  # 默认使用 pc1s

        current_dt = start_dt.date()
        end_date = end_dt.date()

        all_data = {
            'UTC': [],
            'Bx': [],
            'By': [],
            'Bz': [],
            'X': [],
            'Y': [],
            'Z': []
        }

        while current_dt <= end_date:
            y, m, d = current_dt.year, current_dt.month, current_dt.day
            doy = current_dt.timetuple().tm_yday

            file_date_str = f"{y}{doy:03d}"
            xml_name = f"mvn_mag_l2_{file_date_str}{resolution_code}_{y}{m:02d}{d:02d}_v01_r01.xml"
            xml_path = os.path.join(base_folder, xml_name)

            if os.path.exists(xml_path):
                try:
                    structure = pds4_tools.pds4_read(xml_path)
                    MAG_data = structure[1]

                    # 处理时间戳
                    utc_strs = MAG_data['SAMPLE UTC']
                    times = []
                    for t in utc_strs:
                        parts = list(map(int, t.strip().split()))
                        year, doy, hour, minute, second, msec = parts
                        dt = datetime.strptime(f"{year} {doy} {hour} {minute} {second}", "%Y %j %H %M %S")
                        dt = dt.replace(microsecond=msec * 1000)
                        times.append(dt)

                    times = np.array(times)
                    mask = (times >= start_dt) & (times <= end_dt)

                    if np.any(mask):
                        times_str = np.array([dt.strftime("%Y-%m-%dT%H:%M:%S.%f") for dt in times[mask]])
                        bx = MAG_data['BX PLANETOCENTRIC'][mask]
                        by = MAG_data['BY PLANETOCENTRIC'][mask]
                        bz = MAG_data['BZ PLANETOCENTRIC'][mask]
                        x = MAG_data['X'][mask]
                        y = MAG_data['Y'][mask]
                        z = MAG_data['Z'][mask]

                        all_data['UTC'].extend(times_str)
                        all_data['Bx'].extend(bx)
                        all_data['By'].extend(by)
                        all_data['Bz'].extend(bz)
                        all_data['X'].extend(x)
                        all_data['Y'].extend(y)
                        all_data['Z'].extend(z)

                except Exception as e:
                    print(f"读取 {xml_path} 出错: {e}")
            else:
                print(f"文件不存在: {xml_path}")
                download_maven_data(time_range, instru, accur="1sec")
            current_dt += timedelta(days=1)

        # 转换为 numpy 数组
        for key in all_data:
            all_data[key] = np.array(all_data[key])

        return all_data
    #if instru=='kp':
    if instru=='KP':
        """
                   Parameters:
                       time_range: list of str, ["start_time", "end_time"] 格式 "%Y-%m-%dT%H:%M:%S.%f"
                       time_resolution: str, 比如 '1s'、'4s'

                   Returns:
                       dict: 包含时间、磁场、位置数据的字典
                   """

        # 1. 解析时间范围
        start_time, end_time = time_range
        start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")
        end_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f")

        # 2. 生成文件夹路径
        base_folder = os.path.join(os.getcwd(), "MAVEN_Data", "KP")


        current_dt = start_dt.date()
        end_date = end_dt.date()

        all_data = {
            'UTC': [],
            'H_n': [],
            'H_T': [],
            'H_Vx': [],
            'H_Vy': [],
            'H_Vz': [],
            'n_LPW': [],
            'KP_X':[],
            'KP_Y': [],
            'KP_Z': [],
        }

        while current_dt <= end_date:
            y, m, d = current_dt.year, current_dt.month, current_dt.day
            xml_name = f"mvn_kp_insitu_{y}{m:02d}{d:02d}_v22_r01.xml"
            xml_path = os.path.join(base_folder, xml_name)
            if os.path.exists(xml_path):
                try:
                    structure = pds4_tools.pds4_read(xml_path)
                    KP_data = structure[1]

                    # 处理时间戳
                    utc_strs = KP_data['Time (UTC/SCET)']
                    times = []
                    for t in utc_strs:
                        dt = datetime.fromisoformat(t.strip())  # 直接解析 ISO 格式
                        times.append(dt)

                    times = np.array(times)
                    mask = (times >= start_dt) & (times <= end_dt)

                    if np.any(mask):
                        times_str = np.array([dt.strftime("%Y-%m-%dT%H:%M:%S.%f") for dt in times[mask]])
                        H_n = KP_data['SWIA:H+ density'][mask]
                        H_T = KP_data['SWIA:H+ temperature'][mask]
                        H_Vx = KP_data['SWIA:H+ flow velocity MSO X'][mask]
                        H_Vy = KP_data['SWIA:H+ flow velocity MSO Y'][mask]
                        H_Vz = KP_data['SWIA:H+ flow velocity MSO Z'][mask]
                        n_LPW = KP_data['LPW:Electron Density'][mask]
                        KP_X = KP_data['SPICE:Spacecraft MSO X'][mask]
                        KP_Y = KP_data['SPICE:Spacecraft MSO Y'][mask]
                        KP_Z = KP_data['SPICE:Spacecraft MSO Z'][mask]


                        all_data['UTC'].extend(times_str)
                        all_data['H_n'].extend(H_n)
                        all_data['H_T'].extend(H_T)
                        all_data['H_Vx'].extend(H_Vx)
                        all_data['H_Vy'].extend(H_Vy)
                        all_data['H_Vz'].extend(H_Vz)
                        all_data['n_LPW'].extend(n_LPW)
                        all_data['KP_X'].extend(KP_X)
                        all_data['KP_Y'].extend(KP_Y)
                        all_data['KP_Z'].extend(KP_Z)
                except Exception as e:
                    print(f"读取 {xml_path} 出错: {e}")
            else:
                print(f"文件不存在: {xml_path}")
                download_maven_data(time_range,instru='KP')
            current_dt += timedelta(days=1)
        # 转换为 numpy 数组
        for key in all_data:
            all_data[key] = np.array(all_data[key])
        return all_data


time_range_index=1050
def TW1_MAVEN_GUI(Time_range=None, step_days=1/6):
    #—---------获取数据及时间范围
    global time_range_index
    folder = f"TIANWEN1_Data/MOMAG/01Hz_USTC"
    csv_file = os.path.join(folder, "Mars_Timerange_list.csv")
    zoom_range = Time_range
    if Time_range is None:
        if os.path.exists(csv_file):
            time_points_df = pd.read_csv(csv_file)
            time_points = pd.to_datetime(time_points_df['Time']).tolist()
        else:
            if not os.path.exists(folder):
                print(f"文件夹 {folder} 不存在！")
                return
            files = sorted(os.listdir(folder))
            time_points = []
            for file in files:
                try:
                    date_str = file.split('_')[4]
                    file_time = datetime.strptime(date_str, "%Y%m%d")
                    time_points.append(file_time)

                except ValueError:
                    continue
            time_points_df = pd.DataFrame({'Time': time_points})
            time_points_df.to_csv(csv_file, index=False)
        Time_range = [time_points[0], time_points[-1]]
    else:
        if isinstance(Time_range[0], str):
            Time_range = [datetime.strptime(Time_range[0], "%Y-%m-%dT%H:%M:%S.%f"),
                          datetime.strptime(Time_range[1], "%Y-%m-%dT%H:%M:%S.%f")]

    step_minutes = step_days * 24 * 60
    current_index = 0
    time_range_array = []
    cur_t = Time_range[0]
    while cur_t <= Time_range[1]:
        time_range_array.append(cur_t)
        cur_t += timedelta(minutes=step_minutes)
    x_coords = []
    lines1, lines2 = [], []
    can_insert_line = True
    def get_time_slice(start_index, total_points=1):
        start_dt = Time_range[0] + timedelta(minutes=start_index * step_minutes)
        end_dt = start_dt + timedelta(minutes=step_minutes * total_points)
        return [start_dt.strftime("%Y-%m-%dT%H:%M:%S.%f"), end_dt.strftime("%Y-%m-%dT%H:%M:%S.%f")]

    if zoom_range is None:
        current_time_range = get_time_slice(time_range_index)
    else:
        current_time_range = zoom_range
    print( current_time_range )
    TW1_MAG = Read_TW1_data('MOMAG',  current_time_range , accur='01Hz')
    if TW1_MAG is None:
        print("No data returned.")
        time_range_index = time_range_index + 1
        TW1_MAVEN_GUI(Time_range=None, step_days=1/6)


    TW1_Time=[datetime.strptime(t.rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f") for t in TW1_MAG['UTC']]
    TW1_Time = np.array(TW1_Time)
    TW1_Bx, TW1_By, TW1_Bz = TW1_MAG['Bx'], TW1_MAG['By'], TW1_MAG['Bz']
    TW1_Bt = np.sqrt(TW1_Bx**2 + TW1_By**2 + TW1_Bz**2)
    TW1_X, TW1_Y, TW1_Z = TW1_MAG['X'], TW1_MAG['Y'], TW1_MAG['Z']
    if np.mean(np.sqrt(TW1_X**2+TW1_Y**2+TW1_Z**2) )>30 :
        TW1_X, TW1_Y, TW1_Z = TW1_MAG['X']/3390, TW1_MAG['Y']/3390, TW1_MAG['Z']/3390
    #---读取maven数据
    MVMAG = Read_MAVEN_data(instru='MAG', time_range=current_time_range,time_resolution='1s')
    if MVMAG is None:
        print("No data returned.")
        time_range_index = time_range_index + 1
        TW1_MAVEN_GUI(Time_range=None, step_days=1/6)
    MVMAG_Time=[datetime.strptime(t.rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f") for t in MVMAG['UTC']]
    MVMAG_Time = np.array(MVMAG_Time)
    MVMAG_Bx, MVMAG_By, MVMAG_Bz = MVMAG['Bx'], MVMAG['By'], MVMAG['Bz']
    MVMAG_Bt = np.sqrt(MVMAG_Bx**2 + MVMAG_By**2 + MVMAG_Bz**2)
    MVMAG_X, MVMAG_Y, MVMAG_Z = MVMAG['X']/3390, MVMAG['Y']/3390, MVMAG['Z']/3390




    MVKP=Read_MAVEN_data(instru='KP', time_range=current_time_range)
    if MVKP is None:
        print("No data returned.")
        time_range_index = time_range_index + 1
        TW1_MAVEN_GUI(Time_range=None, step_days=1/6)
    MVKP_Time = [datetime.strptime(t.rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f") for t in MVKP['UTC']]
    MVKP_Hn=MVKP['H_n']
    MVKP_HT=MVKP['H_T']
    MVKP_HV = np.sqrt(MVKP['H_Vx']**2 + MVKP['H_Vy']**2 + MVKP['H_Vz']**2)
    MVKP_nLPW=MVKP['n_LPW']
    KP_dis=np.sqrt(MVKP['KP_X']**2 + MVKP['KP_Y']**2 + MVKP['KP_Z']**2)-3396


    # —---------绘制界面------------------------------------
    # Create main window
    root = tk.Tk()
    root.title("Interactive Plot")
    root.geometry("1800x1800+800+100")  # 宽600，高1200，距离屏幕左300，上100
    root.configure(bg='#f0f0f0')
    #
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', font=('Helvetica', 12), padding=10, background='#4CAF50', foreground='white')
    style.map('TButton', background=[('active', '#45a049')])
    style.configure('TLabel', font=('Helvetica', 12), background='#f0f0f0')
    style.configure('TFrame', background='#f0f0f0')
   # 创建图形和子图
    fig = plt.figure(figsize=(4, 4), dpi=100)
    # 第一个子图
    ax1 = fig.add_axes([0.05, 0.85, 0.6, 0.1])  # [left, bottom, width, height]
    ax1.plot(TW1_Time, TW1_Bt, 'black', linewidth=1)
    ax1.set_ylabel('Bt', fontsize=12)
    ax1.get_xaxis().set_visible(False)
    # 提取第一个时间戳并格式化为年-月-日的形式
    first_timestamp = datetime.strptime(TW1_MAG['UTC'][0].rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
    formatted_title = first_timestamp.strftime("%Y-%m-%d")  # 年-月-日格式
    # 设置ax1的标题
    ax1.set_title(formatted_title,fontsize=20)

    # 在图框左上角标注“Tianwen-1”
    ax1.text(0.01, 0.95, 'TianWen-1', transform=ax1.transAxes,
             fontsize=17, verticalalignment='top')
    ax1.set_xlim(TW1_Time[0], TW1_Time[-1])
    ax1.tick_params(axis='y', labelsize=4)


    # 第二个子图
    ax2 = fig.add_axes([0.05, 0.75, 0.6, 0.1])  # [left, bottom, width, height]
    ax2.plot(TW1_Time,TW1_Bx, linewidth=1, label='Bx',color='red')
    ax2.plot(TW1_Time, TW1_By, linewidth=1, label='By',color='green')
    ax2.plot(TW1_Time, TW1_Bz, linewidth=1, label='Bz', color='blue')
    ax2.get_xaxis().set_visible(False)
    ax2.set_xlim(TW1_Time[0], TW1_Time[-1])
    ax2.text(-0.05, 0.75, r'$\mathrm{B_{X}}$', color='red', transform=ax2.transAxes, ha='center', va='center',
             fontsize=12)
    ax2.text(-0.05, 0.5, r'$\mathrm{B_{Y}}$', color='green', transform=ax2.transAxes, ha='center', va='center',
             fontsize=12)
    ax2.text(-0.05, 0.25, r'$\mathrm{B_{Z}}$', color='blue', transform=ax2.transAxes, ha='center', va='center',
             fontsize=12)

    # 第三个子图 - XY 轨迹图
    ax3 = fig.add_axes([0.7, 0.7, 0.25, 0.25])  # [left, bottom, width, height] 右上角正方形
    ax3.plot(TW1_X, TW1_Z, color='darkblue', linewidth=1, label='TianWen-1')
    ax3.plot(MVMAG_X, MVMAG_Z, color='darkgreen', linewidth=1, label='MAVEN')  # 新增 MAVEN轨迹
    ax3.set_xlabel('X [$R_M$]')
    ax3.set_ylabel('Z [$R_M$]')
    ax3.set_xlim(-5, 5)
    ax3.set_ylim(-5, 5)
    # ax3.set_aspect('equal')  # 正方形坐标
    ax3.grid(True)
    ax3.set_title("XZ Plane")
    # ==== 添加极坐标形式的弓激波边界（根据你的拟合结果） ====
    L = 2.04  # 拟合出的 L
    e = 1.03  # 拟合出的 ε
    X0 = 0.64  # 拟合出的 X0
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = L / (1 + e * np.cos(theta))
    # 极坐标转笛卡尔，注意焦点在 X0 位置
    X_bs = X0 + r * np.cos(theta)
    Z_bs = r * np.sin(theta)
    # 可选：限制在可视范围内
    mask = (X_bs > -10) & (X_bs < 10) & (np.abs(Z_bs) < 10)
    ax3.plot(X_bs[mask], Z_bs[mask], color='red', linestyle='-.', linewidth=1, label='BS')
    # ==== 添加极坐标形式的弓激波边界（根据你的拟合结果） ====
    L = 0.96  # 拟合出的 L
    e = 0.90  # 拟合出的 ε
    X0 = 0.78  # 拟合出的 X0
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = L / (1 + e * np.cos(theta))
    # 极坐标转笛卡尔，注意焦点在 X0 位置
    X_mp = X0 + r * np.cos(theta)
    Z_mp = r * np.sin(theta)
    # 可选：限制在可视范围内
    mask = (X_mp > -10) & (X_mp < 10) & (np.abs(Z_mp) < 10)
    ax3.plot(X_mp[mask], Z_mp[mask], color='black', linestyle='-.', linewidth=1, label='MPB')
    # 添加图例
    ax3.legend(loc='upper right', fontsize=8, frameon=True)
    # 火星圆形
    mars = plt.Circle((0, 0), 1, color='orangered', fill=True, alpha=0.5, label='Mars')
    ax3.add_patch(mars)


    # 第四个子图 - YZ 轨迹图
    ax4 = fig.add_axes([0.7, 0.4, 0.25, 0.25])  # 右下角正方形
    ax4.plot(TW1_X, TW1_Y, color='darkblue', linewidth=1, label='TianWen-1')
    ax4.plot(MVMAG_X, MVMAG_Y, color='darkgreen', linewidth=1,  label='MAVEN')  # 新增 MAVEN轨迹
    ax4.set_xlabel('X [$R_M$]')
    ax4.set_ylabel('Y [$R_M$]')
    ax4.set_xlim(-5, 5)
    ax4.set_ylim(-5, 5)
    # ax4.set_aspect('equal')
    # ==== 添加极坐标形式的弓激波边界（根据你的拟合结果） ====
    L = 2.04  # 拟合出的 L
    e = 1.03  # 拟合出的 ε
    X0 = 0.64  # 拟合出的 X0
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = L / (1 + e * np.cos(theta))
    # 极坐标转笛卡尔，注意焦点在 X0 位置
    X_bs = X0 + r * np.cos(theta)
    Z_bs = r * np.sin(theta)
    # 可选：限制在可视范围内
    mask = (X_bs > -10) & (X_bs < 10) & (np.abs(Z_bs) < 10)
    ax4.plot(X_bs[mask], Z_bs[mask], color='red', linestyle='-.', linewidth=1, label='BS')
    # ==== 添加极坐标形式的弓激波边界（根据你的拟合结果） ====
    L = 0.96  # 拟合出的 L
    e = 0.90  # 拟合出的 ε
    X0 = 0.78  # 拟合出的 X0
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = L / (1 + e * np.cos(theta))
    # 极坐标转笛卡尔，注意焦点在 X0 位置
    X_mp = X0 + r * np.cos(theta)
    Z_mp = r * np.sin(theta)
    # 可选：限制在可视范围内
    mask = (X_mp > -10) & (X_mp < 10) & (np.abs(Z_mp) < 10)
    ax4.plot(X_mp[mask], Z_mp[mask], color='black', linestyle='-.', linewidth=1, label='MPB')
    # 添加图例
    #ax4.legend(loc='upper right', fontsize=8, frameon=True)
    ax4.grid(True)
    ax4.set_title("XY Plane")
    # 火星圆形
    mars2 = plt.Circle((0, 0), 1, color='orangered', fill=True, alpha=0.5, label='Mars')
    ax4.add_patch(mars2)



    # 第五个子图
    ax5 = fig.add_axes([0.05, 0.65, 0.6, 0.1])  # [left, bottom, width, height]
    ax5.plot(MVMAG_Time,MVMAG_Bt, 'black', linewidth=1, label='Bt')
    ax5.set_ylabel('Bt', fontsize=12)
    ax5.get_xaxis().set_visible(False)
    # 在图框左上角标注“Tianwen-1”
    ax5.text(0.01, 0.95, 'MAVEN', transform=ax5.transAxes,
             fontsize=17, verticalalignment='top')
    ax5.set_xlim(TW1_Time[0], TW1_Time[-1])
    ax5.set_ylim(0, 25)




    # 第六个子图
    ax6 = fig.add_axes([0.05, 0.55, 0.6, 0.1])  # [left, bottom, width, height]
    ax6.plot(MVMAG_Time,MVMAG_Bx, linewidth=1, label='Bx',color='red')
    ax6.plot(MVMAG_Time,MVMAG_By, linewidth=1, label='By',color='green')
    ax6.plot(MVMAG_Time,MVMAG_Bz, linewidth=1, label='Bz',color='blue')
    ax6.get_xaxis().set_visible(False)
    ax6.set_xlim(TW1_Time[0], TW1_Time[-1])
    ax6.set_ylim(-30, 30)
    ax6.text(-0.05, 0.75, r'$\mathrm{B_{X}}$', color='red', transform=ax2.transAxes, ha='center', va='center',
             fontsize=12)
    ax6.text(-0.05, 0.5, r'$\mathrm{B_{Y}}$', color='green', transform=ax2.transAxes, ha='center', va='center',
             fontsize=12)
    ax6.text(-0.05, 0.25, r'$\mathrm{B_{Z}}$', color='blue', transform=ax2.transAxes, ha='center', va='center',
             fontsize=12)


    # 第七个子图
    ax7 = fig.add_axes([0.05, 0.45, 0.6, 0.1])  # [left, bottom, width, height]
    ax7.plot(MVKP_Time,MVKP_Hn, linewidth=1, label='H+ density')
    ax7.set_ylabel(r'H$^+$ density', fontsize=12)
    ax7.get_xaxis().set_visible(False)
    ax7.set_xlim(TW1_Time[0], TW1_Time[-1])

    # 第七个子图
    ax8 = fig.add_axes([0.05, 0.35, 0.6, 0.1])  # [left, bottom, width, height]
    ax8.plot(MVKP_Time,MVKP_HT, 'black', linewidth=1)
    ax8.set_ylabel(r'H$^+$ T', fontsize=12)
    ax8.get_xaxis().set_visible(False)
    ax8.set_xlim(TW1_Time[0], TW1_Time[-1])

    # 第9个子图
    ax9 = fig.add_axes([0.05, 0.25, 0.6, 0.1])  # [left, bottom, width, height]
    ax9.plot(MVKP_Time,MVKP_HV, 'black', linewidth=1)
    ax9.set_ylabel(r'H$^+$ V', fontsize=12)
    ax9.get_xaxis().set_visible(False)
    ax9.set_xlim(TW1_Time[0], TW1_Time[-1])

    # 第9个子图
    ax10 = fig.add_axes([0.05, 0.15, 0.6, 0.1])  # [left, bottom, width, height]
    ax10.plot(MVKP_Time,MVKP_nLPW, 'black', linewidth=1)
    # 设置横轴格式为 'HH:mm'
    ax10.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax10.set_ylabel(r'e$^-$ density', fontsize=12)
    ax10.set_xlim(TW1_Time[0], TW1_Time[-1])


    # 获取主图时间坐标（用于插值）
    xticks = ax10.get_xticks()
    xticks_datetime = [dt.replace(tzinfo=None) for dt in matplotlib.dates.num2date(xticks)]
    xticks_datetime64 = np.array(xticks_datetime, dtype='datetime64[ns]')

    # 插值 KP_dis（确保时间是 numpy 数组）
    MVKP_Time = np.array(MVKP_Time, dtype='datetime64[ns]')
    if len(MVKP_Time) == 0 or len(KP_dis) == 0:
        print("Error: MVKP_Time or KP_dis is empty.")
        time_range_index=time_range_index+1
        print(time_range_index)
        TW1_MAVEN_GUI()# 或者其他处理逻辑
    dis_interp = np.interp(
        xticks_datetime64.astype('datetime64[s]').astype(float),
        MVKP_Time.astype('datetime64[s]').astype(float),
        KP_dis
    )


    # 添加新的距离轴（❗不 sharex）
    ax10_bottom = fig.add_axes([0.05, 0.12, 0.6, 0.001])  # 不用 sharex
    ax10_bottom.set_xlim(ax10.get_xlim())  # 仍然和主图对齐
    ax10_bottom.set_xticks(xticks)
    ax10_bottom.set_xticklabels([f"{d:.0f}" for d in dis_interp], fontsize=10)
    ax10_bottom.set_yticks([])
    ax10_bottom.set_xlabel("MAVEN-MARs Surface (km)", fontsize=12)

    # 第四个子图 - YZ 轨迹图
    ax11 = fig.add_axes([0.7, 0.35-0.125, 0.25, 0.125])  # 右下角正方形
    ax11.plot(TW1_X, np.sqrt(TW1_Y**2+TW1_Z**2), color='darkblue', linewidth=1, label='TianWen-1')
    ax11.plot(MVMAG_X, np.sqrt(MVMAG_Y**2+MVMAG_Z**2), color='darkgreen', linewidth=1, label='MAVEN')  # 新增 MAVEN轨迹
    ax11.set_xlabel('X [$R_M$]')
    ax11.set_ylabel('YZ [$R_M$]')
    ax11.set_xlim(-5, 5)
    ax11.set_ylim(0, 5)
    # ax4.set_aspect('equal')
    # ==== 添加极坐标形式的弓激波边界（根据你的拟合结果） ====
    L = 2.04  # 拟合出的 L
    e = 1.03  # 拟合出的 ε
    X0 = 0.64  # 拟合出的 X0
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = L / (1 + e * np.cos(theta))
    # 极坐标转笛卡尔，注意焦点在 X0 位置
    X_bs = X0 + r * np.cos(theta)
    Z_bs = r * np.sin(theta)
    # 可选：限制在可视范围内
    mask = (X_bs > -10) & (X_bs < 10) & (np.abs(Z_bs) < 10)
    ax11.plot(X_bs[mask], Z_bs[mask], color='red', linestyle='-.', linewidth=1, label='BS')
    # ==== 添加极坐标形式的弓激波边界（根据你的拟合结果） ====
    L = 0.96  # 拟合出的 L
    e = 0.90  # 拟合出的 ε
    X0 = 0.78  # 拟合出的 X0
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = L / (1 + e * np.cos(theta))
    # 极坐标转笛卡尔，注意焦点在 X0 位置
    X_mp = X0 + r * np.cos(theta)
    Z_mp = r * np.sin(theta)
    # 可选：限制在可视范围内
    mask = (X_mp > -10) & (X_mp < 10) & (np.abs(Z_mp) < 10)
    ax11.plot(X_mp[mask], Z_mp[mask], color='black', linestyle='-.', linewidth=1, label='MPB')
    # 添加图例
    # ax11.legend(loc='upper right', fontsize=8, frameon=True)
    # 火星圆形
    mars2 = plt.Circle((0, 0), 1, color='orangered', fill=True, alpha=0.5, label='Mars')
    ax11.add_patch(mars2)
    ax11.grid(True)
    ax11.set_title("X-YZ Plane")



    # Increase the line thickness and enlarge the labels
    ax1.spines['top'].set_linewidth(1)
    ax1.spines['right'].set_linewidth(1)
    ax1.spines['left'].set_linewidth(1)
    ax1.spines['bottom'].set_linewidth(1)

    ax2.spines['top'].set_linewidth(1)
    ax2.spines['right'].set_linewidth(1)
    ax2.spines['left'].set_linewidth(1)
    ax2.spines['bottom'].set_linewidth(1)



    # Modify tick label font size
    for ax in [ax1, ax2]:
        ax.tick_params(axis='both', labelsize=16)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)
    # Saves a list of vertical horizontal coordinates and vertical objects
    lines1 = []
    lines2 = []
    lines5 = []  # 新增 line5
    lines6 = []  # 新增 line5
    lines7 = []
    lines8 = []
    lines9 = []
    lines10 = []

    x_coords = []  # 存储 X 坐标

    # A flag variable that controls whether a vertical bar can be inserted
    can_insert_line = True

    # A function that handles click events
    def on_click(event):
        nonlocal can_insert_line
        if event.inaxes and can_insert_line:
            click_x = mdates.num2date(event.xdata).replace(tzinfo=None)
            nearest_x = min(TW1_Time, key=lambda x_point: abs(x_point - click_x))
            line1 = ax1.axvline(x=nearest_x, color='r', linestyle='--')
            line2 = ax2.axvline(x=nearest_x, color='r', linestyle='--')
            line5 = ax5.axvline(x=nearest_x, color='b', linestyle='--')  # Add the new vertical line (line5)
            line6 = ax6.axvline(x=nearest_x, color='b', linestyle='--')  # Add the new vertical line (line5)
            line7 = ax7.axvline(x=nearest_x, color='b', linestyle='--')  # Add the new vertical line (line5)
            line8 = ax8.axvline(x=nearest_x, color='b', linestyle='--')  # Add the new vertical line (line5)
            line9 = ax9.axvline(x=nearest_x, color='b', linestyle='--')  # Add the new vertical line (line5)
            line10 = ax10.axvline(x=nearest_x, color='b', linestyle='--')  # Add the new vertical line (line5)
            x_coords.append(nearest_x)
            lines1.append(line1)
            lines2.append(line2)
            lines5.append(line5)  # Add line5 to the list
            lines6.append(line6)  # Add line5 to the list
            lines7.append(line7)  # Add line5 to the list
            lines8.append(line8)  # Add line5 to the list
            lines9.append(line9)  # Add line5 to the list
            lines10.append(line10)  # Add line5 to the list
            if len(lines1) == 2:
                can_insert_line = False
            canvas.draw()

    # Bind click event
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Save the function to CSV file
    def save_to_csv():
        global time_range_index
        file_path = "time_coords.csv"
        new_data = [time_range_index] + x_coords
        if os.path.isfile(file_path):
            # Reading CSV file
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
                # Check whether there is a row corresponding to the current time range index
                for i, line in enumerate(lines):
                    if i > 0 and int(line[0]) == time_range_index + 1:
                        # Replace the data in the current row
                        lines[i] = new_data
                        break
                else:
                    # If there is no row corresponding to the current time_range_index, a new row is added
                    lines.append(new_data)
            # Write the CSV file again
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)
        else:
            # If the file does not exist, write the new data directly
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["number", "X Coordinate 1", "X Coordinate 2", "type"])
                writer.writerow(new_data)
        print(f"Coordinates saved to {file_path}")

    # Function to clear vertical lines
    def clear_lines():
        for line1, line2, line5,line6,line7, line8, line9,line10 in zip(lines1, lines2, lines5,lines6,lines7, lines8, lines9,lines10):
            line1.remove()
            line2.remove()
            line5.remove()  # Remove line5
            line6.remove()
            line7.remove()
            line8.remove()  # Remove line5
            line9.remove()
            line10.remove()
        lines1.clear()
        lines2.clear()
        lines5.clear()  # Clear lines5
        lines6.clear()
        lines7.clear()
        lines8.clear()  # Clear lines5
        lines9.clear()
        lines10.clear()
        x_coords.clear()
        canvas.draw()
        nonlocal can_insert_line
        can_insert_line = True

    # Define amplification function
    def zoom_in():
        if x_coords:
            x_min = min(x_coords)
            x_max = max(x_coords)
            time_range = (TW1_Time >= x_min) & (TW1_Time <= x_max)
            bt_range = TW1_Bt[time_range]
            bx_range = TW1_Bx[time_range]
            by_range = TW1_By[time_range]
            bz_range = TW1_Bz[time_range]
            ax1.set_xlim(x_min, x_max)
            ax2.set_xlim(x_min, x_max)
            ax5.set_xlim(x_min, x_max)
            ax6.set_xlim(x_min, x_max)
            ax7.set_xlim(x_min, x_max)
            ax8.set_xlim(x_min, x_max)
            ax9.set_xlim(x_min, x_max)
            ax10.set_xlim(x_min, x_max)
            ax1.set_ylim(min(bt_range), max(bt_range))
            ax2.set_ylim(min(np.concatenate([bx_range, by_range, bz_range])),
                         max(np.concatenate([bx_range, by_range, bz_range])))
            time_range = (MVMAG_Time >= x_min) & (MVMAG_Time <= x_max)
            bx_range = MVMAG_Bx[time_range]
            by_range = MVMAG_By[time_range]
            bz_range = MVMAG_Bz[time_range]

            # ✅ 更新图10下方距离坐标轴 ax10_bottom
            xticks = ax10.get_xticks()
            xticks_datetime = [dt.replace(tzinfo=None) for dt in matplotlib.dates.num2date(xticks)]
            xticks_datetime64 = np.array(xticks_datetime, dtype='datetime64[ns]')

            MVKP_Time_np = np.array(MVKP_Time, dtype='datetime64[ns]')
            KP_dis_interp = np.interp(
                xticks_datetime64.astype('datetime64[s]').astype(float),
                MVKP_Time_np.astype('datetime64[s]').astype(float),
                KP_dis
            )

            ax10_bottom.set_xlim(x_min, x_max)
            ax10_bottom.set_xticks(xticks)
            ax10_bottom.set_xticklabels([f"{d:.0f}" for d in KP_dis_interp], fontsize=10)


            clear_lines()
            canvas.draw()

    # Definition reduction function
    def zoom_out():
        ax1.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax2.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax5.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax6.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax7.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax8.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax9.set_xlim(TW1_Time[0], TW1_Time[-1])
        ax10.set_xlim(TW1_Time[0], TW1_Time[-1])

        ax1.set_ylim(min(TW1_Bt), max(TW1_Bt))
        ax2.set_ylim(min([min(TW1_Bx), min(TW1_By), min(TW1_Bz)]),
                     max([max(TW1_Bx), max(TW1_By), max(TW1_Bz)]))
        nonlocal can_insert_line
        can_insert_line = True
        clear_lines()
        canvas.draw()

    # Create button frame
    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

    # Create button
    clear_button = ttk.Button(button_frame, text="Clear Lines/清除竖线", command=clear_lines)
    clear_button.grid(row=0, column=0, padx=10, pady=10)

    save_button = ttk.Button(button_frame, text="Save to CSV/保存时间点", command=save_to_csv)
    save_button.grid(row=0, column=1, padx=10, pady=10)

    zoom_button = ttk.Button(button_frame, text="Zoom In/放大", command=zoom_in)
    zoom_button.grid(row=0, column=2, padx=10, pady=10)

    zoom_out_button = ttk.Button(button_frame, text="Zoom Out/缩小", command=zoom_out)
    zoom_out_button.grid(row=0, column=3, padx=10, pady=10)

    # Define the Last button function
    def last_plot():
        global time_range_index
        if time_range_index > 0:
            time_range_index -= 1
            print(time_range_index)
            root.destroy()
            TW1_MAVEN_GUI(Time_range=None)
    # Define the Next button function
    def next_plot():
        global time_range_index
        if time_range_index >= 0 :
            time_range_index += 1
            print(time_range_index)
            root.destroy()
            TW1_MAVEN_GUI(Time_range=None)
        # Save the figure as an image to the "G:/picture" folder

    def save_image():
        save_dir = MARs_data_folder+"\picture"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)  # Create the directory if it doesn't exist
        save_path = os.path.join(save_dir, f"MAVEN_TianWen1_{time_range_index}_{current_time_range[0][0:10]}.png")
        # 确保完全渲染
        fig.savefig(save_path, dpi=130)
        print(f"Plot saved to {save_path}")

        # 清理并关闭当前图形对象，释放内存
        plt.clf()  # 清空当前图形
        plt.close()  # 关闭当前图形，释放内存

        # Add the save image button
    next_button = ttk.Button(button_frame, text="Next/下一张", command=next_plot)
    next_button.grid(row=0, column=4, padx=10, pady=10)
    last_button = ttk.Button(button_frame, text="Last/上一张", command=last_plot)
    last_button.grid(row=0, column=5, padx=10, pady=10)
    save_image_button = ttk.Button(button_frame, text="Save Image/保存图片", command=save_image)
    save_image_button.grid(row=0, column=6, padx=10, pady=10)
    # Label information
    marked_label = ttk.Label(button_frame, text="")
    marked_label.grid(row=0, column=7, padx=10, pady=10)

    # Check if it is marked
    def check_marked():
        global time_range_index
        file_path = "time_coords.csv"
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:  # 检查文件是否存在且不为空
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # 跳过头行
                lines = list(reader)
                marked = False
                for line in lines:
                    if len(line) > 0 and int(line[0]) == time_range_index + 1:
                        marked = True
                        break
                if marked:
                    marked_label.config(text="Marked: Yes")
                else:
                    marked_label.config(text="Marked: No")
        else:
            marked_label.config(text="Marked: No")

    def auto_save():
        save_image()
        next_plot()

    # 使用更长的延迟确保渲染完成
    root.after(100, auto_save)  # 3秒后执行
    check_marked()
    root.mainloop()
    root.destroy()

TW1_MAVEN_GUI(Time_range=None)#["2024-05-18T00:00:00.000", "2024-05-19T00:00:00.000"]
# 示例调用
# download_TW1MOMAG_USTC(
    #Time_range=["2021-11-16T00:00:00.000", "2024-03-31T00:00:00.000"],
# save_dir='\TIANWEN1_Data\MOMAG/01Hz_USTC')

# download_maven_data(["2021-11-01","2024-03-31"],instru='KP')




# data=Read_MAVEN_data(instru='MAG',time_range=["2022-11-18T23:03:00.000", "2022-11-19T01:05:00.000"], time_resolution='1s')

# 调用函数
#webbugs_filenames()