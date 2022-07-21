package dataStruct

import (
	"github.com/name5566/leaf/gate"
	"server/pb"
)

type OnlineAgents struct {
	Agents map[gate.Agent]int
}

type GameHallAgents struct {
	Agents map[gate.Agent]int
}

type MapGameHallAgents struct {
	Agents map[string]*GameHallAgents
}

type Room struct {
	Agents   map[gate.Agent]int
	RoomInfo *pb.Room
}

type RoomMap struct {
	Rooms map[string]*Room
}

type RoomMapByGameType struct {
	RoomMap map[string]*RoomMap
}
