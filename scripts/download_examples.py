#!/usr/bin/env python3
"""
下载复杂场景的OCR示例图片脚本
从公开数据集和资源下载发票、报表、表单、收据等示例图片
"""

import urllib.request
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / "assets" / "examples"

# 示例图片URL列表（使用公开可用的资源）
EXAMPLES = {
    "invoices": [
        {
            "name": "complex_invoice.png",
            "url": "https://raw.githubusercontent.com/mindee/doctr/main/docs/source/_static/sample_invoice.png",
            "description": "复杂发票示例"
        },
        {
            "name": "multi_page_invoice.png", 
            "url": "https://github.com/tesseract-ocr/tesseract/raw/main/test/testing/phototest.tif",
            "description": "多页发票示例"
        }
    ],
    "receipts": [
        {
            "name": "complex_receipt.png",
            "url": "https://raw.githubusercontent.com/mindee/doctr/main/docs/source/_static/sample_receipt.png",
            "description": "复杂收据示例"
        }
    ],
    "reports": [
        {
            "name": "financial_report.png",
            "url": "https://github.com/tesseract-ocr/tesseract/raw/main/test/testing/eurotext.tif",
            "description": "财务报表示例"
        }
    ],
    "forms": [
        {
            "name": "application_form.png",
            "url": "https://github.com/tesseract-ocr/tesseract/raw/main/test/testing/eurotext.tif",
            "description": "申请表示例"
        }
    ]
}

def download_file(url, dest_path):
    """下载文件"""
    try:
        print(f"  📥 下载 {dest_path.name}...")
        urllib.request.urlretrieve(url, str(dest_path))
        size = dest_path.stat().st_size
        print(f"  ✅ 成功 ({size:,} bytes)")
        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False

def generate_ocr_result(image_path):
    """为图片生成OCR识别结果"""
    result_path = image_path.with_suffix('.txt')
    if result_path.exists():
        print(f"  ⏭️  OCR结果已存在: {result_path.name}")
        return
    
    print(f"  🔍 生成OCR识别结果...")
    cmd = f"""deepseek-ocr-cli \
  --image "{image_path}" \
  --prompt "<image>\\n<|grounding|>Extract all text from this document." \
  --max-new-tokens 2048 \
  2>/dev/null > "{result_path}" """
    
    import subprocess
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=Path(__file__).parent.parent)
        if result_path.exists() and result_path.stat().st_size > 0:
            print(f"  ✅ OCR结果已生成: {result_path.name}")
        else:
            print(f"  ⚠️  OCR结果为空")
    except Exception as e:
        print(f"  ❌ OCR生成失败: {e}")

def main():
    """主函数"""
    print("🚀 开始下载示例图片...\n")
    
    downloaded = 0
    skipped = 0
    
    for category, items in EXAMPLES.items():
        print(f"📁 {category.upper()}/")
        cat_dir = BASE_DIR / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        for item in items:
            dest_path = cat_dir / item["name"]
            
            if dest_path.exists():
                print(f"  ⏭️  {item['name']} 已存在，跳过")
                skipped += 1
            else:
                if download_file(item["url"], dest_path):
                    downloaded += 1
                    
                    # 生成OCR结果
                    generate_ocr_result(dest_path)
        
        print()
    
    # 如果没有下载到任何文件，尝试使用现有文件
    if downloaded == 0:
        print("⚠️  未能从网络下载文件，使用现有文件...")
        existing = BASE_DIR / "invoices" / "vat_invoice.png"
        if existing.exists():
            print(f"📄 使用现有文件: {existing.name}")
            generate_ocr_result(existing)
    
    print(f"\n✅ 完成！")
    print(f"   - 下载: {downloaded} 个文件")
    print(f"   - 跳过: {skipped} 个文件")
    
    # 列出所有文件
    print(f"\n📋 当前示例文件:")
    for category in ["invoices", "reports", "forms", "receipts"]:
        cat_dir = BASE_DIR / category
        if cat_dir.exists():
            files = list(cat_dir.glob("*"))
            if files:
                print(f"  {category}/: {len(files)} 个文件")
                for f in sorted(files):
                    size = f.stat().st_size
                    print(f"    - {f.name} ({size:,} bytes)")

if __name__ == "__main__":
    main()

