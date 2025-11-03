# REPORTS 示例

## sample_report.png

### 描述
财务报表/数据报表示例（临时示例，建议替换为更合适的报表图片）。

### 当前状态
⚠️ **临时示例** - 当前使用的是通用文档图片，建议从以下资源下载更合适的报表示例：
- TableBank数据集: https://github.com/doc-analysis/TableBank
- PubTabNet数据集: https://github.com/ibm-aur-nlp/PubTabNet

### 识别结果
识别结果保存在 `sample_report_result.txt` 文件中。

## 建议添加的示例

- 财务报表（资产负债表、利润表）
- 数据报表（包含大量数字和表格）
- 统计报表（包含图表和统计数据）

---

## 🧪 测试用例模板

### Case 1: 完整报表识别

**测试目标**: 验证复杂报表结构的完整识别能力

**执行命令**:

```bash
# Metal加速模式（Apple Silicon，推荐）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all data from this financial report, including tables, numbers, and text." \
  --image assets/examples/reports/sample_report.png \
  --max-new-tokens 2048 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_output.txt

# CPU模式（稳定可靠）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all data from this financial report." \
  --image assets/examples/reports/sample_report.png \
  --max-new-tokens 2048 \
  --device cpu \
  --dtype f32 \
  2>/dev/null > test_output.txt
```

**参考结果**: `sample_report_result.txt`

**验证命令**:

```bash
# 检查结果文件
if [ -f test_output.txt ]; then
  echo "✅ 识别完成"
  echo "结果长度: $(wc -c < test_output.txt) 字符"
  
  # 验证表格结构
  if grep -q "<table>" test_output.txt; then
    echo "✅ 表格结构识别成功"
  else
    echo "❌ 表格结构识别失败"
  fi
  
  # 验证数字数据
  if grep -q "[0-9]\+\.[0-9]\+" test_output.txt; then
    echo "✅ 数字数据提取成功"
  else
    echo "⚠️  数字数据可能缺失"
  fi
else
  echo "❌ 识别失败"
fi
```

**预期结果**:
- 结果长度: > 1000 字符（取决于报表复杂度）
- 包含: 表格结构、数字数据、文本内容
- 包含: 坐标信息

---

### Case 2: 特定数据提取

**测试目标**: 提取报表中的关键数据

**执行命令**:

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract only the following data from this report:\n1. Total revenue\n2. Total expenses\n3. Net profit\nFormat as JSON." \
  --image assets/examples/reports/sample_report.png \
  --max-new-tokens 512 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_extract.txt
```

---

### Case 3: 性能测试

**执行命令**:

```bash
time deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all data from this report." \
  --image assets/examples/reports/sample_report.png \
  --max-new-tokens 2048 \
  --device metal \
  --dtype f16 \
  2>/dev/null > /dev/null
```

---

## 📋 使用方法

### 基本识别

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all data from this financial report." \
  --image assets/examples/reports/sample_report.png \
  --max-new-tokens 2048 \
  2>/dev/null > result.txt
```

### 提取特定数据

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract revenue and profit data only." \
  --image assets/examples/reports/sample_report.png \
  --max-new-tokens 1024
```

---

## ⚠️ 注意事项

1. **必须使用 `<|grounding|>` 标记**才能获得完整识别结果
2. 复杂报表建议使用 `--max-new-tokens 2048` 或更高
3. 识别结果包含坐标信息，可用于后续的数据提取和处理

---

**最后更新**: 2024-11-03
