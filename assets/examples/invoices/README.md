# 发票示例说明

## vat_invoice.png

### 描述
增值税电子普通发票示例，包含复杂的表格结构和多行数据。

### 复杂度
**高** - 包含多种元素：
- 复杂的表格结构（多行多列）
- 合并单元格
- 二维码和印章
- 多种字体和字号

### 特点
- ✅ 复杂表格结构识别
- ✅ 坐标信息提取
- ✅ HTML表格输出
- ✅ 多行数据提取

---

## 🧪 测试用例

### Case 1: 完整发票识别（推荐测试）

**测试目标**: 验证复杂表格结构的完整识别能力

**执行命令**:

```bash
# Metal加速模式（Apple Silicon，推荐）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this VAT invoice to markdown format." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 2048 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_output.txt

# CPU模式（稳定可靠）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this VAT invoice to markdown format." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 2048 \
  --device cpu \
  --dtype f32 \
  2>/dev/null > test_output.txt
```

**验证命令**:

```bash
# 检查结果文件
if [ -f test_output.txt ]; then
  echo "✅ 识别完成"
  echo "结果长度: $(wc -c < test_output.txt) 字符"
  
  # 验证关键信息
  if grep -q "发票代码\|发票号码\|四川增值税" test_output.txt; then
    echo "✅ 关键信息提取成功"
  else
    echo "❌ 关键信息提取失败"
  fi
  
  # 验证表格结构
  if grep -q "<table>" test_output.txt; then
    echo "✅ 表格结构识别成功"
  else
    echo "❌ 表格结构识别失败"
  fi
else
  echo "❌ 识别失败"
fi
```

**预期结果**:
- 结果长度: ~1700+ 字符
- 包含: 发票代码、发票号码、购买方信息、商品明细、金额等
- 包含: HTML表格结构
- 包含: 坐标信息（如 `text[[x1, y1, x2, y2]]`）

**参考结果**: `vat_invoice_result.txt`

---

### Case 2: 特定字段提取

**测试目标**: 验证定向信息提取能力

**执行命令**:

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract only the following information from this invoice:\n1. Invoice number (发票号码)\n2. Date (开票日期)\n3. Buyer name (购买方名称)\n4. Total amount (价税合计)\nFormat as JSON." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 512 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_extract.txt
```

**验证命令**:

```bash
# 检查是否包含关键字段
if grep -q "发票号码\|65281307\|日期\|2019\|西华大学\|79.80" test_extract.txt; then
  echo "✅ 关键字段提取成功"
else
  echo "❌ 关键字段提取失败"
fi
```

---

### Case 3: 性能测试

**测试目标**: 测量识别性能

**执行命令**:

```bash
# 计时测试
time deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this invoice." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 1024 \
  --device metal \
  --dtype f16 \
  2>/dev/null > /dev/null
```

**预期性能**:
- Metal (F16): 模型加载 ~5-10s，生成 ~25-30s，总计 ~30-40s
- CPU (F32): 模型加载 ~10-15s，生成 ~90-100s，总计 ~100-115s

---

## 📋 使用方法

### 基本识别

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Convert this VAT invoice to markdown format." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 2048 \
  2>/dev/null > result.txt
```

### 提取特定信息

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract invoice number, date, buyer name, and total amount from this invoice." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 1024
```

### 查看识别结果

```bash
# 查看完整结果
cat assets/examples/invoices/vat_invoice_result.txt

# 只查看文本内容（过滤坐标）
cat assets/examples/invoices/vat_invoice_result.txt | grep -v "^\[\[" | grep -v "^table\[\[" | grep -v "^title\[\[" | grep -v "^image\[\["
```

---

## 📊 识别结果

识别结果保存在 `vat_invoice_result.txt` 文件中，包含：
- 带坐标的文本提取
- HTML表格格式输出
- 完整的发票信息

### 预期输出格式

```
title[[310, 95, 735, 149]]
# 四川增值税电子普通发票

text[[703, 125, 861, 149]]
发票代码：051001800211

text[[703, 162, 831, 185]]
发票号码：65281307

table[[50, 259, 939, 861]]
<table>
  <tr>
    <td>购买方</td>
    <td colspan="5">名 称：西华大学<br>纳税人识别号：12510000450717578Y</td>
  </tr>
  ...
</table>
```

### 结果统计

- **识别结果长度**: ~1723 字符
- **识别时间**: ~27秒（Metal F16）
- **生成token数**: ~694 tokens
- **包含内容**: 标题、文本、表格、图片坐标

---

## ⚠️ 注意事项

1. **必须使用 `<|grounding|>` 标记**才能获得完整识别结果
2. 复杂表格可能需要较大的 `max-new-tokens`（建议 2048+）
3. 识别结果包含坐标信息，可用于后续的数据提取和处理
4. 使用 `2>/dev/null` 过滤日志，只获取纯文本结果

---

## 🔍 故障排除

### 问题: 识别结果只有 `.<table>`

**原因**: 未使用 `<|grounding|>` 标记

**解决**:
```bash
# ❌ 错误格式
--prompt "<image>\nExtract text."

# ✅ 正确格式
--prompt "<image>\n<|grounding|>Extract text."
```

### 问题: 结果被截断

**原因**: `max-new-tokens` 设置太小

**解决**:
```bash
# 增加token限制
--max-new-tokens 2048  # 或更高
```

---

**最后更新**: 2024-11-03
