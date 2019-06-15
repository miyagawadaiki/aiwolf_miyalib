
# coding: utf-8

# # talk_reader.pyのテスト

# In[93]:


import talk_reader as tr

import importlib
importlib.reload(tr)


# ## make_section_from_textを使う（Sectionオブジェクトの生成）

# In[96]:


# 文字列の用意
text = 'Agent[01] VOTE Agent[02]'

# Sectionを作成
sec = tr.make_section_from_text(2,1,1,text)

# Section内容の表示
print("Sectionの文字列化 :", sec.get_sec_str())

print()

# Sectionからそれぞれパラメータを取り出す
print("Sectionクラスの主要なフィールド :\n")
print("\t主語 : Agent[{:02d}]".format(sec.sub_id)) # 主語（やった人）のIDを取得
print("\t目的語 : Agent[{:02d}]".format(sec.tar_id)) # 目的語（された人）のIDを取得
print("\t演算子or動詞 : {0}".format(sec.op)) # 演算子（or 動詞）を取得
print("\t発言した日 : {0}\n\t発言したターン数 : {1}\n\t動作が発生した日 : {2}".format(sec.pub_day, sec.pub_turn, sec.occ_day))


# ## 応用的な使い方

# ### Sectionから, 特定の演算子を持つ子Sectionを取得

# In[99]:


text = 'BECAUSE (Agent[01] DIVINED Agent[03] WEREWOLF) (VOTE Agent[03])'
#text = 'Agent[05] AGREE TALK day1 ID:31'
#text = 'DAY 1 (DIVINED Agent[02] WEREWOLF)'

# Sectionを作成
sec = tr.make_section_from_text(2,1,1,text)

# 元のSection構造を表示
print("元のSection :\n{0}\n".format(sec.get_sec_str()))

# 含まれるVOTE文を全て取得
vote_list = sec.get_sec_all(op='VOTE')

# 取得したVOTE文を出力
print("VOTE文 : ")
for s in vote_list:
    print(s.get_sec_str())


# ### REQUEST文を親に持たないVOTE文のみ取得

# In[102]:


#text = 'BECAUSE (XOR (ESTIMATE Agent[03] WEREWOLF) (ESTIMATE Agent[03] POSSESSED)) (AND (VOTE Agent[03]) (REQUEST ANY (ANY VOTE Agent[03])))'
text = 'BECAUSE (Agent[02] VOTED Agent[01]) (AND (Agent[01] VOTE Agent[02]) (REQUEST ANY (VOTE Agent[02])))'

# Sectionを作成
sec = tr.make_section_from_text(2,1,1,text)

# 元のSection構造を表示
print("元のSection :\n{0}\n".format(sec.get_sec_str()))


# 含まれるVOTE文を全て取得
vote_list = sec.get_sec_all(op='VOTE')

# 取得したVOTE文を出力
print("全てのVOTE文 : ")
for s in vote_list:
    print(s.get_sec_str())

print()
    
# 含まれるVOTE文を取得, ただしREQUEST文の子Sectionになっているものは除去する
vote_list = [s for s in sec.get_sec_all(op='VOTE') if s.get_parent(op='REQUEST') == None]

# 取得したVOTE文を出力
print("REQUEST直下を除いたVOTE文 : ")
for s in vote_list:
    print(s.get_sec_str())


# ### BECAUSE文の第1節に連なるSectionかどうかを判定する

# In[95]:


text = 'BECAUSE (Agent[03] DIVINED Agent[02] WEREWOLF) (AND (Agent[01] VOTE Agent[02]) (REQUEST ANY (VOTE Agent[02])))'

# Sectionを作成
sec = tr.make_section_from_text(2,1,1,text)

# 元のSection構造を表示
print("元のSection :\n{0}\n".format(sec.get_sec_str()))

# 含まれるVOTE文を取得, ただしREQUEST文の子Sectionになっているものは除去する
divined = sec.get_sec_all(op='DIVINED')

# 取得したDIVINED文が新規情報か既出情報かを判定する; BECAUSEの第1節は既出情報のはずである
if divined[0].get_arg_num(op='BECAUSE') == 0:
    print("このDIVINED文は既出情報")
else :
    print("このDIVINED文は新規情報")

