import matplotlib.pyplot as plt

def plot(recalls):
    """
    Plot the relative performance of link prediction methods compared to baseline random predictor.
    """
    heuristics = ['Random Predictor', 'Distance', 'Common Neighbors (user)', 'Common Neighbors (venue)', 'Adamic/Adar (user)', 'Adamic/Adar (venue)', 'Preferential Attachment', 'Katz (beta=0.005)']
    baseline = recalls[0]
    relative_performance = [float(value)/baseline for value in recalls]
    plt.grid(b=True, alpha=0.3)
    plt.axhline(y=1, color='black', linestyle='-', alpha=0.2)
    plt.scatter([i+1 for i in range(len(recalls) - 1)], relative_performance[1:], marker='_', linewidth=2, s=20*40)
    plt.xticks([i+1 for i in range(len(recalls) - 1)], heuristics[1:], rotation='vertical')
    plt.text(s='Random predictor', x=6, y=1.05)
    plt.ylabel('Relative performance ratio vs random predictions')
    plt.show()

def main():
    recalls = [
        [18.14, 4.88, 6.51, 20.93, 7.44, 20.23, 22.56, 10],
        [20.59, 14.78, 20.18, 41.59, 20.29, 42.1, 39.25, 35.68],
        [19.84, 25.27, 57.44, 64.3, 64.14, 64.84, 57.3, 66.25]
    ]
    for recall in recalls:
        plot(recall)

if __name__ == '__main__':
    main()
