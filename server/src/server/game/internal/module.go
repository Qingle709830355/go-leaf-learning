package internal

import (
	"github.com/name5566/leaf/gate"
	"github.com/name5566/leaf/module"
	"server/base"
	"server/dataStruct"
)

var (
	skeleton          = base.NewSkeleton()
	ChanRPC           = skeleton.ChanRPCServer
	OnlineAgents      = dataStruct.OnlineAgents{Agents: make(map[gate.Agent]int)}
	MapGameHallAgents = dataStruct.MapGameHallAgents{Agents: make(map[string]*dataStruct.GameHallAgents)}
	RoomsMap          = dataStruct.RoomMapByGameType{RoomMap: make(map[string]*dataStruct.RoomMap)}
)

type Module struct {
	*module.Skeleton
}

func (m *Module) OnInit() {
	m.Skeleton = skeleton
}

func (m *Module) OnDestroy() {

}
