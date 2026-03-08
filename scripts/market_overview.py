#!/usr/bin/env python3
"""
市场概览数据获取脚本
生成每日市场概览所需的所有数据
"""

import sys
import os

os.environ["FINSCRAPER_LOG_LEVEL"] = "CRITICAL"

from finscraper.fetchers.index import IndexFetcher
from finscraper.fetchers.market_sentiment import MarketSentimentFetcher
from finscraper.fetchers.commodity import CommodityFetcher
from finscraper.fetchers.hk_index import HKIndexFetcher
from finscraper.fetchers.us_index import USIndexFetcher
from datetime import datetime


class MarketOverview:
    """市场概览数据聚合器"""
    
    def __init__(self):
        self.index_fetcher = IndexFetcher()
        self.sentiment_fetcher = MarketSentimentFetcher()
        self.commodity_fetcher = CommodityFetcher()
        self.hk_index_fetcher = HKIndexFetcher()
        self.us_index_fetcher = USIndexFetcher()
    
    def get_index_summary(self):
        """获取 A 股指数摘要"""
        df = self.index_fetcher.fetch_spot()
        
        main_indices = {
            'sh000001': '沪指',
            'sz399001': '深成指',
            'sz399006': '创业板指'
        }
        
        result = {}
        for symbol, name in main_indices.items():
            row = df[df['代码'] == symbol]
            if not row.empty:
                result[name] = {
                    'change_percent': row['涨跌幅'].iloc[0],
                    'amount': row['成交额'].iloc[0],
                    'volume': row['成交量'].iloc[0]
                }
        return result
    
    def get_volume_status(self, days=5):
        """获取成交量状态"""
        try:
            df_today = self.index_fetcher.fetch_spot()
            today_amount = df_today[df_today['代码'] == 'sh000001']['成交额'].iloc[0]
            
            df_history = self.index_fetcher.fetch_history(
                symbol='000001',
                period='daily'
            )
            if df_history is not None and len(df_history) >= days:
                recent_avg = df_history.tail(days)['amount'].mean()
                ratio = today_amount / recent_avg
                if ratio > 1.2:
                    return '放量', ratio
                elif ratio < 0.8:
                    return '缩量', ratio
                else:
                    return '持平', ratio
            return None, None
        except Exception as e:
            return None, None
    
    def get_sentiment(self):
        """获取市场情绪数据"""
        try:
            df = self.sentiment_fetcher.fetch_sentiment()
            if df is None or len(df) == 0:
                return None
            return {
                'up_count': df['up_count'].iloc[0],
                'down_count': df['down_count'].iloc[0],
                'limit_up': df['limit_up_count'].iloc[0],
                'limit_down': df['limit_down_count'].iloc[0]
            }
        except Exception as e:
            return None
    
    def get_market_strength(self, index_data, sentiment):
        """判断大盘强弱"""
        if sentiment is None:
            return None
        
        sh_change = index_data.get('沪指', {}).get('change_percent', 0)
        up_count = sentiment['up_count']
        down_count = sentiment['down_count']
        limit_up = sentiment['limit_up']
        limit_down = sentiment['limit_down']
        
        if up_count == 0 and down_count == 0:
            return None
        
        up_down_ratio = up_count / down_count if down_count > 0 else float('inf')
        
        if sh_change > 1.5 and up_down_ratio > 2 and limit_up > limit_down * 5:
            return '强势'
        elif sh_change < -1.5 and up_down_ratio < 0.5 and limit_down > limit_up * 3:
            return '弱势'
        else:
            return '震荡'
    
    def get_commodity_data(self):
        """获取大宗商品数据（黄金、原油）"""
        try:
            df = self.commodity_fetcher.fetch_spot()
            result = {}
            
            gold_keywords = ['黄金', '金', 'GOLD']
            oil_keywords = ['原油', '石油', 'OIL', 'WTI', '布伦特']
            
            for _, row in df.iterrows():
                name = str(row.get('名称', ''))
                for keyword in gold_keywords:
                    if keyword in name:
                        result['黄金'] = {
                            'price': row.get('最新价', 0),
                            'change_percent': row.get('涨跌幅', 0)
                        }
                        break
                for keyword in oil_keywords:
                    if keyword in name and '原油' not in result:
                        result['原油'] = {
                            'price': row.get('最新价', 0),
                            'change_percent': row.get('涨跌幅', 0)
                        }
                        break
            
            return result
        except Exception as e:
            return {}
    
    def get_hk_index_data(self):
        """获取港股指数数据"""
        try:
            df = self.hk_index_fetcher.fetch_spot()
            for _, row in df.iterrows():
                name = str(row.get('名称', ''))
                if '恒生' in name:
                    return {
                        'name': name,
                        'price': row.get('最新价', 0),
                        'change_percent': row.get('涨跌幅', 0)
                    }
            return {}
        except Exception as e:
            return {}
    
    def get_us_index_data(self):
        """获取美股指数数据"""
        try:
            us_data = self.us_index_fetcher.fetch_latest()
            return us_data
        except Exception as e:
            return {}
    
    def format_change(self, change_percent):
        """格式化涨跌幅"""
        if change_percent > 0:
            return f"涨{change_percent:.2f}%"
        elif change_percent < 0:
            return f"跌{abs(change_percent):.2f}%"
        else:
            return "平盘"
    
    def generate_report(self):
        """生成完整市场概览报告"""
        index = self.get_index_summary()
        volume_status, ratio = self.get_volume_status()
        sentiment = self.get_sentiment()
        strength = self.get_market_strength(index, sentiment)
        commodity = self.get_commodity_data()
        hk_index = self.get_hk_index_data()
        us_index = self.get_us_index_data()
        
        parts = []
        
        if index:
            index_parts = []
            if '沪指' in index:
                index_parts.append(f"沪指{self.format_change(index['沪指']['change_percent'])}")
            if '深成指' in index:
                index_parts.append(f"深成指{self.format_change(index['深成指']['change_percent'])}")
            if '创业板指' in index:
                index_parts.append(f"创业板指{self.format_change(index['创业板指']['change_percent'])}")
            if index_parts:
                parts.append('，'.join(index_parts))
        
        if volume_status:
            parts.append(f"两市成交额较昨日{volume_status}")
        else:
            parts.append("成交量对比（获取失败）")
        
        if sentiment and (sentiment['up_count'] > 0 or sentiment['down_count'] > 0):
            if sentiment['up_count'] > sentiment['down_count']:
                if sentiment['up_count'] > sentiment['down_count'] * 1.5:
                    parts.append("上涨家数远多于下跌家数")
                else:
                    parts.append("上涨家数略多于下跌家数")
            elif sentiment['down_count'] > sentiment['up_count']:
                if sentiment['down_count'] > sentiment['up_count'] * 1.5:
                    parts.append("下跌家数远多于上涨家数")
                else:
                    parts.append("下跌家数略多于上涨家数")
            else:
                parts.append("涨跌家数基本持平")
        
        if sentiment and (sentiment['limit_up'] > 0 or sentiment['limit_down'] > 0):
            limit_parts = []
            if sentiment['limit_up'] > 0:
                limit_parts.append(f"涨停{sentiment['limit_up']}家")
            if sentiment['limit_down'] > 0:
                limit_parts.append(f"跌停{sentiment['limit_down']}家")
            if limit_parts:
                parts.append('，'.join(limit_parts))
        
        if strength:
            parts.append(f"市场整体{strength}")
        elif sentiment is None:
            parts.append("市场情绪（获取失败）")
        
        optional_parts = []
        
        if hk_index:
            optional_parts.append(f"恒生指数{self.format_change(hk_index['change_percent'])}")
        
        if us_index:
            us_parts = []
            if '道琼斯' in us_index:
                us_parts.append(f"道指{self.format_change(us_index['道琼斯']['change_percent'])}")
            if '纳斯达克' in us_index:
                us_parts.append(f"纳指{self.format_change(us_index['纳斯达克']['change_percent'])}")
            if '标普500' in us_index:
                us_parts.append(f"标普500{self.format_change(us_index['标普500']['change_percent'])}")
            if us_parts:
                optional_parts.append('，'.join(us_parts))
        
        if commodity:
            comm_parts = []
            if '黄金' in commodity:
                comm_parts.append(f"黄金{self.format_change(commodity['黄金']['change_percent'])}")
            if '原油' in commodity:
                comm_parts.append(f"原油{self.format_change(commodity['原油']['change_percent'])}")
            if comm_parts:
                optional_parts.append('，'.join(comm_parts))
        
        report = '，'.join(parts)
        if optional_parts:
            report += '。' + '，'.join(optional_parts) + '。'
        else:
            report += '。'
        
        return report


if __name__ == '__main__':
    overview = MarketOverview()
    print(overview.generate_report())
