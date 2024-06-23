from datetime import datetime, timedelta
from speedtest import Previous, SpeedTest
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64

matplotlib.use('agg')


def get_base64_img(fig: plt.figure) -> str:
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return f'data:image/png;base64, {base64.b64encode(img.read()).decode()}'


def generate_fig(title: str) -> tuple:
    fig, ax = plt.subplots()
    plt.set_loglevel('WARNING')
    ax.set_title(title)
    ax.set_ylabel('Bandwidth (Mbps)')
    ax.set_xlabel('Time')
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.yaxis.get_major_locator().set_params(integer=True)
    return fig, ax


def get_valid_tests(start: datetime, end: datetime) -> list:
    valid = list()
    for test in Previous.tests:
        if start < test.timestamp < end:
            valid.append(test)
    return valid


def average_list(ls: list) -> float | int:
    try:
        count = 0
        for item in ls:
            count += item
        return count / len(ls)
    except ZeroDivisionError:
        return 0
    

def average_tests_day(tests: list) -> list:
    results = list()
    stack = list()
    final = list()
    prev_i = 0
    for i in range(len(tests)):
        if tests[i].timestamp.strftime('%m%d') == tests[prev_i].timestamp.strftime('%m%d'):
            stack.append(tests[i])
        else:
            results.append(stack)
            if i == len(tests) - 1:
                results.append([tests[i]])
            stack = list()
            prev_i = i
        if i == len(tests) - 1 and len(stack) != 0:
            results.append(stack)

    for day in results:
        st = SpeedTest()
        st.download_speed = round(average_list([i.download_speed for i in day]))
        st.upload_speed = round(average_list([i.upload_speed for i in day]))
        st.timestamp = datetime.strptime(day[0].timestamp.strftime('%m/%d'), '%m/%d')
        final.append(st)

    return final


def gen_plot(time_delta: timedelta, title: str) -> str:
    time = datetime.now()
    fig, ax = generate_fig(title)
    valid = get_valid_tests(time - time_delta, time)
    if timedelta(days=30) == time_delta or timedelta(days=7) == time_delta:
        valid = average_tests_day(valid)
        x = [f'{i.timestamp.strftime('%-m/%-d')}' for i in valid]
    elif timedelta(days=1) <= time_delta:
        x = [f'{i.timestamp.strftime('%-I:%M %p %-m/%-d')}' for i in valid]
    else:
        x = [f'{i.timestamp.strftime('%-I:%M %p')}' for i in valid]
    y = [i.download_speed for i in valid]
    z = [i.upload_speed for i in valid]
    ax.plot(x, y, label='Download Speed')
    ax.plot(x, z, label='Upload Speed')
    ax.legend()
    fig.autofmt_xdate()
    for x, y, z in zip(x, y, z):
        ax.annotate(y, xy=(x, y), xycoords='data', xytext=(-5, 4), textcoords='offset points')
        ax.annotate(z, xy=(x, z), xycoords='data', xytext=(-5, 4), textcoords='offset points')
        
    b64 = get_base64_img(fig)
    plt.close(fig)
    return b64 

            
        
    
    
        
    
    