import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import matplotlib.patheffects as path_effects
import mpl_toolkits.axisartist as axisartist
from matplotlib.font_manager import FontProperties

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形和坐标轴 - 按照模板样式设置
fig = plt.figure(figsize=(18, 10))
ax = fig.add_subplot(111)

# 移除默认的轴
ax.axis('off')

# 创建标题框
title_box = Rectangle((0.05, 0.92), 0.9, 0.06, transform=fig.transFigure, 
                      facecolor='lightgray', edgecolor='black', alpha=0.7)
fig.patches.append(title_box)

# 添加标题
fig.text(0.5, 0.94, '白庙子早古生界地层实测剖面图', 
         ha='center', va='center', fontsize=20, fontweight='bold')

# 添加比例尺和测量日期
fig.text(0.05, 0.88, '比 例 尺：1:500', fontsize=12)
fig.text(0.25, 0.88, '测量日期：2025.7.11', fontsize=12)

# 添加制图人、技术负责、审查者、测量单位
fig.text(0.05, 0.85, '制 图 人：文贺鹏、邢文骞、沈子程、黄印、张华港', fontsize=12)
fig.text(0.05, 0.82, '技术负责：潘军、蒋立军', fontsize=12)
fig.text(0.05, 0.79, '审 查 者：潘军、蒋立军', fontsize=12)
fig.text(0.05, 0.76, '测量单位：吉林大学地球科学学院地质系2025班', fontsize=12)

# 添加坐标信息
fig.text(0.6, 0.85, '起点坐标: E:21300990 N:4526438 H:3m', fontsize=10)
fig.text(0.6, 0.82, '终点坐标: E:21300883 N:4526482 H:260m', fontsize=10)

# ========== 绘制地质剖面主体 ==========

# 设置剖面图的位置和大小
ax.set_position([0.1, 0.1, 0.8, 0.65])

# 地形点数据 (水平距离, 高程)
topo_points = [
    (0, 3),        # 起点
    (14.94, 1.69),  # 导线0-1结束
    (21.94, 1.57),  # 导线1-2分层①结束
    (34.94, 1.34),  # 导线1-2分层②结束
    (39.94, 1.25),  # 导线1-2结束
    (56.2, 6.22),   # 导线2-3分层③结束
    (63.85, 8.56),  # 导线2-3结束
    (77.95, 13.69), # 导线3-4分层④结束
    (82.65, 15.4),  # 导线3-4结束
    (88.25, 17.55), # 导线4-5分层⑤结束
    (101.32, 22.57),# 导线4-5结束
    (106.88, 24.82),# 导线5-6分层⑥结束
    (119.86, 30.06) # 终点
]

# 提取x和y坐标
x = [p[0] for p in topo_points]
y = [p[1] for p in topo_points]

# 绘制地形线
ax.plot(x, y, 'k-', linewidth=2.5, zorder=10)
ax.plot(x, y, 'ko', markersize=6, zorder=11)

# 添加高程标记
for i, (xi, yi) in enumerate(topo_points):
    if i == 0 or i == len(topo_points)-1:  # 起点和终点
        ax.text(xi, yi-1, f'{yi}m', ha='center', va='top', fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    elif i % 2 == 0:  # 每隔一个点标记高程
        ax.text(xi, yi-0.5, f'{yi:.1f}m', ha='center', va='top', fontsize=9)

# 地层分界点及其岩性
strata = [
    {'start': 0, 'end': 21.94, 'name': '雾迷山组', 'lithology': '含燧石结核燧石条带白云岩', 'color': '#E0E0E0', 'pattern': '...'},
    {'start': 21.94, 'end': 34.94, 'name': '侵入岩', 'lithology': '花岗细晶岩', 'color': '#F8CECC', 'pattern': 'xx'},
    {'start': 34.94, 'end': 56.2, 'name': '昌平组', 'lithology': '土黄色角砾白云质灰岩', 'color': '#FCE5CD', 'pattern': 'ooo'},
    {'start': 56.2, 'end': 77.95, 'name': '馒头组', 'lithology': '紫红色页岩夹土黄色泥岩', 'color': '#F4CCCC', 'pattern': '--'},
    {'start': 77.95, 'end': 88.25, 'name': '毛庄组', 'lithology': '黄绿色砂页岩', 'color': '#D9EAD3', 'pattern': '///'},
    {'start': 88.25, 'end': 106.88, 'name': '徐庄组', 'lithology': '黄绿色泥页岩夹灰岩', 'color': '#D0E0E3', 'pattern': '||'},
    {'start': 106.88, 'end': 119.86, 'name': '张夏组', 'lithology': '深灰色鲕状灰岩', 'color': '#C9DAF8', 'pattern': 'oo'}
]

# 填充地层区域
for layer in strata:
    start_idx = next(i for i, pt in enumerate(topo_points) if pt[0] >= layer['start'])
    end_idx = next(i for i, pt in enumerate(topo_points) if pt[0] >= layer['end'])
    
    # 获取地层边界点
    boundary_x = [pt[0] for pt in topo_points[start_idx:end_idx+1]]
    boundary_y = [pt[1] for pt in topo_points[start_idx:end_idx+1]]
    
    # 创建地层多边形
    polygon = Polygon(
        list(zip(boundary_x, boundary_y)) + 
        [(boundary_x[-1], 0), (boundary_x[0], 0)],
        closed=True, edgecolor='k', linewidth=0.5,
        facecolor=layer['color'], hatch=layer['pattern'], alpha=0.9
    )
    ax.add_patch(polygon)
    
    # 标注地层名称
    mid_x = (layer['start'] + layer['end']) / 2
    mid_y_idx = next(i for i, x_val in enumerate(x) if x_val >= mid_x)
    mid_y = y[mid_y_idx] + 1
    
    ax.text(mid_x, mid_y, layer['name'], ha='center', va='center', 
            fontsize=12, fontweight='bold', 
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# 绘制断层符号
fault_x = 21.94
fault_y = 1.57
fault_angle = 65

# 创建锯齿状断层线
fault_dx = 1.5
fault_dy = fault_dx * np.tan(np.radians(fault_angle))
fault_points = []
for i in range(5):
    fault_points.append((fault_x + i*fault_dx, fault_y + i*fault_dy))
    fault_points.append((fault_x + (i+0.5)*fault_dx, fault_y + (i+0.5)*fault_dy - 0.5))

ax.plot([p[0] for p in fault_points], [p[1] for p in fault_points], 
        'r-', linewidth=2, zorder=12)
ax.text(fault_x+3, fault_y+2, '断层 310°∠65°', color='red', fontsize=11,
        bbox=dict(facecolor='white', alpha=0.8))

# 标注产状
def draw_attitude(ax, x, y, dip_direction, dip_angle, length=4):
    """绘制地层产状符号"""
    # 计算走向线方向 (垂直于倾向)
    strike_angle = (dip_direction + 90) % 360
    
    # 绘制走向线
    strike_dx = length * np.cos(np.radians(strike_angle))
    strike_dy = length * np.sin(np.radians(strike_angle))
    ax.plot([x - strike_dx/2, x + strike_dx/2], 
            [y - strike_dy/2, y + strike_dy/2], 
            'k-', linewidth=1.5)
    
    # 绘制倾向线
    dip_dx = length * 0.7 * np.cos(np.radians(dip_direction))
    dip_dy = length * 0.7 * np.sin(np.radians(dip_direction))
    ax.plot([x, x + dip_dx], [y, y + dip_dy], 
            'k-', linewidth=1.5)
    
    # 添加标注
    ax.text(x + dip_dx*1.2, y + dip_dy*1.2, 
            f'{dip_direction}°∠{dip_angle}°', 
            fontsize=10, ha='center', va='center')

# 在指定位置添加产状
draw_attitude(ax, 11, 1.69, 10, 20)  # 雾迷山组产状
draw_attitude(ax, 70, 10, 0, 17)     # 馒头组产状

# 标记标本点
specimens = [
    (13.3, 1.69, 'BMZ-05-01'),
    (15, 1.57, 'BMZ-05-02'),
    (21, 1.34, 'BMZ-05-03'),
    (21, 8.56, 'BMZ-05-04'),
    (17, 15.4, 'BMZ-05-05'),
    (11, 22.57, 'BMZ-05-06'),
    (20, 30.06, 'BMZ-05-07')
]

for x, y, label in specimens:
    ax.plot(x, y, 'g*', markersize=15, zorder=20)
    ax.text(x + 1.5, y + 0.5, label, fontsize=10, 
            bbox=dict(facecolor='white', alpha=0.8))

# 添加水平距离标记
ax.set_xlim(-5, 130)
ax.set_ylim(0, 35)
for dist in range(0, 130, 20):
    ax.plot([dist, dist], [0, 0.5], 'k-', linewidth=1)
    ax.text(dist, -0.7, f'{dist}m', ha='center', va='top', fontsize=9)

# 添加图例
legend_elements = [
    plt.Line2D([0], [0], color='red', lw=2, label='断层'),
    plt.Line2D([0], [0], marker='*', color='g', label='标本点', markersize=12, linestyle='None'),
    plt.Rectangle((0,0), 1, 1, fc='#E0E0E0', hatch='...', edgecolor='k', label='白云岩 (雾迷山组)'),
    plt.Rectangle((0,0), 1, 1, fc='#F8CECC', hatch='xx', edgecolor='k', label='花岗细晶岩 (侵入岩)'),
    plt.Rectangle((0,0), 1, 1, fc='#FCE5CD', hatch='ooo', edgecolor='k', label='角砾灰岩 (昌平组)'),
    plt.Rectangle((0,0), 1, 1, fc='#F4CCCC', hatch='--', edgecolor='k', label='页岩 (馒头组)'),
    plt.Rectangle((0,0), 1, 1, fc='#D9EAD3', hatch='///', edgecolor='k', label='砂页岩 (毛庄组)'),
    plt.Rectangle((0,0), 1, 1, fc='#D0E0E3', hatch='||', edgecolor='k', label='泥页岩 (徐庄组)'),
    plt.Rectangle((0,0), 1, 1, fc='#C9DAF8', hatch='oo', edgecolor='k', label='鲕状灰岩 (张夏组)')
]

ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.15), 
          ncol=3, fontsize=10, framealpha=0.8)

# 添加比例尺
def add_scale_bar(ax, length=50, units='m', position=(0.1, 0.05)):
    """添加比例尺"""
    x, y = position
    # 绘制比例尺主体
    ax.plot([x, x+length], [y, y], 'k-', linewidth=2)
    ax.plot([x, x], [y-0.2, y+0.2], 'k-', linewidth=1)
    ax.plot([x+length, x+length], [y-0.2, y+0.2], 'k-', linewidth=1)
    
    # 添加标注
    ax.text(x + length/2, y - 0.5, f'{length} {units}', 
            ha='center', va='top', fontsize=10)

add_scale_bar(ax, length=50, position=(10, 1))

# 添加指北针
def add_north_arrow(ax, x=110, y=25, size=3):
    """添加指北针"""
    # 绘制箭头
    ax.arrow(x, y, 0, size, head_width=size*0.7, head_length=size*0.7, 
             fc='k', ec='k', linewidth=1.5)
    # 添加标注
    ax.text(x, y+size+0.5, 'N', ha='center', va='bottom', fontsize=12, fontweight='bold')

add_north_arrow(ax)

# 添加图框
fig.patches.append(Rectangle((0.05, 0.05), 0.9, 0.9, 
                             transform=fig.transFigure, 
                             fill=False, edgecolor='black', linewidth=1.5))

# 保存和显示
plt.savefig('白庙子早古生界地层实测剖面图.png', dpi=300, bbox_inches='tight')
plt.show()