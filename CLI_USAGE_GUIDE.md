# DeepSeek OCR CLI 使用指南

## 📖 目录

- [快速开始](#快速开始)
- [安装](#安装)
- [基础用法](#基础用法)
- [常用场景](#常用场景)
- [命令参数详解](#命令参数详解)
- [配置文件](#配置文件)
- [性能优化](#性能优化)
- [🍎 macOS 专用指南](#macos-专用指南)
- [故障排除](#故障排除)

---

## 🚀 快速开始

### 前置要求

- Rust 1.78+
- 13GB+ 可用内存
- 15GB+ 磁盘空间（包含模型）

### 一键运行

```bash
# 克隆项目
git clone https://github.com/TimmyOVO/deepseek-ocr.rs.git
cd deepseek-ocr.rs

# 首次运行（自动下载模型 ~6.3GB）
cargo run -p deepseek-ocr-cli --release -- \
  --prompt "<image>\n<|grounding|>Extract all text from this document." \
  --image /path/to/your/document.png \
  --device cpu \
  --max-new-tokens 512
```

> **注意**: 首次运行会下载模型，需要 5-15 分钟，后续运行无需下载。

---

## 📦 安装

### 方式 1: 全局安装（推荐）

```bash
# CPU 版本
cargo install --path crates/cli

# Apple Silicon (Metal 加速)
cargo install --path crates/cli --features metal,accelerate

# Linux NVIDIA GPU (实验性)
cargo install --path crates/cli --features cuda

# Intel CPU (MKL 加速)
cargo install --path crates/cli --features mkl
```

安装后，确保 `~/.cargo/bin` 在 PATH 中：

```bash
# 添加到 shell 配置
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc  # 或 ~/.bashrc
source ~/.zshrc
```

### 方式 2: 项目内运行

```bash
# 编译
cargo build --release -p deepseek-ocr-cli

# 运行
./target/release/deepseek-ocr-cli [OPTIONS]
```

---

## 💡 基础用法

### ⚠️ 重要提示：Prompt 格式

**必须使用 `<|grounding|>` 标记才能获得完整识别结果！**

```bash
# ✅ 正确格式（推荐）
--prompt "<image>\n<|grounding|>Convert this document to markdown."

# ❌ 错误格式（只能输出空表格）
--prompt "<image>\nExtract text."
```

`<|grounding|>` 标记启用定位功能，让模型输出带坐标的完整识别结果。

### 最简命令

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract text." \
  --image document.png
```

### 完整示例

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this invoice to markdown format." \
  --image invoice.png \
  --device cpu \
  --max-new-tokens 1024 \
  --dtype f32
```

### 支持的图像格式

- ✅ PNG (.png)
- ✅ JPEG (.jpg, .jpeg)
- ✅ 其他 image crate 支持的格式

---

## 🎯 常用场景

### 1. 提取收据/发票文本

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this receipt, including items, prices, and total amount." \
  --image receipt.png \
  --max-new-tokens 512
```

**输出示例:**
```
RECEIPT

Coffee    $3.50
Sandwich  $8.00
Tax       $1.15

TOTAL     $12.65

Thank you!
Invoice #12345
```

---

### 2. 发票识别（增值税发票）

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this VAT invoice to markdown format." \
  --image assets/demo1.png \
  --max-new-tokens 2048
```

**输出示例:**
```markdown
title[[310, 95, 735, 149]]
# 四川增值税电子普通发票

text[[703, 125, 861, 149]]
发票代码：051001800211

text[[703, 162, 832, 185]]
发票号码：65281307

table[[50, 259, 939, 860]]
<table>
  <tr>
    <td>购买方</td>
    <td colspan="5">名 称：西华大学<br>纳税人识别号：12510000450717578Y</td>
  </tr>
  ...
</table>
```

### 3. 表格转 Markdown

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this table to markdown format." \
  --image invoice_table.png \
  --max-new-tokens 1024
```

**输出示例:**
```markdown
| Item                    | Qty | Price    | Total      |
|-------------------------|-----|----------|------------|
| Web Development Service | 40  | $150.00  | $6,000.00  |
| Database Design         | 20  | $120.00  | $2,400.00  |
```

---

### 4. 财务报表识别

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all data from this financial report, including tables, numbers, and text." \
  --image financial_report.png \
  --max-new-tokens 2048
```

### 5. 提取表单数据

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all form fields and their values as a structured list." \
  --image application_form.png \
  --max-new-tokens 512
```

**输出示例:**
```
APPLICATION FORM

Name: John Smith
Email: john.smith@email.com
Phone: +1 (555) 123-4567
Address: 456 Oak Avenue, Boston, MA 02101
Date: October 31, 2024
```

---

### 6. 带坐标定位 (Grounding)

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract text with bounding box coordinates." \
  --image document.png \
  --max-new-tokens 512
```

**输出示例:**
```
text[[48, 67, 152, 102]]
RECEIPT

text[[48, 234, 232, 271]]
Coffee $3.50

text[[48, 569, 250, 605]]
TOTAL $12.65
```

> 坐标格式: `[x1, y1, x2, y2]` 表示左上角和右下角

---

### 7. 批量处理文档

```bash
#!/bin/bash
# 批量处理目录下所有图片

for img in ~/Documents/invoices/*.png; do
  echo "Processing: $img"

  deepseek-ocr-cli \
    --prompt "<image>\n<|grounding|>Extract invoice number, date, and total amount." \
    --image "$img" \
    --device cpu \
    --max-new-tokens 512 > "${img%.png}_extracted.txt"

  echo "Saved to: ${img%.png}_extracted.txt"
done

echo "Batch processing complete!"
```

---

### 8. 从文件读取 Prompt

```bash
# 创建 prompt 文件
cat > custom_prompt.txt << 'EOF'
<image>
<|grounding|>Please extract the following information from this invoice:
1. Invoice number
2. Date
3. Customer name
4. Line items with prices
5. Total amount

Format the output as JSON.
EOF

# 使用 prompt 文件
deepseek-ocr-cli \
  --prompt-file custom_prompt.txt \
  --image invoice.png \
  --max-new-tokens 1024
```

---

## 📋 命令参数详解

### 核心参数

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt <TEXT>` | ✅ | - | 包含 `<image>` 占位符的提示词 |
| `--prompt-file <PATH>` | - | - | 从文件读取 prompt（覆盖 --prompt） |
| `--image <PATH>` | ✅ | - | 图片路径，可重复指定多个 |

### 推理参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--device <DEVICE>` | `cpu` | 设备: `cpu` / `metal` / `cuda` |
| `--dtype <DTYPE>` | 自动 | 精度: `f32` / `f16` / `bf16` |
| `--max-new-tokens <NUM>` | `512` | 生成文本的最大 token 数 |
| `--template <NAME>` | `plain` | 模板: plain / deepseek / deepseekv2 |
| `--base-size <NUM>` | `1024` | 全局视图分辨率 |
| `--image-size <NUM>` | `640` | 裁剪块分辨率 |
| `--crop-mode <BOOL>` | `true` | 是否启用动态裁剪 |
| `--no-cache` | - | 禁用 KV 缓存（调试用） |

### 配置参数

| 参数 | 说明 |
|------|------|
| `--config <PATH>` | 指定配置文件路径 |
| `--model <ID>` | 选择模型 ID |
| `--model-config <PATH>` | 覆盖模型配置 JSON |
| `--tokenizer <PATH>` | 覆盖 tokenizer 路径 |
| `--weights <PATH>` | 覆盖模型权重路径 |

### 其他参数

| 参数 | 说明 |
|------|------|
| `-h, --help` | 显示帮助信息 |
| `-V, --version` | 显示版本号 |
| `--bench` | 启用性能基准测试 |
| `--bench-output <PATH>` | 输出基准数据到 JSON 文件 |

---

## ⚙️ 配置文件

### 默认配置路径

| 平台 | 配置文件 | 模型缓存 |
|------|----------|----------|
| **Linux** | `~/.config/deepseek-ocr/config.toml` | `~/.cache/deepseek-ocr/models/` |
| **macOS** | `~/Library/Application Support/deepseek-ocr/config.toml` | `~/Library/Caches/deepseek-ocr/models/` |
| **Windows** | `%APPDATA%\deepseek-ocr\config.toml` | `%LOCALAPPDATA%\deepseek-ocr\models\` |

### 配置文件示例

```toml
[models]
active = "deepseek-ocr"

[models.entries.deepseek-ocr]
# 可选: 指定自定义路径
# config = "/path/to/config.json"
# tokenizer = "/path/to/tokenizer.json"
# weights = "/path/to/model.safetensors"

[inference]
device = "cpu"              # cpu / metal / cuda
template = "plain"
base_size = 1024
image_size = 640
crop_mode = true
max_new_tokens = 512
use_cache = true

[server]
host = "0.0.0.0"
port = 8000
model_id = "deepseek-ocr"
```

### 参数优先级

```
命令行参数 > 配置文件 > 内置默认值
```

### 使用自定义配置

```bash
deepseek-ocr-cli \
  --config ~/my-custom-config.toml \
  --prompt "<image>\nExtract text." \
  --image document.png
```

---

---

## 🍎 macOS 专用指南

### 系统要求

- **macOS**: 13.0+ (Ventura) 或更高版本
- **处理器**: Apple Silicon (M1/M2/M3/M4) 推荐，Intel Mac 也可使用
- **内存**: 至少 8GB 统一内存（推荐 16GB+）
- **磁盘空间**: 至少 15GB（包含模型文件）

### 安装步骤

#### 1. 安装 Rust（如果未安装）

```bash
# 使用 rustup 安装（推荐）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 或使用 Homebrew
brew install rust

# 验证安装
rustc --version
cargo --version
```

#### 2. 克隆项目

```bash
git clone https://github.com/TimmyOVO/deepseek-ocr.rs.git
cd deepseek-ocr.rs
```

#### 3. 编译（推荐使用 Metal 加速）

```bash
# Apple Silicon (M1/M2/M3/M4) - 推荐
cargo build --release -p deepseek-ocr-cli --features metal,accelerate

# Intel Mac（如果没有 Metal 支持）
cargo build --release -p deepseek-ocr-cli

# 全局安装（推荐）
cargo install --path crates/cli --features metal,accelerate
```

#### 4. 配置 PATH

```bash
# 添加到 ~/.zshrc 或 ~/.bash_profile
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证安装
deepseek-ocr-cli --version
```

### 使用 Metal 加速

#### 快速开始

```bash
# 使用 Metal GPU 加速（推荐）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text." \
  --image assets/demo1.png \
  --device metal \
  --dtype f16 \
  --max-new-tokens 2048 \
  2>/dev/null > result.txt
```

#### 性能对比

| 模式 | 模型加载 | 生成时间 | 内存占用 | 稳定性 |
|------|---------|---------|---------|--------|
| **Metal (F16)** | 5-10秒 | 3-5秒/512tokens | ~8GB | ⚠️ 偶尔崩溃 |
| **CPU (F32)** | 10-15秒 | 10-15秒/512tokens | ~13GB | ✅ 非常稳定 |

#### 推荐配置

**快速实验（单次识别）:**
```bash
--device metal --dtype f16 --max-new-tokens 2048
```

**批量处理（稳定优先）:**
```bash
--device cpu --dtype f32 --max-new-tokens 2048
```

**内存受限环境:**
```bash
--device metal --dtype f16 --max-new-tokens 512
```

### macOS 常见问题

#### 1. 编译错误：找不到 Metal 框架

**问题:** `error: failed to run custom build command for 'metal'`

**解决:**
```bash
# 确保 Xcode Command Line Tools 已安装
xcode-select --install

# 或安装完整 Xcode
# 从 App Store 安装 Xcode

# 验证安装
xcode-select -p
```

#### 2. Metal 设备不可用

**问题:** `device metal not available`

**解决:**
```bash
# 检查系统是否支持 Metal
system_profiler SPDisplaysDataType | grep -i metal

# 确保编译时使用了 --features metal
cargo build --release -p deepseek-ocr-cli --features metal,accelerate

# 如果仍然失败，使用 CPU 模式
--device cpu --dtype f32
```

#### 3. 内存不足（Apple Silicon）

**问题:** 系统内存不足，应用被杀死

**解决:**
```bash
# 检查内存使用
vm_stat

# 释放内存
# 1. 关闭其他应用（特别是 Chrome、Xcode 等）
# 2. 重启 Mac
# 3. 使用 CPU 模式（内存占用更稳定）

# 使用 CPU 模式
--device cpu --dtype f32
```

#### 4. 权限问题

**问题:** 无法访问文件或目录

**解决:**
```bash
# 给终端完全磁盘访问权限
# 系统设置 > 隐私与安全性 > 完全磁盘访问权限
# 添加 Terminal.app 或 iTerm.app

# 或使用完整路径
deepseek-ocr-cli \
  --image ~/Downloads/invoice.png \
  --prompt "<image>\n<|grounding|>Extract text."
```

#### 5. 终端显示乱码

**问题:** 中文字符显示为乱码

**解决:**
```bash
# 设置终端编码为 UTF-8
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 或使用 iTerm2（推荐，更好的中文支持）
```

### macOS 性能优化技巧

#### 1. 使用 Metal 加速

```bash
# 编译时启用所有优化
RUSTFLAGS="-C target-cpu=native" cargo build --release \
  -p deepseek-ocr-cli --features metal,accelerate

# 运行时使用 Metal
--device metal --dtype f16
```

#### 2. 减少内存占用

```bash
# 使用 F16 精度（Metal 模式）
--device metal --dtype f16

# 减少 token 限制
--max-new-tokens 512  # 而不是 2048
```

#### 3. 批量处理优化

```bash
# 使用 CPU 模式批量处理（更稳定）
for img in *.png; do
  deepseek-ocr-cli \
    --prompt "<image>\n<|grounding|>Extract text." \
    --image "$img" \
    --device cpu \
    --dtype f32 \
    --max-new-tokens 1024 \
    2>/dev/null > "${img%.png}.txt"
done
```

### 推荐工具

- **终端**: iTerm2 (https://iterm2.com/)
- **包管理**: Homebrew (https://brew.sh/)
- **文本编辑器**: VS Code / Cursor

---

## ⚡ 性能优化

### CPU 模式（稳定可靠）

```bash
# 推荐配置
deepseek-ocr-cli \
  --prompt "<image>\nExtract text." \
  --image document.png \
  --device cpu \
  --dtype f32 \
  --max-new-tokens 512
```

**性能指标:**
- 模型加载: 4-13 秒
- 文本生成: ~10 秒/512 tokens
- 内存占用: ~13GB

---

### Metal 模式（Apple Silicon）

**macOS 专用，强烈推荐！**

```bash
# 编译时启用 Metal 和 Accelerate
cargo build --release -p deepseek-ocr-cli --features metal,accelerate

# 或全局安装
cargo install --path crates/cli --features metal,accelerate

# 运行（使用 Metal GPU 加速）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract text." \
  --image document.png \
  --device metal \
  --dtype f16 \
  --max-new-tokens 512
```

**性能提升:**
- 模型加载: **快 50%** (5-10秒 vs 10-15秒)
- 文本生成: **快 75%** (3秒 vs 12秒)
- 内存占用: **减少 40%** (~8GB vs ~13GB)

**macOS 使用注意事项:**

1. **系统要求**
   - macOS 13.0+ (Ventura)
   - Apple Silicon (M1/M2/M3/M4) 或 Intel Mac 支持 Metal
   - 至少 8GB 统一内存（推荐 16GB+）

2. **首次编译**
   ```bash
   # 确保使用最新版本的 Rust
   rustup update
   
   # 编译时启用 Metal 和 Accelerate
   cargo build --release -p deepseek-ocr-cli --features metal,accelerate
   ```

3. **性能优化建议**
   ```bash
   # 推荐配置（最佳性能）
   --device metal --dtype f16 --max-new-tokens 2048
   
   # 如果遇到内存不足，可以尝试
   --device metal --dtype f16 --max-new-tokens 1024
   ```

4. **已知问题**
   - ⚠️ Metal 后端偶尔可能崩溃（Exit 139），特别是在长时间运行时
   - 💡 **解决方案**: 如果频繁崩溃，建议使用 CPU 模式：
     ```bash
     --device cpu --dtype f32
     ```
   - 建议生产环境或批量处理时使用 CPU 模式（更稳定）
   - 适合快速实验和单次识别任务

5. **检查 Metal 是否可用**
   ```bash
   # 检查系统是否支持 Metal
   system_profiler SPDisplaysDataType | grep -i metal
   
   # 运行测试命令
   deepseek-ocr-cli --image assets/demo1.png \
     --prompt "<image>\n<|grounding|>Test." \
     --device metal --dtype f16
   ```

6. **故障排除**
   - **问题**: `device metal not available`
     - **解决**: 确保编译时使用了 `--features metal,accelerate`
   - **问题**: 崩溃 (Exit 139)
     - **解决**: 切换到 CPU 模式或减少 `max-new-tokens`
   - **问题**: 内存不足
     - **解决**: 关闭其他应用，或使用 CPU 模式

---

### CUDA 模式（实验性）

```bash
# Linux/Windows + NVIDIA GPU
# 需要先安装 CUDA 12.2+

# 编译
cargo build --release -p deepseek-ocr-cli --features cuda

# 运行
deepseek-ocr-cli \
  --prompt "<image>\nExtract text." \
  --image document.png \
  --device cuda \
  --dtype f16 \
  --max-new-tokens 512
```

⚠️ **当前为 Alpha 阶段，不推荐生产使用**

---

### Intel MKL 加速（预览）

```bash
# 安装 Intel oneMKL
# https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html

# 编译
cargo build --release -p deepseek-ocr-cli --features mkl

# 运行（使用 CPU）
deepseek-ocr-cli \
  --prompt "<image>\nExtract text." \
  --image document.png \
  --device cpu
```

---

### 调优建议

#### 1. 控制输出长度

```bash
# 短文本（收据、标签）
--max-new-tokens 256

# 中等长度（表单、简单发票）
--max-new-tokens 512

# 长文本（复杂文档、多页）
--max-new-tokens 1024
```

#### 2. 图像分辨率

```bash
# 高质量文档（推荐）
--base-size 1024 --image-size 640 --crop-mode true

# 快速处理（牺牲精度）
--base-size 768 --image-size 512 --crop-mode false
```

#### 3. 批量处理优化

```bash
# 并行处理（多核 CPU）
for img in *.png; do
  (deepseek-ocr-cli --prompt "<image>\nExtract." --image "$img" > "$img.txt") &
done
wait
```

---

## 🛠️ 故障排除

### 常见问题

#### 1. 模型下载失败

**问题:** 无法连接 Hugging Face

**解决:**
```bash
# 方案 A: 设置代理
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 方案 B: 使用 ModelScope（国内镜像，自动切换）
# 无需额外配置，系统会自动选择最快的源

# 方案 C: 手动下载
# 1. 访问 https://huggingface.co/deepseek-ai/DeepSeek-OCR
# 2. 下载文件到模型缓存目录
# 3. 重新运行
```

---

#### 2. 内存不足

**错误:** `out of memory` 或程序被杀死

**解决:**
```bash
# 检查可用内存
free -h  # Linux
vm_stat  # macOS

# 关闭其他应用释放内存
# 至少保证 13GB 可用内存

# 或使用 swap（不推荐，会很慢）
```

---

#### 3. 输出被截断

**问题:** 生成的文本不完整

**解决:**
```bash
# 增加 token 限制
--max-new-tokens 1024  # 或更高

# 检查日志确认是否达到限制
# 看到 "Generation done" 表示正常结束
```

---

#### 4. 图片无法识别

**错误:** `failed to open image` 或 `Invalid PNG signature`

**解决:**
```bash
# 检查文件是否存在
ls -lh /path/to/image.png

# 验证图片格式
file /path/to/image.png

# 转换图片格式
convert input.webp output.png  # 需要 ImageMagick
```

---

#### 5. Prompt 验证失败

**错误:** `prompt includes 0 <image> tokens but 1 image paths were provided`

**解决:**
```bash
# 确保 prompt 中包含 <image> 占位符和 <|grounding|> 标记
--prompt "<image>\n<|grounding|>Extract text."  # ✅ 正确

--prompt "Extract text."                         # ❌ 错误，缺少 <image>
--prompt "<image>\nExtract text."                # ❌ 错误，缺少 <|grounding|>

# <image> 数量必须与 --image 参数数量一致
--prompt "<image>\n<|grounding|>First image. <image>\n<|grounding|>Second image." \
--image img1.png \
--image img2.png
```

---

#### 6. Metal 崩溃 (Exit 139) - macOS 常见问题

**问题:** 使用 Metal 时偶尔段错误或崩溃

**macOS 特定解决方案:**

```bash
# 方案 1: 切换到 CPU 模式（最稳定）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract text." \
  --image document.png \
  --device cpu \
  --dtype f32 \
  --max-new-tokens 512

# 方案 2: 减少 token 限制（降低内存压力）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract text." \
  --image document.png \
  --device metal \
  --dtype f16 \
  --max-new-tokens 256

# 方案 3: 关闭其他占用 GPU 的应用
# 关闭 Chrome、Final Cut Pro、Xcode 等 GPU 密集型应用

# 方案 4: 检查系统内存
vm_stat  # 查看内存使用情况
```

**预防措施:**
- 批量处理时使用 CPU 模式
- 单次识别可以使用 Metal（更快）
- 确保有足够的可用内存（至少 8GB）
- 定期重启以清理 GPU 缓存

---

#### 7. 命令未找到

**错误:** `command not found: deepseek-ocr-cli`

**解决:**
```bash
# 检查安装路径
ls -lh ~/.cargo/bin/deepseek-ocr-cli

# 添加到 PATH
export PATH="$HOME/.cargo/bin:$PATH"

# 永久添加
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 或使用完整路径
~/.cargo/bin/deepseek-ocr-cli --version
```

---

### 获取详细日志

```bash
# 启用详细日志
RUST_LOG=debug deepseek-ocr-cli \
  --prompt "<image>\nExtract." \
  --image document.png 2>&1 | tee debug.log
```

---

### 性能基准

### 测试环境（macOS）

- **CPU:** Apple M4 Pro (12核)
- **内存:** 16GB 统一内存
- **系统:** macOS 15.1
- **测试图片:** 增值税发票 (1440x1920px)

### 基准结果

| 模式 | 模型加载 | 文本生成 (512 tokens) | 总时间 | 内存占用 |
|------|----------|----------------------|--------|---------|
| CPU (F32) | 10-15秒 | 10-15秒 | ~25秒 | ~13GB |
| Metal (F16) | 5-10秒 | 3-5秒 | ~10秒 | ~8GB |

**性能提升总结:**
- Metal 模式比 CPU 模式快 **60-75%**
- 内存占用减少 **40%**
- 适合快速实验和单次识别

---

## 📚 高级用法

### 结构化输出

```bash
deepseek-ocr-cli \
  --prompt '<image>\nExtract invoice data as JSON:
{
  "invoice_number": "...",
  "date": "...",
  "total": "...",
  "items": [...]
}' \
  --image invoice.png \
  --max-new-tokens 1024
```

---

### 多语言支持

```bash
# 英文
--prompt "<image>\nExtract all text in English."

# 中文
--prompt "<image>\n提取所有文本内容。"

# 混合
--prompt "<image>\nExtract text. Output in Chinese."
```

---

### 与其他工具集成

```bash
# 结合 jq 处理 JSON
deepseek-ocr-cli \
  --prompt "<image>\nOutput JSON." \
  --image invoice.png | jq '.total'

# 保存为文件
deepseek-ocr-cli \
  --prompt "<image>\nExtract." \
  --image doc.png > output.txt

# 通过管道传递
deepseek-ocr-cli --prompt "<image>\nExtract." --image doc.png | \
  grep "TOTAL" | \
  awk '{print $2}'
```

---

## 🔗 相关资源

- **项目主页:** https://github.com/TimmyOVO/deepseek-ocr.rs
- **模型源:** https://huggingface.co/deepseek-ai/DeepSeek-OCR
- **问题反馈:** https://github.com/TimmyOVO/deepseek-ocr.rs/issues
- **完整文档:** [README.md](README.md)

---

## 📄 许可证

本项目遵循上游 DeepSeek-OCR 模型的使用条款。详见 `DeepSeek-OCR/LICENSE`。

---

## 📸 示例图片

项目 `assets/examples/` 目录包含丰富的示例图片供测试：

### 当前示例

- **发票类** (`invoices/`):
  - `vat_invoice.png` - 增值税发票（复杂表格结构）✅

- **报表类** (`reports/`):
  - `report_summary.png` - 汇总报表 ✅
  - `sample_report.png` - 临时示例

- **表单类** (`forms/`):
  - `sample_form.png` - 临时示例

- **收据类** (`receipts/`):
  - `receipt_menu.png` - 手写菜单（4MB）✅
  - `receipt_pos.png` - POS小票 ✅
  - `sample_receipt.png` - 临时示例

### 使用示例图片

```bash
# 测试发票识别
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this invoice to markdown." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 2048 \
  2>/dev/null > result.txt

# 测试手写菜单识别
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all dish names and prices." \
  --image assets/examples/receipts/receipt_menu.png \
  --max-new-tokens 2048 \
  2>/dev/null > menu_result.txt

# 测试POS小票识别
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this receipt." \
  --image assets/examples/receipts/receipt_pos.png \
  --max-new-tokens 1024 \
  2>/dev/null > receipt_result.txt
```

更多示例和使用方法请参考 [`assets/examples/README.md`](assets/examples/README.md)

---

**最后更新:** 2024-11-03
**版本:** 0.3.3
