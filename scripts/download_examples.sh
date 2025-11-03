#!/bin/bash
# 下载示例图片脚本

set -e

BASE_DIR="assets/examples"
cd "$(dirname "$0")/.."

echo "开始下载示例图片..."

# 创建目录
mkdir -p "${BASE_DIR}"/{invoices,reports,forms,receipts}

# 发票示例 - 使用公开的测试数据集
echo "下载发票示例..."
curl -L -o "${BASE_DIR}/invoices/sample_invoice.png" \
  "https://raw.githubusercontent.com/mindee/invoices-dataset/main/samples/invoice.png" 2>/dev/null || \
curl -L -o "${BASE_DIR}/invoices/sample_invoice.png" \
  "https://github.com/tesseract-ocr/tesseract/raw/main/test/testing/phototest.tif" 2>/dev/null || \
echo "发票图片下载失败，将使用备用方法"

# 财务报表示例
echo "下载财务报表示例..."
curl -L -o "${BASE_DIR}/reports/sample_report.png" \
  "https://github.com/ocrmypdf/OCRmyPDF/raw/main/tests/resources/multipage.pdf" 2>/dev/null || \
echo "报表图片下载失败"

# 表单示例
echo "下载表单示例..."
curl -L -o "${BASE_DIR}/forms/sample_form.png" \
  "https://github.com/tesseract-ocr/tesseract/raw/main/test/testing/eurotext.tif" 2>/dev/null || \
echo "表单图片下载失败"

# 收据示例
echo "下载收据示例..."
curl -L -o "${BASE_DIR}/receipts/sample_receipt.png" \
  "https://github.com/mindee/invoices-dataset/raw/main/samples/receipt.png" 2>/dev/null || \
echo "收据图片下载失败"

echo "下载完成！"

