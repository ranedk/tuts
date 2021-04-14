# Nim IO

## File read/write

This looks too much like python!

```nim
proc writeToFile() =
    let langs = ["Python", "Java", "Javascript"]

    # The fmWrite constant specifies that we are opening the file for writing.
    let f = open("/tmp/random", fmWrite)

    # Close the file object when you are done with it
    defer: f.close()

    for l in langs:
        f.writeLine(l)

writeToFile()
```

```nim
proc readFirstLine() =
    let f = open("/tmp/random")
    defer: f.close()

    let firstLine = f.readLine()
    echo firstLine

readFirstLine()


# To read entire file
let firstLine = readFile("/tmp/random")
echo firstLine
```

## Streams

For reading and writing large items. Basic usage:
```nim
import streams

var strm = newStringStream("""The first line
the second line
the third line""")

var line = ""

while strm.readLine(line):
  echo line

# Output:
# The first line
# the second line
# the third line

strm.close()
```

### FileStreams

```nim
import streams

// Writing file stream
var strm = newFileStream("/tmp/random", fmWrite)
var line = ""

if not isNil(strm):
  strm.writeLine("The first line")
  strm.writeLine("the second line")
  strm.writeLine("the third line")
  strm.close()

// Reading file stream
var strm = newFileStream("/tmp/random", fmRead)
var line = ""

if not isNil(strm):
  while strm.readLine(line):
    echo line
  strm.close()
```

### Http Client

```nim
import httpclient

# GET request
var client = newHttpClient()
echo client.getContent("http://google.com")

# POST request with file

var client = newHttpClient()
var data = newMultipartData()
data["output"] = "soap12"
data["uploaded_file"] = ("test.html", "text/html",
  "<html><head></head><body><p>test</p></body></html>")

echo client.postContent("http://validator.w3.org/check", multipart=data)


# GET Async

import asyncdispatch, httpclient

proc asyncProc(): Future[string] {.async.} =
  var client = newAsyncHttpClient()
  return await client.getContent("http://example.com")

echo waitFor asyncProc()
```

## JSON

#### Declaring JSON objects

The nim json module provide a perl like syntax:

- `%` operator which is used to create JSON objects from Nim objects
- `$` operator to convert JSON object to JSON string
- `%*` operator to create a JSON object

```nim
import json

let element = "Hydrogen"
let atomicNumber = 1

let jsonObject = %* {
    "element": element,
    "atomicNumber": atomicNumber
}

echo $jsonObject
```

#### Strings < > JSON

```nim
import json

let jsonObject = """{"name": "Sky", "age": 32}"""

let parsedObject = parseJson(jsonObject)

# Accessing a key
doAssert parsedObject["name"].getStr() == "Sky"

# Accessing an optional key, if not present, value is default of getStr
doAssert parsedObject{"foo"}.getStr() == ""

# Accessing optional key, if not present, return preset value
doAssert parsedObject{"foo"}.getStr("bar") == "bar"

# Object type is defined
doAssert parsedObject.kind == JObject
doAssert parsedObject["age"].kind == JInt

# Also parse Arrays
let jsonArray = """[7, 8, 9]"""
let parsedArray = parseJson(jsonArray)
doAssert parsedArray[1].getInt() == 8

doAssert parsedArray.kind == JArray
```

#### Object < > JSON

```nim
import json

type Lang = object
    name: string
    stars: int
    cool: bool

let cJson = %* {
    "name": "C",
    "stars": 100000000,
    "cool": false
}
# Json object to Nim Object
let c = to(cJson, Lang)

# Nim Object to Json object
let jobj = %c
doAssert jobj.kind == JObject
doAssert jobj == cJson


let nimJson = parseJson("""{ "name": "Nim", "stars": 100000, "cool": true }""")
let nim = to(nimJson, Lang)

# Object to json string, field order is maintained in json
doAssert $(%nim) == """{"name":"Nim","stars":100000,"cool":true}"""
```

# Exception handling

Very similar to python.

```nim
try:
    ...
except ErrorCode:       # Catch specific errors
    ...
except:                 # Catch all
    ...
```
