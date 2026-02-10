# Alembic 数据库迁移工作流程 - 完全自动化版本

## 🎉 完全自动化！无需手动维护导入

本项目已实现**完全自动化的模型检测**，你只需要创建模型文件，其他的都会自动完成！

## ✨ 添加新模型的步骤

### 只需 1 步！创建模型文件

在 `app/models/` 目录下创建新的模型文件，例如 `article.py`：

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base import Base


class Article(Base):
    """文章模型"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="文章标题")
    content = Column(Text, nullable=False, comment="文章内容")
    author = Column(String(50), nullable=False, comment="作者")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        comment="更新时间"
    )
```

**就这样！** 不需要：
- ❌ 修改 `alembic/env.py`
- ❌ 修改 `app/models/__init__.py`
- ❌ 手动导入任何东西

模型会被**自动检测和导入**！

## 🔄 生成和应用迁移

### 生成迁移文件
```bash
uv run alembic revision --autogenerate -m "add articles table"
```

### 应用迁移
```bash
uv run alembic upgrade head
```

## 🛠️ 常用命令

### 查看状态
```bash
# 查看当前版本
uv run alembic current

# 查看迁移历史
uv run alembic history

# 检查数据库状态（是否与模型同步）
uv run alembic check

# 查看数据库详细信息
uv run python scripts/check_migration.py
```

### 迁移管理
```bash
# 应用所有待执行的迁移
uv run alembic upgrade head

# 回滚一个版本
uv run alembic downgrade -1

# 回滚到指定版本
uv run alembic downgrade <revision_id>

# 查看 SQL（不实际执行）
uv run alembic upgrade head --sql
```

## 🔧 自动化原理

### 工作机制

1. **自动发现模型**
   - `app/models/__init__.py` 使用 Python 的 `importlib` 和 `pkgutil`
   - 自动扫描 `app/models/` 目录下的所有 `.py` 文件
   - 检测包含 `__tablename__` 属性的类（SQLAlchemy 模型）
   - 自动导入到命名空间

2. **Alembic 集成**
   - `alembic/env.py` 使用 `from app.models import *`
   - 自动获取所有已注册的模型
   - 通过 `Base.metadata` 检测表结构变化

### 代码实现

```python
# app/models/__init__.py (自动化实现)
import importlib
import pkgutil
from pathlib import Path

__all__ = []
package_dir = Path(__file__).parent

# 遍历所有模块文件
for module_info in pkgutil.iter_modules([str(package_dir)]):
    module_name = module_info.name
    
    if module_name.startswith('_'):
        continue
    
    # 动态导入模块
    module = importlib.import_module(f'.{module_name}', package=__name__)
    
    # 查找 SQLAlchemy 模型类
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        
        if (isinstance(attr, type) and 
            hasattr(attr, '__tablename__') and 
            not attr_name.startswith('_')):
            
            globals()[attr_name] = attr
            __all__.append(attr_name)
```

## 📋 完整示例

### 1. 创建新模型

创建文件 `app/models/product.py`：

```python
from sqlalchemy import Column, Integer, String, Numeric, Boolean
from app.db.base import Base


class Product(Base):
    """商品模型"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="商品名称")
    price = Column(Numeric(10, 2), nullable=False, comment="价格")
    stock = Column(Integer, default=0, comment="库存")
    is_active = Column(Boolean, default=True, comment="是否上架")
```

### 2. 验证自动导入

```bash
# 验证模型已被自动检测
uv run python -c "from app.models import Product; print('✅ Product 模型已自动导入')"
```

### 3. 生成迁移

```bash
uv run alembic revision --autogenerate -m "add products table"
```

输出示例：
```
INFO  [alembic.autogenerate.compare.tables] Detected added table 'products'
Generating /path/to/alembic/versions/xxx_add_products_table.py ... done
```

### 4. 应用迁移

```bash
uv run alembic upgrade head
```

### 5. 验证结果

```bash
uv run python scripts/check_migration.py
```

## ⚠️ 重要提示

### 模型命名规范

为了被自动检测，模型类必须：
1. ✅ 继承自 `Base`
2. ✅ 有 `__tablename__` 属性
3. ✅ 类名不以下划线开头
4. ✅ 文件名不以下划线开头（除了 `__init__.py`）

### 示例

```python
# ✅ 正确 - 会被自动检测
class User(Base):
    __tablename__ = "users"
    # ...

# ✅ 正确 - 会被自动检测
class OrderItem(Base):
    __tablename__ = "order_items"
    # ...

# ❌ 错误 - 不会被检测（没有 __tablename__）
class Helper(Base):
    # ...

# ❌ 错误 - 不会被检测（类名以下划线开头）
class _InternalModel(Base):
    __tablename__ = "internal"
    # ...
```

## 🐛 常见问题排查

### 问题 1: 新模型没有被检测到

**症状**: 运行 `alembic revision --autogenerate` 后没有生成新表的迁移

**解决方法**:
```bash
# 1. 验证模型是否被导入
uv run python -c "from app.models import YourModel; print('✅ 已导入')"

# 2. 检查模型是否有 __tablename__
uv run python -c "from app.models import YourModel; print(YourModel.__tablename__)"

# 3. 查看所有已加载的模型
uv run python -c "import app.models; print(app.models.__all__)"
```

### 问题 2: 迁移生成了但是是空的

**原因**: 模型定义与数据库当前状态一致

**验证**:
```bash
uv run alembic check
```

如果输出 `No new upgrade operations detected.`，说明数据库已是最新状态。

### 问题 3: 想要手动控制导入

如果你不想使用自动导入，可以恢复手动模式：

```python
# app/models/__init__.py (手动模式)
from .user import User
from .product import Product
# ... 手动导入所有模型

__all__ = ["User", "Product", ...]
```

## 📚 最佳实践

### 1. 开发流程

```bash
# 1. 创建模型文件
vim app/models/new_model.py

# 2. 验证自动导入
uv run python -c "from app.models import NewModel; print('✅')"

# 3. 生成迁移
uv run alembic revision --autogenerate -m "add new_model table"

# 4. 检查生成的迁移文件
cat alembic/versions/xxx_add_new_model_table.py

# 5. 应用迁移
uv run alembic upgrade head

# 6. 验证
uv run alembic check
```

### 2. 迁移消息规范

使用清晰的迁移消息：

```bash
# ✅ 好的消息
uv run alembic revision --autogenerate -m "add user profile table"
uv run alembic revision --autogenerate -m "add email column to users"
uv run alembic revision --autogenerate -m "create indexes for performance"

# ❌ 不好的消息
uv run alembic revision --autogenerate -m "update"
uv run alembic revision --autogenerate -m "fix"
uv run alembic revision --autogenerate -m "changes"
```

### 3. 提交前检查

```bash
# 在 git commit 前执行
uv run alembic check
uv run python scripts/check_migration.py
```

### 4. 生产环境部署

```bash
# 1. 备份数据库
mysqldump -u user -p database > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. 测试迁移（查看 SQL 但不执行）
uv run alembic upgrade head --sql > migration.sql
cat migration.sql  # 检查 SQL

# 3. 应用迁移
uv run alembic upgrade head

# 4. 验证
uv run alembic check
```

## 🎯 总结

### 传统方式 vs 自动化方式

| 操作 | 传统方式 | 自动化方式 |
|------|---------|-----------|
| 创建模型 | ✅ 创建文件 | ✅ 创建文件 |
| 导入模型 | ❌ 手动在 `__init__.py` 中导入 | ✅ **自动** |
| 更新 env.py | ❌ 手动添加导入 | ✅ **无需操作** |
| 生成迁移 | ✅ `alembic revision --autogenerate` | ✅ `alembic revision --autogenerate` |
| 应用迁移 | ✅ `alembic upgrade head` | ✅ `alembic upgrade head` |

### 关键优势

- 🚀 **零配置**: 创建模型文件即可，无需任何额外配置
- 🔄 **自动同步**: 模型变更自动被 Alembic 检测
- 🛡️ **类型安全**: 只导入有效的 SQLAlchemy 模型
- 📦 **易于维护**: 不需要维护导入列表
- ⚡ **开发效率**: 减少重复性工作，专注于业务逻辑

现在，你可以专注于编写模型，其他的交给自动化！🎉
