#!/usr/bin/env python3
"""
经济数据分析工具
分析 MarketWatch 和 Investing.com 爬取的数据
Author: kelesit
Date: 2025-02-26
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_latest_data(data_dir="./data"):
    """加载最新的经济和财报数据"""
    economic_data_path = os.path.join(data_dir, "latest_economic_data.csv")
    earnings_data_path = os.path.join(data_dir, "latest_earnings_data.csv")
    
    economic_data = None
    earnings_data = None
    
    if os.path.exists(economic_data_path):
        economic_data = pd.read_csv(economic_data_path)
        print(f"已加载经济数据: {economic_data.shape[0]} 条记录")
    else:
        print("未找到经济数据文件")
        
    if os.path.exists(earnings_data_path):
        earnings_data = pd.read_csv(earnings_data_path)
        print(f"已加载财报数据: {earnings_data.shape[0]} 条记录")
    else:
        print("未找到财报数据文件")
        
    return economic_data, earnings_data

def generate_summary_report(economic_data, earnings_data, output_dir="./reports"):
    """生成数据摘要报告"""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    report_path = os.path.join(output_dir, f"economic_summary_{timestamp}.html")
    
    with open(report_path, 'w') as f:
        f.write("<html><head><title>经济数据摘要报告</title>")
        f.write("<style>body{font-family:Arial;margin:20px}table{border-collapse:collapse;width:100%}th,td{padding:8px;text-align:left;border:1px solid #ddd}th{background-color:#f2f2f2}</style>")
        f.write("</head><body>")
        
        f.write(f"<h1>经济数据摘要报告 - {datetime.now().strftime('%Y-%m-%d')}</h1>")
        
        # 经济数据摘要
        if economic_data is not None:
            f.write("<h2>MarketWatch 经济日历数据</h2>")
            f.write(f"<p>记录总数: {economic_data.shape[0]}</p>")
            f.write("<h3>数据预览</h3>")
            f.write(economic_data.head().to_html())
        
        # 财报数据摘要
        if earnings_data is not None:
            f.write("<h2>Investing.com 财报日历数据</h2>")
            f.write(f"<p>记录总数: {earnings_data.shape[0]}</p>")
            f.write("<h3>数据预览</h3>")
            f.write(earnings_data.head().to_html())
            
            # 按国家分析财报数据
            if 'country' in earnings_data.columns:
                f.write("<h3>按国家分布</h3>")
                country_counts = earnings_data['country'].value_counts()
                f.write(country_counts.to_frame().to_html())
        
        f.write("</body></html>")
    
    print(f"摘要报告已生成: {report_path}")
    return report_path

def visualize_data(economic_data, earnings_data, output_dir="./reports"):
    """可视化经济和财报数据"""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    
    # 设置可视化风格
    sns.set(style="whitegrid")
    
    # 可视化财报数据
    if earnings_data is not None and 'country' in earnings_data.columns:
        plt.figure(figsize=(12, 6))
        top_countries = earnings_data['country'].value_counts().head(10)
        sns.barplot(x=top_countries.index, y=top_countries.values)
        plt.title('Top 10 Countries by Earnings Reports')
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, f"earnings_by_country_{timestamp}.png")
        plt.savefig(chart_path)
        plt.close()
        print(f"已生成图表: {chart_path}")
    
    # 可视化经济数据
    if economic_data is not None and 'actual' in economic_data.columns and 'forecast' in economic_data.columns:
        # 清洗数据，转换为数值类型
        economic_data['actual'] = pd.to_numeric(economic_data['actual'], errors='coerce')
        economic_data['forecast'] = pd.to_numeric(economic_data['forecast'], errors='coerce')
        
        # 计算预测与实际值的差异
        economic_data['difference'] = economic_data['actual'] - economic_data['forecast']
        
        plt.figure(figsize=(12, 6))
        sns.histplot(economic_data['difference'].dropna(), kde=True)
        plt.title('Distribution of Actual vs Forecast Differences')
        plt.xlabel('Difference (Actual - Forecast)')
        plt.tight_layout()
        chart_path = os.path.join(output_dir, f"economic_forecast_diff_{timestamp}.png")
        plt.savefig(chart_path)
        plt.close()
        print(f"已生成图表: {chart_path}")

def main():
    """主函数"""
    print("开始分析经济数据...")
    economic_data, earnings_data = load_latest_data()
    if economic_data is not None or earnings_data is not None:
        report_path = generate_summary_report(economic_data, earnings_data)
        visualize_data(economic_data, earnings_data)
        print(f"分析完成，报告已保存到 {report_path}")
    else:
        print("没有可用的数据进行分析")

if __name__ == "__main__":
    main()