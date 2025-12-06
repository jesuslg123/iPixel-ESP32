Dec 06 13:32:05.518  ATT Send         0x0043  00:00:00:00:00:00  Write Command - Handle:0x0006 - Value: 0700 0880 0100 0F  
	Write Command - Handle:0x0006 - Value: 0700 0880 0100 0F
	Opcode: 0x52
	Attribute Handle: 0x0006 (6)
	Value: 0700 0880 0100 0F
Dec 06 13:32:05.518  L2CAP Send       0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x000A (10) [ 52 06 00 07 00 08 80 01 00 0F ]  
	Channel ID: 0x0004  Length: 0x000A (10) [ 52 06 00 07 00 08 80 01 00 0F ]
	L2CAP Payload:
	00000000: 5206 0007 0008 8001 000F                 R.........
Dec 06 13:32:05.518  ACL Send         0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x0, Length: 0x000E (14)]  
	Packet Boundary Flags: [00] 0x00 - First Non-flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000E Bytes)
Dec 06 13:32:05.518  ACL Send         0x0000  00:00:00:00:00:00  00000000: 4300 0E00 0A00 0400 5206 0007 0008 8001  C.......R.......  
	00000000: 4300 0E00 0A00 0400 5206 0007 0008 8001  C.......R.......
	00000010: 000F                                     ..
Dec 06 13:32:05.547  ATT Receive      0x0043  00:00:00:00:00:00  Handle Value Notification - Handle:0x0009 - Value: 0500 0880 01  
	Handle Value Notification - Handle:0x0009 - Value: 0500 0880 01
	Opcode: 0x1B
	Attribute Handle: 0x0009 (9)
Dec 06 13:32:05.547  L2CAP Receive    0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 08 80 01 ]  
	Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 08 80 01 ]
	L2CAP Payload:
	00000000: 1B09 0005 0008 8001                      ........
Dec 06 13:32:05.547  ACL Receive      0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x2, Length: 0x000C (12)]  
	Packet Boundary Flags: [10] 0x02 - First Flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000C Bytes)
Dec 06 13:32:05.547  ACL Receive      0x0000  00:00:00:00:00:00  00000000: 4320 0C00 0800 0400 1B09 0005 0008 8001  C ..............  
	00000000: 4320 0C00 0800 0400 1B09 0005 0008 8001  C ..............
Dec 06 13:32:05.557  ATT Send         0x0043  00:00:00:00:00:00  Write Command - Handle:0x0006 - Value: 3100 0001 0022 0000 0057 4EBB 8300 0F01…  
	Write Command - Handle:0x0006 - Value: 3100 0001 0022 0000 0057 4EBB 8300 0F01…
	Opcode: 0x52
	Attribute Handle: 0x0006 (6)
	Value: 3100 0001 0022 0000 0057 4EBB 8300 0F01 
	0001 0100 5001 FFFF FF01 0000 0000 FFFF 
	FF00 0000 6363 6363 7F63 6363 6363 0000 
	00
Dec 06 13:32:05.557  L2CAP Send       0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0034 (52) [ 52 06 00 31 00 00 01 00 22 00 00 00 57 4E BB 83 ... ]  
	Channel ID: 0x0004  Length: 0x0034 (52) [ 52 06 00 31 00 00 01 00 22 00 00 00 57 4E BB 83 ... ]
	L2CAP Payload:
	00000000: 5206 0031 0000 0100 2200 0000 574E BB83  R..1...."...WN..
	00000010: 000F 0100 0101 0050 01FF FFFF 0100 0000  .......P........
	00000020: 00FF FFFF 0000 0063 6363 637F 6363 6363  .......cccc.cccc
	00000030: 6300 0000                                c...
Dec 06 13:32:05.557  ACL Send         0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x0, Length: 0x0038 (56)]  
	Packet Boundary Flags: [00] 0x00 - First Non-flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x0038 Bytes)
Dec 06 13:32:05.557  ACL Send         0x0000  00:00:00:00:00:00  00000000: 4300 3800 3400 0400 5206 0031 0000 0100  C.8.4...R..1....  
	00000000: 4300 3800 3400 0400 5206 0031 0000 0100  C.8.4...R..1....
	00000010: 2200 0000 574E BB83 000F 0100 0101 0050  "...WN.........P
	00000020: 01FF FFFF 0100 0000 00FF FFFF 0000 0063  ...............c
	00000030: 6363 637F 6363 6363 6300 0000            ccc.ccccc...
Dec 06 13:32:05.605  ATT Receive      0x0043  00:00:00:00:00:00  Handle Value Notification - Handle:0x0009 - Value: 0500 0001 03  
	Handle Value Notification - Handle:0x0009 - Value: 0500 0001 03
	Opcode: 0x1B
	Attribute Handle: 0x0009 (9)
Dec 06 13:32:05.605  L2CAP Receive    0x0043  00:00:00:00:00:00  Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 00 01 03 ]  
	Channel ID: 0x0004  Length: 0x0008 (08) [ 1B 09 00 05 00 00 01 03 ]
	L2CAP Payload:
	00000000: 1B09 0005 0000 0103                      ........
Dec 06 13:32:05.605  ACL Receive      0x0043  00:00:00:00:00:00  Data [Handle: 0x0043, Packet Boundary Flags: 0x2, Length: 0x000C (12)]  
	Packet Boundary Flags: [10] 0x02 - First Flushable Packet Of Higher Layer Message (Start Of An L2CAP Packet)
	Broadcast Flags: [00] 0x00 - Point-to-point
	Data (0x000C Bytes)
Dec 06 13:32:05.605  ACL Receive      0x0000  00:00:00:00:00:00  00000000: 4320 0C00 0800 0400 1B09 0005 0000 0103  C ..............  
	00000000: 4320 0C00 0800 0400 1B09 0005 0000 0103  C ..............
Dec 06 13:32:05.725  HCI Event        0x0043  00:00:00:00:00:00  Number Of Completed Packets - Handle: 0x0043 - Packets: 0x0002    
	Parameter Length: 5 (0x05)
	Number Of Handles: 0x01
	Connection Handle: 0x0043
	Number Of Packets: 0x0002
Dec 06 13:32:05.725  HCI Event        0x0000  00:00:00:00:00:00  00000000: 1305 0143 0002 00                        ...C...  
	00000000: 1305 0143 0002 00                        ...C...
