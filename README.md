# SPAM

This project includes an implementation of the [Sequential PAttern Mining(SPAM)](https://dl.acm.org/doi/abs/10.1145/775047.775109) algorithm in Python.

```
tree {'[a]': array([[1., 0., 0., 0.],
       [0., 1., 0., 0.],
       [1., 0., 0., 0.]]), '[b]': array([[1., 1., 1., 0.],
       [1., 1., 0., 0.],
       [1., 1., 0., 0.]]), '[c]': array([[0., 1., 1., 0.],
       [0., 1., 0., 0.],
       [0., 1., 0., 0.]]), '[d]': array([[1., 1., 1., 0.],
       [0., 0., 0., 0.],
       [0., 1., 0., 0.]]), '[a][a]': array([[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[a][b]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][c]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][b]': array([[0, 1, 1, 0],
       [0, 1, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][c]': array([[0, 1, 1, 0],
       [0, 1, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[c][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[a][a][a]': array([[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[a][a][b]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][a][c]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][a][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][b][b]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][b][c]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][b][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[a][c][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[a][c][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[a][d][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[b][a][a]': array([[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[b][a][b]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][a][c]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][a][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][b][b]': array([[0, 1, 1, 0],
       [0, 1, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][b][c]': array([[0, 1, 1, 0],
       [0, 1, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][b][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 1, 0, 0]], dtype=int32), '[b][c][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[b][c][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[b][d][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][a][a]': array([[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][a][b]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][a][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][a][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][b][b]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][b][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][b][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][c][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][c][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[c][d][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][a][a]': array([[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][a][b]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][a][c]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][a][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][b][b]': array([[0, 1, 1, 0],
       [0, 1, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][b][c]': array([[0, 1, 1, 0],
       [0, 1, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][b][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][c][c]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][c][d]': array([[0, 0, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32), '[d][d][d]': array([[0, 1, 1, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]], dtype=int32)}
```
