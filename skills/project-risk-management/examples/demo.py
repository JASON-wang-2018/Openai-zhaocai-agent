"""
项目风险管理工具 - 使用示例
演示如何进行风险识别、评估、跟踪和应对
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from risk_manager import RiskManager, RiskAssessmentHelper


def demo_1_create_risk_register():
    """演示1: 创建风险登记册"""
    print("=" * 60)
    print("演示1: 创建风险登记册")
    print("=" * 60)

    rm = RiskManager()
    df = rm.create_risk_register('examples/risk_register_demo.xlsx')

    print("\n✓ 风险登记册已创建")
    print(f"  - 总风险数: {len(df)}")
    print(f"  - 文件路径: examples/risk_register_demo.xlsx")

    # 统计风险分布
    print(f"\n风险分布:")
    print(f"  - 高风险: {len(df[df['风险等级'] == '高'])}")
    print(f"  - 中风险: {len(df[df['风险等级'] == '中'])}")
    print(f"  - 低风险: {len(df[df['风险等级'] == '低'])}")

    return df


def demo_2_add_new_risk():
    """演示2: 添加新风险"""
    print("\n" + "=" * 60)
    print("演示2: 添加新风险")
    print("=" * 60)

    rm = RiskManager()

    # 创建风险登记册（如果不存在）
    if not os.path.exists('examples/risk_register_demo.xlsx'):
        rm.create_risk_register('examples/risk_register_demo.xlsx')

    # 添加几个新风险
    new_risks = [
        {
            '风险描述': '云服务商可能出现故障，导致系统不可用',
            '风险类别': '技术',
            '可能性(1-3)': 1,
            '影响程度(1-3)': 3,
            '应对策略': '缓解',
            '应对措施': '使用多云架构，做灾备方案',
            '责任人': '技术总监'
        },
        {
            '风险描述': '预算可能不足，需要削减功能',
            '风险类别': '资源',
            '可能性(1-3)': 2,
            '影响程度(1-3)': 2,
            '应对策略': '缓解',
            '应对措施': '提前核算成本，预留20%预算',
            '责任人': '项目经理'
        },
        {
            '风险描述': '竞争对手可能提前发布类似产品',
            '风险类别': '外部',
            '可能性(1-3)': 2,
            '影响程度(1-3)': 2,
            '应对策略': '缓解',
            '应对措施': '加快开发进度，做差异化',
            '责任人': '产品经理'
        }
    ]

    for risk in new_risks:
        rm.add_risk('examples/risk_register_demo.xlsx', risk)

    print("\n✓ 新风险已添加")


def demo_3_update_risk_status():
    """演示3: 更新风险状态"""
    print("\n" + "=" * 60)
    print("演示3: 更新风险状态")
    print("=" * 60)

    rm = RiskManager()

    # 创建风险登记册（如果不存在）
    if not os.path.exists('examples/risk_register_demo.xlsx'):
        rm.create_risk_register('examples/risk_register_demo.xlsx')

    # 模拟风险触发
    rm.update_risk_status('examples/risk_register_demo.xlsx', 'R001',
                          '已触发',
                          trigger_event='第三方API在周三宕机3小时')

    # 模拟风险缓解
    rm.update_risk_status('examples/risk_register_demo.xlsx', 'R002', '已缓解')

    # 模拟风险关闭
    rm.update_risk_status('examples/risk_register_demo.xlsx', 'R003', '已关闭')

    print("\n✓ 风险状态已更新")


def demo_4_generate_risk_report():
    """演示4: 生成风险报告"""
    print("\n" + "=" * 60)
    print("演示4: 生成风险报告")
    print("=" * 60)

    rm = RiskManager()

    # 创建风险登记册（如果不存在）
    if not os.path.exists('examples/risk_register_demo.xlsx'):
        rm.create_risk_register('examples/risk_register_demo.xlsx')

    # 生成报告
    report = rm.generate_risk_report('examples/risk_register_demo.xlsx',
                                    'examples/risk_report_demo.md')

    print("\n✓ 风险报告已生成")
    print(f"  - 文件路径: examples/risk_report_demo.md")

    # 显示报告摘要
    print("\n报告摘要:")
    lines = report.split('\n')
    for i, line in enumerate(lines):
        if i >= 20:  # 只显示前20行
            break
        print(line)


def demo_5_analyze_risks():
    """演示5: 分析风险"""
    print("\n" + "=" * 60)
    print("演示5: 分析风险")
    print("=" * 60)

    rm = RiskManager()

    # 创建风险登记册（如果不存在）
    if not os.path.exists('examples/risk_register_demo.xlsx'):
        rm.create_risk_register('examples/risk_register_demo.xlsx')

    # 分析风险
    analysis = rm.analyze_risks('examples/risk_register_demo.xlsx')

    print(f"\n风险分析结果:")
    print(f"  - 总风险数: {analysis['总风险数']}")
    print(f"  - 平均可能性: {analysis['平均可能性']:.1f}/3")
    print(f"  - 平均影响: {analysis['平均影响']:.1f}/3")

    print(f"\n按等级分布:")
    for level, count in analysis['按等级分布'].items():
        icon = '🔴' if level == '高' else '🟡' if level == '中' else '🟢'
        print(f"  - {icon} {level}: {count}")

    print(f"\n按类别分布:")
    for category, count in analysis['按类别分布'].items():
        print(f"  - {category}: {count}")

    print(f"\n按状态分布:")
    for status, count in analysis['按状态分布'].items():
        print(f"  - {status}: {count}")


def demo_6_auto_assess():
    """演示6: 自动评估风险"""
    print("\n" + "=" * 60)
    print("演示6: 自动评估风险")
    print("=" * 60)

    helper = RiskAssessmentHelper()

    # 测试风险描述
    test_risks = [
        '服务器经常宕机，可能导致系统完全不可用',
        '偶尔会出现性能问题，影响部分用户',
        '很少出现bug，影响很小',
        '可能导致项目失败',
        '可能需要延期一周'
    ]

    print("\n自动评估结果:")
    for desc in test_risks:
        likelihood = helper.assess_likelihood(desc)
        impact = helper.assess_impact(desc)
        strategy = helper.suggest_strategy(likelihood, impact)

        print(f"\n风险: {desc}")
        print(f"  - 可能性: {likelihood}/3")
        print(f"  - 影响: {impact}/3")
        print(f"  - 建议策略: {strategy}")


def demo_7_full_workflow():
    """演示7: 完整工作流"""
    print("\n" + "=" * 60)
    print("演示7: 完整工作流")
    print("=" * 60)

    rm = RiskManager()

    print("\n步骤1: 创建风险登记册")
    rm.create_risk_register('examples/project_risks.xlsx')

    print("\n步骤2: 添加项目特定风险")
    project_risks = [
        {
            '风险描述': 'UI设计可能不满意，需要反复修改',
            '风险类别': '质量',
            '可能性(1-3)': 3,
            '影响程度(1-3)': 1,
            '应对策略': '缓解',
            '应对措施': '提前做原型演示，收集反馈',
            '责任人': 'UI设计师'
        },
        {
            '风险描述': '移动端适配可能有问题',
            '风险类别': '技术',
            '可能性(1-3)': 2,
            '影响程度(1-3)': 2,
            '应对策略': '缓解',
            '应对措施': '提前做移动端测试',
            '责任人': '前端开发'
        },
        {
            '风险描述': '用户培训可能不足',
            '风险类别': '资源',
            '可能性(1-3)': 2,
            '影响程度(1-3)': 1,
            '应对策略': '缓解',
            '应对措施': '准备培训材料，提前培训',
            '责任人': '项目经理'
        }
    ]

    for risk in project_risks:
        rm.add_risk('examples/project_risks.xlsx', risk)

    print("\n步骤3: 生成风险报告")
    rm.generate_risk_report('examples/project_risks.xlsx',
                           'examples/project_risk_report.md')

    print("\n步骤4: 导出风险数据")
    rm.export_to_json('examples/project_risks.xlsx',
                      'examples/project_risks.json')

    print("\n✓ 完整工作流演示完成")


def demo_8_risk_monitoring():
    """演示8: 风险监控流程"""
    print("\n" + "=" * 60)
    print("演示8: 风险监控流程")
    print("=" * 60)

    rm = RiskManager()

    # 创建风险登记册
    if not os.path.exists('examples/risk_monitoring.xlsx'):
        rm.create_risk_register('examples/risk_monitoring.xlsx')

    print("\n第1周检查:")
    analysis = rm.analyze_risks('examples/risk_monitoring.xlsx')
    print(f"  - 监控中风险: {analysis['按状态分布'].get('监控中', 0)}")
    print(f"  - 已触发风险: {analysis['按状态分布'].get('已触发', 0)}")

    print("\n第2周检查:")
    # 模拟一个风险触发
    rm.update_risk_status('examples/risk_monitoring.xlsx', 'R004', '已触发',
                          trigger_event='测试人员临时请假，测试进度滞后')
    analysis = rm.analyze_risks('examples/risk_monitoring.xlsx')
    print(f"  - 监控中风险: {analysis['按状态分布'].get('监控中', 0)}")
    print(f"  - 已触发风险: {analysis['按状态分布'].get('已触发', 0)}")

    print("\n第3周检查:")
    # 模拟风险缓解
    rm.update_risk_status('examples/risk_monitoring.xlsx', 'R004', '已缓解')
    analysis = rm.analyze_risks('examples/risk_monitoring.xlsx')
    print(f"  - 监控中风险: {analysis['按状态分布'].get('监控中', 0)}")
    print(f"  - 已触发风险: {analysis['按状态分布'].get('已触发', 0)}")

    print("\n✓ 风险监控流程演示完成")


def main():
    """运行所有演示"""
    print("\n" + "=" * 60)
    print("项目风险管理工具 - 使用示例")
    print("=" * 60)

    # 创建输出目录
    os.makedirs('examples', exist_ok=True)

    try:
        # 运行演示
        demo_1_create_risk_register()
        demo_2_add_new_risk()
        demo_3_update_risk_status()
        demo_4_generate_risk_report()
        demo_5_analyze_risks()
        demo_6_auto_assess()
        demo_7_full_workflow()
        demo_8_risk_monitoring()

        print("\n" + "=" * 60)
        print("✓ 所有演示运行完成!")
        print("=" * 60)
        print("\n生成的文件:")
        print("  - examples/risk_register_demo.xlsx")
        print("  - examples/risk_report_demo.md")
        print("  - examples/project_risks.xlsx")
        print("  - examples/project_risk_report.md")
        print("  - examples/project_risks.json")
        print("  - examples/risk_monitoring.xlsx")

    except Exception as e:
        print(f"\n✗ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
