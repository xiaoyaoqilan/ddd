import csv
import time
import webbrowser
import os
import sys
import pyautogui
from datetime import datetime
import platform
import random
import pandas as pd

def open_twitter_profiles(file_path, max_users=5, auto_click=False, click_delay=5):
    """
    从CSV文件读取用户名并使用本地浏览器打开用户主页
    
    参数:
    csv_file_path: CSV文件路径
    max_users: 要处理的最大用户数量，默认为5
    auto_click: 是否启用自动点击功能，默认为False
    click_delay: 打开页面后等待的秒数，默认为5秒
    """
    print(f"🔍 开始读取文件: {file_path}")
    
    # 验证文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 错误: 文件不存在 - {file_path}")
        return
    
    # 读取CSV或XLSX文件中的用户名
    users = []
    
    try:
        # 检查文件扩展名
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.xlsx' or file_extension == '.xls':
            print(f"📊 正在读取Excel文件({file_extension})...")
            try:
                # 使用pandas读取Excel文件，指定引擎为openpyxl以确保兼容性
                df = pd.read_excel(file_path, engine='openpyxl')
                print(f"✅ 使用openpyxl引擎成功读取文件")
            except Exception as e1:
                print(f"⚠️ openpyxl引擎读取失败: {str(e1)}")
                try:
                    # 然后尝试xlrd引擎(适用于.xls和一些.xlsx)
                    df = pd.read_excel(file_path, engine='xlrd')
                    print("✅ 使用xlrd引擎成功读取文件")
                except Exception as e2:
                    print(f"⚠️ xlrd引擎读取失败: {str(e2)}")
                    # 最后尝试不指定引擎，让pandas自动选择
                    df = pd.read_excel(file_path)
                    print("✅ 使用默认引擎成功读取文件")
            print(f"📋 Excel文件表头: {list(df.columns)}")
            print(f"📍 用户名所在列: 第2列 - '{df.columns[1]}'")
            
            for row_idx, row in df.iterrows():
                if len(df.columns) >= 2:
                    username = str(row.iloc[1])  # 从第二列获取用户名
                    if username and username.strip() and username.lower() != 'nan':
                        if username.startswith('"'):
                            username = username.strip('"')  # 处理双引号
                        users.append(username)
                        if row_idx < 5:  # 显示前5个用户名作为示例
                            print(f"📝 读取到用户名 (第{row_idx+2}行): @{username}")
        else:
            # 默认使用CSV读取方式
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)  # 使用普通reader简化读取
                header = next(reader)  # 跳过表头
                print(f"📋 CSV文件表头: {header}")
                print(f"📍 用户名所在列: 第2列 - '{header[1]}'")
                
                for row_idx, row in enumerate(reader, 2):  # 从第2行开始计数
                    if len(row) >= 2:
                        username = row[1]  # 从第二列获取用户名
                        if username and username.startswith('"'):
                            username = username.strip('"')  # 处理双引号
                        if username:  # 确保用户名不为空
                            users.append(username)
                            if row_idx <= 5:  # 显示前5个用户名作为示例
                                print(f"📝 读取到用户名 (第{row_idx}行): @{username}")
        
        print(f"✅ 成功读取了 {len(users)} 个用户名")
        
        # 限制处理的用户数量为前80个（跳过第一个用户）
        max_users_to_process = 80
        # 跳过第一个用户，然后处理接下来的80个
        if len(users) > 1:
            users_to_process = users[1:max_users_to_process+1]  # 从第二个用户开始，取80个
            actual_max = len(users_to_process)  # 保持变量名一致
            print(f"📋 跳过第一个用户，将处理接下来的{actual_max}个用户名（最多80个）")
        else:
            users_to_process = []
            actual_max = 0
            print("⚠️  CSV文件中用户数量不足，无法处理")
        
        # 显示操作模式信息
        mode_text = "自动点击模式" if auto_click else "手动操作模式"
        print(f"\n🚀 正在使用默认浏览器打开用户主页...")
        print(f"🔧 运行模式: {mode_text}")
        print(f"⚠️  重要提示：请确保您已登录X(Twitter)账户")
        print(f"💡 提示: {'系统将自动模拟点击关注按钮' if auto_click else '需要手动点击关注按钮'}")
        print(f"💻 注意: {'请不要移动鼠标，等待自动点击完成' if auto_click else '请在打开的页面中手动点击关注'}")
        print("=" * 60)
        
        success_count = 0
        error_count = 0
        
        # 打开每个用户的主页
        for i, username in enumerate(users_to_process, 1):
            try:
                # 构建Twitter搜索URL，而不是直接打开用户主页
                search_url = f"https://x.com/search?q={username}&src=typed_query"
                print(f"[{i}/{actual_max}] 正在搜索用户: @{username}")
                
                # 使用默认浏览器打开搜索URL
                webbrowser.open(search_url)
                print(f"[{i}/{actual_max}] ✅ 已打开搜索页面: {search_url}")
                
                # 如果启用了自动点击功能
                if auto_click:
                    try:
                        # 生成8-14秒之间的随机延迟
                        random_delay = random.uniform(8, 14)
                        print(f"[{i}/{actual_max}] ⏳ 等待页面加载 ({random_delay:.1f}秒)...")
                        time.sleep(random_delay)
                        
                        # 查找并点击关注按钮
                        # 这里使用位置参数（可以根据实际情况调整）
                        # 注意：这个位置可能需要用户根据自己的屏幕分辨率调整
                        print(f"[{i}/{actual_max}] 🖱️  正在模拟鼠标点击...")
                        
                        # 获取当前鼠标位置
                        current_x, current_y = pyautogui.position()
                        print(f"[{i}/{actual_max}] ℹ️  当前鼠标位置: X={current_x}, Y={current_y}")
                        
                        # 根据用户提供的HTML元素信息，优化关注按钮位置
                        # <div class="css-175oi2r r-6gpygo" style="min-width: 81px;">
                        #   <button aria-label="Follow @LarissaGreen30" role="button" 
                        #           class="css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l" 
                        #           data-testid="1977369577840676864-follow" type="button">
                        #     <div dir="ltr" class="css-146c3p1 r-bcqeeo r-qvutc0 r-37j5jr r-q4m81j r-a023e6 r-rjixqe r-b88u0q r-1awozwy r-6koalj r-18u37iz r-16y2uox r-1777fci">
                        #       <span class="css-1jxf684 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-a023e6 r-rjixqe">
                        #         <span class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3">Follow</span>
                        #       </span>
                        #     </div>
                        #   </button>
                        # </div>
                        
                        # 获取屏幕信息
                        screen_width, screen_height = pyautogui.size()
                        print(f"[{i}/{actual_max}] 📱 屏幕分辨率: {screen_width}x{screen_height}")
                        
                        # 使用用户指定的固定点击位置
                        target_x = 1120 # 指定的X轴位置
                        target_y = 270  # 指定的Y轴位置
                        click_positions = []
                        
                        # 只使用一个固定位置，不再尝试多个位置
                        click_positions = [(target_x, target_y)]
                        
                        print(f"[{i}/{actual_max}] 🎯 使用固定点击位置: X={target_x}, Y={target_y}")
                        
                        # 强化鼠标移动然后点击的模式
                        click_success = False
                        
                        # 为每个目标位置创建移动-点击序列
                        for pos_idx, (target_x, target_y) in enumerate(click_positions, 1):
                            print(f"[{i}/{actual_max}] 🎯 尝试点击位置 {pos_idx}: X={target_x}, Y={target_y}")
                            
                            # 1. 添加中间移动点，使移动路径更自然
                            mid_x = target_x + random.randint(-30, 30)
                            mid_y = current_y + random.randint(-20, 20)
                            print(f"[{i}/{actual_max}] 🖱️  准备移动到目标位置，设置中间点: X={mid_x}, Y={mid_y}")
                            
                            # 2. 第一步移动：从当前位置到中间点
                            first_move_duration = random.uniform(0.3, 0.7)
                            pyautogui.moveTo(mid_x, mid_y, duration=first_move_duration, tween=pyautogui.easeOutQuad)
                            print(f"[{i}/{actual_max}] 🖱️  第一步移动完成：已到达中间点")
                            time.sleep(random.uniform(0.1, 0.3))  # 短暂停顿
                            
                            # 3. 第二步移动：从中间点到目标位置（移动然后点击模式的核心部分）
                            second_move_duration = random.uniform(0.2, 0.4)
                            pyautogui.moveTo(target_x, target_y, duration=second_move_duration, tween=pyautogui.easeInOutQuad)
                            print(f"[{i}/{actual_max}] 🖱️  第二步移动完成：已到达目标位置")
                            
                            # 4. 微小调整 - 模拟最终对准
                            if random.random() > 0.5:
                                fine_adjustment_x = random.uniform(-2, 2)
                                fine_adjustment_y = random.uniform(-2, 2)
                                pyautogui.moveRel(fine_adjustment_x, fine_adjustment_y, duration=0.1)
                                print(f"[{i}/{actual_max}] 🖱️  进行微小调整以精确对准")
                            
                            # 5. 点击前短暂停顿
                            click_pause = random.uniform(0.1, 0.5)
                            time.sleep(click_pause)
                            print(f"[{i}/{actual_max}] 👁️  对准目标，准备点击")
                            
                            # 6. 执行点击操作
                            # 按照要求，只执行单次点击
                            pyautogui.click()
                            print(f"[{i}/{actual_max}] ✅ 执行单次点击")
                            
                            # 7. 点击后可能的微小移动
                            if random.random() > 0.6:
                                post_click_move = random.uniform(-3, 3)
                                pyautogui.moveRel(post_click_move, post_click_move, duration=0.05)
                                print(f"[{i}/{actual_max}] 🖱️  点击后自然微小移动")
                            
                            # 点击后反应时间
                            post_click_pause = 0.5  # 固定的短时间等待
                            time.sleep(post_click_pause)
                            print(f"[{i}/{actual_max}] 🕐 点击后观察结果")
                            
                            # 自动关闭标签页
                            print(f"[{i}/{actual_max}] 🚪 正在关闭当前标签页...")
                            # 使用快捷键Ctrl+W (Windows/Linux)或Command+W (Mac)关闭标签页
                            if platform.system() == 'Darwin':  # Mac系统
                                pyautogui.hotkey('command', 'w')
                            else:  # Windows/Linux系统
                                pyautogui.hotkey('ctrl', 'w')
                            time.sleep(1)  # 等待标签页关闭
                            
                            # 标记为已尝试点击
                            click_success = True
                            
                            # 由于只点击一次，不需要额外的位置尝试
                            
                        # 人类风格的鼠标恢复 - 自然移动回原位
                        print(f"[{i}/{actual_max}] 🔄 自然移动回原始位置")
                        # 可能先向其他方向移动一点，再回到原位，模拟人类操作
                        if random.random() > 0.6:  # 60%概率有额外移动
                            detour_x = current_x + random.randint(-20, 20)
                            detour_y = current_y + random.randint(-20, 20)
                            pyautogui.moveTo(detour_x, detour_y, duration=random.uniform(0.2, 0.4))
                            time.sleep(random.uniform(0.1, 0.3))
                        pyautogui.moveTo(current_x, current_y, duration=random.uniform(0.3, 0.6))
                        
                        # 增加成功计数
                        if click_success:
                            success_count += 1
                            print(f"[{i}/{actual_max}] ✅ 自动点击操作完成")
                        else:
                            error_count += 1
                            print(f"[{i}/{actual_max}] ❌ 未找到合适的点击位置")
                        
                        # 人类风格的间隔时间 - 不规律的等待
                        next_user_delay = random.uniform(2.5, 4.0)
                        print(f"[{i}/{actual_max}] ⏱️  等待 {next_user_delay:.1f} 秒后处理下一个用户...")
                        time.sleep(next_user_delay)
                        
                    except Exception as click_error:
                        error_count += 1
                        print(f"[{i}/{actual_max}] ❌ 自动点击失败: {str(click_error)}")
                else:
                    # 手动模式
                    success_count += 1
                    time.sleep(2)  # 等待一段时间，避免过快打开多个标签页
                    print(f"[{i}/{actual_max}] ⏳ 请手动点击关注按钮")
                    # 提示关注按钮的位置信息
                    print(f"[{i}/{actual_max}] 💡 关注按钮通常位于页面右侧用户信息区域，按钮文本为'Follow'")
                
            except Exception as e:
                error_count += 1
                print(f"[{i}/{actual_max}] ❌ 打开失败: {username}, 错误: {str(e)}")
                time.sleep(1)  # 出错后也稍微等待一下
        
        print("=" * 60)
        print(f"\n📊 操作完成:")
        print(f"   - 成功打开: {success_count} 个用户主页")
        print(f"   - 打开失败: {error_count} 个用户主页")
        if auto_click:
            print("\n💡 提示: 自动点击功能已完成。请注意，自动点击的准确率取决于屏幕分辨率和页面布局")
            print("   如果自动点击未成功，请手动点击'Follow'按钮")
        else:
            print("\n💡 提示: 请在浏览器中手动点击'Follow'按钮关注这些用户")
            
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 - {file_path}")
    except PermissionError:
        print(f"❌ 错误: 无权限访问文件 - {file_path}")
    except UnicodeDecodeError:
        print(f"❌ 错误: 文件编码错误，请确保文件使用UTF-8编码")
    except Exception as e:
        print(f"❌ 发生未知错误: {str(e)}")


def print_usage():
    """显示程序使用说明"""
    print("用法: python ts_2.py [最大用户数] [是否自动点击(0/1)] [点击延迟秒数]")
    print()
    print("参数说明:")
    print("  最大用户数      - 可选，要处理的最大用户数量，默认为5")
    print("  是否自动点击    - 可选，0表示手动点击，1表示自动点击，默认为1")
    print("  点击延迟秒数    - 可选，自动点击模式下等待页面加载的秒数，默认为5")
    print()
    print("示例:")
    print("  python ts_2.py           # 默认使用固定位置X=1120, Y=280自动点击，等待10秒")
    print("  python ts_2.py 10        # 处理10个用户，启用自动点击")
    print("  python ts_2.py 5 0       # 处理5个用户，禁用自动点击")
    print("  python ts_2.py 3 1 7     # 处理3个用户，启用自动点击，等待7秒")

if __name__ == "__main__":
    # 打印欢迎信息
    print("""
    ====================================================
             Twitter 用户主页批量打开工具
    ====================================================
    此工具使用您的本地默认浏览器打开Twitter用户主页
    从CSV文件读取用户名并支持自动/手动关注功能
    """)
    
    # 默认配置 - 支持CSV或XLSX文件
    default_file_path = "x自动关注用户.xlsx"  # 默认使用当前目录下的xlsx文件
    max_users = 5  # 这个值现在被硬编码为80，但保留参数以兼容命令行
    auto_click = True  # 默认启用自动点击功能
    click_delay = 10  # 增加默认延迟到10秒
    
    # 处理命令行参数
    if len(sys.argv) > 1:
        # 用户提供了文件路径
        file_path = sys.argv[1]
        # 如果用户提供了最大用户数
        if len(sys.argv) > 2:
            try:
                max_users = int(sys.argv[2])
                if max_users <= 0:
                    print("⚠️  警告: 最大用户数必须大于0，将使用默认值5")
                    max_users = 5
            except ValueError:
                print("⚠️  警告: 无效的最大用户数，将使用默认值5")
        # 如果用户指定了是否自动点击
        if len(sys.argv) > 3:
            try:
                auto_click_flag = int(sys.argv[3])
                auto_click = bool(auto_click_flag)
            except ValueError:
                print("⚠️  警告: 无效的自动点击参数，将使用默认值(True)")
        # 如果用户指定了点击延迟
        if len(sys.argv) > 4:
            try:
                click_delay = int(sys.argv[4])
                if click_delay <= 0:
                    print("⚠️  警告: 点击延迟必须大于0，将使用默认值10秒")
                    click_delay = 10
            except ValueError:
                print("⚠️  警告: 无效的点击延迟参数，将使用默认值10秒")
        print(f"📄 使用用户指定的文件: {file_path}")
    else:
        # 使用默认文件路径
        file_path = default_file_path
        print(f"📄 将使用默认文件: {file_path}")
        print("💡 提示: 程序默认启用自动点击功能(固定位置X=1120, Y=280)")
        print("  自动点击前等待10秒以确保页面加载完成")
        print("  点击后将自动关闭标签页")
        print("  您可以在命令行中指定参数，例如: python x自动关注.py 文件名.xlsx 10 1 15")
        print("  要禁用自动点击，请设置第三个参数为0: python x自动关注.py 文件名.xlsx 10 0")
    
    # 显示配置信息
    print(f"⚙️  配置:")
    print(f"   - 文件路径: '{file_path}'")
    print(f"   - 最大用户数: {max_users}")
    print(f"   - 自动点击: {'✅ 已启用' if auto_click else '❌ 已禁用'}")
    print(f"   - 点击延迟: {click_delay}秒")
    print(f"   - 操作后自动关闭标签页: ✅ 已启用")
    print()
    
    # 如果自动点击，显示额外的警告
    if auto_click:
        print("⚠️  人类模拟自动点击功能启用:")
        print("   - 此功能模拟人类自然的鼠标点击行为")
        print(f"   - 使用固定点击位置: X={1120}, Y={280}")
        print(f"   - 自动点击前等待{click_delay}秒以确保页面加载完成")
        print(f"   - 当前系统: {platform.system()} {platform.release()}")
        print("   - 使用过程中请不要移动鼠标，以免干扰模拟操作")
        print("   - 程序模拟人类操作习惯：随机位置偏移、自然移动轨迹")
        print("   - 执行单次点击，模拟人类操作特点")
        print("   - 如有需要，请调整代码中的target_x和target_y值")
        print()
    
    # 执行打开操作
    open_twitter_profiles(file_path, max_users, auto_click, click_delay)
    print("\n✅ 程序执行完成！")
   