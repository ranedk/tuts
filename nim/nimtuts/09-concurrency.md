# Threads

Nim threads work in isolated scopes, so you CANNOT have shared memory. It also has its own GC.
To activate threads, compile with `--threads:on` flag.

```nim
import locks

var
    thr: array[0..4, Thread[tuple[a,b: int]]]
    L: Lock

proc threadFunc(interval: tuple[a,b: int]) {.thread.} =
    for i in interval.a..interval.b:
        acquire(L) # lock stdout
        echo i
        release(L)

initLock(L)

for i in 0..high(thr):
    createThread(thr[i], threadFunc, (i*10, i*10+5))

joinThreads(thr)

deinitLock(L)
```

>NOTE: Threads cannot return any values from the methods

## Threadpool

The `spawn` procedure take a method and returns a value of the type `FlowVar[T]` that holds the return value of the procedure that was called.

```nim
import strformat
import os
import threadpool
import random

randomize()

proc crawler(url: string): int =
    let n = rand(5000)
    sleep(n)
    echo url
    return n

let u1 = spawn crawler("URL-1")
let u2 = spawn crawler("URL-2")
let u3 = spawn crawler("URL-3")

# Wait for all crawlers to finish
sync()

echo fmt"{^u1}, {^u2}, {^u3}"
```

If you don't want to use sync, you can block on the crawl to finish.
```nim
# This will block till all crawlers are finished
while not (u1.isReady and u2.isReady and u3.isReady):
    sleep(10)
```

If you want to block till one succeeds:
```nim
blockUntilAny(@[u1, u2, u3])
```

# Async - Await

Async await is single threaded.

Chat server using async await.

```nim
var clients {.threadvar.}: seq[AsyncSocket]

proc processClient(client: AsyncSocket) {.async.} =
    while true:
        let line = await client.recvLine()
        if line.len == 0: break
        for c in clients:
            await c.send(line & "\c\L")

proc serve() {.async.} =
    clients = @[]
    var server = newAsyncSocket()
    server.setSockOpt(OptReuseAddr, true)
    server.bindAddr(Port(12345))
    server.listen()

    while true:
        let client = await server.accept()
        clients.add client
        asyncCheck processClient(client)

asyncCheck serve()
runForever()
```
