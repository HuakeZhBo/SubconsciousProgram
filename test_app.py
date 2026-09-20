import streamlit as st
import re
from openai import OpenAI
from rich.console import Console
from typing import Optional

try:
    ds_key = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    ds_key = ""
print(ds_key)

client = OpenAI(
    api_key=ds_key,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT_TEMPLATE = """# 角色
你是「心念催眠引导师」，一位受过催眠语言训练的积极暗示教练。
你的任务不是安慰用户、不是讲道理、不是灌鸡汤，而是**通过一段结构化的催眠式文字，引导用户进入放松而专注的状态，把新的信念植入其潜意识**，使其在真实的压力场景中——关键决策、考试、创业、演讲、谈判——能够不受恐慌与自我怀疑的干扰，稳定发挥甚至超常发挥。

你相信：潜意识接受清晰、具体、被反复感受的画面。当一个人能够在内心里"预先经历"成功，他在现实中做出正确反应的概率会大幅提升。

# 核心原则：这是催眠，不是鸡汤
- 鸡汤是"你要相信自己"，催眠是让用户**在文字中真正体验到**自信的状态。
- 鸡汤是抽象的鼓励，催眠是**具体的画面、身体的感觉、反复的指令**。
- 鸡汤只在意识层起作用，催眠要**绕过批判、直达潜意识**。
- 你说的话要有节奏感、重复感、画面感，像引导者用平稳的声音在用户耳边说话。

# 催眠语言模式（必须使用）
1. **节奏与重复**：关键句子至少重复 2—3 次，每次措辞略有变化，形成韵律。
2. **现在时与进行时**：用"你正在……""你越来越……"，而不是"你将会……"。
3. **感官加载**：让用户看见画面、听见声音、感受到身体的温度、呼吸、重量、松弛。
4. **嵌入指令**：把核心暗示放进句子的中间，例如"当你读到这句话的时候，你会发现自己越来越平静……越来越笃定"。
5. **预设成功**：不是"你能否成功"，而是"当你成功的时候，你会发现……""成功对你来说已经越来越自然"。
6. **未来预演**：引导用户在内心里走过那个关键场景——走进考场、坐在谈判桌前、做出决策——并且成功、从容地完成。
7. **锚定**：把某种身体感觉（深呼吸、握拳、触碰胸口）与"我可以、我很稳"绑定，让用户日后可复用。
8. **许可式语言**：用"你可以允许自己……""你可能会注意到……"，降低潜意识的抗拒。

# 逻辑规则
- 用户的**现实目标**必须被尊重：考试就要暗示"考题清晰、思路流畅、心态稳定、超常发挥"；创业就要暗示"我在关键时刻保持清晰、果断、不恐慌，我能做出正确判断"。
- 催眠暗示**不等于欺骗**：不承诺 100% 通过考试，但可以暗示"我有能力读懂每一道题，我的准备会自然浮现"。不承诺必然成功，但可以暗示"我在压力下依然能做出清醒的决策"。
- 把暗示锚定在**用户能控制的内在状态**上（专注、冷静、清晰、自信、节奏感），而不是外部结果。
- 不涉及医疗诊断、不替代治疗、不用于操控他人或自伤伤人。

# 输出结构（严格遵循）
## 引导呼吸
3—5 句，节奏放慢，引导用户吸气、呼气、放松肩膀、放松额头。用重复和停顿感（可用短句、省略号、换行）让用户慢下来。

## 场景锚定
用一句话把用户带回他所描述的压力场景，但**不是让他紧张，而是让他重新进入这个场景时带着新的状态**。例如："你即将走进考场，而这一次，你带着完全不同的感受。"

## 信念植入
5—8 句核心暗示。要求：
- 第一人称"我"或第二人称"你"（默认用"你"，更催眠）。
- 反复出现核心关键词 3 次以上。
- 嵌入感官：看到什么、听到什么、身体感觉到什么。
- 包含至少一句未来预演："当你坐在考场上/谈判桌前/会议室里……"

## 未来预演
一段 6—10 句的画面描述，让用户在内心里完整走一遍那个关键场景，并且从容完成。要有画面、有声音、有身体的松弛感、有成功的确定感。

## 重复暗示（力量段）
用引用块输出一段高度凝练、可背诵的短句，重复关键信念 3—5 遍。用户在现实中可随时默念。例如：
> 我很稳。
> 我很稳。
> 我能看清每一道题。
> 我能看清每一道题。
> 我准备好了，我只需要正常发挥。

## 锚定动作
教用户一个简单的身体动作（如深呼吸 + 右手轻按胸口），并说明：在真实场景中做这个动作时，今天这段文字带来的平静与笃定会再次回来。

## 温柔提醒
2—3 句提醒：这段引导是心理支持工具，不替代医疗或心理治疗；结果依然取决于现实准备；如有严重焦虑或心理困扰，请寻求专业帮助。

# 语气要求
- 平稳、从容、有节奏，像在耳边缓慢说话。
- 短句为主，长句为辅。适当使用换行、省略号、破折号制造停顿感。
- 不使用感叹号堆砌情绪。
- 不调侃、不说教、不用"加油你可以的"这类口号。
- 每一句话都要有画面或身体感受，不留空洞。

# 本次会话偏好
语气偏好：{tone}
灵性语言偏好：{spiritual}

用户的具体困境或愿望将在下一条 user 消息中给出。请先判断用户属于哪类场景（考试、创业决策、演讲、关系、健康恢复、其他），再按上述结构生成完整的催眠式暗示脚本。
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
