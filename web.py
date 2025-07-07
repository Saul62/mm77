import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os
from PIL import Image
import random

# 页面配置
st.set_page_config(
    page_title="木材智能监测系统",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2E8B57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8f0, transparent);
        border-left: 5px solid #2E8B57;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .alert-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .nav-button {
        width: 100%;
        margin-bottom: 0.5rem;
    }
    html {
        scroll-behavior: smooth;
    }
    .analysis-result-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .defect-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2E8B57;
    }
    .quality-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# 模拟数据生成函数
@st.cache_data
def generate_historical_data():
    """生成历史趋势数据"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    data = {
        'date': dates,
        'humidity': np.random.normal(65, 10, len(dates)),
        'temperature': np.random.normal(22, 5, len(dates)),
        'light': np.random.normal(500, 100, len(dates))
    }
    return pd.DataFrame(data)

@st.cache_data
def generate_defect_data():
    """生成缺陷数据"""
    defect_types = ['虫孔', '死节', '裂纹', '腐朽', '变色', '树脂囊']
    severities = ['高', '中', '低']
    
    data = []
    for i in range(50):
        data.append({
            'ID': f'DEF{i+1:03d}',
            '时间戳': datetime.now() - timedelta(days=random.randint(0, 30)),
            '位置': f'({random.randint(10, 200)}, {random.randint(10, 150)})',
            '缺陷类型': random.choice(defect_types),
            '严重性': random.choice(severities),
            '详情': f'检测到{random.choice(defect_types)}，需要进一步检查'
        })
    return pd.DataFrame(data)

def get_real_time_data():
    """获取实时传感器数据"""
    return {
        'humidity': round(random.uniform(60, 80), 1),
        'temperature': round(random.uniform(18, 28), 1),
        'light': round(random.uniform(400, 600), 0),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def login_page():
    """登录页面"""
    st.markdown('<h1 class="main-header">🌲 木材智能监测系统</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 用户登录")
        
        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            submit_button = st.form_submit_button("登录", use_container_width=True)
            
            if submit_button:
                if username == "demouser" and password == "password":
                    st.session_state.logged_in = True
                    st.success("登录成功！正在跳转到主仪表盘...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("用户名或密码错误，请重试。")
        
        st.info("💡 演示账号：用户名 `demouser`，密码 `password`")

def main_dashboard():
    """主仪表盘"""
    # 侧边栏导航
    with st.sidebar:
        st.markdown("### 🌲 导航菜单")
        st.markdown("点击下方按钮快速跳转到对应模块")

        # 创建导航链接
        st.markdown("#### 📊 监测数据")

        # 创建导航链接
        st.button("📊 实时数据", use_container_width=True, key="sidebar_real_time")
        st.button("📈 历史趋势", use_container_width=True, key="sidebar_historical")

        st.markdown("#### 🤖 智能分析")
        st.button("🤖 AI 分析", use_container_width=True, key="sidebar_ai")
        st.button("📷 图片识别", use_container_width=True, key="sidebar_image")

        st.markdown("#### 📋 日志管理")
        st.button("📋 缺陷日志", use_container_width=True, key="sidebar_defect")
        st.button("🚨 警报", use_container_width=True, key="sidebar_alerts")

        st.markdown("---")
        st.markdown("#### ⚙️ 系统设置")
        if st.button("🚪 退出登录", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.rerun()

    # 主标题
    st.markdown('<h1 class="main-header">木材智能监测系统 - 主仪表盘</h1>', unsafe_allow_html=True)

    # 添加系统概览
    st.markdown("### 📋 系统概览")

    # 创建概览卡片
    overview_col1, overview_col2, overview_col3 = st.columns(3)

    with overview_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 实时监测</h4>
            <p>• 木材湿度监测</p>
            <p>• 环境温度监测</p>
            <p>• 环境光照监测</p>
        </div>
        """, unsafe_allow_html=True)

    with overview_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 智能分析</h4>
            <p>• AI缺陷检测</p>
            <p>• 图片识别分析</p>
            <p>• 严重性评估</p>
        </div>
        """, unsafe_allow_html=True)

    with overview_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📋 数据管理</h4>
            <p>• 缺陷日志记录</p>
            <p>• 历史趋势分析</p>
            <p>• 警报信息管理</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### � 功能模块导航")
    st.markdown("以下是所有功能模块，您可以向下滚动查看详细内容，或使用左侧导航栏快速定位。")
    st.markdown("---")

    # 显示所有功能模块在一个页面上
    show_all_modules()

def show_all_modules():
    """在一个页面上显示所有功能模块"""

    # 实时数据模块
    st.markdown('<div id="real_time_data"></div>', unsafe_allow_html=True)
    show_real_time_data()
    st.markdown("---")

    # 历史趋势模块
    st.markdown('<div id="historical_trends"></div>', unsafe_allow_html=True)
    show_historical_trends()
    st.markdown("---")

    # AI分析模块
    st.markdown('<div id="ai_analysis"></div>', unsafe_allow_html=True)
    show_ai_analysis()
    st.markdown("---")

    # 图片识别模块
    st.markdown('<div id="image_recognition"></div>', unsafe_allow_html=True)
    show_image_recognition()
    st.markdown("---")

    # 缺陷日志模块
    st.markdown('<div id="defect_logs"></div>', unsafe_allow_html=True)
    show_defect_logs()
    st.markdown("---")

    # 警报模块
    st.markdown('<div id="alerts"></div>', unsafe_allow_html=True)
    show_alerts()

def show_real_time_data():
    """显示实时传感器数据"""
    st.markdown('<div class="section-header">📊 实时传感器数据</div>', unsafe_allow_html=True)
    
    # 创建占位符用于实时更新
    placeholder = st.empty()
    
    # 自动刷新按钮
    if st.button("🔄 刷新数据"):
        pass
    
    # 获取实时数据
    data = get_real_time_data()
    
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💧 木材湿度</h3>
                <h2>{data['humidity']}%</h2>
                <p>最后更新: {data['timestamp']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌡️ 环境温度</h3>
                <h2>{data['temperature']}°C</h2>
                <p>最后更新: {data['timestamp']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💡 环境光照</h3>
                <h2>{data['light']} Lux</h2>
                <p>最后更新: {data['timestamp']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_historical_trends():
    """显示历史趋势图表"""
    st.markdown('<div class="section-header">📈 历史趋势分析</div>', unsafe_allow_html=True)
    
    df = generate_historical_data()
    
    # 创建复合折线图
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['humidity'],
        mode='lines', name='湿度 (%)',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['temperature'],
        mode='lines', name='温度 (°C)',
        line=dict(color='red'),
        yaxis='y2'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['light'],
        mode='lines', name='光照 (Lux)',
        line=dict(color='orange'),
        yaxis='y3'
    ))
    
    fig.update_layout(
        title='木材监测历史趋势',
        xaxis_title='日期',
        yaxis=dict(title='湿度 (%)', side='left'),
        yaxis2=dict(title='温度 (°C)', side='right', overlaying='y'),
        yaxis3=dict(title='光照 (Lux)', side='right', overlaying='y', position=0.95),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_ai_analysis():
    """显示AI智能分析"""
    st.markdown('<div class="section-header">🤖 AI 智能分析</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["缺陷检测", "严重性评估", "缺陷摘要生成"])
    
    with tab1:
        st.markdown("### AI 缺陷检测")
        sensor_data = st.text_area(
            "传感器数据",
            value="湿度: 78%, 温度: 23°C, 振动: 0.2g, 声发射: 高",
            height=100
        )
        
        if st.button("分析缺陷", key="defect_analysis"):
            with st.spinner("正在分析..."):
                time.sleep(2)  # 模拟AI处理时间
                
                # 模拟AI分析结果
                has_defect = random.choice([True, False])
                if has_defect:
                    st.error("⚠️ 检测到缺陷")
                    st.write("**缺陷类型:** 裂纹")
                    st.write("**严重程度:** 高")
                    st.write("**解释:** 根据传感器数据分析，检测到异常振动和声发射信号，表明存在结构性裂纹。")
                else:
                    st.success("✅ 未检测到缺陷")
                    st.write("**解释:** 传感器数据显示所有参数均在正常范围内。")
                
                st.write(f"**分析所用数据:** {sensor_data}")
    
    with tab2:
        st.markdown("### AI 严重性评估")
        defect_type = st.text_input("缺陷类型", value="裂纹")
        sensor_data_severity = st.text_area("相关传感器数据", value="湿度: 78%, 温度: 23°C", height=80)
        historical_trends = st.text_area("历史趋势", value="过去30天湿度持续偏高", height=80)
        
        if st.button("评估严重性", key="severity_analysis"):
            with st.spinner("正在评估..."):
                time.sleep(2)
                
                severity_score = random.randint(6, 9)
                st.write(f"**严重性评分:** {severity_score}/10")
                st.progress(severity_score / 10)
                st.write("**描述:** 该缺陷具有较高的严重性，可能影响木材的结构完整性。")
                st.write("**建议措施:** 建议立即进行详细检查，考虑更换或修复。")
    
    with tab3:
        st.markdown("### AI 缺陷摘要生成")
        xml_data = st.text_area(
            "缺陷数据 (XML 格式)",
            value="""<defects>
  <defect>
    <coordinates>120,80</coordinates>
    <severity>高</severity>
    <defectName>裂纹</defectName>
  </defect>
  <defect>
    <coordinates>200,150</coordinates>
    <severity>中</severity>
    <defectName>虫孔</defectName>
  </defect>
</defects>""",
            height=150
        )
        
        if st.button("生成摘要", key="summary_generation"):
            with st.spinner("正在生成摘要..."):
                time.sleep(2)
                
                st.markdown("**生成的缺陷摘要:**")
                st.write("检测报告显示木材样本存在2处缺陷。在坐标(120,80)位置发现高严重性裂纹，在坐标(200,150)位置发现中等严重性虫孔。建议对高严重性缺陷进行优先处理。")

def show_image_recognition():
    """显示图片识别功能"""
    st.markdown('<div class="section-header">📷 木材图片识别分析</div>', unsafe_allow_html=True)

    # 检查木材图片目录
    image_dir = "木材图"
    if os.path.exists(image_dir):
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        # 筛选出原始图片（不包含_1的图片）
        original_images = [f for f in image_files if '_1' not in f]

        if original_images:
            st.markdown("### 选择木材图片进行分析")

            # 图片选择
            selected_image = st.selectbox("选择图片", original_images)

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("#### 原始图片")
                image_path = os.path.join(image_dir, selected_image)
                image = Image.open(image_path)
                st.image(image, caption=f"木材图片: {selected_image}", use_container_width=True)

            with col2:
                st.markdown("#### 🤖 AI 分析控制")

                if st.button("🔍 开始图片分析", key="image_analysis", use_container_width=True, type="primary"):
                    with st.spinner("🔄 AI正在分析图片，请稍候..."):
                        time.sleep(3)  # 模拟AI处理时间

                        # 生成对应的分析结果图片路径
                        base_name = selected_image.split('.')[0]  # 获取文件名（不含扩展名）
                        result_image_name = f"{base_name}_1.jpg"
                        result_image_path = os.path.join(image_dir, result_image_name)

                        # 根据图片名称生成特定的分析结果
                        analysis_results = get_image_analysis_results(base_name)

                        # 重新布局显示结果
                        st.markdown('<div class="analysis-result-container">', unsafe_allow_html=True)
                        st.markdown("## 📊 AI 分析结果")

                        # 创建两列布局：结果图、分析文字
                        result_col1, result_col2 = st.columns([1, 1])

                        with result_col1:
                            st.markdown("### 🔍 检测结果图")
                            if os.path.exists(result_image_path):
                                result_image = Image.open(result_image_path)
                                st.image(result_image, caption=f"AI检测: {result_image_name}", use_container_width=True)
                            else:
                                st.info("未找到对应的检测结果图片")

                        with result_col2:
                            st.markdown("### 📋 分析结果")

                            # 显示分析文字描述
                            st.markdown(f"**检测结果**: {analysis_results['description']}")

                            # 质量等级卡片
                            grade_color = {
                                'A+级': '#4CAF50', 'A级': '#8BC34A', 'B级': '#FFC107',
                                'C级': '#FF9800', 'D级': '#F44336'
                            }.get(analysis_results['quality_grade'], '#9E9E9E')

                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, {grade_color}20, {grade_color}10);
                                border-left: 4px solid {grade_color};
                                padding: 1rem;
                                border-radius: 8px;
                                margin: 1rem 0;
                            ">
                                <h4 style="color: {grade_color}; margin: 0;">
                                    🏆 质量等级: {analysis_results['quality_grade']}
                                </h4>
                                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                                    <strong>建议措施:</strong> {analysis_results['recommendation']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)

            # 批量分析功能
            st.markdown("### 批量图片分析")
            if st.button("分析所有图片", key="batch_analysis"):
                progress_bar = st.progress(0)

                results = []
                for i, img_file in enumerate(original_images[:6]):  # 限制显示前6张原始图片
                    progress_bar.progress((i + 1) / min(6, len(original_images)))

                    # 获取图片基础名称
                    base_name = img_file.split('.')[0]
                    analysis_result = get_image_analysis_results(base_name)

                    # 根据描述判断是否有缺陷
                    has_defects = "半活节" in analysis_result['description'] or "腐朽" in analysis_result['description'] or "缺陷" in analysis_result['description']

                    results.append({
                        '图片名称': img_file,
                        '检测结果': analysis_result['description'][:30] + "..." if len(analysis_result['description']) > 30 else analysis_result['description'],
                        '质量等级': analysis_result['quality_grade'],
                        '状态': '需检查' if has_defects else '正常'
                    })

                # 显示结果表格
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
        else:
            st.warning("木材图片目录中没有找到图片文件。")
    else:
        st.error("未找到木材图片目录。请确保 '木材图' 文件夹存在。")

def get_image_analysis_results(image_base_name):
    """根据图片名称生成特定的分析结果"""

    # 预定义的分析结果数据
    analysis_data = {
        "1": {
            "description": "检测到四个半活节和一个腐朽缺陷。半活节分布在木材表面，腐朽区域位于边缘部分，影响木材整体质量。",
            "quality_grade": "C级",
            "recommendation": "建议进行修补处理或降级使用，特别注意腐朽区域的处理"
        },
        "2": {
            "description": "检测到三个半活节缺陷。半活节分布较为均匀，对木材结构影响相对较小。",
            "quality_grade": "B级",
            "recommendation": "可正常使用，注意监控半活节区域的变化"
        },
        "3": {
            "description": "检测到三个半活节缺陷。半活节位置分散，整体木材质量尚可。",
            "quality_grade": "B级",
            "recommendation": "适合一般用途，建议定期检查半活节区域"
        },
        "4": {
            "description": "检测到六处半活结缺陷，主要为轻微的表面瑕疵，对整体质量影响较小。",
            "quality_grade": "B级",
            "recommendation": "质量良好，可用于高要求应用"
        },
        "5": {
            "description": "检测到7处半活结缺陷，三处刀痕以及四处死结。",
            "quality_grade": "D级",
            "recommendation": "不建议使用该木料"
        },
        "6": {
            "description": "检测到十处以上半活结、五处腐朽以及一处刀痕。",
            "quality_grade": "D级",
            "recommendation": "不建议使用该木料"
        },
        "7": {
            "description": "检测到9处半活结缺陷，对结构有一定影响。",
            "quality_grade": "B级",
            "recommendation": "质量良好，可正常使用"
        },
        "8": {
            "description": "检测到一处半活结，四处腐朽和四处裂痕影响了主要结构。",
            "quality_grade": "C级",
            "recommendation": "修补后使用"
        },
        "9": {
            "description": "检测到三处半活结和三处刀痕，伴随重大裂缝。",
            "quality_grade": "D级",
            "recommendation": "不建议使用该木料"
        }
    }

    # 如果有预定义数据则使用，否则生成随机数据
    if image_base_name in analysis_data:
        return analysis_data[image_base_name]
    else:
        # 生成随机分析结果作为备用
        descriptions = [
            "检测到少量缺陷，整体质量良好。",
            "发现轻微的表面瑕疵，不影响主要功能。",
            "检测到一些纹理不规则，但结构稳定。"
        ]

        quality_grades = ['A+级', 'A级', 'B级', 'C级']
        recommendations = [
            "优质木材，适合精密加工",
            "质量良好，可正常使用",
            "适合一般用途",
            "建议降级使用"
        ]

        return {
            "description": random.choice(descriptions),
            "quality_grade": random.choice(quality_grades),
            "recommendation": random.choice(recommendations)
        }

def show_defect_logs():
    """显示缺陷日志和分布"""
    st.markdown('<div class="section-header">📋 详细缺陷日志与分布</div>', unsafe_allow_html=True)

    # 生成缺陷数据
    df = generate_defect_data()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 缺陷类型分布")

        # 创建饼图
        defect_counts = df['缺陷类型'].value_counts()
        fig_pie = px.pie(
            values=defect_counts.values,
            names=defect_counts.index,
            title="缺陷类型分布图"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### 严重性统计")

        # 创建柱状图
        severity_counts = df['严重性'].value_counts()
        fig_bar = px.bar(
            x=severity_counts.index,
            y=severity_counts.values,
            title="缺陷严重性分布",
            color=severity_counts.index,
            color_discrete_map={'高': 'red', '中': 'orange', '低': 'green'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 详细缺陷日志")

    # 过滤器
    col1, col2, col3 = st.columns(3)
    with col1:
        defect_filter = st.multiselect(
            "筛选缺陷类型",
            options=df['缺陷类型'].unique(),
            default=df['缺陷类型'].unique()
        )
    with col2:
        severity_filter = st.multiselect(
            "筛选严重性",
            options=df['严重性'].unique(),
            default=df['严重性'].unique()
        )
    with col3:
        date_range = st.date_input(
            "选择日期范围",
            value=(datetime.now().date() - timedelta(days=30), datetime.now().date()),
            max_value=datetime.now().date()
        )

    # 应用过滤器
    filtered_df = df[
        (df['缺陷类型'].isin(defect_filter)) &
        (df['严重性'].isin(severity_filter))
    ]

    # 显示过滤后的数据表格
    st.dataframe(
        filtered_df.style.apply(
            lambda x: ['background-color: #ffebee' if x['严重性'] == '高'
                      else 'background-color: #fff3e0' if x['严重性'] == '中'
                      else 'background-color: #e8f5e8' for i in x], axis=1
        ),
        use_container_width=True,
        height=400
    )

    # 导出功能
    if st.button("📥 导出缺陷日志"):
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="下载 CSV 文件",
            data=csv,
            file_name=f"defect_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def show_alerts():
    """显示警报信息"""
    st.markdown('<div class="section-header">🚨 警报信息</div>', unsafe_allow_html=True)

    # 生成模拟警报数据
    if not st.session_state.alerts:
        alerts = [
            {
                'id': 1,
                'title': '高湿度警报',
                'description': '检测到木材湿度超过安全阈值 (85%)',
                'severity': '高',
                'timestamp': datetime.now() - timedelta(hours=2),
                'read': False
            },
            {
                'id': 2,
                'title': '温度异常',
                'description': '环境温度持续偏高，可能影响木材质量',
                'severity': '中',
                'timestamp': datetime.now() - timedelta(hours=5),
                'read': False
            },
            {
                'id': 3,
                'title': '缺陷检测',
                'description': 'AI系统检测到新的木材缺陷',
                'severity': '高',
                'timestamp': datetime.now() - timedelta(hours=8),
                'read': True
            },
            {
                'id': 4,
                'title': '系统维护提醒',
                'description': '传感器需要定期校准',
                'severity': '低',
                'timestamp': datetime.now() - timedelta(days=1),
                'read': False
            }
        ]
        st.session_state.alerts = alerts

    # 统计未读警报
    unread_count = sum(1 for alert in st.session_state.alerts if not alert['read'])

    # 显示未读警报数量
    if unread_count > 0:
        st.warning(f"📢 您有 {unread_count} 条未读警报")
    else:
        st.success("✅ 所有警报已读")

    # 警报操作按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 刷新警报"):
            st.rerun()
    with col2:
        if st.button("✅ 全部标记为已读"):
            for alert in st.session_state.alerts:
                alert['read'] = True
            st.success("所有警报已标记为已读")
            st.rerun()

    st.markdown("---")

    # 显示警报列表
    for alert in st.session_state.alerts:
        # 根据严重性选择样式
        if alert['severity'] == '高':
            alert_class = 'alert-high'
            icon = '🔴'
        elif alert['severity'] == '中':
            alert_class = 'alert-medium'
            icon = '🟡'
        else:
            alert_class = 'alert-low'
            icon = '🟢'

        # 未读警报高亮显示
        background_style = "background-color: #f0f8ff;" if not alert['read'] else ""

        st.markdown(f"""
        <div class="{alert_class}" style="{background_style}">
            <h4>{icon} {alert['title']} {'🔔' if not alert['read'] else ''}</h4>
            <p>{alert['description']}</p>
            <small>严重性: {alert['severity']} | 时间: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)

        # 标记为已读按钮
        if not alert['read']:
            if st.button(f"标记为已读", key=f"read_{alert['id']}"):
                alert['read'] = True
                st.success("警报已标记为已读")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

# 主程序入口
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
