Introduction
============

The purpose of this application is to support clients’ ability to store
notes on a server, and to request notes that have certain properties.
The user may also pin/unpin any notes given certain coordinates.
Furthermore, the user can clear any notes that have not been pinned.
Finally, they can disconnect when they are done with the application.

General Tips
============

-   PLEASE START SERVER BEFORE RUNNING THE CLIENT.

-   The client is defaulted to connect via port 6550

Multithreading/Synchronization Policy
=====================================

Multithreading Socket Server
----------------------------

The server class contains a class called ClientThread which has two
uses. The first use is initializing the thread and connecting to the
socket. The second use of ClientThread is to run a thread for each
client connecting to the server. The server runs in a continuous loop
that listens for new clients to connect and runs a new thread for each
connected client.

Multithreading Socket Client
----------------------------

The client connects to the Server (via port 6550 by default) and runs a
continuous loop asking the user to input a command and then running
returning the server’s response to each command.

Error Handling
==============

Client Request
--------------

### Client Request: No Input / Not Enough Input

If the client submits either an empty request or a request with too few
arguments to the server, they are notified from the command line and
prompted to re-enter a valid command.

### POST

When posting a note from the client the user must use the following
format:

-   POST &lt;x-coordinate&gt; &lt;y-coordinate&gt; &lt;width&gt;
    &lt;height&gt; &lt;color&gt; &lt;message&gt;

Please note that there is a space between each attribute and that each
attribute **must be used**. Also, the note must fit the dimensions of
the board and the color chosen must be one of the available colors.

### GET

When submitting a GET request from the client the user must use one of
the following formats:

-   GET color=&lt;color&gt;

-   GET contains= &lt;x-coordinate y-coordinate&gt;

-   GET refersTo=&lt;message&gt;

-   GET contains= &lt;x-coordinate y-coordinate&gt;
    refersTo=&lt;message&gt;

-   GET color=&lt;color&gt; contains= &lt;x-coordinate y-coordinate&gt;

-   GET color=&lt;color&gt; refersTo=&lt;message&gt;

-   GET color=&lt;color&gt; contains= &lt;x-coordinate y-coordinate&gt;
    refersTo=&lt;message&gt;

Please note that there is no space after the equals sign for color and
refersTo, but there is a space before every new command and surrounding
the coordinates. Also, note that the GET request must be in the correct
order. Thus, color will have to be first, followed by contains and
finishing with refersTo. **We always assume this order will be the one
used**. When submitting a GET PINS request from the client the user must
use the following format:

-   GET PINS &lt;x-coordinate&gt; &lt;y-coordinate&gt;

Please note that there is a space between each attribute.

### PIN/UNPIN

When **pinning** a note from the client the user must use the following
format:

-   PIN &lt;x-coordinate y-coordinate&gt;

When **unpinning** a note from the client the user must use the
following format:

-   UNPIN &lt;x-coordinate y-coordinate&gt;

Please note that in order to place a pin, at least one note must contain
the coordinates of the pin. Additionally, there is a space between every
attribute.

### CLEAR

When clearing all notes from the client the user must use the following
format:

-   CLEAR

Please note that only the word CLEAR is needed for the function to
operate.

Server Response
---------------

### POST

If the user does not follow the exact format outlined in section 4.1.2
they will receive the following error message:

-   "POST requires more attributesPlease follow the correct format: POST
    &lt;x-coordinate&gt; &lt;y-coordinate&gt; &lt;width&gt;
    &lt;height&gt; &lt;color&gt; &lt;message&gt;".

If the users post is successful they will receive the following message:

-   "Your note has been posted!"

If the users post does not fit the board they will receive the following
message:

-   "Message not posted: Insufficient space on board..."

If the users post does contains an unavailable color they will receive
the following message:

-   "Message not posted: Color not permitted on board..."

### GET

If the user does not provide color for color=&lt;color&gt; (section
4.1.3) they will receive the following message:

-   "GET color= requires more attributes Please follow the correct
    format: GET color= &lt;color&gt;

If the user does not provide a x or y coordinate for
contains=&lt;x-coordinate&gt; &lt;y-coordinate&gt; (section 4.1.3) they
will receive the following message:

-   "GET contains= requires more attributesPlease follow the correct
    format: GET contains= &lt;x-coordinate&gt; &lt;y-coordinate&gt;"

If the user request is successful they will receive the following:

-   The note object will be returned

### PIN/UNPIN

If the user does not follow the exact format outlined in section 4.1.4
they will receive the following error message:

-   "PIN/UNPIN requires more attributesfollow the correct format:
    PIN/UNPIN &lt;x-coordinate&gt; &lt;y-coordinate&gt;"

If the users pin (section 4.1.5) is successful they will receive the
following message:

-   "Note(s) pinned successfully at coord: x y"

If the users unpin (section 4.1.5) is successful they will receive the
following message:

-   "Note(s) unpinned successfully"

If there is no notes to pin/unpin they will receive the following
message:

-   "No notes to pin/unpin - Please post note first to pin it"

### CLEAR

If the users clear (section 4.1.5) is successful they will receive the
following message:

-   "All unpinned notes cleared!"
