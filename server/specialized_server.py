import asyncio
import serverpi

async def go():

    #Variables to be sued
    inBall = False
    outBall = False
    inBarrel = False
    outBarrel = False
    var_list = [inBall, outBall, inBarrel, outBarrel]

    sp = serverpi.ServerPI(name="Firsta test", port=4840)
    await sp.init_server()
     # Callback function to update variables outside of the OPCUA server.
     # the vars is a list of variables that are available inside the OPCUA server.
    async def cb_func(vars):
        vars[1] = not vars[1]
        vars[3] = not vars[3]
        await sp.write_variable("qxBall", vars[1])
        await sp.write_variable("qxBarrel", vars[3])
        vars[2] = sp.get_variable_value("ixBarrel")
        vars[0] = sp.get_variable_value("ixBall")
    
    await sp.add_variable("ixBall", inBall)
    await sp.add_variable("ixBarrel", inBarrel)
    await sp.add_variable("qxBall", outBall)
    await sp.add_variable("qxBarrel", outBarrel)
    sp.add_callback(cb_func, var_list)
    await sp.go()

if __name__ == "__main__":
    asyncio.run(go())
