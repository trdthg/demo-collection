# RustWriter
这是一个用Rust语言编写的静态博客生成工具。追求简单、自由、快乐。

### 文件结构
``` s
+-- main.rs
+-- lib.rs
+-- cli.yml
+-- util
	+-- path.rs
	+-- file.rs
```

```  s
+-- docs
	+-- .config
		+-- components
		+-- dist
		+-- public
		+-- styles
		+-- config.json
	+-- xxx
	+-- xxx.md
	+-- README.md
+-- deploy.sh
+-- deploy.cmd
```

``` s
+-- assets
	+-- js
	+-- css
	+-- img
+-- xxx
+-- xxx
+-- xxx
+-- index.html
```

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

### 安装
1. 源码方式安装
    - 下载源代码
	```
	git clone https://github.com/tjz101/rsw.git
	cd rsw
	```
    - 编译代码
	```
	cargo build --release
	```
    - Linux 安装
	```
	sudo cp target/release/rsw /usr/local/bin/
	```
2.  二进制方式安装
    - 从 [release](https://github.com/tjz101/rsw/releases) 页面中下载对应平台的可执行文件压缩包解压后就可以使用。
	
    - 为方便使用，可以将rsw添加到环境变量中 或者 Linux系统将rsw文件放到/usr/local/bin，Windows系统将rsw.exe放到C:\Windows\System32中。

### 使用

- rsw -h 查看帮助
- rsw -V 显示版本信息
- rsw new project 创建一个静态博客项目
- rsw build 编译src目录下的文件到build

### 部署
将build目录下的文件上传到你的服务器就可以了。

### 案例

### 感悟

### 特别说明
