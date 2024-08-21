import matplotlib.pyplot as plt

def plot_graph(time_slots_10_min, min_values_10_min, max_values_10_min, avg_values_10_min,
               time_slots_60_min, min_values_60_min, max_values_60_min, avg_values_60_min,
               time_slots_1_day, min_values_1_day, max_values_1_day, avg_values_1_day):
    #plt.figure(figsize=(18, 15))

    # 10 Dakikalık Veriler İçin Subplot
    plt.plot(time_slots_10_min, max_values_10_min, label='Max Current (10 Min)', color='red', marker='o')
    plt.plot(time_slots_10_min, avg_values_10_min, label='Average Current (10 Min)', color='blue', marker='o')
    plt.plot(time_slots_10_min, min_values_10_min, label='Min Current (10 Min)', color='green', marker='o')
    plt.title('10 Dakikalık Veriler')
    plt.xlabel('Zaman Dilimi')
    plt.ylabel('Akım Değerleri')
    plt.xticks(rotation=45)

    plt.show()
    # 60 Dakikalık Veriler İçin Subplot
    plt.plot(time_slots_60_min, max_values_60_min, label='Max Current (60 Min)', color='orange', marker='x')
    plt.plot(time_slots_60_min, avg_values_60_min, label='Average Current (60 Min)', color='purple', marker='x')
    plt.plot(time_slots_60_min, min_values_60_min, label='Min Current (60 Min)', color='brown', marker='x')
    plt.title('60 Dakikalık Veriler')
    plt.xlabel('Zaman Dilimi')
    plt.ylabel('Akım Değerleri')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

    # 1 Günlük Veriler İçin Subplot
    plt.plot(time_slots_1_day, max_values_1_day, label='Max Current (1 Day)', color='black', marker='s')
    plt.plot(time_slots_1_day, avg_values_1_day, label='Average Current (1 Day)', color='darkblue', marker='s')
    plt.plot(time_slots_1_day, min_values_1_day, label='Min Current (1 Day)', color='darkgreen', marker='s')
    plt.title('1 Günlük Veriler')
    plt.xlabel('Zaman Dilimi')
    plt.ylabel('Akım Değerleri')
    plt.xticks(rotation=45)
    plt.legend()

    plt.show()
