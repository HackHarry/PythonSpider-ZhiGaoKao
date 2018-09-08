# ZhiGaokaoSpider

# 介绍
[智高考](http://www.zhigaokao.cn/)是一个高考志愿网站，也是基于Ajax的。高中的时候我在wyz大神的帮忙下，尝试过爬取信息来为填志愿做准备。但是当时没有系统学习过爬虫，几乎都是靠大神带飞，因此今天再次尝试爬取智高考的大学信息。（数据全部基于智高考，侵删）
该网站有多种查询模式，我打算爬取的有两种。
1.各省份的本科大学
2.各学科的本科大学

# 正文

**各省份的本科大学**

首先分析Ajax，可以看到URL为：
```
http://www.zhigaokao.cn/university/getRemoteUniversityList.do?userKey=www&req=ajax&universityName=&areaid=110000&type=&educationLevel=1&property=&offset=0&rows=10
```
其中universityName、type、property均可省略，因为我们没有传入数据。然后通过字面翻译可以知道，areaid是地区代码的意思，也就是代表着各个省份（直辖市）。这里可以选择网上搜索所有省份代码，预处理弄好，这也是我曾经的做法。但是今天我打算直接从网站上爬取所有省份代码。
直接刷新界面，可以看到有好几条xhr信息，仔细观察就能发现其中一条就是存着省份代码的信息。
![](https://images2018.cnblogs.com/blog/1318960/201809/1318960-20180908185300820-40630523.png)
接下来事情就简单了，用requests读取信息，然后解析就可以了，代码如下
```
def get_id():
	url = 'http://www.zhigaokao.cn/university/getRemoteProvinceList.do?'
	payload = {
			'userKey': 'www',
			'req': 'ajax',
		}
	response = requests.get(url, headers=headers, params=payload)
	items = response.json().get('bizData')
	IDs = []
	for item in items:
		IDs.append(item.get('id'))
	return IDs
```
获取省份代码之后，就可以传入之前的params中，通过offset来爬取所有信息。

**各学科的本科大学**

这里比较麻烦的如何传递专业。按照智高考的专业分级有三级，因此我打算一二级用文件夹的形式存，三级作为文件的命名。总的思路和上面的类似，就不细细赘述了。我遭遇到的主要问题就是json结构层次太多，经常会搞晕，然后我没有一开始定下怎么按层次解析，因此踩了不少坑。说到底应该算是基础不扎实、代码量太少的原因吧。
![](https://images2018.cnblogs.com/blog/1318960/201809/1318960-20180908185928616-150910587.png)
还有要提及的一点是，我本打算先爬取所有专业大类存在list里，然后发现这样和最后的学校不容易匹配上，发现最终的json中其实也有专业大类的名称，因此又重新修改了代码，改为直接解析学校的URL。

# 总结
通过这次实践，解决了曾经遗留的一些问题，也搞清楚如何解决Ajax的问题了。不过也发现了一些还不够的地方。一个是事先对代码的结构没有考虑清楚，导致多次重构代码，浪费了不少时间；另一个是python基础不够扎实，对list之类的基本数据结构运用的不熟练。
本次实践代码开源在[github](https://github.com/HackHarry/ZhiGaokaoSpider)
