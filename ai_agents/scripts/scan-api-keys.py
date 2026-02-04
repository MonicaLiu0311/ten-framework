#!/usr/bin/env python3
"""
API Keys Security Scanner
扫描项目中可能存在的 API 密钥和敏感信息
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# 定义要检查的模式
PATTERNS = {
    'OpenAI API Key': r'sk-[a-zA-Z0-9]{32,}',
    'Agora App ID': r'AGORA_APP_ID\s*=\s*["\']?[a-z0-9]{32}',
    'Agora Certificate': r'AGORA_APP_CERTIFICATE\s*=\s*["\']?[a-z0-9]{32}',
    'Generic API Key': r'["\']api[_-]?key["\']\s*:\s*["\'][^"\']{20,}',
    'Bearer Token': r'Bearer\s+[a-zA-Z0-9_\-\.]{20,}',
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'Private Key': r'-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----',
}

# 要跳过的目录
SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', 'venv', '.venv', 
    'dist', 'build', '.next', 'target', 'vendor'
}

# 要跳过的文件扩展名
SKIP_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.ico', '.svg',
    '.woff', '.woff2', '.ttf', '.eot', '.otf',
    '.mp3', '.mp4', '.wav', '.avi', '.mov',
    '.zip', '.tar', '.gz', '.rar',
    '.exe', '.dll', '.so', '.dylib',
    '.pyc', '.pyo', '.class',
}

def should_skip(path: Path) -> bool:
    """判断是否应该跳过此路径"""
    # 跳过目录
    if any(skip_dir in path.parts for skip_dir in SKIP_DIRS):
        return True
    
    # 跳过扩展名
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    
    # 跳过 .env.example 文件（这些是模板）
    if path.name.endswith('.env.example'):
        return True
        
    return False

def scan_file(file_path: Path) -> List[Tuple[str, int, str]]:
    """扫描单个文件，返回发现的问题列表"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern_name, pattern in PATTERNS.items():
                    if re.search(pattern, line):
                        # 脱敏显示
                        sanitized_line = line.strip()
                        if len(sanitized_line) > 100:
                            sanitized_line = sanitized_line[:100] + '...'
                        issues.append((pattern_name, line_num, sanitized_line))
    except Exception as e:
        print(f"⚠️  无法读取文件 {file_path}: {e}", file=sys.stderr)
    
    return issues

def scan_directory(root_dir: Path) -> dict:
    """扫描目录，返回所有发现的问题"""
    all_issues = {}
    
    for root, dirs, files in os.walk(root_dir):
        # 修改 dirs 列表以跳过某些目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_skip(file_path):
                continue
            
            issues = scan_file(file_path)
            if issues:
                rel_path = file_path.relative_to(root_dir)
                all_issues[rel_path] = issues
    
    return all_issues

def main():
    """主函数"""
    print("🔍 API 密钥安全扫描器")
    print("=" * 60)
    
    # 获取项目根目录
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path.cwd()
    
    if not root_dir.exists():
        print(f"❌ 错误: 目录不存在: {root_dir}")
        sys.exit(1)
    
    print(f"扫描目录: {root_dir}")
    print()
    
    # 扫描
    all_issues = scan_directory(root_dir)
    
    # 报告结果
    if not all_issues:
        print("✅ 未发现明显的安全问题")
        return 0
    
    print(f"⚠️  发现 {len(all_issues)} 个文件包含潜在的敏感信息：")
    print()
    
    for file_path, issues in all_issues.items():
        print(f"📄 {file_path}")
        for pattern_name, line_num, line in issues:
            print(f"   第 {line_num} 行: {pattern_name}")
            # 不显示完整内容以避免泄露
            print(f"   预览: {line[:50]}...")
        print()
    
    print("=" * 60)
    print(f"总计: {sum(len(issues) for issues in all_issues.values())} 个潜在问题")
    print()
    print("⚠️  请检查这些文件并移除任何真实的 API 密钥")
    print("📚 参考文档: ai_agents/API_KEYS_SECURITY_GUIDE.zh-CN.md")
    
    return 1

if __name__ == '__main__':
    sys.exit(main())
