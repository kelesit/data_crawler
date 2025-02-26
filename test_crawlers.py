#!/usr/bin/env python3
"""
验证爬虫输出的数据
Author: kelesit
Date: 2025-02-26
"""

import os
import csv
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_marketwatch_data(data_file):
    """验证MarketWatch数据的质量"""
    if not os.path.exists(data_file):
        logger.error(f"文件不存在: {data_file}")
        return False
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        logger.info(f"读取了 {len(rows)} 条数据")
        
        # 检查必要字段是否存在
        required_fields = ["date", "time", "event", "actual", "forecast", "previous"]
        missing_fields = [field for field in required_fields if field not in reader.fieldnames]
        
        if missing_fields:
            logger.error(f"缺少必要字段: {missing_fields}")
            return False
        
        # 检查数据质量
        empty_count = 0
        for row in rows:
            if not row["event"].strip():
                empty_count += 1
        
        if empty_count > 0:
            logger.warning(f"发现 {empty_count} 条记录缺少事件名称")
        
        # 验证通过
        logger.info("MarketWatch数据验证通过")
        return True
        
    except Exception as e:
        logger.error(f"验证过程中出错: {str(e)}")
        return False

def validate_investing_data(data_file):
    """验证Investing.com数据的质量"""
    if not os.path.exists(data_file):
        logger.error(f"文件不存在: {data_file}")
        return False
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        logger.info(f"读取了 {len(rows)} 条数据")
        
        # 检查必要字段是否存在
        required_fields = ["date", "company_name", "symbol"]
        missing_fields = [field for field in required_fields if field not in reader.fieldnames]
        
        if missing_fields:
            logger.error(f"缺少必要字段: {missing_fields}")
            return False
        
        # 检查数据质量
        empty_symbols = 0
        for row in rows:
            if not row["symbol"].strip():
                empty_symbols += 1
        
        if empty_symbols > 0:
            logger.warning(f"发现 {empty_symbols} 条记录缺少股票代码")
        
        # 验证通过
        logger.info("Investing.com数据验证通过")
        return True
        
    except Exception as e:
        logger.error(f"验证过程中出错: {str(e)}")
        return False

def main():
    """主函数"""
    data_dir = Path("./data")
    
    # 验证最新的MarketWatch数据
    marketwatch_file = data_dir / "latest_economic_data.csv"
    if marketwatch_file.exists():
        validate_marketwatch_data(marketwatch_file)
    else:
        logger.error(f"MarketWatch数据文件不存在: {marketwatch_file}")
    
    # 验证最新的Investing.com数据
    investing_file = data_dir / "latest_earnings_data.csv"
    if investing_file.exists():
        validate_investing_data(investing_file)
    else:
        logger.error(f"Investing.com数据文件不存在: {investing_file}")

if __name__ == "__main__":
    main()

"""
运行测试

测试所有爬虫
python test_crawlers.py --all

单独测试 MarketWatch 爬虫
python test_crawlers.py --marketwatch

单独测试 Investing.com 爬虫
python test_crawlers.py --investing
"""