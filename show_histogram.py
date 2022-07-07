import matplotlib.pyplot as plt
import numpy as np

x = np.random.normal(170, 10, 250)

def show_histogram(x):
    fig, ax = plt.subplots()
    ax.set_title('API Response Distribution')
    ax.set_xlabel('Time in Seconds ->')
    ax.set_ylabel('Total Requests ->')
    plt.hist(x)
    plt.show()
