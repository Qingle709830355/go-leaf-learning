package internal

import (
	"github.com/name5566/leaf/gate"
	"github.com/name5566/leaf/log"
	"google.golang.org/protobuf/proto"
	"reflect"
	"server/dataStruct"
	"server/pb"
)

func isValid(a gate.Agent) bool {
	// 判断链接是否正常
	s := OnlineAgents.Agents[a]
	if s != 1 {
		return false
	}
	return true
}

func init() {
	handler(&pb.Hello{}, handleHello)
	handler(&pb.MyMessage{}, handleMsgInfo)
	handler(&pb.LoginRequest{}, handleLogin)
	handler(&pb.GameHall{}, handleGameHall)
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
	chatAgents := MapGameHallAgents.Agents["chat"]
	for c := range chatAgents.Agents {
		if !isValid(c) {
			delete(chatAgents.Agents, c)
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
	log.Debug("收到用户： %v 登录游戏", m.Username)
	response := &pb.LoginResponse{Username: m.Username, Email: "test@123"}
	a.WriteMsg(response)
}

func handleGameHall(args []interface{}) {
	// 处理大厅
	m := args[0].(*pb.GameHall)
	a := args[1].(gate.Agent)
	gameTypeAgents, ok := MapGameHallAgents.Agents[m.GetGameType()]
	if !ok {
		gameTypeAgents = &dataStruct.GameHallAgents{Agents: make(map[gate.Agent]int)}
		MapGameHallAgents.Agents[m.GetGameType()] = gameTypeAgents
	}
	for agent := range gameTypeAgents.Agents {
		if !isValid(agent) {
			delete(gameTypeAgents.Agents, agent)
			continue
		}
	}
	gameTypeAgents.Agents[a] = 1
	m.Players = int32(len(gameTypeAgents.Agents))
	for agent := range gameTypeAgents.Agents {
		log.Debug("发送数据到客户端： %v , 在线人数：%v", agent.RemoteAddr(), m.GetPlayers())
		agent.WriteMsg(m)
	}
}
