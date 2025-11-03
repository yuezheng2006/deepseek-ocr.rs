# 示例图片下载指南

由于网络限制和版权问题，部分示例图片需要手动下载。以下是推荐的资源和方法。

## 📥 推荐资源

### 1. 发票示例 (Invoices)

**已包含**:
- `invoices/vat_invoice.png` - 增值税发票 ✅

**推荐来源**:
- ICDAR 2019 表格识别挑战赛数据集
- CORD 数据集（收据和发票）
- 公开的发票识别测试集

**下载方法**:
```bash
# 访问以下资源下载发票示例
# 1. ICDAR: https://rrc.cvc.uab.es/
# 2. CORD: https://github.com/clovaai/cord-dataset
# 3. 或者使用搜索引擎搜索 "invoice OCR dataset"
```

### 2. 收据示例 (Receipts)

**当前状态**: `sample_receipt.png` (414KB) - 临时示例

**推荐来源**:
- **CORD数据集**: https://github.com/clovaai/cord-dataset
  - 包含10,000+收据图像
  - 可免费下载用于研究

- **SROIE数据集**: https://rrc.cvc.uab.es/?ch=13
  - ICDAR 2019 收据识别挑战赛
  - 包含1000张收据图像

**下载命令示例**:
```bash
# 如果数据集提供直接下载链接
curl -L -o assets/examples/receipts/receipt_sample.png "DATASET_URL"
```

### 3. 报表示例 (Reports)

**当前状态**: `sample_report.png` (414KB) - 临时示例

**推荐来源**:
- **TableBank数据集**: https://github.com/doc-analysis/TableBank
  - 包含表格图像（财务报表、数据报表等）
  - 适用于表格识别测试

- **PubTabNet数据集**: https://github.com/ibm-aur-nlp/PubTabNet
  - 包含大量表格图像
  - 涵盖各种报表类型

**下载方法**:
```bash
# 访问TableBank或PubTabNet下载报表示例
# 确保选择财务报表或数据报表类型的图像
```

### 4. 表单示例 (Forms)

**当前状态**: `sample_form.png` (279KB) - 临时示例

**推荐来源**:
- **FUNSD数据集**: https://guillaumejaume.github.io/FUNSD/
  - 包含199张表单图像
  - 标注了表单字段和值

- **ICDAR 2019 表单识别**: https://rrc.cvc.uab.es/?ch=16
  - 表单识别挑战赛数据集

**下载方法**:
```bash
# 访问FUNSD或ICDAR下载表单示例
# 确保选择申请表、登记表等类型的图像
```

## 🔧 下载脚本

### 使用wget下载（如果提供直接链接）

```bash
# 创建下载目录
mkdir -p assets/examples/{invoices,reports,forms,receipts}

# 下载示例（替换为实际URL）
wget -O assets/examples/receipts/receipt_sample.png "URL_HERE"
wget -O assets/examples/reports/financial_report.png "URL_HERE"
wget -O assets/examples/forms/application_form.png "URL_HERE"
```

### 使用Python脚本下载

```python
import urllib.request
from pathlib import Path

base_dir = Path("assets/examples")

# 替换为实际可用的URL
downloads = {
    "receipts/receipt_sample.png": "URL_HERE",
    "reports/financial_report.png": "URL_HERE",
    "forms/application_form.png": "URL_HERE",
}

for rel_path, url in downloads.items():
    file_path = base_dir / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, str(file_path))
        print(f"✅ 下载成功: {rel_path}")
    except Exception as e:
        print(f"❌ 下载失败: {rel_path} - {e}")
```

## 📋 图片要求

下载示例图片时，请确保：

1. **格式**: PNG 或 JPEG
2. **分辨率**: 建议至少 800x600 像素
3. **质量**: 清晰、无模糊、对比度良好
4. **大小**: 每个文件建议 100KB - 10MB
5. **内容**: 符合对应分类的特点

## ✅ 下载后步骤

1. **重命名文件**: 
   ```bash
   mv downloaded_image.png assets/examples/[category]/[descriptive_name].png
   ```

2. **生成OCR识别结果**:
   ```bash
   deepseek-ocr-cli \
     --prompt "<image>\n<|grounding|>Extract all text." \
     --image assets/examples/[category]/[name].png \
     --max-new-tokens 2048 \
     2>/dev/null > assets/examples/[category]/[name]_result.txt
   ```

3. **更新README**: 编辑对应分类的 `README.md`，添加新示例说明

## 🔗 数据集资源链接

### 公开数据集

1. **ICDAR数据集**: https://rrc.cvc.uab.es/
   - 各种OCR挑战赛数据集
   - 包含表格、收据、表单等

2. **GitHub OCR数据集**:
   - CORD: https://github.com/clovaai/cord-dataset
   - TableBank: https://github.com/doc-analysis/TableBank
   - FUNSD: https://github.com/GuillaumeJaume/FUNSD

3. **学术数据集**:
   - CC-OCR: https://arxiv.org/abs/2412.02210
   - OCR-Quality: https://arxiv.org/abs/2510.21774

### 搜索关键词

- "invoice OCR dataset"
- "receipt OCR dataset"
- "form OCR dataset"
- "financial report OCR dataset"
- "table recognition dataset"

## ⚠️ 注意事项

1. **版权**: 确保使用的图片符合版权要求
2. **隐私**: 不要使用包含真实敏感信息的图片
3. **测试**: 建议使用脱敏后的真实文档图片
4. **许可**: 遵守数据集的使用许可协议

## 📝 当前状态

- ✅ **发票**: `vat_invoice.png` - 已包含完整示例
- ⚠️ **收据**: `sample_receipt.png` - 临时示例，建议替换
- ⚠️ **报表**: `sample_report.png` - 临时示例，建议替换
- ⚠️ **表单**: `sample_form.png` - 临时示例，建议替换

## 🎯 下一步

1. 从上述资源下载合适的示例图片
2. 替换临时示例文件
3. 生成OCR识别结果
4. 更新README文档

---

**最后更新**: 2024-11-03
