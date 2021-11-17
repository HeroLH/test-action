#!/bin/bash
cd `dirname $0`
PATH=$PATH:/usr/local/bin
echo "休眠随机时间0 - 99s"
echo "run..."
python3 run.py >> XiaMen_Huli.txt
echo "日期,更新时间,星期,城市,天气,当日温度区间,当前温度,最高温度,最低温度,湿度,pm2.5,气象图标,风向,风力" > XiaMen_Huli.csv
tac XiaMen_Huli.txt >> XiaMen_Huli.csv
echo "done!"
