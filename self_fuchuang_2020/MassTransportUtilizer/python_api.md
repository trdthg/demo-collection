## 可修改参数的预测

<u>注: 以下均为data, 没有code, msg等信息, 也没有登陆验证等信息</u>

##### 请求URL 

`http://localhost:9999/python/predict`

这仨只是把三项预测项目分开了, 传递的参数不用变

`http://localhost:9999/python/list1`

`http://localhost:9999/python/list4`

`http://localhost:9999/python/list3`

##### 请求参数

```json
{
	# 必选
    无
    
    # 可选

    time: 'month:day:hour:minute'
    	//表示多久后有人群涌入  比如3小时后学校放假
    dayprop: 1, 
    	//[0,1,2]表示是否放假
    weather: ['多云', '晴'], 
    	//分别为上午下午
    	//['多云', '中雨', '阴', '晴', '雷阵雨', '暴雨', '大雨', '小雨']
    temperatures: [9, 22], 
    	//最低气温,最高气温
    station: {
        # 必选
 		name: 'Sta65',
        # 可选
  		flow: [30, 0],
		// flow 和 flow_type 合并了 
         //[0,1,2,3] 表示 in_flow, out_flow, in_flow_plus, out_flow_plus
         type: 1, 
         //[0,1]表示是否为换乘站
         station_classify: 3, 
         //[0,1,2,3,4]表示站点分类
    }
}
```

##### 返回值

```json
{
	list1: [  
        {
            station: 'Sta65',
            flow: [1,1,7,6],  //表示 in_flow, out_flow, in_flow_plus, out_flow_plus
            turn: 1, //现在是7:10, 则 0为7:30, 1为8:00, 2为8:00, 以此类推
        }
    ],
    list3: [  
        {
            station1: 'Sta64',   
            station2: 'Sta65',
            flow: 34,  //从station1 -> station2 间的flow
            turn: 5
        },
    ],
    list4: [
        {
            line: '3号线',
            flow: 79,
            turn: 8
        }
    ]
}
```



## 年龄结构分析 (别看)

##### 返回值

```json
{
	'station': 'Sta65'  //进站
	'time': '6-1'
    0: [0~16, 16~25, 25~40, 40~60, 60~],
	1: [],
	2: [],

}
{
	'station': 'Sta65'   //出站
	'time': '6-1'
    0: [0~16, 16~25, 25~40, 40~60, 60~],
	1: [],
	2: [],

}

```

## 预测行程花费时间

##### 请求URL

`http://localhost:9999/python/dettime`

##### 请求参数

```json
{
	'stationin': 'Sta65',
	'stationout': 'Sta128',
	'month': 5,
	'hour': 11,    //几点进去
	'dayprop': 1,  //放假情况
}
```

##### 返回值

```json
{
	'dettime': 12  //分钟
}
```

