//@version=4
//create by alvin@yousheng
study(title="AI_Auxiliary Graphics Indicators",shorttitle="AI_Auxiliary Graphics Indicators",overlay=false)


//开关选择项目
OBV = input(false,title = "OBV")
MACD = input(false,title = "MACD")
YSDD = input(true,title = "Top and Bottom")
RSI = input(false,title = "Trend strength")
YMJ  = input(false,title = "MJ Weighted index")
// ATR = input(false,title = "ATR")
// YSKD = input(false,title = "KD顶底")




//--------------------------------------------------OBV 开始+ 21天dema均线，跌破21天做空--------------------------------//
//---------------------------------------------------------------------------------------------------------------------//

//https://www.youtube.com/watch?v=TEUuNw-ifrc&t=628s

len_obv = input(21)
src_obv = close
lbR_obv = input(title="Pivot Lookback Right", defval=5)
lbL_obv = input(title="Pivot Lookback Left", defval=5)
rangeUpper_obv = input(title="Max of Lookback Range", defval=60)
rangeLower_obv = input(title="Min of Lookback Range", defval=5)
plotBull_obv = input(title="Plot Bullish", defval=true)
plotHiddenBull_obv = input(title="Plot Hidden Bullish", defval=false)
plotBear_obv = input(title="Plot Bearish", defval=true)
plotHiddenBear_obv = input(title="Plot Hidden Bearish", defval=false)


bearColor_obv = color.new(color.red,30)
bullColor_obv = color.new(color.green,30)
hiddenBullColor_obv = color.new(color.green,30)
hiddenBearColor_obv = color.new(color.red,30)
textColor_obv = color.new(color.white,20)
noneColor_obv = color.new(color.white,99)

obv1(src_obv) => cum(change(src_obv) > 0 ? volume : change(src_obv) < 0 ? -volume : 0*volume)
os=obv1(src_obv)


obv_osc = OBV?(os - ema(os,len_obv)):na
obc_color=obv_osc > 0 ? color.new(color.red,50) : color.new(color.green,50)
plot(obv_osc, color=obc_color, style=plot.style_line,title="OBV-Points", linewidth=2)
plot(obv_osc, color=color.new(color.gray,55), title="OBV", style=plot.style_area)
hline(0)

plFound_obv = na(pivotlow(obv_osc, lbL_obv, lbR_obv)) ? false : true
phFound_obv = na(pivothigh(obv_osc, lbL_obv, lbR_obv)) ? false : true

_inRange_obv(cond) =>
bars = barssince(cond == true)
rangeLower_obv <= bars and bars <= rangeUpper_obv

//------------------------------------------------------------------------------
// Regular Bullish

// Osc: Higher Low
oscHL_obv = obv_osc[lbR_obv] > valuewhen(plFound_obv, obv_osc[lbR_obv], 1) and _inRange_obv(plFound_obv[1])

// Price: Lower Low
priceLL_obv = low[lbR_obv] < valuewhen(plFound_obv, low[lbR_obv], 1)

bullCond_obv = OBV?(plotBull_obv and priceLL_obv and oscHL_obv and plFound_obv):na
plot(
    plFound_obv ? obv_osc[lbR_obv] : na,
offset=-lbR_obv,
       title="Regular Bullish",
             linewidth=2,
                       color=(bullCond_obv ? bullColor_obv : noneColor_obv)
)
plotshape(
    bullCond_obv ? obv_osc[lbR_obv] : na,
offset=-lbR_obv,
       title="Regular Bullish Label",
             text=" Bull ",
                  style=shape.labelup,
                        location=location.absolute,
                                 color=bullColor_obv,
                                       textcolor=textColor_obv
)
//------------------------------------------------------------------------------
// Hidden Bullish
// Osc: Lower Low
oscLL = obv_osc[lbR_obv] < valuewhen(plFound_obv, obv_osc[lbR_obv], 1) and _inRange_obv(plFound_obv[1])
// Price: Higher Low
priceHL_obv = low[lbR_obv] > valuewhen(plFound_obv, low[lbR_obv], 1)
hiddenBullCond_obv = plotHiddenBull_obv and priceHL_obv and oscLL and plFound_obv
// plot(
   // 	 plFound_obv ? obv_osc[lbR_obv] : na,
// 	 offset=-lbR_obv,
// 	 title="Hidden Bullish",
// 	 linewidth=2,
// 	 color=(hiddenBullCond_obv ? hiddenBullColor_obv : noneColor_obv)
             // 	 )
// plotshape(
   // 	 hiddenBullCond_obv ? obv_osc[lbR_obv] : na,
// 	 offset=-lbR_obv,
// 	 title="Hidden Bullish Label",
// 	 text=" H 牛 ",
// 	 style=shape.labelup,
// 	 location=location.absolute,
// 	 color=bullColor_obv,
// 	 textcolor=textColor_obv
                 // 	 )
//------------------------------------------------------------------------------
// Regular Bearish
// Osc: Lower High
oscLH_obv = obv_osc[lbR_obv] < valuewhen(phFound_obv, obv_osc[lbR_obv], 1) and _inRange_obv(phFound_obv[1])
// Price: Higher High
priceHH_obv = high[lbR_obv] > valuewhen(phFound_obv, high[lbR_obv], 1)
bearCond_obv = plotBear_obv and priceHH_obv and oscLH_obv and phFound_obv
plot(
    phFound_obv ? obv_osc[lbR_obv] : na,
offset=-lbR_obv,
       title="Regular Bearish",
             linewidth=2,
                       color=(bearCond_obv ? bearColor_obv : noneColor_obv)
)
plotshape(
    bearCond_obv ? obv_osc[lbR_obv] : na,
offset=-lbR_obv,
       title="Regular Bearish Label",
             text=" Bear ",
                  style=shape.labeldown,
                        location=location.absolute,
                                 color=bearColor_obv,
                                       textcolor=textColor_obv
)
//------------------------------------------------------------------------------
// Hidden Bearish
// Osc: Higher High
oscHH = obv_osc[lbR_obv] > valuewhen(phFound_obv, obv_osc[lbR_obv], 1) and _inRange_obv(phFound_obv[1])
// Price: Lower High
priceLH_obv = high[lbR_obv] < valuewhen(phFound_obv, high[lbR_obv], 1)
hiddenBearCond_obv = plotHiddenBear_obv and priceLH_obv and oscHH and phFound_obv
// plot(
   // 	 phFound_obv ? obv_osc[lbR_obv] : na,
// 	 offset=-lbR_obv,
// 	 title="Hidden Bearish",
// 	 linewidth=2,
// 	 color=(hiddenBearCond_obv ? hiddenBearColor_obv : noneColor_obv)
             // 	 )
// plotshape(
   // 	 hiddenBearCond_obv ? obv_osc[lbR_obv] : na,
// 	 offset=-lbR_obv,
// 	 title="Hidden Bearish Label",
// 	 text=" H 熊 ",
// 	 style=shape.labeldown,
// 	 location=location.absolute,
// 	 color=bearColor_obv,
// 	 textcolor=textColor_obv
                 // 	 )
//--------------------------------------------------OBV结束------------------------------------------------------//


//------------------------------------------------- 底进顶出 开始------------------------------------------------------//
//---------------------------------------------------------------------------------------------------------------------//

n1_ysdd = input(10, "Channel Length")
n2 = input(21, "Average Length")

//超买压力性
obLevel0 = YSDD?(input(70, "Over Bought Level 0")):na
obLevel1 = YSDD?(input(60, "Over Bought Level 1")):na
obLevel2 = YSDD?(input(52, "Over Bought Level 2")):na

// 0轴
obLeveloR = YSDD?(input(0, "Zero_Axis")):na

//超卖支撑线
osLevel0 = YSDD?(input(-70, "Over Sold Level 0")):na
osLevel1 = YSDD?(input(-61, "Over Sold Level 1")):na
osLevel2 = YSDD?(input(-51, "Over Sold Level 2")):na

ap = hlc3
esa = ema(ap, n1_ysdd)
d = ema(abs(ap - esa), n1_ysdd)
ci = (ap - esa) / (0.016 * d)
tci = ema(ci, n2)

wt1 = YSDD?(tci):na
wt2 = YSDD?(sma(wt1,4)):na
// wt2 = sma(wt1,4)

//顶部实体线
plot(0, color=color.new(color.gray,100))


//红色最大压力性
plot(obLevel0, color=color.new(color.red,15),linewidth = 2)
//顶的黄色实线
plot(obLevel1, color=color.new(color.yellow,10),linewidth = 2)
//顶的黄色虚线
plot(obLevel2, color=color.new(color.yellow,5), style=plot.style_circles)

//阴影区域
plot(wt1-wt2, color=color.new(color.blue,90),style=plot.style_area)
plot(obLeveloR, color=color.new(color.white,60),linewidth = 2)


//底的蓝色虚线
plot(osLevel2, color=color.new(color.blue,15), style=plot.style_cross)
//底的蓝色实线
plot(osLevel1, color=color.new(color.blue,10),linewidth = 2)
//底部绿色实线
plot(osLevel0, color=color.new(color.green,5),linewidth = 2)

//绿色线趋势线
plot(wt1, color=color.new(color.red,5),linewidth = 2)
//红色点线趋势线
plot(wt2, color=color.new(color.aqua,5) ,linewidth = 2)

plot(cross(wt1, wt2) ? wt2 : na, color = (wt2 - wt1 > 0 ? color.new(color.red,2) : color.new(color.green,2)) , style = plot.style_circles, linewidth = 3)

GCond=crossover(wt1,wt2)
alertcondition(GCond, "底进顶出金叉", "GoldenCross")
SCond=crossunder(wt1,wt2)
alertcondition(SCond, "底进顶出死叉", "DeathCross")

GDn3=crossunder(wt1, -70)
GUp3=crossover( wt1, 70)
alertcondition(GDn3, "底部实线3买", "实线Topsignal-Buy03")
alertcondition(GUp3, "顶部实线3卖", "实线Topsignal-Sell03")

GDnM1=crossunder(wt1, obLeveloR)
GDnM2=crossunder(wt2, obLeveloR)
alertcondition(GDnM1, "月线指标线1下穿0轴", "月线指标下穿0轴")
alertcondition(GDnM2, "月线指标线2下穿0轴", "月线指标上穿0轴")


//--------------------------------------------------  底进顶出 结束-------------------------------------------------//


//--------------------------------------------------  RSI 开始------------------------------------------------------//
//-----------------------------------------------------------------------------------------------------------------//

//https://www.youtube.com/watch?v=Pg_GsFrTorw
// 0-100范围，50是中位线，上方多，下方空 ，下30上70（超买）
// 背离  钝化低于连续3根k买，卖相反

len = input(title="RSI Period", minval=1, defval=13, type=input.integer)
src_rsi = input(title="RSI Source", defval=close)
lbR_rsi = input(title="Pivot Lookback Right", defval=5, type=input.integer)
lbL_rsi = input(title="Pivot Lookback Left", defval=5, type=input.integer)
rangeUpper_rsi = input(title="Max of Lookback Range", defval=60)
rangeLower_rsi = input(title="Min of Lookback Range", defval=5)
plotBull_rsi = input(title="Plot Bullish", defval=true)
plotHiddenBull_rsi = input(title="Plot Hidden Bullish", defval=false)
plotBear_rsi = input(title="Plot Bearish", defval=true)
plotHiddenBear_rsi = input(title="Plot Hidden Bearish", defval=false)
bearColor_rsi = color.new(color.red, 20)
bullColor_rsi = color.new(color.green, 20)
hiddenBullColor_rsi = color.new(color.green, 20)
hiddenBearColor_rsi = color.new(color.red, 20)
textColor_rsi = color.white
noneColor_rsi = color.new(color.white, 99)
osc_rsi = RSI?(rsi(src_rsi, len)):na

len_rsi = input(14,title="RSI长度")
up = rma(max(change(close), 0), len_rsi)
down = rma(-min(change(close), 0), len_rsi)
rsi = RSI?(down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))):na
plot(rsi, "RSI", color=#AEB404,linewidth=2)
lengthBand1 = RSI?69:na
lengthBandm = RSI?50:na
lengthBand0 = RSI?31:na
band1 = plot(lengthBand1, "超买区", color=color.new(#FF1493, 30))
    bandm = plot(lengthBandm, "中轨", color=color.new(#E6E6E6, 40))
        band0 = plot(lengthBand0, "超卖区",color=color.new(#ADFF2F, 40))
            fill(band1, band0, color=color.rgb(126, 87, 194, 90), title="背景")


plFound_rsi = RSI?(na(pivotlow(osc_rsi, lbL_rsi, lbR_rsi)) ? false : true):na
phFound_rsi = RSI?(na(pivothigh(osc_rsi, lbL_rsi, lbR_rsi)) ? false : true):na
_inRange_rsi(cond) =>
bars = barssince(cond == true)
rangeLower_rsi <= bars and bars <= rangeUpper_rsi

//------------------------------------------------------------------------------
// Regular Bullish
           // Osc: Higher Low

osc_rsiHL = osc_rsi[lbR_rsi] > valuewhen(plFound_rsi, osc_rsi[lbR_rsi], 1) and _inRange_rsi(plFound_rsi[1])

            // Price: Lower Low

priceLL_rsi = low[lbR_rsi] < valuewhen(plFound_rsi, low[lbR_rsi], 1)
bullCond_rsi = plotBull_rsi and priceLL_rsi and osc_rsiHL and plFound_rsi

plot(
    plFound_rsi ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Regular Bullish",
             linewidth=1,
                       color=(bullCond_rsi ? bullColor_rsi : noneColor_rsi)
)

plotshape(
    bullCond_rsi ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Regular Bullish Label",
             text="UP",
                  style=shape.labelup,
                        location=location.absolute,
                                 color=bullColor_rsi,
                                       textcolor=textColor_rsi
)

//------------------------------------------------------------------------------
  // Hidden Bullish
            // Osc: Lower Low

osc_rsiLL = osc_rsi[lbR_rsi] < valuewhen(plFound_rsi, osc_rsi[lbR_rsi], 1) and _inRange_rsi(plFound_rsi[1])

            // Price: Higher Low

priceHL = low[lbR_rsi] > valuewhen(plFound_rsi, low[lbR_rsi], 1)
hiddenBullCond = plotHiddenBull_rsi and priceHL and osc_rsiLL and plFound_rsi

plot(
    plFound_rsi ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Hidden Bullish",
             linewidth=2,
                       color=(hiddenBullCond ? hiddenBullColor_rsi : noneColor_rsi)
)

plotshape(
    hiddenBullCond ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Hidden Bullish Label",
             text="  UP ",
                  style=shape.labelup,
                        location=location.absolute,
                                 color=bullColor_rsi,
                                       textcolor=textColor_rsi
)

//------------------------------------------------------------------------------
  // Regular Bearish
             // Osc: Lower High

osc_rsiLH = osc_rsi[lbR_rsi] < valuewhen(phFound_rsi, osc_rsi[lbR_rsi], 1) and _inRange_rsi(phFound_rsi[1])

            // Price: Higher High

priceHH_rsi = high[lbR_rsi] > valuewhen(phFound_rsi, high[lbR_rsi], 1)

bearCond_rsi = plotBear_rsi and priceHH_rsi and osc_rsiLH and phFound_rsi

plot(
    phFound_rsi ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Regular Bearish",
             linewidth=1,
                       color=(bearCond_rsi ? bearColor_rsi : noneColor_rsi)
)

plotshape(
    bearCond_rsi ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Regular Bearish Label",
             text="Down",
                  style=shape.labeldown,
                        location=location.absolute,
                                 color=bearColor_rsi,
                                       textcolor=textColor_rsi
)

//------------------------------------------------------------------------------
  // Hidden Bearish
            // Osc: Higher High

osc_rsiHH = osc_rsi[lbR_rsi] > valuewhen(phFound_rsi, osc_rsi[lbR_rsi], 1) and _inRange_rsi(phFound_rsi[1])

            // Price: Lower High

priceLH = high[lbR_rsi] < valuewhen(phFound_rsi, high[lbR_rsi], 1)

hiddenBearCond = plotHiddenBear_rsi and priceLH and osc_rsiHH and phFound_rsi

plot(
    phFound_rsi ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Hidden Bearish",
             linewidth=1,
                       color=(hiddenBearCond ? hiddenBearColor_rsi : noneColor_rsi)
)

plotshape(
    hiddenBearCond ? osc_rsi[lbR_rsi] : na,
offset=-lbR_rsi,
       title="Hidden Bearish Label",
             text="Down",
                  style=shape.labeldown,
                        location=location.absolute,
                                 color=bearColor_rsi,
                                       textcolor=textColor_rsi
)


alertcondition(bullCond_rsi, title="趋势强弱买", message="趋势强弱买")
alertcondition(bearCond_rsi, title="趋势强弱卖", message="趋势强弱卖")
// alertcondition(hiddenBullCond, title="隐含RSI买", message="Hidden Bull Div {{ticker}} XXmin")
// alertcondition(hiddenBearCond, title="隐含RSI卖", message="Hidden Bear Div {{ticker}} XXmin")

//-------------------------------------------------- RSI 结束------------------------------------------------------//




                                                         //--------------------------------------------------  YMJ开始-----------------------------------------------------------//
                                                         //---------------------------------------------------------------------------------------------------------------------//


                                                         fast_mj_length = input(12,title="MACD快线长度", type=input.integer)
slow_mj_length = input(26,title="MACD慢线长度", type=input.integer)
signal_mj_length = input(9,title="MACD信号线长度", type=input.integer)


                   // fast_mj_length = input(5,title="MACD快线长度", type=input.integer)
                                       // slow_mj_length = input(13,title="MACD慢线长度", type=input.integer)
                                                           // signal_mj_length = input(5,title="MACD信号线长度", type=input.integer)

col_mj_macd_mj = input(#2962FF, "MACD", input.color, group="Color Settings", inline="MACD")
    col_mj_signal_mj = input(#FF6D00, "信号线", input.color, group="Color Settings", inline="Signal")
        col_mj_grow_above = input(#0404B4, "增长绿柱", input.color, group="Histogram", inline="Above")
            col_mj_fall_above = input(#819FF7, "减弱绿柱", input.color, group="Histogram", inline="Above")
                col_mj_grow_below = input(#F5A9A9, "减弱红柱", input.color, group="Histogram", inline="Below")
                    col_mj_fall_below = input(#FE2E2E, "增长红柱", input.color, group="Histogram", inline="Below")


                                        // Calculating
fast_mj_ma = ema(close, fast_mj_length)
slow_mj_ma = ema(close, slow_mj_length)
macd_mj = YMJ?(fast_mj_ma - slow_mj_ma):na
signal_mj = YMJ?(ema(macd_mj, signal_mj_length)):na
hist_mj = YMJ?(macd_mj - signal_mj):na
plot(hist_mj, title="直方图", style=plot.style_columns, color=color.new((hist_mj>=0 ? (hist_mj[1] < hist_mj ? col_mj_grow_above : col_mj_fall_above) : (hist_mj[1] < hist_mj ? col_mj_grow_below : col_mj_fall_below) ),0))

// 下面的参数本来是开放输入的，为了画面凌乱，先用默认值代替，但不开放输入。
// 先处理KD指标的分数，决定超买超卖区
Length_mj = input(9, minval=1)
            //长度 = 9
DLength_mj = input(3, minval=1)
             // KD参数长度 = 3
vFast_mj = stoch(close, high, low, Length_mj) // KD的快线
vSlow_mj = sma(vFast_mj, DLength_mj)
           // KD的慢线
vSlow_mj2 = sma(vSlow_mj,DLength_mj)
            // KD再一次马
K_mj = YMJ?(vSlow_mj):na
D_mj = YMJ?(vSlow_mj2):na

RSV_mj = stoch(close, high, low, 14)
var K1_mj = 0.0
var D1_mj = 0.0
K1_mj := (0.669)*nz(K1_mj[1],50)+(0.334)*nz(RSV_mj,50)
D1_mj := (0.669)*nz(D1_mj[1],50)+(0.364)*nz(K1_mj,50)
J_mj = YMJ?(((sma(3.5* K1_mj - 1.7 * D1_mj,DLength_mj))-50)*1.9):na

plot(J_mj,  color=color.yellow,title="J",linewidth = 3)
//--------------------------------------------------  YMJ结束------------------------------------------------------//



//--------------------------------------------------  macd 开始------------------------------------------------------//
                                                           //-------------------------------------------------------------------------------------------------------------------//

                                                           fast_length = input(title='快线长度 ', defval=12, type=input.integer)
slow_length = input(title='慢线长度 ', defval=26, type=input.integer)
              // fast_length = input(title='快线长度 Fast Length', defval=13, type=input.integer)
                               // slow_length = input(title='慢线长度 Slow Length', defval=34, type=input.integer)
src = input(title='Source', defval=close)
signal_length = input(title='Signal Smoothing', minval=1, maxval=50, defval=9, type=input.integer)
sma_source = input(title='Oscillator MA Type', defval='EMA', options=['SMA', 'EMA'], type=input.string)
sma_signal = input(title='Signal Line MA Type', defval='EMA', options=['SMA', 'EMA'], type=input.string)
             // Plot colors
col_macd = color.new(#2962FF, 0)
    col_signal = color.new(#FFFF00, 0)
        col_grow_above = color.new(#26A69A, 0)
            col_fall_above = color.new(#B2DFDB, 0)
                col_grow_below = color.new(#FFCDD2, 0)
                    col_fall_below = color.new(#FF5252, 0)

                                     // Calculating
fast_ma = sma_source == 'SMA' ? sma(src, fast_length) : ema(src, fast_length)
slow_ma = sma_source == 'SMA' ? sma(src, slow_length) : ema(src, slow_length)
macd = MACD?(fast_ma - slow_ma):na
signal = MACD?(sma_signal == 'SMA' ? sma(macd, signal_length) : ema(macd, signal_length)):na
hist = MACD?(macd - signal):na

                            //macd柱状图
plot(hist, title='Histogram', style=plot.style_columns, color=hist >= 0 ? hist[1] < hist ? col_grow_above : col_fall_above : hist[1] < hist ? col_grow_below : col_fall_below)
//快线
plot(macd, title='MACD', color=col_macd)
//慢线
plot(signal, title='Signal', color=col_signal)
//金叉和死叉标识
plot(cross(macd, signal) ? signal : na, color = (signal - macd > 0 ? color.new(color.red,2) : color.new(color.green,2)) , style = plot.style_circles, linewidth = 2)

lbR = input(title='向右回看K线数', defval=3)
lbL = input(title='向左回看K线数', defval=3)
rangeUpper = input(title='最大回看范围', defval=60)
rangeLower = input(title='最小回看范围', defval=5)
plotBull = input(title='Plot Bullish', defval=true)
plotBear = input(title='Plot Bearish', defval=true)

bearColor = color.red
bullColor = color.green

textColor = color.white
noneColor = color.new(color.white, 100)
osc = hist

plFound = MACD?(na(pivotlow(osc, lbL, lbR)) ? false : true):na
phFound = MACD?(na(pivothigh(osc, lbL, lbR)) ? false : true):na

_inRange(cond) =>
bars = barssince(cond == true)
rangeLower <= bars and bars <= rangeUpper

//------------------------------------------------------------------------------
// Regular Bullish
           // Osc: Higher Low

oscHL = osc[lbR] > valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1]) and osc[lbR] < 0

        // Price: Lower Low

priceLL = low[lbR] < valuewhen(plFound, low[lbR], 1)
priceHHZero = highest(osc, lbL + lbR + 5)

blowzero = priceHHZero < 0
bullCond = MACD?(plotBull and priceLL and oscHL and plFound):na


plot(plFound ? osc[lbR] : na, offset=-lbR, title='Bullish', linewidth=2, color=bullCond ? bullColor : noneColor)

plotshape(bullCond ? osc[lbR] : na, offset=-lbR, title='Regular Bullish Label', text='UP', style=shape.labelup, location=location.absolute, color=color.new(bullColor, 0), textcolor=color.new(textColor, 0))


//------------------------------------------------------------------------------
  // Regular Bearish
             // Osc: Lower High

oscLH = osc[lbR] < valuewhen(phFound, osc[lbR], 1) and _inRange(phFound[1]) and osc[lbR] > 0

priceLLZero = lowest(osc, lbL + lbR + 5)
              //plot(priceLLZero,title="priceLLZero", color=color.red)
bearzero = priceLLZero > 0

           // Price: Higher High

priceHH = high[lbR] > valuewhen(phFound, high[lbR], 1)

bearCond = plotBear and priceHH and oscLH and phFound

plot(phFound ? osc[lbR] : na, offset=-lbR, title='Bearish', linewidth=2, color=bearCond ? bearColor : noneColor)

plotshape(bearCond ? osc[lbR] : na, offset=-lbR, title='Regular Bearish Label', text='Down ', style=shape.labeldown, location=location.absolute, color=color.new(bearColor, 0), textcolor=color.new(textColor, 0))

// plot(cross(fast_ma, slow_ma) ? slow_ma : na, color = (slow_ma - fast_ma > 0 ? color.new(color.red,2) : color.new(color.green,2)) , style = plot.style_circles, linewidth = 3)

alertcondition(bullCond, title='MACD底背离买', message='MACD底背离买')
// alertcondition(bearCond, title='macd卖', message='Regular Bear Div {{ticker}} XXmin')
alertcondition(bearCond, title='MACD顶背离卖', message='MACD顶背离卖')

//--------------------------------------------------  macd 结束------------------------------------------------------//



