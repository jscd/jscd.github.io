
*This post will be a bit shorter; I just think the concepts are neat*

## The Problem
So, not to get into too much detail, part of my current job involves reading data 
from embedded devices over a network. Each device introduces itself by sending a 
message which includes a device type and a protocol version. Each different
device and each different protocol needs to handle future messages in different
ways. Also, these devices are in conditions where the greatest power consumption
is used to send a message, and the largest buffer sizes possible aren't
particularly large.

How should you do this?

Okay, I'll admit, this wasn't my problem to solve, but a coworker/mentor's. His
code was written in C (originally for Windows Server, *shudders*) and the data
sent was the raw binary for a C structure. The solution he made, though, really 
made me think about how modularity in my projects could/should work, particularly
with servers and other uptime-sensitive things.

## The Solution
His solution went like this: the server starts by listening for clients to call
in, after which the server accepts an incoming message (in the form of a binary
structure) which is consistent between all possible devices. Given this header
message, the server now has the device ID (it's type), and the devices protocol
version. From there, it runs something like the following (with all the super
important error checks removed):

```
char *dlName = malloc(MAX_SIZE_OF_DL_NAME);
sprintf(dlName, "%s_%s.so", deviceId, protocolId);

pthread_t thread;
pthread_create(&thread, NULL, clientProcess, (void*) dlName);
```

So, this just creates a string based on the device Id and protocol version and
spawns a new thread using some function `clientProcess` using that name. Well
what does `clientProcess` do?

```
static void* clientProcess(void *dlNameVoid) {
    char *dlName = (char*) dlNameVoid;
    int (*lib_func)(void);

    void *lib_handle = dlopen(dlName, RTLD_LAZY);
    lib_func = dlsym(lib_handle, "cellDeviceService");

    int flag = (*lib_func)();

    dlclose(lib_handle);

    /* Free memory, handle errors, etc. etc. */
}
```

That's right. The code *dynamically loads a shared object* depending on the
device and protocol, and then calls a known function with implementation 
varying depending on the actual device and protocol.

I know this is technically exactly what these functions were designed to do, but
I think it's a very creative way to separate out server logic from protocol
implementations. Not to mention, it can continuously run; adding new devices or
protocols just involves adding new shared objects to a directory, as it'll
automatically select the correct one based on the name and spawn a new thread
for that given device and protcol.

I don't think I have anything crazy new to say about programming paradigms or
whatever, but I think it's a very neat trick to separate out code, and one I'll
try to remember in the future.

We'll C.

-------


