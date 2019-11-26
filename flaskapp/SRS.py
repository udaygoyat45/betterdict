'''
today
+1 day
+2 days
+3 days
+5 days
+8 days
+13 days
+21 days
+34 days
+55 days
+89 days
+144 days
+233 days
'''

from datetime import datetime, timedelta


def new_time(date, current_level):
    fibonacci_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    return date + timedelta(days=fibonacci_sequence[current_level])
