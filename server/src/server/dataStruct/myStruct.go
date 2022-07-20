package dataStruct

import "github.com/name5566/leaf/gate"

type OnlineAgents struct {
	Agents map[gate.Agent]int
}

type GameHallAgents struct {
	Agents map[gate.Agent]int
}

type MapGameHallAgents struct {
	Agents map[string]*GameHallAgents
}
