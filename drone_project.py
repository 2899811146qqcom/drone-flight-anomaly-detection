import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- 1. 生成模拟无人机飞行数据 ----------------------
np.random.seed(42)  # 固定随机种子，保证结果可复现
time = np.arange(0, 100, 0.1)  # 时间序列：0~100秒，步长0.1

# 正常飞行高度（缓慢变化 + 小噪声）
height = 100 + 5 * np.sin(time * 0.1) + np.random.normal(0, 0.5, len(time))
# 正常飞行速度（平稳 + 小噪声）
speed = 20 + 2 * np.cos(time * 0.15) + np.random.normal(0, 0.3, len(time))

# ---------------------- 2. 注入异常（模拟故障） ----------------------
# 异常1：第30~35秒，高度骤降
height[300:350] = height[300:350] - 10
# 异常2：第60~65秒，速度突变
speed[600:650] = speed[600:650] + 8

# 整理成DataFrame
df = pd.DataFrame({
    'time': time,
    'height': height,
    'speed': speed
})

# ---------------------- 3. 异常检测逻辑 ----------------------
# 高度异常：高度低于95（正常最低约95）
df['height_anomaly'] = df['height'] < 95
# 速度异常：速度高于25（正常最高约25）
df['speed_anomaly'] = df['speed'] > 25
# 总异常标记
df['is_anomaly'] = df['height_anomaly'] | df['speed_anomaly']

# ---------------------- 4. 可视化结果 ----------------------
plt.figure(figsize=(12, 6))

# 绘制高度曲线
plt.subplot(2, 1, 1)
plt.plot(df['time'], df['height'], label='Height (m)', color='blue')
plt.scatter(df[df['height_anomaly']]['time'], 
            df[df['height_anomaly']]['height'], 
            color='red', label='Height Anomaly')
plt.title('Drone Flight Height & Anomalies')
plt.ylabel('Height (m)')
plt.legend()

# 绘制速度曲线
plt.subplot(2, 1, 2)
plt.plot(df['time'], df['speed'], label='Speed (m/s)', color='green')
plt.scatter(df[df['speed_anomaly']]['time'], 
            df[df['speed_anomaly']]['speed'], 
            color='red', label='Speed Anomaly')
plt.title('Drone Flight Speed & Anomalies')
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.legend()

plt.tight_layout()
plt.show()

# ---------------------- 5. 输出异常点统计 ----------------------
print("=== 异常检测结果 ===")
print(f"总数据点数：{len(df)}")
print(f"高度异常点数：{df['height_anomaly'].sum()}")
print(f"速度异常点数：{df['speed_anomaly'].sum()}")
print(f"总异常点数：{df['is_anomaly'].sum()}")
