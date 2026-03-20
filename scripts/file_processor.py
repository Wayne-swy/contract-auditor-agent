#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同文件处理器
支持多种文件格式的文本提取：PDF, Word, 图片 (OCR)
"""

import os
import sys
from pathlib import Path

# 可选依赖，使用时检查
def check_dependencies():
    """检查并安装必要的依赖"""
    missing = []

    try:
        import PIL
    except ImportError:
        missing.append("Pillow")

    try:
        import pdf2image
    except ImportError:
        missing.append("pdf2image")

    try:
        import docx
    except ImportError:
        missing.append("python-docx")

    try:
        import pytesseract
    except ImportError:
        missing.append("pytesseract")

    try:
        import easyocr
    except ImportError:
        missing.append("easyocr")

    return missing

def extract_from_pdf(pdf_path):
    """从 PDF 文件提取文本"""
    try:
        # 方法 1: 尝试提取文本型 PDF
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"PDF 文本提取失败：{e}")

    # 方法 2: 如果是扫描版 PDF，转为图片后 OCR
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=300)
        text = ""
        for img in images:
            text += ocr_from_image(img) + "\n"
        return text
    except ImportError:
        print("错误：需要安装 pdf2image 和 pdfplumber 来处理 PDF 文件")
        print("运行：pip install pdfplumber pdf2image")
        return None
    except Exception as e:
        print(f"PDF OCR 处理失败：{e}")
        return None

def extract_from_docx(docx_path):
    """从 Word 文档提取文本"""
    try:
        from docx import Document
        doc = Document(docx_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except ImportError:
        print("错误：需要安装 python-docx 来处理 Word 文件")
        print("运行：pip install python-docx")
        return None
    except Exception as e:
        print(f"Word 文件处理失败：{e}")
        return None

def ocr_from_image(image_path):
    """从图片进行 OCR 识别"""
    text = ""

    # 方法 1: 使用 EasyOCR (推荐，支持中文)
    try:
        import easyocr
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        results = reader.readtext(str(image_path))
        for (_, _, text_part) in results:
            text += text_part + "\n"
        if text.strip():
            return text
    except ImportError:
        print("EasyOCR 未安装，尝试备用方案...")
    except Exception as e:
        print(f"EasyOCR 识别失败：{e}")

    # 方法 2: 使用 pytesseract
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        # 中文 + 英文
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        return text
    except ImportError:
        print("错误：需要安装 OCR 引擎")
        print("选项 1 (推荐): pip install easyocr")
        print("选项 2: 安装 Tesseract-OCR 和 pytesseract")
        print("  - Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装")
        print("  - 然后：pip install pytesseract")
        return None
    except Exception as e:
        print(f"pytesseract 识别失败：{e}")
        return None

def extract_from_image(image_path):
    """从图片文件提取文本"""
    from pathlib import Path

    # 如果是 PIL Image 对象
    try:
        from PIL import Image
        if isinstance(image_path, Image.Image):
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                image_path.save(f.name)
                temp_path = f.name
            text = ocr_from_image(temp_path)
            os.unlink(temp_path)
            return text
    except:
        pass

    # 如果是文件路径
    return ocr_from_image(image_path)

def process_file(file_path):
    """
    处理上传的文件，提取文本内容

    Args:
        file_path: 文件路径

    Returns:
        str: 提取的文本内容
    """
    path = Path(file_path)

    if not path.exists():
        return f"错误：文件不存在 - {file_path}"

    ext = path.suffix.lower()

    # 支持的格式和对应处理函数
    handlers = {
        # 图片格式
        '.jpg': extract_from_image,
        '.jpeg': extract_from_image,
        '.png': extract_from_image,
        '.gif': extract_from_image,
        '.bmp': extract_from_image,
        '.webp': extract_from_image,
        '.tiff': extract_from_image,
        '.tif': extract_from_image,
        # PDF
        '.pdf': extract_from_pdf,
        # Word
        '.docx': extract_from_docx,
        '.doc': extract_from_docx,  # 旧版 Word 可能需要额外处理
        # 纯文本
        '.txt': lambda p: open(p, 'r', encoding='utf-8').read(),
        '.md': lambda p: open(p, 'r', encoding='utf-8').read(),
    }

    handler = handlers.get(ext)
    if handler is None:
        return f"不支持的文件格式：{ext}\n支持的格式：图片 (jpg/png/gif/bmp/webp/tiff), PDF, Word(docx/doc), 文本 (txt/md)"

    print(f"正在处理文件：{file_path}")
    text = handler(file_path)

    if text and text.strip():
        print(f"成功提取 {len(text)} 字符")
        return text
    else:
        return "未能从文件中提取到文本内容"

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python file_processor.py <文件路径>")
        print("支持的格式：图片 (jpg/png/gif/bmp), PDF, Word(docx), 文本 (txt/md)")
        sys.exit(1)

    file_path = sys.argv[1]
    text = process_file(file_path)

    if text and not text.startswith("错误"):
        print("\n" + "=" * 50)
        print("提取的文本内容:")
        print("=" * 50)
        print(text)
    else:
        print(f"\n{text}")

if __name__ == "__main__":
    main()
