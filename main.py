from flask import Flask, request, jsonify
from tools.db.dbmanager import Database
import timeit

if __name__ == "__main__":
    db = Database()

    db.view_table('scripts')
    db.view_table('clients')
    db.view_table('jobs')



    db.insert_into_table(table_name='clients',
                            data_dict = {"name": ["All American Auto", "Bath, Bed & Beyond"],
                                        "code": ["AAA", "BBB" ],
                                        "description":["Test client 1", "Test client 2"]
                                        }
                            )
execution_time_normal = timeit.timeit(lambda: detect_palindrome_normal(str_list[0]), number=1000)

    ## Application test goals:
    ## 1) Create and manage a database of successful/failed application runs
    ## 2) Create an API endpoint which can run scripts which will "do" something
    ## 3) Add an authentication system (either SSO or another) to restrict connections to people allowed