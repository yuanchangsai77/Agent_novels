import gradio as gr
import os
from agents.OutlineAgent import OutlineAgent
from agents.ChapterAgent import ChapterAgent 
from agents.MemoryAgent import MemoryAgent

class NovelGenerator:
   def __init__(self):
       self.memory_dir = 'output/memory'
       self.chapters_dir = 'output/chapters'
       self.current_chapter = 1
       self.ensure_dirs()

   def ensure_dirs(self):
       for dir in [self.memory_dir, self.chapters_dir]:
           if not os.path.exists(dir):
               os.makedirs(dir)

   def generate_outline(self, initial_prompt, keywords):
       agent = OutlineAgent(initial_prompt, keywords)
       agent.run()
       with open(f'{self.memory_dir}/novel_outline.txt', 'r', encoding='utf-8') as f:
           return f.read()

   def generate_chapter(self, chapter_num, regenerate=False):
       agent = ChapterAgent('novel_outline.txt')
       agent.run(chapter_num)
       
       with open(f'{self.chapters_dir}/chapter_{chapter_num:03d}.txt', 'r', encoding='utf-8') as f:
           chapter_text = f.read()
           
       memory_agent = MemoryAgent()
       memory_agent.run(chapter_text, chapter_num)
       
       return chapter_text

   def load_chapter(self, chapter_num):
       try:
           with open(f'{self.chapters_dir}/chapter_{chapter_num:03d}.txt', 'r', encoding='utf-8') as f:
               return f.read()
       except:
           return ""

def create_ui():
   generator = NovelGenerator()
   
   with gr.Blocks() as app:
       with gr.Tab("大纲生成"):
           initial_prompt = gr.Textbox(
               label="初始提示词",
               value="在未来，一款名为《无限世界》的虚拟现实游戏因技术故障将游戏机制渗透到现实生活中，赋予人们战斗技能、等级和任务系统。28岁的上班族张强和他的同事小美发现自己获得了这些能力，随后游戏中的怪物开始出现在现实世界，威胁人类安全。为了对抗这些威胁，张强和小美联合其他拥有能力的朋友，组建团队并共同对抗试图利用游戏机制统治世界的神秘反派组织。经过一系列激烈的战斗和牺牲，团队最终击败了反派，关闭了游戏门户，世界逐渐恢复平静。张强在这一过程中成长为领导者，与小美一起引领社会重建，展望未来。"
           )
           keywords = gr.Textbox(
               label="关键词(用逗号分隔)",
               value="游戏入侵现实，打怪升级，虚拟现实，能力觉醒，团队合作，反派组织，成长与领导，世界恢复"
           )
           outline_output = gr.Textbox(label="生成的大纲", lines=10)
           generate_btn = gr.Button("生成大纲")
           generate_btn.click(
               generator.generate_outline,
               inputs=[initial_prompt, keywords],
               outputs=outline_output
           )

       with gr.Tab("章节生成"):
           with gr.Row():
               chapter_num = gr.Number(value=1, label="章节号")
               regenerate = gr.Checkbox(label="重新生成")
           
           chapter_output = gr.Textbox(label="章节内容", lines=10)
           memory_output = gr.Textbox(label="记忆/设定提取", lines=5)
           
           generate_chapter_btn = gr.Button("生成/重新生成章节")
           extract_memory_btn = gr.Button("提取记忆")
           next_chapter_btn = gr.Button("下一章")
           
           def extract_memory(chapter_text, chapter_num):
               memory_agent = MemoryAgent()
               memory_data = memory_agent.extract_memory(chapter_text, chapter_num)
               return memory_data
               
           generate_chapter_btn.click(
               generator.generate_chapter,
               inputs=[chapter_num, regenerate],
               outputs=[chapter_output]
           )
           
           extract_memory_btn.click(
               extract_memory,
               inputs=[chapter_output, chapter_num],
               outputs=[memory_output]
           )
           
           next_chapter_btn.click(
               lambda x: x + 1,
               inputs=[chapter_num],
               outputs=[chapter_num]
           )

       with gr.Tab("小说预览"):
           with gr.Row():
               chapter_nav = gr.State(value=1)
               prev_btn = gr.Button("上一章")
               chapter_select = gr.Dropdown(
                   choices=[f"第{i}章" for i in range(1, 100)],
                   value="第1章",
                   label="选择章节"
               )
               next_btn = gr.Button("下一章")
           
           preview_output = gr.Textbox(label="章节内容", lines=15)
           
           def load_preview(chapter):
               num = int(chapter[1:-1])
               return generator.load_chapter(num)
               
           def prev_chapter(chapter):
               if chapter == "第1章":
                   return chapter
               num = int(chapter[1:-1]) - 1
               return f"第{num}章"
               
           def next_chapter(chapter):
               num = int(chapter[1:-1]) + 1 
               return f"第{num}章"
               
           chapter_select.change(
               load_preview,
               inputs=[chapter_select],
               outputs=[preview_output]
           )
           
           prev_btn.click(
               prev_chapter,
               inputs=[chapter_select],
               outputs=[chapter_select]
           )
           
           next_btn.click(
               next_chapter, 
               inputs=[chapter_select],
               outputs=[chapter_select]
           )

   return app

if __name__ == "__main__":
   app = create_ui()
   app.launch()