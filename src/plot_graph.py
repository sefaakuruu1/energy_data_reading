import matplotlib.pyplot as plt



def plot_graph(time_slots_10_min, min_values_10_min, max_values_10_min, avg_values_10_min,
               time_slots_60_min, min_values_60_min, max_values_60_min, avg_values_60_min,
               time_slots_1_day,min_values_1_day, max_values_1_day, avg_values_1_day):
    plt.figure(figsize=(18, 9))

    # 10 Dakikalık Veriler
    plt.plot(time_slots_10_min, max_values_10_min, label='Max Current (10 Min)', color='red', marker='o')
    plt.plot(time_slots_10_min, avg_values_10_min, label='Average Current (10 Min)', color='blue', marker='o')
    plt.plot(time_slots_10_min, min_values_10_min, label='Min Current (10 Min)', color='green', marker='o')

    # 60 Dakikalık Veriler
    plt.plot(time_slots_60_min, max_values_60_min, label='Max Current (60 Min)', color='orange', marker='x')
    plt.plot(time_slots_60_min, avg_values_60_min, label='Average Current (60 Min)', color='purple', marker='x')
    plt.plot(time_slots_60_min, min_values_60_min, label='Min Current (60 Min)', color='brown', marker='x')

    # 1 Günlük Veriler
    plt.plot(time_slots_1_day, max_values_1_day, label='Max Current (1 Day)', color='black', marker='s')
    plt.plot(time_slots_1_day, avg_values_1_day, label='Average Current (1 Day)', color='darkblue', marker='s')
    plt.plot(time_slots_1_day, min_values_1_day, label='Min Current (1 Day)', color='darkgreen', marker='s')

    plt.title('Current Data Over Time (10 Min vs 60 Min)')
    plt.xlabel('Time Slot')
    plt.ylabel('Current Values')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
