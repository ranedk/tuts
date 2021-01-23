import typetraits

type Direction = enum
    EAST = 15,
    NORTH = 1,
    WEST = 20,
    SOUTH = 25

var num = Direction.WEST
echo "num = ", num

echo "string representation of num is = ", $(num)
echo "integer value of num = ", ord(num)
echo "num is ", num.type.name

