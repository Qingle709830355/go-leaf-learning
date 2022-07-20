package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"github.com/golang/protobuf/proto"
	"github.com/name5566/leaf/log"
	"net"
	"server/pb"
)

func IntToBytes(n int, b byte) ([]byte, error) {
	switch b {

	case 1:
		tmp := int8(n)
		bytesBuffer := bytes.NewBuffer([]byte{})
		binary.Write(bytesBuffer, binary.BigEndian, &tmp)
		return bytesBuffer.Bytes(), nil
	case 2:
		tmp := int16(n)
		bytesBuffer := bytes.NewBuffer([]byte{})
		binary.Write(bytesBuffer, binary.BigEndian, &tmp)
		return bytesBuffer.Bytes(), nil
	case 3, 4:
		tmp := int32(n)
		bytesBuffer := bytes.NewBuffer([]byte{})
		binary.Write(bytesBuffer, binary.BigEndian, &tmp)
		return bytesBuffer.Bytes(), nil
	}
	return nil, fmt.Errorf("IntToBytes b param is invaild")
}

func encodeMsg(msgId int, msg proto.Message) []byte {
	data, err := proto.Marshal(msg)
	//newMsg := &pb.Hello{}
	//err = proto.Unmarshal(data, newMsg)
	if err != nil {
		log.Fatal("%v", err)
	}

	msgIdBuffer, err := IntToBytes(msgId, 2)
	if err != nil {
		log.Fatal("%v", err)
	}

	lenBuffer, err := IntToBytes(2+len(data), 2)
	m := make([]byte, 4+len(data))
	copy(m[:2], lenBuffer)
	copy(m[2:4], msgIdBuffer)
	copy(m[4:], data)
	return m
}

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:3563")
	if err != nil {
		panic(err)
	}
	defer conn.Close()
	hello := &pb.Hello{
		Name: proto.String("qinguoyu"),
	}

	conn.Write(encodeMsg(2, hello))
	//times := 30
	//for times > 0 {
	//	times -= 1
	//	time.Sleep(time.Duration(1) * time.Second)
	//}
}
