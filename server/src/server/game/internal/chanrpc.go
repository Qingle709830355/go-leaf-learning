package internal

import (
	"github.com/name5566/leaf/gate"
)

func init() {
	skeleton.RegisterChanRPC("NewAgent", rpcNewAgent)
	skeleton.RegisterChanRPC("CloseAgent", rpcCloseAgent)
}

func rpcNewAgent(args []interface{}) {
	a := args[0].(gate.Agent)
	OnlineAgents.Agents[a] = 1
}

func rpcCloseAgent(args []interface{}) {
	a := args[0].(gate.Agent)
	delete(OnlineAgents.Agents, a)
}
