#!/usr/bin/env python

import re
from satispy.io import DimacsCnf
from satispy import Variable, Cnf
from satispy.solver import Minisat

class Sudoku:

  def __init__(self, pstring):
    self.grid = self._parsegrid(pstring)

  def get_cnf(self):
    return Sudoku._gen_expr(self.grid)

  def get_sat_solution(self):
    solver = Minisat()
    solution = solver.solve(self.get_cnf())
    return solution

  def solve(self):
    sol = self.get_sat_solution()
    flat = sum(Sudoku._gen_matrix(), [])
    flat = sum(flat, [])
    return [str(var) for var in flat if sol[var] == True]

  def brute_force(self):
    pass

  def get_dimacs(self):
    return str(DimacsCnf().tostring(self.get_cnf()))

  @staticmethod
  def _chunks(l, n):
    "Yield successive n-sized chunks from l."
    for i in xrange(0, len(l), n):
      yield l[i:i+n]

  @staticmethod
  def _parsegrid(pstring):
    "Returns a 2D array representing the puzzle."
    cells = [int(n) for n in re.findall(r'[0-9]', pstring.replace('.', '0'))]
    return list(Sudoku._chunks(cells, 9))

  @staticmethod 
  def _gen_expr(grid):
    result = Sudoku._gen_base_expr()
    matrix = Sudoku._gen_matrix()
    # start with row constraints
    for rownum in xrange(9):
      for colnum in xrange(9):
        val = grid[rownum][colnum]
        if val != 0:
          # print str(matrix[rownum][colnum][val-1])
          result &= matrix[rownum][colnum][val-1]
    return result

  @staticmethod
  def _gen_base_expr():
    matrix = Sudoku._gen_matrix()
    result = Cnf()
    # every cell must be included
    for row in matrix:
      for cell in row:
        temp = Cnf()
        for option in cell:
          temp |= option
        result &= temp
    # row constraints
    for row in matrix:
      for cell in row:
        for other in [thing for thing in row if thing is not cell]:
          for i in xrange(9):
            result &= -(cell[i] & other[i])
    # column constraints
    for colnum in xrange(9):
      for rownum in xrange(9):
        cell = matrix[rownum][colnum]
        for otherrow in [n for n in xrange(9) if n != rownum]:
          other = matrix[otherrow][colnum]
          for i in xrange(9):
            result &= -(cell[i] & other[i])
    # box constraints
    for rownum in xrange(9):
      for colnum in xrange(9):
        cell = matrix[rownum][colnum]
        for orow in Sudoku._get_box(matrix, rownum, colnum):
          for other in [thing for thing in orow if thing is not cell]:
            for i in xrange(9):
              result &= -(cell[i] & other[i])
    # it's so crazy it just might work
    return result

  @staticmethod 
  def _get_box(matrix, row, col):
    rdex = (row / 3) * 3
    cdex = (col / 3) * 3
    return [item[cdex:cdex+3] for item in matrix[rdex:rdex+3]]

  @staticmethod 
  def _gen_matrix():
    return [[[Variable("(%d,%d)=%d" % (row, col, val)) for val in xrange(1,10)] for col in xrange(9)] for row in xrange(9)]



