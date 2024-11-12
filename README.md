### GenAI
LangChain(Ver0.3)の機能を活用した勉強用コード

### フォルダ内容
#### langchain_test
・LangChainを用いたChat機能の実装（会話履歴の保持や、テンプレート利用など）<br>
・Chainlitを用いたChatBot用UIの実装<br>
・ベクトルDBを用いた検索機能の実装<br>
・Agentを用いた機能拡充<br>


### ディレクトリ構成
<pre>
src
├── langchain_test
│   ├── setting.ini
│   ├── app.py
│   ├── vectordb.py
│   ├── agent.py
│   └── chabot.py
├── venv
├── .gitignore
└── README.md
</pre>

langchain_test・・・LngChain勉強用フォルダ

### インストールライブラリ
|ライブラリ|-|
|----|-----|
|langchain|Chat|
|langchain-community|RAG|
|faiss-cpu|RAG|
|langchain_anthropic|Agent|