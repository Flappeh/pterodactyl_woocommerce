payload = {
    "name":"test_python",
    "user":1,
    "egg":1,
    "docker_image":"ghcr.io/pterodactyl/yolks:java_18",
    "environment":{
        "BUILD_NUMBER":"latest",
        "SERVER_JARFILE":"fabric-server-launch.jar",
        "FABRIC_VERSION":"latest",
        "LOADER_VERSION":"latest"
    },
    "startup":"java -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
    "limits":{
        "memory": 5000,
        "swap": 0,
        "disk": 10000,
        "io": 500,
        "cpu": 300
    },
    "feature_limits":{
        "databases":1,
        "backups":1,
        "allocations":4
    },
    "allocation":{
        "default":101
    }
}
print("before",payload)
payload["allocation"]["additional"] = [1,2,3]
print("after",payload)