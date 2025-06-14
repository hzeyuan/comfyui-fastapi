"""
ComfyUI 业务逻辑服务
"""
import json
import urllib.request
from typing import Dict, Any
from loguru import logger
from config.settings import comfyui_url


class ComfyUIService:
    """ComfyUI服务类"""
    
    def __init__(self):
        self.server_address = self._get_server_address()
    
    def _get_server_address(self) -> str:
        """获取ComfyUI服务器地址"""
        if comfyui_url.startswith('http://'):
            return comfyui_url[7:]  # 移除 'http://'
        return comfyui_url
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取ComfyUI队列状态"""
        try:
            url = f"http://{self.server_address}/queue"
            logger.debug(f"获取队列状态: {url}")

            response = urllib.request.urlopen(url)
            queue_data = json.loads(response.read())
            
            # 解析队列信息
            queue_running = queue_data.get("queue_running", [])
            queue_pending = queue_data.get("queue_pending", [])
            
            running_count = len(queue_running)
            pending_count = len(queue_pending)
            total_count = running_count + pending_count
            
            logger.info(f"队列状态 - 正在执行: {running_count}, 等待中: {pending_count}, 总计: {total_count}")
            
            return {
                "running": running_count,
                "pending": pending_count,
                "total": total_count,
                "queue_running": queue_running,
                "queue_pending": queue_pending
            }
        except Exception as e:
            logger.error(f"获取队列状态失败: {str(e)}")
            raise
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取ComfyUI系统统计信息"""
        try:
            url = f"http://{self.server_address}/system_stats"
            logger.debug(f"获取系统统计: {url}")

            response = urllib.request.urlopen(url)
            stats_data = json.loads(response.read())
            
            logger.info("系统统计信息获取成功")
            return stats_data
        except Exception as e:
            logger.error(f"获取系统统计失败: {str(e)}")
            raise
    
    def get_server_info(self) -> Dict[str, Any]:
        """获取ComfyUI服务器信息"""
        try:
            url = f"http://{self.server_address}/"
            logger.debug(f"获取服务器信息: {url}")

            response = urllib.request.urlopen(url)
            # ComfyUI根路径通常返回HTML，我们只检查连接状态

            logger.info("ComfyUI服务器连接正常")
            return {
                "server_address": self.server_address,
                "status": "connected",
                "url": comfyui_url
            }
        except Exception as e:
            logger.error(f"获取服务器信息失败: {str(e)}")
            raise

    def interrupt_current_task(self) -> Dict[str, Any]:
        """中断当前正在执行的任务"""
        try:
            url = f"http://{self.server_address}/interrupt"
            logger.debug(f"中断当前任务: {url}")

            req = urllib.request.Request(url, method='POST')
            response = urllib.request.urlopen(req)

            # 有些ComfyUI版本可能返回空响应
            try:
                result = json.loads(response.read())
            except:
                result = {"status": "interrupted"}

            logger.info("当前任务中断成功")
            return result
        except Exception as e:
            logger.error(f"中断当前任务失败: {str(e)}")
            raise

    def get_queue_history(self, max_items: int = 100) -> Dict[str, Any]:
        """获取队列历史记录"""
        try:
            url = f"http://{self.server_address}/history"
            if max_items:
                url += f"?max_items={max_items}"
            logger.debug(f"获取队列历史: {url}")

            response = urllib.request.urlopen(url)
            history_data = json.loads(response.read())

            logger.info(f"队列历史获取成功，共 {len(history_data)} 条记录")
            return history_data
        except Exception as e:
            logger.error(f"获取队列历史失败: {str(e)}")
            raise


# 创建全局服务实例
comfyui_service = ComfyUIService()
