##### Objective
In our class, we have implemented Social Network project using both relational (SQLite) and non-relational databases (MongoDb).The objective of this assignment was 
a) to generate data to compare the 2 implementations, and 
b) use the data and assignment experience to make a recommendation for the implementation method.


##### Profiling Results using cProfile
I used cProfile to time each function within the 2 database implementations.
My inital MongoDB implementation was using insert_one to load users and status into the database. To allow for equal comparison between the 2 implementations, I used 'insert_many' to bulk upload the data into each database.

The results are per below:

| Function            | SQL   Implementation |                 |         | MongoDB   Implementation |                 |         |
|---------------------|:--------------------:|:---------------:|:-------:|:------------------------:|:---------------:|:-------:|
|                     | Function Calls       | Primitive Calls | Seconds | Function Calls           | Primitive Calls | Seconds |
| load_users          | 272437               | 260402          | 0.259   | 50746                    | 50721           | 0.53    |
| load_status_updates | 23193618             | 22165618        | 21.084  | 5004057                  | 5004053         | 6.992   |
| add_user            | 1125                 | 1070            | 0.006   | 445                      | 441             | 0.042   |
| add_status          | 1010                 | 966             | 0.006   | 874                      | 862             | 0.039   |
| update_user         | 1495                 | 1426            | 0.003   | 906                      | 894             | 0.058   |
| update_status       | 2093                 | 2004            | 0.004   | 1335                     | 1315            | 0.005   |
| search_user         | 946                  | 909             | 0.002   | 940                      | 924             | 0.003   |
| search_status       | 857                  | 825             | 0.002   | 941                      | 925             | 0.003   |
| delete_status       | 1132                 | 1090            | 0.004   | 880                      | 868             | 0.05    |
| delete_user         | 1221                 | 1174            | 0.005   | 1242                     | 1226            | 0.232   |

##### Data Interpretation
The results showed that SQL implementation resulted in significantly higher function calls in most cases. SQL was much faster than MongoDb except when loading status updates, where MongoDb was considerably faster. This difference could be attributed to the large volume of data in status_updates file which my SQL implementation broke into chunks to load into the SQLite database to get around SQLite's limit on the number of bound variables in a SQL query.

##### Implementation Experience
While implementing the 2 database types, I personally preferred SQLite due to its ability to implement a schema and enforce rules over the data and develop relationship across tables, while using inter-connected data.

##### Recommendation
In my opinion, the choice of implementation technique  depends on the applicable use case. If an implementation requires dealing with an extremely large database and ability to scale, MongoDB would be preferred. However, SQL has its own advantages and would be best suited in situations that require strong referential integrity.




