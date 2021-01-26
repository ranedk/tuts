proc incrBy(incr: int): iterator(a:int, b:int): int =
  return iterator(a: int, b:int): int =
    var i = a
    while i <= b:
      yield i
      i += incr

let incr3 = incrBy(3)

for i in incr3(4, 20):
    echo "i = ", i

let incr4 = incrBy(4)

var output = ""
while true:
  let next = incr4(4, 20)
  if finished(incr4):
    break
  output.add($next & " ")


echo "output = ", output
