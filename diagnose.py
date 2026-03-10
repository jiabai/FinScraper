import akshare as ak
import pandas as pd

print('='*70)
print('📊 详细诊断脚本')
print('='*70)

def analyze_industry_detail(name):
    print(f'\n\n{"="*70}')
    print(f'🔍 分析行业: {name}')
    print('='*70)
    
    s_df = ak.stock_board_industry_cons_em(symbol=name)
    s_list = s_df.iloc[:, 1].astype(str).str.extract(r'(\d+)')[0].str.zfill(6).tolist()
    print(f'✅ 成分股数: {len(s_list)}')
    print(f'   前5个代码: {s_list[:5]}')
    
    year = 2025
    report_date = f'{year}1231'
    perf_yg = ak.stock_yjyg_em(date=report_date)
    perf_yg['code'] = perf_yg.iloc[:, 1].astype(str).str.zfill(6)
    
    ind_perf = perf_yg[perf_yg['code'].isin(s_list)]
    print(f'\n✅ 匹配业绩预告: {len(ind_perf)} 条记录')
    
    if len(ind_perf) == 0:
        print('⚠️  无匹配数据！')
        return
    
    print('\n📋 预告类型分布:')
    type_counts = ind_perf.iloc[:, 8].value_counts()
    for t, c in type_counts.items():
        print(f'   {t}: {c}')
    
    bad_types = ['预减', '略减', '首亏', '续亏', '减亏', '增亏']
    bad_mask = ind_perf.iloc[:, 8].isin(bad_types)
    bad_count = bad_mask.sum()
    bad_stock_count = ind_perf[bad_mask]['code'].nunique()
    
    print(f'\n⚠️  负面统计:')
    print(f'   负面预告记录数: {bad_count}')
    print(f'   负面预告股票数: {bad_stock_count}')
    print(f'   成分股数: {len(s_list)}')
    print(f'   踩雷比例: {bad_stock_count/len(s_list)*100:.1f}%')
    
    print(f'\n📈 正面类型:')
    positive_mask = ~bad_mask
    if positive_mask.sum() > 0:
        pos_types = ind_perf[positive_mask].iloc[:, 8].unique()
        print(f'   {pos_types.tolist()}')
    
    if len(ind_perf) <= 30:
        print(f'\n📝 所有匹配记录:')
        print(ind_perf[['股票代码', '股票简称', '预告类型', '业绩变动']].to_string())
    else:
        print(f'\n📝 前15条记录:')
        print(ind_perf[['股票代码', '股票简称', '预告类型', '业绩变动']].head(15).to_string())

for industry in ['半导体', '电池', '电力', '航运', '机器人']:
    analyze_industry_detail(industry)

print(f'\n\n{"="*70}')
print('✅ 诊断完成')
print('='*70)
