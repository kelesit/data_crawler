#!/usr/bin/env python3
"""
MarketWatch Economic Calendar Crawler
Author: kelesit
Date: 2025-02-26
"""

import os
import csv
import json
import logging
from datetime import datetime
from crawl4ai import WebCrawler

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("marketwatch_crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("marketwatch_crawler")

class MarketWatchCrawler:
    def __init__(self, output_dir="./data"):
        self.url = "https://www.marketwatch.com/economy-politics/calendar"
        self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化爬虫
        self.crawler = WebCrawler(
            javascript=True,  # MarketWatch可能需要JavaScript渲染
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.marketwatch.com/"
            },
            timeout=60
        )

    def extract_economic_data(self):
        """提取经济日历数据"""
        logger.info(f"开始爬取 {self.url}")
        
        # 配置提取规则
        self.crawler.extract({
            "reports": {
                "selector": "table.calendar__table tr.calendar__row",
                "multiple": True,
                "data": {
                    "date": ".calendar__cell--date",
                    "time": ".calendar__cell--time",
                    "event": ".calendar__cell--event",
                    "actual": ".calendar__cell--actual",
                    "forecast": ".calendar__cell--forecast",
                    "previous": ".calendar__cell--previous"
                }
            },
            # 提取日期范围信息
            "date_range": ".calendar-range"
        })
        
        # 执行爬取
        try:
            self.crawler.wait_for("table.calendar__table")
            results = self.crawler.crawl(self.url)
            logger.info(f"成功爬取数据，获取到 {len(results.get('reports', []))} 条报告")
            return results
        except Exception as e:
            logger.error(f"爬取过程中发生错误: {str(e)}")
            return {"reports": [], "date_range": ""}

    def save_data(self, data):
        """保存爬取的数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存为CSV
        csv_file = os.path.join(self.output_dir, f"marketwatch_economic_data_{timestamp}.csv")
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if not data.get("reports"):
                    logger.warning("没有数据可以保存")
                    return
                
                fieldnames = ["date", "time", "event", "actual", "forecast", "previous"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for report in data.get("reports", []):
                    writer.writerow(report)
            
            logger.info(f"数据已保存到 {csv_file}")
            
            # 同时保存一份最新数据的副本
            latest_csv = os.path.join(self.output_dir, "latest_economic_data.csv")
            with open(latest_csv, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ["date", "time", "event", "actual", "forecast", "previous"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for report in data.get("reports", []):
                    writer.writerow(report)
            
            # 保存元数据
            metadata = {
                "crawl_time": datetime.now().isoformat(),
                "date_range": data.get("date_range", ""),
                "report_count": len(data.get("reports", [])),
                "source_url": self.url
            }
            
            with open(os.path.join(self.output_dir, f"metadata_{timestamp}.json"), 'w') as f:
                json.dump(metadata, f, indent=4)
                
        except Exception as e:
            logger.error(f"保存数据时发生错误: {str(e)}")

    def run(self):
        """执行爬虫流程"""
        logger.info("开始执行 MarketWatch 经济日历爬虫任务")
        data = self.extract_economic_data()
        self.save_data(data)
        logger.info("爬虫任务完成")


if __name__ == "__main__":
    crawler = MarketWatchCrawler()
    crawler.run()