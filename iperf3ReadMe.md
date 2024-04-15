# Overview

***Installing iperf3 on Ubuntu***
First, you need to install iperf3 on your Ubuntu system. It's available in the default Ubuntu repositories and can be installed via the terminal. Here’s how to do it:

1. Update  your package list to ensure you have the latest information on available packages and install iperf3:

```bash
sudo apt update
sudo apt install iperf3
```

## Running iperf3

iperf3 operates in a client-server mode, where one machine operates as the server and another as the client. Here’s how to set up and run these roles:

***Server Setup***
Start the iperf3 server on VM2 or the machine designated as the server:

```bash
iperf3 -s
```

This command starts iperf3 in **server mode**, listening on the default TCP port **5201**.

***Client Setup***
Connect the iperf3 client to the server or another client machine:

```bash
iperf3 -c <server_ip_address>
```

- The sever default is ***0.0.0.0***
- This command runs a standard test for 10 seconds.

## Customizing Tests

You can customize your tests based on what specific data you need:

- Change test duration: Add the -t option followed by the number of seconds (e.g., -t 30 for a 30-second test).
- Test bandwidth: Use the -b option to specify the bandwidth to use in the tests (e.g., -b 100M for 100 Mbps).
- Parallel connections: Use the -P option to specify the number of parallel client threads (e.g., -P 4).

### Gathering Logs

To save the test results for further analysis:
Redirect the output to a file:

```bash
iperf3 -c <server_ip_address> > iperf_log.txt
```

- This command will run the client and save the output directly into iperf_log.txt.
