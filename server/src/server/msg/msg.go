package msg

import (
	"github.com/name5566/leaf/network/protobuf"
	"server/pb"
)

var Processor = protobuf.NewProcessor()

func init() {
	// 登录
	Processor.Register(&pb.LoginRequest{})
	// 聊天室
	Processor.Register(&pb.MyMessage{})

	// 心跳
	Processor.Register(&pb.Hello{})
	// 用户响应
	Processor.Register(&pb.LoginResponse{})
	// 游戏大厅
	Processor.Register(&pb.GameHall{})
	// 房间
	Processor.Register(&pb.Room{})
}
