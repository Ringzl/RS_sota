## 推荐经典模型


### part1 数据集

参考： https://github.com/reczoo/Datasets https://arxiv.org/pdf/2205.09626

论文： SimpleX https://arxiv.org/pdf/2109.12613

#### 1.1 召回数据集

* MovieLens1M
包含6000个用户在近4000部电影上的1亿条评论。

```
ml-1m
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
包含 5w+ 用户和 9w+ 物品的 300w 交互信息

item_list.txt : org_id remap_id
user_list.txt : org_id remap_id

数据预处理：
用户和物品ID映射: 将用户和物品ID转换为连续的数字ID
去重和过滤： 去除重复的交互记录和过滤掉低频用户或物品
生成交互记录： 遍历用户和他们的交互记录，生成用户-物品对，每一行代表一个用户与一个物品的交互。

格式化输出： user_id item_id_1 item_id_2 ... item_id_n


* Yelp18

* Gowalla



#### 1.2  排序数据集