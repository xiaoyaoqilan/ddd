#!/usr/bin/env python3
"""
wxauto库简易使用示例
功能：登录微信、发送消息、获取联系人列表
"""

from wxauto import WeChat
import time

class WeChatAutoDemo:
    def __init__(self):
        """初始化微信自动化对象"""
        try:
            self.wx = WeChat()
            print("微信自动化工具初始化完成")
            # 尝试获取登录用户信息
            self.user_info = self._get_user_info()
            if self.user_info:
                print(f"已登录用户: {self.user_info}")
        except Exception as e:
            print(f"初始化失败: {e}")
            print("请确保微信已打开并登录")
            self.wx = None
        
    def _get_user_info(self):
        """获取用户信息"""
        try:
            # 尝试不同的方法获取用户信息
            # 方法1: 尝试获取当前登录用户昵称
            nickname = self.wx.NickName
            if nickname:
                return nickname
            
            # 方法2: 尝试通过窗口标题获取信息
            window_title = self.wx.WindowTitle
            if window_title and "微信" in window_title:
                # 提取微信昵称（通常窗口标题格式为"微信 - 昵称"）
                if " - " in window_title:
                    return window_title.split(" - ")[-1]
                return window_title
            
            # 如果以上方法都失败，返回默认信息
            return "未知用户"
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            return None
        
    def is_logged_in(self):
        """检查是否已登录"""
        return self.wx is not None and self.user_info is not None
        
    def send_message(self, contact_name, message):
        """发送消息给指定联系人"""
        if not self.is_logged_in():
            print("未登录，无法发送消息")
            return False
            
        try:
            # 搜索联系人
            self.wx.Search(contact_name)
            # 发送消息
            self.wx.SendMsg(message)
            print(f"消息已发送给 {contact_name}: {message}")
            return True
        except Exception as e:
            print(f"发送消息失败: {e}")
            return False
        
    def get_contacts(self, count=10):
        """获取联系人列表"""
        if not self.is_logged_in():
            print("未登录，无法获取联系人列表")
            return []
            
        try:
            # 获取联系人列表
            contacts = self.wx.GetContactList()
            print(f"找到 {len(contacts)} 个联系人，显示前 {count} 个:")
            
            # 显示前count个联系人
            for i, contact in enumerate(contacts[:count]):
                print(f"{i+1}. {contact['NickName']} ({contact.get('RemarkName', '')})")
            
            return contacts
        except Exception as e:
            print(f"获取联系人列表失败: {e}")
            return []
        
    def send_file(self, contact_name, file_path):
        """发送文件给指定联系人"""
        if not self.is_logged_in():
            print("未登录，无法发送文件")
            return False
            
        try:
            # 搜索联系人
            self.wx.Search(contact_name)
            # 发送文件
            self.wx.SendFiles(file_path)
            print(f"文件已发送给 {contact_name}: {file_path}")
            return True
        except Exception as e:
            print(f"发送文件失败: {e}")
            return False
        
if __name__ == "__main__":
    # 创建微信自动化示例
    demo = WeChatAutoDemo()
    
    # 检查登录状态
    if demo.is_logged_in():
        # 获取联系人列表
        demo.get_contacts()
        
        # 发送消息（将'联系人名称'替换为实际联系人）
        # demo.send_message('联系人名称', '你好，这是一条来自wxauto的测试消息')
        
        # 发送文件（将'联系人名称'和'文件路径'替换为实际值）
        # demo.send_file('联系人名称', 'e:\\path\\to\\file.txt')
        
        print("微信自动化演示完成")
    else:
        print("登录失败，无法继续演示")