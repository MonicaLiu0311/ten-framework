#!/bin/bash
# API Keys Security Check Script
# 检查是否有 API 密钥被意外包含在要提交的文件中

set -e

echo "🔐 检查 API 密钥安全..."

# 定义要检查的模式
PATTERNS=(
    "sk-[a-zA-Z0-9]{32,}"                    # OpenAI-like keys
    "AGORA_APP_ID=['\"]?[a-z0-9]{32}"        # Agora App ID
    "AGORA_APP_CERTIFICATE=['\"]?[a-z0-9]"   # Agora Certificate  
    "['\"]api[_-]?key['\"]?\s*[:=]\s*['\"][^'\"]{20,}"  # Generic API keys
    "Bearer [a-zA-Z0-9_\-\.]{20,}"           # Bearer tokens
    "password['\"]?\s*[:=]\s*['\"][^'\"]{8,}" # Passwords
)

# 检查暂存的文件
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo "✅ 没有暂存的文件"
    exit 0
fi

echo "检查文件："
echo "$STAGED_FILES" | sed 's/^/  - /'
echo ""

FOUND_ISSUES=0

# 检查每个文件
for file in $STAGED_FILES; do
    if [ -f "$file" ]; then
        # 跳过某些文件类型
        if [[ "$file" =~ \.(jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ ]]; then
            continue
        fi
        
        # 检查每个模式
        for pattern in "${PATTERNS[@]}"; do
            matches=$(grep -nE "$pattern" "$file" 2>/dev/null || true)
            if [ ! -z "$matches" ]; then
                echo "⚠️  发现潜在的 API 密钥在: $file"
                echo "$matches" | head -3 | sed 's/^/     /'
                FOUND_ISSUES=1
            fi
        done
    fi
done

# 特别检查 .env 文件
if echo "$STAGED_FILES" | grep -qE "\.env$" && ! echo "$STAGED_FILES" | grep -qE "\.env\.example$"; then
    echo "❌ 错误: 尝试提交 .env 文件！"
    echo "   .env 文件不应该被提交到 git"
    echo "   请将其添加到 .gitignore 并使用 .env.example 代替"
    FOUND_ISSUES=1
fi

echo ""

if [ $FOUND_ISSUES -eq 1 ]; then
    echo "❌ 检测到潜在的安全问题！"
    echo ""
    echo "建议："
    echo "  1. 检查标记的内容是否为真实的 API 密钥"
    echo "  2. 如果是密钥，请从文件中移除"
    echo "  3. 使用环境变量或 .env 文件（不要提交）"
    echo "  4. 如果这是误报，可以使用 --no-verify 跳过检查（不推荐）"
    echo ""
    echo "参考文档: ai_agents/API_KEYS_SECURITY_GUIDE.zh-CN.md"
    echo ""
    exit 1
else
    echo "✅ 未发现明显的安全问题"
    exit 0
fi
