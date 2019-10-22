$(document).ready(function(){
    getPlaylists()
})

serverUrl = "http://<serverAddress>:3000/"

var sio = io()

sio.on("server-status", function(msg){
    console.log(msg)
})

sio.on("current-track", function(songName){
    $("#nowPlaying").text(songName)
})

sio.on("player-status", function(status){
    if(status == 0)
        $("#PlayPause").attr("class","fas fa-play-circle fa-3x")
    else if(status == 1)
        $("#PlayPause").attr("class","fas fa-pause-circle fa-3x")
    
})

sio.on("mute-status", function(muteStatus){
    if(muteStatus == false)
        $("#muted").attr("class","fas fa-volume-up fa-2x")
    else if (muteStatus == true)
        $("#muted").attr("class","fas fa-volume-off fa-2x")
})

sio.on("shuffle-status", function(shuffleStatus){
    if(shuffleStatus == true)
        $("#shuffle").css({ opacity: 1 })
    else if (shuffleStatus == false){
        $("#shuffle").css({ opacity: 0.5 })

    }
})

sio.on("update-art", function(data){
    $("#albumArt").attr("src","/img/now_playing.png?d="+(new Date()).getTime().toString())
})


function mute(){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/mute"
    })
}

function shuffle(){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/toggleshuffle"
    })
}

function setVolume(val){
    $.ajax({
        type: "PUT",
        url: serverUrl + "api/setvolume?value="+val
    })

}

function getPlaylists(){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/playlists",
        success: function(data){
            data["plists"].forEach(element => {
                $("#playlists").append("<li onclick=\"playPlaylist('"+element+"')\">"+element+"</li>")
            });
        }
    })
}

function playPause(){
    $.ajax({ 
        type:"GET", 
        url: serverUrl+"api/playpause"
    });
}

function next(){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/next"
    });
    
}

function prev(){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/prev"
    });
    
}

function search(){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/search?songname="+document.getElementById("searchQuery").value
    });
    
}

function playPlaylist(value){
    $.ajax({
        type: "GET",
        url: serverUrl + "api/playplaylist?playlistName=" + value
    })
}
