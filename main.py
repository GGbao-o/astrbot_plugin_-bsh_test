from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("🔧 HelloWorld 插件开始初始化...")
        # 这里可以初始化数据库连接、加载配置等
        self.counter = 100  # 设置初始值
        logger.info(f"✅ HelloWorld 插件初始化完成！计数器初始值: {self.counter}")

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        logger.info("测试--------------------------------------------------------------------");
        """这是一个 hello world 指令"""  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        self.counter += 1  # 每次调用计数器+1
        # user_name = event.get_sender_name()  这个第一次部署时候 拿不到这个 user_name
        # 从消息链中获取用户信息
        message_chain = event.get_messages()
        logger.info(f"完整消息链: {message_chain}")
        # 尝试从消息链中提取发送者
        user_info = "未知用户"
        for msg in message_chain:
            logger.info(f"消息组件类型: {type(msg)}, 内容: {msg}")
            # 如果有 sender 属性
            if hasattr(msg, 'sender'):
                user_info = f"发送者: {msg.sender}"
                break
            # 如果有 user 属性
            elif hasattr(msg, 'user'):
                user_info = f"用户: {msg.user}"
                break

        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_chain = (
            event.get_messages()
        )  # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        logger.info(f"触发hello world指令! 当前计数: {self.counter}")
        yield event.plain_result(
            f"Hello, 用户信息：{user_info}, 你发了 {message_str},你是第 {self.counter} 次调用!"
        )  # 发送一条纯文本消息

    @filter.command("test")
    async def test_command(self, event: AstrMessageEvent):
        """测试命令"""
        yield event.plain_result(f"测试成功！当前计数器: {self.counter}")

    async def terminate(self):
        """插件销毁方法 - 类似 Java 的 @PreDestroy"""
        logger.info("🗑️ HelloWorld 插件开始清理...")
        # 这里可以关闭数据库连接、释放资源等
        logger.info(f"✅ HelloWorld 插件已清理！最终计数器: {self.counter}")
