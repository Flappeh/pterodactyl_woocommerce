#!/bin/bash

if [ "$(PROJECT)" == "purpur" ]; then
    if [ -n "${DL_PATH}" ]; then
    	echo -e "Using supplied download url: ${DL_PATH}"
    	DOWNLOAD_URL=`eval echo $(echo ${DL_PATH} | sed -e 's/{{/${/g' -e 's/}}/}/g')`
    else
    	VER_EXISTS=`curl -s https://api.purpurmc.org/v2/${PROJECT} | jq -r --arg VERSION $MINECRAFT_VERSION '.versions[] | contains($VERSION)' | grep true`
    	LATEST_VERSION=`curl -s https://api.purpurmc.org/v2/${PROJECT} | jq -r '.versions' | jq -r '.[-1]'`
    
    	if [ "${VER_EXISTS}" == "true" ]; then
    		echo -e "Version is valid. Using version ${MINECRAFT_VERSION}"
    	else
    		echo -e "Using the latest ${PROJECT} version"
    		MINECRAFT_VERSION=${LATEST_VERSION}
    	fi
    	
    	BUILD_EXISTS=`curl -s https://api.purpurmc.org/v2/${PROJECT}/${MINECRAFT_VERSION} | jq -r --arg BUILD ${BUILD_NUMBER} '.builds.all | tostring | contains($BUILD)' | grep true`
    	LATEST_BUILD=`curl -s https://api.purpurmc.org/v2/${PROJECT}/${MINECRAFT_VERSION} | jq -r '.builds.latest'`
    	
    	if [ "${BUILD_EXISTS}" == "true" ]; then
    		echo -e "Build is valid for version ${MINECRAFT_VERSION}. Using build ${BUILD_NUMBER}"
    	else
    		echo -e "Using the latest ${PROJECT} build for version ${MINECRAFT_VERSION}"
    		BUILD_NUMBER=${LATEST_BUILD}
    	fi
    	
    	JAR_NAME=${PROJECT}-${MINECRAFT_VERSION}-${BUILD_NUMBER}.jar
    	
    	echo "Version being downloaded"
    	echo -e "MC Version: ${MINECRAFT_VERSION}"
    	echo -e "Build: ${BUILD_NUMBER}"
    	echo -e "JAR Name of Build: ${JAR_NAME}"
    	DOWNLOAD_URL=https://api.purpurmc.org/v2/${PROJECT}/${MINECRAFT_VERSION}/${BUILD_NUMBER}/download
    fi
    
    cd /mnt/server
    
    echo -e "Running curl -o ${SERVER_JARFILE} ${DOWNLOAD_URL}"
    
    if [ -f ${SERVER_JARFILE} ]; then
    	mv ${SERVER_JARFILE} ${SERVER_JARFILE}.old
    fi
    
    curl -o ${SERVER_JARFILE} ${DOWNLOAD_URL}
    
    if [ ! -f server.properties ]; then
        echo -e "Downloading MC server.properties"
        curl -o server.properties https://raw.githubusercontent.com/parkervcp/eggs/master/minecraft/java/server.properties
    fi
elif [ "$(PROJECT)" == "fabric" ]; then
    apt update
    apt install -y curl jq unzip dos2unix wget
    mkdir -p /mnt/server
    cd /mnt/server
    
    # Enable snapshots
    if [ -z "$MINECRAFT_VERSION" ] || [ "$MINECRAFT_VERSION" == "latest" ]; then
      MINECRAFT_VERSION=$(curl -sSL https://meta.fabricmc.net/v2/versions/game | jq -r '.[] | select(.stable== true )|.version' | head -n1)
    elif [ "$MINECRAFT_VERSION" == "snapshot" ]; then
      MINECRAFT_VERSION=$(curl -sSL https://meta.fabricmc.net/v2/versions/game | jq -r '.[] | select(.stable== false )|.version' | head -n1)
    fi
    
    if [ -z "$FABRIC_VERSION" ] || [ "$FABRIC_VERSION" == "latest" ]; then
      FABRIC_VERSION=$(curl -sSL https://meta.fabricmc.net/v2/versions/installer | jq -r '.[0].version')
    fi
    
    if [ -z "$LOADER_VERSION" ] || [ "$LOADER_VERSION" == "latest" ]; then
      LOADER_VERSION=$(curl -sSL https://meta.fabricmc.net/v2/versions/loader | jq -r '.[] | select(.stable== true )|.version' | head -n1)
    elif [ "$LOADER_VERSION" == "snapshot" ]; then
      LOADER_VERSION=$(curl -sSL https://meta.fabricmc.net/v2/versions/loader | jq -r '.[] | select(.stable== false )|.version' | head -n1)
    fi
    
    wget -O fabric-installer.jar https://maven.fabricmc.net/net/fabricmc/fabric-installer/$FABRIC_VERSION/fabric-installer-$FABRIC_VERSION.jar
    java -jar fabric-installer.jar server -mcversion $MINECRAFT_VERSION -loader $LOADER_VERSION -downloadMinecraft
    mv fabric-server-launch.jar $SERVER_JARFILE
    echo -e "Install Complete"
    
elif [ "$(PROJECT)" == "forge" ]; then
    apt update
    apt install -y curl jq
    
    if [[ ! -d /mnt/server ]]; then
      mkdir /mnt/server
    fi
    
    cd /mnt/server
    
    # Remove spaces from the version number to avoid issues with curl
    FORGE_VERSION="$(echo "$FORGE_VERSION" | tr -d ' ')"
    MINECRAFT_VERSION="$(echo "$MINECRAFT_VERSION" | tr -d ' ')"
    
    if [[ ! -z ${FORGE_VERSION} ]]; then
      DOWNLOAD_LINK=https://maven.minecraftforge.net/net/minecraftforge/forge/${FORGE_VERSION}/forge-${FORGE_VERSION}
      FORGE_JAR=forge-${FORGE_VERSION}*.jar
    else
      JSON_DATA=$(curl -sSL https://files.minecraftforge.net/maven/net/minecraftforge/forge/promotions_slim.json)
    
      if [[ "${MINECRAFT_VERSION}" == "latest" ]] || [[ "${MINECRAFT_VERSION}" == "" ]]; then
        echo -e "getting latest version of forge."
        MINECRAFT_VERSION=$(echo -e ${JSON_DATA} | jq -r '.promos | del(."latest-1.7.10") | del(."1.7.10-latest-1.7.10") | to_entries[] | .key | select(contains("latest")) | split("-")[0]' | sort -t. -k 1,1n -k 2,2n -k 3,3n -k 4,4n | tail -1)
        BUILD_TYPE=latest
      fi
    
      if [[ "${BUILD_TYPE}" != "recommended" ]] && [[ "${BUILD_TYPE}" != "latest" ]]; then
        BUILD_TYPE=recommended
      fi
    
      echo -e "minecraft version: ${MINECRAFT_VERSION}"
      echo -e "build type: ${BUILD_TYPE}"
    
      ## some variables for getting versions and things
      FILE_SITE=https://maven.minecraftforge.net/net/minecraftforge/forge/
      VERSION_KEY=$(echo -e ${JSON_DATA} | jq -r --arg MINECRAFT_VERSION "${MINECRAFT_VERSION}" --arg BUILD_TYPE "${BUILD_TYPE}" '.promos | del(."latest-1.7.10") | del(."1.7.10-latest-1.7.10") | to_entries[] | .key | select(contains($MINECRAFT_VERSION)) | select(contains($BUILD_TYPE))')
    
      ## locating the forge version
      if [[ "${VERSION_KEY}" == "" ]] && [[ "${BUILD_TYPE}" == "recommended" ]]; then
        echo -e "dropping back to latest from recommended due to there not being a recommended version of forge for the mc version requested."
        VERSION_KEY=$(echo -e ${JSON_DATA} | jq -r --arg MINECRAFT_VERSION "${MINECRAFT_VERSION}" '.promos | del(."latest-1.7.10") | del(."1.7.10-latest-1.7.10") | to_entries[] | .key | select(contains($MINECRAFT_VERSION)) | select(contains("latest"))')
      fi
    
      ## Error if the mc version set wasn't valid.
      if [ "${VERSION_KEY}" == "" ] || [ "${VERSION_KEY}" == "null" ]; then
        echo -e "The install failed because there is no valid version of forge for the version of minecraft selected."
        exit 1
      fi
    
      FORGE_VERSION=$(echo -e ${JSON_DATA} | jq -r --arg VERSION_KEY "$VERSION_KEY" '.promos | .[$VERSION_KEY]')
    
      if [[ "${MINECRAFT_VERSION}" == "1.7.10" ]] || [[ "${MINECRAFT_VERSION}" == "1.8.9" ]]; then
        DOWNLOAD_LINK=${FILE_SITE}${MINECRAFT_VERSION}-${FORGE_VERSION}-${MINECRAFT_VERSION}/forge-${MINECRAFT_VERSION}-${FORGE_VERSION}-${MINECRAFT_VERSION}
        FORGE_JAR=forge-${MINECRAFT_VERSION}-${FORGE_VERSION}-${MINECRAFT_VERSION}.jar
        if [[ "${MINECRAFT_VERSION}" == "1.7.10" ]]; then
          FORGE_JAR=forge-${MINECRAFT_VERSION}-${FORGE_VERSION}-${MINECRAFT_VERSION}-universal.jar
        fi
      else
        DOWNLOAD_LINK=${FILE_SITE}${MINECRAFT_VERSION}-${FORGE_VERSION}/forge-${MINECRAFT_VERSION}-${FORGE_VERSION}
        FORGE_JAR=forge-${MINECRAFT_VERSION}-${FORGE_VERSION}.jar
      fi
    fi
    
    #Adding .jar when not eding by SERVER_JARFILE
    if [[ ! $SERVER_JARFILE = *\.jar ]]; then
      SERVER_JARFILE="$SERVER_JARFILE.jar"
    fi
    
    #Downloading jars
    echo -e "Downloading forge version ${FORGE_VERSION}"
    echo -e "Download link is ${DOWNLOAD_LINK}"
    
    if [[ ! -z "${DOWNLOAD_LINK}" ]]; then
      if curl -sSL --output /dev/null --head --fail ${DOWNLOAD_LINK}-installer.jar; then
        echo -e "installer jar download link is valid."
      else
        echo -e "link is invalid. Exiting now"
        exit 2
      fi
    else
      echo -e "no download link provided. Exiting now"
      exit 3
    fi
    
    curl -sSL -o installer.jar ${DOWNLOAD_LINK}-installer.jar
    
    #Checking if downloaded jars exist
    if [[ ! -f ./installer.jar ]]; then
      echo "!!! Error downloading forge version ${FORGE_VERSION} !!!"
      exit
    fi
    
    function  unix_args {
      echo -e "Detected Forge 1.17 or newer version. Setting up forge unix args."
      ln -sf libraries/net/minecraftforge/forge/*/unix_args.txt unix_args.txt
    }
    
    # Delete args to support downgrading/upgrading
    rm -rf libraries/net/minecraftforge/forge
    rm unix_args.txt
    
    #Installing server
    echo -e "Installing forge server.\n"
    java -jar installer.jar --installServer || { echo -e "install failed using Forge version ${FORGE_VERSION} and Minecraft version ${MINECRAFT_VERSION}"; exit 4; }
    
    # Check if we need a symlink for 1.17+ Forge JPMS args
    if [[ $MINECRAFT_VERSION =~ ^1\.(17|18|19|20|21|22|23) || $FORGE_VERSION =~ ^1\.(17|18|19|20|21|22|23) ]]; then
      unix_args
    
    # Check if someone has set MC to latest but overwrote it with older Forge version, otherwise we would have false positives
    elif [[ $MINECRAFT_VERSION == "latest" && $FORGE_VERSION =~ ^1\.(17|18|19|20|21|22|23) ]]; then
      unix_args
    else
      # For versions below 1.17 that ship with jar
      mv $FORGE_JAR $SERVER_JARFILE
    fi
    
    echo -e "Deleting installer.jar file.\n"
    rm -rf installer.jar
    
    echo "-----------------------------------------"
    echo "Installation completed..."
    echo "-----------------------------------------"

elif [ "$(PROJECT)" == "waterfall" ]; then
    apt update
    apt install -y curl jq
    
    if [ -n "${DL_PATH}" ]; then
    	echo -e "Using supplied download url: ${DL_PATH}"
    	DOWNLOAD_URL=`eval echo $(echo ${DL_PATH} | sed -e 's/{{/${/g' -e 's/}}/}/g')`
    else
    	VER_EXISTS=`curl -s https://papermc.io/api/v2/projects/${PROJECT} | jq -r --arg VERSION $MINECRAFT_VERSION '.versions[] | contains($VERSION)' | grep true`
    	LATEST_VERSION=`curl -s https://papermc.io/api/v2/projects/${PROJECT} | jq -r '.versions' | jq -r '.[-1]'`
    
    	if [ "${VER_EXISTS}" == "true" ]; then
    		echo -e "Version is valid. Using version ${MINECRAFT_VERSION}"
    	else
    		echo -e "Using the latest ${PROJECT} version"
    		MINECRAFT_VERSION=${LATEST_VERSION}
    	fi
    	
    	BUILD_EXISTS=`curl -s https://papermc.io/api/v2/projects/${PROJECT}/versions/${MINECRAFT_VERSION} | jq -r --arg BUILD ${BUILD_NUMBER} '.builds[] | tostring | contains($BUILD)' | grep true`
    	LATEST_BUILD=`curl -s https://papermc.io/api/v2/projects/${PROJECT}/versions/${MINECRAFT_VERSION} | jq -r '.builds' | jq -r '.[-1]'`
    	
    	if [ "${BUILD_EXISTS}" == "true" ]; then
    		echo -e "Build is valid for version ${MINECRAFT_VERSION}. Using build ${BUILD_NUMBER}"
    	else
    		echo -e "Using the latest ${PROJECT} build for version ${MINECRAFT_VERSION}"
    		BUILD_NUMBER=${LATEST_BUILD}
    	fi
    	
    	JAR_NAME=${PROJECT}-${MINECRAFT_VERSION}-${BUILD_NUMBER}.jar
    	
    	echo "Version being downloaded"
    	echo -e "MC Version: ${MINECRAFT_VERSION}"
    	echo -e "Build: ${BUILD_NUMBER}"
    	echo -e "JAR Name of Build: ${JAR_NAME}"
    	DOWNLOAD_URL=https://papermc.io/api/v2/projects/${PROJECT}/versions/${MINECRAFT_VERSION}/builds/${BUILD_NUMBER}/downloads/${JAR_NAME}
    fi
    
    cd /mnt/server
    
    echo -e "Running curl -o ${SERVER_JARFILE} ${DOWNLOAD_URL}"
    
    if [ -f ${SERVER_JARFILE} ]; then
    	mv ${SERVER_JARFILE} ${SERVER_JARFILE}.old
    fi
    
    curl -o ${SERVER_JARFILE} ${DOWNLOAD_URL}
    
    if [ ! -f config.yml ]; then
    	echo -e "Downloading ${PROJECT} config.yml"
    	curl -o config.yml https://raw.githubusercontent.com/parkervcp/eggs/master/game_eggs/minecraft/proxy/java/waterfall/config.yml
    else
    	echo -e "${PROJECT} config.yml exists. Will not pull a new file"
    fi

elif [ "$(PROJECT)" == "bungeecord" ]; then
    cd /mnt/server
    
    if [ -z "${BUNGEE_VERSION}" ] || [ "${BUNGEE_VERSION}" == "latest" ]; then
        BUNGEE_VERSION="lastStableBuild"
    fi
    
    curl -o ${SERVER_JARFILE} https://ci.md-5.net/job/BungeeCord/${BUNGEE_VERSION}/artifact/bootstrap/target/BungeeCord.jar

elif [ "$(PROJECT)" == "folia" ]; then
    cd /mnt/server
    
    echo -e "Running curl -o ${SERVER_JARFILE} https://cloud.lamahost.de/s/7iSmXjm7SMxb2tk/download/folia-bundler-1.19.4-R0.1-SNAPSHOT-reobf.jar"
    
    curl -o ${SERVER_JARFILE} https://cloud.lamahost.de/s/7iSmXjm7SMxb2tk/download/folia-bundler-1.19.4-R0.1-SNAPSHOT-reobf.jar
    
    if [ ! -f server.properties ]; then
        echo -e "Downloading MC server.properties"
        curl -o server.properties https://raw.githubusercontent.com/parkervcp/eggs/master/minecraft/java/server.properties
    fi
elif [ "$(PROJECT)" == "paper" ]; then
    if [ -n "${DL_PATH}" ]; then
    	echo -e "Using supplied download url: ${DL_PATH}"
    	DOWNLOAD_URL=`eval echo $(echo ${DL_PATH} | sed -e 's/{{/${/g' -e 's/}}/}/g')`
    else
    	VER_EXISTS=`curl -s https://api.papermc.io/v2/projects/${PROJECT} | jq -r --arg VERSION $MINECRAFT_VERSION '.versions[] | contains($VERSION)' | grep -m1 true`
    	LATEST_VERSION=`curl -s https://api.papermc.io/v2/projects/${PROJECT} | jq -r '.versions' | jq -r '.[-1]'`
    
    	if [ "${VER_EXISTS}" == "true" ]; then
    		echo -e "Version is valid. Using version ${MINECRAFT_VERSION}"
    	else
    		echo -e "Specified version not found. Defaulting to the latest ${PROJECT} version"
    		MINECRAFT_VERSION=${LATEST_VERSION}
    	fi
    
    	BUILD_EXISTS=`curl -s https://api.papermc.io/v2/projects/${PROJECT}/versions/${MINECRAFT_VERSION} | jq -r --arg BUILD ${BUILD_NUMBER} '.builds[] | tostring | contains($BUILD)' | grep -m1 true`
    	LATEST_BUILD=`curl -s https://api.papermc.io/v2/projects/${PROJECT}/versions/${MINECRAFT_VERSION} | jq -r '.builds' | jq -r '.[-1]'`
    
    	if [ "${BUILD_EXISTS}" == "true" ]; then
    		echo -e "Build is valid for version ${MINECRAFT_VERSION}. Using build ${BUILD_NUMBER}"
    	else
    		echo -e "Using the latest ${PROJECT} build for version ${MINECRAFT_VERSION}"
    		BUILD_NUMBER=${LATEST_BUILD}
    	fi
    
    	JAR_NAME=${PROJECT}-${MINECRAFT_VERSION}-${BUILD_NUMBER}.jar
    
    	echo "Version being downloaded"
    	echo -e "MC Version: ${MINECRAFT_VERSION}"
    	echo -e "Build: ${BUILD_NUMBER}"
    	echo -e "JAR Name of Build: ${JAR_NAME}"
    	DOWNLOAD_URL=https://api.papermc.io/v2/projects/${PROJECT}/versions/${MINECRAFT_VERSION}/builds/${BUILD_NUMBER}/downloads/${JAR_NAME}
    fi
    
    cd /mnt/server
    
    echo -e "Running curl -o ${SERVER_JARFILE} ${DOWNLOAD_URL}"
    
    if [ -f ${SERVER_JARFILE} ]; then
    	mv ${SERVER_JARFILE} ${SERVER_JARFILE}.old
    fi
    
    curl -o ${SERVER_JARFILE} ${DOWNLOAD_URL}
    
    if [ ! -f server.properties ]; then
        echo -e "Downloading MC server.properties"
        curl -o server.properties https://raw.githubusercontent.com/parkervcp/eggs/master/minecraft/java/server.properties
    fi
else
    echo "Project Name not recognized, please contact Administrator"
fi