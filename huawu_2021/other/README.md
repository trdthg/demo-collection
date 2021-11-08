# Post_Classification 文章分类系统

## 文件

### Dictionnary_Builder.py

构建词库和各类文章的平均向量

### Post_Classify.py

将未分类的文章和各类文章的平均向量进行比对

## 数据库表

### article

未分类的文章，字段最低需求：

- **id 	int	非空	键**

- **category	varchar	可空**

- **content	longtext	非空**

### article_category_data

已分类的文章，字段最低需求：

- **id 	int	非空	键**
- **category	varchar	非空**

- **content	longtext	非空**

- **weight	longtext	可空**

## article_category_weight

各类文章的平均向量，字段最低需求：

- **id	int	非空	键**

- **category	varchar	非空**

- **category_weight	longtext	非空**

## article_dictionary

词库，字段最低需求：

- **id	int	非空	键**

- **dictionary	longtext	非空**

tips: 

- **由于大部分代码和 id 绑定在一起，如果原数据库表有数据可能会有bug存在**
- **代码中的分类可调，相应的已分类的文章需要提供**