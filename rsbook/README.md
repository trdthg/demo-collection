# RsBook
这是一个用Rust语言编写的静态博客生成工具, 参考了RustWritter
仅仅作为练习使用， 几乎没有参考价值 /doge

## 项目结构
参考自 vuepress
``` js
{
	title: 'Trdthg\'s blog',
    head: [ // 注入到当前页面的 HTML <head> 中的标签
      	['link', { rel: 'icon', href: 'logo.png' }], // 增加一个自定义的 favicon(网页标签的图标)
    ],
    description: '我的个人网站',
    base: '/', // 这是部署到github相关的配置
    markdown: {
      	lineNumbers: false // 代码块显示行号
    },
    plugins: ['@vuepress/last-updated'],
    themeConfig: {
		lastUpdated: 'Last Updated', // string | boolean
		sidebarDepth: 3, // 侧边栏显示2级
		sidebar: {
			'/java/': ['java', 'sourceread', 'spring', 'springboot', 'stuffs'],
			'/js/': ['js', 'vue'],
			'/python/': ['python'],
			'/rust/': ['rust', 'lists', 'wasm'],
			'/other/': ['other', 'script', 'datastructure'],
			'/': [''] //不能放在数组第一个，否则会导致右侧栏无法使用 
	}, // 侧边栏配置
	nav:[ // 导航栏配置
		{text: 'Java',  link: '/java/java'},
		{text: '前端', link: '/js/js' },
		{text: 'Python', link: '/python/python'},
		{text: 'Rust', link: '/rust/rust' },
		{text: '其他', link: '/other/other'},
		{text: 'Github', link: 'https://github.com/trdthg'}      
	],
}
```

## 安装
- 下载源代码
```sh
mkdir models # 创建一个与要clone的仓库同名或不同命的目录
cd models
git init #初始化
git remote add origin https://github.com/trdthg/demo-collection.git # 增加远端的仓库地址
git config core.sparsecheckout true # 设置Sparse Checkout 为true 
echo "self_rsbook_2021" >> .git/info/sparse-checkout # 将要部分clone的目录相对根目录的路径写入配置文件
# echo "research/deeplab" >> .git/info/sparse-checkout # 将要部分clone的目录相对根目录的路径写入配置文件
git pull remotebranch mybranch #pull下来代码
```

## 使用
- cargo run new xxx
- cargo run build xxx
- rsw new xxx 创建一个静态博客项目
- rsw build xxx 编译src目录下的文件到dist

## 部署
暂时只有静态文件

## BUG
prime.js 和 prime.css没有正常被复制到dist文件夹内，因此排版不正常，手动添加即可
