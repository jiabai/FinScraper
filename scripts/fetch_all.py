"""Fetch all financial data in one go (legacy script for backward compatibility)."""
import datetime
import os
from finscraper.fetchers import (
    IndexFetcher,
    NorthFlowFetcher,
    SectorFetcher,
    CommodityFetcher,
    MoneyFlowFetcher,
    NewsFetcher,
)
from finscraper.storage.csv_storage import CSVStorage


def main():
    """Main function to fetch all data."""
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    storage = CSVStorage()
    
    print("=" * 60)
    print("FinScraper - 一键获取所有数据")
    print("=" * 60)
    
    try:
        print("\n[1/6] 获取指数数据...")
        index_fetcher = IndexFetcher()
        index_data = index_fetcher.fetch_spot()
        index_path = os.path.join(data_dir, f"index_spot_{today}.csv")
        storage.save(index_data, index_path)
        print(f"   已保存到: {index_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[2/6] 获取北向资金数据...")
        north_flow_fetcher = NorthFlowFetcher()
        north_flow_data = north_flow_fetcher.fetch_daily()
        north_flow_path = os.path.join(data_dir, f"north_flow_daily_{today}.csv")
        storage.save(north_flow_data, north_flow_path)
        print(f"   已保存到: {north_flow_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[3/6] 获取板块数据...")
        sector_fetcher = SectorFetcher()
        sector_data = sector_fetcher.fetch_list()
        sector_path = os.path.join(data_dir, f"sector_list_{today}.csv")
        storage.save(sector_data, sector_path)
        print(f"   已保存到: {sector_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[4/6] 获取大宗商品数据...")
        commodity_fetcher = CommodityFetcher()
        commodity_data = commodity_fetcher.fetch_spot()
        commodity_path = os.path.join(data_dir, f"commodity_spot_{today}.csv")
        storage.save(commodity_data, commodity_path)
        print(f"   已保存到: {commodity_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[5/6] 获取资金流向数据...")
        money_flow_fetcher = MoneyFlowFetcher()
        money_flow_data = money_flow_fetcher.fetch_market()
        money_flow_path = os.path.join(data_dir, f"money_flow_market_{today}.csv")
        storage.save(money_flow_data, money_flow_path)
        print(f"   已保存到: {money_flow_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[6/6] 获取新闻数据...")
        news_fetcher = NewsFetcher()
        news_data = news_fetcher.fetch_global()
        news_path = os.path.join(data_dir, f"news_global_{today}.csv")
        storage.save(news_data, news_path)
        print(f"   已保存到: {news_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    print("\n" + "=" * 60)
    print("数据获取完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
