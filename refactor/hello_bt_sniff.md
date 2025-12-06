Dec 06 13:16:04.684  ATT Send         0x0042  00:00:00:00:00:00  Write Command - Handle:0x0006 - Value: 0700 0880 0100 0B  
	Write Command - Handle:0x0006 - Value: 0700 0880 0100 0B
	Opcode: 0x52
	Attribute Handle: 0x0006 (6)
	Value: 0700 0880 0100 0B
Dec 06 13:16:04.684  L2CAP Send       0x0042  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x000A (10) [ 52 06 00 07 00 08 80 01 00 0B ]  
	Channel ID: 0x0004  Length: 0x000A (10) [ 52 06 00 07 00 08 80 01 00 0B ]
	L2CAP Payload:
	00000000: 5206 0007 0008 8001 000B                 R.........
Dec 06 13:16:04.684  ACL Send         0x0042  00:00:00:00:00:00  Data [Handle: 0x0042, Packet Boundary Flags: 0x0, Length: 0x000E (14)]  
	Packet Boundary Flags: [00] 0x00 - First Non-flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000E Bytes)
Dec 06 13:16:04.684  ACL Send         0x0000  00:00:00:00:00:00  00000000: 4200 0E00 0A00 0400 5206 0007 0008 8001  B.......R.......  
	00000000: 4200 0E00 0A00 0400 5206 0007 0008 8001  B.......R.......
	00000010: 000B                                     ..
Dec 06 13:16:04.705  ATT Receive      0x0042  00:00:00:00:00:00  Handle Value Notification - Handle:0x0009 - Value: 0500 0880 01  
	Handle Value Notification - Handle:0x0009 - Value: 0500 0880 01
	Opcode: 0x1B
	Attribute Handle: 0x0009 (9)
Dec 06 13:16:04.705  L2CAP Receive    0x0042  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 08 80 01 ]  
	Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 08 80 01 ]
	L2CAP Payload:
	00000000: 1B09 0005 0008 8001                      ........
Dec 06 13:16:04.705  ACL Receive      0x0042  00:00:00:00:00:00  Data [Handle: 0x0042, Packet Boundary Flags: 0x2, Length: 0x000C (12)]  
	Packet Boundary Flags: [10] 0x02 - First Flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000C Bytes)
Dec 06 13:16:04.705  ACL Receive      0x0000  00:00:00:00:00:00  00000000: 4220 0C00 0800 0400 1B09 0005 0008 8001  B ..............  
	00000000: 4220 0C00 0800 0400 1B09 0005 0008 8001  B ..............
Dec 06 13:16:04.720  ATT Send         0x0042  00:00:00:00:00:00  Write Command - Handle:0x0006 - Value: 8100 0001 0072 0000 00CA D870 F900 0B05…  
	Write Command - Handle:0x0006 - Value: 8100 0001 0072 0000 00CA D870 F900 0B05…
	Opcode: 0x52
	Attribute Handle: 0x0006 (6)
	Value: 8100 0001 0072 0000 00CA D870 F900 0B05 
	0001 0100 5001 FFFF FF01 0000 0000 FFFF 
	FF00 0000 6363 6363 7F63 6363 6363 0000 
	0000 FFFF FF00 0000 0000 003E 6363 7F03 
	633E 0000 0000 FFFF FF00 0000 1818 1818 
	1818 1818 1838 0000 0000 FFFF FF00 0000 
	1818 1818 1818 1818 1838 0000 0000 FFFF 
	FF00 0000 0000 003E 6363 6363 633E 0000 
	00
Dec 06 13:16:04.720  L2CAP Send       0x0042  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0084 (132) [ 52 06 00 81 00 00 01 00 72 00 00 00 CA D8 70 F9 ... ]  
	Channel ID: 0x0004  Length: 0x0084 (132) [ 52 06 00 81 00 00 01 00 72 00 00 00 CA D8 70 F9 ... ]
	L2CAP Payload:
	00000000: 5206 0081 0000 0100 7200 0000 CAD8 70F9  R.......r.....p.
	00000010: 000B 0500 0101 0050 01FF FFFF 0100 0000  .......P........
	00000020: 00FF FFFF 0000 0063 6363 637F 6363 6363  .......cccc.cccc
	00000030: 6300 0000 00FF FFFF 0000 0000 0000 3E63  c.............>c
	00000040: 637F 0363 3E00 0000 00FF FFFF 0000 0018  c..c>...........
	00000050: 1818 1818 1818 1818 3800 0000 00FF FFFF  ........8.......
	00000060: 0000 0018 1818 1818 1818 1818 3800 0000  ............8...
	00000070: 00FF FFFF 0000 0000 0000 3E63 6363 6363  ..........>ccccc
	00000080: 3E00 0000                                >...
Dec 06 13:16:04.720  ACL Send         0x0042  00:00:00:00:00:00  Data [Handle: 0x0042, Packet Boundary Flags: 0x0, Length: 0x0088 (136)]  
	Packet Boundary Flags: [00] 0x00 - First Non-flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x0088 Bytes)
Dec 06 13:16:04.720  ACL Send         0x0000  00:00:00:00:00:00  00000000: 4200 8800 8400 0400 5206 0081 0000 0100  B.......R.......  
	00000000: 4200 8800 8400 0400 5206 0081 0000 0100  B.......R.......
	00000010: 7200 0000 CAD8 70F9 000B 0500 0101 0050  r.....p........P
	00000020: 01FF FFFF 0100 0000 00FF FFFF 0000 0063  ...............c
	00000030: 6363 637F 6363 6363 6300 0000 00FF FFFF  ccc.ccccc.......
	00000040: 0000 0000 0000 3E63 637F 0363 3E00 0000  ......>cc..c>...
	00000050: 00FF FFFF 0000 0018 1818 1818 1818 1818  ................
	00000060: 3800 0000 00FF FFFF 0000 0018 1818 1818  8...............
	00000070: 1818 1818 3800 0000 00FF FFFF 0000 0000  ....8...........
	00000080: 0000 3E63 6363 6363 3E00 0000            ..>ccccc>...
Dec 06 13:16:04.764  ATT Receive      0x0042  00:00:00:00:00:00  Handle Value Notification - Handle:0x0009 - Value: 0500 0001 03  
	Handle Value Notification - Handle:0x0009 - Value: 0500 0001 03
	Opcode: 0x1B
	Attribute Handle: 0x0009 (9)
Dec 06 13:16:04.764  L2CAP Receive    0x0042  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 00 01 03 ]  
	Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 00 01 03 ]
	L2CAP Payload:
	00000000: 1B09 0005 0000 0103                      ........
Dec 06 13:16:04.764  ACL Receive      0x0042  00:00:00:00:00:00  Data [Handle: 0x0042, Packet Boundary Flags: 0x2, Length: 0x000C (12)]  
	Packet Boundary Flags: [10] 0x02 - First Flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000C Bytes)
Dec 06 13:16:04.764  ACL Receive      0x0000  00:00:00:00:00:00  00000000: 4220 0C00 0800 0400 1B09 0005 0000 0103  B ..............  
	00000000: 4220 0C00 0800 0400 1B09 0005 0000 0103  B ..............
Dec 06 13:16:04.885  HCI Event        0x0042  00:00:00:00:00:00  Number Of Completed Packets - Handle: 0x0042 - Packets: 0x0002    
	Parameter Length: 5 (0x05)
	Number Of Handles: 0x01
	Connection Handle: 0x0042
	Number Of Packets: 0x0002
Dec 06 13:16:04.885  HCI Event        0x0000  00:00:00:00:00:00  00000000: 1305 0142 0002 00                        ...B...  
	00000000: 1305 0142 0002 00                        ...B...
