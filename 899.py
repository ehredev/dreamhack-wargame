def reverse():
    menu_str = "1_c_3_c_0__ff_3e"
    st = ['' for i in range(16)]
    org = 0
    a = 15
    for c in menu_str:
        if c == '_':
            res = 11 #res = 11 (2진수: 1011), ~res는 11111111111111111111111111110100 (32비트에서 비트 반전), ~res & 0xf는 0b0100 (하위 4비트 추출), 0b0100는 16진수로 0x4.
            org = ( res << (4 * a)) | org # 
        elif c in ['c','d','e','f']: #12 보다 큰 놈들
            res = int(c, base=16)
            org = (res << (4 * a)) | org
        else:
            res = int(c)
            org = (res << (4 * a)) | org
        a = a - 1
    return org

print(reverse())

# 다시는 이런 문제 못풀꺼같다 
