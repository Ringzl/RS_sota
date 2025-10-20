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

0. **指标**

$R(u)$ 根据用户在训练集上的行为给用户做出的推荐列表

$T(u)$ 用户在测试集上的行为列表

（1）Recall

$$
Recall = \frac{\sum_{u\in U}|R(u) \cap T(u)|}{\sum_{u \in U}|T(u)|}
$$

样本中的正例有多少被预测正确, 表示用户的喜好被捕捉到的能力

（2）Precision

$$
Precision = \frac{\sum_{u\in U}|R(u) \cap T(u)|}{\sum_{u \in U}|R(u)|}
$$

预测样本为正的样本中有多少是真正的正样本,衡量召回的结果中用户偏好的程度


$$
Precision@K = \frac{\sum_{u\in U}|R(u)@K \cap T(u)|}{K}
$$

表示返回K个召回结果时的精确度

（3）F1

$$
F1 = \frac{2*Precision}{Precision + Recall}
$$

作为Recall和Precision的一种权衡, 调和平均

（4）HitRate

$$
HitRate@K = \frac{NumberofHits@K}{|GT|} 
$$

表示召回的K个item是否包含用户后续会点击的item，有记为1,否则为0（测试集中的item出现在Top-N推荐列表中的用户数量），最后求sum(hit) / 总用户数；

（5）NDCG

NDCG 考虑的是评分的排序，推荐 K 个物品：

$$
CG_k = \sum_{i=1}^k rel_i
$$

$rel_i$ 是第i个物品的相关性/评分，考虑物品顺序（DCG）

$$
DCG_k = \sum_{i=1}^k\frac{2^{rel_i}-1}{log_2(i+1)}
$$

考虑推荐列表与检索真正有效结果个数：

$$
NDCG_k = \frac{DCG_k}{IDCG_k}
$$

IDCG 与真实评分排序一致，NDCG为0到1的数，越接近1推荐越准确。

1. **协同过滤 （CF）**
根据用户之前的喜好以及其他兴趣相近的用户的选择来给用户推荐物品。

* UserCF

基于用户的协同过滤，先找到和用户A有相似兴趣的其他用户，将共同兴趣用户喜欢的，但用户A未交互过的物品推荐给A。

$$ R_{\mathrm{u}, \mathrm{p}}=\frac{\sum_{\mathrm{s} \in S}\left(w_{\mathrm{u}, \mathrm{s}} \cdot R_{\mathrm{s}, \mathrm{p}}\right)}{\sum_{\mathrm{s} \in S} w_{\mathrm{u}, \mathrm{s}}} $$

 $$ R_{\mathrm{u}, \mathrm{p}}=\bar{R}{u} + \frac{\sum{\mathrm{s} \in S}\left(w_{\mathrm{u}, \mathrm{s}} \cdot \left(R_{s, p}-\bar{R}{s}\right)\right)}{\sum{\mathrm{s} \in S} w_{\mathrm{u}, \mathrm{s}}} $$

实现： 构建共现矩阵； 计算用户向量之间相似度；根据相似用户的相似度和评分加权求和得到目标用户评分；

特点：适用于社交特性场景，兴趣点分散，如新闻推荐

* ItemCF

基于物品的协同过滤，根据所有用户的历史行为数据，计算物品之间的相似性，把与用户A喜欢的物品的相似物品推荐给用户。

实现：构建共现矩阵；计算物品向量之间的相似度；根据目标用户历史行为中的正反馈物品，找到Top k个相似物品。

特点：适用兴趣变化稳定的场景，如电商推荐、视频推荐。

itemKNN和userKNN：分别是基于item和user相似度的KNN推荐，即由k个最相近的user或item的评分决定某个用户对某个物品的未知评分。

权重改进：
（1）热门物品与任何物品的相似度都很高

对热门物品进行惩罚，控制惩罚力度：

$$ w_{i j}=\frac{|N(i) \cap N(j)|}{|N(i)|^{1-\alpha}|N(j)|^{\alpha}} $$

对活跃用户进行惩罚：

 $$ w_{i j}=\frac{\sum_{\operatorname{\text {u}\in N(i) \cap N(j)}} \frac{1}{\log 1+|N(u)|}}{|N(i)|^{1-\alpha}|N(j)|^{\alpha}} $$


2. **矩阵分解（MF）**

为了使得协同过滤更好处理稀疏矩阵问题，增强泛化能力。从协同过滤中衍生出矩阵分解模型(Matrix Factorization, MF)或者叫隐语义模型。

MF:
基于评分矩阵，将其分解成Q和P两个矩阵乘积的形式，获取用户兴趣和物品的隐向量表达。基于两个分解矩阵去预测某个用户对某个物品的评分，再进行物品推荐。

$$
\operatorname{score}(u, i)=r_{u i}=p_{u}^{T} q_{i}=\sum_{k=1}^{K} p_{u, k} q_{i,k}
$$

求解： 特征值分解（EVD）或 奇异值分解（SVD）

EVD 只能分解方阵，SVD 要求原始矩阵是稠密，但是现实中用户的评分矩阵是非常稀疏的。

FunkSVD： 转成最优化问题，初始化一个用户矩阵和物品矩阵，对评分矩阵的每个元素，计算SSE误差，通过梯度下降最小化预测误差损失 + l2正则。

BiasSVD： 加入偏置项，消除用户和物品的打分偏差。

$$
\hat{r}_{u i}=\mu+b_{u}+b_{i}+p_{u}^{T} \cdot q_{i}
$$

优化目标：

$$
\begin{aligned}
\min _{q^{*}, p^{*}} \frac{1}{2} \sum_{(u, i) \in K} &\left(r_{u i}-\left(\mu+b_{u}+b_{i}+q_{i}^{T} p_{u}\right)\right)^{2} \\
&+\lambda\left(\left\|p_{u}\right\|^{2}+\left\|q_{i}\right\|^{2}+b_{u}^{2}+b_{i}^{2}\right)
\end{aligned}
$$

### part2 排序

#### 1.2  排序数据集

