package internal

import (
	"github.com/name5566/leaf/gate"
	"github.com/name5566/leaf/log"
	"google.golang.org/protobuf/proto"
	"reflect"
	"server/pb"
)

func isValid(a gate.Agent) bool {
	// 判断链接是否正常
	s := OnlineAgents[a]
	if s != 1 {
		return false
	}
	return true
}

var chatAgents = make(map[gate.Agent]struct{})

func init() {
	handler(&pb.Hello{}, handleHello)
	handler(&pb.MyMessage{}, handleMsgInfo)
	handler(&pb.LoginRequest{}, handleLogin)
}

func handler(m interface{}, h interface{}) {
	skeleton.RegisterChanRPC(reflect.TypeOf(m), h)
}

func handleHello(args []interface{}) {
	m := args[0].(*pb.Hello)
	a := args[1].(gate.Agent)

	log.Debug("hello %v", m.GetName())

	a.WriteMsg(&pb.Hello{
		Name: proto.String("client"),
	})
}

func handleMsgInfo(args []interface{}) {
	m := args[0].(*pb.MyMessage)
	//a := args[1].(gate.Agent)

	for c := range chatAgents {
		if !isValid(c) {
			delete(chatAgents, c)
			continue
		}
		log.Debug("recv user [%v] msg: %v -->", m.GetUserInfo().Username, m.GetMsg(), c.RemoteAddr())

		c.WriteMsg(&pb.MyMessage{
			Msg:      m.GetMsg(),
			UserInfo: m.GetUserInfo(),
		})
	}
}

func handleLogin(args []interface{}) {
	m := args[0].(*pb.LoginRequest)
	a := args[1].(gate.Agent)

	chatAgents[a] = struct{}{}

	log.Debug("收到用户： %v 登录游戏", m.Username)
	response := &pb.LoginResponse{Username: m.Username, Email: "test@123"}
	a.WriteMsg(response)
}
