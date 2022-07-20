package msg

import (
	"github.com/name5566/leaf/network/protobuf"
	"server/pb"
)

var Processor = protobuf.NewProcessor()

func init() {
	Processor.Register(&pb.LoginRequest{})
	Processor.Register(&pb.MyMessage{})
	Processor.Register(&pb.Hello{})
	Processor.Register(&pb.LoginResponse{})
}
