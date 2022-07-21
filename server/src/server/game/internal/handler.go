package internal

import (
	"github.com/name5566/leaf/gate"
	"github.com/name5566/leaf/log"
	"github.com/xiaonanln/goworld/engine/uuid"
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
	handler(&pb.Room{}, handleRoom)
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

func handleRoom(args []interface{}) {
	// 处理房间相关
	m := args[0].(*pb.Room)
	a := args[1].(gate.Agent)
	isCreate := false

	if m.GetRoomId() == "" {
		// 生产新的roomId
		isCreate = true
		m.RoomId = uuid.GenUUID()
	}
	roomMap, ok := RoomsMap.RoomMap[m.GetGameType()]
	if !ok {
		// 当前游戏类型不存在房间，则创建一个新的
		roomMap = &dataStruct.RoomMap{Rooms: make(map[string]*dataStruct.Room)}
	}
	room, ok := roomMap.Rooms[m.RoomId]
	if !ok {
		// 初始化客户端列表
		agents := make(map[gate.Agent]int)
		room = &dataStruct.Room{RoomInfo: m, Agents: agents}
	}

	room.Agents[a] = 1
	if m.GetRoomId() != "no" {

		// 不等于no再添加创建房间
		roomMap.Rooms[m.RoomId] = room
	} else {
		isCreate = true
	}
	RoomsMap.RoomMap[m.GetGameType()] = roomMap

	if isCreate {
		// 当前大厅人数
		hallAgents := MapGameHallAgents.Agents[m.GetGameType()]
		// 创建房间
		gameHallInfo := &pb.GameHall{GameType: m.GetGameType(), Players: int32(len(hallAgents.Agents))}
		// 组装大厅数据
		for _, r := range roomMap.Rooms {
			gameHallInfo.Rooms = append(gameHallInfo.Rooms, r.RoomInfo)
		}
		log.Debug("用户： %v, 创建房间: %v, 当前大厅中房间个数：%v", m.GetUsers()[0].Username, m.GetRoomId(), len(roomMap.Rooms))
		// 创建房间，向所有客户端广播房间列表
		for agent := range room.Agents {
			// 生产大厅数据
			agent.WriteMsg(gameHallInfo)
		}
	} else {
		// 进入房间, 将用户信息加入房间数据中
		room.RoomInfo.Users = append(room.RoomInfo.Users, m.GetUsers()[0])
		room.RoomInfo.PlayerNum = int32(len(room.RoomInfo.Users))
		log.Debug("用户： %v 进入 房间： %v， 当前房间人数: %v", m.Users[0].Username, room.RoomInfo.RoomId, room.RoomInfo.PlayerNum)
		for agent := range room.Agents {
			agent.WriteMsg(room.RoomInfo)
		}
	}
}
