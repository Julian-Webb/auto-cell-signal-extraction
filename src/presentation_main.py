import os


presentation_base_dir = "/Users/julian/Desktop/Research Project I/Presentation/"
csv_path = os.path.join(presentation_base_dir, "selected_signals.csv")
raw_grid_plot_path = os.path.join(presentation_base_dir, "grid_plot_raw_signals.png")

# -------
selected_rois = all_rois[4:9, 4:9]
selected_signals = all_signals_df[selected_rois.flatten()]
selected_signals.to_csv(csv_path)
from presentation_grid_plot import presentation_grid_plot

presentation_grid_plot(selected_signals).savefig(raw_grid_plot_path)

# smooth signals
smooth_grid_plot_path = os.path.join(presentation_base_dir, "grid_plot_smooth_signals.png")
selected_signals_smooth = smoothed_signals_df[selected_rois.flatten()]
presentation_grid_plot(selected_signals_smooth).savefig(smooth_grid_plot_path)

from src.C_get_ROI_signals.visualization.single_plot import single_plot
smooth_single_plot_path = os.path.join(presentation_base_dir, "single_plot_smooth_signals.png")
single_plot(selected_signals_smooth.iloc[:, :2]).savefig(smooth_single_plot_path)