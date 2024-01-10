
# Usage for ML based chat bot

### Dataset used: 

https://huggingface.co/datasets/dzunggg/legal-qa-v1
<br>
- Local file saved in `./data/legal_qa_full.csv`
- Data extracted from https://thelawdictionary.org/ and https://answers.justia.com/


### 1. Install packages
```
pip install -r requirements.txt
```

### 2. Run Chat Bot
Run the app.py file.
```
python app.py
```
Type `exit` to stop the program.

<br><br><br>

# Usage for similarity based chat bot (v2)

### Dataset used: 

- Local file saved in `./data/legal_qa_summarized_full.csv`
- Data extracted from https://thelawdictionary.org/ (summarized answers) and https://answers.justia.com/

### 1. Install packages
```
pip install -r requirements.txt
```

### 2. Run Chat Bot
Go to the folder `rule_based_chatbot`and run `SimilarityChatBot_v2.py` file.
```
python SimilarityChatBot_v2.py
```
Type `exit` to stop the program.
