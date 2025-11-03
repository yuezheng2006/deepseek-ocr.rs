# RECEIPTS 示例

## sample_receipt.png

### 描述
收据示例（临时示例，建议替换为更合适的收据图片）。

### 当前状态
⚠️ **临时示例** - 当前使用的是通用文档图片，建议从以下资源下载更合适的收据示例：
- CORD数据集: https://github.com/clovaai/cord-dataset
- SROIE数据集: https://rrc.cvc.uab.es/?ch=13 (ICDAR 2019 收据识别)

### 识别结果
识别结果保存在 `sample_receipt_result.txt` 文件中。

## 建议添加的示例

- 收据（标准收据格式）
- 小票（购物小票、POS机小票）
- 账单（各种账单格式）

---

## 🧪 测试用例模板

### Case 1: 完整收据识别

**测试目标**: 验证收据信息的完整识别能力

**执行命令**:

```bash
# Metal加速模式（Apple Silicon，推荐）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this receipt, including items, prices, and total amount." \
  --image assets/examples/receipts/sample_receipt.png \
  --max-new-tokens 512 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_output.txt

# CPU模式（稳定可靠）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this receipt." \
  --image assets/examples/receipts/sample_receipt.png \
  --max-new-tokens 512 \
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
  if grep -q "金额\|total\|合计\|price" test_output.txt; then
    echo "✅ 金额信息提取成功"
  else
    echo "❌ 金额信息提取失败"
  fi
  
  # 验证商品信息
  if grep -q "商品\|item\|名称\|name" test_output.txt; then
    echo "✅ 商品信息提取成功"
  else
    echo "⚠️  商品信息可能缺失"
  fi
else
  echo "❌ 识别失败"
fi
```

**预期结果**:
- 结果长度: > 200 字符（取决于收据复杂度）
- 包含: 商品名称、价格、总金额等
- 包含: 坐标信息

---

### Case 2: 金额提取

**测试目标**: 只提取收据中的金额信息

**执行命令**:

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract only prices and total amount from this receipt. Format as JSON." \
  --image assets/examples/receipts/sample_receipt.png \
  --max-new-tokens 256 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_extract.txt
```

---

### Case 3: 性能测试

**执行命令**:

```bash
time deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this receipt." \
  --image assets/examples/receipts/sample_receipt.png \
  --max-new-tokens 512 \
  --device metal \
  --dtype f16 \
  2>/dev/null > /dev/null
```

---

## 📋 使用方法

### 基本识别

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text from this receipt." \
  --image assets/examples/receipts/sample_receipt.png \
  --max-new-tokens 512 \
  2>/dev/null > result.txt
```

### 提取金额信息

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract items, prices, and total amount only." \
  --image assets/examples/receipts/sample_receipt.png \
  --max-new-tokens 512
```

---

## ⚠️ 注意事项

1. **必须使用 `<|grounding|>` 标记**才能获得完整识别结果
2. 收据识别通常需要 `--max-new-tokens 512` 即可
3. 识别结果包含坐标信息，可用于后续的数据提取和处理

---

**最后更新**: 2024-11-03
