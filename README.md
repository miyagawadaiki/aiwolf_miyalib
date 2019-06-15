# aiwolf\_miyalib

## talk\_reader.py
diff\_data から取れるプレイヤー（あるいはシステム）の発言を, Sectionクラスに変換する.  
Sectionクラスは会話が行われた日, ターン, 誰が何をやったのか, などについて管理するクラスである.  
入れ子構造にも対応している. 

構文は[ここ](http://aiwolf.org/control-panel/wp-content/uploads/2019/02/protocol_2019_3_6m.pdf)を参考にしている (2019/06/12時点)

### Sectionクラス
#### 概要
"主語 動詞 修飾語（目的語, 補語など）" で構成される文字列をsentenceと呼ぶ.  

* "Agent[01] DIVINED Agent[03] HUMAN"

sentenceはoperator（AND, ORなど）を使うと, 一つの文中に複数含めることや, 入れ子構造を作ることができる.  

* "AND (Agent[01] DIVINED Agent[04] HUMAN) (Agent[01] ESTIMATE Agent[04] POSSESSED)"
* "BECAUSE (Agent[02] VOTED Agent[01]) (AND (Agent[01] VOTE Agent[02]) (REQUEST ANY (VOTE Agent[02])))"

これらの文字列について, 構造化して使いやすい形にしたものがSectionクラスである.  
例えば, 入れ子構造についても次のように解決できる.  

* Section化前 :  
"BECAUSE (Agent[02] VOTED Agent[01]) (AND (Agent[01] VOTE Agent[02]) (REQUEST ANY (VOTE Agent[02])))"
* Section化後 :  
Agent[00] BECAUSE agent\[00\] () at Day[00] on Turn[00]
    Agent[02] VOTED agent[01] () at Day[00] on Turn[00]
    Agent[00] AND agent[00] () at Day[00] on Turn[00]
        Agent[01] VOTE agent[02] () at Day[00] on Turn[00]
        Agent[00] REQUEST agent[-1] () at Day[00] on Turn[00]
            Agent[-1] VOTE agent[02] () at Day[00] on Turn[00]

<br><br>
#### 仕様
* フィールド
	- pub\_day  : 発言が公表された日
	- pub\_turn : 発言が公表されたターン
	- occ\_day  : 発言内容が行われた日（初日潜伏占い師が2日目に前日の結果と合わせて言う時など）
	- sub\_id   : 主語となるエージェントのID（ANYの場合はID=-1）
	- tar\_id   : 目的語となるエージェントのID（ANYの場合はID=-1）
	- op        : 演算子または動詞の文字列
	- comp      : 補語（プロトコル資料における[role]や[species]が入る）
	- sec\_list : 直下に包含するSectionクラスのリスト（無ければ空リスト）
	- parent    : 親となるSection（親がいなければNone）
	- index     : 親Sectionから見て何番目の節か（親がいなければ-1, BECAUSEあたりでしか使わない）

* メソッド
	- get\_sec\_str(num=0):
		* 説明   : Sectionクラスの中身を出力させるときに使う. 
		* 使い方 : ```print(sec.get_sec_str())```
		* 引数   : いじる必要なし

	- get\_sec\_str\_p(num=0):
		* 説明   : ほぼget\_sec\_str(num=0)と同じだが, parentとindexも表示する. 

	- get\_sec\_all(op=None):
		* 説明   : 自分自身と, 己が含む全ての子Sectionの中から演算子がopと等しいものを検索してリストで全て返す. op=Noneのときは検索せず入れ子になっている全てのSectionを返す. 
		* 使い方 : ```sections = sec.get_sec_all(op='VOTE')```
		* 引数   :
			- op : 検索したい演算子or動詞の文字列. Noneはワイルドカード扱い. 

	- get\_parent(op=None):
		* 説明   : 自分が子Sectionの場合, 親Sectionを返す. opに演算子or動詞を設定することで, 親を辿って検索することもできる. 親がそもそもいない場合, 検索しても見つからなかった場合はNoneを返す. 
		* 使い方 : ```if child_sec.get_parent(op='REQUEST') != None: ```
		* 引数   : 
			- op : 検索したい演算子or動詞の文字列. Noneだと直上にある親を返す. 

	- get\_arg\_num(op=None):
		* 説明   : 基本的には, 親から見て何番目の子Sectionなのかを返す（番号は0から始まる）. opに演算子or動詞を指定すると, 親を遡ってそのopを検索し, 祖先に存在したときは, その祖先の第n文に連なるかのnを返す. 無ければ-1を返す. BECAUSEのとき以外は第1文と第2文に違いはないので, BECAUSEでしか使わないだろう. 
		* 使い方 : ```if child_sec.get_arg_num(op='BECAUSE') == 0:```
		* 引数   : 
			- op : 検索したい演算子or動詞の文字列. Noneだと直上にある親から見た位置を返す.

	- contains(op):
		* 説明   : Section構造の中に, opが含まれているかどうかを返す. 
		* 使い方 : ```if sec.contains('DIVINED') and not(sec.contains('BECAUSE'): ```
		* 引数   : 
			- op : 検索したい演算子or動詞の文字列. 

	- get\_all\_op():
		* 説明   : Section構造から, 含まれる全ての演算子or動詞をリストで返す. 
		* 使い方 : ```op_list = sec.get_all_op()```

	- has\_parent():
		* 説明   : 直上に親がいるかどうか返す. 


<br>
### Sectionクラスを作るための関数
* make\_section\_from\_text(pd, pt, a\_num, text, par=None, idx=-1):
	- 説明 : 文字列と, 日付, ターン数, 主語のID（大抵文字列内では省略されるので必要）を使ってSectionを生成する. 日付などのデータはdiff\_dataから得ることになるだろう. 
	- 引数 : 
		* pd    : 発言された日付
		* pt    : 発言されたターン
		* a_num : 発言した人（主語）
		* text  : 発言内容の文字列
		* par   : 気にしなくていい
		* idx   : 気にしなくていい


<br>
### 具体的な使用例
Jupyter Notebookが使えるなら, Test.ipynbにもいくつかメソッド使用例が示してある. 

#### diff\_dataのtype=talkの行からSectionクラスを生成
```
talk_data = diff\_data.query('type = "talk"')  # talkの行のみ抽出

# make_section_from_text関数を使って, Section化する.   
sec = make_section_from_text(talk_data.day[0], talk_data.turn[0], talk_data.agent[0], talk_data.text[0])
```

#### Sectionから特定の演算子を持つSectionを検索して取得 & 表示
```
sec = make_section_from_text(1,1,2,'BECAUSE (Agent[01] DIVINED Agent[03] WEREWOLF) (VOTE Agent[03])')
sections = sec.get_sec_all(op='VOTE')
print(sections[0].get_sec_str())  # Agent[02] VOTE agent[03] () at Day[01] on Turn[01]
```

#### 'REQUEST'を親に持たない'VOTE'文のみ検索
```
text = 'BECAUSE (Agent[02] VOTED Agent[01]) (AND (Agent[01] VOTE Agent[02]) (REQUEST ANY (VOTE Agent[02])))'
sec = make_section_from_text(2,1,1,text)
vote = [s for s in sec.get_sec_all(op='VOTE') if s.get_parent('REQUEST') == None]
```

#### 'BECAUSE'の第1文に連なるSectionかどうかを判定. 
```
text = 'BECAUSE (Agent[03] DIVINED Agent[02] WEREWOLF) (AND (Agent[01] VOTE Agent[02]) (REQUEST ANY (VOTE Agent[02])))'
sec = make_section_from_text(2,1,1,text)
voted = sec.get_sec_all(op='DIVINED')
if voted.get_arg_num('BECAUSE') == 0:
	# BECAUSEの第1文なので新規情報ではない
```


