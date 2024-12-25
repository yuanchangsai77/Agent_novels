# OutlineAgent.py

import os
import json
from agents.Agent_llm import initialize_llm, create_outline_prompt

class OutlineAgent:
    def __init__(self, initial_prompt, keyword_prompts, memory_dir='output/memory'):
        self.initial_prompt = initial_prompt
        self.keyword_prompts = keyword_prompts
        self.memory_dir = memory_dir
        self.llm = initialize_llm()
        self.prompt_template = create_outline_prompt()
        self.ensure_memory_dir()

    def ensure_memory_dir(self):
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)

    def generate_outline(self):
        input_data = {
            'initial_prompt': self.initial_prompt,
            'keyword_prompts': self.keyword_prompts,
            'total_chapters':10
        }
        outline = self.prompt_template | self.llm
        response = outline.invoke(input=input_data)
        return response.content

    def format_outline(self, outline_text):
        try:
            return json.loads(outline_text)
        except json.JSONDecodeError:
            return {"outline_text": outline_text}

    def save_outline(self, outline_data, filename='novel_outline.txt'):
        filepath = os.path.join(self.memory_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(outline_data)
        print(f"大纲已保存到 {filepath}")

    def run(self):
        print("正在生成小说大纲...")
        outline_text = self.generate_outline()
        # print("大纲生成完毕，正在格式化...")
        # outline_data = self.format_outline(outline_text)
        print("大纲生成完毕，正在保存...")
        self.save_outline(outline_text)
        print("大纲生成流程完成。")

if __name__ == "__main__":
    initial_prompt = "在未来，一款名为《无限世界》的虚拟现实游戏因技术故障将游戏机制渗透到现实生活中，赋予人们战斗技能、等级和任务系统。28岁的上班族张强和他的同事小美发现自己获得了这些能力，随后游戏中的怪物开始出现在现实世界，威胁人类安全。为了对抗这些威胁，张强和小美联合其他拥有能力的朋友，组建团队并共同对抗试图利用游戏机制统治世界的神秘反派组织。经过一系列激烈的战斗和牺牲，团队最终击败了反派，关闭了游戏门户，世界逐渐恢复平静。张强在这一过程中成长为领导者，与小美一起引领社会重建，展望未来。"
    keyword_prompts = '游戏入侵现实，打怪升级，虚拟现实，能力觉醒，团队合作，反派组织，成长与领导，世界恢复'
    
    agent = OutlineAgent(initial_prompt, keyword_prompts)
    agent.run()