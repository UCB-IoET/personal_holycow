require ("cord")
calibrationTime=30
pirPin = storm.io.D2
shellip = "2001:470:66:3f9::2"
listen_port = 1337
sendsock = storm.net.udpsocket(listen_port, function() end)
lastval=0
send = 1

function setup()
	storm.io.set_mode(storm.io.INPUT, pirPin)
	storm.io.set(0, pirPin)
	print("Calibrating sensor")
	for i=0, calibrationTime do
		cord.await(storm.os.invokeLater, storm.os.SECOND)
		print(".")
	end
	print("Done. Sensor ready")
	cord.await(storm.os.invokeLater, 50*storm.os.MILLISECOND)
end

function loop()
	pirVal= storm.io.get(pirPin)
	if(pirVal ==1) then 
		print("Motion Detected") 
	end
	return pirVal
end 

cord.new(function()
	setup()
	while (1) do
		cord.await(storm.os.invokeLater, storm.os.SECOND)
		pir = loop()
		if(pir ~= lastval) then
		storm.net.sendto(sendsock, storm.mp.pack(pir), shellip, 1236)
		lastval= pir
		end
	end
	end) --end of cord.new function

cord.enter_loop()
