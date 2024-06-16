## Financial Engineering-800 (Project in Financial Engineering)


**Research Question:**  How profitable is the chooser option, assuming an unforeseen jump will occur in stock price?

<br/>

We begin by studying the chooser option price:
```math
C_{chooser} (S , X , t, T , q, r) = S e^{-qT} N(d_1) - X e^{-rT} N(d_2) - S e^{-qT} N(-d_1^{*}) + X e^{-rT} N(-d_2^{*})
```

Where: 

```math
d_1 = \frac{ ln(\frac{S}{X}) + (r-q+ \frac{\sigma^2}{2})T  }{ \sigma \sqrt{T} }

d_2 = d_1 - \sigma \sqrt{T}
```

<br/>

```math
d_1^{*} = \frac{ ln(\frac{S}{X}) + (r-q)T+ (\frac{\sigma^2}{2})t  }{ \sigma \sqrt{t} }

d_2^{*} = d_1^{*} - \sigma \sqrt{t}
```



- S = Stock Price
- X = Strike Price 
- T = Time to maturity 
- r = risk-free rate
- q = dividend yield
- sigma = volatility

The plot below builds confidence in the closed form solution.

<img align="center" src="https://raw.githubusercontent.com/Riley25/FE-800/main/plots/MC_Chooser.png" width="350" height="350" />


Banks will sell over the counter (OTC) options, but they need to hedge their risk. Use delta to find the cost of hedging. 


```math
\Delta_{chooser} = e^{-qT} N( d_1 )  + e^{-qT} [N(d_1^*) -1 ]
```


```math
\Gamma_{chooser} = \frac{e^{-qT} N^{'}(d_1) }{S \sigma \sqrt{T}} + \frac{e^{-qT} N^{'}(d_1^*)}{S \sigma \sqrt{t}}
```

<img align = 'center' src='https://raw.githubusercontent.com/Riley25/FE-800/main/plots/DELTA.jpg' width = '350' height = '350' />

[Project Update]("https://github.com/Riley25/FE-800/raw/main/GROUP 6 - Team Update - October 18  (v2).pdf")
