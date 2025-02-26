#!/usr/bin/env python3
"""
Investing.com Earnings Calendar Crawler
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
        logging.FileHandler("investing_crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("investing_crawler")

class InvestingEarningsCrawler:
    def __init__(self, output_dir="./data"):
        self.url = "https://www.investing.com/earnings-calendar/"
        self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化爬虫
        self.crawler = WebCrawler(
            javascript=True,  # Investing.com需要JavaScript渲染
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.investing.com/"
            },
            timeout=90,  # 增加超时时间，因为页面加载可能较慢
            cookies={
                "adBlockerNewUserDomains": "1633094489",  # 可能需要一些cookies来避免反爬
                "PHPSESSID": "random_session_id"
            }
        )

    def extract_earnings_data(self):
        """提取财报日历数据"""
        logger.info(f"开始爬取 {self.url}")
        
        # 配置提取规则
        self.crawler.extract({
            "earnings_dates": {
                "selector": ".earningsCalendarDiv table tbody tr",
                "multiple": True,
                "data": {
                    "date": {
                        "selector": ".theDay",
                        "processor": "text"
                    },
                    "country": {
                        "selector": "td:nth-child(2) span",
                        "attribute": "title"
                    },
                    "company_name": "td.symbolColumn a",
                    "symbol": {
                        "selector": "td.symbolColumn span",
                        "processor": "text"
                    },
                    "eps_forecast": "td.eps.bold",
                    "eps_actual": "td.actual.bold",
                    "revenue_forecast": "td.rev.bold",
                    "revenue_actual": "td.actualRev.bold",
                    "market_cap": "td.marketCap"
                }
            },
            # 提取当前日期范围信息
            "current_period": ".currentDateView"
        })
        
        # 执行爬取
        try:
            # 等待页面加载完成
            self.crawler.wait_for(".earningsCalendarDiv table")
            
            # 可能需要点击某些按钮来显示更多数据
            # self.crawler.click(".showMoreButton")
            
            results = self.crawler.crawl(self.url)
            logger.info(f"成功爬取数据，获取到 {len(results.get('earnings_dates', []))} 条财报记录")
            return results
        except Exception as e:
            logger.error(f"爬取过程中发生错误: {str(e)}")
            return {"earnings_dates": [], "current_period": ""}

    def save_data(self, data):
        """保存爬取的数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存为CSV
        csv_file = os.path.join(self.output_dir, f"investing_earnings_data_{timestamp}.csv")
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if not data.get("earnings_dates"):
                    logger.warning("没有数据可以保存")
                    return
                
                fieldnames = ["date", "country", "company_name", "symbol", "eps_forecast", 
                              "eps_actual", "revenue_forecast", "revenue_actual", "market_cap"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for earning in data.get("earnings_dates", []):
                    writer.writerow(earning)
            
            logger.info(f"数据已保存到 {csv_file}")
            
            # 同时保存一份最新数据的副本
            latest_csv = os.path.join(self.output_dir, "latest_earnings_data.csv")
            with open(latest_csv, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ["date", "country", "company_name", "symbol", "eps_forecast", 
                              "eps_actual", "revenue_forecast", "revenue_actual", "market_cap"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for earning in data.get("earnings_dates", []):
                    writer.writerow(earning)
            
            # 保存元数据
            metadata = {
                "crawl_time": datetime.now().isoformat(),
                "period": data.get("current_period", ""),
                "earnings_count": len(data.get("earnings_dates", [])),
                "source_url": self.url
            }
            
            with open(os.path.join(self.output_dir, f"investing_metadata_{timestamp}.json"), 'w') as f:
                json.dump(metadata, f, indent=4)
                
        except Exception as e:
            logger.error(f"保存数据时发生错误: {str(e)}")

    def run(self):
        """执行爬虫流程"""
        logger.info("开始执行 Investing.com 财报日历爬虫任务")
        data = self.extract_earnings_data()
        self.save_data(data)
        logger.info("爬虫任务完成")


if __name__ == "__main__":
    crawler = InvestingEarningsCrawler()
    crawler.run()