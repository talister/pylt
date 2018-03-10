import matplotlib.pyplot  as plt
import matplotlib.dates as mdates

def plot_readings(readings, low_clip=None, xlabel="", ylabel="", data_label=""):

    dates = []
    values = []
    datemin = 1e99
    datemax = -1e99
    for z in readings:
        date = mdates.date2num(z[0])
        if low_clip != None:
            if z[1] > low_clip:
                dates.append(date)
                values.append(z[1])
                
        else:
            dates.append(date)
            values.append(z[1])
        datemin = min(datemin, date)
        datemax = max(datemax, date)
    fig, ax = plt.subplots()
    ax.plot_date(dates, values, 'k-', label=data_label)

#    plt.ticklabel_format(axis='y', useOffset=False)
    ax.set_xlabel(xlabel)
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator())
    ax.set_ylabel(ylabel)
    ax.set_xlim(datemin, datemax)
    ax.format_xdata = mdates.DateFormatter('%H:%M')
#    plt.legend(fontsize='x-small')
    ax.grid(True)
    fig.autofmt_xdate()
    plt.show()
