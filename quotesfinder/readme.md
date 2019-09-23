From finder.SmithWaterman.v2

인용 구문 찾기 ( feat. Smith-Waterman )

한의학 서적에는 많은 구문들이 상호 인용 관계를 맺고 있다. 이런 인용구문들은 명시적인 경우도 있지만 그렇지 않은 경우도 있다. 후자의 경우 이를 알아차리는 것은 매우 어렵다. 전자의 경우라 하더라도 어디까지 인용되었는지 모호한 경우가 많기 때문에 원문을 찾고 확인해야 하는 경우가 많다.

2가지 텍스트가 주어졌을 때, 상호 인용관계를 맺는 구문을 자동으로 찾는 방법을 모색해 보았다.

텍스트는 편의상 참조된 텍스트(REF), 참조한 텍스트(TRG)으로 구분할 수 있다. REF는 시대적으로 더 앞선 문헌으로 TRG가 이를 참고하여 구문을 인용할 수 있어야 한다.

TRG는 REF의 여러 부분을 인용할 수 있다. 따라서 최종 인용구문 결과에서 TRG의 구절은 중복되는 부분이 있어서는 안되지만, REF의 구절은 중복이 발생할 수도 있다. 중복된 부분은 2번 이상 인용된 부분이다.

중복된 부분을 찾는 방법으로 Smith-Waterman 알고리즘을 사용하였다. 글자의 일치, 추가, 삭제에 대한 점수를 부여하여 글자 단위로 상호 비교를 통해 유사한 문자열을 찾는 방법이다. 원하는 결과를 도출할 수 있는 좋은 방법이지만, 글자와 글자를 하나 하나 대조하기 때문에 연산에 많은 시간이 소요된다.


### Build

```
# ./
pyinstaller qtfinder.py --onefile
# pyinstaller qtfinder.py --onefile --exclude numpy

# or
pyinstaller qtfinder.spec
```
### dist

Generating distribution archives

```
# python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```

Uploading the distribution archives

```
# conda install -c conda-forge twine
# python -m pip install --user --upgrade twine

# test
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

```
python -m twine upload --repository-url https://pypi.org/legacy/ dist/*
```


### Test

```
python qtfinder.py tests\DATA\SOMUN.SAMPLE.txt tests\DATA\DYBG.SAMPLE.txt
```

```
# ./
# linux
dist/qtfinder tests/DATA/SOMUN.SAMPLE.txt tests/DATA/DYBG.SAMPLE.txt

# windows
dist\qtfinder.exe tests\DATA\SOMUN.SAMPLE.txt tests\DATA\DYBG.SAMPLE.txt
```


### REF

#### Algorithm

https://tiefenauer.github.io/blog/smith-waterman/

#### Code

* pyinstaller : https://realpython.com/pyinstaller-python/
