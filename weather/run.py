# --coding: utf-8 --
"""
   Created by Lin Vision at 2021/11/17.
   Copyright (c) 2013-present, XiaMen DianChu Technology Co.,Ltd.
   Description:
   Changelog: all notable changes to this file will be documented
"""
import pytz, datetime
import requests, json, re
from bs4 import BeautifulSoup
from dataclasses import dataclass

html = '''
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="renderer" content="webkit">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1" ><meta http-equiv="Cache-Control" content="no-siteapp" />
    <link href="https://static.nowapi.com/style/bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" rel="stylesheet"/>
    <link href="https://www.nowapi.com/style/css/api.css?20200811" type="text/css" rel="stylesheet"/>
    <script type="text/javascript" src="https://static.nowapi.com/style/jquery/1.11.3/jquery.min.js"></script>
    <script type="text/javascript" src="https://static.nowapi.com/style/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <title>实时天气接口  - 数据接口 - NowAPI</title>
</head>
<body>
<div class="header">
    <div class="header-auto">
        <div class="header-body">
            <div class="logo"><a href="https://www.nowapi.com"><img src="https://www.nowapi.com/style/img/logo.png"></a></div>
            <div class="nav"><h2><a href="https://www.nowapi.com">首页</a></h2><h2 class="active"><a href="https://www.nowapi.com/api">API</a></h2><h2><a href="https://www.nowapi.com/mail">邮件</a></h2><h2><a href="https://www.nowapi.com/article">动态</a></h2><h2><a href="https://www.nowapi.com/?app=control">控制台</a></h2></div>
            <div class="login"><a href="https://www.nowapi.com/?app=account.login">登录</a> <a href="https://www.nowapi.com/?app=account.register">注册</a></div>
        </div>
    </div>
</div>

<div class="api-lista">
    <div class="api-lista-auto">
        <div class="api-lista-body">
            <div class="cdetail">
                <div class="cdetail-intimg"><img src="https://static.nowapi.com/nowapi/upload/api/weather.png"></div>
                <div class="cdetail-intrem">
                    <div class="title"><h1>实时天气</h1></div>
                    <div class="remark">查询国内城市气象数据，同时也支持国外热门城市查询</div>
                    <div class="param">
                        <table>
                            <tr><td>接口编号: 506</td><td>接口名称: 天气预报</td><td>连接应用: 8179个</td></tr>
                            <tr><td>应用编号: 106004</td><td>应用标识: weather.today</td><td>服务商: NowAPI</td></tr>
                        </table>
                    </div>
                </div>
                <div class="cdetail-intbut">
                    <a target="_blank" class="btn btn-primary" href="https://www.nowapi.com/?app=buy.setmealNew&action=new&intid=506">立即开通</a>
                </div>
            </div>
            <div class="cdetail">
                <ul class="nav nav-tabs" role="tablist"><li role="presentation" class="active"><a href="#doc" aria-controls="doc" role="tab" data-toggle="tab">接口文档</a></li><li role="presentation"><a href="#cost" aria-controls="cost" role="tab" data-toggle="tab">套餐费用</a></li><li role="presentation"><a href="#other" aria-controls="other" role="tab" data-toggle="tab">其它相关</a></li></ul><div class="tab-content"><div role="tabpanel" class="tab-pane active" id="doc"><div class="cdetail-reqnav"><a href="https://www.nowapi.com/api/weather.realtime"> 天气预报(整合版)</a><a href="https://www.nowapi.com/api/weather.future"> 天气预报(5-7天)</a><a class="active" href="https://www.nowapi.com/api/weather.today"> 实时天气</a><a href="https://www.nowapi.com/api/weather.realtimeBatch"> 实时天气(批量)</a><a href="https://www.nowapi.com/api/weather.history"> 历史天气</a><a href="https://www.nowapi.com/api/weather.pm25"> PM2.5 AQI</a><a href="https://www.nowapi.com/api/weather.lifeindex"> 生活指数(5-7天)</a><a href="https://www.nowapi.com/api/weather.city"> 城市列表</a><a href="https://www.nowapi.com/api/weather.wtype"> 天气类型</a></div>
            <div class="cdetail-reqbody">
                <div class="item"><p>说明</p><pre>实时天气信息，每小时更新一次

更新日志:
2015-05-13 weaid参数可指定IP地址（系统会分析该IP所在城市，并提取该城市天气数据）
2015-01-01 增加实时湿度 temperature_curr和temp_curr栏位.
2018-04-13 增加aqi pm2.5字段.

<b>测试示例:</b> <a target="_blank" href="http://api.k780.com/?app=weather.today&weaId=1&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json">http://api.k780.com/?app=weather.today&weaId=1&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json</a> (示例中sign会不定期调整)</pre></div><div class="item"><p>调用方式</p><pre>Get/Post</pre></div><div class="item"><p>请求url</p><pre><b> HTTP:</b> http://api.k780.com<br><b>HTTPS:</b> https://sapi.k780.com<br></pre></div><div class="item">
                    <p>请求参数</p>
                    <table class="table table-striped" style="font-size:12px;">
                        <thead>
                            <tr>
                                <th width="15%">参数</th>
                                <th width="15%">类型</th>
                                <th width="10%">是否必须</th>
                                <th>备注</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                        <td>weaId</td>
                        <td>string</td>
                        <td>是</td>
                        <td>通过weaId查询，例: 1 <br>城市列表<a href="https://www.nowapi.com/api/weather.city">城市列表</a>中weaId<br>(参数weaId,cityId,cityNm,cityIp,wgs84ll中取1个作为查询条件)</td>
                    </tr><tr>
                        <td>cityId</td>
                        <td>number</td>
                        <td>否</td>
                        <td>通过气象局编号查询，例: 101010100 <br>城市列表<a href="https://www.nowapi.com/api/weather.city">城市列表</a>中cityId</td>
                    </tr><tr>
                        <td>cityNm</td>
                        <td>string</td>
                        <td>否</td>
                        <td>通过中文城市名查询，例: 北京 <br>城市列表<a href="https://www.nowapi.com/api/weather.city">城市列表</a>中cityNm (带入前urlencode)</td>
                    </tr><tr>
                        <td>cityIp</td>
                        <td>string</td>
                        <td>否</td>
                        <td>通过ip地址查询，例: 202.104.153.201 </td>
                    </tr><tr>
                        <td>wgs84ll</td>
                        <td>string</td>
                        <td>否</td>
                        <td>通过经纬度坐标查询，例:116.442708,39.917344 <br>（付费用户可用）</td>
                    </tr><tr>
                        <td>appkey</td>
                        <td>string</td>
                        <td>是</td>
                        <td>使用API的唯一凭证 <a href="https://www.nowapi.com/?app=intf.appkey">获取</a></td>
                    </tr><tr>
                        <td>sign</td>
                        <td>string</td>
                        <td>是</td>
                        <td>md5后的32位密文,登陆用. <a href="https://www.nowapi.com/?app=intf.appkey">获取</a></td>
                    </tr><tr>
                        <td>format</td>
                        <td>{json|xml}</td>
                        <td>否</td>
                        <td>返回数据格式</td>
                    </tr><tr>
                        <td>jsoncallback</td>
                        <td>string</td>
                        <td>否</td>
                        <td>js跨域使用jsonp时可使用此参数</td>
                    </tr>
                        </tbody>
                    </table>
                </div><div class="item"><p>Json请求示例</p><pre>http://api.k780.com/?app=weather.today&weaId=1&appkey=APPKEY&sign=SIGN&format=json</pre></div><div class="item"><p>Json返回示例</p><pre>1.正常返回
{
    "success": "1",
    "result": {
        "weaid": "1",
        "days": "2014-07-30",
        "week": "星期三",
        "cityno": "beijing",
        "citynm": "北京",
        "cityid": "101010100",
        "temperature": "31℃/24℃", /*当日温度区间 (注: 夜间只有一个温度如24℃/24℃)*/
        "temperature_curr": "21℃", /*当前温度*/
        "humidity": "50%",/*湿度*/
        "aqi": "100",/*pm2.5 说明详见<a href="https://www.nowapi.com/api/weather.pm25">weather.pm25</a>*/
        "weather": "多云转晴", /*天气*/
        "weather_icon": "http://api.k780.com/upload/weather/d/1.gif", /*气象图标 <a target="_blank" href="http://static.nowapi.com/download/weather_icon.zip">全部气象图标下载</a>*/
        "weather_icon1": "", /*无意义不必理会*/
        "wind": "微风",/*风向*/
        "winp": "小于3级", /*风力*/
        "temp_high": "31", /*最高温度*/
        "temp_low": "24", /*最低温度*/
        "humi_high": "87.8", /*最大湿度 [历史遗留栏位不再更新]*/
        "humi_low": "75.2", /*最小湿度 [历史遗留栏位不再更新]*/
        "weatid": "2", /*天气ID，可对照<a target="_blank" href="https://www.nowapi.com/api/weather.wtype">weather.wtype</a>接口中weaid*/
        "weatid1": "", /*无意义不必理会*/
        "windid": "1", /*风向ID(暂无对照表)*/
        "winpid": "2" /*风力ID(暂无对照表)*/
        "weather_iconid": "1"  /*气象图标编号,对应weather_icon 1.gif*/
    }
}

2.异常或无数据
{
    success: "0",
    msgid: "...",
    msg: "..."
}
..............</pre></div><div class="item">
                    <p>示例代码</p>
                    <ul class="nav nav-tabs" role="tablist">
                        <li role="presentation" class="active"><a href="#scode_php" role="tab" data-toggle="tab">PHP</a></li><li role="presentation"><a href="#scode_python" role="tab" data-toggle="tab">Python</a></li><li role="presentation"><a href="#scode_java" role="tab" data-toggle="tab">Java</a></li><li role="presentation"><a href="#scode_curl" role="tab" data-toggle="tab">Curl</a></li>
                    </ul>
                    <!-- Tab panes -->
                    <div class="tab-content">
                        <div role="tabpanel" class="tab-pane active" id="scode_php"><p></p><pre>&lt;?php
header(&quot;Content-Type:text/html;charset=UTF-8&quot;);
function nowapi_call($a_parm){
    if(!is_array($a_parm)){
        return false;
    }
    //combinations
    $a_parm[&#039;format&#039;]=empty($a_parm[&#039;format&#039;])?&#039;json&#039;:$a_parm[&#039;format&#039;];
    $apiurl=empty($a_parm[&#039;apiurl&#039;])?&#039;http://api.k780.com/?&#039;:$a_parm[&#039;apiurl&#039;].&#039;/?&#039;;
    unset($a_parm[&#039;apiurl&#039;]);
    foreach($a_parm as $k=&gt;$v){
        $apiurl.=$k.&#039;=&#039;.$v.&#039;&amp;&#039;;
    }
    $apiurl=substr($apiurl,0,-1);
    if(!$callapi=file_get_contents($apiurl)){
        return false;
    }
    //format
    if($a_parm[&#039;format&#039;]==&#039;base64&#039;){
        $a_cdata=unserialize(base64_decode($callapi));
    }elseif($a_parm[&#039;format&#039;]==&#039;json&#039;){
        if(!$a_cdata=json_decode($callapi,true)){
            return false;
        }
    }else{
        return false;
    }
    //array
    if($a_cdata[&#039;success&#039;]!=&#039;1&#039;){
        echo $a_cdata[&#039;msgid&#039;].&#039; &#039;.$a_cdata[&#039;msg&#039;];
        return false;
    }
    return $a_cdata[&#039;result&#039;];
}

$nowapi_parm[&#039;app&#039;]=&#039;weather.today&#039;;
$nowapi_parm[&#039;weaId&#039;]=&#039;1&#039;;
$nowapi_parm[&#039;appkey&#039;]=&#039;APPKEY&#039;;
$nowapi_parm[&#039;sign&#039;]=&#039;SIGN&#039;;
$nowapi_parm[&#039;format&#039;]=&#039;json&#039;;
$result=nowapi_call($nowapi_parm);
var_dump($result);
print_r($result);
</pre></div><div role="tabpanel" class="tab-pane" id="scode_python"><p></p><pre>#python
import json,urllib
from urllib import urlencode

url = &#039;http://api.k780.com&#039;
params = {
  &#039;app&#039; : &#039;weather.today&#039;,
  &#039;weaId&#039; : &#039;1&#039;,
  &#039;appkey&#039; : &#039;APPKEY&#039;,
  &#039;sign&#039; : &#039;SIGN&#039;,
  &#039;format&#039; : &#039;json&#039;,
}
params = urlencode(params)

f = urllib.urlopen(&#039;%s?%s&#039; % (url, params))
nowapi_call = f.read()
#print content
a_result = json.loads(nowapi_call)
if a_result:
  if a_result[&#039;success&#039;] != &#039;0&#039;:
    print a_result[&#039;result&#039;];
  else:
    print a_result[&#039;msgid&#039;]+&#039; &#039;+a_result[&#039;msg&#039;]
else:
  print &#039;Request nowapi fail.&#039;;
</pre></div><div role="tabpanel" class="tab-pane" id="scode_java"><p></p><pre>import java.net.*;
import java.io.*;

public class test{
    public static void main(String args[]) throws Exception {
        URL u=new URL(&quot;http://api.k780.com/?app=weather.today&amp;weaId=1&amp;appkey=APPKEY&amp;sign=SIGN&amp;format=json&quot;);
        InputStream in=u.openStream();
        ByteArrayOutputStream out=new ByteArrayOutputStream();
        try {
            byte buf[]=new byte[1024];
            int read = 0;
            while ((read = in.read(buf)) &gt; 0) {
                out.write(buf, 0, read);
            }
        }  finally {
            if (in != null) {
                in.close();
            }
        }
        byte b[]=out.toByteArray( );
        System.out.println(new String(b,&quot;utf-8&quot;));
    }
}
</pre></div><div role="tabpanel" class="tab-pane" id="scode_curl"><p></p><pre>curl "http://api.k780.com/?app=weather.today&weaId=1&appkey=APPKEY&sign=SIGN&format=json"</pre></div>
                    </div>
                </div>
            </div></div><div role="tabpanel" class="tab-pane" id="cost"><div class="item">
                    <p>包月套餐说明:</p>
                    <p class="text-muted">适合调用量比较平均的高频应用场景；有配额限制，超出配额会被暂停调用1小时，请留意购买足够配额.</p>
                    <table class="table table-striped" style="font-size:12px;">
                        <thead><tr><th width="5%">规格</th><th width="20%">套餐名称</th><th width="12%">价格</th><th width="67%">描述</th></tr></thead>
                        <tbody><tr><td>102</td><td>2000 次配额/每小时</td><td><span style="color:#FF7018;">87 元/月</span></td><td>省￥ 9 享9.8折</td></tr><tr><td>103</td><td>3000 次配额/每小时</td><td><span style="color:#FF7018;">130 元/月</span></td><td>省￥ 14 享9.5折</td></tr><tr><td>104</td><td>5000 次配额/每小时</td><td><span style="color:#FF7018;">218 元/月</span></td><td>省￥ 22 享9折</td></tr><tr><td>105</td><td>10000 次配额/每小时</td><td><span style="color:#FF7018;">439 元/月</span></td><td>省￥ 41 享8.5折</td></tr><tr><td>106</td><td>20000 次配额/每小时</td><td><span style="color:#FF7018;">883 元/月</span></td><td>省￥ 77 享8折</td></tr><tr><td>107</td><td>30000 次配额/每小时</td><td><span style="color:#FF7018;">1332 元/月</span></td><td>省￥ 108 享7.5折</td></tr><tr><td>108</td><td>40000 次配额/每小时</td><td><span style="color:#FF7018;">1786 元/月</span></td><td>省￥ 134 享7折</td></tr><tr><td>109</td><td>50000 次配额/每小时</td><td><span style="color:#FF7018;">2244 元/月</span></td><td>省￥ 156 享6.5折</td></tr><tr><td>110</td><td>100000  次配额/每小时</td><td><span style="color:#FF7018;">4800 元/月</span></td><td>-</td></tr></tbody>
                    </table>
                    <a target="_blank" class="btn btn-warning" href="https://www.nowapi.com/?app=buy.setmealNew&intid=506">立即开通</a>
                </div><div class="item">
                    <p>流量包套餐说明:</p>
                    <p class="text-muted">买多少用多少，多买有优惠，10元起买，适合大多数应用场景.</p>
                    <table class="table table-striped" style="font-size:12px;">
                        <thead><tr><th width="5%">规格</th><th width="20%">套餐名称</th><th width="12%">价格</th><th width="67%">描述</th></tr></thead>
                        <tbody><tr><td>201</td><td>流量包 15000 次</td><td><span style="color:#FF7018;">10 元</span></td><td>-</td></tr><tr><td>202</td><td>流量包 157500 次</td><td><span style="color:#FF7018;">100 元</span></td><td>含 7500 次赠送流量</td></tr><tr><td>203</td><td>流量包 318000 次</td><td><span style="color:#FF7018;">200 元</span></td><td>含 18000 次赠送流量</td></tr><tr><td>204</td><td>流量包 481500 次</td><td><span style="color:#FF7018;">300 元</span></td><td>含 31500 次赠送流量</td></tr><tr><td>205</td><td>流量包 817500 次</td><td><span style="color:#FF7018;">500 元</span></td><td>含 67500 次赠送流量</td></tr><tr><td>206</td><td>流量包 1650000 次</td><td><span style="color:#FF7018;">1000 元</span></td><td>含 150000 次赠送流量</td></tr><tr><td>207</td><td>流量包 3330000 次</td><td><span style="color:#FF7018;">2000 元</span></td><td>含 330000 次赠送流量</td></tr><tr><td>208</td><td>流量包 5040000 次</td><td><span style="color:#FF7018;">3000 元</span></td><td>含 540000 次赠送流量</td></tr><tr><td>209</td><td>流量包 8625000 次</td><td><span style="color:#FF7018;">5000 元</span></td><td>含 1125000 次赠送流量</td></tr><tr><td>210</td><td>流量包 18000000 次</td><td><span style="color:#FF7018;">10000 元</span></td><td>含 3000000 次赠送流量</td></tr></tbody>
                    </table>
                    <a target="_blank" class="btn btn-warning" href="https://www.nowapi.com/?app=buy.setmealNew&intid=506">立即开通</a>
                </div><div class="item">
                    <p>免费试用套餐说明:</p>
                    <p class="text-muted">商用请选择付费套餐。 (系统繁忙或极端情况下，优先保证付费用户使用).</p>
                    <table class="table table-striped" style="font-size:12px;">
                        <thead><tr><th width="5%">规格</th><th width="20%">套餐名称</th><th width="12%">价格</th><th width="67%">描述</th></tr></thead>
                        <tbody><tr><td>0</td><td>免费套餐 200 次配额/每小时</td><td><span style="color:#FF7018;">0 元/月</span></td><td>可免费试用套餐3个月.</td></tr></tbody>
                    </table>
                    <a target="_blank" class="btn btn-warning" href="https://www.nowapi.com/?app=buy.setmealNew&intid=506">立即开通</a>
                </div></div><div role="tabpanel" class="tab-pane" id="other"><div class="item">
                <p>客户服务</p>
                <pre>客服QQ: 1486133340 <a target="_blank" href="tencent://message/?uin=1486133340&Site=www.nowapi.com&Menu=yes"><img src="https://www.nowapi.com/style/img/qq.gif"></a><br> QQ群8: 204490433 <br><br>客服微信:<br><img src="https://www.nowapi.com/style/img/kf_weixin.jpg">
                </pre>
            </div>
            <div class="item">
                <p>数据定制</p>
                <pre>定制接口、定制数据格式、采集等；联系请提供数据样式范本。1486133340 <a target="_blank" href="tencent://message/?uin=1486133340&Site=www.nowapi.com&Menu=yes"><img src="https://www.nowapi.com/style/img/qq.gif"></a></pre>
            </div>
            <div class="item">
                <p>意见反馈</p>
                <pre><a target="_blank" href="https://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=Snt-c316enp4fXkKOztkKSUn" style="text-decoration:none;"><img src="https://rescdn.qqmail.com/zh_CN/htmledition/images/function/qm_open/ico_mailme_12.png"/></a></pre>
            </div></div></div>
            </div>
        </div>
    </div>
</div>



<div class="footer">
    <div class="footer-auto">
        <div class="footer-body">
            <div class="contact">
                <p class="tit">线上支持</p>
                <p><a href="https://www.nowapi.com/intro/about.html">商务合作</a></p>
                <p><a href="https://www.nowapi.com/intro/about.html">客户服务</a></p>
            </div>
            <div class="help">
                <p class="tit">帮助中心</p>
                <p><a href="https://www.nowapi.com/intro/help.html">常见问题</a></p>
                <p><a href="https://www.nowapi.com/intro/policy.html">政策法规</a></p>
                <p><a href="https://www.nowapi.com/intro/fapiao.html">发票</a></p>
            </div>
            <div class="about">
                <p class="tit">关于我们</p>
                <p><a href="https://www.nowapi.com/intro/company.html">公司简介</a></p>
                <p><a href="https://www.nowapi.com/intro/policy.html">免责声明</a></p>
                <p><a href="https://www.nowapi.com/intro/about.html">联系我们</a></p>
            </div>
            <div class="subs">
                <p class="tit">微信关注</p>
                <p><img src="https://www.nowapi.com/style/img/qr_weixin.jpg"></p>
            </div>
        </div>
        <div class="footer-link">
            Copyright © 中山诺派信息技术有限公司 <a href="http://www.miitbeian.gov.cn">粤ICP备15098231号-3</a><script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "//hm.baidu.com/hm.js?eddf6f7878f7b4baad01098160209d24";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
        </div>
    </div>
</div>

</body>
</html>
'''


@dataclass
class WeatherTodayDto:
    """
    当天天气数据结构
    """
    weaid: str
    weatid: str  # 天气ID，可对照 weather.wtype 接口中 weaid
    days: str
    week: str
    cityno: str
    citynm: str
    cityid: str
    temperature: str  # 当日温度区间 (注: 夜间只有一个温度如24℃/24℃)
    temperature_curr: str  # 当前温度
    temp_high: str  # 最高温度
    temp_low: str  # 最低温度
    humidity: str  # 湿度
    aqi: str  # pm2.5 说明详见weather.pm25
    weather: str  # 天气
    weather_icon: str  # 气象图标
    wind: str  # 风向
    winp: str  # 风力


def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def get_param_dict(url):
    param_list = url.strip().split('?')[1].split('&')
    param_dict = {}
    for item in param_list:
        param_dict[item.split('=')[0]] = item.split('=')[1]
    return param_dict


def parse_test_exp_result(html):
    test_link_list = re.findall('<a target="_blank" href=".*?">.*?</a> \(示例中sign会不定期调整\)', html)
    if len(test_link_list) != 1:
        raise Exception("测试链接获取有误")
    soup = BeautifulSoup(test_link_list[0], "lxml")
    url = soup.find('a').get("href")
    data = get_param_dict(url)
    data["url"] = url
    return data


def parse_weather_result(url):
    data = None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
    except requests.RequestException as err:
        raise Exception("请求天气数据报错: ", err)

    if data.get("success") != "1":
        raise Exception(f"请求天气数据报错, 响应code 为 {data.get('msg', '')}， 错误信息为 {data.get('success', '')}")

    result = data.get('result', {})
    if "weather_icon1" in result:
        del result["weather_icon1"]
    if "humi_high" in result:
        del result["humi_high"]
    if "humi_low" in result:
        del result["humi_low"]
    if "weatid1" in ["weatid1"]:
        del result["weatid1"]
    if "windid" in result:
        del result["windid"]
    if "winpid" in result:
        del result["winpid"]
    if "weather_curr" in result:
        del result["weather_curr"]
    if "temp_curr" in result:
        del result["temp_curr"]
    if "weather_iconid" in result:
        del result["weather_iconid"]

    return WeatherTodayDto(**data.get('result', {}))


def write_item_to_file(item):
    print('开始写入数据 ====> ' + str(item))
    with open('book.txt', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main():
    url = "https://www.nowapi.com/api/weather.today"
    html = request_url(url)
    test_exp_param = parse_test_exp_result(html)  # 得到测试用例的数据

    wea_id = 2955  # 厦门湖里
    get_weather_url = f"http://api.k780.com/?app=weather.today&weaId={wea_id}&appkey={test_exp_param.get('appkey', '')}&sign={test_exp_param.get('sign', '')}&format=json"
    weather_info = parse_weather_result(get_weather_url)

    tz = pytz.timezone('Asia/Shanghai')
    update_time = datetime.datetime.now(tz).strftime("%H:%M:%S")

    line = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        weather_info.days,
        update_time,
        weather_info.week,
        weather_info.citynm,
        weather_info.weather,
        weather_info.temperature,
        weather_info.temperature_curr,
        weather_info.temp_high,
        weather_info.temp_low,
        weather_info.humidity,
        weather_info.aqi,
        weather_info.weather_icon,
        weather_info.wind,
        weather_info.winp,
    )
    print(line)


if __name__ == "__main__":
    main()
