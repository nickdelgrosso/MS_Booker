import matplotlib
import matplotlib.pyplot as plt

def plot_gradient(gradient, x_labelsize=20, y_labelsize=30):
    """Returns fig with gradient plotted"""
    df = gradient.copy()
    df['Time (min)'] = df['duration'].cumsum() / 60.

    fig = plt.figure()
    matplotlib.rc('xtick', labelsize=x_labelsize)
    matplotlib.rc('ytick', labelsize=y_labelsize)
    plt.plot(df['Time (min)'], df['percentB'], 'k', linewidth=10.)
    plt.ylim([0, 100])
    plt.ylabel('Percent B')
    return fig

