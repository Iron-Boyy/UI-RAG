from retrieval import DocumentRetrieval
import gradio as gr

db_sys = None

def echo(message, history):
    global db_sys
    if db_sys is None: return "当前未传入文档，请传入文档后再尝试"
    message = db_sys.chat_qa(message)
    return message

def process_file(filepath):
    global db_sys
    try:
        db_sys = DocumentRetrieval(512, emd_path="../bge-small-zh-v1.5", override_db=True)
        db_sys.add_document(filepath, chunk_size=200)
        response = db_sys.chat_summary(0)
        return response
        return "文件解析成功，可以开始对话"
    except:
        return "文件解析失败，请重试或更换文件"

def main():
    with gr.Blocks() as demo:
        gr.Markdown('## Step 1: 上传文件')
        with gr.Row():
            with gr.Column( scale=1):
                file = gr.File(type='filepath', scale=1, height=100)
                button = gr.Button(value='上传文件', scale=1, variant='primary', min_width=50)
            filetext = gr.Textbox(label='文件解析结果', scale=2, lines=3)
        button.click(process_file, inputs=[file], outputs=[filetext])

        gr.Markdown('\n\n## Step 2: 开始对话')
        chatinterface = gr.ChatInterface(fn=echo, chatbot=gr.Chatbot(height=500, render=False))
    demo.launch(server_port=7968, server_name='0.0.0.0')

if __name__ == '__main__':
    main()