# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 13:30
# @Author  : alvin
# @File    : ai_主图指标.py
# @Software: PyCharm
//@version=5
//create by alvin@ai 20221115
indicator(title="AI_主图指标", shorttitle="AI_主图指标",overlay=true,max_boxes_count = 300,max_labels_count=500,max_lines_count=500,max_bars_back=500)
//买卖点

// HighLow_Indicators=input(false,title ="AI_天地")
Channel_Indicators=input(true,title ="通道")
Chip_Indicators=input(true,title ="筹码峰")
BuySell_Indicators=input(true,title ="买卖提示")
// TD9 = input(false,title ="神奇九转")
RGTrend_Indicators=input(true,title ="红绿趋势线")
UpDownTrend_Indicators=input(true,title ="支撑压力线")
//Double_Trend_Indicators=input(false,title ="双均线战法")
// RSI_Indicators=input(false,title ="多空提示预警")
DirectionLine_Indicators=input(true,title ="方向线与多空背景")
//OBV_auxiliary_Indicators=input(false,title ="副图OBV辅助DEMA")


group1 = "AI_通道设置"
useUpperDevInput = input.bool(true, title="Upper Deviation", inline = "Upper Deviation", group = group1)
upper_Channel_IndicatorsMultInput = input.float(2.0, title="", inline = "Upper Deviation", group = group1)
useLowerDevInput = input.bool(true, title="Lower Deviation", inline = "Lower Deviation", group = group1)
lower_Channel_IndicatorsMultInput = input.float(2.0, title="", inline = "Lower Deviation", group = group1)

group2 = "AI_通道延长"
showPearsonInput = input.bool(false, "皮尔森R", group = group2)
extendLeftInput = input.bool(false, "延长左侧", group = group2)
extendRightInput = input.bool(true, "延长右侧", group = group2)
extendStyle = switch
extendLeftInput and extendRightInput => extend.both
extendLeftInput => extend.left
extendRightInput => extend.right
=> extend.none

group3 = "AI_通道颜色"
colorUpper = input.color(color.new(color.blue, 85), "", inline = group3, group = group3)
colorLower = input.color(color.new(color.yellow, 95), "", inline = group3, group = group3)


//-----------------------------------------------------------------AI买卖提示开始
Periods = BuySell_Indicators?input.int(title="Period", defval=10):10
src = BuySell_Indicators?input(hl2, title="Source"):na
Multiplier = input.float(title="Multiplier", step=0.1, defval=3.0)
changeATR= input.bool(title="Change Calculation Method ?", defval=true)
showsignals = input.bool(title="Show Buy/Sell Signals ?",defval=true)
highlighting = input.bool(title="Highlighter On/Off ?",defval=true)
atr2 = ta.sma(ta.tr, Periods)
atr= changeATR ? ta.atr(Periods) : atr2
up=src-(Multiplier*atr)
up1 = nz(up[1],up)
up := close[1] > up1 ? math.max(up,up1) : up
dn=src+(Multiplier*atr)
dn1 = nz(dn[1], dn)
dn := close[1] < dn1 ? math.min(dn, dn1) : dn
trend = 1
trend := nz(trend[1], trend)
trend := trend == -1 and close > dn1 ? 1 : trend == 1 and close < up1 ? -1 : trend
upPlot = plot(trend == 1 ? up : na, title="Up Trend", style=plot.style_linebr, linewidth=2, color=color.green)
buySignal = trend == 1 and trend[1] == -1
plotshape(buySignal ? up : na, title="UpTrend Begins", location=location.absolute, style=shape.circle, size=size.tiny, color=color.new(color.green,0))
plotshape(buySignal and showsignals ? up : na, title="买", text="买", location=location.absolute, style=shape.labelup, size=size.tiny,color=color.new(color.green,0), textcolor=color.white)
dnPlot = plot(trend == 1 ? na : dn, title="Down Trend", style=plot.style_linebr, linewidth=2, color=color.red)
sellSignal = trend == -1 and trend[1] == 1
plotshape(sellSignal ? dn : na, title="DownTrend Begins", location=location.absolute, style=shape.circle, size=size.tiny, color=color.new(color.red,0))
plotshape(sellSignal and showsignals ? dn : na, title="卖", text="卖", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.new(color.red,0), textcolor=color.white)
mPlot = plot(ohlc4, title="", style=plot.style_circles, linewidth=0)
longFillColor = highlighting ? (trend == 1 ? color.green : color.white) : color.white
shortFillColor = highlighting ? (trend == -1 ? color.red : color.white) : color.white
fill(mPlot, upPlot, title="UpTrend Highligter", color=color.new(color.green,80))
fill(mPlot, dnPlot, title="DownTrend Highligter", color=color.new(color.red,80))

changeCond = trend != trend[1]
// alertcondition(changeCond, title="SuperTrend Direction Change", message="SuperTrend has changed direction!")

alertcondition(buySignal, title="买点提示", message="买点提示")
alertcondition(sellSignal, title="卖点提示", message="卖点提示")
//..................................................................AI_买卖提示结束


//..................................................................AI_方向线开始
close_price = close[0]
len = DirectionLine_Indicators?input.int(defval=100, minval=1, title="Linear Regression length"):na
linear_reg =DirectionLine_Indicators?ta.linreg(close_price, len, 0):na
linear_reg_prev = DirectionLine_Indicators?ta.linreg(close[1], len, 0):na
slope = (linear_reg - linear_reg_prev) / timeframe.multiplier
//灰色方向线
plot(linear_reg, color=color.gray, title="Linear Regression Curve", style=plot.style_line, linewidth=2)
//..................................................................AI_方向线结束



//..................................................................AI_红绿趋势线  和 AI_支撑压力线开始
showZones = input(true, title="Show Bullish/Bearish Zones")
// bullish signal rule:
bullishRule = slope > 0
// bearish signal rule:
bearishRule = slope <= 0
// current trading State
ruleState = 0
ruleState := bullishRule ? 1 : bearishRule ? -1 : nz(ruleState[1])
bgcolor(showZones ? ruleState == 1 ? color.new(color.blue,90) : ruleState == -1 ? color.new(color.red,90) : color.new(color.gray,100) : na, title=" Bullish/Bearish Zones")
length = input.int(title="Bollinger Length", defval=20, minval=1)
multiplier = input.int(title="Bollinger Deviation", defval=2, minval=1)
overbought = input.int(title="Overbought", defval=1, minval=1)
oversold = input.int(title="Oversold", defval=0, minval=0)
custom_timeframe = input.bool(title="Use another Timeframe?", defval=false)
highTimeFrame = input.timeframe(title="Select The Timeframe", defval="60")
res = custom_timeframe ? highTimeFrame : timeframe.period

smabasis = ta.sma(close, length)
stdev = ta.stdev(close, length)
cierre = request.security(syminfo.tickerid, res, close,gaps = barmerge.gaps_off)
alta = request.security(syminfo.tickerid, res, high, gaps = barmerge.gaps_off)
baja = request.security(syminfo.tickerid, res, low,gaps = barmerge.gaps_off)
basis1 = request.security(syminfo.tickerid, res, smabasis,gaps = barmerge.gaps_off)
stdevb = request.security(syminfo.tickerid, res, stdev,gaps = barmerge.gaps_off)
dev = multiplier * stdevb  // stdev(cierre, length)
upper = basis1 + dev
lower = basis1 - dev

bbr = (cierre - lower) / (upper - lower)

// plot(bbr)

// // MARCA LAS RESISTENCIAS  支撑压力线
pintarojo = 0.0
pintarojo := nz(pintarojo[1])
pintarojo := UpDownTrend_Indicators?(bbr[1] > overbought and bbr < overbought ? alta[1] : nz(pintarojo[1])):na
p = plot(pintarojo, color=color.red, style=plot.style_circles, linewidth=1)

// // MARCA LOS SOPORTES
pintaverde = 0.0
pintaverde := nz(pintaverde[1])
pintaverde := UpDownTrend_Indicators?(bbr[1] < oversold and bbr > oversold ? baja[1] : nz(pintaverde[1])):na
g = plot(pintaverde, color=color.blue, style=plot.style_circles, linewidth=1)


buy = ta.crossover(slope, 0)
sell = ta.crossunder(slope, 0)

// 支撑压力线 UpDownTrend_Indicators
plotshape(sell, title="sell1", style=shape.triangledown, location=location.abovebar, color=color.new(color.red,0), size=size.tiny)
plotshape(buy, title="buy1", style=shape.triangleup, location=location.belowbar, color=color.new(color.green,0), size=size.tiny)

///////////////////////////////////
//Modified on 5-5-14 for 4apprentice08 with Optional BarColor based on Price  Crossing MA #1, or #2
//Modified on 7-25-2014 to Add in Tilson T3
//Plots The Majority of Moving Averages
//Defaults to Current Chart Time Frame --- But Can Be Changed to Higher Or Lower Time Frames
//2nd MA Capability with Show Crosses Feature
//inputs
src_RGTrend_Indicators = close[0]
useCurrentRes = input(true, title="Use Current Chart Resolution?")
resCustom = input.timeframe(title="Use Different Timeframe? Uncheck Box Above", defval="D")
lenA1 = input(20, title="Moving Average lenA1A1gth - LookBack Period")
//periodT3 = input(defval=7, title="Tilson T3 Period", minval=1)
factorT3 = input.int(defval=7, title="Tilson T3 Factor - *.10 - so 7 = .7 etc.", minval=0)
atype = input.int(1, minval=1, maxval=8, title="1=SMA, 2=EMA, 3=WMA, 4=HullMA, 5=VWMA, 6=RMA, 7=TEMA, 8=Tilson T3")
spc = input(false, title="Show Price Crossing 1st Mov Avg - Highlight Bar?")
cc = input(true, title="Change Color Based On Direction?")
smoothe = input.int(2, minval=1, maxval=10, title="Color Smoothing - Setting 1 = No Smoothing")
doma2 = UpDownTrend_Indicators?(input(false, title="Optional 2nd Moving Average")):na
spc2 = input(false, title="Show Price Crossing 2nd Mov Avg?")
len2 = input(50, title="Moving Average lenA1gth - Optional 2nd MA")
sfactorT3 = input.int(defval=7, title="Tilson T3 Factor - *.10 - so 7 = .7 etc.", minval=0)
atype2 = input.int(1, minval=1, maxval=8, title="1=SMA, 2=EMA, 3=WMA, 4=HullMA, 5=VWMA, 6=RMA, 7=TEMA, 8=Tilson T3")
cc2 = input(true, title="Change Color Based On Direction 2nd MA?")
warn = input(false, title="***You Can Turn On The Show Dots Parameter Below Without Plotting 2nd MA to See Crosses***")
warn2 = input(false, title="***If Using Cross Feature W/O Plotting 2ndMA - Make Sure 2ndMA Parameters are Set Correctly***")
sd = input(false, title="Show Dots on Cross of Both MA's")
resA1 = useCurrentRes ? timeframe.period : resCustom
//hull ma definition
hullma = ta.wma(2 * ta.wma(src_RGTrend_Indicators, lenA1 / 2) - ta.wma(src_RGTrend_Indicators, lenA1), math.round(math.sqrt(lenA1)))
//TEMA definition
ema1 = ta.ema(src_RGTrend_Indicators, lenA1)
ema2 = ta.ema(ema1, lenA1)
ema3 = ta.ema(ema2, lenA1)
tema = 3 * (ema1 - ema2) + ema3

//Tilson T3
factor = factorT3 * .10
gd(src_RGTrend_Indicators, lenA1, factor) =>
ta.ema(src_RGTrend_Indicators, lenA1) * (1 + factor) - ta.ema(ta.ema(src_RGTrend_Indicators, lenA1), lenA1) * factor
t3(src_RGTrend_Indicators, lenA1, factor) =>
gd(gd(gd(src_RGTrend_Indicators, lenA1, factor), lenA1, factor), lenA1, factor)
tilT3 = t3(src_RGTrend_Indicators, lenA1, factor)


sma_1 = ta.sma(src_RGTrend_Indicators, lenA1)
ema_1 = ta.ema(src_RGTrend_Indicators, lenA1)
wma_1 = ta.wma(src_RGTrend_Indicators, lenA1)
vwma_1 = ta.vwma(src_RGTrend_Indicators, lenA1)
rma_1 = ta.rma(src_RGTrend_Indicators, lenA1)
avg = atype == 1 ? sma_1 : atype == 2 ? ema_1 :
atype == 3 ? wma_1 : atype == 4 ? hullma : atype == 5 ? vwma_1 :
atype == 6 ? rma_1 : atype == 7 ? 3 * (ema1 - ema2) + ema3 : tilT3
//2nd Ma - hull ma definition
hullma2 = ta.wma(2 * ta.wma(src_RGTrend_Indicators, len2 / 2) - ta.wma(src_RGTrend_Indicators, len2), math.round(math.sqrt(len2)))
//2nd MA TEMA definition
sema1 =ta.ema(src_RGTrend_Indicators, len2)
sema2 = ta.ema(sema1, len2)
sema3 = ta.ema(sema2, len2)
stema = 3 * (sema1 - sema2) + sema3

//2nd MA Tilson T3
sfactor = sfactorT3 * .10
sgd(src_RGTrend_Indicators, len2, sfactor) =>
ta.ema(src_RGTrend_Indicators, len2) * (1 + sfactor) - ta.ema(ta.ema(src_RGTrend_Indicators, len2), len2) * sfactor
st3(src_RGTrend_Indicators, len2, sfactor) =>
sgd(sgd(gd(src_RGTrend_Indicators, len2, sfactor), len2, sfactor), len2, sfactor)
stilT3 = st3(src_RGTrend_Indicators, len2, sfactor)

sma_2 = ta.sma(src_RGTrend_Indicators, len2)
ema_2 = ta.ema(src_RGTrend_Indicators, len2)
wma_2 = ta.wma(src_RGTrend_Indicators, len2)
vwma_2 = ta.vwma(src_RGTrend_Indicators, len2)
rma_2 = ta.rma(src_RGTrend_Indicators, len2)
avg2 = atype2 == 1 ? sma_2 : atype2 == 2 ? ema_2 :
atype2 == 3 ? wma_2 : atype2 == 4 ? hullma2 : atype2 == 5 ? vwma_2 :
atype2 == 6 ? rma_2 : atype2 == 7 ? 3 * (ema1 - ema2) + ema3 : stilT3

out = avg
out_two = avg2

out1 = RGTrend_Indicators?(request.security(syminfo.tickerid, resA1, out)):na
out2 = request.security(syminfo.tickerid, resA1, out_two)

//Formula for Price Crossing Moving Average #1
cr_up = open < out1 and close > out1
cr_Down = open > out1 and close < out1
//Formula for Price Crossing Moving Average #2
cr_up2 = open < out2 and close > out2
cr_Down2 = open > out2 and close < out2
//barcolor Criteria for Price Crossing Moving Average #1
iscrossUp() =>
cr_up
iscrossDown() =>
cr_Down
//barcolor Criteria for Price Crossing Moving Average #2
iscrossUp2() =>
cr_up2
iscrossDown2() =>
cr_Down2

ma_up = out1 >= out1[smoothe]
ma_down = out1 < out1[smoothe]

col = cc ? ma_up ? color.lime : ma_down ? color.red : color.aqua : color.aqua
col2 = cc2 ? ma_up ? color.lime : ma_down ? color.red : color.aqua : color.white

circleYPosition = out2

//红绿趋势线颜色 ,out1比较陡，out2平滑
plot(out1, title="Multi-Timeframe Moving Avg", style=plot.style_line, linewidth=2, color=col)
plot(doma2 and out2 ? out2 : na, title="2nd Multi-TimeFrame Moving Average", style=plot.style_circles, linewidth=2, color=col2)
plot(sd and ta.cross(out1, out2) ? circleYPosition : na, style=plot.style_cross, linewidth=15, color=color.aqua)


//barcolor Plot for Price Crossing Moving Average #1
iscrossUp_1 = iscrossUp()
barcolor(spc and iscrossUp() ? iscrossUp_1 ? color.yellow : na : na)
iscrossDown_1 = iscrossDown()
barcolor(spc and iscrossDown() ? iscrossDown_1 ? color.yellow : na : na)
//barcolor Plot for Price Crossing Moving Average #2
iscrossUp2_1 = iscrossUp2()
barcolor(spc2 and iscrossUp2() ? iscrossUp2_1 ? color.yellow : na : na)
iscrossDown2_1 = iscrossDown2()
barcolor(spc2 and iscrossDown2() ? iscrossDown2_1 ? color.yellow : na : na)

alertcondition(sell, title='支撑买点', message='买点提示')
alertcondition(buy, title='压力卖点', message='卖点提示')

//..................................................................AI_红绿支撑压力线结束

//..................................................................AI_天地开始

length_HighLow_Indicators = input(50,'Pivot Length')

show_reg   = input.bool(true,'Regular Pivots',inline='inline1')
reg_ph_css = input.color(#ef5350,'High',inline='inline1')
    reg_pl_css = input.color(#26a69a,'Low',inline='inline1')

        show_miss   = input.bool(true,'Missed Pivots',inline='inline2')
miss_ph_css = input.color(#ef5350,'High',inline='inline2')
    miss_pl_css = input.color(#26a69a,'Low',inline='inline2')

        label_css = input.color(color.white,'Text Label Color')
                    //------------------------------------------------------------------------------
        var line zigzag = na
var line ghost_level = na
var max = 0.,var min = 0.
var max_x1 = 0,var min_x1 = 0
var follow_max = 0.,var follow_max_x1 = 0
var follow_min = 0.,var follow_min_x1 = 0
var os = 0,var py1 = 0.,var px1 = 0
                                  //------------------------------------------------------------------------------

n = bar_index
ph = ta.pivothigh(length_HighLow_Indicators,length_HighLow_Indicators)
pl = ta.pivotlow(length_HighLow_Indicators,length_HighLow_Indicators)

max := math.max(high[length_HighLow_Indicators],max)
min := math.min(low[length_HighLow_Indicators],min)
follow_max := math.max(high[length_HighLow_Indicators],follow_max)
follow_min := math.min(low[length_HighLow_Indicators],follow_min)

if max > max[1]
max_x1 := n-length_HighLow_Indicators
follow_min := low[length_HighLow_Indicators]
if min < min[1]
min_x1 := n-length_HighLow_Indicators
follow_max := high[length_HighLow_Indicators]

if follow_min < follow_min[1]
follow_min_x1 := n-length_HighLow_Indicators
if follow_max > follow_max[1]
follow_max_x1 := n-length_HighLow_Indicators

                 //------------------------------------------------------------------------------
line.set_x2(ghost_level[1],n)

if ph
if show_miss
if os[1] == 1
label.new(min_x1,min,'地',color=miss_pl_css,style=label.style_label_up,size=size.small,
// label.new(min_x1,min,'地two',color=miss_pl_css,style=label.style_label_up,size=size.small,
tooltip=str.tostring(min,'#.####'))

zigzag := line.new(px1,py1,min_x1,min,color=miss_ph_css,style=line.style_dashed)
px1 := min_x1,py1 := min

line.set_x2(ghost_level[1],px1)
ghost_level := line.new(px1,py1,px1,py1,color=color.new(reg_pl_css,50),width=2)
else if ph < max
label.new(max_x1,max,'地',color=miss_ph_css,style=label.style_label_down,size=size.small,
// label.new(max_x1,max,'地1',color=miss_ph_css,style=label.style_label_down,size=size.small,
tooltip=str.tostring(max,'#.####'))
// label.new(follow_min_x1,follow_min,'天2',color=miss_pl_css,style=label.style_label_up,size=size.small,
label.new(follow_min_x1,follow_min,'天',color=miss_pl_css,style=label.style_label_up,size=size.small,
tooltip=str.tostring(min,'#.####'))

zigzag := line.new(px1,py1,max_x1,max,color=miss_pl_css,style=line.style_dashed)
px1 := max_x1,py1 := max
line.set_x2(ghost_level[1],px1)
ghost_level := line.new(px1,py1,px1,py1,color=color.new(reg_ph_css,50),width=2)

zigzag := line.new(px1,py1,follow_min_x1,follow_min,color=miss_ph_css,style=line.style_dashed)
px1 := follow_min_x1,py1 := follow_min
line.set_x2(ghost_level,px1)
ghost_level := line.new(px1,py1,px1,py1,color=color.new(reg_pl_css,50),width=2)

if show_reg
label.new(n-length_HighLow_Indicators,ph,'天',textcolor=label_css,color=reg_ph_css,style=label.style_label_down,size=size.small,
tooltip=str.tostring(ph,'#.####'))
zigzag := line.new(px1,py1,n-length_HighLow_Indicators,ph,color=miss_pl_css,style=ph < max or os[1] == 1 ? line.style_dashed : line.style_solid)


py1 := ph,px1 := n-length_HighLow_Indicators,os := 1,max := ph,min := ph
                                                                      //------------------------------------------------------------------------------
if pl
if show_miss
if os[1] == 0
   // label.new(max_x1,max,'天ONE',color=miss_ph_css,style=label.style_label_down,size=size.small,
                label.new(max_x1,max,'天',color=miss_ph_css,style=label.style_label_down,size=size.small,
                          tooltip=str.tostring(max,'#.####'))

zigzag := line.new(px1,py1,max_x1,max,color=miss_pl_css,style=line.style_dashed)
px1 := max_x1,py1 := max

line.set_x2(ghost_level[1],px1)
ghost_level := line.new(px1,py1,px1,py1,color=color.new(reg_ph_css,50),width=2)
else if pl > min
// label.new(follow_max_x1,follow_max,'地3',color=miss_ph_css,style=label.style_label_down,size=size.small,
label.new(follow_max_x1,follow_max,'地',color=miss_ph_css,style=label.style_label_down,size=size.small,
tooltip=str.tostring(max,'#.####'))
// label.new(min_x1,min,'天3',color=miss_pl_css,style=label.style_label_up,size=size.small,
label.new(min_x1,min,'天',color=miss_pl_css,style=label.style_label_up,size=size.small,
tooltip=str.tostring(min,'#.####'))

zigzag := line.new(px1,py1,min_x1,min,color=miss_ph_css,style=line.style_dashed)
px1 := min_x1,py1 := min
line.set_x2(ghost_level[1],px1)
ghost_level := line.new(px1,py1,px1,py1,color=color.new(reg_pl_css,50),width=2)

zigzag := line.new(px1,py1,follow_max_x1,follow_max,color=miss_pl_css,style=line.style_dashed)
px1 := follow_max_x1,py1 := follow_max
line.set_x2(ghost_level,px1)
ghost_level := line.new(px1,py1,px1,py1,color=color.new(reg_ph_css,50),width=2)

if show_reg
label.new(n-length_HighLow_Indicators,pl,'地',textcolor=label_css,color=reg_pl_css,style=label.style_label_up,size=size.small,
tooltip=str.tostring(pl,'#.####'))
zigzag := line.new(px1,py1,n-length_HighLow_Indicators,pl,color=miss_ph_css,style=pl > min or os[1] == 0 ? line.style_dashed : line.style_solid)


py1 := pl,px1 := n-length_HighLow_Indicators,os := 0,max := pl,min := pl
                                                                      //------------------------------------------------------------------------------
var label lbl = na
if barstate.islast
x = 0,y = 0.

prices = array.new_float(0)
prices_x = array.new_int(0)

for i = 0 to n-px1-1
array.push(prices,os==1?low[i]:high[i])
array.push(prices_x,n-i)

label.delete(lbl[1])
//企鹅和牛
if os == 1
y := array.min(prices)
x := array.get(prices_x,array.indexof(prices,y))

if show_miss
   // lbl := label.new(x,y,'👻',color=miss_pl_css,style=label.style_label_up,size=size.small,  地ONE
lbl := label.new(x,y,'地',color=miss_pl_css,style=label.style_label_up,size=size.small,
                 tooltip=str.tostring(y,'#.####'))
else
y := array.max(prices)
x := array.get(prices_x,array.indexof(prices,y))

if show_miss
   // lbl := label.new(x,y,'👻',color=miss_ph_css,style=label.style_label_down,size=size.small,
             // lbl := label.new(x,y,'天two',color=miss_ph_css,style=label.style_label_down,size=size.small,
                                 lbl := label.new(x,y,'天',color=miss_ph_css,style=label.style_label_down,size=size.small,
                                                  tooltip=str.tostring(y,'#.####'))

                                 if show_miss
line.delete(line.new(px1,py1,x,y,color=os == 1 ? miss_ph_css : miss_pl_css,style=line.style_dashed)[1])

line.delete(line.new(x,y,n,y,color = color.new(os == 1 ? miss_ph_css : miss_pl_css,50),width=2)[1])
//..................................................................AI_天地结束




  //..................................................................AI_筹码峰开始

bbars = Chip_Indicators?(input.int(title="Number of Bars", defval = 150, minval = 1, maxval = 500)):150
cnum = Chip_Indicators?(input.int(title="Row Size", defval = 24, minval = 5, maxval = 100)):24
percent = Chip_Indicators?(input.float(70., title="Value Area Volume %", minval = 0, maxval = 100)):70.

poc_color = Chip_Indicators?(input.color(defval = #f7ff00, title = "POC Color", inline = "poc")):na
                                         poc_width = Chip_Indicators?(input.int(defval = 2, title = "Width", minval = 1, maxval = 3, inline = "poc")):2

                                                                                                                                                      //中数区，白色是买，粉色是卖
vup_color = Chip_Indicators?(input(defval = color.new(#899ad5, 30), title = "Value Area Up")):na
    vdown_color = Chip_Indicators?(input(defval = color.new(color.orange, 30), title = "Value Area Down")):na

                                                                                                           //中数区，蓝色是买，黄色是卖
up_color = Chip_Indicators?(input(defval = color.new(#d3d3d3, 75), title = "UP Volume")):na
    down_color = Chip_Indicators?(input(defval = color.new(#ff9e81, 75), title = "Down Volume")):na

top = ta.highest(bbars)
bot = ta.lowest(bbars)
dist = (top - bot) / 500
step = (top - bot) / cnum

       // calculate/keep channel levels
levels = array.new_float(cnum + 1)
for x = 0 to cnum
array.set(levels, x, bot + step * x)

// get the volume if there is intersection
get_vol(y11, y12, y21, y22, height, vol)=> nz(math.max(math.min(math.max(y11, y12), math.max(y21, y22)) - math.max(math.min(y11, y12), math.min(y21, y22)), 0) * vol / height)

if barstate.islast
// calculate/get volume for each channel and candle
volumes = array.new_float(cnum * 2, 0.)
for bars = 0 to bbars - 1
body_top = math.max(close[bars], open[bars])
body_bot = math.min(close[bars], open[bars])
itsgreen = close[bars] >= open[bars]

topwick = high[bars] - body_top
bottomwick = body_bot - low[bars]
body = body_top - body_bot

bodyvol = body * volume[bars] / (2 * topwick + 2 * bottomwick + body)
topwickvol = 2 * topwick * volume[bars] / (2 * topwick + 2 * bottomwick + body)
bottomwickvol = 2 * bottomwick * volume[bars] / (2 * topwick + 2 * bottomwick + body)
for x = 0 to cnum - 1
array.set(volumes, x, array.get(volumes, x) +
(itsgreen ? get_vol(array.get(levels, x), array.get(levels, x + 1), body_bot, body_top, body, bodyvol) : 0) +
                                                                                                            get_vol(array.get(levels, x), array.get(levels, x + 1), body_top, high[bars], topwick, topwickvol) / 2 +
                                                                                                            get_vol(array.get(levels, x), array.get(levels, x + 1), body_bot, low[bars], bottomwick, bottomwickvol) / 2)
array.set(volumes, x + cnum, array.get(volumes, x + cnum) +
          (itsgreen ? 0 : get_vol(array.get(levels, x), array.get(levels, x + 1), body_bot, body_top, body, bodyvol)) +
                                                                                                                      get_vol(array.get(levels, x), array.get(levels, x + 1), body_top, high[bars], topwick, topwickvol) / 2 +
                                                                                                                      get_vol(array.get(levels, x), array.get(levels, x + 1), body_bot, low[bars], bottomwick, bottomwickvol) / 2)

totalvols = array.new_float(cnum, 0.)
for x = 0 to cnum - 1
array.set(totalvols, x, array.get(volumes, x) + array.get(volumes, x + cnum))

int poc = array.indexof(totalvols, array.max(totalvols))

// calculate value area
totalmax = array.sum(totalvols) * percent / 100.
va_total = array.get(totalvols, poc)
int up = poc
int down = poc
for x = 0 to cnum - 1
if va_total >= totalmax
break
uppervol = up < cnum - 1 ? array.get(totalvols, up + 1) : 0.
lowervol = down > 0 ? array.get(totalvols, down - 1) : 0.
if uppervol == 0 and lowervol == 0
    break
if uppervol >= lowervol
    va_total += uppervol
    up += 1
else
    va_total += lowervol
    down -= 1

maxvol = array.max(totalvols)
for x = 0 to cnum * 2 - 1
array.set(volumes, x, array.get(volumes, x) * bbars / (3 * maxvol))


// Draw VP rows
var vol_bars = array.new_box(cnum * 2, na)
for x = 0 to cnum - 1
box.delete(array.get(vol_bars, x))
box.delete(array.get(vol_bars, x + cnum))
array.set(vol_bars, x, box.new(bar_index - bbars + 1, array.get(levels, x + 1) - dist,
                               bar_index - bbars + 1 + math.round(array.get(volumes, x)), array.get(levels, x) + dist,
                               border_width = 0,
                               bgcolor = x >= down and x <= up ? vup_color : up_color))
array.set(vol_bars, x + cnum, box.new(bar_index - bbars + 1 + math.round(array.get(volumes, x)), array.get(levels, x + 1) - dist,
                                      bar_index - bbars + 1 + math.round(array.get(volumes, x)) + math.round(array.get(volumes, x + cnum)), array.get(levels, x) + dist,
                                      border_width = 0,
                                      bgcolor = x >= down and x <= up ? vdown_color : down_color))

// Draw POC line
var line poc_line = na
line.delete(poc_line)
poc_line := line.new(bar_index - bbars + 1, (array.get(levels, poc) + array.get(levels, poc + 1)) / 2,
                     bar_index - bbars + 2, (array.get(levels, poc) + array.get(levels, poc + 1)) / 2,
            //方向
extend = extend.right,
         color = poc_color,
                 width = poc_width)
//..................................................................AI_筹码峰结束




//..................................................................AI_通道开始

lengthInput = Channel_Indicators?(input.int(100, title="Length", minval = 1, maxval = 5000)):na
sourceInput = input.source(close, title="Source")


calcSlope(source, length) =>
max_bars_back(source, 5000)
if not barstate.islast or length <= 1
    [float(na), float(na), float(na)]
else
    sumX = 0.0
    sumY = 0.0
    sumXSqr = 0.0
    sumXY = 0.0
    for i = 0 to length - 1 by 1
    val = source[i]
    per = i + 1.0
    sumX += per
    sumY += val
    sumXSqr += per * per
    sumXY += val * per
slope = (length * sumXY - sumX * sumY) / (length * sumXSqr - sumX * sumX)
average = sumY / length
intercept = average - slope * sumX / length + slope
[slope, average, intercept]

[s, a, i] = calcSlope(sourceInput, lengthInput)
startPrice = i + s * (lengthInput - 1)
endPrice = i
var line baseLine = na
if na(baseLine) and not na(startPrice)
    baseLine := line.new(bar_index - lengthInput + 1, startPrice, bar_index, endPrice, width=1, extend=extendStyle, color=color.new(colorLower, 0))
else
    line.set_xy1(baseLine, bar_index - lengthInput + 1, startPrice)
    line.set_xy2(baseLine, bar_index, endPrice)
    na

calcDev(source, length, slope, average, intercept) =>
upDev = 0.0
dnDev = 0.0
stdDevAcc = 0.0
dsxx = 0.0
dsyy = 0.0
dsxy = 0.0
periods = length - 1
daY = intercept + slope * periods / 2
val = intercept
for j = 0 to periods by 1
price = high[j] - val
if price > upDev
    upDev := price
price := val - low[j]
if price > dnDev
    dnDev := price
price := source[j]
dxt = price - average
dyt = val - daY
price -= val
stdDevAcc += price * price
dsxx += dxt * dxt
dsyy += dyt * dyt
dsxy += dxt * dyt
val += slope
stdDev = math.sqrt(stdDevAcc / (periods == 0 ? 1 : periods))
pearsonR = dsxx == 0 or dsyy == 0 ? 0 : dsxy / math.sqrt(dsxx * dsyy)
[stdDev, pearsonR, upDev, dnDev]

[stdDev, pearsonR, upDev, dnDev] = calcDev(sourceInput, lengthInput, s, a, i)
upper_Channel_IndicatorsStartPrice = startPrice + (useUpperDevInput ? upper_Channel_IndicatorsMultInput * stdDev : upDev)
upper_Channel_IndicatorsEndPrice = endPrice + (useUpperDevInput ? upper_Channel_IndicatorsMultInput * stdDev : upDev)
var line upper_Channel_Indicators = na
lower_Channel_IndicatorsStartPrice = startPrice + (useLowerDevInput ? -lower_Channel_IndicatorsMultInput * stdDev : -dnDev)
lower_Channel_IndicatorsEndPrice = endPrice + (useLowerDevInput ? -lower_Channel_IndicatorsMultInput * stdDev : -dnDev)
var line lower_Channel_Indicators = na
if na(upper_Channel_Indicators) and not na(upper_Channel_IndicatorsStartPrice)
    upper_Channel_Indicators := line.new(bar_index - lengthInput + 1, upper_Channel_IndicatorsStartPrice, bar_index, upper_Channel_IndicatorsEndPrice, width=1, extend=extendStyle, color=color.new(colorUpper, 0))
else
    line.set_xy1(upper_Channel_Indicators, bar_index - lengthInput + 1, upper_Channel_IndicatorsStartPrice)
    line.set_xy2(upper_Channel_Indicators, bar_index, upper_Channel_IndicatorsEndPrice)
    na
if na(lower_Channel_Indicators) and not na(lower_Channel_IndicatorsStartPrice)
    lower_Channel_Indicators := line.new(bar_index - lengthInput + 1, lower_Channel_IndicatorsStartPrice, bar_index, lower_Channel_IndicatorsEndPrice, width=1, extend=extendStyle, color=color.new(colorUpper, 0))
else
    line.set_xy1(lower_Channel_Indicators, bar_index - lengthInput + 1, lower_Channel_IndicatorsStartPrice)
    line.set_xy2(lower_Channel_Indicators, bar_index, lower_Channel_IndicatorsEndPrice)
    na
linefill.new(upper_Channel_Indicators, baseLine, color = colorUpper)
linefill.new(baseLine, lower_Channel_Indicators, color = colorLower)

// Pearson's R
var label r = na
label.delete(r[1])
if showPearsonInput and not na(pearsonR)
    r := label.new(bar_index - lengthInput + 1, lower_Channel_IndicatorsStartPrice, str.tostring(pearsonR, "#.################"), color = color.new(color.white, 100), textcolor=color.new(colorUpper, 0), size=size.normal, style=label.style_label_up)
//..................................................................AI_通道结束

//------------------------------------------------------------------------


//-----------------------------------------------OBV_auxiliary_Indicators 输出dema 21 开始

//obv_DEMAlength1 = input.int(21, minval=1)
//src_OBV_auxiliary_Indicators = input(close, title="Source")
//e1 = ta.ema(src_OBV_auxiliary_Indicators, obv_DEMAlength1)
//e2 = ta.ema(e1, obv_DEMAlength1)
//dema1 = OBV_auxiliary_Indicators?(2 * e1 - e2):na
//plot(dema1,color= color.new(color.yellow,2) , linewidth = 2)
//-----------------------------------------------OBV_auxiliary_Indicators 输出dema 21 结束


//-----------------------------------------------RSI_Indicators多空开始

// longCondition_rsi = RSI_Indicators?(ta.crossunder(ta.rsi(close, 10) , 25)):na
// shortCondition_rsi =RSI_Indicators?(ta.crossover(ta.rsi(close, 10) , 75)):na
// if longCondition_rsi
    //     alert('', alert.freq_once_per_bar)
// if shortCondition_rsi
    //     alert('', alert.freq_once_per_bar)

// plotshape(longCondition_rsi, title = "Buy Signal", text ="开多", textcolor = color.white, style=shape.labelup, size = size.normal, location=location.belowbar, color =color.new(color.blue, 10))
// plotshape(shortCondition_rsi, title = "Sell Signal",text ="开空", textcolor = color.white, style=shape.labeldown, size = size.normal, location=location.abovebar, color =color.new(color.red, 10))

// alertcondition(longCondition_rsi, title="开多", message = "开多")
// alertcondition(shortCondition_rsi, title="开空", message = "开空")
//-----------------------------------------------RSI_Indicators多空结束


//-----------------------------------------------双均线战法开始

//M1_Double_Trend_Indicators = ta.sma(close, 6)
//M2_Double_Trend_Indicators = ta.sma(close, 12)
//M3_Double_Trend_Indicators = ta.sma(close, 24)
//BBI = Double_Trend_Indicators?((M1_Double_Trend_Indicators + M2_Double_Trend_Indicators + M3_Double_Trend_Indicators) / 3):na


//len_Double_Trend_Indicators = input.int(30, minval=1, title="Length")
//src_Double_Trend_Indicators = input(close, title="Source")
//offset_Double_Trend_Indicators = input.int(title="Offset", defval=0, minval=-500, maxval=500)
//out_Double_Trend_Indicators = Double_Trend_Indicators?(ta.ema(src_Double_Trend_Indicators, len_Double_Trend_Indicators)):na
//plot(out_Double_Trend_Indicators, title="EMA30", color=color.white, offset=offset_Double_Trend_Indicators)

//plot(BBI, color = (out_Double_Trend_Indicators - BBI > 0 ? color.new(color.red,2) : color.new(color.green,2)) ,linewidth = 2)
// plot(BBI, color=color.new(color.yellow,52), linewidth=2)

//-----------------------------------------------双均线战法结束

//-----------------------------------------------神器9转开始

// transp=input(0)
// Numbers=input(true)
// SR=input(true)
// Barcolor=input(true)
// var TD = 0
// var TS = 0
// TD := close > close[4] ?nz(TD[1])+1:0
// TS := close < close[4] ?nz(TS[1])+1:0

// TDUp = TD9?(TD - ta.valuewhen(TD < TD[1], TD , 1 )):na
// TDDn = TD9?(TS - ta.valuewhen(TS < TS[1], TS , 1 )):na

// plotshape(Numbers?(TDUp==9?true:na):na,style=shape.triangledown,text="9",color=color.new(color.yellow,20),location=location.abovebar,size=size.tiny  )

// plotshape(Numbers?(TDDn==9?true:na):na,style=shape.triangleup,text="9",color=color.new(color.green,20),location=location.belowbar,size=size.tiny )


// // S/R Code By johan.gradin
// //------------//
// // Sell Setup //
// //------------//
// priceflip = ta.barssince(close<close[4])
// sell_TD9setup = close>close[4] and priceflip
// sell_TD9 = TD9?(sell_TD9setup and ta.barssince(priceflip!=9)):na
// sell_TD9overshoot = TD9?(sell_TD9setup and  ta.barssince(priceflip!=13)):na
// sell_TD9overshoot1 = TD9?(sell_TD9setup and ta.barssince(priceflip!=14)):na
// sell_TD9overshoot2 = TD9?(sell_TD9setup and ta.barssince(priceflip!=15)):na
// sell_TD9overshoot3 = TD9?(sell_TD9setup and ta.barssince(priceflip!=16)):na

// //----------//
// // Buy setup//
// //----------//
// priceflip1 = ta.barssince(close>close[4])
// buy_TD9setup = close<close[4] and priceflip1
// buy_TD9 = TD9?(buy_TD9setup and ta.barssince(priceflip1!=9)):na
// buy_TD9overshoot = TD9?(ta.barssince(priceflip1!=13) and buy_TD9setup):na
// buy_TD9overshoot1 = TD9?(ta.barssince(priceflip1!=14) and buy_TD9setup):na
// buy_TD9overshoot2 = TD9?(ta.barssince(priceflip1!=15) and buy_TD9setup):na
// buy_TD9overshoot3 = TD9?(ta.barssince(priceflip1!=16) and buy_TD9setup):na

// //----------//
// // TD lines //
// //----------//
// TDbuy_TD9h = TD9?(ta.valuewhen(buy_TD9,high,0)):na
// TDbuy_TD9l = TD9?(ta.valuewhen(buy_TD9,low,0)):na
// TDsell_TD9h = TD9?(ta.valuewhen(sell_TD9,high,0)):na
// TDsell_TD9l = TD9?(ta.valuewhen(sell_TD9,low,0)):na

// //----------//
// //   Plots  //
// //----------//

// plot(SR?(TDbuy_TD9h ? TDbuy_TD9l: na):na,style=plot.style_circles, linewidth=1, color=color.new(color.lime,20))
// plot(SR?(TDsell_TD9l ? TDsell_TD9h : na):na,style=plot.style_circles, linewidth=1, color=color.new(color.yellow,20))
// barcolor(Barcolor?(sell_TD9? #FF0000 : buy_TD9? #00FF00 : sell_TD9overshoot? #FF66A3 : sell_TD9overshoot1? #FF3385 : sell_TD9overshoot2? #FF0066 : sell_TD9overshoot3? #CC0052 : buy_TD9overshoot? #D6FF5C : buy_TD9overshoot1? #D1FF47 : buy_TD9overshoot2? #B8E62E : buy_TD9overshoot3? #8FB224 : na):na)


//-----------------------------------------------神器9转结束
