proc writeToFile() =
    let langs = ["Python", "Java", "Javascript"]

    # The fmWrite constant specifies that we are opening the file for writing.
    let f = open("/tmp/random", fmWrite)

    # Close the file object when you are done with it
    defer: f.close()

    for l in langs:
        f.writeLine(l)

proc readFile() =
    # let f = open("/tmp/random")
    # defer: f.close()

    let firstLine = readFile("/tmp/random")
    echo firstLine

readFile()
