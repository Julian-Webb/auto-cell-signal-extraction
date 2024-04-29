import random
import time

import numpy as np
import pandas as pd
import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def distance_for_one_roi(roi: str, compare_to: np.array, shared_dists):
    """Computes the distances from one ROI to all the ROIs it should be compared to."""
    for other_roi in compare_to:
        shared_dists[(roi, other_roi)] = signal_dist(roi, other_roi)


def signal_dist(roi1, roi2):
    return random.random() + 1


if __name__ == '__main__':
    # --- initialization ---
    rois = [f'roi{i}' for i in range(200)]

    rois_copy = rois.copy()

    comparisons = {}
    for roi in rois:
        rois_copy.remove(roi)
        if len(rois_copy) != 0:
            comparisons[roi] = rois_copy.copy()

    distances = pd.DataFrame(1.0, index=rois, columns=rois)

    print(f'Main ID: {id(distances)}')
    # ----------------------------

    # ---- compute distances concurrently ----
    start = time.perf_counter()
    manager = multiprocessing.Manager()
    shared_dists = manager.dict()

    # print(shared_dists)
    # Create processes
    processes = []
    for roi, compare_to in comparisons.items():
        p = multiprocessing.Process(target=distance_for_one_roi, args=(roi, compare_to, shared_dists))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print(f'concurrent part: {time.perf_counter() - start}s')

    # Enter the distances into the DataFrame
    # print(shared_dists)
    start = time.perf_counter()

    for key, dist in shared_dists.items():
        roi1, roi2 = key
        distances.loc[roi1, roi2] = distances.loc[roi2, roi1] = dist  # enter it in both permutations

    print(f'entering in df: {time.perf_counter() - start}s')
# #
#
#     # with concurrent.futures.ProcessPoolExecutor() as executor:
#     #     for roi in comparisons.keys():
#     #         executor.submit(distance_for_one_roi, roi, comparisons, distances)
#         # Note: The context handler (with) automatically waits for all processes to finish
#
#     # compute distances serially
#     # for roi in comparisons.keys():
#     #     distance_for_one_roi(roi, comparisons, distances)
#
#     print('executor finished')
#
# #
# def process_data(df_shared, index):
#     # Access the shared DataFrame
#     df = df_shared['dataframe']
#
#     print(f'function ID: {id(df)}')
#     print(type(df))
#
#     # Perform computation
#     df.loc[index, 'result'] = df.loc[index, 'value'] * 2
#
#     print('\n---- df ----')
#     print(df)
#
#
# if __name__ == '__main__':
#     # Create a DataFrame
#     data = {'value': [1, 2, 3, 4, 5]}
#     df = pd.DataFrame(data)
#
#     print(f'main ID: {id(df)}')
#
#     # Create a multiprocessing manager
#     manager = multiprocessing.Manager()
#
#     # Share the DataFrame using the manager
#     dist_shared = manager.dict()
#     dist_shared['dataframe'] = df
#
#     # Create processes
#     processes = []
#     for i in range(len(df)):
#         p = multiprocessing.Process(target=process_data, args=(dist_shared, i))
#         processes.append(p)
#         p.start()
#
#     # Wait for all processes to finish
#     for p in processes:
#         p.join()
#
#     # Retrieve the updated DataFrame
#     df_updated = dist_shared['dataframe']
#     print(df_updated)
