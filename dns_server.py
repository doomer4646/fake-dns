import socket
from dnslib import DNSRecord, QTYPE, RR, A

# サーバーの設定
HOST, PORT = '0.0.0.0', 53
CUSTOM_DOMAIN = 'example.com'
CUSTOM_RESPONSE = 'yahoo.co.jp'
EXTERNAL_DNS = '8.8.8.8'

# ソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

def handle_request(data, addr):
    request = DNSRecord.parse(data)
    qname = str(request.q.qname)
    qtype = QTYPE[request.q.qtype]

    if qname == CUSTOM_DOMAIN + '.':
        reply = request.reply()
        reply.add_answer(RR(qname, qtype, rdata=A(CUSTOM_RESPONSE)))
    else:
        # 外部DNSサーバーにフォワード
        forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forward_sock.sendto(data, (EXTERNAL_DNS, 53))
        response, _ = forward_sock.recvfrom(512)
        forward_sock.close()
        sock.sendto(response, addr)
        return

    sock.sendto(reply.pack(), addr)

print(f"DNS Server is running on {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(512)
    handle_request(data, addr)
