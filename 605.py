import dpkt
from datetime import datetime
from dpkt.compat import compat_ord
from urllib.parse import unquote

def analyze_packets(pcap):
    flag = ['X'] * 39
    post_sent = False
    payload = ''
    request_time = 0
    response_time = 0
    
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            continue
        
        ip = eth.data
        tcp = ip.data
        
        if not post_sent and tcp.dport == 80 and len(tcp.data) > 0:
            request_time = timestamp
            time = datetime.utcfromtimestamp(timestamp)
            print('Timestamp: ', str(time), '(' + str(timestamp) + ')')
            
            try:
                http = dpkt.http.Request(tcp.data)
                payload = unquote(http.uri)
                print('-- request --\n {0} {1}\n'.format(http.method, payload))
                
                if http.method == 'POST':
                    post_sent = True
            except dpkt.dpkt.NeedData:
                continue
            except dpkt.dpkt.UnpackError:
                continue
        
        elif post_sent and tcp.sport == 80 and len(tcp.data) > 0:
            response_time = timestamp
            time = datetime.utcfromtimestamp(timestamp)
            print('Timestamp: ', str(time), '(' + str(timestamp) + ')')
            
            try:
                http = dpkt.http.Response(tcp.data)
                print('-- response --\n{0}'.format(http.status))
                
                if response_time - request_time >= 2.8:
                    payload = payload[payload.find('LIMIT 1),') + 9:]
                    idx = int(payload[:payload.find(',')]) - 1
                    ch = chr(int(payload[payload.find('))=') + 3:payload.find(', SLEEP(3)')]))
                    flag[idx] = ch
                    print('\n\nFound!!\n\n flag[{0}] : {1}\n\ncurrent flag : {2}'.format(idx, ch, ''.join(flag)))
            except dpkt.dpkt.NeedData:
                continue
            except dpkt.dpkt.UnpackError:
                continue
            
            post_sent = False
    
    return ''.join(flag)

pcap_file_path = './dump.pcap'

with open(pcap_file_path, 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    flag = analyze_packets(pcap)
    print('flag : ' + flag)

# 3초 이상인 패킷을 찾아서 합치는 문제 GPT가 코드 짜줬다... 
