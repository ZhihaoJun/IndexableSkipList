from skip_list import SkipList
import random

def print_layer(n):
  cur = n
  line = ''
  while cur is not None:
    line += '{}:{}({}) -> '.format(cur.key, cur.value, cur.dis())
    cur = cur.next
  print(line)

def print_skip_list(sl):
  cur = sl._head
  while 1:
    print_layer(cur)
    cur = cur.down
    if cur is None:
      break

def main():
  sl = SkipList()

  sl.set(1, 1)
  sl.set(2, 2)
  sl.set(4, 4)
  sl.set(3, 3)
  sl.set(6, 6)
  sl.set(5, 5)

  print_skip_list(sl)

  sl.remove(3)

  print_skip_list(sl)

  print(sl.at(4))

def main1():
  import skip_list
  sl = skip_list.test_skip_list()
  print_skip_list(sl)
  sl.remove(3)
  print_skip_list(sl)
  print(sl.at(0))
  print(sl.range(0, 1))

if __name__ == '__main__':
  main1()
