# Components of system design

## Protocols

`HTTP1.1` - Supports Pipelining (ability to send requests without waiting for response).
However, the specification also requires servers to send responses in proper order (no pipelining). This lead to **Head of line blocking** where older delayed responses can block ready new responses. Browsers do not support pipelining on HTTP1.1 because intermediate nodes also need to support pipelining, else it will fail. Since order must be maintained, any bad actor in the network can mangle responses.

`HTTP2` - Supports  Multiplexing (ability to send/receive different signals on same connection at once) with a unique ID attached to each request/response. The request/response is called a `Stream`. Because of a unique identifier in every frame (unit of data transfer), the client and the server can dismangle requests and responses and multiplexing works.

`HTTP2` also allows server push when indicated by the client. If the client wants to get a `html` page, it can also specify the `js` and `css` scripts needed for the page such that the server can push those with the html page without client generating any requests.

However, `HTTP2` is over `TCP` which doesn't isn't multiplexed; meaning that in case of packet loss, since TCP isn't aware of multiplexing (different data frames in one connection), it slows down entire connection and hence all requests/responses. So, `QUIC`, the better version of TCP will also have multiplexing, which means that packet loss will lead to slowing down of only that particular request/response and not all the other data frames. `HTTP3` over `QUIC` will solve this **Head of line blocking** problem for `HTTP2`

`REST` - Set of guidelines over `HTTP1.1` for GET, POST, PUT, DELETE. Generally uses Json or Xml.

`SOAP` - Old complex XML based protocol. Complicated and difficult because of legacy enterprises and Java people.

`gRPC` - Google's `RPC` format which standardizes on `protobuf` (binary format) over `HTTP2`. You must define `.proto` files which would generate the client and receiver code. Major advantages on parsing speed, correctness and more data structures over Json or Xml

`graphQL` - Provides a lot of flexibility for the client to request specific information from the server. It doesn't derive its advantages from `HTTP2` or `protobuf` and is used with `json` very often. While its initial goal was to avoid round trips and get the required strucured data in one go, `HTTP2` manages this better by multiplexing multiple calls into one. `graphQL` is hence more used for its nice API and control on requested data.

Data over these protocols can be further compressed with algorithms like `Kryo`

## Text encoding

UTF-8: Super cool hack to represent ASCII (127 characters) to Unidcode (1,114,112 characters). Its a variable length encoding such that initial bits encode the length of the character being represented.
UTF-32: Fixed width and very space wasting.

## Text compression

Huffman encoding: Create a frequency tree and then assign bits based on left or right traversal of tree. Basis of most text encoding methods.


## Rate limiting

1. Sliding window approach to manage number of requests per minute (the length the sliding window)
2. Timer wheel approach which manages the slot and also timeout scenario for requests which are taking too long to respond.

**Oracle**: Services register with the Oracle (it can also act as a load balancer and a heart beat system). Services can tell the api rate limit they want for themselves to the Oracle (dynamically via an API) and pass every requests request-id and timestamp to the Oracle. The Oracle can use the above mentioned rate limiting algorithms to manage throttling and timeouts of requests.


 