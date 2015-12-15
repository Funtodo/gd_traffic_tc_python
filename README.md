# gd_traffic_tc_python
- 来源：阿里天池，广东公共交通大数据竞赛
- 目的：熟悉Python，学会用Python进行数据处理（特征提取、特征选择），以及python的机器学习库scikit-learn的使用，Just Try。
- 初次上手，时间有限，最终成绩294/ 57.04%（总人数2734/82.22%）

<p>竞赛官网 <a href="http://tianchi.aliyun.com/competition/information.htm?spm=5176.100067.5678.2.3o7931&raceId=231514" title="阿里天池">
阿里天池-广东交通大数据竞赛</a></p>

## 竞赛题目
本次大赛要求选手根据广州市内及广佛同城公交线路的历史公交刷卡数据，挖掘固定人群在公共交通中的行为模式。建立公交线路乘车人次预测模型，并用模型预测未来一周（20150101-20150107）每日06时至21时每小时段各个线路的乘车人次。Part2将更换一批新数据。

大赛开放20140801至20141231五个月广东部分公交线路岭南通用户刷卡数据，共涉及近200万用户2条线路约800多万条数据记录。同时大赛提供20140801至20150131期间广州市的天气状况信息。

## 数据说明
- 乘车刷卡交易数据表（gd_train_data）
- 公交线路信息表（gd_line_desc）
- 广州市天气状况信息（gd_weather_report）
- 选手需要提交结果表（gd_predict.txt）

<p>
	乘车刷卡交易数据表（gd_train_data）</p>
<table border="1" cellpadding="0" cellspacing="0">
	<tbody>
		<tr>
			<td style="width:157px;">
				<p>
					列名</p>
			</td>
			<td style="width:140px;">
				<p>
					类型</p>
			</td>
			<td style="width:133px;">
				<p>
					说明</p>
			</td>
			<td style="width:128px;">
				<p>
					示例</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Use_city</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					使用地</p>
			</td>
			<td style="width:128px;">
				<p>
					广州</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Line_name</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					线路名称</p>
			</td>
			<td style="width:128px;">
				<p>
					线路1</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Terminal_id</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					刷卡终端ID</p>
			</td>
			<td style="width:128px;">
				<p>
					4589bb610f9be53a43a7bc26bb40e44d</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Card_id</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					卡片ID</p>
			</td>
			<td style="width:128px;">
				<p>
					8ce79e0b647053f191d20c5552eb49f0</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Create_city</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					发卡地</p>
			</td>
			<td style="width:128px;">
				<p>
					佛山</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Deal_time</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					交易时间(yyyymmddhh)</p>
			</td>
			<td style="width:128px;">
				<p>
					2014091008</p>
			</td>
		</tr>
		<tr>
			<td style="width:157px;">
				<p>
					Card_type</p>
			</td>
			<td style="width:140px;">
				<p>
					String</p>
			</td>
			<td style="width:133px;">
				<p>
					卡类型</p>
			</td>
			<td style="width:128px;">
				<p>
					学生卡</p>
			</td>
		</tr>
	</tbody>
</table>
<p>
	&nbsp;</p>
<p>
	公交线路信息表（gd_line_desc）</p>
<table border="1" cellpadding="0" cellspacing="0">
	<tbody>
		<tr>
			<td style="width:121px;">
				<p>
					列名</p>
			</td>
			<td style="width:95px;">
				<p>
					类型</p>
			</td>
			<td style="width:113px;">
				<p>
					说明</p>
			</td>
			<td style="width:236px;">
				<p>
					示例</p>
			</td>
		</tr>
		<tr>
			<td style="width:121px;">
				<p>
					Line_name</p>
			</td>
			<td style="width:95px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					线路名称</p>
			</td>
			<td style="width:236px;">
				<p>
					线路1</p>
			</td>
		</tr>
		<tr>
			<td style="width:121px;">
				<p>
					Stop_cnt</p>
			</td>
			<td style="width:95px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					线路站点数量</p>
			</td>
			<td style="width:236px;">
				<p>
					24</p>
			</td>
		</tr>
		<tr>
			<td style="width:121px;">
				<p>
					Line_type</p>
			</td>
			<td style="width:95px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					线路类型</p>
			</td>
			<td style="width:236px;">
				<p>
					广州市内/广州佛山跨区域</p>
			</td>
		</tr>
	</tbody>
</table>
<p>
	&nbsp;</p>
<p>
	广州市天气状况信息（gd_weather_report）</p>
<table border="1" cellpadding="0" cellspacing="0">
	<tbody>
		<tr>
			<td style="width:138px;">
				<p>
					列名</p>
			</td>
			<td style="width:77px;">
				<p>
					类型</p>
			</td>
			<td style="width:113px;">
				<p>
					说明</p>
			</td>
			<td style="width:236px;">
				<p>
					示例</p>
			</td>
		</tr>
		<tr>
			<td style="width:138px;">
				<p>
					Date_time</p>
			</td>
			<td style="width:77px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					日期</p>
			</td>
			<td style="width:236px;">
				<p>
					2014/8/1</p>
			</td>
		</tr>
		<tr>
			<td style="width:138px;">
				<p>
					Weather</p>
			</td>
			<td style="width:77px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					天气状况（白天/夜间）</p>
			</td>
			<td style="width:236px;">
				<p>
					小雨</p>
			</td>
		</tr>
		<tr>
			<td style="width:138px;">
				<p>
					Temperature</p>
			</td>
			<td style="width:77px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					气温（最高/最低）</p>
			</td>
			<td style="width:236px;">
				<p>
					36℃/26℃</p>
			</td>
		</tr>
		<tr>
			<td style="width:138px;">
				<p>
					Wind_direction_force</p>
			</td>
			<td style="width:77px;">
				<p>
					String</p>
			</td>
			<td style="width:113px;">
				<p>
					风向风力（白天/夜间）</p>
			</td>
			<td style="width:236px;">
				<p>
					无持续风向&le;3级/无持续风向&le;3级</p>
			</td>
		</tr>
	</tbody>
</table>
<p>
	&nbsp;</p>
<p>
	预测数据集为这些公交线路在20150101-20150107每个线路每日06时至21时各个小时段的乘车人次总和。（注：21时指的是<font color="#000000" face="Helvetica" style="font-size: 9pt; word-wrap: break-word; word-break: break-all; color: rgb(0, 0, 0); line-height: 18px; widows: auto; background-color: rgb(252, 252, 252);">21:0</font><font color="#000000" face="Helvetica" style="font-size: 9pt; word-wrap: break-word; word-break: break-all; color: rgb(0, 0, 0); line-height: 18px; widows: auto; background-color: rgb(252, 252, 252);">0-21</font><font color="#000000" face="Heiti SC" style="font-size: 9pt; word-wrap: break-word; word-break: break-all; color: rgb(0, 0, 0); line-height: 18px; widows: auto; background-color: rgb(252, 252, 252);">:</font><font color="#000000" face="Helvetica" style="font-size: 9pt; word-wrap: break-word; word-break: break-all; color: rgb(0, 0, 0); line-height: 18px; widows: auto; background-color: rgb(252, 252, 252);">59这个时间段</font>）</p>
<p>
	<span style="color:#f00;">选手需要提交结果表（gd_predict.txt）</span></p>
<table border="1" cellpadding="0" cellspacing="0">
	<tbody>
		<tr>
			<td style="width:140px;">
				<p>
					列名</p>
			</td>
			<td style="width:75px;">
				<p>
					类型</p>
			</td>
			<td style="width:113px;">
				<p>
					说明</p>
			</td>
			<td style="width:236px;">
				<p>
					示例</p>
			</td>
		</tr>
		<tr>
			<td style="width:140px;">
				<p>
					Line_name</p>
			</td>
			<td style="width:75px;">
				<p>
					string</p>
			</td>
			<td style="width:113px;">
				<p>
					线路名称</p>
			</td>
			<td style="width:236px;">
				<p>
					线路1</p>
			</td>
		</tr>
		<tr>
			<td style="width:140px;">
				<p>
					Deal _date</p>
			</td>
			<td style="width:75px;">
				<p>
					string</p>
			</td>
			<td style="width:113px;">
				<p>
					日期</p>
			</td>
			<td style="width:236px;">
				<p>
					20150101</p>
			</td>
		</tr>
		<tr>
			<td style="width:140px;">
				<p>
					Deal_hour</p>
			</td>
			<td style="width:75px;">
				<p>
					string</p>
			</td>
			<td style="width:113px;">
				<p>
					小时段</p>
			</td>
			<td style="width:236px;">
				<p>
					08</p>
			</td>
		</tr>
		<tr>
			<td style="width:140px;">
				<p>
					Passenger_count</p>
			</td>
			<td style="width:75px;">
				<p>
					bigint</p>
			</td>
			<td style="width:113px;">
				<p>
					乘车人次</p>
			</td>
			<td style="width:236px;">
				<p>
					1234</p>
			</td>
		</tr>
	</tbody>
</table>
