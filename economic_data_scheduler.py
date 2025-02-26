#!/usr/bin/env python3
"""
经济数据爬虫调度器
定期执行 MarketWatch 和 Investing.com 爬虫
Author: kelesit
Date: 2025-02-26
"""

import logging
import time
import json
import os
import schedule
from datetime import datetime
from marketwatch_crawler import MarketWatchCrawler
from investing_crawler import InvestingEarningsCrawler

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("economic_data_scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("economic_data_scheduler")

# 加载配置
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置失败: {str(e)}")
        # 返回默认配置
        return {
            "output_directory": "./data",
            "schedule": {
                "marketwatch_morning": "09:00",
                "marketwatch_evening": "18:00",
                "investing_morning": "09:30",
                "investing_evening": "18:30"
            }
        }

def crawl_marketwatch():
    """执行 MarketWatch 爬虫任务"""
    logger.info(f"开始 MarketWatch 计划任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        config = load_config()
        crawler = MarketWatchCrawler(output_dir=config.get("output_directory", "./data"))
        crawler.run()
        logger.info("MarketWatch 任务完成")
    except Exception as e:
        logger.error(f"MarketWatch 任务执行失败: {str(e)}")

def crawl_investing():
    """执行 Investing.com 爬虫任务"""
    logger.info(f"开始 Investing.com 计划任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        config = load_config()
        crawler = InvestingEarningsCrawler(output_dir=config.get("output_directory", "./data"))
        crawler.run()
        logger.info("Investing.com 任务完成")
    except Exception as e:
        logger.error(f"Investing.com 任务执行失败: {str(e)}")

def setup_schedule():
    """设置定期执行计划"""
    config = load_config()
    schedule_config = config.get("schedule", {})
    
    # 设置 MarketWatch 调度
    schedule.every().day.at(schedule_config.get("marketwatch_morning", "09:00")).do(crawl_marketwatch)
    schedule.every().day.at(schedule_config.get("marketwatch_evening", "18:00")).do(crawl_marketwatch)
    
    # 设置 Investing.com 调度
    schedule.every().day.at(schedule_config.get("investing_morning", "09:30")).do(crawl_investing)
    schedule.every().day.at(schedule_config.get("investing_evening", "18:30")).do(crawl_investing)
    
    logger.info("调度器已启动，将按计划执行爬虫任务")
    
    # 记录下一次执行的时间
    jobs = schedule.get_jobs()
    for job in jobs:
        logger.info(f"计划任务: {job}, 下一次执行时间: {job.next_run}")
    
    # 立即执行一次每个爬虫
    crawl_marketwatch()
    crawl_investing()

    # 持续运行调度器
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    setup_schedule()