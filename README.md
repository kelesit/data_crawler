# scrape google finance Today's finnancial news

## envirement setup

```bash
poetry install

poetry run playwright --version # check if playwright is installed

poetry run playwright install # install browser

poetry shell # activate virtual env

```

使用说明
安装所需依赖：

setup.sh
pip install -r requirements.txt
运行集成调度器：

run.sh
python economic_data_scheduler.py
或者使用Docker构建和运行：

docker_run.sh

## 构建Docker镜像

docker build -t economic-data-crawler .

## 运行Docker容器

docker run -d -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs --name economic-crawler economic-data-crawler

\
运行数据分析脚本：

analyze.sh
python analyze_economic_data.py
注意事项
Investing.com可能会检测爬虫行为，建议调整请求间隔和添加适当的代理
两个网站的结构可能会变化，需要定期检查并更新爬虫的选择器
经济数据有时会有较大波动，分析时请考虑异常值处理
使用Docker容器可以解决运行环境依赖问题，但确保挂载卷以保存爬取的数据
这个完整的解决方案将帮助您定期爬取MarketWatch和Investing.com的经济和财报数据，并提供基本的数据分析功能。
