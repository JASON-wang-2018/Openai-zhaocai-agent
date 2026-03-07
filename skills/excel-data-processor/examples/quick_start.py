"""
Excel 数据处理 - 快速入门示例
演示常用功能和典型场景
"""

import pandas as pd
import sys
import os

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from excel_processor import ExcelProcessor, ProjectManager


def example_1_read_and_basic_analysis():
    """示例1: 读取 Excel 文件并进行基础分析"""
    print("=" * 50)
    print("示例1: 读取和基础分析")
    print("=" * 50)

    processor = ExcelProcessor()

    # 读取文件（假设文件存在）
    # df = processor.read_excel('data.xlsx', sheet_name='Sheet1')

    # 创建示例数据
    data = {
        '产品': ['产品A', '产品B', '产品C', '产品D', '产品E'],
        '销量': [100, 150, 200, 180, 120],
        '价格': [99, 129, 199, 159, 109],
        '销售额': [9900, 19350, 39800, 28620, 13080],
        '区域': ['北京', '上海', '广州', '深圳', '北京']
    }
    df = pd.DataFrame(data)

    print("\n数据预览:")
    print(df.head())

    print("\n数据信息:")
    print(f"行数: {len(df)}")
    print(f"列数: {len(df.columns)}")

    print("\n数值统计:")
    print(df.describe())

    print("\n区域分析:")
    region_sales = df.groupby('区域')['销售额'].sum()
    print(region_sales)

    return df


def example_2_data_cleaning():
    """示例2: 数据清洗"""
    print("\n" + "=" * 50)
    print("示例2: 数据清洗")
    print("=" * 50)

    # 创建包含问题的数据
    data = {
        '姓名': ['张三 ', ' 李四', '王五', None, '赵六'],
        '年龄': [25, 30, None, 28, 35],
        '城市': ['北京', '上海', '北京', '广州', '上海'],
        '收入': [10000, 15000, 12000, None, 20000]
    }
    df = pd.DataFrame(data)

    print("\n原始数据:")
    print(df)

    processor = ExcelProcessor()

    # 清洗数据
    df_clean = processor.clean_data(
        df,
        dropna_cols=['姓名'],  # 删除姓名为空的行
        fillna_dict={'年龄': df['年龄'].mean(), '收入': df['收入'].mean()},  # 填充平均值
        strip_cols=['姓名', '城市']  # 去除空格
    )

    print("\n清洗后数据:")
    print(df_clean)

    return df_clean


def example_3_filter_and_sort():
    """示例3: 数据筛选和排序"""
    print("\n" + "=" * 50)
    print("示例3: 数据筛选和排序")
    print("=" * 50)

    data = {
        '员工': ['张三', '李四', '王五', '赵六', '孙七'],
        '部门': ['技术', '销售', '技术', '市场', '销售'],
        '销售额': [50000, 80000, 60000, 70000, 90000],
        '完成率': [0.85, 1.2, 0.9, 1.1, 1.3]
    }
    df = pd.DataFrame(data)

    print("\n原始数据:")
    print(df)

    # 筛选1: 销售额大于60000
    high_sales = df[df['销售额'] > 60000]
    print("\n销售额 > 60000:")
    print(high_sales)

    # 筛选2: 技术部门
    tech_dept = df[df['部门'] == '技术']
    print("\n技术部门:")
    print(tech_dept)

    # 筛选3: 多条件（销售部 + 完成率 > 1.0）
    sales_overperform = df[(df['部门'] == '销售') & (df['完成率'] > 1.0)]
    print("\n销售部门且完成率 > 1.0:")
    print(sales_overperform)

    # 排序
    df_sorted = df.sort_values('销售额', ascending=False)
    print("\n按销售额降序:")
    print(df_sorted)

    return df


def example_4_pivot_table():
    """示例4: 数据透视表"""
    print("\n" + "=" * 50)
    print("示例4: 数据透视表")
    print("=" * 50)

    data = {
        '产品': ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'C'],
        '地区': ['北京', '上海', '北京', '上海', '北京', '上海', '北京', '上海', '北京'],
        '季度': ['Q1', 'Q1', 'Q1', 'Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2'],
        '销售额': [100, 120, 80, 90, 110, 130, 105, 95, 115]
    }
    df = pd.DataFrame(data)

    print("\n原始数据:")
    print(df)

    processor = ExcelProcessor()

    # 透视表1: 产品 × 地区
    pivot1 = processor.create_pivot_table(
        df,
        index='产品',
        columns='地区',
        values='销售额',
        aggfunc='sum'
    )
    print("\n透视表 - 产品×地区:")
    print(pivot1)

    # 透视表2: 产品 × 季度
    pivot2 = processor.create_pivot_table(
        df,
        index='产品',
        columns='季度',
        values='销售额',
        aggfunc='mean'
    )
    print("\n透视表 - 产品×季度 (平均):")
    print(pivot2)

    return df


def example_5_project_management():
    """示例5: 项目管理模板"""
    print("\n" + "=" * 50)
    print("示例5: 项目管理模板")
    print("=" * 50)

    pm = ProjectManager()

    # 创建模板
    print("\n创建项目管理模板...")

    # 创建输出目录
    os.makedirs('examples/output', exist_ok=True)

    # 进度跟踪表
    pm.create_progress_tracker('examples/output/进度表.xlsx')
    print("✓ 进度跟踪表")

    # 资源分配表
    pm.create_resource_allocation('examples/output/资源表.xlsx')
    print("✓ 资源分配表")

    # 风险登记册
    pm.create_risk_register('examples/output/风险表.xlsx')
    print("✓ 风险登记册")

    # 生成状态报告
    report = pm.generate_status_report(
        'examples/output/进度表.xlsx',
        'examples/output/项目状态报告.md'
    )
    print("\n✓ 项目状态报告已生成")

    return None


def example_6_write_and_format():
    """示例6: 写入和格式化 Excel"""
    print("\n" + "=" * 50)
    print("示例6: 写入和格式化 Excel")
    print("=" * 50)

    # 创建示例数据
    data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '收入': [100000, 120000, 115000, 130000, 145000, 160000],
        '支出': [80000, 85000, 90000, 95000, 100000, 105000],
        '利润': [20000, 35000, 25000, 35000, 45000, 55000]
    }
    df = pd.DataFrame(data)

    processor = ExcelProcessor()

    # 创建输出目录
    os.makedirs('examples/output', exist_ok=True)

    # 写入 Excel
    processor.write_excel(df, 'examples/output/财务报表.xlsx')

    # 格式化 Excel
    processor.format_excel('examples/output/财务报表.xlsx')

    print("\n✓ 财务报表已生成并格式化")

    # 多个 sheet
    data_dict = {
        '收入数据': pd.DataFrame({
            '月份': ['1月', '2月', '3月'],
            '金额': [100000, 120000, 115000]
        }),
        '支出数据': pd.DataFrame({
            '类别': ['人力', '办公', '营销'],
            '金额': [50000, 20000, 15000]
        })
    }

    processor.export_multiple_sheets(
        data_dict,
        'examples/output/多Sheet报表.xlsx',
        format_all=True
    )

    print("✓ 多 Sheet 报表已生成")

    return df


def example_7_merge_files():
    """示例7: 合并多个 Excel 文件"""
    print("\n" + "=" * 50)
    print("示例7: 合并多个 Excel 文件")
    print("=" * 50)

    processor = ExcelProcessor()

    # 创建示例文件
    os.makedirs('examples/output', exist_ok=True)

    file1 = pd.DataFrame({'部门': ['技术'], '人数': [10]})
    file2 = pd.DataFrame({'部门': ['销售'], '人数': [15]})
    file3 = pd.DataFrame({'部门': ['市场'], '人数': [8]})

    file1.to_excel('examples/output/部门数据1.xlsx', index=False)
    file2.to_excel('examples/output/部门数据2.xlsx', index=False)
    file3.to_excel('examples/output/部门数据3.xlsx', index=False)

    print("✓ 创建了3个示例文件")

    # 合并文件
    file_list = [
        'examples/output/部门数据1.xlsx',
        'examples/output/部门数据2.xlsx',
        'examples/output/部门数据3.xlsx'
    ]

    merged = processor.merge_excels(
        file_list,
        'examples/output/合并后的数据.xlsx',
        add_source=True
    )

    if merged is not None:
        print("\n合并后的数据:")
        print(merged)

    return merged


def example_8_generate_weekly_report():
    """示例8: 生成周报"""
    print("\n" + "=" * 50)
    print("示例8: 生成项目周报")
    print("=" * 50)

    pm = ProjectManager()

    # 假设已有进度表
    if not os.path.exists('examples/output/进度表.xlsx'):
        pm.create_progress_tracker('examples/output/进度表.xlsx')

    # 生成周报（假设当前周）
    from datetime import datetime, timedelta

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    report = pm.generate_weekly_report(
        'examples/output/进度表.xlsx',
        start_of_week.strftime('%Y-%m-%d'),
        end_of_week.strftime('%Y-%m-%d')
    )

    print("\n" + report)

    # 保存周报
    with open('examples/output/本周项目周报.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n✓ 周报已保存到 examples/output/本周项目周报.md")

    return report


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Excel 数据处理 - 快速入门示例")
    print("=" * 60)

    try:
        # 运行各个示例
        example_1_read_and_basic_analysis()
        example_2_data_cleaning()
        example_3_filter_and_sort()
        example_4_pivot_table()
        example_5_project_management()
        example_6_write_and_format()
        example_7_merge_files()
        example_8_generate_weekly_report()

        print("\n" + "=" * 60)
        print("✓ 所有示例运行完成!")
        print("=" * 60)
        print("\n生成的文件保存在 examples/output/ 目录下")

    except Exception as e:
        print(f"\n✗ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
