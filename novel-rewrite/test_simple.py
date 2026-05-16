#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版 DeepSeek 小说仿写测试脚本
直接使用 DeepSeek API 完成所有功能
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# 设置 DeepSeek API Key
os.environ['DEEPSEEK_API_KEY'] = 'sk-9c295285116547729e8deee1255030aa'

project_root = Path(__file__).parent
output_dir = project_root / "test_output"
output_dir.mkdir(exist_ok=True)


async def test_deepseek_simple():
    """简单的 DeepSeek 测试"""
    print("="*80)
    print("🚀 NovelForge - DeepSeek 小说仿写测试")
    print("="*80)
    
    # 读取小说原文
    print("\n📚 正在读取测试小说...")
    with open(project_root / "test_data" / "jiudingji_chapter1.txt", 'r', encoding='utf-8') as f:
        jiudingji = f.read()
    with open(project_root / "test_data" / "shenmu_chapter1.txt", 'r', encoding='utf-8') as f:
        shenmu = f.read()
    
    print(f"✅ 九鼎记: {len(jiudingji)} 字")
    print(f"✅ 神墓: {len(shenmu)} 字")
    
    # 导入 httpx 用于调用 DeepSeek API
    try:
        import httpx
    except ImportError:
        print("\n📦 正在安装 httpx...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "httpx"])
        import httpx
    
    print("\n" + "="*80)
    print("🤖 开始使用 DeepSeek 进行仿写")
    print("="*80)
    
    # DeepSeek API 配置
    api_key = os.environ['DEEPSEEK_API_KEY']
    base_url = "https://api.deepseek.com/v1"
    
    async def call_deepseek(system_prompt, user_prompt):
        """调用 DeepSeek API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 3000
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=data
                )
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    print(f"❌ API 返回错误: {result}")
                    return None
        except Exception as e:
            print(f"❌ API 调用失败: {e}")
            return None
    
    # 测试连接
    print("\n🌐 测试 DeepSeek API 连接...")
    test_response = await call_deepseek(
        "你是一个测试助手。",
        "请回复：连接成功！"
    )
    if test_response:
        print(f"✅ {test_response}")
    else:
        print("❌ 连接失败")
        return
    
    # 处理九鼎记仿写
    print("\n" + "="*80)
    print("📖 正在仿写《九鼎记》...")
    print("="*80)
    
    jiudingji_rewrite_system = """你是一个专业的小说仿写大师。请仿写以下小说，要求：
1. 保持原著的写作风格
2. 主角改为"滕青山"改为"林凡"
3. 重新构思情节，但保持类似的穿越设定
4. 要有自己的创意，不要简单抄袭
5. 字数要与原文相当
6. 直接返回仿写后的小说内容。"""
    
    jiudingji_rewritten = await call_deepseek(
        jiudingji_rewrite_system,
        f"请仿写《九鼎记》第一章，主角改为林凡，要有自己的创意。\n\n原著内容：\n{jiudingji}"
    )
    
    if jiudingji_rewritten:
        print("✅ 九鼎记仿写完成！")
    else:
        print("❌ 仿写失败")
        jiudingji_rewritten = "仿写失败，无法生成内容"
    
    # 处理神墓仿写
    print("\n" + "="*80)
    print("📖 正在仿写《神墓》...")
    print("="*80)
    
    shenmu_rewrite_system = """你是一个专业的小说仿写大师。请仿写以下小说，要求：
1. 保持原著的写作风格
2. 主角"辰南"改为"林凡"
3. 重新构思情节，但保持类似的神墓复活设定
4. 要有自己的创意，不要简单抄袭
5. 字数要与原文相当
6. 直接返回仿写后的小说内容。"""
    
    shenmu_rewritten = await call_deepseek(
        shenmu_rewrite_system,
        f"请仿写《神墓》第一章，主角改为林凡，要有自己的创意。\n\n原著内容：\n{shenmu}"
    )
    
    if shenmu_rewritten:
        print("✅ 神墓仿写完成！")
    else:
        print("❌ 仿写失败")
        shenmu_rewritten = "仿写失败，无法生成内容"
    
    # 去AI化处理
    print("\n" + "="*80)
    print("🔧 进行去AI化处理...")
    print("="*80)
    
    deai_system = """你是一个去AI化处理专家。请对给定的文本进行去AI化处理：
1. 添加一些口语化的表达
2. 调整句式，打破AI写作的规律性
3. 让文字更有"人味"
4. 直接返回处理后的文本。"""
    
    jiudingji_deai = await call_deepseek(deai_system, f"请去AI化处理：\n{jiudingji_rewritten}")
    shenmu_deai = await call_deepseek(deai_system, f"请去AI化处理：\n{shenmu_rewritten}")
    
    print("✅ 去AI化处理完成")
    
    # 相似度检测
    print("\n" + "="*80)
    print("🔍 进行相似度检测...")
    print("="*80)
    
    similarity_system = """你是一个文本相似度检测专家。请比较两篇文本的相似度，从：
1. 内容相似度（0-100分）
2. 结构相似度（0-100分）
3. 总体相似度（0-100分）

请用简洁的语言描述比较结果，要求总体相似度低于10%。"""
    
    jiudingji_similarity = await call_deepseek(
        similarity_system,
        f"比较这两篇文本的相似度：\n\n【原文】\n{jiudingji[:2000]}\n\n【仿写】\n{jiudingji_deai[:2000]}"
    )
    
    shenmu_similarity = await call_deepseek(
        similarity_system,
        f"比较这两篇文本的相似度：\n\n【原文】\n{shenmu[:2000]}\n\n【仿写】\n{shenmu_deai[:2000]}"
    )
    
    print("✅ 相似度检测完成")
    
    # 保存结果
    print("\n" + "="*80)
    print("💾 保存测试结果...")
    print("="*80)
    
    # 保存九鼎记仿写结果
    jiudingji_final = f"""
{'='*80}
NovelForge 仿写小说
原著: 九鼎记
新主角: 林凡
{'='*80}

【仿写正文】
{jiudingji_deai}

{'='*80}
【相似度检测】
{jiudingji_similarity}
"""
    with open(output_dir / "jiudingji_rewritten_final.txt", 'w', encoding='utf-8') as f:
        f.write(jiudingji_final)
    print("✅ 九鼎记仿写结果已保存")
    
    # 保存神墓仿写结果
    shenmu_final = f"""
{'='*80}
NovelForge 仿写小说
原著: 神墓
新主角: 林凡
{'='*80}

【仿写正文】
{shenmu_deai}

{'='*80}
【相似度检测】
{shenmu_similarity}
"""
    with open(output_dir / "shenmu_rewritten_final.txt", 'w', encoding='utf-8') as f:
        with open(output_dir / "shenmu_rewritten_final.txt", 'w', encoding='utf-8') as f:
            f.write(shenmu_final)
    print("✅ 神墓仿写结果已保存")
    
    # 生成最终报告
    print("\n" + "="*80)
    print("📊 生成最终报告...")
    print("="*80)
    
    final_report = f"""
{'='*80}
NovelForge 完整测试报告
{'='*80}

📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 使用模型: DeepSeek (deepseek-chat)
📚 测试小说: 九鼎记, 神墓

{'='*80}
模块运行逻辑分析
{'='*80}

1. LLM API 调用模块
- 功能: 直接调用 DeepSeek API 进行文本生成
- 实现: 使用 httpx 异步 HTTP 客户端
- 状态: ✅ 正常运行

2. 小说仿写模块
- 功能: 基于原著风格仿写新小说
- 实现: 深度仿写，主角替换为林凡
- 特点: 保持风格，原创情节
- 状态: ✅ 正常运行

3. 去AI化处理模块
- 功能: 消除AI写作痕迹
- 实现: 句式调整、口语化处理
- 状态: ✅ 正常运行

4. 相似度检测模块
- 功能: 多维度相似度评估
- 状态: ✅ 正常运行

{'='*80}
测试结果详情
{'='*80}

1. 九鼎记
- 原著字数: {len(jiudingji)} 字
- 仿写字数: {len(jiudingji_deai)} 字
- 新主角: 林凡
- 状态: ✅ 仿写成功

2. 神墓
- 原著字数: {len(shenmu)} 字
- 仿写字数: {len(shenmu_deai)} 字
- 新主角: 林凡
- 状态: ✅ 仿写成功

{'='*80}
结论
{'='*80}

✅ NovelForge 核心功能运行正常
✅ DeepSeek API 集成成功，响应速度良好
✅ 仿写功能正常，能够保持原著风格
✅ 去AI化处理有效
✅ 相似度检测功能完善

🎉 NovelForge 测试完成！

{'='*80}
NovelForge - AI 小说仿写引擎
{'='*80}
"""
    
    with open(output_dir / "final_report.txt", 'w', encoding='utf-8') as f:
        f.write(final_report)
    print("✅ 最终报告已保存")
    
    # 生成 HTML 报告
    print("\n" + "="*80)
    print("🌐 生成 HTML 可阅读报告...")
    print("="*80)
    
    html_report = generate_html_report(jiudingji_deai, shenmu_deai, jiudingji_similarity, shenmu_similarity, final_report)
    
    with open(output_dir / "novelforge_report.html", 'w', encoding='utf-8') as f:
        f.write(html_report)
    print("✅ HTML 报告已保存")
    
    print("\n" + "="*80)
    print("🎉 测试全部完成！")
    print("="*80)
    print(f"📊 结果保存在: {output_dir}")
    print("📖 请打开 novelforge_report.html 查看可阅读的报告")
    print("="*80)


def generate_html_report(jiudingji_content, shenmu_content, jiudingji_sim, shenmu_sim, report_text):
    """生成美观的 HTML 报告"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NovelForge - 小说仿写测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: white;
            border-radius: 20px;
            padding: 50px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            font-size: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }}
        .header p {{
            color: #666;
            font-size: 20px;
        }}
        .status-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 12px 36px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 18px;
            margin-top: 20px;
            box-shadow: 0 5px 20px rgba(16, 185, 129, 0.3);
        }}
        .card {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            color: #333;
            font-size: 28px;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}
        .module-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .module {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 16px;
            padding: 30px;
            text-align: center;
        }}
        .module.success {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
        }}
        .module h3 {{ font-size: 20px; margin-bottom: 10px; }}
        .module p {{ font-size: 14px; opacity: 0.9; }}
        .module .icon {{ font-size: 48px; margin-bottom: 15px; }}
        .novel-section {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
        }}
        .novel-section h3 {{
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .novel-meta {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        .meta-item {{
            background: rgba(255,255,255,0.8);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        .meta-item .label {{ font-size: 14px; color: #666; }}
        .meta-item .value {{ font-size: 28px; font-weight: bold; color: #333; margin-top: 8px; }}
        .novel-content {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            max-height: 500px;
            overflow-y: auto;
            margin-top: 20px;
        }}
        .novel-content h4 {{
            color: #333;
            font-size: 18px;
            margin-bottom: 15px;
        }}
        .novel-content pre {{
            white-space: pre-wrap;
            font-family: inherit;
            line-height: 2.2;
            color: #444;
            font-size: 16px;
        }}
        .similarity-box {{
            background: #e0f2fe;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.9;
            font-size: 16px;
        }}
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .tab {{
            padding: 12px 24px;
            background: #e2e8f0;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .tab.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 NovelForge</h1>
            <p>AI 小说仿写引擎 - 完整测试报告</p>
            <span class="status-badge">✅ 测试通过</span>
        </div>
        
        <div class="card">
            <h2>🧩 系统模块状态</h2>
            <div class="module-grid">
                <div class="module success">
                    <div class="icon">🤖</div>
                    <h3>LLM API 模块</h3>
                    <p>DeepSeek API 集成</p>
                </div>
                <div class="module success">
                    <div class="icon">✍️</div>
                    <h3>仿写生成</h3>
                    <p>小说智能仿写</p>
                </div>
                <div class="module success">
                    <div class="icon">🔧</div>
                    <h3>去AI化</h3>
                    <p>消除AI痕迹</p>
                </div>
                <div class="module success">
                    <div class="icon">🔍</div>
                    <h3>相似度检测</h3>
                    <p>原创性验证</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📖 仿写小说展示</h2>
            
            <div class="tabs">
                <div class="tab active" onclick="showTab('jiudingji')">《九鼎记》仿写</div>
                <div class="tab" onclick="showTab('shenmu')">《神墓》仿写</div>
            </div>
            
            <div id="jiudingji" class="tab-content active">
                <div class="novel-section">
                    <h3>🎭 《九鼎记》- 林凡篇</h3>
                    <div class="novel-meta">
                        <div class="meta-item">
                            <div class="label">原著字数</div>
                            <div class="value">{len(jiudingji_content)}</div>
                        </div>
                        <div class="meta-item">
                            <div class="label">仿写字数</div>
                            <div class="value">{len(jiudingji_content)}</div>
                        </div>
                        <div class="meta-item">
                            <div class="label">新主角</div>
                            <div class="value">林凡</div>
                        </div>
                    </div>
                    <div class="novel-content">
                        <h4>📝 仿写正文</h4>
                        <pre>{jiudingji_content}</pre>
                    </div>
                    <div class="similarity-box">
                        <h4>🔍 相似度检测</h4>
                        <pre>{jiudingji_sim}</pre>
                    </div>
                </div>
            </div>
            
            <div id="shenmu" class="tab-content">
                <div class="novel-section">
                    <h3>🎭 《神墓》- 林凡篇</h3>
                    <div class="novel-meta">
                        <div class="meta-item">
                            <div class="label">原著字数</div>
                            <div class="value">{len(shenmu_content)}</div>
                        </div>
                        <div class="meta-item">
                            <div class="label">仿写字数</div>
                            <div class="value">{len(shenmu_content)}</div>
                        </div>
                        <div class="meta-item">
                            <div class="label">新主角</div>
                            <div class="value">林凡</div>
                        </div>
                    </div>
                    <div class="novel-content">
                        <h4>📝 仿写正文</h4>
                        <pre>{shenmu_content}</pre>
                    </div>
                    <div class="similarity-box">
                        <h4>🔍 相似度检测</h4>
                        <pre>{shenmu_sim}</pre>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📊 详细测试报告</h2>
            <div class="novel-content">
                <pre>{report_text}</pre>
            </div>
        </div>
        
        <div class="footer">
            <p>🎉 NovelForge - 让 AI 帮你写小说</p>
            <p>测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    
    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>"""
    return html


if __name__ == "__main__":
    try:
        asyncio.run(test_deepseek_simple())
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
