Dec 06 13:35:59.204  ATT Send         0x0043  00:00:00:00:00:00  Write Command - Handle:0x0006 - Value: 0700 0880 0100 12  
	Write Command - Handle:0x0006 - Value: 0700 0880 0100 12
	Opcode: 0x52
	Attribute Handle: 0x0006 (6)
	Value: 0700 0880 0100 12
Dec 06 13:35:59.204  L2CAP Send       0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x000A (10) [ 52 06 00 07 00 08 80 01 00 12 ]  
	Channel ID: 0x0004  Length: 0x000A (10) [ 52 06 00 07 00 08 80 01 00 12 ]
	L2CAP Payload:
	00000000: 5206 0007 0008 8001 0012                 R.........
Dec 06 13:35:59.204  ACL Send         0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x0, Length: 0x000E (14)]  
	Packet Boundary Flags: [00] 0x00 - First Non-flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000E Bytes)
Dec 06 13:35:59.204  ACL Send         0x0000  00:00:00:00:00:00  00000000: 4300 0E00 0A00 0400 5206 0007 0008 8001  C.......R.......  
	00000000: 4300 0E00 0A00 0400 5206 0007 0008 8001  C.......R.......
	00000010: 0012                                     ..
Dec 06 13:35:59.228  ATT Receive      0x0043  00:00:00:00:00:00  Handle Value Notification - Handle:0x0009 - Value: 0500 0880 01  
	Handle Value Notification - Handle:0x0009 - Value: 0500 0880 01
	Opcode: 0x1B
	Attribute Handle: 0x0009 (9)
Dec 06 13:35:59.228  L2CAP Receive    0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 08 80 01 ]  
	Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 08 80 01 ]
	L2CAP Payload:
	00000000: 1B09 0005 0008 8001                      ........
Dec 06 13:35:59.228  ACL Receive      0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x2, Length: 0x000C (12)]  
	Packet Boundary Flags: [10] 0x02 - First Flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000C Bytes)
Dec 06 13:35:59.228  ACL Receive      0x0000  00:00:00:00:00:00  00000000: 4320 0C00 0800 0400 1B09 0005 0008 8001  C ..............  
	00000000: 4320 0C00 0800 0400 1B09 0005 0008 8001  C ..............
Dec 06 13:35:59.240  ATT Send         0x0043  00:00:00:00:00:00  Write Command - Handle:0x0006 - Value: 6D00 0001 005E 0000 0043 5F9F DA00 1204…  
	Write Command - Handle:0x0006 - Value: 6D00 0001 005E 0000 0043 5F9F DA00 1204…
	Opcode: 0x52
	Attribute Handle: 0x0006 (6)
	Value: 6D00 0001 005E 0000 0043 5F9F DA00 1204 
	0001 0100 5001 FFFF FF01 0000 0000 FFFF 
	FF00 0000 0706 063E 6666 6666 6667 0000 
	0000 FFFF FF00 0000 0000 003E 6363 6363 
	633E 0000 0000 FFFF FF00 0000 1818 1818 
	1818 1818 1838 0000 0000 FFFF FF00 0000 
	0000 001E 303E 3333 3B6E 0000 00
Dec 06 13:35:59.240  L2CAP Send       0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0070 (112) [ 52 06 00 6D 00 00 01 00 5E 00 00 00 43 5F 9F DA ... ]  
	Channel ID: 0x0004  Length: 0x0070 (112) [ 52 06 00 6D 00 00 01 00 5E 00 00 00 43 5F 9F DA ... ]
	L2CAP Payload:
	00000000: 5206 006D 0000 0100 5E00 0000 435F 9FDA  R..m....^...C_..
	00000010: 0012 0400 0101 0050 01FF FFFF 0100 0000  .......P........
	00000020: 00FF FFFF 0000 0007 0606 3E66 6666 6666  ..........>fffff
	00000030: 6700 0000 00FF FFFF 0000 0000 0000 3E63  g.............>c
	00000040: 6363 6363 3E00 0000 00FF FFFF 0000 0018  cccc>...........
	00000050: 1818 1818 1818 1818 3800 0000 00FF FFFF  ........8.......
	00000060: 0000 0000 0000 1E30 3E33 333B 6E00 0000  .......0>33;n...
Dec 06 13:35:59.240  ACL Send         0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x0, Length: 0x0074 (116)]  
	Packet Boundary Flags: [00] 0x00 - First Non-flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x0074 Bytes)
Dec 06 13:35:59.240  ACL Send         0x0000  00:00:00:00:00:00  00000000: 4300 7400 7000 0400 5206 006D 0000 0100  C.t.p...R..m....  
	00000000: 4300 7400 7000 0400 5206 006D 0000 0100  C.t.p...R..m....
	00000010: 5E00 0000 435F 9FDA 0012 0400 0101 0050  ^...C_.........P
	00000020: 01FF FFFF 0100 0000 00FF FFFF 0000 0007  ................
	00000030: 0606 3E66 6666 6666 6700 0000 00FF FFFF  ..>fffffg.......
	00000040: 0000 0000 0000 3E63 6363 6363 3E00 0000  ......>ccccc>...
	00000050: 00FF FFFF 0000 0018 1818 1818 1818 1818  ................
	00000060: 3800 0000 00FF FFFF 0000 0000 0000 1E30  8..............0
	00000070: 3E33 333B 6E00 0000                      >33;n...
Dec 06 13:35:59.301  ATT Receive      0x0043  00:00:00:00:00:00  Handle Value Notification - Handle:0x0009 - Value: 0500 0001 03  
	Handle Value Notification - Handle:0x0009 - Value: 0500 0001 03
	Opcode: 0x1B
	Attribute Handle: 0x0009 (9)
Dec 06 13:35:59.301  L2CAP Receive    0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 00 01 03 ]  
	Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 00 01 03 ]
	L2CAP Payload:
	00000000: 1B09 0005 0000 0103                      ........
Dec 06 13:35:59.301  ACL Receive      0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x2, Length: 0x000C (12)]  
	Packet Boundary Flags: [10] 0x02 - First Flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000C Bytes)
Dec 06 13:35:59.301  ACL Receive      0x0000  00:00:00:00:00:00  00000000: 4320 0C00 0800 0400 1B09 0005 0000 0103  C ..............  
	00000000: 4320 0C00 0800 0400 1B09 0005 0000 0103  C ..............
Dec 06 13:35:59.406  HCI Event        0x0043  00:00:00:00:00:00  Number Of Completed Packets - Handle: 0x0043 - Packets: 0x0002    
	Parameter Length: 5 (0x05)
	Number Of Handles: 0x01
	Connection Handle: 0x0043
	Number Of Packets: 0x0002
Dec 06 13:35:59.406  HCI Event        0x0000  00:00:00:00:00:00  00000000: 1305 0143 0002 00                        ...C...  
	00000000: 1305 0143 0002 00                        ...C...
