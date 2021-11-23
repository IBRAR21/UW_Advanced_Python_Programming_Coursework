## Multiprocessing implementation report

##### Objective
The objective of the assignment was to speed up the loading process of CSV files into MongoDB database by applying multiprocessing.

##### Implementation
The functions "load_users" and "load_status_updates" were re-factored using pandas and multiprocessing to try to improve performance. After the implementation, cProfile was used to measure and record performance.

##### Profiling results

Below are the results from the various MongoDB implementations. The base case used Mongodb's insert_many method to insert data. Various multi-processing implementations used differnt chunk sizes to load the data into the database.

|    Implementation   Type    | Function calls |                     | Time (seconds) |                     |   |   |
|:---------------------------:|:--------------:|:-------------------:|:--------------:|:-------------------:|---|---|
|                             | load_users     | load_status_updates | load_users     | load_status_updates |   |   |
| Base (insert many)          | 50746          | 5004056             | 0.206          | 6.476               |   |   |
| Multiprocessing_cpu_count   | 12447          | 12180               | 2.969          | 18.186              |   |   |
| Multiprocessing_length/2    | 8015           | 8110                | 3.008          | 17.696              |   |   |
| Multiprocessing_length/4    | 12445          | 12178               | 3.074          | 29.108              |   |   |
| Multiprocessing_length/10   | 25783          | 24414               | 5.082          | 20.059              |   |   |
| Multiprocessing_length/15   | 39193          | 36633               | 8.553          | 25.094              |   |   |
| Multiprocessing_length/20   | 48173          | 44754               | 9.241          | 23.837              |   |   |
| Multiprocessing_size 1000   | 7976           | 413471              | 2.218          | 94.084              |   |   |
| Multiprocessing_size 100000 | 5764           | 4537                | 2.105          | 16.944              |   |   |
|                             |                |                     |                |                     |   |   |

#### Data Interpretation
Surprisingly, while multiprocessing significantly reduced the function calls, the fastest implementation remained using mongodb's insert_many and not any of the multiprocessing implementations. 

