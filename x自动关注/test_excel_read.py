import pandas as pd
import os

# 测试Excel文件读取
def test_excel_reading(file_path):
    print(f"尝试读取文件: {file_path}")
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    
    try:
        # 尝试使用不同引擎
        print("尝试使用openpyxl引擎...")
        df = pd.read_excel(file_path, engine='openpyxl')
        print("成功！文件内容:")
        print(df.head())
        return True
    except Exception as e:
        print(f"openpyxl引擎错误: {str(e)}")
    
    try:
        print("尝试使用xlrd引擎...")
        df = pd.read_excel(file_path, engine='xlrd')
        print("成功！文件内容:")
        print(df.head())
        return True
    except Exception as e:
        print(f"xlrd引擎错误: {str(e)}")
    
    return False

# 测试当前文件
test_excel_reading('x自动关注用户.xlsx')