import random

class SkipListNode(object):
  def __init__(self, key, value, height, sentinel=False):
    super(SkipListNode, self).__init__()
    self.key = key
    self.value = value
    self.height = height
    self._sentinel = sentinel
    self.next = None
    self.down = None
    self._dis = 0
  
  def is_sentinel(self):
    return self._sentinel
  
  def dis(self):
    return self._dis
  
  def set_dis(self, dis):
    self._dis = dis

class SkipList(object):
  def __init__(self):
    super(SkipList, self).__init__()
    self._head = SkipListNode(0, 0, 0, True)
    self._layers = 1
    self._size = 0
  
  def find(self, key):
    cur = self._head
    while 1:
      if cur.is_sentinel():
        if cur.next is None or cur.next.key > key:
          cur = cur.down
        else:
          # ccondition is cur.next.key <= key
          cur = cur.next
      elif cur.key == key:
        return cur.value
      else:
        # there is no cur.key > key condition
        if cur.next is None or cur.next.key > key:
          cur = cur.down
        else:
          # ccondition is cur.next.key <= key
          cur = cur.next

      if cur is None:
        raise KeyError('key {} not found'.format(key))
  
  def _at(self, idx):
    if idx >= self._size:
      raise IndexError('index out of range')

    cur = self._head
    cur_idx = -1
    while 1:
      if cur.next is None or cur_idx + cur.dis() > idx:
        cur = cur.down
      else:
        cur_idx += cur.dis()
        cur = cur.next
        if cur_idx == idx:
          return cur
      
      if cur is None:
        break
    raise IndexError('index out of range')

  def at(self, idx):
    return self._at(idx).value
  
  def range(self, start_idx, end_idx):
    start_node = self._at(start_idx)
    dis = 0
    # sink down
    while start_node.down is not None:
      start_node = start_node.down
    
    cur = start_node
    result = []
    while cur is not None and dis <= end_idx - start_idx:
      result.append(cur.value)
      cur = cur.next
      dis += 1
    return result
  
  def size(self):
    return self._size

  def _flip_coin(self):
    return random.randint(0, 1)

  def _insert_height(self):
    height = 0
    for i in xrange(self._layers-1):
      if self._flip_coin() == 1:
        height += 1
    return height

  def _insert_here(self, node, key, value):
    new_node = SkipListNode(key, value, node.height)
    new_node.set_dis(1)
    new_node.next = node.next
    node.next = new_node
    return new_node

  def set(self, key, value):
    insert_height = self._insert_height()
    cur = self._head
    dis = 0
    if insert_height >= self._layers-1:
      # insert a sentinel head above
      new_head = SkipListNode(0, 0, self._layers, True)
      new_head.down = self._head
      self._layers += 1
      self._head = new_head

    last_inserted = None
    to_update = []
    to_update_idx = []
    to_update_inserted = []

    while 1:
      if cur.next is None or cur.next.key >= key:
        to_update.append(cur)
        to_update_idx.append(dis)
        to_update_inserted.append(False)

        if cur.next is not None and cur.next.key == key:
          # modify
          cur.next.value = value
        elif cur.height <= insert_height:
          # insert
          new_node = self._insert_here(cur, key, value)
          if last_inserted is not None:
            last_inserted.down = new_node
          last_inserted = new_node
          to_update_inserted[-1] = True

        cur = cur.down
      else: # cur.next.key < key
        dis += cur.dis()
        cur = cur.next

      if cur is None:
        break

    new_node_idx = dis + 1

    # update dis
    for i, n in enumerate(to_update):
      if to_update_inserted[i]:
        n.set_dis(new_node_idx - to_update_idx[i])
      else:
        n.set_dis(new_node_idx - to_update_idx[i] + 1)
    
    self._size += 1

  def remove(self, key):
    cur = self._head
    to_update = []
    dis = 0

    while 1:
      if cur.next is None or cur.next.key >= key:
        to_update.append(cur)

        if cur.next is not None and cur.next.key == key:
          # remove
          removed = cur.next
          cur.next = removed.next
          removed.down = None
          cur.set_dis(cur.dis() + removed.dis() - 1)
        elif cur.next is not None:
          cur.set_dis(cur.dis() - 1)

        cur = cur.down
      else: # cur.next.key < key
        dis += cur.dis()
        cur = cur.next

      if cur is None:
        break

    self._size -= 1

class _HandCraftSkipList(SkipList):
  def __init__(self):
    super(_HandCraftSkipList, self).__init__()
    self._i = 0

  def _insert_height(self):
    self._i += 1
    return (0, 0, 1, 2, 2, 3)[self._i - 1]

def test_skip_list():
  sl = _HandCraftSkipList()

  sl.set(1, 1)
  sl.set(2, 2)
  sl.set(4, 4)
  sl.set(3, 3)
  sl.set(6, 6)
  sl.set(5, 5)

  return sl
