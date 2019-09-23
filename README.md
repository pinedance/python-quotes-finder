# Quotes Finder

When writing in East Asia, the author wrote and quoted from the authoritative books of earlier times. These citations were a means of justifying one's opinion as an important basis for assertion.

Many scholars who study East Asia books or texts today do not remember as extensive a literature as in the past. Therefore, when citations are not explicitly expressed in the literature, there are many cases in which the citations are not read and the reading is not read.

This project is to __extract the citation relationship between the texts in Chinese.__

We used the algorithm [Smith-Waterman](https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm) as a way to find similar parts of texts. It is a method of finding similar strings through mutual comparison by letter It's a good way to get the results you want, but it takes a lot of time to compute because it contrasts letters one by one.

## Usage

```
python qtfinder.py [REF_TEXT] [TRG_TEXT] {[OUTPUT]}
```

The argument used means:

* `[REF_TEXT]`: Reference Text
* `[TRG_TEXT]`: Target Text. These texts should be utf-8 encoded electronic files.
* `[OUTPUT]`: Name of the folder to save the results. it can be omitted.

If you do not have python installed, you can use precompiled files in the `./dist` folder.

```
# windows
dist\qtfinder.exe [REF_TEXT] [TRG_TEXT] {[OUTPUT]}
```

## Test

If you don't have sample files now, you can try this package using our sample data.

```
python qtfinder.py tests\DATA\SOMUN.SAMPLE.txt tests\DATA\DYBG.SAMPLE.txt
```

```
# windows
dist\qtfinder.exe tests\DATA\SOMUN.SAMPLE.txt tests\DATA\DYBG.SAMPLE.txt
```

## Install

This package is optimized for Python 3.6. If you are using the latest python 3.7x, some dependencies may not work properly.

* regex
* blist
* tqdm


```
pip install -r requirements.txt
# or
conda install --file reqiurements.txt
```


## License

MIT License


***

# Quotes Finder

동아시아에서는 저술을 할 때 앞선 시대의 권위 있는 서적의 내용들을 즐겨 인용하며 글을 써 내려갔다. 이 인용문들은 주장의 중요한 근거로서 자시의 의견을 정당화하는 수단이었다.

오늘날 이를 연구하는 학자들은 과거와 같이 폭넓은 문헌을 기억하고 있지 못한 경우가 많다. 따라서 문헌 내에서 명시적으로 인용관계를 표현하고 있지 않은 경우, 인용 관계를 모르고 독해를 하는 경우가 적지 않다.

본 프로젝트는 한문으로 이루어진 텍스트 사이의 인용 관계를 추출하기 위한 것이다.

중복된 부분을 찾는 방법으로 [Smith-Waterman](https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm) 알고리즘을 사용하였다. 글자의 일치, 추가, 삭제에 대한 점수를 부여하여 글자 단위로 상호 비교를 통해 유사한 문자열을 찾는 방법이다. 원하는 결과를 도출할 수 있는 좋은 방법이지만, 글자와 글자를 하나 하나 대조하기 때문에 연산에 많은 시간이 소요된다.

## Usage

사용법은 다음과 같다.

```
python qtfinder.py [REF_TEXT] [TRG_TEXT] {[OUTPUT]}
```

사용된 인자는 다음을 의미한다.

* `[REF_TEXT]`: 인용된 텍스트
* `[TRG_TEXT]`: 인용한 텍스트. 이 텍스트들은 utf-8로 인코딩된 전자파일을 가정한다.
* `[OUTPUT]`: 결과를 저장할 폴더 이름이며, 생략 가능하다.


python이 설치되어 있지 않다면, `dist` 폴더 안에 미리 컴파일 된 파일을 사용할 수 있다.

```
dist\qtfinder.exe [REF_TEXT] [TRG_TEXT] {[OUTPUT]}
```

## Test

당장 검토해 볼 파일이 없다면 sample data를 이용해 시험해 볼 수 있다.

```
python qtfinder.py tests\DATA\SOMUN.SAMPLE.txt tests\DATA\DYBG.SAMPLE.txt
```

```
dist\qtfinder.exe tests\DATA\SOMUN.SAMPLE.txt tests\DATA\DYBG.SAMPLE.txt
```

sample data는 다음과 같다.

* SOMUN.SAMPLE.txt : 황제내경 소문 1편
* DYBG.SAMPLE.txt : 동의보감 신형문~기문까지

## Install

Python 3.6에 최적화 되어 있다. 최신 python 3.7x를 사용할 경우 package들이 정상작동하지 않을 수 있다.

* regex
* blist
* tqdm


```
pip install -r requirements.txt
# or
conda install --file reqiurements.txt
```


## License

MIT License
