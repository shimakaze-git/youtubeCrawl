import oseti

analyzer = oseti.Analyzer()

score = analyzer.analyze('天国で待ってる。')
# => [1.0]
print('score', score)

score = analyzer.analyze('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
# => [0.3333333333333333, 1.0]
print('score', score)

count_polarity = analyzer.count_polarity('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
print('count_polarity', count_polarity)

analyze_detail = analyzer.analyze_detail('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
print('analyze_detail', analyze_detail)
