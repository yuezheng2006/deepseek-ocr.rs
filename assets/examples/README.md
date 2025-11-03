# 示例图片集合

本目录包含用于测试 DeepSeek-OCR 的各种复杂场景示例图片及其识别结果。

## 📁 目录结构

```
examples/
├── invoices/      # 发票类示例
│   ├── vat_invoice.png              # 增值税发票
│   ├── vat_invoice_result.txt       # 识别结果
│   └── README.md                    # 示例说明
├── reports/       # 报表类示例
│   └── README.md
├── forms/         # 表单类示例
│   └── README.md
├── receipts/      # 收据类示例
│   └── README.md
├── index.json     # 示例索引文件
├── README.md      # 本文件
└── DOWNLOAD_GUIDE.md  # 下载指南
```

## 📋 当前示例

### ✅ 已包含

- **发票类** (`invoices/`)
  - `vat_invoice.png` - 增值税电子普通发票（复杂表格结构）
  - `vat_invoice_result.txt` - 完整OCR识别结果

### 📝 待添加

请参考 [DOWNLOAD_GUIDE.md](./DOWNLOAD_GUIDE.md) 添加更多示例：

- **报表类** (`reports/`): 财务报表、数据报表、统计报表
- **表单类** (`forms/`): 申请表、登记表、审批表  
- **收据类** (`receipts/`): 收据、小票、账单

## 🚀 快速开始

### 测试现有示例

```bash
# 测试发票识别
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this VAT invoice to markdown format." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 2048 \
  2>/dev/null > result.txt
```

### 查看识别结果

```bash
# 查看发票识别结果
cat assets/examples/invoices/vat_invoice_result.txt
```

### 批量处理

```bash
# 批量处理所有示例图片
for category in invoices reports forms receipts; do
  for img in assets/examples/$category/*.png; do
    if [ -f "$img" ]; then
      echo "Processing: $img"
      deepseek-ocr-cli \
        --prompt "<image>\n<|grounding|>Extract all text." \
        --image "$img" \
        --max-new-tokens 2048 \
        2>/dev/null > "${img%.png}_output.txt"
    fi
  done
done
```

## 📖 使用说明

### 每个示例包含

1. **图片文件** (`.png`, `.jpg`): 待识别的原始图片
2. **识别结果** (`*_result.txt`): OCR识别后的文本输出
3. **README.md**: 示例说明文档（包含使用方法、特点等）

### 识别结果格式

识别结果包含：
- **坐标信息**: `text[[x1, y1, x2, y2]]` - 文本位置
- **HTML表格**: `<table>...</table>` - 表格结构
- **原始文本**: 提取的文本内容

示例：
```
title[[310, 95, 735, 149]]
# 四川增值税电子普通发票

text[[703, 125, 861, 149]]
发票代码：051001800211

table[[50, 259, 939, 860]]
<table>
  <tr>
    <td>购买方</td>
    <td colspan="5">名 称：西华大学</td>
  </tr>
</table>
```

## ⚠️ 重要提示

1. **必须使用 `<|grounding|>` 标记**才能获得完整识别结果
2. 复杂场景建议使用 `--max-new-tokens 2048` 或更高
3. 识别结果包含坐标信息，可用于后续处理

## 🔗 相关文档

- [下载指南](./DOWNLOAD_GUIDE.md) - 如何添加新示例
- [CLI使用指南](../../CLI_USAGE_GUIDE.md) - 完整使用文档
- [项目README](../../README.md) - 项目说明

## 📊 示例统计

查看 `index.json` 获取所有示例的详细信息。

---

**最后更新**: 2024-11-03
**版本**: 1.0
