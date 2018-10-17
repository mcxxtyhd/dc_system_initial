import socket
Compute_name=socket.getfqdn(socket.gethostname()) # get name
Compute_addr=socket.gethostbyname(Compute_name)   #get ip

print(Compute_name)
print(Compute_addr)


