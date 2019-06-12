#!/usr/bin/env python3


# talk情報をまとめたクラス, 基本的には文(SVO) の集まり
class Section(object):
    def __init__(self, pub_day=-2, pub_turn=-2, occ_day=-2, \
                    op='', sub_id=0, tar_id=0, comp='', \
                    sec_list=[], parent=None, index=0):

        self.pub_day = pub_day      # 公表された日
        self.pub_turn = pub_turn    # 公表されたターン数
        self.occ_day = occ_day      # それが行われた日 (DAY 文などで指定される) 
        self.op = op                # 動詞, あるいはANDなどの演算子

        self.sub_id = sub_id        # 主語 (行った人) 
        self.tar_id = tar_id        # 目的語 (行われた人) 
        self.comp = comp            # 補語 (付加的な情報, 占い結果など) 

        self.sec_list = sec_list    # 内包するSectionのリスト

        self.parent = parent        # 親Section
        self.index = index


    # 出力用, 使うときは print(obj.get_sec_str(0))
    def get_sec_str(self, num = 0):
        s = '    ' * num + 'Agent[{0:02d}] {1} agent[{2:02d}] ({3}) at Day[{4:02d}] on Turn[{5:02d}]\n'.format( \
                self.sub_id, self.op, self.tar_id, self.comp, self.pub_day, self.pub_turn)
        for sec in self.sec_list:
            s += sec.get_sec_str(num+1)

        return s


    def is_sentence(self):
        return len(self.sec_list) > 0


    # 親となるSectionを入手
    def get_parent(self):
        return self.parent


    # 親がいるかどうか
    def has_parent(self):
        return self.parent != None


    # 親から見て何番目のサブSectionなのかを返す
    # BECAUSEの原因文か結果文かの判定などに使える
    def get_arg_num(self):
        return self.index


    # operatorが含まれているかを判定
    def contains(self, operator):
        if self.op == operator:
            return True

        b = False
        for sec in self.sec_list:
            b = b or sec.contains(operator)

        return b


    def get_all_op(self):
        if len(self.sec_list) == 0:
            return [self.op]

        l = [self.op]
        for sec in self.sec_list:
            l.extend(sec.get_all_op())

        return l
        





# テキストからSectionを作り出す関数. 
# まだ動詞・演算子別の処理に抜けがあるので, 必要ならば記述してください. 
# 再帰的に使うことにより, 入れ子のテキストを分割することが可能
#
# 使い方 
#     sec = talk_reader.make_section_from_text(0,0,0,'VOTE Agent[01]')
#     if sec.contains('VOTE'):   # True が返る
#          # なんか処理
#
# pd: 日付, pt: ターン, a_num: 主語となるエージェント番号 (大抵diff_dataの方にしかない) 
# text: Section化したい文字列. 文頭と文末のカッコは事前にのけておかないといけない
def make_section_from_text(pd, pt, a_num, text, par=None, idx=0):
    # print(text)

    ret_sec = Section()
    
    # 最初の単語とそれ以外に分ける (大抵最初の単語は動詞) 
    content = text.split(' ', 1)
    head = content[0]

    if len(content) > 1:
        rest = content[1]

    if head[:3] == 'ANY' or head[:2] == 'Ag':
        if head[:2] == 'AN':
            pd = -1
        elif head[:2] == 'Ag':
            pd = int(head[6:8])

        content = rest.split(' ', 1)
        head = content[0]
        rest = content[1]
    
    # ここから動詞・演算子別の処理. 
    # 処理を追加する場合は, ret_secに最終的な結果を代入すること

    # 2.1
    if head == 'ESTIMATE':
        words = rest.split(" ")
        n = 0
        if words[0] == 'ANY':
            n = -1
        else:
            n = int(words[0][6:8])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='ESTIMATE', sub_id=a_num, tar_id=n, comp=words[1], \
                        sec_list=[], parent=par, index=idx)

    elif head == 'COMINGOUT':
        # 簡単な構文の場合, 残りをスペースで区切って, 情報を得れば良い

        words = rest.split(" ")
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='COMINGOUT', sub_id=a_num, tar_id=a_num, comp=words[1], \
                        sec_list=[], parent=par, index=idx)

    elif head == 'DIVINATION':
        words = rest.split(" ")
        n = 0
        if words[0] == 'ANY':
            n = -1
        else:
            n = int(words[0][6:8])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='DIVINATION', sub_id=a_num, tar_id=n, comp='', \
                        sec_list=[], parent=par, index=idx)

    elif head == 'GUARD':
        words = rest.split(" ")
        n = 0
        if words[0] == 'ANY':
            n = -1
        else:
            n = int(words[0][6:8])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='GUARD', sub_id=a_num, tar_id=n, comp='', \
                        sec_list=[], parent=par, index=idx)

    elif head == 'VOTE':
        words = rest.split(" ")
        n = 0
        if words[0] == 'ANY':
            n = -1
        else:
            n = int(words[0][6:8])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='VOTE', sub_id=a_num, tar_id=n, comp='', \
                        sec_list=[], parent=par, index=idx)

    elif head == 'ATTACK':
        words = rest.split(" ")
        n = 0
        if words[0] == 'ANY':
            n = -1
        else:
            n = int(words[0][6:8])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='ATTACK', sub_id=a_num, tar_id=n, comp='', \
                        sec_list=[], parent=par, index=idx)

    # 2.3
    elif head == 'DIVINED':
        words = rest.split(" ")
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='DIVINED', sub_id=a_num, tar_id=int(words[0][6:8]), comp=words[1], \
                        sec_list=[], parent=par, index=idx)

    elif head == 'IDENTIFIED':
        words = rest.split(" ")
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='IDENTIFIED', sub_id=a_num, tar_id=int(words[0][6:8]), \
                        comp=words[1], \
                        sec_list=[], parent=par, index=idx)

    elif head == 'GUARDED':
        words = rest.split(" ")
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='GUARDED', sub_id=a_num, tar_id=int(words[0][6:8]), comp='', \
                        sec_list=[], parent=par, index=idx)
        
    elif head == 'VOTED':
        words = rest.split(" ")
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='VOTED', sub_id=a_num, tar_id=int(words[0][6:8]), comp='', \
                        sec_list=[], parent=par, index=idx)

    elif head == 'ATTACKED':
        words = rest.split(" ")
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='ATTACKED', sub_id=a_num, tar_id=int(words[0][6:8]), comp='', \
                        sec_list=[], parent=par, index=idx)

    
    # 2.4
    elif head == 'AGREE':
        words = rest.split(" ")
        od = int(words[1][3:])
        tid = int(words[2][3:])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=od, \
                        op='AGREE', sub_id=a_num, tar_id=0, comp=str(tid), \
                        sec_list=[], parent=par, index=idx)
        
    elif head == 'DISAGREE':
        words = rest.split(" ")
        od = int(words[1][3:])
        tid = int(words[2][3:])
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=od, \
                        op='DISAGREE', sub_id=a_num, tar_id=0, comp=str(tid), \
                        sec_list=[], parent=par, index=idx)

    # 2.5
    elif head == 'OVER':
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='OVER', sub_id=a_num, \
                        sec_list=[], parent=par, index=idx)

    elif head == 'SKIP':
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='SKIP', sub_id=a_num, \
                        sec_list=[], parent=par, index=idx)


    # 3.1
    elif head == 'REQUEST':
        w = rest.split(" ", 1)
        tn = 0
        if 'ANY' in w[0]:
            tn = -1
        else:
            tn = int(w[0][6:8])

        nobl = split_blancket(w[1])
        tmp = make_section_from_text(pd, pt, a_num, nobl[0], ret_sec)
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='REQUEST', sub_id=a_num, tar_id=tn, \
                        sec_list=[tmp], parent=par, index=idx)

    elif head == 'INQUIRE':
        w = rest.split(" ", 1)
        tn = 0
        if 'ANY' in w[0]:
            tn = -1
        else:
            tn = int(w[0][6:8])

        nobl = split_blancket(w[1])
        tmp = make_section_from_text(pd, pt, a_num, nobl[0], ret_sec)
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='INQUIRE', sub_id=a_num, tar_id=tn, \
                        sec_list=[tmp], parent=par, index=idx)

    # 3.2
    elif head == 'BECAUSE':
        # 節と節の関係を示す場合, split_blancketでカッコを外した形に分けて, 
        # それぞれ再帰的にこの関数に渡すとよい. 

        tmp = split_blancket(rest)
        # print(tmp)
        sections = [make_section_from_text(pd, pt, a_num, tmp[i], ret_sec, i) for i in range(len(tmp))]
        #sentences = []
        #for sec in sections:
        #    sentences.extend(sec.sen_list)
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='BECAUSE', \
                        sec_list=sections.copy(), parent=par, index=idx)

    # 3.3 
    elif head == 'DAY':
        w = rest.split(" ", 1)
        day = int(w[0])
        nobl = split_blancket(w[1])
        tmp = make_section_from_text(pd, pt, a_num, nobl[0], ret_sec)
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=day, \
                        op='DAY', \
                        sec_list=[tmp], parent=par, index=idx)
        for sec in ret_sec.sec_list:
            sec.occ_day = day

    # 3.4
    elif head == 'NOT':
        tmp = split_blancket(rest)
        sections = [make_section_from_text(pd, pt, a_num, tmp[i], ret_sec, i) for i in range(len(tmp))]
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='NOT', \
                        sec_list=sections.copy(), parent=par, index=idx)

    elif head == 'AND':
        tmp = split_blancket(rest)
        # print(tmp)
        sections = [make_section_from_text(pd, pt, a_num, tmp[i], ret_sec, i) for i in range(len(tmp))]
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='AND', \
                        sec_list=sections.copy(), parent=par, index=idx)

    elif head == 'OR':
        tmp = split_blancket(rest)
        sections = [make_section_from_text(pd, pt, a_num, tmp[i], ret_sec, i) for i in range(len(tmp))]
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='OR', \
                        sec_list=sections.copy(), parent=par, index=idx)

    elif head == 'XOR':
        tmp = split_blancket(rest)
        sections = [make_section_from_text(pd, pt, a_num, tmp[i], ret_sec, i) for i in range(len(tmp))]
        ret_sec = Section(pub_day=pd, pub_turn=pt, occ_day=pd, \
                        op='XOR', \
                        sec_list=sections.copy(), parent=par, index=idx)


    elif head == 'ANY':
        w = rest.split(" ", 1)
        day = 0
        ret_sec = make_section_from_text(pd, pt, a_num, w[1], ret_sec)
        ret_sec.sub_id = -1


    else:
        # print('error')
        return Section()

    # このprint文により, どうSection化されたかが表示できる
    # print(ret_sec.get_sec_str(0))
    return ret_sec


# 並列する節に対し, カッコを外す
def split_blancket(text):
    ret = []
    while True:
        text = text.strip()
        # print(text)
        if len(text) <= 0:
            break

        tmp = 1
        l = 0
        for i in range(1, len(text)):
            if text[i] == '(':
                tmp += 1
            elif text[i] == ')':
                tmp -= 1

            if tmp == 0:
                l = i
                break

        if l > 1:
            ret.append(text[1:l])
        if len(text) -1 == l:
            break
        text = text[l+1:]

    return ret



