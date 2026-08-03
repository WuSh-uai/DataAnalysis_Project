import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from datetime import datetime
import sqlite3
import os
import sys
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi']
matplotlib.rcParams['axes.unicode_minus'] = False

# 添加Django项目路径以访问数据库
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 页面配置
st.set_page_config(
    page_title="校园消费数据分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 加载数据的函数
@st.cache_data(ttl=600)
def load_data():
    """从SQLite数据库加载消费数据"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')

    if not os.path.exists(db_path):
        # 如果没有数据库，使用示例数据
        return create_sample_data()

    try:
        conn = sqlite3.connect(db_path)
        query = """
            SELECT student_id, name, consumption_type, amount, consumption_time, location
            FROM consumption
            ORDER BY consumption_time
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return create_sample_data()

        # 数据类型转换
        df['amount'] = pd.to_numeric(df['amount'])
        df['consumption_time'] = pd.to_datetime(df['consumption_time'])

        return df
    except Exception as e:
        st.warning(f"无法连接数据库，使用示例数据: {e}")
        return create_sample_data()


def create_sample_data():
    """创建示例数据"""
    data = {
        'student_id': ['2026001', '2026002', '2026003', '2026004', '2026005', '2026006', '2026007', '2026008'],
        'name': ['张三', '李四', '王五', '赵六', '孙七', '周八', '吴九', '郑十'],
        'consumption_type': ['餐饮', '文具', '餐饮', '饮品', '文具', '餐饮', '饮品', '餐饮'],
        'amount': [18.5, 25.0, 22.0, 8.0, 36.0, 15.0, 12.0, 28.0],
        'consumption_time': pd.to_datetime(['2026-06-01', '2026-06-01', '2026-06-02', '2026-06-02',
                                            '2026-06-03', '2026-06-03', '2026-06-04', '2026-06-04']),
        'location': ['一食堂', '校园超市', '二食堂', '奶茶店', '校园超市', '一食堂', '奶茶店', '二食堂']
    }
    return pd.DataFrame(data)


# 计算每日消费总额的函数
def calculate_daily_amount(df):
    """计算每日消费总额"""
    daily = df.groupby(df['consumption_time'].dt.date)['amount'].sum().reset_index()
    daily.columns = ['日期', '当日总消费金额']
    return daily


# 计算地点消费统计的函数
def calculate_location_stats(df):
    """计算各地点消费统计"""
    stats = df.groupby('location').agg({
        'amount': ['sum', 'count']
    }).reset_index()
    stats.columns = ['消费地点', '累计消费金额', '消费次数']
    return stats


# 主页面标题
st.title("🏫 校园消费数据可视化分析平台")
st.markdown("---")

# ==================== 侧边栏筛选 ====================
st.sidebar.header("🔍 数据筛选")

# 加载数据
df = load_data()

# 侧边栏筛选控件 - 按消费地点
st.sidebar.subheader("按消费地点筛选")
locations = ['全部'] + sorted(df['location'].unique().tolist())
selected_location = st.sidebar.selectbox("选择消费地点", locations)

# 侧边栏筛选控件 - 按消费时间
st.sidebar.subheader("按消费时间筛选")
min_date = df['consumption_time'].min().date()
max_date = df['consumption_time'].max().date()

date_range = st.sidebar.date_input(
    "选择日期范围",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 侧边栏信息
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **平台功能：**
    - 📊 消费类型占比分析
    - 📈 每日消费趋势变化
    - 🎯 地点-金额关联分析
    - 🔍 多维度数据筛选
    """
)

# 应用筛选条件
filtered_df = df.copy()
filtered_df['consumption_time'] = pd.to_datetime(filtered_df['consumption_time'])

# 地点筛选
if selected_location != '全部':
    filtered_df = filtered_df[filtered_df['location'] == selected_location]

# 时间筛选
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['consumption_time'].dt.date >= start_date) &
        (filtered_df['consumption_time'].dt.date <= end_date)
        ]

# 显示当前数据量
st.sidebar.metric("当前数据量", f"{len(filtered_df)} 条记录")

# ==================== 主内容区域 - 选项卡 ====================
tab1, tab2, tab3 = st.tabs(["📊 消费类型分析", "📈 消费趋势分析", "🎯 地点-金额分析"])

# -------------------- Tab 1: Matplotlib 柱状图 --------------------
with tab1:
    st.header("消费类型占比分析")
    st.markdown("使用 **Matplotlib** 绘制消费类型金额占比柱状图")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Matplotlib 柱状图
        type_amount = filtered_df.groupby('consumption_type')['amount'].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax.bar(type_amount.index, type_amount.values, color=colors[:len(type_amount)])

        # 添加数值标签
        for bar, value in zip(bars, type_amount.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'¥{value:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('消费类型', fontsize=12)
        ax.set_ylabel('消费金额 (元)', fontsize=12)
        ax.set_title('不同消费类型总金额对比', fontsize=14, fontweight='bold')
        ax.set_facecolor('#f8f9fa')
        ax.grid(axis='y', alpha=0.3)

        st.pyplot(fig)
        plt.close()

    with col2:
        # 数据显示
        st.subheader("消费类型统计")
        st.write(f"**当前筛选后数据:** {len(filtered_df)} 条记录")
        st.markdown("---")

        for type_name, amount in type_amount.items():
            percentage = (amount / type_amount.sum()) * 100
            st.metric(
                label=f"🍽️ {type_name}",
                value=f"¥{amount:.1f}",
                delta=f"{percentage:.1f}% 占比"
            )

# -------------------- Tab 2: Plotly 交互式折线图 --------------------
with tab2:
    st.header("每日消费金额趋势分析")
    st.markdown("使用 **Plotly** 绘制交互式折线图，支持缩放、悬停查看详情")

    # 计算每日消费总额
    daily_amount = filtered_df.groupby(filtered_df['consumption_time'].dt.date)['amount'].sum().reset_index()
    daily_amount.columns = ['日期', '消费金额']

    # 使用 Plotly 绘制交互式折线图
    fig = px.line(
        daily_amount,
        x='日期',
        y='消费金额',
        title='每日消费金额变化趋势',
        markers=True,
        line_shape='linear'
    )

    fig.update_traces(
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8, color='#4ECDC4', symbol='circle')
    )

    fig.update_layout(
        xaxis_title='日期',
        yaxis_title='消费金额 (元)',
        hovermode='x unified',
        plot_bgcolor='#f8f9fa',
        title_font_size=16
    )

    fig.add_hline(
        y=daily_amount['消费金额'].mean(),
        line_dash="dash",
        line_color="green",
        annotation_text=f"平均消费: ¥{daily_amount['消费金额'].mean():.1f}"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 显示每日明细
    with st.expander("📋 查看每日消费明细"):
        st.dataframe(
            daily_amount.style.format({'消费金额': '¥{:.2f}'}),
            use_container_width=True,
            hide_index=True
        )

# -------------------- Tab 3: Altair 散点图 --------------------
with tab3:
    st.header("消费地点与消费金额关联分析")
    st.markdown("使用 **Altair** 绘制散点图，展示各地点消费金额分布")

    col1, col2 = st.columns([2, 1])

    with col1:
        # 计算各地点统计
        location_stats = filtered_df.groupby('location').agg({
            'amount': ['sum', 'count', 'mean']
        }).reset_index()
        location_stats.columns = ['消费地点', '累计消费金额', '消费次数', '平均消费金额']
        location_stats['平均消费金额'] = location_stats['平均消费金额'].round(2)

        # Altair 散点图
        scatter = alt.Chart(location_stats).mark_circle(size=100).encode(
            x=alt.X('消费次数:Q', title='消费次数'),
            y=alt.Y('累计消费金额:Q', title='累计消费金额 (元)'),
            size=alt.Size('平均消费金额:Q', title='平均消费金额'),
            color=alt.Color('消费地点:N', legend=alt.Legend(title="消费地点")),
            tooltip=['消费地点', '消费次数', '累计消费金额', '平均消费金额']
        ).properties(
            title='消费地点关联分析：次数 vs 金额',
            height=400
        ).interactive()

        # 添加趋势线
        trend_line = scatter.transform_regression('消费次数', '累计消费金额').mark_line(color='red', strokeDash=[5, 5])

        st.altair_chart(scatter + trend_line, use_container_width=True)

    with col2:
        st.subheader("地点消费统计")
        st.dataframe(
            location_stats.style.format({
                '累计消费金额': '¥{:.1f}',
                '平均消费金额': '¥{:.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )

        # 饼图展示各地点金额占比
        fig_pie, ax_pie = plt.subplots(figsize=(5, 4))
        ax_pie.pie(
            location_stats['累计消费金额'],
            labels=location_stats['消费地点'],
            autopct='%1.1f%%',
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        )
        ax_pie.set_title('各地点消费金额占比')
        st.pyplot(fig_pie)
        plt.close()

# ==================== 数据预览区域 ====================
st.markdown("---")
st.subheader("📋 原始数据预览")

with st.expander("点击展开查看详细数据"):
    display_df = filtered_df.copy()
    display_df['consumption_time'] = display_df['consumption_time'].dt.strftime('%Y-%m-%d')
    display_df = display_df.rename(columns={
        'student_id': '学号',
        'name': '姓名',
        'consumption_type': '消费类型',
        'amount': '消费金额',
        'consumption_time': '消费时间',
        'location': '消费地点'
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            '消费金额': st.column_config.NumberColumn(format="¥%.2f")
        }
    )

    st.caption(f"共 {len(filtered_df)} 条记录")

# ==================== 页脚 ====================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>校园消费数据展示与分析平台 | 基于 Streamlit + Django 开发</p>
        <p>数据可视化期末实验 | 更新时间: 2024</p>
    </div>
    """,
    unsafe_allow_html=True
)