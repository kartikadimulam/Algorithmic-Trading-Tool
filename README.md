# Alogrithmic Trading Tool

A tool that will generate trading signals using technical momentum indicators for long-short and long-only trading strategies. 

Each individual file in this project can be run separately to generate the respective strategy/visualization

## Usage
Download project to local:
```bash
git clone https://github.com/kartikadimulam/Algorithmic-Trading-Tool.git
cd Algorithmic-Trading-Tool
```
To run a backtested trading strategy:

```bash
python3 AAPL_STOCHF_Backtest.py
```

You should see an output like this: 

```bash
Estimated slippage: 0.0022
Total Strategy Returns are 10.02%
Strategy CAGR is 1.95%
Sharpe ratio of this strategy is 0.49
Maximum drawdown of Long and Short strategy is -40.87%
Total Long Only Strategy Returns are 110.36%
Long Only Strategy CAGR is 16.27%
The Sharpe ratio of the long only strategy is 0.49
Maximum drawdown of Long Only Strategy is -30.46%
| Stats Name       |   Long and Short Strategy |   Long Only Strategy |
|------------------+---------------------------+----------------------|
| Strategy Returns |                 10.0167   |            110.359   |
| Sharpe           |                  0.487167 |              1.26235 |
| CAGR             |                  1.95421  |             16.2721  |
| Maximum Drawdown |                -40.8694   |            -30.4631  |

```
![Long-Short Visualization](Long-Short.png)

To create a candlestick model:

```bash
python3 TSLA_Candlestick.py
```

This  should generate a candlestick model looking like:

![Candlestick Model](TSLA-Candlestick.png)
















