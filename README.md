## 推荐经典模型


### part1 召回

参考： 
* https://github.com/reczoo/Datasets 
* https://arxiv.org/pdf/2205.09626
* https://www.cnblogs.com/MTandHJ/p/16362042.html

论文： 
* BARS： https://arxiv.org/abs/2210.12922
* SimpleX https://arxiv.org/pdf/2109.12613

#### 1.1 召回数据集

* MovieLens1M： 包含6000个用户在近4000部电影上的1亿条评论。

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

* AmazonBooks： 包含 5w+ 用户和 9w+ 物品的 300w 交互信息

item_list.txt : org_id remap_id
user_list.txt : org_id remap_id

数据预处理：
用户和物品ID映射: 将用户和物品ID转换为连续的数字ID
去重和过滤： 去除重复的交互记录和过滤掉低频用户或物品
生成交互记录： 遍历用户和他们的交互记录，生成用户-物品对，每一行代表一个用户与一个物品的交互。

格式化输出： user_id item_id_1 item_id_2 ... item_id_n -> train.txt test.txt

* Yelp18： 3.8w users 和 156w items， 124w 次交互

Yelp数据集主要由三部分组成:

交互（interaction）数据文件： review_id、user_idbusiness_id、stars ...

商品（item）数据文件： business_id、item_name、address、city ...

用户（user）数据文件: user_id、user_name...


* Gowalla： 3w用户、4w item、103w 次交互

Gowalla 是一个基于位置的社交网站, 用户可以在其中通过签到来分享他们的位置. 此社交网络是无向的, 使用公共 API 所收集, 由 196,591 个节点和 950,327 个边组成. 在 2009 年 2 月至 2010 年 10 月期间，我们共收集了这些用户的 6,442,890 次签到。

用户 ID、地点 ID、签到时间、地点...

#### 1.2 召回算法

1. 协同过滤
根据用户之前的喜好以及其他兴趣相近的用户的选择来给用户推荐物品。

* UserCF

基于用户的协同过滤，先找到和用户A有相似兴趣的其他用户，将共同兴趣用户喜欢的，但用户A未交互过的物品推荐给A。

实现： 构建共现矩阵； 计算用户向量之间相似度；根据相似用户的相似度和评分加权求和得到目标用户评分；

特点：适用于社交特性场景，兴趣点分散，如新闻推荐

* ItemCF

### part2 排序

#### 1.2  排序数据集

