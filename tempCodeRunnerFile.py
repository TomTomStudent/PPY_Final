figure_labels = ['Correlation Heatmap',
                 'Model 1', 'Model 2', 'Model 3', 'Model 4']
current_figure_index = 0

fig, ax = plt.subplots(figsize=(10, 8))
heatmap = None
scatter_plot = None


def plot_correlation_heatmap():
    ax.clear()
    global heatmap
    if heatmap is not None:
        heatmap.remove()
    heatmap = sns.heatmap(correlation_matrix, annot=True,
                          cmap='flare', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap')


def plot_scatter_plot(index, y_pred, label):
    ax.clear()
    ax.scatter(y_pred, comp)
    ax.set_xlabel('Predicted PER')
    ax.set_ylabel('Actual PER')
    ax.set_title(f'Comparison of Predicted PER vs Actual PER ({label})')


def plot_figure(index):
    if index == 0:
        plot_correlation_heatmap()
    else:
        model_index = index - 1
        y_pred = [y_pred_m_1, y_pred_m_2, y_pred_m_3, y_pred_m_4][model_index]
        label = figure_labels[model_index + 1]
        plot_scatter_plot(index, y_pred, label)

    fig.canvas.draw_idle()  # Redraw the figure


def on_radio_button_clicked(label):
    global current_figure_index
    current_figure_index = figure_labels.index(label)
    plot_figure(current_figure_index)


# Initialize the plot with the first figure
plot_figure(current_figure_index)

# Create radio buttons and connect the event handler
ax_radio_buttons = plt.axes([0.2, 0.05, 0.6, 0.1])
radio_buttons = RadioButtons(ax_radio_buttons, figure_labels)
radio_buttons.on_clicked(on_radio_button_clicked)

# Show the plot
plt.show()