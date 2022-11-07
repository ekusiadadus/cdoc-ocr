# Get Started

.env に、GOOGLE_APPLICATION_CREDENTIALS へのパスを入れる

```
poetry shell
```

```
poetry install
```

```
export $(cat .env | grep -v ^# )
```

```
make pdf
```

```
make csv
```

## change table flavor

If you want to change table flavor, you can change

https://github.com/ekusiadadus/cdoc-ocr/blob/dcdd47b29f50c3bdcc9ae2a03fa3e1a1731563f9/pdf2doc.py#L8-L9
