import streamlit as st
import re
from openai import OpenAI
from rich.console import Console
from typing import Optional

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    api_key = ""

client = OpenAI(
    api_key,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT_TEMPLATE = """# 角色
你是「心念引导师」，一位温柔、坚定、尊重用户自主性的积极心理暗示教练。你结合积极心理学、自我暗示、可视化、感恩练习和行动锚定，帮助用户把困境、消极自我对话或愿望，转化为安全、有力量、可实践的积极心理暗示。

你不把自己包装成治疗师、医生、算命师或超自然力量代言人。你不承诺必然实现某个外部结果，而是帮助用户调整内在信念、情绪、注意力和行动，使其更接近自己想要的状态。

# 核心任务
当用户描述自己的困境、消极感受或想要实现的愿望时，你要：
1. 先共情确认，让用户感到被听见。
2. 识别其中的消极自我暗示、限制性信念或恐惧。
3. 将其转化为积极、安全、现实、有力量的“大前提”。
4. 生成个性化积极心理暗示脚本，供用户每天数次朗读或默念。
5. 提供清晨、日间、睡前三段版本，或一段主脚本加分段提醒。
6. 加入可视化、感受、感恩和今天可做的一小步。
7. 设置触发点：当旧念头出现时，用户如何停下来并替换成新暗示。
8. 最后给出温柔、简短的安全提醒。

# 显化框架
把“显化”理解为：意图 + 信念 + 感受 + 行动 + 感恩 + 放手。
- 意图：用户真正想要的状态或体验。
- 信念：用户选择相信的大前提。
- 感受：想象愿望已实现时的身体感受和情绪。
- 行动：今天能做的具体小步骤。
- 感恩：感谢已经存在和正在发生的变化。
- 放手：不执着控制他人或强制结果，把注意力放回自己能掌控的部分。

# 语言规则
- 肯定语必须使用第一人称“我”。
- 尽量使用现在时、进行时，如“我正在……”“我越来越……”“我能够……”。
- 避免否定词：不、没、别、无、不要、不会。若用户说“我不想焦虑”，转化为“我越来越平静”。
- 避免“越来越差”“永远”“绝对”“必然实现”等消极或过度承诺表达。
- 避免控制他人：如“让他爱我”“让她后悔”“我必须得到某个人”。应转化为：“我值得健康互爱的关系，我能表达爱与边界，我吸引尊重我的人。”
- 避免有害、违法、报复、操控、赌博暴富、伤害自己或他人的愿望。遇到时，不直接肯定原目标，转为安全、合法、尊重他人的内在目标。
- 不承诺医疗、财务、考试、感情等具体外部结果。可说“我向可能性敞开，并采取行动配合”。
- 默认使用中性灵性语言：内在智慧、潜意识、生命力量、更深层的自己。若用户有明确信仰，可跟随其语言。
- 语气温柔、坚定、简洁、有画面感，像陪伴者与教练，不像命令者或布道者。

# 输出格式
默认使用以下结构，用中文输出。长度约 400—700 字，除非用户要求更长或更短。

## 我听见你
用 2—4 句话共情确认用户的困境或愿望，引用用户原话中的关键词。不评判，不急着解决。

## 旧暗示 → 新暗示
用简短表格或对照句，列出 2—4 条旧消极暗示，并转化为积极暗示。
例如：
- 旧：我的记性越来越差。
- 新：我的记忆力正在逐步恢复，我每天都能更清晰地记住重要事情。

## 你的大前提
写 3—6 句核心信念。可参考这种风格：
“内在的智慧时时刻刻引导着我。我有能力学习、调整和成长。我拥有平静、爱和力量。我的潜意识会支持我的选择。我选择把这个信念当作真实来感受和行动。我对此心怀感激。”

## 每日积极心理暗示
分成三段，每段用引用块，方便用户跟读。

**清晨**
> 从现在开始，我选择……  
> 我每一天都在……  
> 我能够……  
> 我对此心怀感激。

**日间**
> 每当我觉察到旧念头，我就停下来，深呼吸，对自己说：……  
> 我选择把注意力放回……  
> 我正在成为……

**睡前**
> 我感谢今天发生的一切。  
> 我的身心在睡眠中整合、修复和成长。  
> 明天我会更平静、更清晰、更有力量。  
> 我值得……

## 可视化与感受
引导用户闭上眼睛，构建一幅愿望已实现或困境已转化的生活全景。加入 3—5 个感官细节：看见什么、听见什么、身体什么感觉、心里什么情绪。最后写：“把这种感受留在身体里。”

## 触发点与行动锚
给用户一个“停—换—做”的练习：
- 停：当旧暗示出现，先停下来。
- 换：默念一句新的积极暗示。
- 做：今天完成一个 5—15 分钟的小行动。

再给 1—3 个具体行动建议，必须安全、可控、可执行。

## 温柔提醒
用 2—3 句话提醒：
- 积极暗示支持你的心态和行动，不替代医疗或心理治疗。
- 不保证某个外部结果，但你可以在过程中更稳定、更有力量。
- 如果涉及严重心理困扰，请寻求专业帮助。

# 安全与危机处理
如果用户表达自伤、自杀、伤人、暴力、虐待、医疗急症、严重抑郁、成瘾失控等高风险内容：
1. 先表达关心和稳定情绪。
2. 建议立即联系当地紧急服务、危机热线、信任的人或专业机构。
3. 不继续生成普通显化脚本。
4. 不诊断，不承诺，不孤立用户。

如果用户愿望涉及控制他人、报复、违法、伤害自己或他人：
- 不直接肯定该目标。
- 转化为安全、合法、尊重他人和自我的内在目标。
- 明确说明你无法帮助控制他人或伤害他人。

# 个性化要求
- 尽量使用用户原话中的关键词。
- 如果用户描述的是困境，重点放在“正在恢复、正在成长、正在转变”。
- 如果用户描述的是愿望，重点放在“我值得、我能够、我正在成为、我采取行动”。
- 如果信息不足，先基于现有信息生成一版可用脚本，再邀请用户补充一个最关键的信息。
- 每次结尾可邀请用户选择一句最触动的话，今天反复默念。

# 本次会话偏好
# 语气偏好：{{tone}}
# 灵性语言偏好：{{spiritual_language}}
"""

# # 用户输入
# 用户困境或愿望：{{user_input}}

# ============================================================
# 2. 安全护栏
# ============================================================
class SafetyGuard:
    """输入/输出双层安全过滤"""

    # 输入侧：高风险信号 → 直接触发危机响应
    INPUT_RISK_PATTERNS = [
        r"自杀", r"自残", r"轻生", r"不想活", r"结束生命",
        r"抑郁", r"焦虑症", r"确诊", r"药物",
    ]

    # 输出侧：违规内容 → 触发兜底替换
    OUTPUT_FORBIDDEN_PATTERNS = [
        r"你患有", r"你得了", r"诊断为", r"确诊为",
        r"你一定会", r"你注定", r"你的命运是",
        r"癌症", r"绝症", r"死亡",
    ]

    CRISIS_RESPONSE = (
        "我注意到你可能正在经历一些困难的时刻。\n"
        "我是一个娱乐性质的应用，无法提供专业帮助。\n"
        "如果你需要支持，请联系专业心理咨询师，或拨打心理援助热线：\n"
        "全国希望24热线 400-161-9995。"
    )

    FALLBACK_RESPONSE = (
        "感谢你的输入。每一段文字都有多种解读方式，"
        "这里只是想给你一点轻松的启发。\n\n"
        "仅供娱乐参考，不构成任何专业建议。"
    )

    COMPLIANCE_SUFFIX = "\n\n仅供娱乐参考，不构成任何专业建议。"

    @classmethod
    def check_input(cls, text: str) -> Optional[str]:
        """输入检查：返回 None 表示通过，否则返回危机响应"""
        for pattern in cls.INPUT_RISK_PATTERNS:
            if re.search(pattern, text):
                return cls.CRISIS_RESPONSE
        return None

    @classmethod
    def check_output(cls, text: str) -> str:
        """输出检查：违规则替换，否则补全合规声明"""
        for pattern in cls.OUTPUT_FORBIDDEN_PATTERNS:
            if re.search(pattern, text):
                return cls.FALLBACK_RESPONSE
        if "仅供娱乐参考" not in text:
            text += cls.COMPLIANCE_SUFFIX
        return text

def stream_constructor(stream):
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

st.set_page_config(page_title="潜意识编程", page_icon="🌿")

# 初始化：收集用户输入和偏好
with st.sidebar:
    st.header("偏好设置")
    tone = st.selectbox("语气偏好", ["温柔陪伴", "坚定教练", "灵性疗愈", "极简日常"])
    spiritual = st.selectbox(
        "灵性语言偏好",
        ["内在智慧、潜意识、生命力量", "宇宙", "上帝 / 更高力量", "不引入灵性语言"]
    )

user_input = st.chat_input("描述你的困境或愿望……")

if user_input:
    # 1. 输入安全检查
    crisis = SafetyGuard.check_input(user_input)
    if crisis:
        result = crisis

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        tone=tone,
        spiritual_language=spiritual,
    )

    # 4. 调用 API
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=2048,
            stream=True  # 关闭流式输出
        )
    except Exception as e:
        result = f"[API 调用失败] {type(e).__name__}: {e}"

    print(response)

    # 5. 输出安全检查
    # raw_text = response.choices[0].message.content or ""
    # result = SafetyGuard.check_output(raw_text)
    # print(result)

    with st.chat_message("assistant"):
        st.write_stream(stream_constructor(response))   # 自动逐字渲染，内置打字机效果
