package gate

import (
	"server/game"
	"server/msg"
	"server/pb"
)

func init() {
	msg.Processor.SetRouter(&pb.Hello{}, game.ChanRPC)
	msg.Processor.SetRouter(&pb.LoginRequest{}, game.ChanRPC)
	msg.Processor.SetRouter(&pb.MyMessage{}, game.ChanRPC)
	msg.Processor.SetRouter(&pb.GameHall{}, game.ChanRPC)
	msg.Processor.SetRouter(&pb.Room{}, game.ChanRPC)
}
