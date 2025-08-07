## 推荐经典模型


### part1 数据集

参考： https://github.com/reczoo/Datasets https://arxiv.org/pdf/2205.09626

论文： SimpleX https://arxiv.org/pdf/2109.12613

#### 1.1 召回数据集

* MovieLens1M
包含6000个用户在近4000部电影上的1亿条评论。

```
MovieLens1M_1m
    ├── movies.dat // 电影数据
    ├── ratings.dat // 评分数据
    ├── README
    └── users.dat // 用户数据
```
> 用户数据
用户ID、性别、年龄、职业ID和邮编等字段。
数据格式：UserID::Gender::Age::Occupation::Zip-code

> 电影数据
电影ID、电影名和电影风格等字段。
数据格式：MovieID::Title::Genres

> 评分数据
用户ID、电影ID、评分和时间戳等字段。
数据格式：UserID::MovieID::Rating::Timestamp

* AmazonBooks

* Yelp18

* Gowalla



#### 1.2  排序数据集