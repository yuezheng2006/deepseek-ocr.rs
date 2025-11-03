# FORMS 示例

## sample_form.png

### 描述
表单示例（临时示例，建议替换为更合适的表单图片）。

### 当前状态
⚠️ **临时示例** - 当前使用的是通用文档图片，建议从以下资源下载更合适的表单示例：
- FUNSD数据集: https://guillaumejaume.github.io/FUNSD/
- ICDAR 2019 表单识别: https://rrc.cvc.uab.es/?ch=16

### 识别结果
识别结果保存在 `sample_form_result.txt` 文件中。

## 建议添加的示例

- 申请表（各种申请表格）
- 登记表（信息登记表格）
- 审批表（审批流程表格）

---

## 🧪 测试用例模板

### Case 1: 完整表单识别

**测试目标**: 验证表单字段的完整识别能力

**执行命令**:

```bash
# Metal加速模式（Apple Silicon，推荐）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all form fields and their values as a structured list." \
  --image assets/examples/forms/sample_form.png \
  --max-new-tokens 1024 \
  --device metal \
  --dtype f16 \
  2>/dev/null > test_output.txt

# CPU模式（稳定可靠）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all form fields and their values." \
  --image assets/examples/forms/sample_form.png \
  --max-new-tokens 1024 \
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
  
  # 验证字段提取
  if grep -q "姓名\|name\|电话\|phone\|邮箱\|email" test_output.txt; then
    echo "✅ 表单字段提取成功"
  else
    echo "❌ 表单字段提取失败"
  fi
else
  echo "❌ 识别失败"
fi
```

**预期结果**:
- 结果长度: > 500 字符（取决于表单复杂度）
- 包含: 字段名称和对应的值
- 包含: 坐标信息

---

### Case 2: 特定字段提取

**测试目标**: 提取表单中的关键字段

**执行命令**:

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract only the following fields:\n1. Name (姓名)\n2. Email (邮箱)\n3. Phone (电话)\nFormat as JSON." \
  --image assets/examples/forms/sample_form.png \
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
  --prompt "<image>\n<|grounding|>Extract all form fields." \
  --image assets/examples/forms/sample_form.png \
  --max-new-tokens 1024 \
  --device metal \
  --dtype f16 \
  2>/dev/null > /dev/null
```

---

## 📋 使用方法

### 基本识别

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all form fields and their values." \
  --image assets/examples/forms/sample_form.png \
  --max-new-tokens 1024 \
  2>/dev/null > result.txt
```

### 提取特定字段

```bash
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract name, email, and phone number only." \
  --image assets/examples/forms/sample_form.png \
  --max-new-tokens 512
```

---

## ⚠️ 注意事项

1. **必须使用 `<|grounding|>` 标记**才能获得完整识别结果
2. 表单识别建议使用 `--max-new-tokens 1024` 或更高
3. 识别结果包含坐标信息，可用于后续的数据提取和处理

---

**最后更新**: 2024-11-03
