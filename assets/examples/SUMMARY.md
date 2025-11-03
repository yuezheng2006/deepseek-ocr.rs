# 示例图片集合总结

## ✅ 已完成的工作

### 1. 目录结构创建
- ✅ 创建了 `assets/examples/` 目录结构
- ✅ 按场景分类：`invoices/`, `reports/`, `forms/`, `receipts/`
- ✅ 每个分类目录包含 README.md 说明文档

### 2. 示例文件添加
- ✅ **发票示例**: `invoices/vat_invoice.png` (279KB)
  - 增值税电子普通发票
  - 包含复杂表格结构、多行数据
  - 已生成OCR识别结果：`vat_invoice_result.txt` (6.6KB)

### 3. 文档创建
- ✅ `assets/examples/README.md` - 总体说明
- ✅ `assets/examples/DOWNLOAD_GUIDE.md` - 下载指南
- ✅ `assets/examples/index.json` - 示例索引文件
- ✅ 各分类目录的 README.md - 分类说明

### 4. 工具脚本
- ✅ `scripts/download_examples.py` - 自动下载和生成OCR结果脚本
- ✅ `scripts/download_examples.sh` - 备用下载脚本

## 📋 当前示例文件

```
assets/examples/
├── invoices/
│   ├── vat_invoice.png              # 增值税发票 (279KB)
│   ├── vat_invoice_result.txt       # OCR识别结果 (6.6KB)
│   └── README.md                    # 示例说明
├── reports/
│   └── README.md                    # 待添加示例说明
├── forms/
│   └── README.md                    # 待添加示例说明
├── receipts/
│   └── README.md                    # 待添加示例说明
├── index.json                       # 示例索引
├── README.md                        # 总体说明
└── DOWNLOAD_GUIDE.md                # 下载指南
```

## 🎯 示例特点

### vat_invoice.png (增值税发票)

**复杂度**: ⭐⭐⭐⭐⭐ (高)

**包含元素**:
- ✅ 复杂表格结构（多行多列）
- ✅ 合并单元格
- ✅ 二维码和印章
- ✅ 多种字体和字号
- ✅ 坐标信息提取
- ✅ HTML表格输出

**识别结果**:
- 包含完整的发票信息
- 带坐标的文本提取
- HTML表格格式输出
- 1723 字符的识别结果

## 📝 添加新示例的方法

### 方法1: 手动添加

```bash
# 1. 将图片复制到对应目录
cp your_image.png assets/examples/invoices/

# 2. 生成OCR识别结果
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract all text." \
  --image assets/examples/invoices/your_image.png \
  --max-new-tokens 2048 \
  2>/dev/null > assets/examples/invoices/your_image_result.txt

# 3. 更新README和索引
```

### 方法2: 使用下载脚本

```bash
# 运行自动下载脚本
python3 scripts/download_examples.py
```

## 🔗 相关资源

### 推荐的数据集来源

1. **ICDAR数据集**
   - ICDAR 2019 表格识别挑战赛
   - ICDAR 2015 自然场景文本
   - URL: https://rrc.cvc.uab.es/

2. **公开OCR测试集**
   - Tesseract OCR测试图片
   - 各种开源OCR项目的测试数据

3. **自制数据集**
   - 使用脱敏后的真实文档
   - 确保遵守版权和使用条款

## 📊 使用示例

### 测试现有示例

```bash
# 查看识别结果
cat assets/examples/invoices/vat_invoice_result.txt

# 重新识别（测试不同prompt）
deepseek-ocr-cli \
  --prompt "<image>\n<|grounding|>Extract invoice number and total amount only." \
  --image assets/examples/invoices/vat_invoice.png \
  --max-new-tokens 512
```

### 批量处理

```bash
# 处理所有示例图片
for img in assets/examples/**/*.png; do
  echo "Processing: $img"
  deepseek-ocr-cli \
    --prompt "<image>\n<|grounding|>Extract all text." \
    --image "$img" \
    --max-new-tokens 2048 \
    2>/dev/null > "${img%.png}_output.txt"
done
```

## ⚠️ 注意事项

1. **必须使用 `<|grounding|>` 标记**才能获得完整识别结果
2. 复杂场景建议使用 `--max-new-tokens 2048` 或更高
3. 确保图片清晰、对比度良好
4. 遵守版权和使用条款
5. 使用脱敏后的真实文档

## 🎯 下一步建议

1. **添加更多示例图片**:
   - 财务报表（`reports/`）
   - 申请表（`forms/`）
   - 收据小票（`receipts/`）

2. **丰富示例类型**:
   - 不同复杂度的文档
   - 不同语言的文档
   - 手写文档

3. **完善文档**:
   - 添加每个示例的详细说明
   - 提供使用技巧和最佳实践
   - 记录常见问题和解决方案

---

**创建日期**: 2024-11-03
**版本**: 1.0

