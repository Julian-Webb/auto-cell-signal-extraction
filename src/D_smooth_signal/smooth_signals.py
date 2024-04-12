import pandas as pd


def smooth_signals(signals_df: pd.DataFrame, window_size: int) -> (pd.DataFrame, int):
    """Smoothes the raw signals by subtracting a rolling mean from the original signals.

    :param signals_df : A DataFrame where each column represents the signal of  ROI
    :param window_size : The number of frames of the window used to calculate the rolling mean.
    :return: smoothed_signals: DataFrame containing the smoothed signals for each ROI.
     n_frames_smooth: Number of frames for of the smoothed signal
    """

    rolling_mean = signals_df.rolling(window_size, center=True).mean()

    smoothed_signals = signals_df - rolling_mean

    # remove the frames (rows) at the beginning and end which are nan
    smoothed_signals.dropna(axis='index', how='all', ignore_index=True, inplace=True)

    # calculate new number of frames
    n_frames_smooth = smoothed_signals.shape[0]
    return smoothed_signals, n_frames_smooth
