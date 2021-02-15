import strformat

var s = @[[1,2,3,4], [4,6,7,8]]

echo "s = ", s

var l: seq[seq[int]]

for i in 0..3:
    var s: seq[int]
    for j in 0..3:
        s.add(i * j)
    l.add(s)

echo "l = ", l
    