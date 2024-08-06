import os
 
path = '/home/SENSETIME/luozhihao/code/AppAgent/apps/Markor/demo_docs'
path_sys = '/home/SENSETIME/luozhihao/code/AppAgent/apps/sys_doc'
 
flie_dir = os.listdir(path)
flie_sys_dir = os.listdir(path_sys)
for file in flie_dir:
    with open(os.path.join(path, file), "r") as w:
        doc_content = w.read()
    doc_item = file[:-4]+":"+doc_content+"\n"
    f = open("Label.txt",'a')
    f.write(doc_item)
for file in flie_sys_dir:
    with open(os.path.join(path_sys, file), "r") as w:
        doc_content = w.read()
    doc_item = file[:-4]+":"+doc_content+"\n"
    f.write(doc_item)



