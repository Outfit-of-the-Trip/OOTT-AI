# OOTT-AI

## Trend Crawling
### 1. Create a `secret.json` file using the following code.
```json
{
	"INSTAGRAM_KEY": {
    "ID": "input isntagram id",
    "PW": "input instagram password"
  }
}
```
### 2. Change save image path
```python
# trend_crawling/main.py
SAVE_PATH = 'Set/saving/path/what/you/want'
```

### 3. Run
```zsh
% cd trend_crawling
% pip install requirements.txt
% python main.py
```