"""
Models package.
自动导入所有模型文件，无需手动维护。
"""

import importlib
import pkgutil
from pathlib import Path

# 自动导入当前包下的所有模块
__all__ = []

# 获取当前包的路径
package_dir = Path(__file__).parent

# 遍历所有 .py 文件（排除 __init__.py）
for module_info in pkgutil.iter_modules([str(package_dir)]):
    module_name = module_info.name

    # 跳过私有模块和 __init__
    if module_name.startswith("_"):
        continue

    # 动态导入模块
    module = importlib.import_module(f".{module_name}", package=__name__)

    # 获取模块中所有的类
    for attr_name in dir(module):
        attr = getattr(module, attr_name)

        # 检查是否是类，并且是 SQLAlchemy 模型（有 __tablename__ 属性）
        if (
            isinstance(attr, type)
            and hasattr(attr, "__tablename__")
            and not attr_name.startswith("_")
        ):
            # 将类添加到当前命名空间
            globals()[attr_name] = attr
            __all__.append(attr_name)

# 打印已加载的模型（仅在开发时有用）
if __name__ == "__main__":
    print(f"✅ 自动加载了 {len(__all__)} 个模型:")
    for model_name in sorted(__all__):
        print(f"  - {model_name}")
