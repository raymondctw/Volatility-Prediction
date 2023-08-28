# Volatility Predition

The most important things for options trader are **price and volatility movement** of underlying asset. So it's necessery to generate an algorithm to predict them. There're mess of academic research paper on these issue. But after several years experience of options trading. 

## Volatility

Volatility is a very interesting time series data. It's not like traditional random walk path, so we couldn't make it indepentently over days. 

- **Volatility Clustering**: Positive correlation with recent trend
- **Mean-Reversion**: Negative correlation with long-term volatility range

## Pillar 1: Predictor of Price Movement and Volatility
According to my past experience of options trading, TTM Squeeze is extrordinary useful for options trading. It can given the 


### Price Momentum
TTM Squeeze use common way of price momentum calculation to represent to price movement direction.

$$Momentum_t(n) = Price_t / Price_{t-n} - 1  $$



### Volatility Flag On/Off

TTM Squeeze use two factors to classify volatile situation. There're ordinary standard deviation of price and average true range. If price standard deviation is higher than average true range, it can be defined as volatile.

$$ PriceStd_t(n) = \frac{1}{n-1} \sum_{t=1}^n (Price_t - \overline{Price})$$
$$ TR_t = Max(High_t-Low_t, \vert High_t - Close_{t-1} \vert, \vert Low_t - Close_{t-1} \vert ) $$
$$ ATR_t(n) = \frac {ATR(n-1)_{t-1}+TR_t}{n}$$

**Python Example with talib**
```python
# volatility related indicators calculation
price_history_df['price_std'] = talib.STDDEV(price_data_df['close'], timeperiod=n)
price_history_df['ATR'] = talib.ATR(price_data_df['high'], price_data_df['low'], price_data_df['close'], timeperiod=n)

# volatility signal(dummy variable)
price_history_df['volatility_on'] = np.where(price_history_df['price_std'] - price_history_df['ATR'] > 0, 1, 0)
```

## Pillar 2: Mean-Reversion
Mean-Reversion is the most important characrteristic of volatility. When current volatility was near the highest level in the recent time period, it tend to be reverted to the average of volatility zone. So we can put this idea into our algorithm.

##### Step 1: Determine the base volatility series
For example, it is very common to use monthly volatility with 22 trading days.

```python
price_history_df['vol(22)'] = talib.EMA(price_history_df['abs_return'] * np.sqrt(252), timeperiod = 22)
```


##### Step 2: Calculate the percentile of last volatility figure

We can use the last 252 trading days to calculate percentile by ranking.

```python
price_history_df['vol_pr'] = price_history_df['vol(22)'].tail(252).rank()/252
print(price_history_df['vol_pr'].iloc[-1])
```

If the figure closed to 1(100%), it had reached new high of volatility in the past year. Volatility has highly probability to go back to the average range of volatility. If not? There's the new world! (Economic or fundamental condition changed)

## Summary
Is it possible to consolidate the two pillars as a aggregate indicator? In theorically, yes! But it is very hard to find the appropriate weight for each of them. In my past experience, it was a dynamic impact between two of the pillars.

|Symbol|Price Movement|Volatility|Vol PR|
|---|---|---|---|
|NVDA|$\uparrow$|$\uparrow$|45%|
|TSM|$\uparrow$|$\downarrow$|38%|
|JPM|$\downarrow$|$\uparrow$|78%|

In practice, I use the table above to make decision.
