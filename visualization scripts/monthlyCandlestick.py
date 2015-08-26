import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
     DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc, plot_day_summary_ohlc
%matplotlib inline

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2015, 2, 1)
date2 = (2015, 3, 1)


mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12

quotes = quotes_historical_yahoo_ohlc('GOOG', date1, date2)
if len(quotes) == 0:
    raise SystemExit

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
#ax.xaxis.set_minor_formatter(dayFormatter)

#plot_day_summary_ohlc(ax, quotes, ticksize=3, colorup=u'g', colordown=u'r')
#candlestick_ohlc(ax, quotes, width=0.2, colorup=u'k', colordown=u'r', alpha=1.0)
candlestick_ohlc(ax, quotes, width=0.6, colorup=u'g')

ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()