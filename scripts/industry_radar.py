import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

class FinalSurgicalRadar:
    def __init__(self):
        self.industries = ["半导体", "电池", "电力", "航运", "机器人"]

    def clean_code(self, series):
        return series.astype(str).str.extract(r'(\d+)')[0].str.zfill(6)
    
    def find_column_by_keywords(self, df, keywords, fallback_idx=None):
        for col in df.columns:
            if all(kw in str(col) for kw in keywords):
                return col
        if fallback_idx is not None and fallback_idx < len(df.columns):
            return df.columns[fallback_idx]
        return None

    def scan(self):
        print(f"🚀 正在启动全时段扫描... (当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M')})")
        try:
            all_lock = None
            perf_yg = None
            all_stock_flow = None
            
            lock_code_col = None
            lock_date_col = None
            perf_code_col = None
            perf_type_col = None
            flow_code_col = None
            flow_net_col = None
            s_code_col = None
            
            try:
                all_lock = ak.stock_restricted_release_queue_em()
                lock_code_col = self.find_column_by_keywords(all_lock, ['代码'], 0)
                lock_date_col = self.find_column_by_keywords(all_lock, ['日期', '解禁'], 1)
                all_lock['code'] = self.clean_code(all_lock[lock_code_col])
            except Exception as e:
                print(f"⚠️ 解禁数据获取失败: {e}")
            
            year = datetime.now().year
            report_date = f"{year-1}1231"
            try:
                perf_yg = ak.stock_yjyg_em(date=report_date)
            except:
                try:
                    perf_yg = ak.stock_yjyg_em(date=f"{year-2}1231")
                except:
                    perf_yg = None
            if perf_yg is not None:
                perf_code_col = self.find_column_by_keywords(perf_yg, ['代码'], 1)
                perf_type_col = self.find_column_by_keywords(perf_yg, ['预告', '类型'], 8)
                perf_yg['code'] = self.clean_code(perf_yg[perf_code_col])
            
            print("🕒 正在对齐主力资金流(多级兜底模式)...")
            try:
                all_stock_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
            except:
                try:
                    all_stock_flow = ak.stock_individual_fund_flow_rank(indicator="5日")
                except:
                    all_stock_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
            if all_stock_flow is not None:
                flow_code_col = self.find_column_by_keywords(all_stock_flow, ['代码'], 1)
                flow_net_col = self.find_column_by_keywords(all_stock_flow, ['净流入', '净额'], 5)
                all_stock_flow['code'] = self.clean_code(all_stock_flow[flow_code_col])
                if flow_net_col:
                    print(f"✅ 找到主力资金流列: {flow_net_col}")
            
            lock_latest = None
            lock_status = "⚠️ 解禁数据不可用"
            if all_lock is not None and lock_date_col:
                lock_latest = pd.to_datetime(all_lock[lock_date_col], errors='coerce').max()
                if lock_latest and pd.notna(lock_latest):
                    lock_status = "⚠️ 解禁数据源已失效(最新2020年)" if lock_latest.year < 2023 else "✅ 解禁数据正常"

        except Exception as e:
            print(f"❌ 基础数据调取失败: {e}"); return

        results = []
        risk_details = []
        for name in self.industries:
            try:
                s_df = ak.stock_board_industry_cons_em(symbol=name)
                if s_df.empty: continue
                s_code_col = self.find_column_by_keywords(s_df, ['代码'], 1)
                s_list = self.clean_code(s_df[s_code_col]).tolist()
                stock_count = len(s_list)
                
                l_count = 0
                if all_lock is not None and lock_date_col:
                    ind_lock = all_lock[all_lock['code'].isin(s_list)]
                    if not ind_lock.empty:
                        date_series = pd.to_datetime(ind_lock[lock_date_col], errors='coerce')
                        l_count = len(ind_lock[(date_series >= datetime.now()) & (date_series <= datetime.now() + timedelta(days=15))])
                
                bad_count = 0
                bad_stock_count = 0
                bad_ratio = 0.0
                if perf_yg is not None and perf_type_col:
                    ind_perf = perf_yg[perf_yg['code'].isin(s_list)]
                    if not ind_perf.empty:
                        bad_types = ['预减', '略减', '首亏', '续亏', '减亏', '增亏']
                        bad_mask = ind_perf[perf_type_col].isin(bad_types)
                        bad_count = bad_mask.sum()
                        bad_stock_count = ind_perf[bad_mask]['code'].nunique()
                        bad_ratio = bad_stock_count / stock_count if stock_count > 0 else 0.0
                
                flow_val = 0.0
                if all_stock_flow is not None and flow_net_col:
                    ind_flow = all_stock_flow[all_stock_flow['code'].isin(s_list)]
                    flow_val = pd.to_numeric(ind_flow[flow_net_col], errors='coerce').fillna(0).sum() / 1e8

                results.append({
                    "行业": name, 
                    "成分": stock_count, 
                    "15D解禁": l_count if (lock_latest and pd.notna(lock_latest) and lock_latest.year >= 2023) else "-", 
                    "业绩雷": bad_count,
                    "负面股数": bad_stock_count,
                    "踩雷比例": f"{bad_ratio*100:.1f}%", 
                    "主力(亿)": round(flow_val, 2)
                })
                risk_details.append({
                    "行业": name,
                    "主力资金": round(flow_val, 2),
                    "业绩雷股票数": bad_stock_count,
                    "成分股数": stock_count,
                    "解禁数": l_count
                })
            except: continue

        df = pd.DataFrame(results)
        print("\n" + "="*60)
        print(f"📊 避雷终端(全时段版) | 业绩期: {report_date}")
        print("-" * 60)
        if not df.empty:
            print(df.sort_values(by="主力(亿)").to_string(index=False))
            print("-" * 60)
            for _, detail in enumerate(risk_details):
                risk_score = 0
                if detail['主力资金'] < -2: risk_score += 1 
                if detail['成分股数'] > 0 and (detail['业绩雷股票数'] / detail['成分股数'] > 0.1): risk_score += 1 
                if detail['解禁数'] > 0: risk_score += 1
                
                risk_icons = "★" * risk_score + "☆" * (3 - risk_score)
                advice = "持仓观察" if risk_score == 0 else ("建议减仓" if risk_score == 1 else "强制避险")
                print(f" - 【{detail['行业']}】风险: {risk_icons} | 建议: {advice}")
            
            print("-" * 60)
            print(lock_status + "，暂无法获取未来解禁计划")
        else:
            print("⚠️ 未抓取到有效成分股数据。")
        print("="*60)

if __name__ == "__main__":
    FinalSurgicalRadar().scan()
