"""Đề bài: . là ô trắng, # là ô xám, D/N là tổng dọc/ngang."""

from model import Puzzle

SAMPLE = Puzzle("Bảng mẫu 5×5", """
# # 21/0 14/0 #
# 14/12 . . 11/0
0/21 . . . .
0/11 . . . .
# 0/16 . . #
""")

COMPLEX = Puzzle("Bảng kiểm thử 9×9", """
# # 44/0 16/0 9/0 # 15/0 44/0 #
# 0/22 . . . 11/3 . . 14/0
# 17/28 . . . . . . .
0/14 . . # 12/20 . . . .
0/17 . . 29/22 . . . . 7/0
# 12/28 . . . . 0/12 . .
0/14 . . . . 7/0 12/6 . .
0/39 . . . . . . . #
# 0/16 . . 0/8 . . . #
""")

# Bảng bổ sung để thấy MRV, mâu thuẫn và khôi phục miền khi quay lui.
DEMO = Puzzle("Minh họa quay lui 4×4", """
# 13/0 15/0 12/0
0/19 . . .
0/12 . . .
0/9 . . .
""")

PUZZLES = (SAMPLE, COMPLEX, DEMO)
