package internal

import (
	"github.com/name5566/leaf/gate"
	"github.com/name5566/leaf/log"
	"reflect"
	"server/pb"
)

func handle(m interface{}, h interface{}) {
	skeleton.RegisterChanRPC(reflect.TypeOf(m), h)
}

func init() {
	handle(&pb.LoginResponse{}, handleLogin)
}

func handleLogin(args []interface{}) {
	m := args[0].(*pb.LoginRequest)
	a := args[1].(gate.Agent)

	log.Debug("收到用户： %v 登录游戏", m.Username)
	response := &pb.LoginResponse{Username: m.Username, Email: "test@123"}
	a.WriteMsg(response)
}
