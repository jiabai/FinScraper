"""FinScraper usage examples."""
from finscraper.fetchers import (
    IndexFetcher,
    NorthFlowFetcher,
    SectorFetcher,
    CommodityFetcher,
    MoneyFlowFetcher,
    NewsFetcher,
)
from finscraper.storage.csv_storage import CSVStorage


def example_index_fetcher():
    """Example: IndexFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 1: IndexFetcher - A 股指数数据")
    print("=" * 60)
    
    try:
        fetcher = IndexFetcher()
        
        print("\n获取指数实时行情...")
        spot_data = fetcher.fetch_spot()
        print(f"成功获取 {len(spot_data)} 条指数实时数据")
        print(spot_data.head())
        
        print("\n获取上证指数历史数据...")
        history_data = fetcher.fetch_history(
            symbol="000001",
            start_date="20240101",
            end_date="20241231",
        )
        print(f"成功获取 {len(history_data)} 条历史数据")
        print(history_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_north_flow_fetcher():
    """Example: NorthFlowFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 2: NorthFlowFetcher - 北向资金数据")
    print("=" * 60)
    
    try:
        fetcher = NorthFlowFetcher()
        
        print("\n获取北向资金日数据...")
        daily_data = fetcher.fetch_daily()
        print(f"成功获取 {len(daily_data)} 条北向资金日数据")
        print(daily_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_sector_fetcher():
    """Example: SectorFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 3: SectorFetcher - 板块数据")
    print("=" * 60)
    
    try:
        fetcher = SectorFetcher()
        
        print("\n获取板块列表...")
        sector_list = fetcher.fetch_list()
        print(f"成功获取 {len(sector_list)} 个板块")
        print(sector_list.head())
        
        print("\n获取板块实时行情...")
        spot_data = fetcher.fetch_spot()
        print(f"成功获取 {len(spot_data)} 条板块实时数据")
        print(spot_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_commodity_fetcher():
    """Example: CommodityFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 4: CommodityFetcher - 大宗商品数据")
    print("=" * 60)
    
    try:
        fetcher = CommodityFetcher()
        
        print("\n获取大宗商品实时行情...")
        spot_data = fetcher.fetch_spot()
        print(f"成功获取 {len(spot_data)} 条大宗商品实时数据")
        print(spot_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_money_flow_fetcher():
    """Example: MoneyFlowFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 5: MoneyFlowFetcher - 资金流向数据")
    print("=" * 60)
    
    try:
        fetcher = MoneyFlowFetcher()
        
        print("\n获取市场资金流向...")
        market_data = fetcher.fetch_market()
        print(f"成功获取 {len(market_data)} 条市场资金流向数据")
        print(market_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_news_fetcher():
    """Example: NewsFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 6: NewsFetcher - 新闻数据")
    print("=" * 60)
    
    try:
        fetcher = NewsFetcher()
        
        print("\n获取全球新闻...")
        global_news = fetcher.fetch_global()
        print(f"成功获取 {len(global_news)} 条全球新闻")
        print(global_news.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_storage():
    """Example: Storage usage."""
    print("\n" + "=" * 60)
    print("示例 7: 数据存储示例")
    print("=" * 60)
    
    try:
        fetcher = IndexFetcher()
        spot_data = fetcher.fetch_spot()
        
        print("\n保存为 CSV...")
        storage = CSVStorage()
        storage.save(spot_data, "example_index_spot.csv")
        print("已保存到 example_index_spot.csv")
        
        print("\n从 CSV 加载...")
        loaded_data = storage.load("example_index_spot.csv")
        print(f"成功加载 {len(loaded_data)} 条数据")
    except Exception as e:
        print(f"示例执行失败: {e}")


def main():
    """Run all examples."""
    print("FinScraper - 使用示例")
    print("=" * 60)
    
    example_index_fetcher()
    example_north_flow_fetcher()
    example_sector_fetcher()
    example_commodity_fetcher()
    example_money_flow_fetcher()
    example_news_fetcher()
    example_storage()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
